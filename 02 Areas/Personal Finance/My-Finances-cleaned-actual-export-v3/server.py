from __future__ import annotations

import json
import sqlite3
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from simplefin_sync import DB_PATH, claim_setup_token, sync_simplefin
from finance_rules import apply_rules


ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
HOST = "127.0.0.1"
PORT = 8787


BUDGET_GROUP_MAP = {
    "Food": "Food & Drink",
    "Shopping": "Shopping Detail",
    "UCSD": "School & UCSD",
    "Bills": "Bills & Services",
    "Bills (Flexible)": "Bills & Services",
    "General": "Shopping Detail",
}


def cents(value: int | float | None) -> float:
    return round((value or 0) / 100, 2)


def date_label(value: int | str | None) -> str:
    if not value:
        return ""
    text = str(value)
    return f"{text[0:4]}-{text[4:6]}-{text[6:8]}"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def month_label(month: str | int | None) -> str:
    text = str(month or "")
    return f"{text[0:4]}-{text[4:6]}" if len(text) == 6 else text


def get_summary(selected_month: str | None = None) -> dict:
    with connect() as conn:
        accounts = [
            {
                "id": row["id"],
                "name": row["name"],
                "balance": cents(row["balance_current"]),
                "available": cents(row["balance_available"]),
                "type": row["type"] or row["subtype"] or "Account",
                "syncSource": row["account_sync_source"] or "local",
                "lastSync": time.strftime("%Y-%m-%d %H:%M", time.localtime(int(row["last_sync"]) / 1000))
                if row["last_sync"]
                else "",
            }
            for row in conn.execute(
                """
                select id, name, balance_current, balance_available, type, subtype, account_sync_source, last_sync
                from accounts
                where ifnull(tombstone,0)=0 and ifnull(closed,0)=0 and ifnull(offbudget,0)=0
                order by balance_current desc
                """
            )
        ]
        total_balance = sum(account["balance"] for account in accounts)
        cash_balance = sum(account["balance"] for account in accounts if account["balance"] > 0)
        debt_balance = sum(account["balance"] for account in accounts if account["balance"] < 0)

        range_row = conn.execute(
            "select min(date) as min_date, max(date) as max_date from transactions where ifnull(tombstone,0)=0"
        ).fetchone()
        current_month = str(range_row["max_date"])[0:6] if range_row and range_row["max_date"] else ""

        month_rows = conn.execute(
            """
            select substr(date,1,4) || '-' || substr(date,5,2) as month,
                   count(*) as tx_count,
                   sum(case when amount > 0 and transferred_id is null then amount else 0 end) as inflow,
                   sum(case when amount < 0 and transferred_id is null then -amount else 0 end) as outflow,
                   sum(case when transferred_id is null then amount else 0 end) as net
            from transactions
            where ifnull(tombstone,0)=0 and ifnull(starting_balance_flag,0)=0
            group by month
            order by month
            """
        ).fetchall()
        monthly = [
            {
                "month": row["month"],
                "txCount": row["tx_count"],
                "inflow": cents(row["inflow"]),
                "outflow": cents(row["outflow"]),
                "net": cents(row["net"]),
            }
            for row in month_rows
        ]
        latest_month_key = monthly[-1]["month"].replace("-", "") if monthly else ""
        current_month = (selected_month or latest_month_key).replace("-", "")
        latest_month = next(
            (row for row in monthly if row["month"].replace("-", "") == current_month),
            {"month": month_label(current_month), "inflow": 0, "outflow": 0, "net": 0, "txCount": 0},
        )

        category_rows = conn.execute(
            """
            select coalesce(c.id, 'uncategorized') as category_id,
                   coalesce(cg.id, 'uncategorized') as group_id,
                   coalesce(cg.name, 'Uncategorized') as group_name,
                   coalesce(c.name, 'Uncategorized') as category,
                   count(*) as tx_count,
                   sum(case when t.amount < 0 then -t.amount else 0 end) as spending
            from transactions t
            left join categories c on c.id = t.category
            left join category_groups cg on cg.id = c.cat_group
            where ifnull(t.tombstone,0)=0
              and ifnull(t.starting_balance_flag,0)=0
              and t.transferred_id is null
              and t.amount < 0
              and substr(t.date,1,6)=?
            group by coalesce(c.id, 'uncategorized')
            order by spending desc
            """,
            (current_month,),
        ).fetchall()
        categories = [
            {
                "id": row["category_id"],
                "groupId": row["group_id"],
                "group": row["group_name"],
                "category": row["category"],
                "txCount": row["tx_count"],
                "spending": cents(row["spending"]),
            }
            for row in category_rows
        ]

        group_rows = conn.execute(
            """
            select coalesce(cg.id, 'uncategorized') as group_id,
                   coalesce(cg.name, 'Uncategorized') as group_name,
                   count(*) as tx_count,
                   sum(case when t.amount < 0 then -t.amount else 0 end) as spending
            from transactions t
            left join categories c on c.id = t.category
            left join category_groups cg on cg.id = c.cat_group
            where ifnull(t.tombstone,0)=0
              and ifnull(t.starting_balance_flag,0)=0
              and t.transferred_id is null
              and t.amount < 0
              and substr(t.date,1,6)=?
            group by group_id
            order by spending desc
            """,
            (current_month,),
        ).fetchall()
        groups = [
            {
                "id": row["group_id"],
                "group": row["group_name"],
                "txCount": row["tx_count"],
                "spending": cents(row["spending"]),
            }
            for row in group_rows
        ]

        recent_rows = conn.execute(
            """
            select t.date, a.name as account, coalesce(p.name, t.imported_description, 'Imported Transaction') as payee,
                   case when t.transferred_id is not null then 'Transfer' else coalesce(c.name, 'Uncategorized') end as category,
                   case when t.transferred_id is not null then 'Transfers' else coalesce(cg.name, 'Uncategorized') end as group_name,
                   t.amount
            from transactions t
            left join accounts a on a.id = t.acct
            left join payees p on p.id = t.description
            left join categories c on c.id = t.category
            left join category_groups cg on cg.id = c.cat_group
            where ifnull(t.tombstone,0)=0
              and ifnull(t.starting_balance_flag,0)=0
              and substr(t.date,1,6)=?
            order by t.date desc, t.sort_order desc
            """,
            (current_month,),
        ).fetchall()
        recent = [
            {
                "date": date_label(row["date"]),
                "account": row["account"],
                "payee": row["payee"],
                "category": row["category"],
                "group": row["group_name"],
                "amount": cents(row["amount"]),
            }
            for row in recent_rows
        ]

        account_transaction_rows = conn.execute(
            """
            select t.date, t.acct as account_id, a.name as account,
                   coalesce(p.name, t.imported_description, 'Imported Transaction') as payee,
                   case when t.transferred_id is not null then 'Transfer' else coalesce(c.name, 'Uncategorized') end as category,
                   case when t.transferred_id is not null then 'Transfers' else coalesce(cg.name, 'Uncategorized') end as group_name,
                   t.amount
            from transactions t
            left join accounts a on a.id = t.acct
            left join payees p on p.id = t.description
            left join categories c on c.id = t.category
            left join category_groups cg on cg.id = c.cat_group
            where ifnull(t.tombstone,0)=0
              and ifnull(t.starting_balance_flag,0)=0
            order by t.date desc, t.sort_order desc
            """
        ).fetchall()
        account_transactions = [
            {
                "date": date_label(row["date"]),
                "accountId": row["account_id"],
                "account": row["account"],
                "payee": row["payee"],
                "category": row["category"],
                "group": row["group_name"],
                "amount": cents(row["amount"]),
            }
            for row in account_transaction_rows
        ]

        budget_rows = conn.execute(
            """
            select c.name as budget_category, zb.amount as budgeted,
                   coalesce(sum(case when t.amount < 0 then -t.amount else 0 end), 0) as spent
            from zero_budgets zb
            join categories c on c.id = zb.category
            left join transactions t
              on t.category = c.id and substr(t.date,1,6) = cast(zb.month as text) and ifnull(t.tombstone,0)=0
             and t.transferred_id is null
            where cast(zb.month as text)=? and zb.amount > 0
            group by c.id
            order by spent desc
            limit 10
            """,
            (current_month,),
        ).fetchall()
        budgeted_by_group: dict[str, int] = {}
        for row in budget_rows:
            group_name = BUDGET_GROUP_MAP.get(row["budget_category"], row["budget_category"])
            budgeted_by_group[group_name] = budgeted_by_group.get(group_name, 0) + (row["budgeted"] or 0)

        spent_by_group = {row["group"]: row["spending"] for row in groups}
        categories_by_group: dict[str, list[dict]] = {}
        for category in categories:
            categories_by_group.setdefault(category["group"], []).append(category)

        budget_names = sorted(
            set(budgeted_by_group) | set(spent_by_group),
            key=lambda name: max(budgeted_by_group.get(name, 0) / 100, spent_by_group.get(name, 0)),
            reverse=True,
        )
        budgets = []
        for name in budget_names:
            budgeted = cents(budgeted_by_group.get(name, 0))
            spent = spent_by_group.get(name, 0)
            budgets.append(
                {
                    "group": name,
                    "budgeted": budgeted,
                    "spent": spent,
                    "remaining": round(budgeted - spent, 2),
                    "percent": round((spent / budgeted) * 100, 1) if budgeted else None,
                    "categories": categories_by_group.get(name, []),
                }
            )

    return {
        "asOf": time.strftime("%Y-%m-%d %H:%M"),
        "dateRange": {
            "start": date_label(range_row["min_date"] if range_row else None),
            "end": date_label(range_row["max_date"] if range_row else None),
        },
        "currentMonth": f"{current_month[0:4]}-{current_month[4:6]}" if current_month else "",
        "netWorth": round(total_balance, 2),
        "cashBalance": round(cash_balance, 2),
        "debtBalance": round(debt_balance, 2),
        "latestMonth": latest_month,
        "accounts": accounts,
        "monthly": monthly[-8:],
        "availableMonths": [row["month"] for row in monthly],
        "groups": groups,
        "categories": categories,
        "recent": recent,
        "accountTransactions": account_transactions,
        "budgets": budgets,
    }


class Handler(BaseHTTPRequestHandler):
    def _serve_path(self, body: bytes, content_type: str, include_body: bool = True) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if include_body:
            self.wfile.write(body)

    def send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        if path in ("/", "/dashboard.html"):
            body = (ROOT / "dashboard.html").read_bytes()
            self._serve_path(body, "text/html; charset=utf-8")
        elif path == "/api/summary":
            self.send_json(get_summary(query.get("month", [None])[0]))
        elif path.startswith("/static/"):
            file_path = STATIC / path.removeprefix("/static/")
            if not file_path.exists():
                self.send_error(404)
                return
            content_type = "text/css" if file_path.suffix == ".css" else "application/javascript"
            body = file_path.read_bytes()
            self._serve_path(body, content_type)
        else:
            self.send_error(404)

    def do_HEAD(self) -> None:
        path = urlparse(self.path).path
        if path in ("/", "/dashboard.html"):
            self._serve_path((ROOT / "dashboard.html").read_bytes(), "text/html; charset=utf-8", include_body=False)
        elif path.startswith("/static/"):
            file_path = STATIC / path.removeprefix("/static/")
            if not file_path.exists():
                self.send_error(404)
                return
            content_type = "text/css" if file_path.suffix == ".css" else "application/javascript"
            self._serve_path(file_path.read_bytes(), content_type, include_body=False)
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            if path == "/api/sync":
                self.send_json(sync_simplefin().as_dict())
            elif path == "/api/claim-setup-token":
                access_url = claim_setup_token()
                self.send_json({
                    "message": "Setup token claimed and access URL saved to .env.local.",
                    "saved": access_url.startswith(("http://", "https://")),
                })
            elif path == "/api/apply-rules":
                self.send_json(apply_rules())
            else:
                self.send_error(404)
        except Exception as exc:
            self.send_json({"error": str(exc)}, status=500)


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Finance dashboard: http://{HOST}:{PORT}")
    server.serve_forever()
