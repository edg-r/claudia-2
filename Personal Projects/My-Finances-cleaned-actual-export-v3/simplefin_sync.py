from __future__ import annotations

import base64
import json
import os
import shutil
import sqlite3
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import certifi
from finance_rules import apply_transfer_rules


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "db.sqlite"
ENV_FILES = (ROOT / ".env.local", ROOT / ".env")
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


@dataclass
class SyncResult:
    accounts_seen: int = 0
    accounts_updated: int = 0
    transactions_seen: int = 0
    transactions_inserted: int = 0
    transactions_skipped: int = 0
    backup_path: str | None = None
    message: str = ""

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    for path in ENV_FILES:
        if not path.exists():
            continue
        for raw_line in path.read_text().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def simplefin_access_url() -> str:
    url = os.environ.get("SIMPLEFIN_ACCESS_URL") or load_env().get("SIMPLEFIN_ACCESS_URL", "")
    if not url:
        raise RuntimeError("Missing SIMPLEFIN_ACCESS_URL. Put it in .env.local.")
    return url.rstrip("/")


def simplefin_setup_token() -> str:
    token = os.environ.get("SIMPLEFIN_SETUP_TOKEN") or load_env().get("SIMPLEFIN_SETUP_TOKEN", "")
    if not token:
        access_value = os.environ.get("SIMPLEFIN_ACCESS_URL") or load_env().get("SIMPLEFIN_ACCESS_URL", "")
        if access_value and not access_value.startswith(("http://", "https://")):
            token = access_value
    if not token:
        raise RuntimeError("Missing SIMPLEFIN_SETUP_TOKEN. Put it in .env.local only if you need to claim a setup token.")
    return token


def _money_to_cents(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(round(float(str(value)) * 100))
    except (TypeError, ValueError):
        return None


def _date_to_int(value: str | None) -> int | None:
    if not value:
        return None
    return int(value[:10].replace("-", ""))


def _request_json(url: str, method: str = "GET", body: bytes | None = None) -> dict[str, Any]:
    req = urllib.request.Request(url, data=body, method=method)
    with urllib.request.urlopen(req, timeout=60, context=SSL_CONTEXT) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload)


def _accounts_url(access_url: str, start_date: int | None = None) -> str:
    parsed = urllib.parse.urlparse(access_url)
    path = parsed.path.rstrip("/")
    if not path.endswith("/accounts"):
        path = f"{path}/accounts"
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    if start_date:
        query.append(("start-date", str(start_date)))
    return urllib.parse.urlunparse(parsed._replace(path=path, query=urllib.parse.urlencode(query)))


def _decode_if_base64_url(value: str) -> str:
    if value.startswith(("http://", "https://")):
        return value
    try:
        decoded = base64.b64decode(value).decode("utf-8").strip()
    except Exception:
        return value
    return decoded if decoded.startswith(("http://", "https://")) else value


def _persist_access_url(access_url: str) -> None:
    env_path = ROOT / ".env.local"
    lines = env_path.read_text().splitlines() if env_path.exists() else []
    seen = False
    output: list[str] = []
    for line in lines:
        if line.strip().startswith("SIMPLEFIN_ACCESS_URL="):
            output.append(f'SIMPLEFIN_ACCESS_URL="{access_url}"')
            seen = True
        elif line.strip().startswith("SIMPLEFIN_SETUP_TOKEN="):
            output.append('SIMPLEFIN_SETUP_TOKEN=""')
        else:
            output.append(line)
    if not seen:
        output.append(f'SIMPLEFIN_ACCESS_URL="{access_url}"')
    env_path.write_text("\n".join(output).rstrip() + "\n")


def claim_setup_token() -> str:
    token = simplefin_setup_token()
    claim_url = _decode_if_base64_url(token)
    url = claim_url if "/claim/" in claim_url else "https://bridge.simplefin.org/simplefin/setup-token"
    body = b"" if "/claim/" in claim_url else token.encode("utf-8")
    try:
        req = urllib.request.Request(url, data=body, method="POST")
        if "/claim/" in claim_url:
            req.add_header("Content-Length", "0")
        response = urllib.request.urlopen(req, timeout=60, context=SSL_CONTEXT)
        data = response.read().decode("utf-8").strip()
    except urllib.error.HTTPError as exc:
        if exc.code == 403 and "/claim/" in claim_url:
            raise RuntimeError(
                "SimpleFIN rejected this one-time app connection token with HTTP 403. "
                "Generate a fresh SimpleFIN app connection token and paste it into .env.local; "
                "the app will claim it once and replace it with the saved access URL."
            ) from exc
        raise RuntimeError(f"SimpleFIN setup-token claim failed: HTTP {exc.code} {exc.reason}") from exc
    try:
        access_url = base64.b64decode(data).decode("utf-8")
    except Exception:
        access_url = data
    if access_url.startswith(("http://", "https://")):
        _persist_access_url(access_url)
    return access_url


def _ensure_payee(conn: sqlite3.Connection, name: str | None) -> str:
    clean = (name or "Imported Transaction").strip() or "Imported Transaction"
    row = conn.execute(
        "select p.id from payees p where lower(p.name)=lower(?) and ifnull(p.tombstone,0)=0 limit 1",
        (clean,),
    ).fetchone()
    if row:
        return row[0]
    payee_id = str(uuid.uuid4())
    conn.execute("insert into payees (id, name, tombstone) values (?, ?, 0)", (payee_id, clean))
    conn.execute("insert into payee_mapping (id, targetId) values (?, ?)", (payee_id, payee_id))
    return payee_id


def _latest_transaction_unix(conn: sqlite3.Connection) -> int | None:
    row = conn.execute("select max(date) from transactions where ifnull(tombstone,0)=0 and date is not null").fetchone()
    if not row or not row[0]:
        return None
    date_text = str(row[0])
    parsed = time.strptime(date_text, "%Y%m%d")
    return int(time.mktime(parsed))


def sync_simplefin(db_path: Path = DB_PATH) -> SyncResult:
    result = SyncResult()
    access_url = simplefin_access_url()
    if not access_url.startswith(("http://", "https://")):
        access_url = claim_setup_token()
    backup = db_path.with_suffix(f".{time.strftime('%Y%m%d-%H%M%S')}.bak")
    shutil.copy2(db_path, backup)
    result.backup_path = str(backup)

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        start_date = _latest_transaction_unix(conn)
        payload = _request_json(_accounts_url(access_url, start_date=start_date))
        accounts = payload.get("accounts", [])
        result.accounts_seen = len(accounts)

        account_map = {
            row["account_id"]: dict(row)
            for row in conn.execute("select * from accounts where ifnull(tombstone,0)=0")
        }
        existing_financial_ids = {
            row[0]
            for row in conn.execute(
                "select financial_id from transactions where financial_id is not null and ifnull(tombstone,0)=0"
            )
        }

        for account in accounts:
            simplefin_id = account.get("id")
            if not simplefin_id or simplefin_id not in account_map:
                continue
            acct = account_map[simplefin_id]
            balance = _money_to_cents(account.get("balance"))
            available = _money_to_cents(account.get("available-balance"))
            last_sync_ms = int(time.time() * 1000)
            conn.execute(
                """
                update accounts
                   set balance_current = coalesce(?, balance_current),
                       balance_available = coalesce(?, balance_available),
                       last_sync = ?
                 where id = ?
                """,
                (balance, available, str(last_sync_ms), acct["id"]),
            )
            result.accounts_updated += 1

            for tx in account.get("transactions", []):
                result.transactions_seen += 1
                tx_id = tx.get("id") or tx.get("transaction-id")
                if not tx_id or tx_id in existing_financial_ids:
                    result.transactions_skipped += 1
                    continue
                posted = tx.get("posted") or tx.get("date") or tx.get("transacted_at")
                date_int = _date_to_int(posted)
                amount = _money_to_cents(tx.get("amount"))
                if date_int is None or amount is None:
                    result.transactions_skipped += 1
                    continue
                payee_name = tx.get("description") or tx.get("payee") or tx.get("memo")
                payee_id = _ensure_payee(conn, payee_name)
                raw = {
                    "booked": True,
                    "date": str(posted)[:10],
                    "payeeName": payee_name,
                    "notes": tx.get("memo") or payee_name,
                    "transactionAmount": {"amount": str(tx.get("amount")), "currency": account.get("currency", "USD")},
                    "transactionId": tx_id,
                    "postedDate": str(posted)[:10],
                    "cleared": True,
                    "amount": str(tx.get("amount")),
                    "imported_payee": payee_name,
                    "account": acct["id"],
                    "payee": payee_id,
                }
                conn.execute(
                    """
                    insert into transactions (
                        id, acct, amount, description, date, financial_id, imported_description,
                        sort_order, tombstone, cleared, pending, reconciled, raw_synced_data
                    ) values (?, ?, ?, ?, ?, ?, ?, ?, 0, 1, 0, 0, ?)
                    """,
                    (
                        str(uuid.uuid4()),
                        acct["id"],
                        amount,
                        payee_id,
                        date_int,
                        tx_id,
                        payee_name,
                        int(time.time()),
                        json.dumps(raw, separators=(",", ":")),
                    ),
                )
                existing_financial_ids.add(tx_id)
                result.transactions_inserted += 1

        rules = apply_transfer_rules(conn)
        conn.commit()

    result.message = (
        f"Sync complete. Deterministic rules linked {rules['transfer_pairs_linked']} transfer pairs."
    )
    return result
