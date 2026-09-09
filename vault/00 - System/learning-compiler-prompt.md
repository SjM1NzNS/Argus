# ARGUS LEARNING COMPILER PROMPT

Process the newest learning inbox folder under `~/SecurityResearch/01 - Learning/Inbox/YYYY-MM-DD/` or the folder explicitly provided by the user.

Input files usually include:
- `learning-candidates.jsonl`
- `learning-run-summary.md`
- manually added source notes
- report outcomes
- triager feedback
- tool-output reviews

## Hard content-quality gate

The compiler must prioritize **actual source content**, not indexes or source roots.

Compile only records that meet all of these conditions unless the user explicitly asks for discovery analysis:

- `local_processing_status=fetched_content`
- `content_quality=actual_content`
- substantial `content_excerpt` / `content_char_count`

Treat these as discovery context only, not learning lessons:

- `fetched_index_metadata`
- `content_quality=index_or_listing`
- topic pages, homepages, source roots, all-topics pages, report lists, GitHub org/repo landing pages
- skipped/deferred/backfill records

If a run contains few `actual_content` records, report that the ingest was learning-incomplete rather than padding compiler output with index pages.

The compiler's job is not to hoard articles. The job is to compile sources into actionable security methodology:

source → source summary → technique extraction → affected surfaces → preconditions → test method → evidence requirements → false positives → scope risks → severity limits → skill patch proposal → changelog → eval update.

For every item, produce or update the appropriate notes:

1. source summary
2. extracted technique
3. affected surfaces
4. preconditions
5. attacker model
6. victim/protocol model
7. exploit or abuse path
8. minimal test method
9. evidence requirements
10. common false positives
11. scope risks
12. tooling support
13. reportability criteria
14. severity limits
15. skill patch proposal
16. changelog entry
17. eval update proposal

## Required knowledge classification

Assign one or more of the bounded candidate knowledge types carried by registry schema v2:

- `vulnerability_pattern`
- `validation_technique`
- `architecture_trust_boundary`
- `false_positive_condition`
- `evidence_requirement`
- `reportability_criterion`
- `hunting_methodology`
- `tooling_procedure`

Also retain the existing vulnerability-class/domain classification for vault routing. Multi-label classification is expected: for example, one source may contribute a validation technique, an evidence requirement, and a false-positive condition. Classification is a review aid and never authorizes promotion.

## Source quality and promotion policy

Use the categorical registry fields (`role`, `trust`, `promotion_policy`, `original_source_required`, and `independent_corroboration`) as the authoritative promotion semantics. Use `~/SecurityResearch/00 - System/source-quality.md` and the legacy 0–10 quality value only for triage within the configured policy.

Rules:
- Every compiler output starts as `promotion_status: proposal_only`.
- Authority/primary material still requires manual review and eval/changelog review.
- `original_source_required` material cannot be promoted from an index/listing or abstract; resolve and inspect the original linked source.
- `corroboration_required` material cannot be promoted until independently corroborated.
- `proposals_only` and `context_only` material cannot directly update a mature playbook.
- Accepted reports, rejected reports, duplicates, and triager feedback may have high learning value, but their disposition and provenance must be preserved.

## AppSec.fyi rule

Treat AppSec.fyi as a curated vulnerability-topic index, not a final authority.

For AppSec.fyi linked resources:
1. Score the original linked resource independently.
2. Compile only high-signal linked resources.
3. Prefer top 5–10 high-signal resources per topic per run.
4. Deduplicate by URL.
5. Mark unavailable/paywalled/dynamic/shallow items as `manual_review_required` or `rejected_low_signal`.
6. Do not create changelog entries unless the linked resource causes a meaningful skill change.

## Web3 extraction rule

For every Rekt, Immunefi, or Solodit item, extract:

- protocol type: bridge, lending, staking, vault, AMM, oracle, governance, account abstraction, cross-chain messaging, key management, supply chain, other
- root-cause category: access control, missing validation, oracle manipulation, share accounting, rounding/precision, signature replay, reentrancy, upgradeability/proxy issue, bridge proof/message validation, admin/private key compromise, dependency/supply chain, economic design flaw, other
- attacker path: required permissions, transaction sequence, external dependencies, assumptions
- impact: stolen funds, frozen funds, minted unbacked assets, governance/control compromise, insolvency, data/key compromise, gas/efficiency only, unclear
- hunting lesson: invariant, code pattern, Foundry/Slither/Echidna test, false positives to avoid
- reportability lesson: proof needed, likely severity, downgrade conditions, assumptions triage would reject
- skill patch recommendation: affected Web3 playbook, rule to add/change, confidence, eval case to create/update

## Output locations

Use:
- Source summaries: `~/SecurityResearch/01 - Learning/Source Summaries/`
- Skill patch proposals: `~/SecurityResearch/01 - Learning/Skill Patch Proposals/`
- Rejected/low-signal lessons: `~/SecurityResearch/01 - Learning/Rejected Lessons/`
- Changelog draft/current month: `~/SecurityResearch/07 - Skill Changelog/YYYY-MM.md`
- Eval proposals/stubs: `~/SecurityResearch/06 - Evals/Web2/` or `~/SecurityResearch/06 - Evals/Web3/`

## Promotion workflow

For every candidate, preserve the stable `candidate_id` from `01 - Learning/Provenance Manifests/<run-id>.jsonl`. Before any mature change, instantiate `08 - Templates/learning-promotion-decision.md.template` and link source summary → decision → playbook/index/Hermes-skill target → eval where applicable → changelog. A patch is incomplete if this chain is missing.

## Safety scope quarantine

Keep `scope_review_required` candidates in untrusted staging. Do not promote phishing or credential-theft workflows, C2 infrastructure/procedures, persistence, destructive automation, abuse-oriented payload packs, or unnecessary post-exploitation procedures. Defensive analysis that mentions these topics still requires an explicit authorized-scope decision before use.

## Mature skill safety

Do not directly overwrite mature skills unless:

1. the record is bound to a registry source ID and digest,
2. the configured original-source and corroboration gates are satisfied,
3. the lesson is specific/actionable and source quality is sufficient within that policy,
4. false-positive risk is understood,
5. evidence, reportability, and severity implications are explicit,
6. a changelog entry is written,
7. relevant evals are updated or proposed,
8. the reviewer records an explicit promotion decision.

No configured source role or numeric quality score permits automatic promotion. When unsure, write a skill patch proposal instead of modifying a playbook.
