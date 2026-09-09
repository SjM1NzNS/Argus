#!/usr/bin/env bash
set -euo pipefail
ROOT="${ARGUS_SECURITY_RESEARCH:-$HOME/SecurityResearch}"
CONFIG="${ARGUS_LEARNING_SOURCES:-$HOME/.config/argus/learning-sources.yaml}"
BROWSER_PYTHON="${ARGUS_BROWSER_PYTHON:-$HOME/.local/share/argus-browser/venv/bin/python}"
OUT_DIR="${1:-$ROOT/01 - Learning/Source Triage/browser-all-sources-$(date +%Y%m%d-%H%M%S)}"
if [[ ! -x "$BROWSER_PYTHON" ]]; then
  printf 'Argus browser Python is missing: %s\n' "$BROWSER_PYTHON" >&2
  exit 1
fi
TOTAL_SECONDS="${ARGUS_BROWSER_MAX_TOTAL_SECONDS:-1800}"
[[ "$TOTAL_SECONDS" =~ ^[1-9][0-9]*$ ]] || { printf 'Invalid ARGUS_BROWSER_MAX_TOTAL_SECONDS: %s\n' "$TOTAL_SECONDS" >&2; exit 2; }
PROCESS_SECONDS=$((TOTAL_SECONDS + 60))
export ARGUS_CHROME_BINARY="${ARGUS_CHROME_BINARY:-/usr/bin/google-chrome}"
export ARGUS_BROWSER_EGRESS_PROXY="${ARGUS_BROWSER_EGRESS_PROXY:-http://127.0.0.1:9219}"
MEMORY_MAX="${ARGUS_BROWSER_MEMORY_MAX:-2G}"
TASKS_MAX="${ARGUS_BROWSER_TASKS_MAX:-160}"
BOUNDED_RUN=(systemd-run --user --scope --quiet --collect -p "MemoryMax=$MEMORY_MAX" -p "TasksMax=$TASKS_MAX")
if ! systemctl --user show-environment >/dev/null 2>&1; then
  if [[ "${ARGUS_BROWSER_ALLOW_NO_CGROUP:-0}" != "1" ]]; then
    printf 'Argus browser requires a working user systemd manager for cgroup bounds\n' >&2
    exit 2
  fi
  BOUNDED_RUN=()
fi
exec "${BOUNDED_RUN[@]}" timeout --signal=TERM --kill-after=15s "${PROCESS_SECONDS}s" \
  "$BROWSER_PYTHON" "$ROOT/11 - Scripts/learning/browser_source_triage.py" "$CONFIG" "$OUT_DIR"
