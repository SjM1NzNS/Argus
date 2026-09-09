#!/usr/bin/env bash
set -euo pipefail

# Explicit targeted backfill. No source is fetched unless its stable registry ID and
# a concrete reason are supplied by the operator.
ROOT="${ARGUS_SECURITY_RESEARCH:-$HOME/SecurityResearch}"
CONFIG="${ARGUS_LEARNING_SOURCES:-$HOME/.config/argus/learning-sources.yaml}"
: "${ARGUS_SOURCE_FILTER:?Set ARGUS_SOURCE_FILTER to one or more comma-separated registry source IDs}"
: "${ARGUS_BACKFILL_REASON:?Set ARGUS_BACKFILL_REASON to the concrete refresh/backfill reason}"
RUN_ID="${ARGUS_RUN_ID:-$(date +%Y%m%d-%H%M%S)}"
RUN_LABEL="${ARGUS_RUN_LABEL:-targeted-backfill-$RUN_ID}"
LOG_DIR="$ROOT/12 - Logs/learning"
LOG_FILE="$LOG_DIR/targeted-backfill-$RUN_ID.log"
mkdir -p "$LOG_DIR"

python3 "$ROOT/11 - Scripts/learning/validate_learning_registry.py" --config "$CONFIG" | tee -a "$LOG_FILE"
echo "[$(date -Is)] targeted backfill start; sources=$ARGUS_SOURCE_FILTER reason=$ARGUS_BACKFILL_REASON" | tee -a "$LOG_FILE"
ARGUS_RUN_ID="$RUN_ID" \
ARGUS_RUN_LABEL="$RUN_LABEL" \
ARGUS_LEARNING_CADENCE=backfill \
ARGUS_INCLUDE_BACKFILL=1 \
ARGUS_MAX_TOTAL_SECONDS="${ARGUS_MAX_TOTAL_SECONDS:-1800}" \
ARGUS_MAX_SOURCES_PER_GROUP="${ARGUS_MAX_SOURCES_PER_GROUP:-999}" \
ARGUS_BROWSER_MAX_SOURCES="${ARGUS_BROWSER_MAX_SOURCES:-0}" \
ARGUS_COMPILE_AFTER_INGEST=0 \
bash "$ROOT/11 - Scripts/learning/run_daily_learning_ingest.sh" | tee -a "$LOG_FILE"
RUN_DIR="$ROOT/01 - Learning/Inbox/$RUN_LABEL"
set +e
python3 "$ROOT/11 - Scripts/learning/learning_reconciliation.py" \
  --config "$CONFIG" --run-dir "$RUN_DIR" --cadence backfill \
  --source-ids "$ARGUS_SOURCE_FILTER" | tee -a "$LOG_FILE"
RECONCILIATION_EXIT=${PIPESTATUS[0]}
set -e
if [[ "$RECONCILIATION_EXIT" -eq 0 ]]; then
  python3 "$ROOT/11 - Scripts/learning/compile_learning_inbox.py" "$RUN_DIR" | tee -a "$LOG_FILE"
  python3 "$ROOT/11 - Scripts/learning/create_learning_digest.py" "$RUN_DIR" | tee -a "$LOG_FILE"
else
  echo "Targeted backfill reconciliation incomplete; compiler/review artifacts were not generated." | tee -a "$LOG_FILE" >&2
fi
python3 "$ROOT/11 - Scripts/learning/publish_learning_run.py" \
  --config "$CONFIG" --run-dir "$RUN_DIR" --cadence backfill \
  --source-ids "$ARGUS_SOURCE_FILTER" --reconciliation-exit "$RECONCILIATION_EXIT" | tee -a "$LOG_FILE"
if [[ "$RECONCILIATION_EXIT" -ne 0 ]]; then
  exit "$RECONCILIATION_EXIT"
fi
echo "[$(date -Is)] targeted backfill complete" | tee -a "$LOG_FILE"
