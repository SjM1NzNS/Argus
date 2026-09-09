# Learning Compiler, Provenance, and Promotion Audit

Use this reference when auditing or changing Argus learning ingestion, compiler output, review, promotion, rejection, cleanup, or playbook routing.

## Audit the layers separately

Do not infer executable enforcement from policy terminology. Compare these layers independently:

1. **Ingestion records** — original/effective URL, retrieval time, content hash, source type, acquisition lane, discovery lineage, content quality, and source-native requirements.
2. **Compiler and digest code** — eligibility gate, deduplication, caps, classification, source scoring, proposal/eval generation, and emitted status fields.
3. **Normative policy and templates** — source-quality tiers, required classifications, promotion gates, patch/eval schemas, and mature-playbook safety rules.
4. **Generated drafts** — source summaries, patch proposals, eval proposals, digests, and skipped/rejected audits.
5. **Reviewed outcomes** — curated promotion summaries, no-promotion reviews, changelogs, cleanup logs, and actual playbook/router changes.

A matching label is not proof that policy is enforced. Record whether each rule is: encoded, reviewer-enforced, advisory only, or absent.

## Core semantic checks

### Provenance continuity

Trace one candidate end to end. Verify that a stable candidate ID and at least the following survive through the durable review record:

- original and effective/canonical URL;
- retrieval timestamp;
- content hash and character count;
- acquisition method/lane and extraction version;
- source type and discovery parent;
- reviewer disposition and linked promotion/rejection record.

If inbox/raw material is deleted, require a compact immutable provenance manifest first. A URL-only narrative is insufficient for replaying the exact reviewed source state.

### Trust and corroboration

Keep these concepts separate:

- source quality/evidence rigor;
- source role (official, primary, accepted report, secondary, social, RAG);
- RAG relevance score;
- independence of corroboration;
- exact claims supported by each source.

Check whether quality actually gates proposals/promotion. Do not let content length, hostname substrings, or a high retrieval-relevance score stand in for evidentiary trust. Use effective/canonical hosts with exact or suffix-safe matching.

### Knowledge and promotion classes

Avoid one enum that mixes semantic type, domain, disposition, and destination. Prefer independent fields:

```yaml
knowledge_class: concept | technique | tool_workflow | vulnerability_pattern | false_positive | reportability | severity | target_specific
domain: web2 | web3 | cross_domain
disposition: reject | duplicate | watchlist | defer | propose | promote
promotion_target: vault_playbook | routing_index | eval | hermes_skill | none
```

Verify every documented class is representable in code and outputs; provide `unknown` rather than forcing a class from weak keywords.

### Proposal and eval coupling

Automatic artifacts are drafts. Require a shared candidate ID across:

`source summary -> patch proposal -> eval -> promotion review -> changelog`

A patch proposal should instantiate the patch template: affected target, old/new rule, reason, source, confidence, false-positive/reportability/severity notes, and eval effects. An eval must be source-specific enough to test the proposed rule and include reportability, severity, missing proof, likely triage rejection, next action, disposition, and expected reasoning. Generic class boilerplate is not promotion evidence.

### Rejection and cleanup

Do not conflate rejection, duplicate, watchlist, defer, source-native follow-up, and compiler-cap omission. Emit one structured disposition per candidate, including `duplicate_of`, `deferred_reason`, `follow_up`, and `retention_required` where applicable.

Before cleanup:

1. Compare the durable review, changelog, and cleanup plan for contradictions.
2. Ensure deferred/source-native records marked for retention will actually survive.
3. Preserve provenance manifests and promotion ledgers.
4. Use exact paths, staging, absence checks, preservation controls, and hashes.

### Vault playbooks versus Hermes skills

Argus vulnerability “skills” normally mean vault playbooks routed through Web2/Web3 indexes. Hermes skills are separate `SKILL.md` packages. Require an explicit `promotion_target`; default learning promotion to `vault_playbook`. Patch/create a Hermes skill only for reusable agent execution behavior and only when a named Hermes skill is part of the reviewed promotion.

## Known audit pitfalls

- Broad substring classifiers (for example, a bare `ai`) create recurrent routing errors.
- Deduplication or record caps can be mislabeled as low-quality rejection.
- Source scoring may use the original host while the fetch followed a redirect.
- Browser/deep-link lanes can lose the parent source type or trust metadata.
- Digest “high signal” often means keyword review priority, not promotability.
- Script comments can claim manual compilation while defaults compile drafts automatically.
- Generated summaries may semantically elevate untrusted excerpts under headings such as “Extracted methodology.”
- Defining a changelog path in code does not mean changelog enforcement exists.

## Source-roster and cadence audit

When asked which sources a scheduled learning run uses, derive the answer from the live canonical registry and the same selector code used by ingestion; do not reconstruct the roster from memory or raw YAML scanning alone.

1. Load the configured registry path (normally `~/.config/argus/learning-sources.yaml`) through `learning_registry.load_registry` and enumerate with `select_sources`.
2. Report the registry digest and separate:
   - `daily`: explicitly daily roots only;
   - `weekly`: daily plus weekly roots;
   - `weekly-only`: weekly-selected roots whose effective source cadence is `weekly`;
   - acquisition lanes, especially static/feed/deep-link versus `browser_dom`.
3. Remember that group defaults are materialized by the registry loader. A source that omits a field in YAML may inherit cadence, acquisition, trust, or promotion policy from its group; manual line reading can therefore misclassify it.
4. List on-demand/periodic/backfill sources separately rather than implying they run on the normal schedule.
5. Keep ingestion and promotion distinct: a configured or fetched source remains proposal-only until reconciliation, source-specific review/evals, and an actual reviewed promotion artifact exist.

A concise roster should show the daily roots once, then the additional weekly-only roots, with a summary such as `weekly total = daily + weekly-only` and the static/browser lane counts.

## Evidence-backed reporting format

Deliver:

1. Verdict and current safety boundary.
2. Severity-ranked findings with exact `path:line-range` evidence.
3. Policy-versus-implementation distinctions.
4. Minimal remediation for each finding.
5. Positive controls that already work.
6. Files modified, tests run, and blockers.

State clearly when safety depends on manual review rather than executable enforcement. For review-only tasks, do not modify the workspace or run commands that create caches/artifacts.