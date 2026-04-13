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
CURRENT_WEEK = 3
TOTAL_WEEKS = 11

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


def generate_dashboard():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

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

    assignments = query_db(conn, """
        SELECT a.id, a.title, a.due_date, a.status, a.grade, a.weight, a.notes,
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
        course_stats.append({
            "code": code, "name": c["name"], "professor": c["professor"],
            "files": files, "readings": readings, "assignments": assigns, "embeddings": embeds,
        })

    readings_data = query_db(conn, """
        SELECT r.title, r.authors, r.week, r.summary_status, c.code
        FROM readings r
        LEFT JOIN courses c ON r.course_id = c.id
        ORDER BY c.code, r.week, r.title
    """)

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
        if week is not None and week <= 2:
            status = "completed"
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
        course_rows += f'<tr><td><strong>{label}</strong></td><td>{cs["professor"]}</td><td>{cs["files"]}</td><td>{cs["readings"]}</td><td>{cs["assignments"]}</td><td>{cs["embeddings"]}</td></tr>'

    # Coverage table
    coverage_rows = ""
    for cs in course_stats:
        total_c = cs["files"]
        emb_c = cs["embeddings"]
        pct = coverage_pct(emb_c, total_c)
        bar_w = (emb_c / total_c * 100) if total_c > 0 else 0
        label = course_label(cs["code"], cs["name"])
        coverage_rows += f'<tr><td>{label}</td><td>{emb_c} / {total_c}</td><td><div class="bar-bg"><div class="bar-fill" style="width:{bar_w}%"></div></div></td><td>{pct}</td></tr>'

    # Readings table
    readings_rows = ""
    current_course = None
    for r in readings_data:
        code = r["code"] or "Unassigned"
        if code != current_course:
            current_course = code
            label = course_label(code, course_name_map.get(code, ""))
            readings_rows += f'<tr class="course-header"><td colspan="4">{label}</td></tr>'
        status_cls = "summarized" if r["summary_status"] != "pending" else "pending-reading"
        readings_rows += f'<tr class="{status_cls}"><td>W{r["week"] or "?"}</td><td>{r["title"]}</td><td>{r["authors"] or ""}</td><td>{r["summary_status"] or "pending"}</td></tr>'

    # Logs table
    log_rows = ""
    for l in logs:
        log_rows += f'<tr><td>{l["timestamp"] or ""}</td><td>{l["agent"] or ""}</td><td>{l["action"] or ""}</td><td>{(l["details"] or "")[:120]}</td></tr>'
    if not logs:
        log_rows = '<tr><td colspan="4">No activity logged yet.</td></tr>'

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
    padding: 2rem;
    line-height: 1.5;
}}
h1 {{ font-size: 1.8rem; margin-bottom: 0.25rem; color: #fff; }}
.subtitle {{ color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1.5rem; }}
h2 {{
    font-size: 1.2rem; color: #ccc; margin-bottom: 1rem;
    padding-bottom: 0.5rem; border-bottom: 1px solid var(--border);
}}

/* Cards */
.cards {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem; margin-bottom: 2rem;
}}
.card {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 1.25rem; text-align: center;
}}
.card-value {{ font-size: 2rem; font-weight: 700; color: #fff; }}
.card-label {{ font-size: 0.85rem; color: #999; margin-top: 0.25rem; }}
.card-sub {{ font-size: 0.75rem; color: var(--text-dim); margin-top: 0.25rem; }}

/* Tabs */
.tab-bar {{
    display: flex; gap: 0; margin-bottom: 1.5rem;
    border-bottom: 2px solid var(--border);
}}
.tab-btn {{
    padding: 0.6rem 1.4rem; cursor: pointer;
    background: none; border: none; color: var(--text-muted);
    font-size: 0.9rem; font-weight: 500;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px; transition: all 0.15s;
}}
.tab-btn:hover {{ color: #fff; }}
.tab-btn.active {{ color: var(--accent); border-bottom-color: var(--accent); }}
.tab-panel {{ display: none; }}
.tab-panel.active {{ display: block; }}

/* Section */
.section {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem;
}}

/* Tables */
table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
th {{
    text-align: left; padding: 0.5rem 0.75rem;
    border-bottom: 1px solid #333; color: #999;
    font-weight: 600; font-size: 0.8rem;
    text-transform: uppercase; letter-spacing: 0.05em;
}}
td {{ padding: 0.5rem 0.75rem; border-bottom: 1px solid #1f1f1f; }}
tr:hover {{ background: #222; }}
tr.overdue td {{ color: #ff6b6b; }}
tr.soon td {{ color: #ffa94d; }}
tr.completed td {{ color: #69db7c; text-decoration: line-through; opacity: 0.7; }}
tr.course-header td {{
    font-weight: 700; color: var(--accent);
    padding-top: 1rem; border-bottom: 1px solid #333; font-size: 0.9rem;
}}
tr.exam-row td {{ font-weight: 600; }}
tr.pending-reading td {{ color: var(--text); }}
tr.summarized td {{ color: #69db7c; }}
.bar-bg {{ background: var(--border); border-radius: 4px; height: 8px; width: 100%; overflow: hidden; }}
.bar-fill {{ background: var(--accent); height: 100%; border-radius: 4px; }}
p {{ margin-bottom: 1rem; color: #999; font-size: 0.85rem; }}

/* ===== WEEK VIEW ===== */
.week-group {{
    margin-bottom: 1rem;
}}
.week-header {{
    display: flex; align-items: center; gap: 0.75rem;
    padding: 0.6rem 0; cursor: pointer; user-select: none;
}}
.week-header h3 {{
    font-size: 0.95rem; color: #ccc; font-weight: 600;
}}
.week-header .week-dates {{
    font-size: 0.78rem; color: var(--text-dim);
}}
.week-header .badge {{
    font-size: 0.7rem; padding: 0.15rem 0.5rem;
    border-radius: 10px; font-weight: 600;
}}
.badge-current {{ background: var(--accent); color: #000; }}
.badge-completed {{ background: #2d4a2d; color: #69db7c; }}
.week-items {{
    padding-left: 1rem; border-left: 2px solid var(--border);
    margin-left: 0.5rem;
}}
.week-group.current .week-items {{ border-left-color: var(--accent); }}
.week-group.past .week-header h3 {{ color: var(--text-dim); }}
.week-group.past .week-items {{ opacity: 0.5; }}
.week-item {{
    display: flex; align-items: center; gap: 0.75rem;
    padding: 0.4rem 0.75rem; font-size: 0.85rem;
    border-radius: 4px; margin-bottom: 2px;
}}
.week-item:hover {{ background: #222; }}
.week-item .course-tag {{
    font-size: 0.7rem; font-weight: 700;
    padding: 0.1rem 0.45rem; border-radius: 4px;
    white-space: nowrap;
}}
.week-item .due {{ color: var(--text-dim); font-size: 0.78rem; margin-left: auto; white-space: nowrap; }}
.week-item.completed-item {{ text-decoration: line-through; color: var(--text-dim); }}
.week-no-items {{ padding: 0.4rem 0.75rem; font-size: 0.8rem; color: var(--text-dim); font-style: italic; }}

/* ===== CALENDAR VIEW ===== */
.cal-controls {{
    display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;
}}
.cal-controls button {{
    background: var(--surface); border: 1px solid var(--border);
    color: var(--text); padding: 0.35rem 0.8rem; border-radius: 6px;
    cursor: pointer; font-size: 0.85rem;
}}
.cal-controls button:hover {{ border-color: var(--accent); }}
.cal-controls .cal-month-label {{ font-size: 1.1rem; font-weight: 600; color: #fff; min-width: 160px; text-align: center; }}
.cal-grid {{
    display: grid; grid-template-columns: repeat(7, 1fr); gap: 1px;
    background: var(--border); border-radius: 8px; overflow: hidden;
}}
.cal-day-header {{
    background: #222; padding: 0.4rem; text-align: center;
    font-size: 0.75rem; color: var(--text-muted); font-weight: 600;
    text-transform: uppercase;
}}
.cal-day {{
    background: var(--surface); min-height: 80px; padding: 0.35rem;
    position: relative;
}}
.cal-day.empty {{ background: #141414; }}
.cal-day.today {{ outline: 2px solid var(--accent); outline-offset: -2px; z-index: 1; }}
.cal-day .day-num {{
    font-size: 0.75rem; color: var(--text-dim); margin-bottom: 0.2rem;
}}
.cal-day.today .day-num {{ color: var(--accent); font-weight: 700; }}
.cal-event {{
    font-size: 0.65rem; padding: 0.15rem 0.3rem;
    border-radius: 3px; margin-bottom: 2px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    cursor: default; color: #000; font-weight: 600;
}}
.cal-event:hover {{ filter: brightness(1.15); }}

/* ===== EISENHOWER MATRIX ===== */
.matrix-container {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
    gap: 1rem;
}}
.matrix-label-row {{
    display: contents;
}}
.matrix-col-label {{
    text-align: center; font-size: 0.8rem; font-weight: 700;
    color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em;
    padding-bottom: 0.25rem;
}}
.quadrant {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 1rem; min-height: 220px;
    transition: border-color 0.15s;
}}
.quadrant.drag-over {{ border-color: var(--accent); background: #1e2a1e; }}
.quadrant-header {{
    display: flex; align-items: center; gap: 0.5rem;
    margin-bottom: 0.75rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}}
.quadrant-header .q-icon {{ font-size: 1rem; }}
.quadrant-header .q-title {{ font-size: 0.85rem; font-weight: 700; }}
.quadrant-header .q-subtitle {{ font-size: 0.7rem; color: var(--text-dim); }}
.q1 .quadrant-header {{ color: #ff6b6b; }}
.q2 .quadrant-header {{ color: #ffa94d; }}
.q3 .quadrant-header {{ color: var(--accent); }}
.q4 .quadrant-header {{ color: var(--text-dim); }}
.matrix-row-label {{
    writing-mode: vertical-lr; transform: rotate(180deg);
    font-size: 0.8rem; font-weight: 700; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.08em;
    display: flex; align-items: center; justify-content: center;
    padding: 0 0.25rem;
}}
.matrix-card {{
    display: flex; align-items: center; gap: 0.5rem;
    padding: 0.45rem 0.6rem; margin-bottom: 0.35rem;
    background: #222; border: 1px solid #333; border-radius: 6px;
    font-size: 0.8rem; cursor: grab;
    transition: transform 0.1s, box-shadow 0.1s;
}}
.matrix-card:active {{ cursor: grabbing; }}
.matrix-card.dragging {{ opacity: 0.4; }}
.matrix-card .course-tag {{
    font-size: 0.65rem; font-weight: 700;
    padding: 0.1rem 0.35rem; border-radius: 3px;
    white-space: nowrap;
}}
.matrix-card .card-title {{ flex: 1; }}
.matrix-card .card-due {{ font-size: 0.7rem; color: var(--text-dim); white-space: nowrap; }}
.matrix-empty {{ font-size: 0.78rem; color: var(--text-dim); font-style: italic; padding: 0.5rem; }}

/* Course tag colors */
{" ".join(f'.tag-{code.replace(" ","")} {{ background: {color}; color: #000; }}' for code, color in COURSE_COLORS.items())}

/* Legend */
.legend {{
    display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem;
}}
.legend-item {{
    display: flex; align-items: center; gap: 0.35rem; font-size: 0.78rem; color: var(--text-muted);
}}
.legend-dot {{
    width: 10px; height: 10px; border-radius: 2px;
}}

/* Collapsible */
.collapsible {{ margin-bottom: 1.5rem; }}
.collapsible-header {{
    display: flex; align-items: center; gap: 0.5rem;
    cursor: pointer; user-select: none; padding: 0.75rem 1rem;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; margin-bottom: 0;
}}
.collapsible-header h2 {{ margin: 0; padding: 0; border: none; }}
.collapsible-header .chevron {{
    color: var(--text-dim); transition: transform 0.2s; font-size: 0.8rem;
}}
.collapsible-header.open .chevron {{ transform: rotate(90deg); }}
.collapsible-header.open {{ border-radius: 8px 8px 0 0; margin-bottom: 0; }}
.collapsible-body {{
    display: none; background: var(--surface);
    border: 1px solid var(--border); border-top: none;
    border-radius: 0 0 8px 8px; padding: 1rem 1.5rem;
}}
.collapsible-body.open {{ display: block; }}
</style>
</head>
<body>

<h1>Claudia Dashboard</h1>
<div class="subtitle">Generated {now.strftime('%Y-%m-%d %H:%M:%S')} &middot; Spring 2026 &middot; UC San Diego GPS &middot; Week {CURRENT_WEEK}</div>

<!-- Summary Cards -->
<div class="cards">
    <div class="card"><div class="card-value">{len(courses)}</div><div class="card-label">Courses</div></div>
    <div class="card"><div class="card-value">{total_files}</div><div class="card-label">Files Tracked</div></div>
    <div class="card"><div class="card-value">{total_readings}</div><div class="card-label">Readings</div><div class="card-sub">{pending_readings} pending / {summarized_readings} summarized</div></div>
    <div class="card"><div class="card-value">{total_assignments}</div><div class="card-label">Assignments</div><div class="card-sub">{upcoming_assignments} upcoming / {completed_assignments} completed</div></div>
    <div class="card"><div class="card-value">{total_embeddings}</div><div class="card-label">Embedding Chunks</div><div class="card-sub">{total_embedded_files} files indexed</div></div>
</div>

<!-- Legend -->
<div class="legend">
    {"".join(f'<div class="legend-item"><div class="legend-dot" style="background:{color}"></div>{code}</div>' for code, color in COURSE_COLORS.items())}
</div>

<!-- Tabs -->
<div class="tab-bar">
    <button class="tab-btn active" data-tab="week">Week View</button>
    <button class="tab-btn" data-tab="calendar">Calendar</button>
    <button class="tab-btn" data-tab="eisenhower">Eisenhower Matrix</button>
</div>

<!-- Week View -->
<div class="tab-panel active" id="tab-week">
    <div id="week-view"></div>
</div>

<!-- Calendar View -->
<div class="tab-panel" id="tab-calendar">
    <div class="cal-controls">
        <button id="cal-prev">&larr;</button>
        <div class="cal-month-label" id="cal-month-label"></div>
        <button id="cal-next">&rarr;</button>
    </div>
    <div id="cal-grid-container"></div>
</div>

<!-- Eisenhower Matrix -->
<div class="tab-panel" id="tab-eisenhower">
    <p>Drag assignments between quadrants. Your arrangement is saved locally.</p>
    <div style="display:grid; grid-template-columns: auto 1fr 1fr; grid-template-rows: auto auto auto; gap: 0;">
        <div></div>
        <div class="matrix-col-label" style="padding:0.5rem">Urgent</div>
        <div class="matrix-col-label" style="padding:0.5rem">Not Urgent</div>

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

<!-- Collapsible static sections -->
<div style="margin-top:2rem;">

<div class="collapsible">
    <div class="collapsible-header" onclick="toggleCollapse(this)">
        <span class="chevron">&#9654;</span><h2>Per-Course Breakdown</h2>
    </div>
    <div class="collapsible-body">
        <table><thead><tr><th>Course</th><th>Professor</th><th>Files</th><th>Readings</th><th>Assignments</th><th>Embedded</th></tr></thead>
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
        <span class="chevron">&#9654;</span><h2>Readings Status</h2>
    </div>
    <div class="collapsible-body">
        <table><thead><tr><th>Week</th><th>Title</th><th>Authors</th><th>Status</th></tr></thead>
        <tbody>{readings_rows}</tbody></table>
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
const CURRENT_WEEK = {CURRENT_WEEK};
const COURSE_COLORS = {json.dumps(COURSE_COLORS)};

// --- Tabs ---
document.querySelectorAll('.tab-btn').forEach(btn => {{
    btn.addEventListener('click', () => {{
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
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

        const dateRange = formatDate(weekStart.toISOString().slice(0,10)) + ' - ' + formatDate(weekEnd.toISOString().slice(0,10));

        html += `<div class="week-group ${{cls}}">`;
        html += `<div class="week-header" onclick="this.parentElement.querySelector('.week-items').classList.toggle('collapsed')">`;
        html += `<h3>Week ${{w}}</h3><span class="week-dates">${{dateRange}}</span>${{badge}}`;
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
            html += `<span class="due">${{formatDate(a.due_date)}}</span>`;
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
    const todayStr = new Date().toISOString().slice(0,10);

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
            html += `<div class="cal-event" style="background:${{bg}}" title="${{a.course}}: ${{a.title}}">${{a.title}}</div>`;
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
    const dueDate = hasDate ? new Date(a.due_date + 'T00:00:00') : null;
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
                    <span class="card-due">${{formatDate(a.due_date)}}</span>
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
