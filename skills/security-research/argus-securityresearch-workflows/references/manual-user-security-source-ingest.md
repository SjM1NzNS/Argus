# Manual user-supplied security source ingest

Use this branch when the user gives one or more security articles and asks Argus to “learn” them without requesting recurring monitoring.

## Goals

- Preserve the exact supplied sources and provenance.
- Separate author claims from independently corroborated facts.
- Promote only reusable class-level methodology, evidence gates, false-positive controls, and mitigations.
- Keep operational payloads, crash reproducers, real-secret paths, tokens, and unauthorized escalation steps quarantined in raw source material.
- Update seen-state only after review, using hashes compatible with the learning pipeline.

## Workflow

### 1. Route before ingest

1. Load `argus-vault-routing` and this workflow skill.
2. Read `00 - System/web2-skill-index.md` or `web3-skill-index.md` and the likely destination playbooks.
3. Read `00 - System/external-rag-source-policy.md` when a source covers a bypass, payload, CVE, security header, mitigation, exploit technique, false-positive check, or reportability/evidence question.
4. Keep the supplied article as Zone 0 source material; it is not target proof or permission.

### 2. Build an isolated one-time manifest

Use a temporary manifest rather than adding one-off URLs to the persistent learning-source configuration. Normalize canonical URLs by removing analytics parameters and fragments, but preserve the exact user-supplied URL in provenance.

Representative shape:

```yaml
manual_user_security_articles:
  - name: Human-readable source name
    url: "https://example.test/canonical-article"
    type: security_article
    priority: high
    cadence: one_time
    handling: single_page_content
    notes: "User-supplied one-time source; preserve provenance; do not execute linked payloads."
```

Run only the requested pages. For the current Argus ingest, the useful isolation controls are:

```bash
ARGUS_LEARNING_SOURCES=/tmp/manual-sources.yaml
ARGUS_RUN_LABEL=manual-user-security-articles-YYYYMMDD
ARGUS_INCLUDE_BACKFILL=1
ARGUS_MAX_BACKFILL_DEEP_LINK_FETCHES=0
ARGUS_MAX_BACKFILL_LINKS_PER_SOURCE=0
ARGUS_MAX_SOURCES_PER_GROUP=<exact requested count>
```

Do not change persistent monitoring unless the user asks for recurring coverage.

### 3. Preserve source material and prove the access level

The learning candidate record may intentionally contain only a bounded excerpt. For reviewed user-supplied sources, also preserve when legitimately available:

- raw HTML or original document bytes;
- response headers and effective canonical URL;
- an offline extraction of the **actually accessible article body**;
- retrieval timestamp, byte size, and SHA-256;
- upstream advisory, patch, or PR metadata/patch when the article cites one.

Before calling anything “full text,” inspect platform state and the semantic article container. Paywalled/published platforms may return a large rendered DOM whose bulk is serialized application state, recommendations, or scripts while the article itself is only a locked preview. Record explicit access state such as `full_article`, `locked_preview_only`, `shell/index`, or `blocked`; preserve declared word count and accessible article-character count when available. Never bypass a paywall or reconstruct hidden article claims from unrelated sources.

Keep three artifacts distinct when needed: rendered HTML (raw evidence), rendered visible-DOM text (browser evidence), and clean article-container text (review material). A large HTML/DOM byte count is not evidence of a substantive article body.

Write an acquisition manifest that maps supplied URL → canonical URL → access state → raw/rendered/article filenames → sizes/hashes. Never embed API keys or private credentials.

### 4. Extract selectively

For each source, record separately:

- author claims;
- affected component and exact entry point;
- prerequisites and attacker reachability;
- primitive versus claimed escalation;
- safe validation method and negative controls;
- false-positive/downgrade conditions;
- remediation and fix verification;
- reportability/authorization boundaries.

Promote class-level invariants, not literal payload lists. Examples:

- authentication articles → server-side assurance-state and artifact-binding gates;
- native parser articles → entry-point reachability, post-transformation length contracts, local sanitizer validation, and patch/backport checks;
- file-processing articles → effective loader graph, inert owned-canary proof, worker isolation, and secret-policy routing.

Keep exact crash bytes, brute-force candidates, real secret paths, credential minting, role assumption, customer-data access, and destructive/concurrent test recipes out of reusable playbooks.

### 5. Corroborate precisely

Run one exact Preview.is RAG query per technique, not one broad query for the whole batch. Cite only returned URLs used.

Then inspect direct primary sources when available:

- upstream patch/PR and merged commit;
- vendor/framework advisory;
- release notes or backport record;
- authoritative vulnerability database entry.

A PR merged to `main` does not prove which maintenance release contains the fix. If no authoritative release/backport mapping exists, preserve the article's version table as a secondary claim and require commit-equivalent or release-advisory evidence. Never invent a CVE or patched version.

### 6. Promote into the existing class-level library

Prefer, in order:

1. patch an existing playbook cluster;
2. create a new class-level playbook cluster only for a real routing gap;
3. update the Web2/Web3 skill index triggers and loads;
4. add focused eval scenarios that encode positive, downgrade, and stop conditions;
5. write a reviewed source summary under `01 - Learning/Source Summaries/` as the promotion ledger.

Do not create one playbook per article. When an article only adds a mechanism to an existing CVE/class, patch that existing cluster and eval suite.

### 7. Update seen-state after review

Check the run summary rather than assuming a one-time/backfill run marked the source seen. If reviewed records need to be added manually:

- use the trusted canonical acquisition URL from the isolated manifest, not a sanitized/redacted evidence URL;
- canonicalize it with the shared learning-state helper and persist only the keyed-HMAC identity in the canonical nested `urls` bucket;
- use the clean accessible-body/candidate hash and character count that future ingest will compare, not the raw rendered-HTML hash/size;
- copy `retrieved_at`, source ID/group, access state, and final review disposition;
- update under the shared exclusive lock, write JSON atomically, enforce mode `0600`, and validate it parses;
- confirm all reviewed identities, hashes, lengths, and dispositions match the acquisition/review ledger;
- recursively audit the **entire state document**, including top-level keys and legacy metadata buckets, for `http://` or `https://` keys/values. Do not check only `state["urls"]`.

If legacy raw URLs exist outside the canonical `urls` bucket, migrate each through the shared canonicalizer/HMAC helper, merge deterministically into `urls`, remove the raw entry in the same locked atomic replacement, and rerun the recursive zero-raw-URL assertion. An additive merge that leaves stray top-level URL keys is not a completed migration.

This avoids sanitized-URL identity collisions, prevents a raw capture hash from breaking normal deduplication semantics, and avoids marking unreviewed, failed, shell-only, or preview-only material as fully learned.

### 8. Validate before completion

Minimum deterministic checks:

- every requested source is substantive, not merely a shell/index/error page;
- verify every manifest-declared artifact against **both** byte count and SHA-256, resolving paths from the manifest's documented base (acquisition entries, capture manifests, and primary-corroboration manifests may use different relative roots);
- verify each capture manifest's ledger hash and cross-check any duplicate hash recorded by the acquisition manifest;
- recursively check the run root and every private evidence descendant: directories `0700`, files `0600`; do not inspect files while overlooking a permissive parent directory;
- all promoted files and internal/index references exist and are non-empty;
- YAML frontmatter and fenced code blocks are balanced;
- no stray patch markers remain;
- new index routes resolve to real files;
- eval numbering is sequential and includes downgrade/stop cases;
- seen-state matches candidate hashes and lengths;
- scan the **exact promoted-file allowlist**, not the whole vault, for quarantined payload/tool/exploit strings; manually distinguish a safe routing/stop trigger (for example, an endpoint name) from an executable operational procedure;
- parse actual Markdown link targets (`](https://...)`) rather than every URL-shaped string in frontmatter or prose delimiters. Validate through the mandatory proxy. Treat `404`, transport failure, and invalid TLS as hard link failures; record `403` as reachable but access-controlled, not content-verified;
- replace dead links with a current primary/effective URL when authoritative. If a saved RAG/source snapshot remains evidentially relevant but the upstream is now dead or has invalid TLS, remove the live hyperlink and label it honestly as a retained snapshot instead of silently preserving a broken citation;
- the reviewed source summary records validation and explicit non-actions.

After any permission or citation repair, rerun the complete artifact/link check and report counts (artifacts checked, hash/size mismatches, permission errors, links checked, hard failures). If the vault is Git-backed, also run `git diff --check`; otherwise record that the deterministic vault checks are the applicable guard.

## Pitfalls

- **Rendered application state mistaken for article text:** `<script>` JSON, styles, templates, hidden UI, recommendations, and paywall chrome can dwarf the accessible body. Exclude non-visible nodes in browser extraction and inspect the semantic article container plus platform lock state before declaring content substantive.
- **Locked preview called full text:** record preview-only access honestly, preserve it, and hold article-specific methods until legitimate full-text or author-shared access exists.
- **Wrapper manifest argument silently ignored:** pass the isolated manifest through the wrapper's documented environment/config variable and verify the selected source IDs/count before trusting the run label.
- **Bounded excerpt mistaken for preservation:** candidate JSON may prove quality but is not a full auditable capture.
- **Tracking URL stored as canonical:** strip analytics parameters for fetching/deduplication but retain the supplied URL in provenance.
- **One-time source added to recurring config:** use an isolated manifest unless recurring monitoring was requested.
- **Seen-state updated before review:** mark only substantive reviewed records after promotion/disposition.
- **Wrong hash domain:** raw HTML SHA-256 is for evidence integrity; candidate `content_hash` is for ingest deduplication.
- **Secondary version table treated as authoritative:** require release/backport evidence.
- **Primitive collapsed into escalation:** file read is not automatically credential compromise/RCE; parser memory corruption is not automatically remote RCE or meaningful DoS.
- **Operational payload promotion:** preserve dangerous examples only in quarantined raw material and replace them with safe canary/local-harness gates in reusable playbooks.
