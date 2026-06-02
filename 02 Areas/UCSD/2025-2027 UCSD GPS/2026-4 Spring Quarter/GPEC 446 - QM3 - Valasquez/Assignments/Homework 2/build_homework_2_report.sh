#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

DRAFT_DIR="$ROOT/drafts"
mkdir -p "$DRAFT_DIR"

pandoc "$DRAFT_DIR/Homework_2_Agunias_Draft.md" \
  --standalone \
  --metadata title="Homework 2: Panel and Regression Discontinuity" \
  --css "report.css" \
  -o "$DRAFT_DIR/Homework_2_Agunias_Draft.html"

if command -v weasyprint >/dev/null 2>&1; then
  if weasyprint "$DRAFT_DIR/Homework_2_Agunias_Draft.html" "$DRAFT_DIR/Homework_2_Agunias_Draft.pdf"; then
    exit 0
  fi
fi

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [[ -x "$CHROME" ]]; then
  "$CHROME" \
    --headless \
    --disable-gpu \
    --no-sandbox \
    --no-pdf-header-footer \
    --print-to-pdf="$DRAFT_DIR/Homework_2_Agunias_Draft.pdf" \
    "file://$DRAFT_DIR/Homework_2_Agunias_Draft.html"
  exit 0
fi

echo "No working PDF renderer found. HTML was built successfully." >&2
exit 1
