# Historical security-article verification and promotion

Use this reference for manual or scheduled reviews of security research articles, CVE writeups, exploit-chain retrospectives, and technique posts before they become durable Argus guidance.

## Core rule

Promote **class-level invariants and proof gates**, not an article's narrative or headline. A secondary article, external RAG match, scanner result, CVE identifier, or version string is Zone 0 material until source-native evidence establishes each claimed edge.

## 1. Capture and provenance

For every source retain:

- supplied URL and resolved/final URL;
- access date and archive timestamp where applicable;
- source-native body (`article.txt` plus raw HTML/headers when useful);
- explicit browser-fallback note when robots rules or client rendering prevent the collector from producing a normal record;
- canonical CVE/vendor/specification/code references used for verification.

A browser fallback may repair capture coverage, but it does not upgrade the article's authority.

## 2. Source hierarchy and claim ledger

Review claims in this order:

1. canonical CVE record and vendor advisory;
2. fixed-versus-affected source/code or upstream patch;
3. relevant standards and language/runtime documentation;
4. source-native technical analysis;
5. Preview.is or other external RAG corroboration;
6. aggregators, headlines, and scanner/version assertions.

For each material claim record one of:

- **confirmed** — primary evidence supports the exact claim;
- **conditional** — a primitive is real, but downstream impact needs additional edges;
- **analogous only** — useful class-level corroboration, not evidence for this implementation;
- **rejected/overclaimed** — source does not support the stated scope, severity, or chain.

Preview.is scores help prioritize reading, not decide truth. An exact high-score result can corroborate technique mechanics; a high-score but wrong CVE/product remains irrelevant. Save the exact query and JSON/Markdown result pair.

## 3. Decompose impact chains

Never collapse multi-stage chains into one finding. Build an edge matrix and prove each boundary separately. Common examples:

- browser eligibility to send a cookie → proxy actually forwards that header → backend action accepts it;
- delimiter/control-byte injection → downstream parser accepts a second command → response/key misassociation → sensitive data reaches the attacker;
- untrusted structured data → exact DOM sink → browser execution → privileged victim/meaningful action;
- parser accepts `NaN`/Infinity → validation comparison behaves unexpectedly → stored/transformed value reaches a safety-critical consumer → concrete business effect;
- download/quarantine state → launch behavior → local-file rendering → origin inheritance → permission/API access.

A missing edge downgrades the claim; it must not be filled with article prose or CVSS language.

## 4. Vendor URL drift and false primary sources

Old vendor support IDs can return HTTP 200 after redirecting to an unrelated advisory. Do not treat status code or vendor hostname as proof.

Validate every retained vendor page by checking:

- page title/product/release;
- expected CVE or issue identifier;
- affected and fixed versions;
- security-component text;
- whether the resolved URL is the current canonical location.

If an obsolete URL resolves to unrelated content, preserve the correct current page and classify the obsolete capture as disposable/incorrect evidence.

## 5. Promotion gate

Promote only material that adds at least one reusable item:

- invariant or boundary model;
- evidence requirement;
- false-positive/downgrade condition;
- mitigation hierarchy;
- routing trigger;
- adversarial eval scenario.

Prefer patching existing class playbooks. Create a new class-level playbook only when no existing class covers the primitive. Keep historical specifics in a source summary or this skill's references rather than creating one skill per article/CVE.

Every promotion should update, as applicable:

1. class playbook(s);
2. routing index;
3. source summary with URLs and claim disposition;
4. eval suite with positive, negative, incomplete-chain, and fixed-control cases;
5. monthly changelog;
6. run summary and target-specific finding count.

## 6. Validation and manifest discipline

Before completion verify:

- every promoted and routed path exists and is non-empty;
- source-summary copies are byte-identical when both inbox and durable copies exist;
- eval numbering is contiguous and expected count matches;
- routing triggers and changelog entry occur exactly as intended;
- promoted Markdown has closed frontmatter and no NUL bytes;
- no API key/header assignment appears in promoted artifacts;
- approved cleanup removed only the authorized paths;
- retained replacement/control sources still exist.

Build `source-manifest.sha256` from **immutable source/provenance artifacts only**: article captures, primary references, source metadata, and saved RAG records. Exclude mutable run summaries, cleanup notes, validation reports, and the manifest itself. Run `sha256sum -c` after cleanup and record the entry count.

## 7. Cleanup approval sequence

1. Produce an exact cleanup inventory with path, size, and reason.
2. Separate obviously incorrect/disposable captures from useful raw provenance.
3. Ask the user to approve a specific set; do not delete by category shorthand.
4. Delete exactly the approved paths.
5. Verify absence plus retained replacement controls.
6. Regenerate the immutable-source manifest.
7. Rerun structural validation and write a final report.

Raw HTML, response headers, source-native text, primary references, and RAG query records should normally be retained unless the user explicitly approves a broader cleanup.

## Completion report

Report compactly:

- articles reviewed;
- target-specific findings versus learning-only dispositions;
- Preview.is exact/analogous/weak result quality;
- promoted artifact and eval counts;
- manifest and structural-validation status;
- approved deletion count/bytes;
- paths to durable summary, evals, validation report, manifest, and changelog.
