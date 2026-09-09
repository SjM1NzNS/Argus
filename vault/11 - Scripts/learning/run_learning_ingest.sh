#!/usr/bin/env bash
set -euo pipefail

ROOT="${ARGUS_SECURITY_RESEARCH:-$HOME/SecurityResearch}"
CONFIG="${ARGUS_LEARNING_SOURCES:-$HOME/.config/argus/learning-sources.yaml}"
SCRIPT_DIR="$ROOT/11 - Scripts/learning"
LOG_DIR="$ROOT/12 - Logs/learning"
INBOX_ROOT="$ROOT/01 - Learning/Inbox"
mkdir -p "$LOG_DIR" "$INBOX_ROOT"

RUN_DATE="$(date +%F)"
RUN_ID="$(date +%Y%m%d-%H%M%S)"
RUN_LABEL="${ARGUS_RUN_LABEL:-$RUN_DATE}"
RUN_DIR="$INBOX_ROOT/$RUN_LABEL"
mkdir -p "$RUN_DIR"
LOG_FILE="$LOG_DIR/learning-ingest-$RUN_ID.log"

exec > >(tee -a "$LOG_FILE") 2>&1

echo "[$(date -Is)] Argus learning ingest start"
echo "Config: $CONFIG"
echo "Run dir: $RUN_DIR"

python3 "$SCRIPT_DIR/learning_ingest.py" "$CONFIG" "$RUN_DIR"

echo "[$(date -Is)] Argus learning ingest complete"
