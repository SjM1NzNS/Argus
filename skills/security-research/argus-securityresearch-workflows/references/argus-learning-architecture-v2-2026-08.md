# Argus Learning Architecture v2 (2026-08)

Use this reference when operating, reviewing, repairing, or extending the Argus learning pipeline. The vault architecture document remains authoritative for deployed behavior:

- Architecture: `$HOME/SecurityResearch/00 - System/learning-architecture.md`
- Registry: `$HOME/.config/argus/learning-sources.yaml`
- Validator: `$HOME/SecurityResearch/11 - Scripts/learning/validate_learning_registry.py`
- Seen state: `$HOME/.config/argus/learning-seen-urls.json`
- Source health: `$HOME/.config/argus/learning-source-health.json`

## Class-level operating model

The durable pipeline is runtime-portable:

```text
registry/config
→ explicit cadence + acquisition lane
→ untrusted staging record with source policy, run ID, and registry digest
→ strict root reconciliation
→ provenance/safety/content compiler gates
→ durable candidate/disposition manifest + heuristic draft
→ semantic review/original-source resolution/corroboration
→ promotion decision
→ playbook/index/eval/changelog change OR rejection/defer record
```

Hermes is a thin scheduler/reviewer. Do not collapse vulnerability knowledge into Hermes `SKILL.md`; workflow/routing changes belong here, while security methodology belongs in vault playbooks and evals.

## Registry policy

Schema v2 materializes stable source ID, role, domain, acquisition lane, cadence, categorical trust, promotion policy, original-source/corroboration requirements, refetch interval, discovery limit, priority, and expected content type. Code/config owns these invariants; models perform semantic novelty, evidence, and applicability judgment.

Fail closed on duplicate YAML keys, malformed required types, duplicate canonical URLs, unknown source IDs, credentialed/private URLs, and contradictory discovery-index policy. An explicit empty allowlist selects nothing. Discovery indexes and report aggregators identify candidates; they are not authority.

## Three cadences

### Daily bounded incremental

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_daily_incremental_learning.sh"
```

Select only `cadence: daily`, use static/feed/deep-link acquisition, and keep budgets bounded. Required order:

```text
acquire → reconcile selected roots → compile/digest only if complete → publish exact daily manifest/pointer
```

Do not launch browser-DOM acquisition merely because the compatibility orchestrator supports it.

### Weekly comprehensive reconciliation

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_weekly_learning_reconciliation.sh"
```

Select daily+weekly roots, run static and browser-DOM lanes, then validate exactly one root per expected source, run ID, cadence, lane, registry schema/digest, and degraded/budget-skip state. The parent combined run ID must be injected into both lanes; component directory suffixes such as `-static` and `-browser-dom` are forensic storage labels, not provenance run IDs. Compile only after complete reconciliation. Weekly provides eventual coverage without a full daily crawl.

### Periodic/on-demand maintenance

Read-only maintenance audit:

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_periodic_learning_maintenance.sh"
```

Targeted backfill or refresh:

```bash
ARGUS_SOURCE_FILTER='exact-stable-source-id' \
ARGUS_BACKFILL_REASON='concrete refresh reason' \
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_targeted_learning_backfill.sh"
```

An explicit targeted backfill may name any configured source, but an unfiltered backfill remains limited to periodic/on-demand eligibility. Never refetch stable foundational sources without an exact allowlist and recorded reason.

## Exact-run handoff

Cadence wrappers publish:

- `<inbox>/learning-run-manifest.json`
- `~/.config/argus/latest-daily-learning-run.json`
- `~/.config/argus/latest-weekly-learning-run.json`
- `~/.config/argus/latest-backfill-learning-run.json`

Review jobs must consume the exact pointer and require `ready_for_review=true`; never infer “latest” from lexical directory order. Reconciliation must precede compilation. An incomplete run still publishes status, but downstream promotion stops.

### Scheduler-migration safety

Before editing a scheduled wrapper or its handoff contract:

1. Inspect OS/Hermes schedules, active processes, and the current run log. Either pause acquisition briefly or let the in-flight run finish; do not assume file edits change a process that already started.
2. Treat any run launched before the final edit as evidence about the old snapshot, never as verification of the finalized code.
3. If that run is incomplete or used pre-final ordering, publish/retain an exact pointer with `ready_for_review=false` so downstream review stops. Proposal artifacts from such a run remain staging and are not promotion evidence.
4. After edits, verify the deployed wrapper order and both scheduler definitions. The completion criterion is: acquire → reconcile → compile only on success → publish pointer, with no overlapping daily/weekly acquisition.

## Shared acquisition state

Static and browser lanes should use one canonical, locked, atomic state service:

- normalize scheme/host/default ports, fragments, query order, and common tracking parameters;
- preserve `first_seen`; track `last_checked`, `last_changed`, and hashes;
- merge concurrent updates under an exclusive lock using unique temporary files;
- quarantine and report corrupt state rather than silently treating it as empty;
- suppress unchanged browser content by hash;
- record per-source health and make repeated processing of the same run ID idempotent;
- recognize `last_checked_at` as the source-health merge clock before an older retained `last_success_at`;
- derive published provenance-error counts from reconciliation's actual `provenance_mismatch_source_ids` field.

Browser acquisition should avoid startup when zero sources are selected, bound total runtime, reject non-public navigation/redirect destinations, avoid unconditional `--no-sandbox`, and emit degraded root records on startup/fetch failures. When cron omits session variables, a scheduled browser wrapper may reconstruct only the current user's owned `/run/user/<uid>` runtime and bus addresses; it must still fail closed if the user manager is unavailable.

Browser runtime v2 adds stronger required invariants: use the dedicated Playwright/PyYAML venv through `run_browser_dom_ingest.sh` or `run_browser_source_triage.sh`; create one context per source; disable downloads and service workers; re-resolve and revalidate every request; block tracker hosts and unsafe/private destinations; use state-aware waits instead of fixed sleeps; and retain only bounded, value-redacted, mode-`0600` network evidence plus hashed manifests and source-derived artifact inventories. `browser_source_triage_selenium.py` is deprecated compatibility glue, not a separate engine.

## Provenance, promotion, and safety

Every candidate must retain source and parent IDs, original/effective URL, retrieval time, content SHA-256, acquisition/discovery lineage, run ID/cadence, registry schema/digest, source role/trust/policy, and backfill reason where applicable.

The compiler stores stable candidate IDs and structured dispositions in:

```text
01 - Learning/Provenance Manifests/<run-id>.jsonl
```

Automatic output is `deterministic-heuristic-draft`, `review_status: pending`, and `promotion_status: proposal_only`. Do not represent generic compiler prompts as extracted methodology. Content length or a familiar hostname must not increase evidentiary trust.

Candidate knowledge types are multi-label: vulnerability pattern, validation technique, architecture/trust boundary, false-positive condition, evidence requirement, reportability criterion, hunting methodology, and tooling/procedure.

For every promote/reject/defer decision, instantiate `08 - Templates/learning-promotion-decision.md.template` and preserve:

```text
candidate ID → source summary → decision → playbook/index/Hermes workflow target
→ eval where applicable → changelog
```

Configured original-source and corroboration gates remain mandatory. Explicit operational phishing/credential-theft workflows, C2, persistence, destructive automation, abuse payload packs, and unnecessary post-exploitation procedures stay quarantined for authorized-scope review and are never promoted as operational methodology.

## Verification discipline

Run the final verification only after the last edit—not merely after an earlier green checkpoint:

```bash
cd "$HOME/SecurityResearch/11 - Scripts/learning"
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m py_compile *.py tests/*.py
for f in *.sh; do bash -n "$f" || exit 1; done
python3 validate_learning_registry.py --config "$HOME/.config/argus/learning-sources.yaml"
```

Then exercise isolated daily, weekly, browser-zero-source, targeted-backfill, reconciliation, compiler, manifest, and maintenance fixtures with separate `HOME`, seen, health, and pointer paths. A useful full-lane fixture binds one healthy root per selected source plus one synthetic substantial candidate to the real registry digest; assert exact root counts, zero provenance mismatches, one draft disposition, pointer readiness, health entries, and zero mature writes.

Do not stop at pure-function tests. Execute Markdown/report rendering, health-state updates for an exact targeted allowlist, incomplete-run pointer publication (`ready_for_review=false`), and compiler/eval/provenance artifact generation. These integration surfaces can reference fields that unit tests never render.

Avoid repeating an expensive live all-source crawl solely for verification. Unless acquisition behavior itself changed, pair the isolated full-lane fixture with one bounded public browser-root smoke (zero deep links and isolated state). Inspect generated records and manifests; verify no mature playbook or mature eval changed.

### Pitfall: green tests before later edits

A green suite is stale evidence once another code or test edit occurs. If a late patch leaves a syntax error, incorrect fixture ID, or empty assertion block, report the work as incomplete and repair/re-run before declaring success. Final claims must cite the post-edit run, not an earlier checkpoint.
