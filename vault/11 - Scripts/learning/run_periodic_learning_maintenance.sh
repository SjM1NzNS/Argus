#!/usr/bin/env bash
set -euo pipefail

# Read-only periodic/on-demand maintenance audit. It never refetches foundational
# material or edits playbooks; targeted refreshes use run_targeted_learning_backfill.sh.
ROOT="${ARGUS_SECURITY_RESEARCH:-$HOME/SecurityResearch}"
CONFIG="${ARGUS_LEARNING_SOURCES:-$HOME/.config/argus/learning-sources.yaml}"
python3 "$ROOT/11 - Scripts/learning/validate_learning_registry.py" --config "$CONFIG"
python3 "$ROOT/11 - Scripts/learning/audit_learning_maintenance.py" \
  --config "$CONFIG" --root "$ROOT" "$@"
