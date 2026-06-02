# macOS-Native Setup Checklist

Use this checklist on the Mac mini. These are manual settings, not commands for the scripts to change.

## Canonical Folder

- Confirm the Claudia workspace exists at `/Users/edgar/Documents/000 Files`.
- Keep generated databases, dashboards, logs, and LaunchAgents on the Mac mini by default.
- Avoid putting the whole Claudia runtime inside iCloud Drive.

## File Sharing / SMB

- Open System Settings > General > Sharing.
- Turn on File Sharing.
- Add `/Users/edgar/Documents/000 Files` as a shared folder if it is not already available through Edgar's home folder.
- Set access for Edgar's account only unless a broader share is intentional.
- From the MacBook Air, connect using Finder > Go > Connect to Server with `smb://<mac-mini-name>.local`.

## Remote Login / SSH

- Open System Settings > General > Sharing.
- Turn on Remote Login for Edgar's account.
- From the MacBook Air, connect with `ssh edgar@<mac-mini-name>.local`.
- Prefer SSH for maintenance commands and log inspection.

## Screen Sharing

- Open System Settings > General > Sharing.
- Turn on Screen Sharing for Edgar's account.
- Use it for GUI checks, permission prompts, and visual maintenance.

## Time Machine

- Attach or select the Mac mini backup destination.
- Confirm Time Machine includes `/Users/edgar/Documents/000 Files`.
- Exclude caches only if backup size becomes a problem.

## launchd

- Review `_claudia/infra/launchd/com.claudia.daily-maintenance.plist.example`.
- Copy it manually to `~/Library/LaunchAgents/com.claudia.daily-maintenance.plist` only after review.
- Load it manually with `launchctl` when ready.

## Shortcuts

- Optional: create a Shortcut that SSHes into the Mac mini and runs `_claudia/infra/daily_maintenance.sh`.
- Optional: create a Shortcut that opens the Mac mini shared folder in Finder.

## iCloud Drive

- Use iCloud Drive only for selected outputs Edgar wants everywhere.
- Good candidates: exported PDFs, briefing Markdown, screenshots, or final dashboard snapshots.
- Avoid syncing `_claudia/claudia.db`, `_claudia/infra/logs/`, caches, and runtime folders through iCloud Drive.

## Syncthing Later

- Treat Syncthing as a later full-mirror option, not the initial default.
- If enabled later, start from `_claudia/infra/syncthing_ignore_template.txt`.
- Do not run database-generating jobs on both machines at the same time.
