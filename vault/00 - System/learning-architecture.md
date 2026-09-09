# Argus Learning Architecture

Status: operational architecture, registry schema v2  
Canonical registry: `$HOME/.config/argus/learning-sources.yaml`

## Design goals

The system optimizes for bounded incremental monitoring, eventual source coverage, provenance, and review-gated knowledge quality. It preserves the existing static and browser-DOM acquisition lanes, compiler, inbox, vault layout, evals, and promotion review. The main architectural change is cadence separation and configuration-driven source policy.

## End-to-end state machine

```text
configured source
  -> selected by explicit cadence/lane
  -> fetched root/discovered deep link
  -> staged JSONL record with registry digest + source policy + run ID
  -> strict root reconciliation
  -> compiler provenance/safety/content gate
  -> durable candidate/disposition manifest + heuristic draft summary
  -> semantic review + original-source resolution + corroboration as configured
  -> mature playbook/eval/index/changelog promotion OR recorded rejection/defer decision
```

Invariants:

1. Ingestion never implies trust.
2. Every compiler output is `proposal_only`.
3. Index/listing records are discovery context, not lessons.
4. `discovery_index` material must resolve to the original linked source before promotion.
5. Promotion requires an explicit review decision, eval impact review, and changelog entry.
6. A registry digest and run ID travel with acquired records and compiled summaries so policy/run drift is auditable.
7. The compiler rejects stale/unbound provenance and labels all automatic output as deterministic heuristic draft material.
8. Quarantine phishing and credential-theft workflows for scope review. Also block C2, persistence, destructive automation, abuse payload packs, and unnecessary post-exploitation procedures from promotion.
9. Hermes consumes an exact ready run pointer rather than guessing the newest directory.
10. A multi-lane run uses the parent combined run ID in every static and browser record; component directory suffixes are forensic storage labels, not provenance run IDs.

## Operational cadences

### Daily — bounded incremental monitoring

Command:

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_daily_incremental_learning.sh"
```

Behavior:

- selects only registry entries with `cadence: daily`;
- runs the inexpensive static/feed/deep-link lane only;
- respects per-source refetch intervals and shared seen-URL state;
- uses bounded source/deep-link/time budgets;
- reconciles all selected roots before compiler/digest generation;
- publishes an exact run manifest and `~/.config/argus/latest-daily-learning-run.json` pointer only after recording reconciliation status;
- does not launch the browser-DOM lane.

The registry currently has eight daily roots. Daily work is intentionally not a complete crawl.

### Weekly — comprehensive reconciliation

Command:

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_weekly_learning_reconciliation.sh"
```

Behavior:

- selects all `daily` and `weekly` roots;
- runs both the existing static and browser-DOM acquisition lanes;
- raises lane budgets so group caps do not silently exclude roots;
- performs deep-link discovery within each source's configured limit;
- respects seen/refetch state;
- reconciles expected roots before compiler/digest generation;
- writes `learning-reconciliation.json` and `.md` comparing expected roots with observed roots and strict registry/run provenance;
- updates `~/.config/argus/learning-source-health.json` with idempotent per-run source health and last comprehensive reconciliation;
- publishes `learning-run-manifest.json` plus `~/.config/argus/latest-weekly-learning-run.json` for exact-run review handoff;
- exits non-zero when expected roots are missing, duplicated, provenance-stale, or degraded.

The current weekly set is 27 roots: 17 static/feed/repository roots and 10 browser-DOM roots.

#### Browser/static egress runtime v3

The browser lane and source triage share `browser_runtime.py` and Playwright rather than maintaining separate Selenium and Playwright policy stacks. `browser_source_triage_selenium.py` is only a compatibility redirect. Static acquisition uses `mandatory_proxy.py`; it does not use ambient `urlopen`/`NO_PROXY` routing for roots, `robots.txt`, or redirects.

Runtime invariants:

- no browser process starts when selection produces zero browser sources;
- each source receives a new incognito context with downloads disabled and service workers blocked; browser launch, context creation, and guard readiness are tracked separately;
- all static and browser HTTP(S) traffic is forced through the credential-free loopback egress proxy; the shared validator accepts only port `1..65535` and rejects `direct://`, remote proxies, userinfo, missing/zero/malformed ports, and path/query/fragment suffixes;
- the proxy rejects a destination when any DNS answer is not strict global unicast, pins the connection to an approved address, kills and cancellation-shields reaping of resolver subprocesses, and bounds semaphore wait plus handling under one connection-lifetime deadline;
- every HTTP(S) navigation, redirect, subresource, static root, and `robots.txt` request crosses that proxy boundary even under hostile `NO_PROXY`; static openers install only HTTP(S) handlers so FTP/file/data redirects cannot escape, while credentialed URLs, private/link-local/loopback targets, unsafe schemes, and known tracker hosts are blocked;
- browser WebSockets are disabled in source-acquisition contexts rather than advertised as captured surfaces;
- fixed sleeps are replaced with bounded DOM, network-idle, and meaningful-content waits;
- incremental DOM traversal bounds scanned nodes and browser-to-Python title/URL/text/attribute transfer, excludes inert/hidden/script/template/SVG content, and persists stopped traversal as lower-bound—not exact—totals;
- request/response metadata and every persisted static/browser URL field are value-redacted; raw exception text is replaced with controlled codes, and byte-bounded evidence is hashed and written mode `0600` below `browser-evidence/<source-id>/`; short/double-encoded/semicolon capability-path tokens, UUIDs, opaque values, and request/correlation IDs are not retained;
- run summaries aggregate retained/truncated/dropped network events and bytes plus blocked total/recorded/dropped samples from per-source manifests;
- shared seen state stores HMAC-SHA-256 URL identities only; migration removes nested and legacy top-level raw URL keys atomically, normalizes naive/aware legacy timestamps to UTC before canonical-collision precedence, ignores malformed timestamps for precedence when a valid timestamp exists, and retains IPv6 brackets;
- production wrappers and persistent CDP Chrome are cgroup-bounded with finite `MemoryMax` and `TasksMax`;
- scheduled browser wrappers reconstruct only the current user's owned `/run/user/<uid>` runtime and bus addresses when cron omits `XDG_RUNTIME_DIR`/`DBUS_SESSION_BUS_ADDRESS`, then fail closed if the user manager remains unavailable;
- sandbox disablement is explicit opt-in only through `ARGUS_BROWSER_NO_SANDBOX=1`.

The browser Python environment is `$HOME/.local/share/argus-browser/venv` with pinned Playwright and PyYAML dependencies. Recreate it with `11 - Scripts/browser/setup_argus_browser_runtime.sh`. Production uses `run_browser_dom_ingest.sh`; manual triage uses `run_browser_source_triage.sh`. The persistent CDP service uses a dedicated private profile and accepts only a validated loopback HTTP proxy.

Zone 0 RAG corroboration for the redirect and DNS-rebinding design (not proof of this implementation): [StackShield](https://stackshield.io/blog/laravel-ssrf-http-client-vulnerability) (`0.9945`) and [IntruderLabs](https://intruderlabs.com.br/en/blog/ssrf-bypass-techniques) (`0.9759`). Both independently emphasize revalidating redirects, rejecting private/reserved answers, and connecting to the exact validated address.

### Periodic / on-demand — maintenance and targeted backfill

Read-only maintenance audit:

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_periodic_learning_maintenance.sh"
```

The audit reports registry integrity, stale playbook review candidates, old unresolved proposals, taxonomy/index path integrity, eval inventory, and repeatedly degraded sources. Staleness is a review signal, not an automatic rewrite trigger.

Targeted backfill:

```bash
ARGUS_SOURCE_FILTER='portswigger-web-security-academy' \
ARGUS_BACKFILL_REASON='refresh after upstream academy restructuring' \
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_targeted_learning_backfill.sh"
```

A targeted backfill requires:

- one or more exact stable registry source IDs;
- a concrete reason preserved in every acquisition record;
- explicit operator invocation.

It can target a source from any cadence and chooses its configured static or browser lane. Stable foundational material is not automatically scheduled.

## Registry schema v2

Group policies provide defaults and source entries provide explicit overrides. `learning_registry.py` materializes effective policy and rejects incomplete or contradictory records.

Required effective fields:

| Field | Meaning |
|---|---|
| `id` | Stable provenance key; source name changes do not break history |
| `role` | `authority`, `primary_research`, `discovery_index`, `report_repository`, `practitioner_commentary`, `watchlist`, or `foundational_reference` |
| `domain` | `web2`, `web3`, `ai_security`, `platform_specific`, `cross_domain`, or `other` |
| `acquisition` | `static`, `deep_link_discovery`, `browser_dom`, `feed`, `repository`, `single_page`, or `transcript` |
| `cadence` | `daily`, `weekly`, `periodic`, or `on_demand` |
| `trust` | `authority`, `primary`, `curated_secondary`, `discovery_only`, or `contextual` |
| `promotion_policy` | `review_required`, `corroboration_required`, `original_source_required`, `proposals_only`, or `context_only` |
| `original_source_required` | Whether a linked/index record must be resolved to its original source |
| `independent_corroboration` | `required`, `conditional`, or `not_required` |
| `refetch_interval_days` | Source-specific minimum refresh interval |
| `deep_link_limit` | Maximum discovered deep links processed per source/run |
| `priority` | Operational ordering/budget hint, not a trust score |
| `expected_content_type` | Expected root/deep content shape for auditing |

Categorical trust affects triage but never grants automatic promotion. Validate the registry with:

```bash
python3 "$HOME/SecurityResearch/11 - Scripts/learning/validate_learning_registry.py" \
  --config "$HOME/.config/argus/learning-sources.yaml"
```

## Knowledge and promotion semantics

A candidate may carry one or more explicit knowledge types:

- `vulnerability_pattern`
- `validation_technique`
- `architecture_trust_boundary`
- `false_positive_condition`
- `evidence_requirement`
- `reportability_criterion`
- `hunting_methodology`
- `tooling_procedure`

The compiler performs deterministic multi-label candidate classification. This is a review aid, not a promotion decision.

Promotion reviewers must record:

1. original source and source role/trust;
2. knowledge type(s);
3. original-source resolution status where required;
4. independent corroboration status;
5. affected playbook/eval/index paths;
6. false-positive and evidence/reportability gates;
7. promotion or rejection rationale;
8. changelog entry for any mature-vault change.

Procedural lessons that change how Hermes operates may additionally update `argus-securityresearch-workflows`. Content-level security lessons normally update vault playbooks/evals and are loaded later through `argus-vault-routing`.

## Provenance and run artifacts

Each acquisition record includes:

- `source_id`, role, domain, acquisition, cadence, trust and promotion policy;
- original-source and corroboration requirements;
- refetch interval and expected content type;
- run ID, run cadence and record kind (`root`, `discovery_page`, `discovered_content`);
- registry schema version and SHA-256 digest;
- `discovered_from` where applicable;
- target/backfill reason when applicable;
- content URL/hash/status and retrieval time.

Weekly reconciliation separates acquisition coverage from learning quality: a complete root traversal does not prove that any lesson deserves promotion.

The compiler retains a compact immutable manifest at `01 - Learning/Provenance Manifests/<run-id>.jsonl`. Each candidate has a stable ID, original/effective URL, content hash, acquisition/discovery lineage, configured policy, and structured disposition (`draft_compiled_pending_review`, duplicate, deferred, provenance quarantine, scope quarantine, or discovery/not-fetched). Promoted lessons must carry that candidate ID into the review decision, playbook change, eval linkage where applicable, and changelog.

`learning-run-manifest.json` in the inbox and the cadence pointer in `~/.config/argus/` bind scheduler review to one exact reconciled run. `ready_for_review=false` means downstream promotion work stops rather than consuming stale output.

Seen/source-health JSON is shared through locked, unique-temp, atomic helpers. URL identity normalizes scheme/host/default ports, fragments, query order, and common tracking parameters. Corrupt state is quarantined with a timestamped filename and reported instead of being silently treated as empty; concurrent lane saves merge under an exclusive lock. Source-health merge precedence uses `last_checked_at` before an older retained `last_success_at`, and published provenance-error counts derive from reconciliation's `provenance_mismatch_source_ids`.

## On-demand offline research cascades

For a reviewed full paper/RFC/advisory that merits bounded fresh-context ideation, use `00 - System/offline-research-cascade.md` and `argus-research-cascade`. This is an on-demand analysis lane, not another acquisition cadence:

- it accepts only a hash-bound local UTF-8 artifact already acquired and sanitized through existing workflows;
- it slices the source into attributed micro-inspiration packets and prepares no-tool fresh-context tasks;
- it performs no network, model, Burp, payload-generation, or target action itself;
- strict result ingestion deduplicates hypotheses while preserving source-fragment lineage;
- all output remains `proposal_only` and every normalized hypothesis must end in one terminal disposition;
- target-specific evaluation remains governed by exact scope contracts, routed playbooks, deterministic owned controls, and separate approval.

The architecture deliberately does not duplicate arbitrary URL fetchers, source databases, generated request corpora, remote uploaders, or ambient Burp-history automation from source research systems. Implement a class-specific local evaluator only when a selected hypothesis justifies it.

## Compatibility and deliberate non-changes

- `learning_ingest.py` and `browser_dom_ingest.py` remain the acquisition engines.
- `run_daily_learning_ingest.sh` remains the reusable two-lane compatibility orchestrator, now parameterized by `ARGUS_LEARNING_CADENCE`.
- Inbox, source-summary, patch-proposal, rejected-lesson, eval, playbook, index, and changelog locations remain unchanged.
- Existing seen-URL state shape remains readable and is migrated through canonical, locked atomic updates; source-specific intervals control refetch eligibility.
- The compiler retains the actual-content gate, adds strict current-provenance/safety gates, emits heuristic drafts only, and never overwrites mature playbooks.
