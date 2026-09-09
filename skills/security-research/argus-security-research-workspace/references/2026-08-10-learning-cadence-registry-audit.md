# Argus learning cadence and source-registry audit — 2026-08-10

Use this reference when auditing or changing Argus learning ingestion, registry policy, cron cadence, seen-state behavior, compilation, or promotion.

## Audit method that exposed the important gaps

Do not audit the registry or scheduler in isolation. Trace one source through all layers:

1. Registry declaration and group defaults.
2. Effective source selection for each cadence and acquisition lane.
3. Shell-wrapper environment propagation.
4. OS/Hermes scheduler timing and overlap.
5. Static/browser fetch and discovered-record provenance.
6. Seen-state canonicalization, freshness, hashes, and writes.
7. Combined run manifest and reconciliation.
8. Compiler policy gates and promotion workflow.
9. Cleanup, rejection, and historical logs.

For each declared policy field, search for the runtime consumer. A field that is validated and copied into records but never used to select, fetch, reconcile, compile, or gate promotion is informational rather than operational.

## Snapshot findings

The schema-v2 registry validated with 53 unique sources:

- 8 daily
- 19 weekly
- 3 periodic
- 23 on-demand
- 10 browser-DOM sources

The intended executor selections were:

- daily: 8 sources, no browser lane
- weekly: 27 sources (daily + weekly), 17 static and 10 browser
- backfill eligibility: 26 periodic/on-demand sources

During the audit, registry and ingestion modules were being edited concurrently. Re-stat and re-read active files before finalizing an audit; do not assume an earlier read is still current. Distinguish historical production logs from newly written, not-yet-scheduled code.

Key integration gaps observed at the cutoff:

- Static and browser ingestors understood schema v2, but production wrappers still defaulted to `legacy` because they did not propagate an explicit cadence.
- The Hermes weekly job reviewed existing material but did not itself run weekly acquisition or reconciliation.
- Reconciliation existed as a module but was not invoked by production wrappers.
- Compiler promotion metadata had been added, but scheduling and promotion still lacked a shared run manifest/dependency gate.
- AppSec-derived records could lose parent source ID and categorical original-source policy.
- Static and browser seen-state behavior differed, shared the same unlocked state file, and used different canonicalization/change-detection semantics.
- Repository, transcript, and feed acquisitions were declared categorically but did not all have source-native runtime adapters.

These are point-in-time observations, not permanent negative claims. Re-verify each before remediation.

## Durable invariants

### Cadence

Use three executor cadences:

- **daily incremental**: bounded changed/new content from daily sources
- **weekly reconciliation**: daily + weekly roots, including browser acquisition
- **targeted backfill**: explicit source-ID allowlist only

Treat `periodic` and `on_demand` as trigger/eligibility modes under targeted backfill rather than independent broad jobs.

Every production invocation must set cadence explicitly. Avoid a permissive implicit `legacy` default after migration.

### Scheduling

A weekly run should replace that day's daily run or consume/reconcile its manifest; it should not independently refetch the same sources while a daily promotion job edits the same artifacts. Tie promotion to an exact completed run ID.

### Registry and provenance

Every root and discovered record should carry:

- source ID and parent source ID
- record kind
- source role/trust/promotion policy
- acquisition method and run cadence
- registry schema version and digest
- discovery chain

Discovery indexes such as AppSec.fyi must not become authority. Their children must retain `original_source_required` semantics.

### State

Use one canonicalization function and one transactional state writer. State should be keyed by source ID plus canonical URL and retain first seen, last checked, last changed, last success, hash/validators, next due time, failure/backoff, and run ID. Lock the state for the full orchestrated run. Corrupt state must be quarantined/reported rather than silently treated as empty.

### Reconciliation and promotion

A run may make partial progress, but compilation/promotion should require a reconciliation artifact covering expected roots and lane completion. Promoters consume an explicit manifest, never a lexically inferred “latest” directory.

Keep all compiler output proposal-only. Authority changes review requirements; it never enables automatic mature-playbook promotion. Discovery-only material requires original-source resolution and applicable corroboration.

### Backfill

Require explicit source IDs unless an operator deliberately supplies an `--all`-style override. Dispatch by acquisition method: static HTTP/deep-link, browser DOM, repository, feed, and transcript are distinct lanes. A generic HTML fetch that returns `source_native_required` is a degraded acquisition, not successful coverage.

## Verification checklist

- Validate the live registry and count each cadence/lane.
- Confirm wrappers pass explicit cadence and source filters.
- Confirm daily selects only daily sources; weekly selects daily + weekly; backfill is exact.
- Confirm browser sources are absent from daily if policy says weekly.
- Confirm all derived records have source and parent provenance.
- Confirm AppSec children retain original-source resolution policy.
- Confirm seen-state freshness and unchanged-hash behavior match across lanes.
- Confirm a run-level lock prevents overlapping state/artifact writes.
- Confirm reconciliation is invoked before compile/promotion.
- Confirm compiler/promotion consume an explicit run directory/manifest.
- Check Tuesday/Sunday scheduling for daily/weekly overlap.
- Inspect recent logs for start-without-complete runs and stale artifact consumption.
- Run syntax checks and architecture tests without launching live network ingestion during a review-only audit.

## Historical efficiency signal

A pre-migration daily run on 2026-08-10 produced 213 records but only 26 actual-content records; 145 were not fetched. The browser lane produced 60 records with one actual-content item and 43 seen skips. This demonstrated why cadence correction and manifest-level skip counters matter. Re-measure after explicit cadence wiring rather than treating these numbers as permanent.