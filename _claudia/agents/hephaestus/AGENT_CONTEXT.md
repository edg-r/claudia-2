# Hephaestus - Agent Context

**Role:** Coding and implementation agent
**Domain:** Software engineering, scripting, web development, data tooling

## Workspace Technical Notes

### Apple Freeform Local Sync Engine (`_claudia/scripts/freeform_sync.py`)
- **Purpose:** Extracts canvas previews, embedded slides/PDFs/images from Apple Freeform local containers and routes them to course-specific folders.
- **Course Mappings:** Mappings are defined in `COURSE_MAPPINGS`. Keywords are evaluated case-insensitively. Shorthands like 'polsea', 'politics of sea' route to GPPS 463; 'p&s', 'pol/sec', and 'pol:sec' route to GPCO 410.
- **Exclusion Rules:** Prior-term classes containing 'qm1', 'qm 1', 'qm2', or 'qm 2' are explicitly prevented from matching GPEC 446 (QM3) in `get_course_info()` and route to `03 Resources/Freeform Sync Unsorted` instead.
- **Database Logging:** Sync operations are registered in `_claudia/claudia.db` in the `files` table to track synced previews and assets.

## PARA Workspace Layout
- Current workspace root remains `/Users/edgar/Documents/000 Files`.
- Active projects live in `01 Projects/`.
- Ongoing areas live in `02 Areas/`; active Spring 2026 course folders live under `02 Areas/2025-2027 UCSD GPS/2026-4 Spring Quarter/`.
- Reusable references live in `03 Resources/`.
- Course-agent manifest memory paths and generated `.codex/agents/*.toml` configs must point to the moved course `_agent/` folders.
- Root-level `admin/` and `Personal Projects/` shells were removed during the PARA migration; route future admin and personal-finance files into the appropriate Area.

### macOS LaunchAgent Daemon (`/Users/edgar/Library/LaunchAgents/com.claudia.freeformsync.plist`)
- **Label:** `com.claudia.freeformsync`
- **Interpreter:** Explicitly uses `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` to bypass macOS sandbox/TCC restrictions associated with the Command Line Tools python3 stub `/usr/bin/python3`.
- **Triggers:** Automatically runs every 900 seconds (15-minute interval) or whenever changes are detected in either `/Users/edgar/Library/Group Containers/group.com.apple.freeform/Snapshot.plist` or `/Users/edgar/Library/Group Containers/group.com.apple.freeform/Boards/boards.db`.
- **Logs:** Outputs stdout and stderr to `/Users/edgar/Documents/000 Files/_claudia/dispatches/freeform_sync.log`.
- **Launchctl Commands:**
  - Bootstrap: `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.claudia.freeformsync.plist`
  - Enable: `launchctl enable gui/$(id -u)/com.claudia.freeformsync`
  - Restart: `launchctl kickstart -k gui/$(id -u)/com.claudia.freeformsync`

## Artifact Archive Protocol
Superseded AI-generated or iterative artifacts now belong in the course-local archive under `[Course Folder]/.archive/<project_slug>/`, with mappings recorded in `[Course Folder]/.archive/ARCHIVE_INDEX.md`. Technical cleanup scripts should keep source readings, professor-provided files, final submitted files, and the latest active working/clean/submission candidate visible, while moving older generated PDFs, notes sidecars, build scripts, tracked copies, and partial outputs into the course-local archive. Do not rely on Git alone for binary rollback.
