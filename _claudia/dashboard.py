#!/usr/bin/env python3
"""
Claudia Dashboard Generator
Generates a static HTML dashboard from the Claudia SQLite database.

Usage:
    python3 dashboard.py
"""

import json
import sqlite3
from calendar import monthrange
from collections import defaultdict
from datetime import datetime, timedelta, date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "claudia.db"
OUTPUT_PATH = SCRIPT_DIR / "dashboard.html"

QUARTER_START = date(2026, 3, 30)  # Monday of week 1
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
    "GPCO 403": "#7cb3ff",
    "GPCO 410": "#ffa94d",
    "GPEC 446": "#b197fc",
    "GPPS 444": "#ff6b6b",
    "GPPS 463": "#69db7c",
}


def query_db(conn, sql, params=()):
    return conn.execute(sql, params).fetchall()


def get_week_number(due_date_str):
    """Derive academic week number from a due date string."""
    if not due_date_str:
        return None
    try:
        d = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        delta = (d - QUARTER_START).days
        if delta < 0:
            return 0
        return delta // 7 + 1
    except ValueError:
        return None


def get_current_week(today_date):
    """Derive the academic week number from the local date."""
    delta = (today_date - QUARTER_START).days
    if delta < 0:
        return 0
    return min(delta // 7 + 1, TOTAL_WEEKS)


def table_columns(conn, table_name):
    return {row["name"] for row in conn.execute(f"PRAGMA table_info({table_name})")}


def generate_dashboard():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    now = datetime.now()
    today_date = now.date()
    current_week = get_current_week(today_date)

    # --- Gather data ---
    courses = query_db(conn, "SELECT * FROM courses ORDER BY code")
    total_files = query_db(conn, "SELECT COUNT(*) as n FROM files")[0]["n"]
    total_readings = query_db(conn, "SELECT COUNT(*) as n FROM readings")[0]["n"]
    pending_readings = query_db(conn, "SELECT COUNT(*) as n FROM readings WHERE summary_status = 'pending'")[0]["n"]
    summarized_readings = total_readings - pending_readings
    total_assignments = query_db(conn, "SELECT COUNT(*) as n FROM assignments")[0]["n"]
    completed_assignments = query_db(conn, "SELECT COUNT(*) as n FROM assignments WHERE status = 'completed'")[0]["n"]
    upcoming_assignments = total_assignments - completed_assignments
    total_embeddings = query_db(conn, "SELECT COUNT(*) as n FROM embeddings")[0]["n"]
    total_embedded_files = query_db(conn, "SELECT COUNT(DISTINCT source_path) as n FROM embeddings")[0]["n"]
    total_pages_all = query_db(conn, "SELECT COALESCE(SUM(pages), 0) as n FROM readings")[0]["n"]

    assignment_columns = table_columns(conn, "assignments")
    optional_selects = [
        f"a.{col}" for col in ASSIGNMENT_OPTIONAL_COLUMNS if col in assignment_columns
    ]
    optional_select_sql = ", " + ", ".join(optional_selects) if optional_selects else ""
    assignments = query_db(conn, f"""
        SELECT a.id, a.title, a.due_date, a.status, a.grade, a.weight, a.notes{optional_select_sql},
               c.code, c.name as course_name
        FROM assignments a
        LEFT JOIN courses c ON a.course_id = c.id
        ORDER BY a.due_date
    """)

    course_stats = []
    for c in courses:
        cid = c["id"]
        code = c["code"]
        files = query_db(conn, "SELECT COUNT(*) as n FROM files WHERE course_id = ?", (cid,))[0]["n"]
        readings = query_db(conn, "SELECT COUNT(*) as n FROM readings WHERE course_id = ?", (cid,))[0]["n"]
        assigns = query_db(conn, "SELECT COUNT(*) as n FROM assignments WHERE course_id = ?", (cid,))[0]["n"]
        embeds = query_db(conn, "SELECT COUNT(DISTINCT source_path) as n FROM embeddings WHERE course_code = ?", (code,))[0]["n"]
        total_pages = query_db(conn, "SELECT COALESCE(SUM(pages), 0) as n FROM readings WHERE course_id = ?", (cid,))[0]["n"]
        course_stats.append({
            "code": code, "name": c["name"], "professor": c["professor"],
            "files": files, "readings": readings, "assignments": assigns, "embeddings": embeds,
            "total_pages": total_pages,
        })

    readings_data = query_db(conn, """
        SELECT r.title, r.authors, r.week, r.summary_status, r.pages, c.code
        FROM readings r
        LEFT JOIN courses c ON r.course_id = c.id
        ORDER BY r.week, c.code, r.title
    """)

    # --- Time log data ---
    time_log_rows = query_db(conn, """
        SELECT id, date, course_code, title, category, start_time, end_time, duration_hrs, pages_read, notes
        FROM time_log ORDER BY date, start_time
    """)

    # Compute per-course reading speeds from Required Reading entries with pages > 0
    GLOBAL_FALLBACK_SPEED = 15.0  # pages/hr
    speed_by_course = {}
    from collections import defaultdict as _dd2
    reading_hrs = _dd2(float)
    reading_pages = _dd2(int)
    for row in time_log_rows:
        if row["category"] == "Required Reading" and row["pages_read"] and row["pages_read"] > 0:
            reading_hrs[row["course_code"]] += row["duration_hrs"] or 0
            reading_pages[row["course_code"]] += row["pages_read"]
    for code in reading_hrs:
        if reading_hrs[code] > 0:
            speed_by_course[code] = reading_pages[code] / reading_hrs[code]

    def reading_speed(course_code):
        return speed_by_course.get(course_code, GLOBAL_FALLBACK_SPEED)

    def fmt_est_time(pages, speed):
        if not pages:
            return "--"
        hrs = pages / speed
        h = int(hrs)
        m = round((hrs - h) * 60)
        if h == 0:
            return f"{m}m"
        if m == 0:
            return f"{h}h"
        return f"{h}h {m}m"

    # Week reading loads for all weeks
    week_reading_loads = {}
    for wk in range(1, TOTAL_WEEKS + 1):
        wk_readings = [r for r in readings_data if r["week"] == wk]
        wk_pages = sum(r["pages"] for r in wk_readings if r["pages"])
        wk_hrs = sum(r["pages"] / reading_speed(r["code"] or "") for r in wk_readings if r["pages"])
        week_reading_loads[wk] = {"pages": wk_pages, "hrs": round(wk_hrs, 1)}

    # Week 3 reading load
    current_week_readings = [r for r in readings_data if r["week"] == current_week]
    current_week_pages = sum(r["pages"] for r in current_week_readings if r["pages"])
    current_week_hrs = 0.0
    for r in current_week_readings:
        if r["pages"]:
            current_week_hrs += r["pages"] / reading_speed(r["code"] or "")
    weekly_load_str = f'{current_week_pages} pages / ~{current_week_hrs:.1f} hrs'

    logs = query_db(conn, """
        SELECT agent, action, details, timestamp
        FROM agent_logs ORDER BY timestamp DESC LIMIT 20
    """)

    conn.close()

    course_name_map = {c["code"]: c["name"] for c in courses}

    def course_label(code, name):
        if code and name:
            return f"{code} &mdash; {name}"
        return code or name or "Unknown"

    # --- Build assignment data for JS ---
    assignments_json = []
    for a in assignments:
        week = get_week_number(a["due_date"])
        status = a["status"] or "pending"
        is_recurring = a["is_recurring"] if "is_recurring" in assignment_columns else None
        if is_recurring is None:
            is_recurring = status == "recurring" or not a["due_date"]
        assignments_json.append({
            "id": a["id"],
            "title": a["title"],
            "due_date": a["due_date"] or "",
            "status": status,
            "grade": a["grade"] or "",
            "weight": a["weight"] or "",
            "notes": a["notes"] or "",
            "course": a["code"] or "",
            "course_name": a["course_name"] or "",
            "week": week,
            "due_time": a["due_time"] if "due_time" in assignment_columns and a["due_time"] else "",
            "timezone": a["timezone"] if "timezone" in assignment_columns and a["timezone"] else "",
            "deadline_source": a["deadline_source"] if "deadline_source" in assignment_columns and a["deadline_source"] else "",
            "source_path": a["source_path"] if "source_path" in assignment_columns and a["source_path"] else "",
            "source_confidence": a["source_confidence"] if "source_confidence" in assignment_columns and a["source_confidence"] else "",
            "date_kind": a["date_kind"] if "date_kind" in assignment_columns and a["date_kind"] else "",
            "is_recurring": bool(is_recurring),
            "recurrence_rule": a["recurrence_rule"] if "recurrence_rule" in assignment_columns and a["recurrence_rule"] else "",
            "opens_at": a["opens_at"] if "opens_at" in assignment_columns and a["opens_at"] else "",
            "submitted_at": a["submitted_at"] if "submitted_at" in assignment_columns and a["submitted_at"] else "",
            "last_verified_at": a["last_verified_at"] if "last_verified_at" in assignment_columns and a["last_verified_at"] else "",
            "external_id": a["external_id"] if "external_id" in assignment_columns and a["external_id"] else "",
        })

    # --- Static sections (courses, readings, logs, coverage) ---
    def deadline_class(due_date, status):
        if status == "completed":
            return "completed"
        if not due_date:
            return ""
        try:
            due = datetime.strptime(due_date, "%Y-%m-%d")
            if due.date() < now.date():
                return "overdue"
            elif due.date() <= (now + timedelta(days=7)).date():
                return "soon"
        except ValueError:
            pass
        return ""

    def coverage_pct(embedded, total):
        if total == 0:
            return "0%"
        return f"{embedded / total * 100:.0f}%"

    # Per-course table
    course_rows = ""
    for cs in course_stats:
        label = course_label(cs["code"], cs["name"])
        pages_disp = str(cs["total_pages"]) if cs["total_pages"] else "&mdash;"
        spd = reading_speed(cs["code"])
        spd_disp = f'{spd:.0f}' if cs["code"] in speed_by_course else f'~{spd:.0f}'
        est_total = fmt_est_time(cs["total_pages"] or None, spd)
        course_rows += f'<tr><td><strong>{label}</strong></td><td>{cs["professor"]}</td><td>{cs["files"]}</td><td>{cs["readings"]}</td><td>{cs["assignments"]}</td><td>{cs["embeddings"]}</td><td>{pages_disp}</td><td>{spd_disp}</td><td>{est_total}</td></tr>'

    # Coverage table
    coverage_rows = ""
    for cs in course_stats:
        total_c = cs["files"]
        emb_c = cs["embeddings"]
        pct = coverage_pct(emb_c, total_c)
        bar_w = (emb_c / total_c * 100) if total_c > 0 else 0
        label = course_label(cs["code"], cs["name"])
        coverage_rows += f'<tr><td>{label}</td><td>{emb_c} / {total_c}</td><td><div class="bar-bg"><div class="bar-fill" style="width:{bar_w}%"></div></div></td><td>{pct}</td></tr>'

    # Readings table -- grouped by week
    # Pre-group readings by week to compute totals
    from collections import defaultdict as _dd
    readings_by_week = _dd(list)
    for r in readings_data:
        readings_by_week[r["week"]].append(r)

    readings_weeks_html = ""
    for week in sorted(readings_by_week.keys(), key=lambda w: (w is None, w)):
        week_readings = readings_by_week[week]
        week_label = f"Week {week}" if week is not None else "No Week Assigned"
        week_pages = sum(r["pages"] for r in week_readings if r["pages"] is not None)
        pages_label = f' <span style="font-size:0.75rem;font-weight:400;color:#aaa;margin-left:0.5rem">{week_pages} pp</span>' if week_pages else ""
        # Past weeks collapsed, current and future expanded
        is_past = (week is not None) and (week < current_week)
        open_cls = "" if is_past else " open"
        rows = ""
        for r in week_readings:
            status_cls = "summarized" if r["summary_status"] != "pending" else "pending-reading"
            code = r["code"] or ""
            color = COURSE_COLORS.get(code, "#888")
            course_badge = f'<span style="font-size:0.7rem;font-weight:700;padding:0.1rem 0.4rem;border-radius:4px;background:{color};color:#000">{code}</span>' if code else ""
            pages_cell = str(r["pages"]) if r["pages"] is not None else ""
            est_cell = fmt_est_time(r["pages"], reading_speed(r["code"] or ""))
            rows += f'<tr class="{status_cls}"><td>{course_badge}</td><td>{r["title"]}</td><td>{r["authors"] or ""}</td><td>{pages_cell}</td><td>{est_cell}</td><td>{r["summary_status"] or "pending"}</td></tr>'
        readings_weeks_html += f'''
        <div class="collapsible week-collapsible">
            <div class="collapsible-header{open_cls}" onclick="toggleCollapse(this)">
                <span class="chevron">&#9654;</span>
                <h2 style="font-size:0.85rem">{week_label}{pages_label}</h2>
            </div>
            <div class="collapsible-body{open_cls}">
                <table><thead><tr><th>Course</th><th>Title</th><th>Authors</th><th>Pages</th><th>Est. Time</th><th>Status</th></tr></thead>
                <tbody>{rows}</tbody></table>
            </div>
        </div>'''

    # Logs table
    log_rows = ""
    for l in logs:
        log_rows += f'<tr><td>{l["timestamp"] or ""}</td><td>{l["agent"] or ""}</td><td>{l["action"] or ""}</td><td>{(l["details"] or "")[:120]}</td></tr>'
    if not logs:
        log_rows = '<tr><td colspan="4">No activity logged yet.</td></tr>'

    # Time tracker table rows
    tracker_rows = ""
    for row in time_log_rows:
        code = row["course_code"] or ""
        color = COURSE_COLORS.get(code, "#888")
        badge = f'<span style="font-size:0.7rem;font-weight:700;padding:0.1rem 0.4rem;border-radius:4px;background:{color};color:#000">{code}</span>' if code in COURSE_COLORS else f'<span style="font-size:0.7rem;color:#888">{code}</span>'
        pages_cell = str(row["pages_read"]) if row["pages_read"] else "&mdash;"
        dur = f'{row["duration_hrs"]:.2f}h' if row["duration_hrs"] else "&mdash;"
        tracker_rows += f'<tr><td>{row["date"]}</td><td>{badge}</td><td>{row["title"]}</td><td>{row["category"]}</td><td>{row["start_time"] or ""}</td><td>{row["end_time"] or ""}</td><td>{dur}</td><td>{pages_cell}</td></tr>'

    # Per-course summary for time tracker
    tracker_summary_rows = ""
    all_codes_logged = sorted(set(row["course_code"] for row in time_log_rows if row["course_code"] in COURSE_COLORS))
    for code in all_codes_logged:
        course_rows_log = [r for r in time_log_rows if r["course_code"] == code]
        total_hrs = sum(r["duration_hrs"] or 0 for r in course_rows_log)
        reading_rows_log = [r for r in course_rows_log if r["category"] == "Required Reading" and r["pages_read"]]
        total_pg_read = sum(r["pages_read"] for r in reading_rows_log)
        spd = speed_by_course.get(code)
        spd_disp = f'{spd:.0f} pg/hr' if spd else "&mdash;"
        # total assigned pages for this course
        total_assigned = next((cs["total_pages"] for cs in course_stats if cs["code"] == code), 0)
        pct = (total_pg_read / total_assigned * 100) if total_assigned else 0
        bar = f'<div class="bar-bg"><div class="bar-fill" style="width:{min(pct,100):.0f}%"></div></div>'
        pct_label = f'{pct:.0f}%' if total_assigned else "&mdash;"
        color = COURSE_COLORS.get(code, "#888")
        badge = f'<span style="font-size:0.7rem;font-weight:700;padding:0.1rem 0.4rem;border-radius:4px;background:{color};color:#000">{code}</span>'
        tracker_summary_rows += f'<tr><td>{badge}</td><td>{total_hrs:.1f}</td><td>{total_pg_read}</td><td>{total_assigned}</td><td>{bar} {pct_label}</td><td>{spd_disp}</td></tr>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Claudia Dashboard</title>
<style>
:root {{
    --bg: #0f0f0f;
    --surface: #1a1a1a;
    --border: #2a2a2a;
    --text: #e0e0e0;
    --text-muted: #888;
    --text-dim: #666;
    --accent: #7cb3ff;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    padding: 0.75rem 1.25rem;
    line-height: 1.4;
}}

/* Header */
.header {{
    display: flex; align-items: baseline; gap: 1rem;
    margin-bottom: 0.5rem;
}}
h1 {{ font-size: 1.1rem; font-weight: 700; color: #fff; }}
.subtitle {{ color: var(--text-dim); font-size: 0.75rem; }}
h2 {{
    font-size: 1rem; color: #ccc; margin-bottom: 0.75rem;
    padding-bottom: 0.4rem; border-bottom: 1px solid var(--border);
}}

/* Stat cards row */
.cards {{
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 0.5rem; margin-bottom: 0.6rem;
}}
@media (max-width: 1100px) {{
    .cards {{ grid-template-columns: repeat(4, 1fr); }}
}}
.card {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 6px; padding: 0.5rem 0.6rem;
}}
.card-value {{ font-size: 1.3rem; font-weight: 700; color: #fff; line-height: 1.1; }}
.card-label {{ font-size: 0.7rem; color: #999; margin-top: 0.1rem; }}
.card-sub {{ font-size: 0.65rem; color: var(--text-dim); margin-top: 0.1rem; }}

/* Legend */
.legend {{
    display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 0.6rem; align-items: center;
}}
.legend-item {{
    display: flex; align-items: center; gap: 0.3rem; font-size: 0.72rem; color: var(--text-muted);
}}
.legend-dot {{
    width: 8px; height: 8px; border-radius: 2px; flex-shrink: 0;
}}

/* Tabs */
.tab-bar {{
    display: flex; gap: 0; margin-bottom: 0;
    border-bottom: 2px solid var(--border);
}}
.tab-btn {{
    padding: 0.45rem 1.1rem; cursor: pointer;
    background: none; border: none; color: var(--text-muted);
    font-size: 0.85rem; font-weight: 500;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px; transition: all 0.15s;
}}
.tab-btn:hover {{ color: #fff; }}
.tab-btn.active {{ color: var(--accent); border-bottom-color: var(--accent); }}
.tab-panel {{ display: none; padding-top: 1rem; }}
.tab-panel.active {{ display: block; }}

/* Sub-tabs (inside Timeline) */
.subtab-bar {{
    display: flex; gap: 0; margin-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}}
.subtab-btn {{
    padding: 0.3rem 0.9rem; cursor: pointer;
    background: none; border: none; color: var(--text-muted);
    font-size: 0.8rem; font-weight: 500;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px; transition: all 0.15s;
}}
.subtab-btn:hover {{ color: #fff; }}
.subtab-btn.active {{ color: var(--accent); border-bottom-color: var(--accent); }}
.subtab-panel {{ display: none; }}
.subtab-panel.active {{ display: block; }}

/* Section */
.section {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 1.25rem; margin-bottom: 1.25rem;
}}

/* Tables */
table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
th {{
    text-align: left; padding: 0.4rem 0.65rem;
    border-bottom: 1px solid #333; color: #999;
    font-weight: 600; font-size: 0.75rem;
    text-transform: uppercase; letter-spacing: 0.04em;
}}
td {{ padding: 0.4rem 0.65rem; border-bottom: 1px solid #1f1f1f; }}
tr:hover {{ background: #222; }}
tr.overdue td {{ color: #ff6b6b; }}
tr.soon td {{ color: #ffa94d; }}
tr.completed td {{ color: #69db7c; text-decoration: line-through; opacity: 0.7; }}
tr.course-header td {{
    font-weight: 700; color: var(--accent);
    padding-top: 0.75rem; border-bottom: 1px solid #333; font-size: 0.85rem;
}}
tr.exam-row td {{ font-weight: 600; }}
tr.pending-reading td {{ color: var(--text); }}
tr.summarized td {{ color: #69db7c; }}
.bar-bg {{ background: var(--border); border-radius: 4px; height: 6px; width: 100%; overflow: hidden; }}
.bar-fill {{ background: var(--accent); height: 100%; border-radius: 4px; }}
p {{ margin-bottom: 0.75rem; color: #999; font-size: 0.82rem; }}

/* ===== WEEK VIEW ===== */
.week-group {{ margin-bottom: 0.75rem; }}
.week-header {{
    display: flex; align-items: center; gap: 0.6rem;
    padding: 0.45rem 0; cursor: pointer; user-select: none;
}}
.week-header h3 {{ font-size: 0.88rem; color: #ccc; font-weight: 600; }}
.week-header .week-dates {{ font-size: 0.72rem; color: var(--text-dim); }}
.week-header .badge {{
    font-size: 0.65rem; padding: 0.1rem 0.4rem;
    border-radius: 10px; font-weight: 600;
}}
.badge-current {{ background: var(--accent); color: #000; }}
.badge-completed {{ background: #2d4a2d; color: #69db7c; }}
.week-items {{
    padding-left: 0.75rem; border-left: 2px solid var(--border);
    margin-left: 0.4rem;
}}
.week-group.current .week-items {{ border-left-color: var(--accent); }}
.week-group.past .week-header h3 {{ color: var(--text-dim); }}
.week-group.past .week-items {{ opacity: 0.5; }}
.week-item {{
    display: flex; align-items: center; gap: 0.5rem;
    padding: 0.3rem 0.6rem; font-size: 0.82rem;
    border-radius: 4px; margin-bottom: 1px;
}}
.week-item:hover {{ background: #222; }}
.week-item .course-tag {{
    font-size: 0.65rem; font-weight: 700;
    padding: 0.1rem 0.35rem; border-radius: 3px;
    white-space: nowrap; flex-shrink: 0;
}}
.week-item .due {{ color: var(--text-dim); font-size: 0.72rem; margin-left: auto; white-space: nowrap; }}
.week-item.completed-item {{ text-decoration: line-through; color: var(--text-dim); }}
.week-no-items {{ padding: 0.3rem 0.6rem; font-size: 0.75rem; color: var(--text-dim); font-style: italic; }}

/* ===== CALENDAR VIEW ===== */
.cal-controls {{
    display: flex; align-items: center; gap: 1rem; margin-bottom: 0.75rem;
}}
.cal-controls button {{
    background: var(--surface); border: 1px solid var(--border);
    color: var(--text); padding: 0.3rem 0.7rem; border-radius: 6px;
    cursor: pointer; font-size: 0.82rem;
}}
.cal-controls button:hover {{ border-color: var(--accent); }}
.cal-controls .cal-month-label {{ font-size: 1rem; font-weight: 600; color: #fff; min-width: 140px; text-align: center; }}
.cal-grid {{
    display: grid; grid-template-columns: repeat(7, 1fr); gap: 1px;
    background: var(--border); border-radius: 8px; overflow: hidden;
}}
.cal-day-header {{
    background: #222; padding: 0.35rem; text-align: center;
    font-size: 0.7rem; color: var(--text-muted); font-weight: 600;
    text-transform: uppercase;
}}
.cal-day {{
    background: var(--surface); min-height: 70px; padding: 0.3rem;
    position: relative;
}}
.cal-day.empty {{ background: #141414; }}
.cal-day.today {{ outline: 2px solid var(--accent); outline-offset: -2px; z-index: 1; }}
.cal-day .day-num {{ font-size: 0.7rem; color: var(--text-dim); margin-bottom: 0.15rem; }}
.cal-day.today .day-num {{ color: var(--accent); font-weight: 700; }}
.cal-event {{
    font-size: 0.6rem; padding: 0.1rem 0.25rem;
    border-radius: 3px; margin-bottom: 2px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    cursor: default; color: #000; font-weight: 600;
}}
.cal-event:hover {{ filter: brightness(1.15); }}

/* ===== EISENHOWER MATRIX ===== */
.matrix-col-label {{
    text-align: center; font-size: 0.75rem; font-weight: 700;
    color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em;
    padding-bottom: 0.2rem;
}}
.quadrant {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 0.85rem; min-height: 200px;
    transition: border-color 0.15s;
}}
.quadrant.drag-over {{ border-color: var(--accent); background: #1e2a1e; }}
.quadrant-header {{
    display: flex; align-items: center; gap: 0.4rem;
    margin-bottom: 0.6rem; padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}}
.quadrant-header .q-icon {{ font-size: 0.9rem; }}
.quadrant-header .q-title {{ font-size: 0.82rem; font-weight: 700; }}
.quadrant-header .q-subtitle {{ font-size: 0.66rem; color: var(--text-dim); }}
.q1 .quadrant-header {{ color: #ff6b6b; }}
.q2 .quadrant-header {{ color: #ffa94d; }}
.q3 .quadrant-header {{ color: var(--accent); }}
.q4 .quadrant-header {{ color: var(--text-dim); }}
.matrix-row-label {{
    writing-mode: vertical-lr; transform: rotate(180deg);
    font-size: 0.75rem; font-weight: 700; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.08em;
    display: flex; align-items: center; justify-content: center;
    padding: 0 0.2rem;
}}
.matrix-card {{
    display: flex; align-items: center; gap: 0.4rem;
    padding: 0.35rem 0.5rem; margin-bottom: 0.3rem;
    background: #222; border: 1px solid #333; border-radius: 5px;
    font-size: 0.78rem; cursor: grab;
    transition: transform 0.1s, box-shadow 0.1s;
}}
.matrix-card:active {{ cursor: grabbing; }}
.matrix-card.dragging {{ opacity: 0.4; }}
.matrix-card .course-tag {{
    font-size: 0.62rem; font-weight: 700;
    padding: 0.08rem 0.3rem; border-radius: 3px;
    white-space: nowrap; flex-shrink: 0;
}}
.matrix-card .card-title {{ flex: 1; }}
.matrix-card .card-due {{ font-size: 0.66rem; color: var(--text-dim); white-space: nowrap; }}
.matrix-empty {{ font-size: 0.75rem; color: var(--text-dim); font-style: italic; padding: 0.4rem; }}

/* Course tag colors */
{" ".join(f'.tag-{code.replace(" ","")} {{ background: {color}; color: #000; }}' for code, color in COURSE_COLORS.items())}

/* Collapsible */
.collapsible {{ margin-bottom: 1rem; }}
.collapsible-header {{
    display: flex; align-items: center; gap: 0.5rem;
    cursor: pointer; user-select: none; padding: 0.6rem 0.85rem;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; margin-bottom: 0;
}}
.collapsible-header h2 {{ margin: 0; padding: 0; border: none; font-size: 0.9rem; }}
.collapsible-header .chevron {{
    color: var(--text-dim); transition: transform 0.2s; font-size: 0.75rem;
}}
.collapsible-header.open .chevron {{ transform: rotate(90deg); }}
.collapsible-header.open {{ border-radius: 8px 8px 0 0; }}
.collapsible-body {{
    display: none; background: var(--surface);
    border: 1px solid var(--border); border-top: none;
    border-radius: 0 0 8px 8px; padding: 0.85rem 1.1rem;
}}
.collapsible-body.open {{ display: block; }}

/* Nested week collapsibles inside Readings Status */
.week-collapsible {{ margin-bottom: 0.5rem; }}
.week-collapsible .collapsible-header {{ background: #222; border-color: #333; }}
.week-collapsible .collapsible-body {{ background: #1e1e1e; border-color: #333; padding: 0.5rem 0.75rem; }}

/* Section heading inside tabs */
.section-heading {{
    font-size: 0.8rem; font-weight: 700; color: #aaa;
    text-transform: uppercase; letter-spacing: 0.05em;
    margin-bottom: 0.6rem; padding-bottom: 0.35rem;
    border-bottom: 1px solid var(--border);
}}
</style>
</head>
<body>

<!-- Header -->
<div class="header">
    <h1>Claudia</h1>
    <div class="subtitle">Generated {now.strftime('%Y-%m-%d %H:%M')} &middot; Spring 2026 &middot; GPS &middot; Week {current_week} of {TOTAL_WEEKS}</div>
</div>

<!-- Summary Cards -->
<div class="cards">
    <div class="card"><div class="card-value">{len(courses)}</div><div class="card-label">Courses</div></div>
    <div class="card"><div class="card-value">{total_files}</div><div class="card-label">Files</div></div>
    <div class="card"><div class="card-value">{total_readings}</div><div class="card-label">Readings</div><div class="card-sub">{pending_readings} pending &middot; {summarized_readings} done</div></div>
    <div class="card"><div class="card-value">{total_assignments}</div><div class="card-label">Assignments</div><div class="card-sub">{upcoming_assignments} up &middot; {completed_assignments} done</div></div>
    <div class="card"><div class="card-value">{total_embeddings}</div><div class="card-label">Chunks</div><div class="card-sub">{total_embedded_files} files indexed</div></div>
    <div class="card"><div class="card-value">{total_pages_all}</div><div class="card-label">Pages</div><div class="card-sub">all courses</div></div>
    <div class="card"><div class="card-value" style="font-size:0.95rem;line-height:1.3">{weekly_load_str}</div><div class="card-label">Wk {current_week} Load</div></div>
</div>

<!-- Legend -->
<div class="legend">
    {"".join(f'<div class="legend-item"><div class="legend-dot" style="background:{color}"></div>{code}</div>' for code, color in COURSE_COLORS.items())}
</div>

<!-- Main Tabs -->
<div class="tab-bar">
    <button class="tab-btn active" data-tab="timeline">Timeline</button>
    <button class="tab-btn" data-tab="readings">Readings</button>
    <button class="tab-btn" data-tab="overview">Overview</button>
</div>

<!-- ===== TAB: TIMELINE ===== -->
<div class="tab-panel active" id="tab-timeline">
    <div class="subtab-bar">
        <button class="subtab-btn active" data-subtab="week">Week View</button>
        <button class="subtab-btn" data-subtab="calendar">Calendar</button>
        <button class="subtab-btn" data-subtab="matrix">Eisenhower Matrix</button>
    </div>

    <div class="subtab-panel active" id="subtab-week">
        <div id="week-view"></div>
    </div>

    <div class="subtab-panel" id="subtab-calendar">
        <div class="cal-controls">
            <button id="cal-prev">&larr;</button>
            <div class="cal-month-label" id="cal-month-label"></div>
            <button id="cal-next">&rarr;</button>
        </div>
        <div id="cal-grid-container"></div>
    </div>

    <div class="subtab-panel" id="subtab-matrix">
        <p style="margin-bottom:0.75rem">Drag assignments between quadrants. Arrangement is saved locally.</p>
        <div style="display:grid; grid-template-columns: auto 1fr 1fr; grid-template-rows: auto auto auto; gap: 0.75rem 0.5rem;">
            <div></div>
            <div class="matrix-col-label">Urgent</div>
            <div class="matrix-col-label">Not Urgent</div>

            <div class="matrix-row-label">Important</div>
            <div class="quadrant q1" data-quadrant="q1" id="q1">
                <div class="quadrant-header"><span class="q-icon">&#9888;</span><div><div class="q-title">Do First</div><div class="q-subtitle">Urgent + Important</div></div></div>
                <div class="q-items"></div>
            </div>
            <div class="quadrant q2" data-quadrant="q2" id="q2">
                <div class="quadrant-header"><span class="q-icon">&#9733;</span><div><div class="q-title">Schedule</div><div class="q-subtitle">Not Urgent + Important</div></div></div>
                <div class="q-items"></div>
            </div>

            <div class="matrix-row-label">Not Important</div>
            <div class="quadrant q3" data-quadrant="q3" id="q3">
                <div class="quadrant-header"><span class="q-icon">&#8644;</span><div><div class="q-title">Delegate</div><div class="q-subtitle">Urgent + Not Important</div></div></div>
                <div class="q-items"></div>
            </div>
            <div class="quadrant q4" data-quadrant="q4" id="q4">
                <div class="quadrant-header"><span class="q-icon">&#128465;</span><div><div class="q-title">Eliminate</div><div class="q-subtitle">Not Urgent + Not Important</div></div></div>
                <div class="q-items"></div>
            </div>
        </div>
    </div>
</div>

<!-- ===== TAB: READINGS ===== -->
<div class="tab-panel" id="tab-readings">

    <div class="collapsible">
        <div class="collapsible-header open" onclick="toggleCollapse(this)">
            <span class="chevron" style="transform:rotate(90deg)">&#9654;</span><h2>Readings Status</h2>
        </div>
        <div class="collapsible-body open">
            {readings_weeks_html}
        </div>
    </div>

    <div class="collapsible">
        <div class="collapsible-header" onclick="toggleCollapse(this)">
            <span class="chevron">&#9654;</span><h2>Study Time Tracker</h2>
        </div>
        <div class="collapsible-body">
            <div class="section-heading">Per-Course Summary</div>
            <table style="margin-bottom:1.25rem"><thead><tr><th>Course</th><th>Total Hrs</th><th>Pages Read</th><th>Pages Assigned</th><th>Progress</th><th>Speed</th></tr></thead>
            <tbody>{tracker_summary_rows}</tbody></table>
            <div class="section-heading">Session Log</div>
            <table><thead><tr><th>Date</th><th>Course</th><th>Task</th><th>Category</th><th>Start</th><th>End</th><th>Duration</th><th>Pages</th></tr></thead>
            <tbody>{tracker_rows}</tbody></table>
        </div>
    </div>

</div>

<!-- ===== TAB: OVERVIEW ===== -->
<div class="tab-panel" id="tab-overview">

    <div class="collapsible">
        <div class="collapsible-header open" onclick="toggleCollapse(this)">
            <span class="chevron" style="transform:rotate(90deg)">&#9654;</span><h2>Per-Course Breakdown</h2>
        </div>
        <div class="collapsible-body open">
            <table><thead><tr><th>Course</th><th>Professor</th><th>Files</th><th>Readings</th><th>Assignments</th><th>Embedded</th><th>Pages</th><th>Speed (pg/hr)</th><th>Est. Total</th></tr></thead>
            <tbody>{course_rows}</tbody></table>
        </div>
    </div>

    <div class="collapsible">
        <div class="collapsible-header" onclick="toggleCollapse(this)">
            <span class="chevron">&#9654;</span><h2>Embeddings Coverage</h2>
        </div>
        <div class="collapsible-body">
            <p>Overall: {total_embedded_files} / {total_files} files indexed ({coverage_pct(total_embedded_files, total_files)})</p>
            <table><thead><tr><th>Course</th><th>Indexed / Total</th><th>Progress</th><th>%</th></tr></thead>
            <tbody>{coverage_rows}</tbody></table>
        </div>
    </div>

    <div class="collapsible">
        <div class="collapsible-header" onclick="toggleCollapse(this)">
            <span class="chevron">&#9654;</span><h2>Recent Activity</h2>
        </div>
        <div class="collapsible-body">
            <table><thead><tr><th>Timestamp</th><th>Agent</th><th>Action</th><th>Details</th></tr></thead>
            <tbody>{log_rows}</tbody></table>
        </div>
    </div>

</div>

<script>
const ASSIGNMENTS = {json.dumps(assignments_json)};
const QUARTER_START = new Date('2026-03-30');
const CURRENT_WEEK = {current_week};
const COURSE_COLORS = {json.dumps(COURSE_COLORS)};
const WEEK_READING_LOADS = {json.dumps(week_reading_loads)};

// --- Main Tabs ---
document.querySelectorAll('.tab-btn').forEach(btn => {{
    btn.addEventListener('click', () => {{
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    }});
}});

// --- Sub-tabs (Timeline) ---
document.querySelectorAll('.subtab-btn').forEach(btn => {{
    btn.addEventListener('click', () => {{
        document.querySelectorAll('.subtab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.subtab-panel').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('subtab-' + btn.dataset.subtab).classList.add('active');
    }});
}});

// --- Collapsibles ---
function toggleCollapse(header) {{
    header.classList.toggle('open');
    header.nextElementSibling.classList.toggle('open');
}}

function courseTag(code) {{
    const cls = 'tag-' + code.replace(/\\s/g, '');
    return `<span class="course-tag ${{cls}}">${{code}}</span>`;
}}

function formatDate(d) {{
    if (!d) return '';
    const dt = new Date(d + 'T00:00:00');
    return dt.toLocaleDateString('en-US', {{ month: 'short', day: 'numeric' }});
}}

function localDateString(dt) {{
    const y = dt.getFullYear();
    const m = String(dt.getMonth() + 1).padStart(2, '0');
    const d = String(dt.getDate()).padStart(2, '0');
    return `${{y}}-${{m}}-${{d}}`;
}}

function dueDateTime(a) {{
    if (!a.due_date) return null;
    const time = a.due_time || '23:59';
    return new Date(`${{a.due_date}}T${{time}}:00`);
}}

function formatDue(a) {{
    if (!a.due_date) return a.is_recurring ? 'Recurring' : '';
    let label = formatDate(a.due_date);
    if (a.due_time) label += ` ${{a.due_time}}`;
    return label;
}}

// ===== WEEK VIEW =====
function renderWeekView() {{
    const container = document.getElementById('week-view');
    let html = '';

    for (let w = 1; w <= 11; w++) {{
        const weekStart = new Date(QUARTER_START);
        weekStart.setDate(weekStart.getDate() + (w - 1) * 7);
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekEnd.getDate() + 6);

        const items = ASSIGNMENTS.filter(a => a.week === w);
        const recurring = ASSIGNMENTS.filter(a => a.week === null && a.status === 'recurring');
        const isPast = w < CURRENT_WEEK;
        const isCurrent = w === CURRENT_WEEK;

        const cls = isPast ? 'past' : isCurrent ? 'current' : '';
        const badge = isCurrent ? '<span class="badge badge-current">Current</span>' :
                      isPast ? '<span class="badge badge-completed">Completed</span>' : '';

        const dateRange = formatDate(localDateString(weekStart)) + ' - ' + formatDate(localDateString(weekEnd));

        html += `<div class="week-group ${{cls}}">`;
        const wkLoad = WEEK_READING_LOADS[w];
        const wkLoadStr = wkLoad && wkLoad.pages > 0 ? `${{wkLoad.pages}} pp / ~${{wkLoad.hrs}}h reading` : '';
        html += `<div class="week-header" onclick="this.parentElement.querySelector('.week-items').classList.toggle('collapsed')">`;
        html += `<h3>Week ${{w}}</h3><span class="week-dates">${{dateRange}}</span>${{badge}}`;
        if (wkLoadStr) html += `<span style="font-size:0.72rem;color:#777;margin-left:auto">${{wkLoadStr}}</span>`;
        html += `</div><div class="week-items ${{isPast && !isCurrent ? '' : ''}}">`;

        if (items.length === 0 && (w >= CURRENT_WEEK || !isPast)) {{
            html += '<div class="week-no-items">No dated assignments</div>';
        }}

        for (const a of items) {{
            const done = a.status === 'completed' ? 'completed-item' : '';
            html += `<div class="week-item ${{done}}">`;
            html += courseTag(a.course);
            html += `<span>${{a.title}}</span>`;
            if (a.weight) html += `<span style="font-size:0.7rem;color:#666">${{a.weight}}</span>`;
            html += `<span class="due">${{formatDue(a)}}</span>`;
            html += `</div>`;
        }}

        html += '</div></div>';
    }}

    // Recurring items at bottom
    const recurring = ASSIGNMENTS.filter(a => a.week === null);
    if (recurring.length) {{
        html += '<div class="week-group"><div class="week-header"><h3>Recurring</h3></div><div class="week-items">';
        for (const a of recurring) {{
            html += `<div class="week-item">${{courseTag(a.course)}}<span>${{a.title}}</span>`;
            if (a.weight) html += `<span style="font-size:0.7rem;color:#666">${{a.weight}}</span>`;
            html += '</div>';
        }}
        html += '</div></div>';
    }}

    container.innerHTML = html;
}}
renderWeekView();

// ===== CALENDAR VIEW =====
let calMonth = 3; // April (0-indexed)
let calYear = 2026;

function renderCalendar() {{
    const label = document.getElementById('cal-month-label');
    const container = document.getElementById('cal-grid-container');
    const monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    label.textContent = monthNames[calMonth] + ' ' + calYear;

    const firstDay = new Date(calYear, calMonth, 1).getDay(); // 0=Sun
    const daysInMonth = new Date(calYear, calMonth + 1, 0).getDate();
    const todayStr = localDateString(new Date());

    let html = '<div class="cal-grid">';
    ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].forEach(d => {{
        html += `<div class="cal-day-header">${{d}}</div>`;
    }});

    // Empty leading cells
    for (let i = 0; i < firstDay; i++) {{
        html += '<div class="cal-day empty"></div>';
    }}

    for (let d = 1; d <= daysInMonth; d++) {{
        const dateStr = `${{calYear}}-${{String(calMonth+1).padStart(2,'0')}}-${{String(d).padStart(2,'0')}}`;
        const isToday = dateStr === todayStr;
        const dayAssignments = ASSIGNMENTS.filter(a => a.due_date === dateStr);

        html += `<div class="cal-day ${{isToday ? 'today' : ''}}">`;
        html += `<div class="day-num">${{d}}</div>`;
        for (const a of dayAssignments) {{
            const bg = COURSE_COLORS[a.course] || '#555';
            html += `<div class="cal-event" style="background:${{bg}}" title="${{a.course}}: ${{a.title}} ${{formatDue(a)}}">${{a.due_time ? a.due_time + ' ' : ''}}${{a.title}}</div>`;
        }}
        html += '</div>';
    }}

    // Trailing empty cells
    const totalCells = firstDay + daysInMonth;
    const remaining = (7 - totalCells % 7) % 7;
    for (let i = 0; i < remaining; i++) {{
        html += '<div class="cal-day empty"></div>';
    }}

    html += '</div>';
    container.innerHTML = html;
}}

document.getElementById('cal-prev').addEventListener('click', () => {{
    calMonth--; if (calMonth < 0) {{ calMonth = 11; calYear--; }}
    renderCalendar();
}});
document.getElementById('cal-next').addEventListener('click', () => {{
    calMonth++; if (calMonth > 11) {{ calMonth = 0; calYear++; }}
    renderCalendar();
}});
renderCalendar();

// ===== EISENHOWER MATRIX =====
const STORAGE_KEY = 'claudia-eisenhower';

function defaultQuadrant(a) {{
    // Auto-assign: upcoming exams/midterms -> q1, near-term homework -> q1,
    // future important -> q2, recurring -> q3, rest -> q4
    if (a.status === 'completed') return null; // skip completed
    const title = a.title.toLowerCase();
    const isExam = title.includes('exam') || title.includes('midterm');
    const hasDate = !!a.due_date;
    const dueDate = hasDate ? dueDateTime(a) : null;
    const now = new Date();
    const daysOut = dueDate ? (dueDate - now) / 86400000 : 999;

    if (isExam && daysOut <= 21) return 'q1';
    if (isExam) return 'q2';
    if (hasDate && daysOut <= 7) return 'q1';
    if (hasDate && daysOut <= 21) return 'q2';
    if (a.status === 'recurring') return 'q3';
    if (hasDate) return 'q2';
    return 'q4';
}}

function loadMatrix() {{
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {{
        try {{ return JSON.parse(saved); }} catch(e) {{}}
    }}
    // Build default mapping: id -> quadrant
    const mapping = {{}};
    ASSIGNMENTS.forEach(a => {{
        const q = defaultQuadrant(a);
        if (q) mapping[a.id] = q;
    }});
    return mapping;
}}

function saveMatrix(mapping) {{
    localStorage.setItem(STORAGE_KEY, JSON.stringify(mapping));
}}

function renderMatrix() {{
    const mapping = loadMatrix();
    const byQ = {{ q1: [], q2: [], q3: [], q4: [] }};

    // Group assignments by quadrant
    for (const a of ASSIGNMENTS) {{
        const q = mapping[a.id];
        if (q && byQ[q]) byQ[q].push(a);
    }}

    for (const qid of ['q1','q2','q3','q4']) {{
        const container = document.querySelector(`#${{qid}} .q-items`);
        if (byQ[qid].length === 0) {{
            container.innerHTML = '<div class="matrix-empty">Drop items here</div>';
        }} else {{
            container.innerHTML = byQ[qid].map(a => `
                <div class="matrix-card" draggable="true" data-id="${{a.id}}">
                    ${{courseTag(a.course)}}
                    <span class="card-title">${{a.title}}</span>
                    <span class="card-due">${{formatDue(a)}}</span>
                </div>
            `).join('');
        }}
    }}

    // Drag and drop
    document.querySelectorAll('.matrix-card').forEach(card => {{
        card.addEventListener('dragstart', e => {{
            e.dataTransfer.setData('text/plain', card.dataset.id);
            card.classList.add('dragging');
        }});
        card.addEventListener('dragend', () => card.classList.remove('dragging'));
    }});

    document.querySelectorAll('.quadrant').forEach(quad => {{
        quad.addEventListener('dragover', e => {{
            e.preventDefault();
            quad.classList.add('drag-over');
        }});
        quad.addEventListener('dragleave', () => quad.classList.remove('drag-over'));
        quad.addEventListener('drop', e => {{
            e.preventDefault();
            quad.classList.remove('drag-over');
            const id = parseInt(e.dataTransfer.getData('text/plain'));
            const qid = quad.dataset.quadrant;
            const mapping = loadMatrix();
            mapping[id] = qid;
            saveMatrix(mapping);
            renderMatrix();
        }});
    }});
}}
renderMatrix();
</script>

</body>
</html>"""

    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"Dashboard generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_dashboard()
