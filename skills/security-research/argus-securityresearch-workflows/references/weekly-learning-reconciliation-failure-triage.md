# Weekly Learning Reconciliation Failure Triage

Use this reference when an exact weekly Argus learning pointer is incomplete, source health disagrees with reconciliation, or a two-lane run cannot reach semantic review.

## Fail-closed review order

1. Read the exact cadence pointer; never infer the newest run from directory names.
2. Read `learning-run-manifest.json`, but treat it as a derived summary.
3. Read `learning-reconciliation.json` before any candidate content. Compare expected, observed, missing, degraded, duplicate, and provenance-mismatch source IDs.
4. Inspect static and browser component logs independently. A combined summary can exist even when one component never produced records.
5. Cross-check selected roots against registry-v2 role, trust, promotion policy, original-source, and corroboration fields.
6. Inspect shared source health only after the exact reconciliation. If they disagree, report the state inconsistency and use the exact reconciliation as the run-level authority.
7. Stop before semantic content review unless reconciliation is complete and the exact pointer says `ready_for_review=true`.

## Two-lane provenance invariant

Component directory names such as `<parent>-static` and `<parent>-browser-dom` are forensic storage labels. Every record in both components must carry the parent combined run ID. Inject the parent ID into each acquisition process rather than rewriting concatenated JSONL afterward; post-acquisition rewriting weakens byte-level provenance.

A regression fixture should assert both lane launchers receive the parent ID and an isolated acquired record retains it. Keep component folders for evidence.

## Derived-summary disagreement

Do not trust a zero count merely because a manifest field is zero. Confirm that publisher field names match the reconciliation schema. For example, provenance totals must derive from `provenance_mismatch_source_ids`, not an invented or obsolete field. Preserve the failed manifest as historical evidence; fix publication code for future runs rather than silently reclassifying the old run.

Also compare same-named URL counters by population and canonicalization rules. `learning-reconciliation.json` counts canonical non-root candidate URLs using `effective_url` before `url`, while a publisher may count every record URL, including roots, and use a different duplicate formula. A manifest can therefore label all record URLs as `candidate_url_count` even though reconciliation reports a smaller non-root candidate population. This does not invalidate exact run identity or `ready_for_review`, but the counters must be normalized or renamed before they are used as coverage/yield evidence.

## Source-health merge pitfall

Health entries can retain an older `last_success_at` while receiving a newer failed `last_checked_at`. Merge precedence must use the event clock (`last_checked_at`) before the retained success clock, or stale healthy state can overwrite a current degraded update. Test this with an older healthy record plus a newer degraded record that intentionally has no new success timestamp.

## Cron browser-manager recovery

A user cron environment may omit `XDG_RUNTIME_DIR` and `DBUS_SESSION_BUS_ADDRESS` even when the user systemd manager is active. A scheduled wrapper may derive only the current user's owned `/run/user/<uid>` and owned bus socket, then retry the manager check. Retain fail-closed cgroup behavior if the manager is genuinely unavailable. Verify with a cron-like `env -i` fixture and a harmless bounded command, not a public-source crawl.

## Promotion and decision artifacts

An incomplete run is deferred at the run gate, not semantically rejected. If the compiler never produced durable candidate IDs, do not instantiate candidate promotion-decision templates: doing so fabricates lineage. Report zero promotions/rejections and identify the raw material as unreviewed/deferred.

Do not promote source summaries, playbooks, evals, or routing changes from an incomplete run. Operational pipeline repairs may update architecture, workflow references, tests, and changelog independently.

## Verification matrix

After repairs, run:

- registry-v2 validation;
- focused RED/GREEN regressions for parent run ID, source-health precedence, publisher counts, and cron-like browser-manager access;
- the complete learning test suite;
- Python compilation and shell syntax checks;
- one isolated dry-run record proving parent-ID binding;
- read-only maintenance audit for missing indexes, stale playbooks/proposals, overdue sources, and repeated degradation.

Avoid rerunning an expensive all-source acquisition solely to validate orchestration repairs. Preserve the failed run and let the next scheduled acquisition provide production evidence, unless the user explicitly requests a fresh crawl.
