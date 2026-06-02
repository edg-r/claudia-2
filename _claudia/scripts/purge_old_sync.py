#!/usr/bin/env python3
"""
Purges the old Freeform sync database entries and files.
Part of the Hephaestus agent cleanup.
"""

import os
import shutil
import sqlite3

WORKSPACE_DIR = "/Users/edgar/Documents/000 Files"
CLAUDIA_DB_PATH = os.path.join(WORKSPACE_DIR, "_claudia", "claudia.db")

COURSE_FOLDERS = [
    "02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPCO 403 - Intl Econ - Handley",
    "02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPCO 410 - Intl Pol:Sec - Praether",
    "02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPEC 446 - QM3 - Valasquez",
    "02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPPS 444 - History of Warfare - Thomas",
    "02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/GPPS 463 - Pol SEA - Ravanilla",
    "03 Resources/Freeform Sync Unsorted"
]

def purge_db():
    print("Connecting to Claudia DB...")
    if not os.path.exists(CLAUDIA_DB_PATH):
        print(f"Error: Database not found at {CLAUDIA_DB_PATH}")
        return

    try:
        conn = sqlite3.connect(CLAUDIA_DB_PATH)
        cursor = conn.cursor()

        # Count matching rows first
        cursor.execute("SELECT COUNT(*) FROM files WHERE summary LIKE '%Apple Freeform%';")
        count = cursor.fetchone()[0]
        print(f"Found {count} database rows related to 'Apple Freeform'.")

        if count > 0:
            cursor.execute("DELETE FROM files WHERE summary LIKE '%Apple Freeform%';")
            conn.commit()
            print(f"Successfully deleted {count} rows from the 'files' table.")
        else:
            print("No rows required deletion.")

        conn.close()
    except Exception as e:
        print(f"Error executing database purge: {e}")

def purge_files():
    print("\nScanning for old 'Freeform Sync' directories...")
    deleted_count = 0

    # We walk the directories to find any subdirectory named "Freeform Sync"
    for base in COURSE_FOLDERS:
        base_path = os.path.join(WORKSPACE_DIR, base)
        if not os.path.exists(base_path):
            continue

        for root, dirs, files in os.walk(base_path, topdown=False):
            for d in dirs:
                if d == "Freeform Sync":
                    full_path = os.path.join(root, d)
                    print(f"Removing old sync directory: {full_path}")
                    try:
                        shutil.rmtree(full_path)
                        deleted_count += 1
                    except Exception as e:
                        print(f"Error removing {full_path}: {e}")

    print(f"Completed directory purge. Removed {deleted_count} 'Freeform Sync' directories.")

def main():
    print("=== Hephaestus Old Freeform Sync Purge Tool ===")
    purge_db()
    purge_files()
    print("=== Purge Completed ===")

if __name__ == "__main__":
    main()
