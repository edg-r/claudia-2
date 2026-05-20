#!/usr/bin/env python3
"""
Generate a minimal Obsidian-ready daily dispatch from Claudia data.

Usage:
    python3 _claudia/daily_dispatch_md.py
"""

import argparse
import json
import re
import sqlite3
import subprocess
import sys
import tempfile
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "claudia.db"
DISPATCH_DIR = SCRIPT_DIR / "dispatches"
QUARTER_START = date(2026, 3, 30)

DONE_STATUSES = {"complete", "completed", "done", "submitted"}
ACTIVE_STATUSES = {"active", "in progress", "in_progress", "working", "drafting"}
COURSE_ORDER = ["GPCO 403", "GPCO 410", "GPEC 446", "GPPS 444", "GPPS 463"]
COURSE_EMOJIS = {
    "GPCO 403": "💵",
    "GPCO 410": "🌎",
    "GPEC 446": "📊",
    "GPPS 444": "⚔️",
    "GPPS 463": "🌏",
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--out", default="")
    parser.add_argument("--weather-summary", default="")
    parser.add_argument("--calendar-json", default="")
    parser.add_argument("--email-json", default="")
    parser.add_argument(
        "--auto-email",
        action="store_true",
        help="Collect local UCSD Gmail diagnostics/items when --email-json is not supplied.",
    )
    return parser.parse_args()


def parse_day(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def current_week(day):
    delta = (day - QUARTER_START).days
    if delta < 0:
        return 0
    return delta // 7 + 1


def week_end(day):
    return day + timedelta(days=(6 - day.weekday()))


def read_json(path):
    if not path:
        return None
    source = Path(path)
    if not source.exists():
        return None
    return json.loads(source.read_text(encoding="utf-8"))


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def query_courses(conn):
    rows = conn.execute(
        """
        SELECT id, code, name, professor, folder_path
        FROM courses
        ORDER BY code
        """
    ).fetchall()
    return [dict(row) for row in rows]


def query_assignments(conn, start, end):
    rows = conn.execute(
        """
        SELECT a.id, a.title, a.due_date, a.due_time, a.status, a.weight,
               a.notes, a.source_path, a.submitted_at, c.code, c.name AS course_name
        FROM assignments a
        LEFT JOIN courses c ON c.id = a.course_id
        WHERE a.due_date IS NOT NULL
          AND date(a.due_date) BETWEEN date(?) AND date(?)
        ORDER BY a.due_date, a.due_time, c.code, a.title
        """,
        (start.isoformat(), end.isoformat()),
    ).fetchall()
    return [dict(row) for row in rows]


def query_readings(conn, weeks):
    placeholders = ",".join("?" for _ in weeks)
    rows = conn.execute(
        f"""
        SELECT r.id, r.title, r.authors, r.week, r.summary_status, r.file_path,
               r.summary_path, r.pages, c.code, c.name AS course_name
        FROM readings r
        LEFT JOIN courses c ON c.id = r.course_id
        WHERE r.week IN ({placeholders})
        ORDER BY c.code, r.week, r.id
        """,
        tuple(weeks),
    ).fetchall()
    return [dict(row) for row in rows]


def rel(path):
    if not path:
        return ""
    candidate = Path(path)
    if candidate.is_absolute():
        try:
            return str(candidate.relative_to(ROOT))
        except ValueError:
            return str(candidate)
    return str(candidate)


def clean_inline(value):
    text = str(value or "").strip()
    text = re.sub(r"\s+", " ", text)
    text = text.replace("\u2014", "-").replace("\u2013", "-")
    return text.replace("[", "(").replace("]", ")")


def truncate(text, limit=140):
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def bold(text):
    return f"**{text}**" if text else text


def status_percent(item):
    status = clean_inline(item.get("status") or item.get("summary_status")).lower()
    haystack = " ".join(
        clean_inline(item.get(key)) for key in ("status", "notes", "title")
    )
    match = re.search(r"(\d{1,3})\s*%", haystack)
    if match:
        return max(0, min(100, int(match.group(1))))
    if item.get("submitted_at") or status in DONE_STATUSES:
        return 100
    if status in ACTIVE_STATUSES:
        return 50
    if status in {"pending", "", "todo", "not started"}:
        return 0
    return 25


def progress_bar(percent, width=10):
    filled = round((percent / 100) * width)
    return "[" + "#" * filled + "-" * (width - filled) + f"] {percent:>3}%"


def task_line(item):
    percent = status_percent(item)
    due_date = item.get("due_date") or "date unknown"
    due = item.get("due_time") or "all day"
    label = item["title"]
    title = bold(clean_inline(label))
    weight = clean_inline(item.get("weight"))
    weight_text = f" - ({weight} of grade)" if weight else ""
    status = clean_inline(item.get("status") or "pending")
    notes = truncate(clean_inline(item.get("notes")))
    lines = [
        f"- [ ] 📝 {due_date} {due} - {title}{weight_text}",
        f"  Progress: {progress_bar(percent)} - {status}",
    ]
    if notes:
        lines.append(f"  Description: {notes}")
    return "\n".join(lines)


def reading_line(item, label_prefix=""):
    label = item["title"]
    title = bold(clean_inline(label))
    pages = item.get("pages") or 0
    status = clean_inline(item.get("summary_status") or "pending")
    prefix = f"{label_prefix} " if label_prefix else ""
    lines = [f"- [ ] 📖 {prefix}{title}", f"  Status: {status}"]
    if pages:
        lines.append(f"  Pages: {pages} pp")
    return "\n".join(lines)


def load_schedule(calendar_json):
    data = read_json(calendar_json)
    if not data:
        return []
    if isinstance(data, dict):
        data = data.get("events", [])
    return data if isinstance(data, list) else []


def schedule_line(event):
    time_text = clean_inline(event.get("time") or event.get("start") or "time unknown")
    title = clean_inline(event.get("title") or event.get("summary") or "Untitled")
    location = clean_inline(event.get("location") or "No location")
    notes = clean_inline(event.get("notes") or event.get("description") or "")
    return f"- 🕒 {time_text} - {title} - {location} - {notes or 'No notes'}"


def load_email(email_json):
    data = read_json(email_json)
    if not isinstance(data, dict):
        return {"ucsd": [], "personal": []}
    return {
        "ucsd": data.get("ucsd", []) if isinstance(data.get("ucsd", []), list) else [],
        "personal": data.get("personal", [])
        if isinstance(data.get("personal", []), list)
        else [],
        "diagnostics": data.get("diagnostics", [])
        if isinstance(data.get("diagnostics", []), list)
        else [],
    }


def email_line(item):
    subject = clean_inline(item.get("subject") or item.get("title") or "Untitled")
    action = clean_inline(item.get("action") or item.get("summary") or "Review")
    confidence = clean_inline(item.get("confidence") or "unknown")
    draft_path = rel(item.get("draft_path") or item.get("draft") or "")
    draft = f" - draft: {draft_path}" if draft_path else ""
    return f"- [ ] ✉️ {subject} - {action} - confidence: {confidence}{draft}"


def collect_auto_email():
    helper = SCRIPT_DIR / "gmail_dispatch_json.py"
    if not helper.exists():
        return {"ucsd": [], "personal": [], "diagnostics": ["Email helper missing."]}
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        subprocess.run(
            [sys.executable, str(helper), "--out", str(tmp_path)],
            check=False,
            text=True,
            capture_output=True,
        )
        return load_email(str(tmp_path))
    finally:
        try:
            tmp_path.unlink()
        except FileNotFoundError:
            pass


def course_sort_key(course):
    code = course.get("code", "")
    try:
        return COURSE_ORDER.index(code)
    except ValueError:
        return len(COURSE_ORDER)


def course_heading(course):
    code = clean_inline(course.get("code"))
    name = clean_inline(course.get("name"))
    emoji = COURSE_EMOJIS.get(code, "🎓")
    if code and name:
        return f"{emoji} {code} - {name}"
    return f"{emoji} {code or name or 'Unknown Course'}"


def build_dispatch(day, weather, schedule, emails, courses, assignments, readings):
    end_this_week = week_end(day)
    end_next_week = end_this_week + timedelta(days=7)
    week = current_week(day)
    assignments_by_course = defaultdict(list)
    readings_by_course = defaultdict(list)
    for item in assignments:
        assignments_by_course[item.get("code", "")].append(item)
    for item in readings:
        readings_by_course[item.get("code", "")].append(item)

    lines = [
        f"# 🌅 Daily Dispatch - {day.strftime('%A, %B %-d, %Y')}",
        "",
        "## 🌤️ Weather",
        weather or "Weather unavailable. Eos should add the live La Jolla summary before final morning use.",
        "",
        "## 🗓️ Schedule",
    ]

    if schedule:
        lines.extend(schedule_line(event) for event in schedule)
    else:
        lines.append("- 🕒 No calendar data supplied.")

    lines.extend(["", "## 🎓 UCSD"])
    for course in sorted(courses, key=course_sort_key):
        code = course["code"]
        course_assignments = assignments_by_course.get(code, [])
        course_readings = readings_by_course.get(code, [])
        today_items = [
            item for item in course_assignments if item.get("due_date") == day.isoformat()
        ]
        week_items = [
            item
            for item in course_assignments
            if day.isoformat() < item.get("due_date", "") <= end_this_week.isoformat()
        ]
        next_items = [
            item
            for item in course_assignments
            if end_this_week.isoformat() < item.get("due_date", "") <= end_next_week.isoformat()
        ]
        this_week_readings = [item for item in course_readings if item.get("week") == week]
        next_week_readings = [item for item in course_readings if item.get("week") == week + 1]

        lines.extend(["", f"### {course_heading(course)}", "🔥 Due today"])
        lines.extend(task_line(item) for item in today_items)
        if not today_items:
            lines.append("- ✅ None")

        lines.append("📅 Rest of week")
        lines.extend(task_line(item) for item in week_items)
        if this_week_readings:
            lines.extend(reading_line(item, "Reading:") for item in this_week_readings)
        if not week_items and not this_week_readings:
            lines.append("- ✅ None")

        lines.append("🔭 Peek next week")
        lines.extend(task_line(item) for item in next_items)
        if next_week_readings:
            lines.extend(reading_line(item, "Reading:") for item in next_week_readings)
        if not next_items and not next_week_readings:
            lines.append("- ✅ None")

    lines.extend(["", "## 📬 UCSD Email"])
    if emails["ucsd"]:
        lines.extend(email_line(item) for item in emails["ucsd"])
    else:
        lines.append("- ✉️ No UCSD email summary supplied.")

    lines.extend(["", "## 🏠 Personal"])
    if emails["personal"]:
        lines.extend(email_line(item) for item in emails["personal"])
    else:
        lines.append("- ✉️ No personal email summary supplied.")

    diagnostics = emails.get("diagnostics", [])
    if diagnostics:
        lines.extend(["", "## 🛠️ Email Access Diagnostics"])
        lines.extend(f"- {clean_inline(item)}" for item in diagnostics)

    lines.extend(
        [
            "",
            "---",
            "Generated for: Edgar Agunias",
            f"Date: {day.isoformat()}",
            "Model: GPT-5 (Codex, medium reasoning) plus deterministic Python generator",
            "Sources: `_claudia/claudia.db`; optional Eos-supplied weather, calendar, and email JSON inputs when provided",
            "Agent: Hephaestus, for Eos daily dispatch use",
            "---",
        ]
    )
    return "\n".join(lines) + "\n"


def main():
    args = parse_args()
    day = parse_day(args.date)
    output_path = Path(args.out) if args.out else DISPATCH_DIR / f"{day.isoformat()}_daily-dispatch.md"
    lookahead_end = week_end(day) + timedelta(days=7)
    weeks = [current_week(day), current_week(day) + 1]

    conn = connect_db()
    try:
        courses = query_courses(conn)
        assignments = query_assignments(conn, day, lookahead_end)
        readings = query_readings(conn, weeks)
    finally:
        conn.close()

    output = build_dispatch(
        day=day,
        weather=args.weather_summary,
        schedule=load_schedule(args.calendar_json),
        emails=collect_auto_email()
        if args.auto_email and not args.email_json
        else load_email(args.email_json),
        courses=courses,
        assignments=assignments,
        readings=readings,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
