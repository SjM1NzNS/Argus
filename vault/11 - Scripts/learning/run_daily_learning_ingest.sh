#!/usr/bin/env bash
set -euo pipefail

# Reusable Argus two-lane learning ingestion orchestrator.
#
# Purpose:
#   Run sources selected by ARGUS_LEARNING_CADENCE through the existing lanes:
#   1. static/feed/deep-link acquisition
#   2. browser DOM acquisition for configured dynamic roots
#
# Scheduled daily work uses run_daily_incremental_learning.sh (static only).
# Scheduled weekly work calls this compatibility orchestrator with cadence=weekly.

ROOT="${ARGUS_SECURITY_RESEARCH:-$HOME/SecurityResearch}"
CONFIG="${ARGUS_LEARNING_SOURCES:-$HOME/.config/argus/learning-sources.yaml}"
RUN_ID="${ARGUS_RUN_ID:-$(date +%Y%m%d-%H%M%S)}"
CADENCE="${ARGUS_LEARNING_CADENCE:-legacy}"
RUN_LABEL="${ARGUS_RUN_LABEL:-${CADENCE}-$RUN_ID}"
INBOX_ROOT="$ROOT/01 - Learning/Inbox"
RUN_DIR="$INBOX_ROOT/$RUN_LABEL"
LOG_DIR="$ROOT/12 - Logs/learning"
LOG_FILE="$LOG_DIR/daily-learning-ingest-$RUN_ID.log"
mkdir -p "$RUN_DIR" "$LOG_DIR"

STATIC_LABEL="$RUN_LABEL-static"
BROWSER_LABEL="$RUN_LABEL-browser-dom"
STATIC_DIR="$INBOX_ROOT/$STATIC_LABEL"
BROWSER_DIR="$INBOX_ROOT/$BROWSER_LABEL"

echo "[$(date -Is)] Argus learning ingest start (cadence=$CADENCE)" | tee -a "$LOG_FILE"
echo "Config: $CONFIG" | tee -a "$LOG_FILE"
echo "Cadence: $CADENCE" | tee -a "$LOG_FILE"
echo "Combined run dir: $RUN_DIR" | tee -a "$LOG_FILE"
echo "Static component: $STATIC_DIR" | tee -a "$LOG_FILE"
echo "Browser component: $BROWSER_DIR" | tee -a "$LOG_FILE"

# Static lane. Cadence/schema selection excludes roots outside the requested mode.
ARGUS_RUN_LABEL="$STATIC_LABEL" \
ARGUS_PROVENANCE_RUN_ID="$RUN_LABEL" \
ARGUS_LEARNING_CADENCE="$CADENCE" \
ARGUS_INCLUDE_BACKFILL="${ARGUS_INCLUDE_BACKFILL:-0}" \
ARGUS_PRIORITY_ONLY="${ARGUS_PRIORITY_ONLY:-0}" \
ARGUS_MIN_CONTENT_CHARS="${ARGUS_MIN_CONTENT_CHARS:-1200}" \
ARGUS_MAX_TOTAL_SECONDS="${ARGUS_MAX_TOTAL_SECONDS:-420}" \
ARGUS_MAX_SOURCES_PER_GROUP="${ARGUS_MAX_SOURCES_PER_GROUP:-20}" \
ARGUS_MAX_APPSEC_LINK_FETCHES="${ARGUS_MAX_APPSEC_LINK_FETCHES:-25}" \
ARGUS_MAX_APPSEC_LINK_RECORDS="${ARGUS_MAX_APPSEC_LINK_RECORDS:-80}" \
ARGUS_MAX_DAILY_DEEP_LINK_FETCHES="${ARGUS_MAX_DAILY_DEEP_LINK_FETCHES:-35}" \
ARGUS_MAX_DEEP_LINKS_PER_SOURCE="${ARGUS_MAX_DEEP_LINKS_PER_SOURCE:-5}" \
ARGUS_REFETCH_SEEN_AFTER_DAYS="${ARGUS_REFETCH_SEEN_AFTER_DAYS:-30}" \
bash "$ROOT/11 - Scripts/learning/run_learning_ingest.sh" | tee -a "$LOG_FILE"

# Browser DOM lane. Handles selected config entries with acquisition=browser_dom.
set +e
ARGUS_RUN_LABEL="$BROWSER_LABEL" \
ARGUS_PROVENANCE_RUN_ID="$RUN_LABEL" \
ARGUS_LEARNING_CADENCE="$CADENCE" \
ARGUS_BROWSER_MAX_SOURCES="${ARGUS_BROWSER_MAX_SOURCES:-20}" \
ARGUS_BROWSER_MAX_LINKS_PER_SOURCE="${ARGUS_BROWSER_MAX_LINKS_PER_SOURCE:-5}" \
ARGUS_REFETCH_SEEN_AFTER_DAYS="${ARGUS_REFETCH_SEEN_AFTER_DAYS:-30}" \
bash "$ROOT/11 - Scripts/learning/run_browser_dom_ingest.sh" | tee -a "$LOG_FILE"
BROWSER_EXIT=${PIPESTATUS[0]}
set -e

# Combined daily inbox. Keep component folders for forensics, but provide a single
# learning-candidates.jsonl for compiler/review if the user wants a unified daily pass.
: > "$RUN_DIR/learning-candidates.jsonl"
for component in "$STATIC_DIR" "$BROWSER_DIR"; do
  if [[ -s "$component/learning-candidates.jsonl" ]]; then
    cat "$component/learning-candidates.jsonl" >> "$RUN_DIR/learning-candidates.jsonl"
  fi
done
if [[ -d "$BROWSER_DIR/browser-evidence" ]]; then
  mkdir -p "$RUN_DIR/browser-evidence"
  chmod 700 "$RUN_DIR/browser-evidence"
  cp -a "$BROWSER_DIR/browser-evidence/." "$RUN_DIR/browser-evidence/"
fi

python3 - "$RUN_DIR" "$STATIC_DIR" "$BROWSER_DIR" "$CADENCE" <<'PY'
from pathlib import Path
import json, sys, collections, datetime
run=Path(sys.argv[1]); static=Path(sys.argv[2]); browser=Path(sys.argv[3]); cadence=sys.argv[4]
records=[]
jsonl=run/'learning-candidates.jsonl'
if jsonl.exists():
    records=[json.loads(l) for l in jsonl.read_text(encoding='utf-8').splitlines() if l.strip()]
statuses=collections.Counter(r.get('local_processing_status','unknown') for r in records)
qualities=collections.Counter(r.get('content_quality') or 'not_fetched' for r in records)
groups=collections.Counter(r.get('source_group','unknown') for r in records)
summary=run/'learning-run-summary.md'
summary.write_text(
    f'# Argus {cadence.title()} Learning Ingest Summary\n\n'
    f'- Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n'
    f'- Cadence: {cadence}\n'
    f'- Combined records: {len(records)}\n'
    f'- Static component: `{static}`\n'
    f'- Browser DOM component: `{browser}`\n'
    f'- Candidate file: `{jsonl}`\n\n'
    '## Statuses\n' + ''.join(f'- {k}: {v}\n' for k,v in sorted(statuses.items())) + '\n'
    '## Content quality\n' + ''.join(f'- {k}: {v}\n' for k,v in sorted(qualities.items())) + '\n'
    '## Source groups\n' + ''.join(f'- {k}: {v}\n' for k,v in sorted(groups.items())) + '\n',
    encoding='utf-8')
print(json.dumps({'run_dir':str(run),'records':len(records),'summary':str(summary),'static_component':str(static),'browser_component':str(browser)}, indent=2, sort_keys=True))
PY

if [[ "${ARGUS_COMPILE_AFTER_INGEST:-1}" == "1" && "$BROWSER_EXIT" -eq 0 ]]; then
  echo "[$(date -Is)] Compiling $CADENCE learning inbox into vault notes/proposals" | tee -a "$LOG_FILE"
  ARGUS_COMPILER_MAX_RECORDS="${ARGUS_COMPILER_MAX_RECORDS:-60}" \
    python3 "$ROOT/11 - Scripts/learning/compile_learning_inbox.py" "$RUN_DIR" | tee -a "$LOG_FILE"
  echo "[$(date -Is)] Creating daily learning digest" | tee -a "$LOG_FILE"
  python3 "$ROOT/11 - Scripts/learning/create_learning_digest.py" "$RUN_DIR" | tee -a "$LOG_FILE"
fi

if [[ "$BROWSER_EXIT" -ne 0 ]]; then
  echo "Browser DOM component failed with exit $BROWSER_EXIT; combined diagnostics were preserved and compilation was suppressed." | tee -a "$LOG_FILE" >&2
  exit "$BROWSER_EXIT"
fi
echo "[$(date -Is)] Argus $CADENCE learning ingest complete" | tee -a "$LOG_FILE"
