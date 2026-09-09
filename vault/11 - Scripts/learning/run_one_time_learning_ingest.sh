#!/usr/bin/env bash
set -euo pipefail

# One-time Argus learning ingestion orchestrator.
#
# Purpose:
#   Run heavyweight reference corpora / standards / taxonomies through the
#   one-time/backfill lane only. This is intentionally separate from daily
#   ingestion and should be launched deliberately, not by daily cron.
#
# Includes sources with cadence=one_time_full and core-theory groups:
#   - HackTricks / PortSwigger Academy / OWASP / Arcanum taxonomy
#   - Solidity / SCSVS / Immunefi Learn / Trail of Bits / OpenZeppelin / DVDeFi
#
# This script does not compile/promote automatically.

ROOT="${ARGUS_SECURITY_RESEARCH:-$HOME/SecurityResearch}"
RUN_ID="${ARGUS_RUN_ID:-$(date +%Y%m%d-%H%M%S)}"
RUN_LABEL="${ARGUS_RUN_LABEL:-one-time-$RUN_ID}"
INBOX_ROOT="$ROOT/01 - Learning/Inbox"
RUN_DIR="$INBOX_ROOT/$RUN_LABEL"
LOG_DIR="$ROOT/12 - Logs/learning"
LOG_FILE="$LOG_DIR/one-time-learning-ingest-$RUN_ID.log"
mkdir -p "$RUN_DIR" "$LOG_DIR"

echo "[$(date -Is)] Argus one-time learning ingest start" | tee -a "$LOG_FILE"
echo "Run dir: $RUN_DIR" | tee -a "$LOG_FILE"

# Underlying backfill runner handles unique labels, depth, and one-time source inclusion.
ARGUS_RUN_LABEL="$RUN_LABEL" \
ARGUS_INCLUDE_BACKFILL=1 \
ARGUS_PRIORITY_ONLY="${ARGUS_PRIORITY_ONLY:-0}" \
ARGUS_MIN_CONTENT_CHARS="${ARGUS_MIN_CONTENT_CHARS:-1200}" \
ARGUS_MAX_TOTAL_SECONDS="${ARGUS_MAX_TOTAL_SECONDS:-1800}" \
ARGUS_MAX_SOURCES_PER_GROUP="${ARGUS_MAX_SOURCES_PER_GROUP:-20}" \
ARGUS_MAX_BACKFILL_DEEP_LINK_FETCHES="${ARGUS_MAX_BACKFILL_DEEP_LINK_FETCHES:-300}" \
ARGUS_MAX_BACKFILL_LINKS_PER_SOURCE="${ARGUS_MAX_BACKFILL_LINKS_PER_SOURCE:-75}" \
ARGUS_MAX_BACKFILL_CRAWL_DEPTH="${ARGUS_MAX_BACKFILL_CRAWL_DEPTH:-4}" \
ARGUS_MAX_APPSEC_LINK_FETCHES="${ARGUS_MAX_APPSEC_LINK_FETCHES:-0}" \
ARGUS_MAX_APPSEC_LINK_RECORDS="${ARGUS_MAX_APPSEC_LINK_RECORDS:-0}" \
bash "$ROOT/11 - Scripts/learning/run_learning_backfill_once.sh" | tee -a "$LOG_FILE"

cat > "$RUN_DIR/one-time-ingest-manifest.md" <<EOF
# Argus One-Time Learning Ingest Manifest

- Run label: \`$RUN_LABEL\`
- Run dir: \`$RUN_DIR\`
- Log: \`$LOG_FILE\`
- Mode: one-time/backfill only
- Crawl depth: \`${ARGUS_MAX_BACKFILL_CRAWL_DEPTH:-4}\`
- Max backfill links per source: \`${ARGUS_MAX_BACKFILL_LINKS_PER_SOURCE:-75}\`
- Max backfill deep-link fetches: \`${ARGUS_MAX_BACKFILL_DEEP_LINK_FETCHES:-300}\`

Compile manually after review:

\`\`\`bash
python3 "$ROOT/11 - Scripts/learning/compile_learning_inbox.py" "$RUN_DIR"
\`\`\`
EOF

if [[ "${ARGUS_COMPILE_AFTER_INGEST:-1}" == "1" ]]; then
  echo "[$(date -Is)] Compiling one-time learning inbox into vault notes/proposals" | tee -a "$LOG_FILE"
  ARGUS_COMPILER_MAX_RECORDS="${ARGUS_COMPILER_MAX_RECORDS:-200}" \
    python3 "$ROOT/11 - Scripts/learning/compile_learning_inbox.py" "$RUN_DIR" | tee -a "$LOG_FILE"
fi

echo "[$(date -Is)] Argus one-time learning ingest complete" | tee -a "$LOG_FILE"
