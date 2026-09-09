# Manual Learning Operations

Canonical architecture: `~/SecurityResearch/00 - System/learning-architecture.md`  
Canonical registry: `~/.config/argus/learning-sources.yaml`

## Daily — bounded incremental monitoring

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_daily_incremental_learning.sh"
```

This selects only `cadence: daily` sources, runs the static/feed lane, respects source-specific refetch intervals, compiles substantial actual content, creates a digest, and checks daily root coverage. It deliberately does not run browser-DOM acquisition or traverse every source.

## Weekly — complete two-lane reconciliation

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_weekly_learning_reconciliation.sh"
```

This traverses every daily+weekly root using both static/deep-link and browser-DOM lanes, compiles/digests candidates, then writes deterministic root-coverage and source-health reports. A missing/degraded expected root causes a non-zero reconciliation exit.

## Periodic/on-demand maintenance

Read-only audit:

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_periodic_learning_maintenance.sh"
```

Targeted refresh/backfill:

```bash
ARGUS_SOURCE_FILTER='exact-registry-source-id' \
ARGUS_BACKFILL_REASON='concrete reason for refreshing this source' \
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_targeted_learning_backfill.sh"
```

The source filter and reason are mandatory. Stable foundational material is never refetched merely because a periodic audit ran.

## Registry validation and source IDs

```bash
python3 "$HOME/SecurityResearch/11 - Scripts/learning/validate_learning_registry.py" \
  --config "$HOME/.config/argus/learning-sources.yaml"
```

Source IDs, cadence, lane, role, trust, promotion policy, corroboration, refetch interval, and discovery limits are configuration-driven. `priority` is an operational hint, not a trust score.

## Low-level / smoke operations

Static dry-run without network:

```bash
ARGUS_DRY_RUN=1 ARGUS_LEARNING_CADENCE=daily ARGUS_TRACK_SEEN_STATE=0 \
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_learning_ingest.sh"
```

Single browser root, no deep links:

```bash
ARGUS_LEARNING_CADENCE=backfill \
ARGUS_SOURCE_FILTER='immunefi-research' \
ARGUS_BROWSER_MAX_SOURCES=1 \
ARGUS_BROWSER_MAX_LINKS_PER_SOURCE=0 \
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_browser_dom_ingest.sh"
```

Browser runtime setup and manual registry triage:

```bash
bash "$HOME/SecurityResearch/11 - Scripts/browser/setup_argus_browser_runtime.sh"
ARGUS_SOURCE_FILTER='immunefi-research' ARGUS_BROWSER_MAX_SOURCES=1 \
  bash "$HOME/SecurityResearch/11 - Scripts/learning/run_browser_source_triage.sh" /tmp/argus-browser-triage
```

The shared Playwright runtime uses one sandboxed context per source, routes every HTTP(S) request through the exact-IP-pinning loopback proxy, disables WebSockets/downloads/service workers, and writes bounded value-redacted evidence manifests mode `0600`. Static roots, `robots.txt`, and redirects use an HTTP(S)-only mandatory opener through the same proxy; FTP/file/data redirects are rejected, hostile `NO_PROXY=*` cannot bypass it, and persisted candidate URLs/errors are sanitized. The dedicated CDP service is pinned to `http://127.0.0.1:9219`; do not call the deprecated Selenium triage entrypoint for new work.

Manual compiler for a specific inbox:

```bash
python3 "$HOME/SecurityResearch/11 - Scripts/learning/compile_learning_inbox.py" \
  "$HOME/SecurityResearch/01 - Learning/Inbox/<run-label>"
```

Manual reconciliation:

```bash
python3 "$HOME/SecurityResearch/11 - Scripts/learning/learning_reconciliation.py" \
  --config "$HOME/.config/argus/learning-sources.yaml" \
  --run-dir "$HOME/SecurityResearch/01 - Learning/Inbox/<run-label>" \
  --cadence weekly
```

## Runtime controls

- `ARGUS_MAX_TOTAL_SECONDS`: static-lane wall-clock budget.
- `ARGUS_MAX_SOURCES_PER_GROUP`: safety cap; weekly wrapper sets this above the configured count.
- `ARGUS_MAX_DAILY_DEEP_LINK_FETCHES`: total static deep-link budget.
- `ARGUS_MAX_DEEP_LINKS_PER_SOURCE`: global cap; registry `deep_link_limit` may lower it.
- `ARGUS_MAX_APPSEC_LINK_FETCHES` / `ARGUS_MAX_APPSEC_LINK_RECORDS`: AppSec discovery bounds.
- `ARGUS_BROWSER_MAX_SOURCES`: browser-root cap; `0` means all selected roots.
- `ARGUS_BROWSER_MAX_LINKS_PER_SOURCE`: browser deep-link cap; registry limit may lower it.
- `ARGUS_TRACK_SEEN_STATE`: shared seen/refetch tracking.
- `ARGUS_SOURCE_FILTER`: exact comma-separated stable source IDs.
- `ARGUS_BACKFILL_REASON`: required reason preserved on targeted-backfill records.

## Promotion rule

The compiler accepts only `fetched_content`/`browser_fetched_content` records with `content_quality=actual_content` and sufficient content length. Indexes/listings are discovery context only. All outputs are `proposal_only` and require review, configured original-source resolution/corroboration, eval impact review, and changelog recording before mature playbook promotion.
