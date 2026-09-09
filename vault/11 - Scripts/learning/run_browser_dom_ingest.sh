#!/usr/bin/env bash
set -euo pipefail

ROOT="${ARGUS_SECURITY_RESEARCH:-$HOME/SecurityResearch}"
CONFIG="${ARGUS_LEARNING_SOURCES:-$HOME/.config/argus/learning-sources.yaml}"
SCRIPT="$ROOT/11 - Scripts/learning/browser_dom_ingest.py"
BROWSER_PYTHON="${ARGUS_BROWSER_PYTHON:-$HOME/.local/share/argus-browser/venv/bin/python}"
RUN_LABEL="${ARGUS_RUN_LABEL:-browser-dom-$(date +%Y%m%d-%H%M%S)}"
RUN_DIR="$ROOT/01 - Learning/Inbox/$RUN_LABEL"
LOG_DIR="$ROOT/12 - Logs/learning"
mkdir -p "$RUN_DIR" "$LOG_DIR"
LOG_FILE="$LOG_DIR/browser-dom-ingest-$(date +%Y%m%d-%H%M%S).log"

echo "[$(date -Is)] Argus browser DOM learning ingest start" | tee -a "$LOG_FILE"
echo "Config: $CONFIG" | tee -a "$LOG_FILE"
echo "Run dir: $RUN_DIR" | tee -a "$LOG_FILE"
if [[ ! -x "$BROWSER_PYTHON" ]]; then
  echo "Argus browser Python is missing: $BROWSER_PYTHON" | tee -a "$LOG_FILE" >&2
  echo "Create it with: bash '$ROOT/11 - Scripts/browser/setup_argus_browser_runtime.sh'" | tee -a "$LOG_FILE" >&2
  exit 1
fi
TOTAL_SECONDS="${ARGUS_BROWSER_MAX_TOTAL_SECONDS:-1800}"
[[ "$TOTAL_SECONDS" =~ ^[1-9][0-9]*$ ]] || { echo "Invalid ARGUS_BROWSER_MAX_TOTAL_SECONDS: $TOTAL_SECONDS" >&2; exit 2; }
PROCESS_SECONDS=$((TOTAL_SECONDS + 60))
export ARGUS_CHROME_BINARY="${ARGUS_CHROME_BINARY:-/usr/bin/google-chrome}"
export ARGUS_BROWSER_EGRESS_PROXY="${ARGUS_BROWSER_EGRESS_PROXY:-http://127.0.0.1:9219}"
MEMORY_MAX="${ARGUS_BROWSER_MEMORY_MAX:-2G}"
TASKS_MAX="${ARGUS_BROWSER_TASKS_MAX:-160}"
if [[ -z "${XDG_RUNTIME_DIR:-}" ]]; then
  RUNTIME_CANDIDATE="/run/user/$(id -u)"
  if [[ -d "$RUNTIME_CANDIDATE" && -O "$RUNTIME_CANDIDATE" ]]; then
    export XDG_RUNTIME_DIR="$RUNTIME_CANDIDATE"
  fi
fi
if [[ -z "${DBUS_SESSION_BUS_ADDRESS:-}" && -n "${XDG_RUNTIME_DIR:-}" && -S "$XDG_RUNTIME_DIR/bus" && -O "$XDG_RUNTIME_DIR/bus" ]]; then
  export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"
fi
BOUNDED_RUN=(systemd-run --user --scope --quiet --collect -p "MemoryMax=$MEMORY_MAX" -p "TasksMax=$TASKS_MAX")
if ! systemctl --user show-environment >/dev/null 2>&1; then
  if [[ "${ARGUS_BROWSER_ALLOW_NO_CGROUP:-0}" != "1" ]]; then
    echo "Argus browser requires a working user systemd manager for cgroup bounds" | tee -a "$LOG_FILE" >&2
    exit 2
  fi
  BOUNDED_RUN=()
fi
"${BOUNDED_RUN[@]}" timeout --signal=TERM --kill-after=15s "${PROCESS_SECONDS}s" \
  "$BROWSER_PYTHON" "$SCRIPT" "$CONFIG" "$RUN_DIR" | tee -a "$LOG_FILE"
echo "[$(date -Is)] Argus browser DOM learning ingest complete" | tee -a "$LOG_FILE"
