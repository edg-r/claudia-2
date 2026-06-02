# Claudia Mac mini Infrastructure

Purpose: keep the Mac mini as the always-on canonical Claudia operations box, while the MacBook Air remains a fast local machine with macOS-native access into the canonical workspace.

## Machine Roles

- Mac mini: canonical workspace, scheduled maintenance, local Claudia services, long-running jobs, logs, and backups.
- MacBook Air: mobile editing and review machine that accesses the Mac mini over the LAN when the canonical workspace is needed.
- Source of truth: files under `/Users/edgar/Documents/000 Files` on the Mac mini.

## Default Access Model

Use macOS-native infrastructure first:

- File Sharing / SMB: LAN access to the canonical workspace from the MacBook Air.
- Remote Login / SSH: terminal maintenance from the MacBook Air.
- Screen Sharing: GUI maintenance when a visual session is easier.
- Time Machine: Mac mini backup for the canonical workspace.
- launchd: scheduled local checks and maintenance.
- Shortcuts: optional manual triggers for common commands.
- iCloud Drive: optional selected user-facing outputs only, not the whole Claudia runtime.

## Bootstrap

On a new Mac mini, review then run:

```bash
cd "/Users/edgar/Documents/000 Files"
bash _claudia/infra/bootstrap_mac_mini.sh
```

The bootstrap script checks expected tools and folders, creates local log folders, and prints next manual steps. It does not install packages or modify LaunchAgents by itself.

For the manual System Settings checklist, use `_claudia/infra/macos_native_setup_checklist.md`.

## Daily Maintenance

The daily script is launchd-ready:

```bash
bash _claudia/infra/daily_maintenance.sh
```

To enable it later, copy `_claudia/infra/launchd/com.claudia.daily-maintenance.plist.example` to `~/Library/LaunchAgents/com.claudia.daily-maintenance.plist`, review paths, then load it manually with `launchctl`.

## Optional iCloud Outputs

iCloud Drive is best reserved for selected human-facing exports, such as a dashboard snapshot, PDF, memo, or briefing Edgar wants available everywhere. Avoid putting `_claudia/claudia.db`, logs, caches, or full runtime folders in iCloud Drive.

## Optional Later Sync

Syncthing is not the default infrastructure path. If Edgar later wants a full bidirectional mirror, `_claudia/infra/syncthing_ignore_template.txt` is retained as a starting policy. Treat it as an optional future route, and avoid two machines editing generated databases or logs at the same time.

## Operating Pattern

1. Keep Claudia's canonical runtime on the Mac mini.
2. Use SMB, SSH, or Screen Sharing from the MacBook Air when working against canonical files.
3. Prefer the Mac mini for scheduled jobs and database-generating maintenance.
4. Export only selected outputs to iCloud Drive if Edgar wants convenient access outside the LAN.
5. Keep LaunchAgents installed only on the Mac mini unless Edgar explicitly wants mirrored automation.
6. If full file sync is added later, resolve conflict files before running Claudia jobs that write to `_claudia/claudia.db` or generated dashboards.
