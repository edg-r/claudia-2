from __future__ import annotations

import shutil
import sqlite3
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "db.sqlite"


TRANSFER_KEYWORDS = (
    "capital one",
    "deposit from",
    "withdrawal to",
    "payment",
    "paycheck percentage transfer",
    "transfer",
)


def _transfer_payees(conn: sqlite3.Connection) -> dict[str, str]:
    return {
        row["transfer_acct"]: row["id"]
        for row in conn.execute("select id, transfer_acct from payees where transfer_acct is not null")
    }


def _looks_like_transfer(row: sqlite3.Row) -> bool:
    text = " ".join(
        str(row[key] or "").lower()
        for key in ("imported_description", "notes", "raw_synced_data")
        if key in row.keys()
    )
    return any(keyword in text for keyword in TRANSFER_KEYWORDS)


def _date_distance(left: int | str, right: int | str) -> int:
    left_date = datetime.strptime(str(left), "%Y%m%d")
    right_date = datetime.strptime(str(right), "%Y%m%d")
    return abs((left_date - right_date).days)


def apply_transfer_rules(conn: sqlite3.Connection) -> dict[str, int]:
    transfer_payees = _transfer_payees(conn)
    rows = conn.execute(
        """
        select id, date, acct, amount, imported_description, notes, raw_synced_data
        from transactions
        where ifnull(tombstone,0)=0
          and transferred_id is null
          and ifnull(starting_balance_flag,0)=0
          and amount != 0
        order by date desc
        """
    ).fetchall()

    used: set[str] = set()
    linked = 0
    for left in rows:
        if left["id"] in used or not _looks_like_transfer(left):
            continue
        for right in rows:
            if right["id"] in used or right["id"] == left["id"]:
                continue
            if left["acct"] == right["acct"]:
                continue
            if left["amount"] + right["amount"] != 0:
                continue
            if _date_distance(left["date"], right["date"]) > 3:
                continue
            if not (_looks_like_transfer(right) or left["imported_description"] == right["imported_description"]):
                continue
            left_payee = transfer_payees.get(right["acct"])
            right_payee = transfer_payees.get(left["acct"])
            if not left_payee or not right_payee:
                continue
            conn.execute(
                "update transactions set transferred_id=?, description=?, category=null where id=?",
                (right["id"], left_payee, left["id"]),
            )
            conn.execute(
                "update transactions set transferred_id=?, description=?, category=null where id=?",
                (left["id"], right_payee, right["id"]),
            )
            used.add(left["id"])
            used.add(right["id"])
            linked += 1
            break

    return {"transfer_pairs_linked": linked, "transactions_updated": linked * 2}


def apply_rules(db_path: Path = DB_PATH, backup: bool = True) -> dict[str, str | int | None]:
    backup_path = None
    if backup:
        backup_path = db_path.with_suffix(f".rules-{time.strftime('%Y%m%d-%H%M%S')}.bak")
        shutil.copy2(db_path, backup_path)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        result = apply_transfer_rules(conn)
        conn.commit()
    return {**result, "backup_path": str(backup_path) if backup_path else None}


if __name__ == "__main__":
    print(apply_rules())
