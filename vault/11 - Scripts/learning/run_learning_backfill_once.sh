#!/usr/bin/env bash
set -euo pipefail

# One-time / less-frequent deep ingest for heavyweight reference sources
# such as PortSwigger, HackTricks, OWASP, Solidity docs, Trail of Bits,
# and OpenZeppelin. Keep this out of the daily cron.
#
# This is a bounded same-site crawl/scrape: each configured backfill root is
# fetched as discovery context, then same-domain topic/article/doc links are
# crawled up to ARGUS_MAX_BACKFILL_CRAWL_DEPTH and scraped when they contain
# substantial content.

export ARGUS_PRIORITY_ONLY="${ARGUS_PRIORITY_ONLY:-0}"
export ARGUS_INCLUDE_BACKFILL="${ARGUS_INCLUDE_BACKFILL:-1}"
export ARGUS_MIN_CONTENT_CHARS="${ARGUS_MIN_CONTENT_CHARS:-1200}"
export ARGUS_MAX_TOTAL_SECONDS="${ARGUS_MAX_TOTAL_SECONDS:-1800}"
export ARGUS_MAX_SOURCES_PER_GROUP="${ARGUS_MAX_SOURCES_PER_GROUP:-30}"
export ARGUS_MAX_DAILY_DEEP_LINK_FETCHES="${ARGUS_MAX_DAILY_DEEP_LINK_FETCHES:-0}"
export ARGUS_MAX_BACKFILL_DEEP_LINK_FETCHES="${ARGUS_MAX_BACKFILL_DEEP_LINK_FETCHES:-300}"
export ARGUS_MAX_BACKFILL_LINKS_PER_SOURCE="${ARGUS_MAX_BACKFILL_LINKS_PER_SOURCE:-75}"
export ARGUS_MAX_BACKFILL_CRAWL_DEPTH="${ARGUS_MAX_BACKFILL_CRAWL_DEPTH:-4}"
export ARGUS_MAX_DEEP_LINKS_PER_SOURCE="${ARGUS_MAX_DEEP_LINKS_PER_SOURCE:-12}"
export ARGUS_MAX_APPSEC_LINK_FETCHES="${ARGUS_MAX_APPSEC_LINK_FETCHES:-0}"
export ARGUS_MAX_APPSEC_LINK_RECORDS="${ARGUS_MAX_APPSEC_LINK_RECORDS:-0}"
export ARGUS_RUN_LABEL="${ARGUS_RUN_LABEL:-backfill-$(date +%Y%m%d-%H%M%S)}"

bash "${ARGUS_SECURITY_RESEARCH:-$HOME/SecurityResearch}/11 - Scripts/learning/run_learning_ingest.sh"
