#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/edgar/Documents/000 Files"
LOG_DIR="$ROOT/_claudia/infra/logs"

echo "Claudia Mac mini bootstrap check"
echo "Root: $ROOT"

if [[ ! -d "$ROOT/_claudia" ]]; then
  echo "Missing Claudia folder at $ROOT/_claudia"
  exit 1
fi

mkdir -p "$LOG_DIR"

echo
echo "Tool checks:"
for tool in git python3 sqlite3 bash; do
  if command -v "$tool" >/dev/null 2>&1; then
    echo "ok: $tool ($(command -v "$tool"))"
  else
    echo "missing: $tool"
  fi
done

echo
echo "Workspace checks:"
for path in "_claudia/claudia.db" "_claudia/dashboard.py" "_claudia/agents/hephaestus" "_claudia/system/manifest.json"; do
  if [[ -e "$ROOT/$path" ]]; then
    echo "ok: $path"
  else
    echo "missing: $path"
  fi
done

echo
echo "Manual next steps:"
echo "1. Review _claudia/infra/macos_native_setup_checklist.md."
echo "2. Enable File Sharing / SMB for LAN access to the canonical workspace."
echo "3. Enable Remote Login / SSH and Screen Sharing if Edgar wants remote maintenance."
echo "4. Confirm Time Machine is backing up the Mac mini."
echo "5. Review _claudia/infra/launchd/com.claudia.daily-maintenance.plist.example before installing it."
echo "6. Run: bash _claudia/infra/daily_maintenance.sh"
echo "7. Keep Syncthing as an optional later mirror path, not the default."
