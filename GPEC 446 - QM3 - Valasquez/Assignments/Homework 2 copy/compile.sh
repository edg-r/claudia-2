#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "=== STEP 1: Running R analysis and generating figures and tables ==="
Rscript --vanilla Homework_2.R

echo "=== STEP 2: Compiling report to HTML and PDF ==="
./build_report.sh

echo "=== Compilation completed successfully! ==="
