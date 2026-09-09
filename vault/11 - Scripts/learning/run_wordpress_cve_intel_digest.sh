#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
: "${ARGUS_WP_CVE_MAX:=10}"
: "${ARGUS_WP_CVE_ENRICH:=5}"

exec python3 "$SCRIPT_DIR/wordpress_cve_intel_digest.py" \
  --max-candidates "$ARGUS_WP_CVE_MAX" \
  --enrich "$ARGUS_WP_CVE_ENRICH" \
  "$@"
