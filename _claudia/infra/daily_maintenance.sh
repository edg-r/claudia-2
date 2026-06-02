#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/edgar/Documents/000 Files"
LOG_DIR="$ROOT/_claudia/infra/logs"
STAMP="$(date '+%Y-%m-%d_%H%M%S')"
LOG="$LOG_DIR/daily_maintenance_$STAMP.log"

mkdir -p "$LOG_DIR"

{
  echo "Claudia daily maintenance"
  echo "Started: $(date)"
  echo "Root: $ROOT"
  echo

  cd "$ROOT"

  echo "Git status summary:"
  git status --short || true
  echo

  echo "SQLite integrity:"
  if [[ -f "_claudia/claudia.db" ]]; then
    sqlite3 "_claudia/claudia.db" "PRAGMA integrity_check;" || true
  else
    echo "missing: _claudia/claudia.db"
  fi
  echo

  echo "Python compile checks:"
  python3 -m py_compile \
    _claudia/dashboard.py \
    _claudia/brain.py \
    _claudia/vector_dashboard_server.py \
    _claudia/gmail_dispatch_json.py || true
  echo

  echo "Disk usage:"
  df -h "$ROOT" || true
  echo

  echo "Finished: $(date)"
} >>"$LOG" 2>&1

echo "$LOG"
