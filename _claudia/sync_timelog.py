import csv
import sqlite3
import os
from datetime import datetime

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "admin", "GPS_TimeTracker_Spring2026.xlsx - Time Log.csv")
DB_PATH = os.path.join(os.path.dirname(__file__), "claudia.db")

HEADER_KEYWORDS = {"date", "course", "title", "category", "start", "end", "duration", "pages"}


def is_data_row(row):
    if not row or not row[0].strip():
        return False
    date_val = row[0].strip()
    if date_val.lower() in HEADER_KEYWORDS:
        return False
    if date_val.startswith("GPS") or date_val.startswith("GPCO") or date_val.startswith("GPEC") or date_val.startswith("GPPS"):
        return False
    if date_val.startswith("💡"):
        return False
    try:
        datetime.strptime(date_val, "%m/%d/%Y")
        return True
    except ValueError:
        pass
    try:
        datetime.strptime(date_val, "%m/%d/%0Y")
        return True
    except ValueError:
        pass
    return False


def parse_date(raw):
    for fmt in ("%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(raw.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return raw.strip()


def parse_float(val):
    try:
        return float(val.strip()) if val and val.strip() else None
    except ValueError:
        return None


def parse_int(val):
    try:
        return int(val.strip()) if val and val.strip() else None
    except ValueError:
        return None


def sync():
    rows_imported = []

    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            if not is_data_row(row):
                continue
            # Columns: Date, Course, Title/Task, Category, Start, End, Duration, RunningTotal, %Week, PagesRead, Notes, ...
            date = parse_date(row[0])
            course_code = row[1].strip() if len(row) > 1 else None
            title = row[2].strip() if len(row) > 2 else None
            category = row[3].strip() if len(row) > 3 else None
            start_time = row[4].strip() if len(row) > 4 else None
            end_time = row[5].strip() if len(row) > 5 else None
            duration_hrs = parse_float(row[6]) if len(row) > 6 else None
            pages_read = parse_int(row[9]) if len(row) > 9 else None
            notes = row[10].strip() if len(row) > 10 else None

            if not course_code or not title:
                continue

            rows_imported.append((date, course_code, title, category, start_time, end_time, duration_hrs, pages_read, notes))

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DELETE FROM time_log")
    cur.executemany(
        "INSERT INTO time_log (date, course_code, title, category, start_time, end_time, duration_hrs, pages_read, notes) VALUES (?,?,?,?,?,?,?,?,?)",
        rows_imported,
    )
    conn.commit()

    # Summary
    total_hrs = sum(r[6] for r in rows_imported if r[6] is not None)
    courses = sorted(set(r[1] for r in rows_imported))
    by_course = {}
    for r in rows_imported:
        c = r[1]
        by_course[c] = by_course.get(c, 0) + (r[6] or 0)

    print(f"Time log sync complete.")
    print(f"  Rows imported : {len(rows_imported)}")
    print(f"  Total hours   : {total_hrs:.2f}")
    print(f"  Courses       : {', '.join(courses)}")
    print()
    for c in sorted(by_course):
        print(f"  {c}: {by_course[c]:.2f} hrs")

    conn.close()


if __name__ == "__main__":
    sync()
