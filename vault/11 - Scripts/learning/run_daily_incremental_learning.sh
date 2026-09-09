#!/usr/bin/env bash
set -euo pipefail

# Bounded daily cadence: explicit daily roots, static/feed lane only, seen-state aware.
ROOT="${ARGUS_SECURITY_RESEARCH:-$HOME/SecurityResearch}"
CONFIG="${ARGUS_LEARNING_SOURCES:-$HOME/.config/argus/learning-sources.yaml}"
RUN_ID="${ARGUS_RUN_ID:-$(date +%Y%m%d-%H%M%S)}"
RUN_LABEL="${ARGUS_RUN_LABEL:-daily-incremental-$RUN_ID}"
RUN_DIR="$ROOT/01 - Learning/Inbox/$RUN_LABEL"
LOG_DIR="$ROOT/12 - Logs/learning"
LOG_FILE="$LOG_DIR/daily-incremental-$RUN_ID.log"
mkdir -p "$LOG_DIR"

python3 "$ROOT/11 - Scripts/learning/validate_learning_registry.py" --config "$CONFIG" | tee -a "$LOG_FILE"

echo "[$(date -Is)] bounded daily incremental learning start" | tee -a "$LOG_FILE"
ARGUS_RUN_LABEL="$RUN_LABEL" \
ARGUS_LEARNING_CADENCE=daily \
ARGUS_INCLUDE_BACKFILL=0 \
ARGUS_MAX_TOTAL_SECONDS="${ARGUS_MAX_TOTAL_SECONDS:-240}" \
ARGUS_MAX_SOURCES_PER_GROUP="${ARGUS_MAX_SOURCES_PER_GROUP:-20}" \
ARGUS_MAX_APPSEC_LINK_FETCHES="${ARGUS_MAX_APPSEC_LINK_FETCHES:-0}" \
ARGUS_MAX_APPSEC_LINK_RECORDS="${ARGUS_MAX_APPSEC_LINK_RECORDS:-0}" \
ARGUS_MAX_DAILY_DEEP_LINK_FETCHES="${ARGUS_MAX_DAILY_DEEP_LINK_FETCHES:-12}" \
ARGUS_MAX_DEEP_LINKS_PER_SOURCE="${ARGUS_MAX_DEEP_LINKS_PER_SOURCE:-3}" \
ARGUS_TRACK_SEEN_STATE=1 \
bash "$ROOT/11 - Scripts/learning/run_learning_ingest.sh" | tee -a "$LOG_FILE"

set +e
python3 "$ROOT/11 - Scripts/learning/learning_reconciliation.py" \
  --config "$CONFIG" --run-dir "$RUN_DIR" --cadence daily | tee -a "$LOG_FILE"
RECONCILIATION_EXIT=${PIPESTATUS[0]}
set -e

if [[ "$RECONCILIATION_EXIT" -eq 0 ]]; then
  python3 "$ROOT/11 - Scripts/learning/compile_learning_inbox.py" "$RUN_DIR" | tee -a "$LOG_FILE"
  python3 "$ROOT/11 - Scripts/learning/create_learning_digest.py" "$RUN_DIR" | tee -a "$LOG_FILE"
else
  echo "Daily reconciliation incomplete; compiler/review artifacts were not generated." | tee -a "$LOG_FILE" >&2
fi
python3 "$ROOT/11 - Scripts/learning/publish_learning_run.py" \
  --config "$CONFIG" --run-dir "$RUN_DIR" --cadence daily \
  --reconciliation-exit "$RECONCILIATION_EXIT" | tee -a "$LOG_FILE"
if [[ "$RECONCILIATION_EXIT" -ne 0 ]]; then
  exit "$RECONCILIATION_EXIT"
fi
echo "[$(date -Is)] bounded daily incremental learning complete" | tee -a "$LOG_FILE"
