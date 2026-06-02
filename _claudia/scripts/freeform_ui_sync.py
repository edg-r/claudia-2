#!/usr/bin/env python3
"""
Apple Freeform On-Demand High-Res Vector PDF UI Sync
Part of the Hephaestus agent suite.
Automates Freeform via GUI scripting to export the last 10 modified boards as vector PDFs,
storing them in a centralized folder tree.
"""

import os
import sys
import re
import sqlite3
import shutil
import subprocess
import time
from datetime import datetime

# Workspace & Freeform config
WORKSPACE_DIR = "/Users/edgar/Documents/000 Files"
CLAUDIA_DB_PATH = os.path.join(WORKSPACE_DIR, "_claudia", "claudia.db")
CENTRALIZED_SYNC_DIR = os.path.join(WORKSPACE_DIR, "_claudia", "freeform_sync")
SPRING_2026_DIR = "02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter"
UNMATCHED_FREEFORM_DIR = "03 Resources/Freeform Sync Unsorted"

FREEFORM_GROUP_DIR = os.path.expanduser("~/Library/Group Containers/group.com.apple.freeform")
SNAPSHOT_PLIST_PATH = os.path.join(FREEFORM_GROUP_DIR, "Snapshot.plist")
BOARDS_DB_PATH = os.path.join(FREEFORM_GROUP_DIR, "Boards", "boards.db")

# Course definitions
COURSE_MAPPINGS = [
    {
        "id": 1,
        "code": "GPCO 403",
        "folder": os.path.join(SPRING_2026_DIR, "GPCO 403 - Intl Econ - Handley"),
        "keywords": ["gpco 403", "econ 403", "econ", "economics", "handley"]
    },
    {
        "id": 2,
        "code": "GPCO 410",
        "folder": os.path.join(SPRING_2026_DIR, "GPCO 410 - Intl Pol:Sec - Praether"),
        "keywords": ["gpco 410", "pol:sec", "p&s", "pol/sec", "politics & security", "politics and security", "praether", "intl p&s"]
    },
    {
        "id": 3,
        "code": "GPEC 446",
        "folder": os.path.join(SPRING_2026_DIR, "GPEC 446 - QM3 - Valasquez"),
        "keywords": ["gpec 446", "qm3", "qm 3", "qm", "quantitative", "valasquez", "methods 3"]
    },
    {
        "id": 4,
        "code": "GPPS 444",
        "folder": os.path.join(SPRING_2026_DIR, "GPPS 444 - History of Warfare - Thomas"),
        "keywords": ["gpps 444", "warfare", "history of warfare", "thomas"]
    },
    {
        "id": 5,
        "code": "GPPS 463",
        "folder": os.path.join(SPRING_2026_DIR, "GPPS 463 - Pol SEA - Ravanilla"),
        "keywords": ["gpps 463", "pol sea", "politics of sea", "polsea", "southeast asia", "ravanilla"]
    }
]

def sanitize_filename(name):
    """Sanitizes names to make them safe for files and directories."""
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def get_course_info(board_title):
    """Routes a board title to the correct course details based on keywords."""
    title_lower = board_title.lower()
    # Specifically prevent prior-term classes from matching
    if any(excl in title_lower for excl in ["qm1", "qm 1", "qm2", "qm 2"]):
        return UNMATCHED_FREEFORM_DIR, None
    for mapping in COURSE_MAPPINGS:
        if any(keyword in title_lower for keyword in mapping["keywords"]):
            return mapping["folder"], mapping["id"]
    return UNMATCHED_FREEFORM_DIR, None

def get_uuid_to_title_map():
    """Parses Snapshot.plist to build a mapping from Board UUID -> Board Title."""
    if not os.path.exists(SNAPSHOT_PLIST_PATH):
        print(f"Error: Snapshot.plist not found at {SNAPSHOT_PLIST_PATH}", file=sys.stderr)
        return {}

    try:
        import plistlib
        with open(SNAPSHOT_PLIST_PATH, "rb") as f:
            plist_data = plistlib.load(f)

        uuid_to_title = {}

        def extract_nodes(nodes):
            if not nodes:
                return
            for node in nodes:
                item = node.get("item")
                if item and "board" in item:
                    board = item["board"]
                    vm = board.get("viewModel")
                    if vm:
                        title = vm.get("title")
                        bi = vm.get("boardIdentifier")
                        if bi and "storage" in bi:
                            uuid = bi["storage"].get("boardUUID")
                            if uuid and title:
                                uuid_to_title[uuid.upper()] = title
                children = node.get("children")
                if children:
                    extract_nodes(children)

        extract_nodes(plist_data.get("rootNodes", []))
        return uuid_to_title
    except Exception as e:
        print(f"Error reading Snapshot.plist: {e}", file=sys.stderr)
        return {}

def hex_to_uuid(hex_str):
    """Converts a 32-character uppercase hex string to a hyphenated UUID format."""
    h = hex_str.upper()
    if len(h) != 32:
        return h
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"

def get_last_10_boards():
    """Queries boards.db via a temporary local copy to fetch the last 10 modified boards."""
    if not os.path.exists(BOARDS_DB_PATH):
        print(f"Error: boards.db not found at {BOARDS_DB_PATH}", file=sys.stderr)
        return []

    uuid_to_title = get_uuid_to_title_map()
    temp_db = "/tmp/boards_sync_temp.db"

    try:
        # Copy to avoid locking issues
        shutil.copy2(BOARDS_DB_PATH, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # Query boards ordered by last activity time (tombstoned = 0 are active boards)
        cursor.execute("SELECT hex(board_identifier), last_activity_time FROM boards WHERE tombstoned = 0 ORDER BY last_activity_time DESC;")
        rows = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Error querying boards.db: {e}", file=sys.stderr)
        return []
    finally:
        if os.path.exists(temp_db):
            try:
                os.remove(temp_db)
            except OSError:
                pass

    boards = []
    for hex_id, last_active in rows:
        uuid = hex_to_uuid(hex_id)
        title = uuid_to_title.get(uuid)
        if title:
            # Core Data timestamp is seconds since Jan 1 2001
            dt = datetime.fromtimestamp(last_active + 978307200)
            boards.append({
                "uuid": uuid,
                "title": title,
                "last_modified": dt.strftime("%Y-%m-%d %H:%M:%S")
            })
            if len(boards) >= 10:
                break

    return boards

def run_applescript(script_content):
    """Runs AppleScript and returns stdout, stderr, and success status."""
    process = subprocess.Popen(
        ['osascript', '-e', script_content],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    return process.returncode == 0, stdout.strip(), stderr.strip()

def automate_export(board_title, dest_path):
    """Executes macOS AppleScript GUI Scripting to automate Freeform PDF Export."""
    # Escape double quotes for AppleScript
    escaped_title = board_title.replace('"', '\\"')
    escaped_dest = dest_path.replace('"', '\\"')

    # We first activate Freeform
    # Then we use Cmd+F, type the board title, wait, press Down Arrow and Return to open the board.
    # Then File -> Export as PDF...
    # Then Cmd+Shift+G to specify the exact save destination.
    # Then press Return/Save and handle replace if it already exists.
    # Then close the window (Cmd+W).

    applescript_code = f"""
    tell application "Freeform" to activate
    delay 1.0

    tell application "System Events"
        tell process "Freeform"
            -- 1. Focus search using Cmd+F
            keystroke "f" using {{command down}}
            delay 0.5

            -- 2. Select all and delete any old search query
            keystroke "a" using {{command down}}
            key code 51 -- Delete key
            delay 0.2

            -- 3. Input board title to search
            keystroke "{escaped_title}"
            delay 1.5 -- Wait for search results to filter

            -- 4. Navigate down and open the board
            key code 125 -- Down Arrow to highlight the first result
            delay 0.2
            key code 36 -- Return to open the board
            delay 2.5 -- Wait for board window to open

            -- 5. Export as PDF
            click menu item "Export as PDF..." of menu "File" of menu bar item "File" of menu bar 1
            delay 1.5 -- Wait for export sheet

            -- 6. Open Go to Folder sheet using Cmd+Shift+G
            keystroke "g" using {{command down, shift down}}
            delay 0.8

            -- 7. Enter exact destination path
            keystroke "{escaped_dest}"
            delay 0.5
            key code 36 -- Confirm path
            delay 0.8

            -- 8. Confirm Save
            key code 36 -- Save/Export
            delay 1.5

            -- 9. Handle overwrite if "Replace" dialog appears
            if exists (sheet 1 of window 1) then
                click button "Replace" of sheet 1 of window 1
                delay 1.0
            end if

            -- 10. Close the board window using Cmd+W
            keystroke "w" using {{command down}}
            delay 0.5
        end tell
    end tell
    """

    return run_applescript(applescript_code)

def log_to_claudia_db(pdf_path, filename, course_id, summary):
    """Registers the high-res PDF path in claudia.db's files table."""
    rel_path = os.path.relpath(pdf_path, WORKSPACE_DIR)

    try:
        conn = sqlite3.connect(CLAUDIA_DB_PATH)
        cursor = conn.cursor()

        # Check if the file is already logged
        cursor.execute("SELECT id FROM files WHERE path = ?;", (rel_path,))
        row = cursor.fetchone()

        if not row:
            cursor.execute(
                "INSERT INTO files (path, filename, course_id, file_type, summary) VALUES (?, ?, ?, ?, ?);",
                (rel_path, filename, course_id, "pdf", summary)
            )
            conn.commit()
            print(f"Logged to Claudia DB: {rel_path}")
        else:
            # Update summary if already exists
            cursor.execute(
                "UPDATE files SET summary = ?, course_id = ? WHERE path = ?;",
                (summary, course_id, rel_path)
            )
            conn.commit()
            print(f"Updated Claudia DB entry for: {rel_path}")

        conn.close()
    except Exception as e:
        print(f"Error logging to claudia.db: {e}", file=sys.stderr)

def main():
    print("=============================================================")
    print("Starting Apple Freeform High-Res UI Sync Transition...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=============================================================")

    # 1. Fetch top 10 modified boards
    boards = get_last_10_boards()
    if not boards:
        print("No active boards found in database.", file=sys.stderr)
        sys.exit(1)

    print(f"Identified the last 10 modified boards:")
    for idx, b in enumerate(boards):
        print(f"  {idx+1}. {b['title']} (Modified: {b['last_modified']})")

    print("\n-------------------------------------------------------------")
    print("Executing AppleScript GUI Export...")
    print("-------------------------------------------------------------")

    success_count = 0
    accessibility_error_triggered = False

    for idx, board in enumerate(boards):
        title = board["title"]
        sanitized = sanitize_filename(title)
        course_folder, course_id = get_course_info(title)

        dest_dir = os.path.join(CENTRALIZED_SYNC_DIR, course_folder)
        os.makedirs(dest_dir, exist_ok=True)

        dest_pdf_path = os.path.join(dest_dir, f"{sanitized}.pdf")

        print(f"[{idx+1}/10] Exporting '{title}' -> '{course_folder}/{sanitized}.pdf'...")

        success, stdout, stderr = automate_export(title, dest_pdf_path)

        if success:
            print(f"  Successfully exported board to PDF.")
            # Register in Claudia DB
            summary = f"Apple Freeform high-res vector PDF sync for board: {title}"
            log_to_claudia_db(dest_pdf_path, f"{sanitized}.pdf", course_id, summary)
            success_count += 1
        else:
            print(f"  FAILED to export board '{title}'.")
            if "assistive access" in stderr or "assistive access" in stdout or "-1719" in stderr:
                accessibility_error_triggered = True
                print("  Reason: macOS Accessibility/Assistive Access permissions are missing.", file=sys.stderr)
                break
            else:
                print(f"  Error Details: {stderr or stdout}", file=sys.stderr)

    print("\n=============================================================")
    if accessibility_error_triggered:
        print("CRITICAL: The script failed due to macOS security sandbox constraints.")
        print("To enable Freeform UI Sync automation, please grant 'Accessibility' permission to your Terminal or IDE.")
        print("Steps:")
        print("  1. Open System Settings -> Privacy & Security -> Accessibility.")
        print("  2. Click '+' and add your Terminal (e.g. iTerm, Terminal.app) or IDE.")
        print("  3. Toggle the switch to blue to enable it.")
        print("  4. Rerun this script: python3 _claudia/scripts/freeform_ui_sync.py")
        sys.exit(1)
    else:
        print(f"Sync complete. Successfully processed {success_count}/10 boards.")
    print("=============================================================")

if __name__ == "__main__":
    main()
