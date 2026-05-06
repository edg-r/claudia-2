#!/usr/bin/env python3
"""
Claudia Dashboard Generator
Generates a static HTML dashboard from the Claudia SQLite database.

Usage:
    python3 dashboard.py
"""

import json
import re
import sqlite3
from datetime import date, datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "claudia.db"
OUTPUT_PATH = SCRIPT_DIR / "dashboard.html"
DISPATCH_DIR = SCRIPT_DIR / "dispatches"

QUARTER_START = date(2026, 3, 30)
TOTAL_WEEKS = 11
ASSIGNMENT_OPTIONAL_COLUMNS = [
    "due_time",
    "timezone",
    "deadline_source",
    "source_path",
    "source_confidence",
    "date_kind",
    "is_recurring",
    "recurrence_rule",
    "opens_at",
    "submitted_at",
    "last_verified_at",
    "external_id",
]

COURSE_COLORS = {
    "GPCO 403": "#006fba",
    "GPCO 410": "#f2a000",
    "GPEC 446": "#6b45a4",
    "GPPS 444": "#ef3e33",
    "GPPS 463": "#4b9f38",
}

DISPATCH_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})_daily-briefing\.md$")
DISPATCH_SIGNAL_SECTIONS = [
    {"title": "Weather", "starts": ("Weather",)},
    {"title": "Personal Gmail", "starts": ("Personal Gmail",)},
    {"title": "UCSD Email", "starts": ("UCSD Email",)},
    {"title": "Delegation Suggestions", "starts": ("Delegation Suggestions",)},
]


def query_db(conn, sql, params=()):
    return conn.execute(sql, params).fetchall()


def get_week_number(due_date_str):
    if not due_date_str:
        return None
    try:
        due = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError:
        return None
    delta = (due - QUARTER_START).days
    if delta < 0:
        return 0
    return delta // 7 + 1


def get_current_week(today_date):
    delta = (today_date - QUARTER_START).days
    if delta < 0:
        return 0
    return min(delta // 7 + 1, TOTAL_WEEKS)


def table_columns(conn, table_name):
    return {row["name"] for row in conn.execute(f"PRAGMA table_info({table_name})")}


def row_value(row, columns, key, default=""):
    if key not in columns:
        return default
    value = row[key]
    return value if value is not None else default


def parse_frontmatter_and_body(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, text[end + 5 :]


def markdown_heading_title(body):
    for line in body.splitlines():
        if line.startswith("## "):
            return line[3:].strip()
    return ""


def dispatch_signal_sections(body):
    sections = {}
    current_title = None
    current_display_title = None
    current_lines = []

    def save_current():
        if current_display_title:
            cleaned = "\n".join(current_lines).strip()
            sections[current_display_title] = cleaned

    def display_title_for(heading):
        normalized = heading.strip().lower()
        for signal in DISPATCH_SIGNAL_SECTIONS:
            if any(normalized.startswith(prefix.lower()) for prefix in signal["starts"]):
                return signal["title"]
        return None

    for line in body.splitlines():
        if line.startswith("### "):
            save_current()
            current_title = line[4:].strip()
            current_display_title = display_title_for(current_title)
            current_lines = []
        elif line.startswith("## "):
            save_current()
            current_title = None
            current_display_title = None
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)
    save_current()

    return [
        {"title": signal["title"], "content": sections.get(signal["title"], "")}
        for signal in DISPATCH_SIGNAL_SECTIONS
    ]


def latest_daily_dispatch(today_date):
    if not DISPATCH_DIR.exists():
        return {
            "present": False,
            "status": "missing",
            "message": "No dispatch directory found.",
        }

    dispatches = []
    for path in DISPATCH_DIR.iterdir():
        match = DISPATCH_PATTERN.match(path.name)
        if not match:
            continue
        try:
            dispatch_date = datetime.strptime(match.group(1), "%Y-%m-%d").date()
        except ValueError:
            continue
        dispatches.append((dispatch_date, path))

    if not dispatches:
        return {
            "present": False,
            "status": "missing",
            "message": "No daily briefing dispatch files found.",
        }

    dispatch_date, path = max(dispatches, key=lambda item: item[0])
    raw = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter_and_body(raw)
    delta_days = (today_date - dispatch_date).days
    if delta_days == 0:
        freshness = "current"
        label = "today"
    elif delta_days > 0:
        freshness = "stale"
        label = f"{delta_days} day{'s' if delta_days != 1 else ''} old"
    else:
        freshness = "future"
        label = f"{abs(delta_days)} day{'s' if delta_days != -1 else ''} ahead"

    return {
        "present": True,
        "status": freshness,
        "freshness_label": label,
        "is_today": delta_days == 0,
        "days_from_today": delta_days,
        "date": dispatch_date.isoformat(),
        "path": str(path.relative_to(SCRIPT_DIR.parent)),
        "filename": path.name,
        "title": markdown_heading_title(body),
        "metadata": {
            "dispatch": meta.get("dispatch", ""),
            "date": meta.get("date", dispatch_date.isoformat()),
            "generated": meta.get("generated", ""),
            "skill": meta.get("skill", ""),
        },
        "signals": dispatch_signal_sections(body),
    }


def get_dashboard_payload():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    now = datetime.now()
    today_date = now.date()
    current_week = get_current_week(today_date)

    courses = query_db(conn, "SELECT * FROM courses ORDER BY code")
    total_files = query_db(conn, "SELECT COUNT(*) AS n FROM files")[0]["n"]
    total_readings = query_db(conn, "SELECT COUNT(*) AS n FROM readings")[0]["n"]
    pending_readings = query_db(
        conn, "SELECT COUNT(*) AS n FROM readings WHERE summary_status = 'pending'"
    )[0]["n"]
    summarized_readings = total_readings - pending_readings
    total_assignments = query_db(conn, "SELECT COUNT(*) AS n FROM assignments")[0]["n"]
    completed_assignments = query_db(
        conn,
        "SELECT COUNT(*) AS n FROM assignments WHERE lower(coalesce(status, '')) IN ('completed', 'submitted')",
    )[0]["n"]
    upcoming_assignments = total_assignments - completed_assignments
    total_embeddings = query_db(conn, "SELECT COUNT(*) AS n FROM embeddings")[0]["n"]
    total_embedded_files = query_db(
        conn, "SELECT COUNT(DISTINCT source_path) AS n FROM embeddings"
    )[0]["n"]
    total_pages_all = query_db(
        conn, "SELECT COALESCE(SUM(pages), 0) AS n FROM readings"
    )[0]["n"]

    assignment_columns = table_columns(conn, "assignments")
    optional_selects = [
        f"a.{col}" for col in ASSIGNMENT_OPTIONAL_COLUMNS if col in assignment_columns
    ]
    optional_select_sql = ", " + ", ".join(optional_selects) if optional_selects else ""
    assignments = query_db(
        conn,
        f"""
        SELECT a.id, a.title, a.due_date, a.status, a.grade, a.weight, a.notes{optional_select_sql},
               c.code, c.name AS course_name
        FROM assignments a
        LEFT JOIN courses c ON a.course_id = c.id
        ORDER BY a.due_date, a.due_time, c.code, a.title
        """,
    )
    readings = query_db(
        conn,
        """
        SELECT r.id, r.title, r.authors, r.week, r.summary_status, r.pages,
               r.file_path, r.summary_path, c.code, c.name AS course_name
        FROM readings r
        LEFT JOIN courses c ON r.course_id = c.id
        ORDER BY r.week, c.code, r.title
        """,
    )

    assignments_json = []
    for row in assignments:
        status = row["status"] or "pending"
        is_recurring = row_value(row, assignment_columns, "is_recurring", None)
        if is_recurring is None:
            is_recurring = status == "recurring" or not row["due_date"]
        assignments_json.append(
            {
                "id": row["id"],
                "title": row["title"],
                "due_date": row["due_date"] or "",
                "status": status,
                "grade": row["grade"] or "",
                "weight": row["weight"] or "",
                "notes": row["notes"] or "",
                "course": row["code"] or "",
                "course_name": row["course_name"] or "",
                "week": get_week_number(row["due_date"]),
                "due_time": row_value(row, assignment_columns, "due_time"),
                "timezone": row_value(row, assignment_columns, "timezone"),
                "deadline_source": row_value(row, assignment_columns, "deadline_source"),
                "source_path": row_value(row, assignment_columns, "source_path"),
                "source_confidence": row_value(row, assignment_columns, "source_confidence"),
                "date_kind": row_value(row, assignment_columns, "date_kind"),
                "is_recurring": bool(is_recurring),
                "recurrence_rule": row_value(row, assignment_columns, "recurrence_rule"),
                "opens_at": row_value(row, assignment_columns, "opens_at"),
                "submitted_at": row_value(row, assignment_columns, "submitted_at"),
                "last_verified_at": row_value(row, assignment_columns, "last_verified_at"),
                "external_id": row_value(row, assignment_columns, "external_id"),
            }
        )

    logs = query_db(
        conn,
        """
        SELECT agent, action, details, timestamp
        FROM agent_logs
        ORDER BY timestamp DESC
        LIMIT 20
        """,
    )
    conn.close()

    return {
        "generated_at": now.isoformat(timespec="seconds"),
        "generated_label": now.strftime("%Y-%m-%d %H:%M"),
        "today": today_date.isoformat(),
        "term": "Spring 2026",
        "program": "GPS",
        "current_week": current_week,
        "total_weeks": TOTAL_WEEKS,
        "cards": {
            "courses": len(courses),
            "files": total_files,
            "readings": total_readings,
            "pending_readings": pending_readings,
            "summarized_readings": summarized_readings,
            "assignments": total_assignments,
            "upcoming_assignments": upcoming_assignments,
            "completed_assignments": completed_assignments,
            "chunks": total_embeddings,
            "indexed_files": total_embedded_files,
            "pages": total_pages_all,
        },
        "course_colors": COURSE_COLORS,
        "courses": [dict(row) for row in courses],
        "readings": [dict(row) for row in readings],
        "assignments": assignments_json,
        "recent_activity": [dict(row) for row in logs],
        "dispatch": latest_daily_dispatch(today_date),
        "db_mtime": DB_PATH.stat().st_mtime if DB_PATH.exists() else None,
        "html_mtime": OUTPUT_PATH.stat().st_mtime if OUTPUT_PATH.exists() else None,
    }


def generate_dashboard():
    payload = get_dashboard_payload()
    payload_json = json.dumps(payload, ensure_ascii=False)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Claudia Dashboard</title>
  <style>
    :root {{
      --ink: #151512;
      --soft-ink: #484842;
      --muted: #77766d;
      --line: #d5d1c6;
      --field: #fbfaf4;
      --paper: #f4f1e7;
      --white: #fffefa;
      --blue: #006fba;
      --orange: #f2a000;
      --red: #ef3e33;
      --violet: #6b45a4;
      --green: #4b9f38;
    }}

    * {{ box-sizing: border-box; }}
    html {{ background: var(--field); }}
    body {{
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      font-family: "Avenir Next", "Helvetica Neue", Helvetica, system-ui, sans-serif;
      letter-spacing: 0;
      background: #e9e8df;
    }}
    button {{ font: inherit; }}
    h1, h2, h3, p {{ margin: 0; }}
    h1 {{
      font-size: clamp(48px, 8vw, 116px);
      line-height: 0.86;
      font-weight: 950;
      letter-spacing: 0;
    }}
    h2 {{ font-size: 20px; line-height: 1.04; font-weight: 900; }}

    .page {{
      width: min(1480px, calc(100vw - 40px));
      margin: 0 auto;
      padding: 24px 0 44px;
    }}
    .manual-page {{
      min-height: calc(100vh - 48px);
      border: 2px solid var(--ink);
      border-radius: 4px;
      background:
        linear-gradient(90deg, transparent 0 84px, rgba(21,21,18,0.08) 84px 85px, transparent 85px),
        var(--field);
      padding: 14px 18px 18px 108px;
      position: relative;
      overflow: hidden;
    }}
    .manual-page:before,
    .manual-page:after {{
      content: "";
      position: absolute;
      left: 34px;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: var(--ink);
    }}
    .manual-page:before {{ top: 34%; }}
    .manual-page:after {{ bottom: 24%; }}
    .manual-head {{
      display: grid;
      grid-template-columns: 0.8fr 1fr auto;
      gap: 20px;
      border-top: 2px solid var(--ink);
      border-bottom: 1px solid var(--ink);
      padding: 8px 0 7px;
      margin-bottom: 34px;
      font-size: 12px;
      font-weight: 800;
    }}
    .live-status {{
      border: 1px solid var(--line);
      border-radius: 6px;
      background: rgba(255, 254, 250, 0.75);
      min-height: 27px;
      padding: 4px 8px;
      text-align: center;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .live-status.connected {{ color: var(--green); }}
    .live-status.refreshing {{ color: var(--orange); }}

    .manual-layout {{
      display: grid;
      grid-template-columns: 275px 1fr;
      gap: 52px;
    }}
    .manual-copy {{
      display: grid;
      align-content: start;
      gap: 22px;
    }}
    .manual-copy p {{
      max-width: 260px;
      color: var(--soft-ink);
      font-size: 14px;
      line-height: 1.32;
      font-weight: 650;
    }}
    .label {{
      color: var(--soft-ink);
      font-size: 12px;
      line-height: 1.4;
      font-weight: 900;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }}
    .source-strip {{
      border-top: 2px solid var(--ink);
      border-bottom: 1px solid var(--line);
      display: grid;
      gap: 7px;
      padding: 9px 0 10px;
      max-width: 260px;
    }}
    .source-strip div {{
      display: grid;
      grid-template-columns: 84px 1fr;
      gap: 14px;
      color: var(--soft-ink);
      font-size: 12px;
      line-height: 1.2;
      font-weight: 750;
    }}
    .source-strip b {{
      color: var(--ink);
      font-weight: 950;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .dispatch-panel {{
      border-top: 2px solid var(--ink);
      display: grid;
      gap: 10px;
      max-width: 260px;
      padding-top: 10px;
    }}
    .dispatch-meta {{
      align-items: center;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .dispatch-freshness {{
      border: 1px solid var(--line);
      border-radius: 4px;
      color: var(--soft-ink);
      font-size: 10px;
      font-weight: 950;
      letter-spacing: 0.04em;
      padding: 3px 6px;
      text-transform: uppercase;
    }}
    .dispatch-freshness.current {{
      border-color: var(--green);
      color: var(--green);
    }}
    .dispatch-freshness.stale,
    .dispatch-freshness.future {{
      border-color: var(--red);
      color: var(--red);
    }}
    .dispatch-title {{
      color: var(--ink);
      font-size: 12px;
      font-weight: 900;
      line-height: 1.22;
    }}
    .dispatch-subtitle {{
      color: var(--muted);
      font-size: 11px;
      font-weight: 750;
      line-height: 1.25;
      overflow-wrap: anywhere;
    }}
    .dispatch-section {{
      border-top: 1px solid var(--line);
      display: grid;
      gap: 5px;
      padding-top: 8px;
    }}
    .dispatch-section h3 {{
      color: var(--red);
      font-size: 11px;
      font-weight: 950;
      letter-spacing: 0.04em;
      line-height: 1.2;
      text-transform: uppercase;
    }}
    .dispatch-section ul {{
      display: grid;
      gap: 5px;
      list-style: none;
      margin: 0;
      padding: 0;
    }}
    .dispatch-section li {{
      color: var(--soft-ink);
      font-size: 11px;
      font-weight: 700;
      line-height: 1.25;
    }}
    .dispatch-section li:before {{
      content: "";
      display: inline-block;
      width: 5px;
      height: 5px;
      margin: 0 6px 1px 0;
      background: var(--ink);
    }}
    .course-tag {{
      display: inline-flex;
      align-items: center;
      min-height: 23px;
      padding: 3px 7px;
      border-radius: 5px;
      color: #fff;
      font-size: 11px;
      font-weight: 950;
      letter-spacing: 0.02em;
    }}

    .program-grid {{
      display: grid;
      grid-template-columns: repeat(5, minmax(120px, 1fr));
      gap: 16px;
      align-items: end;
    }}
    .program {{
      appearance: none;
      border: 1px solid var(--line);
      border-radius: 4px;
      color: inherit;
      cursor: pointer;
      min-height: 410px;
      background: var(--white);
      display: grid;
      grid-template-rows: auto 1fr 118px;
      padding: 0;
      text-align: left;
      overflow: hidden;
      transition: transform 240ms ease, box-shadow 240ms ease, border-color 240ms ease;
    }}
    .program:hover,
    .program:focus-visible,
    .program[aria-expanded="true"] {{
      border-color: var(--ink);
      box-shadow: 0 14px 34px rgba(21, 21, 18, 0.14);
      outline: none;
      transform: translateY(-4px);
    }}
    .program[aria-expanded="true"] {{
      box-shadow: inset 0 0 0 4px rgba(255, 254, 250, 0.28), 0 16px 38px rgba(21, 21, 18, 0.18);
    }}
    .program header {{
      padding: 11px 10px;
      min-height: 104px;
    }}
    .program header h2 {{
      font-size: 19px;
      line-height: 0.98;
      overflow-wrap: anywhere;
    }}
    .program .center {{
      display: grid;
      align-content: end;
      padding: 10px;
      gap: 8px;
      color: var(--soft-ink);
      font-size: 12px;
      font-weight: 800;
    }}
    .program .signal {{
      border-top: 1px solid rgba(0,0,0,0.2);
      background-color: rgba(255,255,255,0.92);
    }}
    .program.full, .program.full header, .program.full .center {{ color: #fff; }}
    .program.full .label {{ color: #fff; }}
    .program.c403 {{ background: var(--blue); }}
    .program.c410 {{ background: var(--orange); color: #161000; }}
    .program.c446 {{ background: var(--violet); }}
    .program.c444 {{ background: var(--red); }}
    .program.c463 {{ background: var(--green); color: #091c08; }}
    .program.c410.full, .program.c463.full {{ color: #161000; }}
    .signal-water {{
      background:
        repeating-radial-gradient(ellipse at 50% 50%, transparent 0 10px, var(--ink) 11px 14px, transparent 15px 22px);
    }}
    .signal-lines {{
      background:
        repeating-linear-gradient(90deg, var(--ink) 0 6px, transparent 6px 13px);
    }}
    .signal-stripe {{
      background:
        repeating-linear-gradient(135deg, var(--ink) 0 10px, transparent 10px 16px, var(--ink) 16px 19px, transparent 19px 26px);
    }}
    .signal-wave {{
      background:
        radial-gradient(ellipse at 12px 11px, transparent 0 8px, var(--ink) 8px 10px, transparent 10px 17px) 0 0 / 34px 19px repeat-x,
        linear-gradient(var(--ink), var(--ink));
    }}

    .pamphlet {{
      border-top: 2px solid var(--ink);
      margin-top: 28px;
      max-height: 0;
      opacity: 0;
      overflow: hidden;
      transform: translateY(-8px);
      transition: max-height 520ms cubic-bezier(.2,.8,.2,1), opacity 260ms ease, transform 320ms ease;
    }}
    .pamphlet.is-open {{
      max-height: 1200px;
      opacity: 1;
      transform: translateY(0);
    }}
    .pamphlet-head {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 18px;
      align-items: start;
      padding: 16px 0 12px;
      border-bottom: 1px solid var(--line);
    }}
    .pamphlet-title {{ display: grid; gap: 2px; }}
    .pamphlet-title strong {{
      font-size: clamp(26px, 3.6vw, 52px);
      line-height: 0.92;
      font-weight: 950;
    }}
    .pamphlet-title span {{
      color: var(--soft-ink);
      font-size: 12px;
      font-weight: 850;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }}
    .pamphlet-close {{
      appearance: none;
      border: 1px solid var(--ink);
      border-radius: 6px;
      background: var(--field);
      color: var(--ink);
      cursor: pointer;
      font-size: 12px;
      font-weight: 900;
      min-height: 32px;
      padding: 6px 10px;
    }}
    .pamphlet-panels {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 0;
      background:
        linear-gradient(90deg, transparent 0 calc(33.333% - 1px), var(--line) calc(33.333% - 1px) 33.333%, transparent 33.333% calc(66.666% - 1px), var(--line) calc(66.666% - 1px) 66.666%, transparent 66.666%),
        var(--field);
    }}
    .pamphlet-panel {{
      min-height: 360px;
      padding: 18px 16px 20px;
      position: relative;
    }}
    .pamphlet-panel:before {{
      content: attr(data-count);
      position: absolute;
      right: 12px;
      top: 8px;
      color: rgba(21,21,18,0.08);
      font-size: 76px;
      line-height: 1;
      font-weight: 950;
      pointer-events: none;
    }}
    .pamphlet-panel h3 {{
      border-bottom: 1px solid var(--ink);
      color: var(--red);
      font-size: 13px;
      letter-spacing: 0.05em;
      margin: 0 0 12px;
      padding-bottom: 7px;
      text-transform: uppercase;
    }}
    .pamphlet-list {{
      display: grid;
      gap: 9px;
      max-height: 310px;
      overflow: auto;
      padding-right: 6px;
    }}
    .pamphlet-item {{
      border-bottom: 1px solid rgba(21,21,18,0.13);
      display: grid;
      gap: 4px;
      padding-bottom: 8px;
    }}
    .pamphlet-item.is-complete {{
      opacity: 0.52;
    }}
    .pamphlet-item.is-complete strong,
    .pamphlet-item.is-complete span {{
      color: var(--muted);
      text-decoration: line-through;
      text-decoration-thickness: 1px;
    }}
    .pamphlet-item strong {{
      font-size: 12px;
      line-height: 1.12;
      font-weight: 900;
    }}
    .pamphlet-item span {{
      color: var(--soft-ink);
      font-size: 11px;
      line-height: 1.25;
      font-weight: 700;
    }}

    .register {{
      display: grid;
      grid-template-columns: 1fr 92px 84px 80px;
      margin-top: 18px;
      border-top: 2px solid var(--ink);
    }}
    .register div {{
      border-bottom: 1px solid var(--line);
      padding: 8px 7px;
      min-height: 34px;
      font-size: 12px;
      font-weight: 750;
    }}
    .register .head {{
      color: var(--red);
      font-size: 11px;
      font-weight: 900;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}

    @media (max-width: 1150px) {{
      .manual-page {{ padding-left: 28px; }}
      .manual-page:before, .manual-page:after {{ display: none; }}
      .manual-layout,
      .manual-head,
      .program-grid,
      .register,
      .pamphlet-panels {{
        grid-template-columns: 1fr;
      }}
      .pamphlet-panels {{ background: var(--field); }}
      .program {{ min-height: 260px; }}
    }}
    @media (max-width: 720px) {{
      .page {{ width: min(100vw - 24px, 720px); padding-top: 14px; }}
      .manual-page {{ padding: 12px; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="manual-page">
      <div class="manual-head">
        <span>Claudia Academic Operations</span>
        <span id="generated-line">Generated from claudia.db</span>
        <span id="live-status" class="live-status">static</span>
      </div>

      <div class="manual-layout">
        <aside class="manual-copy">
          <div>
            <div class="label">Due today</div>
            <h1 id="due-count">0</h1>
            <p id="due-summary"></p>
          </div>

          <div>
            <div class="label">Next action</div>
            <p id="next-course"></p>
            <p id="next-action"></p>
          </div>

          <div>
            <div class="label">Source record</div>
            <div class="source-strip">
              <div><b>DB</b><span>claudia.db</span></div>
              <div><b>Week</b><span id="week-line"></span></div>
              <div><b>Mode</b><span>study operations</span></div>
            </div>
          </div>

          <section class="dispatch-panel" id="dispatch-panel">
            <div class="label">Dispatch signals</div>
            <div class="dispatch-meta">
              <span class="dispatch-freshness" id="dispatch-freshness">checking</span>
              <span class="dispatch-title" id="dispatch-title"></span>
            </div>
            <div class="dispatch-subtitle" id="dispatch-subtitle"></div>
            <div id="dispatch-sections"></div>
          </section>
        </aside>

        <section>
          <div class="program-grid" id="program-grid"></div>

          <section class="pamphlet" id="course-pamphlet" aria-live="polite">
            <div class="pamphlet-head">
              <div class="pamphlet-title">
                <span id="pamphlet-code">Select a course</span>
                <strong id="pamphlet-name">Course record</strong>
              </div>
              <button class="pamphlet-close" type="button" id="pamphlet-close">Close</button>
            </div>
            <div class="pamphlet-panels">
              <section class="pamphlet-panel" id="pamphlet-readings" data-count="0">
                <h3>Readings</h3>
                <div class="pamphlet-list"></div>
              </section>
              <section class="pamphlet-panel" id="pamphlet-assignments" data-count="0">
                <h3>Assignments</h3>
                <div class="pamphlet-list"></div>
              </section>
              <section class="pamphlet-panel" id="pamphlet-exams" data-count="0">
                <h3>Exams</h3>
                <div class="pamphlet-list"></div>
              </section>
            </div>
          </section>

          <div class="register" id="register"></div>
        </section>
      </div>
    </section>
  </main>

  <script>
    const DASHBOARD_PAYLOAD = {payload_json};
    const DONE_STATUSES = new Set(['completed', 'submitted', 'done']);
    const SIGNALS = {{
      'GPCO 403': 'signal-lines',
      'GPCO 410': 'signal-wave',
      'GPEC 446': 'signal-lines',
      'GPPS 444': 'signal-stripe',
      'GPPS 463': 'signal-water'
    }};

    function text(value) {{
      return value === null || value === undefined || value === '' ? '' : String(value);
    }}

    function courseClass(code) {{
      return 'c' + code.replace(/\\D/g, '').slice(-3);
    }}

    function isDone(item) {{
      return DONE_STATUSES.has(text(item.status).toLowerCase());
    }}

    function isExam(item) {{
      const title = text(item.title).toLowerCase();
      return title.includes('exam') || title.includes('midterm') || title.includes('quiz');
    }}

    function formatDate(dateString) {{
      if (!dateString) return '';
      const dt = new Date(dateString + 'T00:00:00');
      return dt.toLocaleDateString('en-US', {{ month: 'short', day: 'numeric' }});
    }}

    function formatDue(item) {{
      if (!item.due_date) return item.is_recurring ? 'Recurring' : '';
      let label = formatDate(item.due_date);
      if (item.due_time) label += ' at ' + item.due_time;
      return label;
    }}

    function cleanDispatchLine(line) {{
      return text(line)
        .replace(/^\\s*[-*]\\s+/, '')
        .replace(/^\\s*\\d+\\.\\s+/, '')
        .replace(/\\*\\*/g, '')
        .replace(/`/g, '')
        .trim();
    }}

    function dispatchLines(content) {{
      return text(content)
        .split('\\n')
        .map(cleanDispatchLine)
        .filter(Boolean)
        .slice(0, 4);
    }}

    function courseTag(code) {{
      const span = document.createElement('span');
      span.className = 'course-tag ' + courseClass(code);
      span.textContent = code;
      span.style.background = DASHBOARD_PAYLOAD.course_colors[code] || '#151512';
      if (code === 'GPCO 410' || code === 'GPPS 463') span.style.color = '#151512';
      return span;
    }}

    function activeAssignments() {{
      return DASHBOARD_PAYLOAD.assignments.filter(item => !isDone(item));
    }}

    function sortedUpcoming() {{
      const today = DASHBOARD_PAYLOAD.today;
      return activeAssignments()
        .filter(item => item.due_date && item.due_date >= today)
        .sort((a, b) => {{
          const ad = (a.due_date || '9999-99-99') + 'T' + (a.due_time || '23:59');
          const bd = (b.due_date || '9999-99-99') + 'T' + (b.due_time || '23:59');
          return ad.localeCompare(bd);
        }});
    }}

    function setProminentStatus() {{
      const dueToday = activeAssignments().filter(item => item.due_date === DASHBOARD_PAYLOAD.today);
      const dueCount = document.getElementById('due-count');
      const dueSummary = document.getElementById('due-summary');
      dueCount.textContent = dueToday.length;
      if (dueToday.length) {{
        dueSummary.textContent = dueToday.map(item => item.course + ': ' + item.title + (item.due_time ? ' at ' + item.due_time : '')).join(' / ');
      }} else {{
        const day = new Date(DASHBOARD_PAYLOAD.today + 'T00:00:00').toLocaleDateString('en-US', {{
          weekday: 'long',
          month: 'long',
          day: 'numeric'
        }});
        dueSummary.textContent = 'No hard deadline on ' + day + '. The empty state stays large so Edgar knows the day is study-focused.';
      }}

      const next = sortedUpcoming()[0];
      const nextCourse = document.getElementById('next-course');
      const nextAction = document.getElementById('next-action');
      nextCourse.innerHTML = '';
      if (next) {{
        nextCourse.appendChild(courseTag(next.course));
        nextAction.innerHTML = '<strong></strong><br><span></span><br><span></span>';
        nextAction.querySelector('strong').textContent = next.title;
        nextAction.querySelectorAll('span')[0].textContent = formatDue(next);
        nextAction.querySelectorAll('span')[1].textContent = next.weight ? next.weight + ' of grade' : text(next.status);
      }} else {{
        nextAction.textContent = 'No upcoming dated action in the live payload.';
      }}
    }}

    function courseItems(code) {{
      const readings = DASHBOARD_PAYLOAD.readings.filter(item => item.code === code);
      const assignments = DASHBOARD_PAYLOAD.assignments.filter(item => item.course === code);
      const exams = assignments.filter(isExam);
      return {{ readings, assignments, exams }};
    }}

    function cardSignal(course, items) {{
      const next = items.assignments.filter(item => !isDone(item) && (item.due_date || item.is_recurring))[0];
      if (next) return formatDue(next) + '\\n' + next.title;
      const pending = items.readings.filter(item => text(item.summary_status).toLowerCase() === 'pending').length;
      if (pending) return pending + ' pending readings';
      return 'Current record complete';
    }}

    function shortName(name) {{
      return text(name)
        .replace('International Economics', 'Intl Economics')
        .replace('International Politics & Security', 'Intl Security')
        .replace('Quantitative Methods 3', 'QM3');
    }}

    function renderPrograms() {{
      const grid = document.getElementById('program-grid');
      grid.innerHTML = '';
      DASHBOARD_PAYLOAD.courses.forEach(course => {{
        const items = courseItems(course.code);
        const button = document.createElement('button');
        button.className = 'program full ' + courseClass(course.code);
        button.type = 'button';
        button.dataset.course = course.code;
        button.setAttribute('aria-expanded', 'false');
        button.setAttribute('aria-controls', 'course-pamphlet');

        const header = document.createElement('header');
        const label = document.createElement('div');
        label.className = 'label';
        label.textContent = course.code;
        const h2 = document.createElement('h2');
        h2.textContent = shortName(course.name);
        header.append(label, h2);

        const center = document.createElement('div');
        center.className = 'center';
        center.textContent = cardSignal(course, items);

        const signal = document.createElement('div');
        signal.className = 'signal ' + (SIGNALS[course.code] || 'signal-lines');

        button.append(header, center, signal);
        button.addEventListener('click', () => openPamphlet(course.code));
        grid.appendChild(button);
      }});
    }}

    function createPamphletItem(primary, secondary, tertiary, complete = false) {{
      const item = document.createElement('div');
      item.className = 'pamphlet-item';
      if (complete) item.classList.add('is-complete');
      const strong = document.createElement('strong');
      strong.textContent = primary;
      item.appendChild(strong);
      [secondary, tertiary].filter(Boolean).forEach(value => {{
        const span = document.createElement('span');
        span.textContent = value;
        item.appendChild(span);
      }});
      return item;
    }}

    function renderPanel(panelId, records, builder) {{
      const panel = document.getElementById(panelId);
      const list = panel.querySelector('.pamphlet-list');
      const activeRecords = records.filter(record => !record.__complete);
      const completeRecords = records.filter(record => record.__complete);
      const orderedRecords = activeRecords.concat(completeRecords);
      panel.dataset.count = activeRecords.length + '/' + records.length;
      list.innerHTML = '';
      if (!orderedRecords.length) {{
        list.appendChild(createPamphletItem('No live records', 'Nothing is currently attached to this class.'));
        return;
      }}
      orderedRecords.forEach(record => list.appendChild(builder(record)));
    }}

    function openPamphlet(code) {{
      const course = DASHBOARD_PAYLOAD.courses.find(item => item.code === code);
      const items = courseItems(code);
      document.querySelectorAll('.program').forEach(button => {{
        button.setAttribute('aria-expanded', button.dataset.course === code ? 'true' : 'false');
      }});
      document.getElementById('pamphlet-code').textContent = code;
      document.getElementById('pamphlet-name').textContent = course ? course.name : 'Course record';
      const readings = items.readings.map(item => ({{
        ...item,
        __complete: isDone({{ status: text(item.summary_status) || 'pending' }})
      }}));
      const assignments = items.assignments.map(item => ({{
        ...item,
        __complete: isDone(item)
      }}));
      const exams = items.exams.map(item => ({{
        ...item,
        __complete: isDone(item)
      }}));
      renderPanel('pamphlet-readings', readings, item => {{
        const week = item.week ? 'Week ' + item.week : 'No week';
        const status = text(item.summary_status) || 'pending';
        const pages = item.pages ? item.pages + ' pages' : '';
        return createPamphletItem(
          item.title,
          [week, status, pages].filter(Boolean).join(' / '),
          item.authors,
          item.__complete
        );
      }});
      renderPanel('pamphlet-assignments', assignments, item => {{
        const status = text(item.status) || 'pending';
        const weight = item.weight ? item.weight : '';
        return createPamphletItem(
          item.title,
          [formatDue(item), status, weight].filter(Boolean).join(' / '),
          item.notes,
          item.__complete
        );
      }});
      renderPanel('pamphlet-exams', exams, item => {{
        return createPamphletItem(
          item.title,
          [formatDue(item), text(item.status), item.weight].filter(Boolean).join(' / '),
          item.notes,
          item.__complete
        );
      }});
      document.getElementById('course-pamphlet').classList.add('is-open');
    }}

    function closePamphlet() {{
      document.getElementById('course-pamphlet').classList.remove('is-open');
      document.querySelectorAll('.program').forEach(button => button.setAttribute('aria-expanded', 'false'));
    }}

    function renderRegister() {{
      const cards = DASHBOARD_PAYLOAD.cards;
      const rows = [
        ['Record', 'Count', 'Status', 'Source'],
        ['Assignments', cards.assignments, cards.upcoming_assignments + ' up', 'DB'],
        ['Completed assignments', cards.completed_assignments, 'verified', 'DB'],
        ['Readings', cards.readings, cards.pending_readings + ' pending', 'DB'],
        ['Pages', cards.pages, 'all courses', 'DB'],
        ['Files indexed', cards.indexed_files, cards.chunks + ' chunks', 'DB']
      ];
      const register = document.getElementById('register');
      register.innerHTML = '';
      rows.forEach((row, index) => {{
        row.forEach(value => {{
          const div = document.createElement('div');
          if (index === 0) div.className = 'head';
          div.textContent = value;
          register.appendChild(div);
        }});
      }});
    }}

    function renderDispatchPanel() {{
      const dispatch = DASHBOARD_PAYLOAD.dispatch || {{}};
      const badge = document.getElementById('dispatch-freshness');
      const title = document.getElementById('dispatch-title');
      const subtitle = document.getElementById('dispatch-subtitle');
      const sections = document.getElementById('dispatch-sections');
      sections.innerHTML = '';
      badge.className = 'dispatch-freshness ' + text(dispatch.status);

      if (!dispatch.present) {{
        badge.textContent = 'missing';
        title.textContent = 'No briefing found';
        subtitle.textContent = text(dispatch.message) || 'No dispatch signals are available in the payload.';
        return;
      }}

      badge.textContent = dispatch.is_today ? 'today' : text(dispatch.freshness_label);
      title.textContent = dispatch.date;
      const generated = dispatch.metadata && dispatch.metadata.generated ? 'Generated ' + dispatch.metadata.generated : 'Generated time unavailable';
      subtitle.textContent = [dispatch.title || 'Daily briefing', generated].filter(Boolean).join(' / ');

      (dispatch.signals || []).forEach(signal => {{
        const lines = dispatchLines(signal.content);
        if (!lines.length) return;
        const block = document.createElement('section');
        block.className = 'dispatch-section';
        const h3 = document.createElement('h3');
        h3.textContent = signal.title;
        const ul = document.createElement('ul');
        lines.forEach(line => {{
          const li = document.createElement('li');
          li.textContent = line;
          ul.appendChild(li);
        }});
        block.append(h3, ul);
        sections.appendChild(block);
      }});
    }}

    function setMetadata() {{
      document.getElementById('generated-line').textContent =
        'Generated ' + DASHBOARD_PAYLOAD.generated_label + ' / ' +
        DASHBOARD_PAYLOAD.term + ' / ' +
        DASHBOARD_PAYLOAD.program;
      document.getElementById('week-line').textContent =
        DASHBOARD_PAYLOAD.current_week + ' of ' + DASHBOARD_PAYLOAD.total_weeks;
    }}

    function setLiveStatus(label, cls) {{
      const el = document.getElementById('live-status');
      if (!el) return;
      el.textContent = label;
      el.className = 'live-status' + (cls ? ' ' + cls : '');
    }}

    function connectDashboardEvents() {{
      if (!window.EventSource || !/^https?:$/.test(window.location.protocol)) return;
      const events = new EventSource('/events');
      events.addEventListener('open', () => setLiveStatus('live', 'connected'));
      events.addEventListener('dashboard-change', async () => {{
        setLiveStatus('refreshing', 'refreshing');
        try {{
          await fetch('/api/dashboard', {{ cache: 'no-store' }});
        }} catch (err) {{}}
        window.location.reload();
      }});
      events.addEventListener('dashboard-error', () => setLiveStatus('error', ''));
      events.addEventListener('error', () => setLiveStatus('checking', ''));
    }}

    setMetadata();
    setProminentStatus();
    renderDispatchPanel();
    renderPrograms();
    renderRegister();
    document.getElementById('pamphlet-close').addEventListener('click', closePamphlet);
    const requestedCourse = new URLSearchParams(window.location.search).get('course');
    if (requestedCourse && DASHBOARD_PAYLOAD.courses.some(course => course.code === requestedCourse)) {{
      openPamphlet(requestedCourse);
    }}
    connectDashboardEvents();
  </script>
</body>
</html>
"""
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"Dashboard generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_dashboard()
