#!/usr/bin/env bash
set -euo pipefail

# Comprehensive weekly cadence: every daily+weekly root, static and browser-DOM lanes,
# then deterministic coverage/source-health reconciliation.
ROOT="${ARGUS_SECURITY_RESEARCH:-$HOME/SecurityResearch}"
CONFIG="${ARGUS_LEARNING_SOURCES:-$HOME/.config/argus/learning-sources.yaml}"
RUN_ID="${ARGUS_RUN_ID:-$(date +%Y%m%d-%H%M%S)}"
RUN_LABEL="${ARGUS_RUN_LABEL:-weekly-reconciliation-$RUN_ID}"
RUN_DIR="$ROOT/01 - Learning/Inbox/$RUN_LABEL"
LOG_DIR="$ROOT/12 - Logs/learning"
LOG_FILE="$LOG_DIR/weekly-reconciliation-$RUN_ID.log"
mkdir -p "$LOG_DIR"

python3 "$ROOT/11 - Scripts/learning/validate_learning_registry.py" --config "$CONFIG" | tee -a "$LOG_FILE"

echo "[$(date -Is)] comprehensive weekly learning reconciliation start" | tee -a "$LOG_FILE"
set +e
ARGUS_RUN_ID="$RUN_ID" \
ARGUS_RUN_LABEL="$RUN_LABEL" \
ARGUS_LEARNING_CADENCE=weekly \
ARGUS_INCLUDE_BACKFILL=0 \
ARGUS_MAX_TOTAL_SECONDS="${ARGUS_MAX_TOTAL_SECONDS:-1200}" \
ARGUS_MAX_SOURCES_PER_GROUP="${ARGUS_MAX_SOURCES_PER_GROUP:-999}" \
ARGUS_MAX_APPSEC_LINK_FETCHES="${ARGUS_MAX_APPSEC_LINK_FETCHES:-40}" \
ARGUS_MAX_APPSEC_LINK_RECORDS="${ARGUS_MAX_APPSEC_LINK_RECORDS:-120}" \
ARGUS_MAX_DAILY_DEEP_LINK_FETCHES="${ARGUS_MAX_DAILY_DEEP_LINK_FETCHES:-80}" \
ARGUS_MAX_DEEP_LINKS_PER_SOURCE="${ARGUS_MAX_DEEP_LINKS_PER_SOURCE:-8}" \
ARGUS_BROWSER_MAX_SOURCES="${ARGUS_BROWSER_MAX_SOURCES:-0}" \
ARGUS_BROWSER_MAX_LINKS_PER_SOURCE="${ARGUS_BROWSER_MAX_LINKS_PER_SOURCE:-8}" \
ARGUS_COMPILE_AFTER_INGEST=0 \
bash "$ROOT/11 - Scripts/learning/run_daily_learning_ingest.sh" | tee -a "$LOG_FILE"
ACQUISITION_EXIT=${PIPESTATUS[0]}
set -e

set +e
python3 "$ROOT/11 - Scripts/learning/learning_reconciliation.py" \
  --config "$CONFIG" --run-dir "$RUN_DIR" --cadence weekly | tee -a "$LOG_FILE"
RECONCILIATION_EXIT=${PIPESTATUS[0]}
set -e

FINAL_EXIT="$RECONCILIATION_EXIT"
if [[ "$ACQUISITION_EXIT" -ne 0 ]]; then
  FINAL_EXIT="$ACQUISITION_EXIT"
fi

if [[ "$FINAL_EXIT" -eq 0 ]]; then
  python3 "$ROOT/11 - Scripts/learning/compile_learning_inbox.py" "$RUN_DIR" | tee -a "$LOG_FILE"
  python3 "$ROOT/11 - Scripts/learning/create_learning_digest.py" "$RUN_DIR" | tee -a "$LOG_FILE"
else
  echo "Weekly reconciliation incomplete; compiler/review artifacts were not generated." | tee -a "$LOG_FILE" >&2
fi
python3 "$ROOT/11 - Scripts/learning/publish_learning_run.py" \
  --config "$CONFIG" --run-dir "$RUN_DIR" --cadence weekly \
  --reconciliation-exit "$FINAL_EXIT" | tee -a "$LOG_FILE"
if [[ "$FINAL_EXIT" -ne 0 ]]; then
  exit "$FINAL_EXIT"
fi
echo "[$(date -Is)] comprehensive weekly learning reconciliation complete" | tee -a "$LOG_FILE"
