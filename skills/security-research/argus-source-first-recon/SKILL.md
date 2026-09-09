---
name: argus-source-first-recon
description: Use when mapping authorized Web/SPAs, local source trees, JavaScript bundles, source maps, OpenAPI documents, structured API errors, or evidence artifacts. Enforces exact-source provenance, local-only deterministic parsing, redacted outputs, scope-gated replay, candidate disposition, and comparable cross-run evidence. Never performs network requests or secret validation by itself.
version: 1.3.29
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security-research, source-first, javascript, source-maps, openapi, evidence]
    related_skills: [argus-vault-routing, argus-securityresearch-workflows]
---

# Argus Source-First Recon

For reusable JVM/process/plugin/task-worker pools, sidecars, and other cross-request execution hosts, use `references/reusable-worker-cross-task-isolation.md`. It separates serial concurrency from lifecycle isolation; inventories surviving threads, processes, classloaders, global identity context, and credential caches; defines a real-handler/fake-credential sequential canary; and requires public-fix differentials plus deployment-level tenant-pool proof.

For cryptographic and attestation verifiers that consume ordered collections of claims, measurements, certificates, or digests, use `references/cryptographic-verifier-duplicate-key-and-policy-composition.md`. It covers partial-key first/last/any-match ambiguity, exact-value verification invariants, three-control simulator proofs, downstream policy-composition sinks, released-version and advisory differentials, duplicate/no-go gates, and precise remediation that preserves protocol-valid multi-algorithm records.

For fixed-commit OSS candidates that may overlap active public fixes, use `references/oss-public-prior-art-and-repository-saturation.md`. It defines exact-duplicate, same-root consequence, adjacent-family, incomplete-fix, and distinct-root classes; requires PR-diff and advisory review plus a two-way remediation test; treats parallel-agent findings as unverified leads; and provides a repository-saturation pivot gate when an active hardening series already covers the subsystem.

For authenticated export, archive, portability, signed-URL, and component-download authorization testing, use `references/authenticated-export-signed-download-authorization.md`. It defines minimal two-owned-account fixtures, UI hydration and exact-dialog/checkbox gates, source-derived selector tuples, mandatory post-reauth A->A/B->B positive controls before a one-shot foreign probe, private-versus-sanitized evidence rules, reauth-aware dispositions, reversible source cleanup, disposable-clone handling, and the required ledger-before-manifest finalization order.

For fixed-point SPA chunk closure and safe retries when a server omits a public CA intermediate, use `references/frontend-chunk-closure-and-tls-chain-retry.md`. It covers multiple literal lazy-import forms, manifest-bounded closure, AIA artifacts as untrusted input until root validation, temporary augmented trust bundles, hostname verification, and the prohibition on `-k`/`--insecure`.

For Next.js/webpack applications, use `references/nextjs-webpack-closure-and-secret-sanitization.md`. It covers locale-redirect staging, root-literal manifests, runtime `.e(id)` plus `.u` filename resolution (including alias maps), fixed-point dynamic closure, syntax checks for extensionless evidence via stdin, client-identifier redaction before contextual inspection, and dual original-versus-sanitized ledger accounting.

For authorized no-session testing of Next.js private account routes, use `references/nextjs-auth-gate-and-no-session-bypass-controls.md`. It defines the normal-page/data-path/private-backend matrix, no-follow redirect evidence, scoped `__NEXT_DATA__.props.pageProps` inspection, generic-500 disposition, owned-marker stop gates, primary-advisory version checks, bounded path/header/session/JWT mutation families, adaptive header isolation, explicit high-risk exclusions, and evidence-validator schema/reclassification gates.

For deterministic next-target ranking and source-mapped AI/MCP/Skill registries, use `references/cluster-selection-and-ai-registry-gates.md`. It adds deployment-cluster sibling deduplication, thin-branch cut/continue rules, attribution-aware cloud-backend scope classification, client-versus-backend role and validation gates, browser-fetch-versus-SSRF distinctions, and agent supply-chain reportability requirements.

For exact first-party CLI/package boundaries exposed by frontend source, use `references/official-cli-package-provenance-and-symlink-fixtures.md`. It separates metadata, archive-only static review, and separately authorized owned module execution; covers hash and tar safety gates, distinct API/public-registry leads, lexical-versus-real path analysis, normal-clone Git symlink evidence, natural supported-slug controls, entrypoint-fidelity and asset-eligibility gates, independent technical/impact/reportability verdicts, and conservative HOLD/Low disposition when a real primitive is not submission-ready.

For mission closure, ledger reconciliation, and safe evidence retention when a vault is not a Git worktree, use `references/evidence-hygiene-without-git.md`. It distinguishes Git cleanliness from filesystem hygiene, requires schema inspection before ledger arithmetic, redacts authentication-adjacent response capabilities, and reruns verification after the final report write.

For authentication-adjacent URLs in HTML, headers, HARs, JavaScript, and derived inventories, use `references/authentication-adjacent-url-sanitization.md`. It requires HTML decoding before parsing, removal of userinfo, value-free query inventories, fragment redaction, immutable private raw evidence, focused parser tests, and regeneration plus post-scan when a derivative retained capability material.

For Keycloak/OIDC source-first validation, use `references/oidc-keycloak-source-first-validation.md`. It covers bounded no-follow redirect matrices, callback canonicalization and PKCE chain gates, exact browser User-Agent verification, manual password/CAPTCHA boundaries, static-resource version-range fingerprinting, CVE prerequisite gates, guest action disposition, and extractor/redaction verifier pitfalls.

For OpenID/OIDC/OAuth/SAML account-linking callbacks, use `references/federated-identity-linking-csrf-validation.md`. It defines the session-bound link-intent invariant, real-provider signed-assertion harness, distinct attacker/victim request proof under deployed singleton lifetime, persistence plus fresh-login ATO closure, replay and trust-policy controls, cluster/browser gates, clean-patch evidence packaging, and separate technical/OSS-program/production-service dispositions.

For endpoints that authorize one visible anchor and then expand an internal index/cache/relation query into additional objects, use `references/internal-query-authorization-and-indirect-serializer-disclosure.md`. It treats internal queries and generic serializers as separate authorization boundaries; uses sibling-caller and branch differentials; requires direct-hidden-denial versus indirect-byte disclosure controls; preserves configuration/data-shape prerequisites; and packages focused plus full-suite evidence against an exact pin.

For public WordPress/custom-theme reconnaissance, use `references/public-wordpress-theme-and-rest-gates.md`. It covers exact canonical/theme/GTM executable closure, live-instantiation gates for legacy AJAX code, passive core-versus-plugin REST triage, a two-step non-executable reflected-XSS context ladder, author-trust boundaries, advisory/RAG confidence gates, and post-closure accounting order.

## Overview

Use this skill to turn already-collected, in-scope source artifacts into a deterministic attack-surface inventory. It adapts selected methodology from `uphiago/recon-skills` without importing its network automation, agent-policy files, credential workflows, mutable dependencies, or offensive execution defaults.

This skill is **local-only**. Its scripts read operator-supplied files and write redacted structured outputs. They do not resolve DNS, fetch URLs, contact APIs, validate credentials, execute JavaScript, install dependencies, or mutate targets.

## When to Use

Use for:

- saved HTML, JavaScript, TypeScript, runtime config, manifests, and source maps;
- fixed-commit public source trees;
- OpenAPI/Swagger JSON or YAML already acquired within scope;
- structured validation/error responses already captured through an approved request;
- HAR evidence that must be sanitized before notes, reports, or upload packages;
- repeated source-first passes that need comparable inventories and deltas.

Do not use this skill as authorization to:

- guess or crawl endpoints;
- contact source-mentioned sibling or third-party hosts;
- validate candidate keys or credentials;
- enumerate objects, tables, accounts, sessions, or IDs;
- send `POST`, `PUT`, `PATCH`, `DELETE`, uploads, or workflow-triggering `GET`s;
- publish packages, open PRs, trigger CI, or touch self-hosted runners.

## Workflow

### 1. Lock scope and provenance

Before parsing, record:

- program and exact in-scope asset;
- source acquisition URL or repository `commit:path`;
- capture timestamp;
- acquisition method;
- SHA-256 of every artifact;
- whether the artifact is target-owned, third-party, generated, or researcher-authored.

Completion criterion: every input has an origin and digest; each source-mentioned host is classified as an explicit asset, a directly embedded functional application backend, or unrelated/context-only infrastructure. Provider-domain naming alone must not create either automatic authorization or an automatic hard border.

### 2. Build the local source inventory

Run:

```bash
python3 scripts/extract_source_inventory.py \
  --input /path/to/saved-assets \
  --output /path/to/source-inventory.json
```

The parser inventories exact files, validates source maps, inspects embedded `sourcesContent` without writing reconstructed plaintext, and emits candidates for:

- URLs and origins;
- API-like routes and methods;
- source-map references;
- literal static/lazy asset references with source location and reference kind;
- auth/session header names and storage patterns;
- object, tenant, account, and workflow selectors;
- upload/export/import/action signals;
- feature flags and environment names;
- browser or server sinks;
- secret-like values represented only by type, length, hash prefix, and source location.

Completion criterion: output is deterministic JSON, mode `0600`, and contains no candidate secret plaintext. For bundled SPAs, also iterate all literal reference forms (`/assets/`, `assets/`, relative `import("./...")`, preload maps, `new URL(..., import.meta.url)`, and relevant CSS references) until `referenced - acquired` is empty; one extractor pattern or one successful batch is not graph exhaustion.

### 3. Parse an acquired API specification

Run:

```bash
python3 scripts/extract_openapi_inventory.py \
  --input /path/to/openapi.json \
  --output /path/to/openapi-inventory.json
```

YAML is supported only when local PyYAML is already available; the script never installs it. Preserve method, path, operation ID, parameters, security requirements, request-body media types/schema references, and response schema references.

Completion criterion: every operation retains specification provenance and is still only an inventory lead.

### 4. Rank exact source-derived surfaces

Rank locally before any replay:

1. auth/session/token refresh and identity boundaries;
2. admin, role, tenant, organization, account, and object selectors;
3. read/export/download and prior-state retrieval;
4. upload/import/job/action and state transitions;
5. runtime config, feature flags, alternate API versions, and environment bases;
6. CI/CD workflow, package/registry, release, SBOM, and build paths for fixed-commit OSS review.

Mark each item:

```text
source_mapped -> candidate -> validated -> reportable
```

or:

```text
blocked | disproved | out_of_scope | accepted_behavior | duplicate_risk
```

Never delete a failed lead merely because it is not reportable. Preserve the disproving control and disposition.

### 5. Gate any live replay separately

A parsed route is not authorization. Before an approved request, establish:

- explicit scope membership or documented functional-backend attribution to an in-scope application;
- for provider-hosted endpoints, whether the in-scope client directly embeds and uses the exact endpoint as its production backend, whether tokens and product-specific operations bind it to the app, and whether the program expressly excludes it;
- state semantics, not only HTTP method;
- actor/account/object model;
- smallest safe request and stop condition;
- random-path or catch-all control;
- no-auth, malformed-auth, and owned-auth comparison where relevant;
- owned/synthetic data plan;
- request count, pacing, redirect, and response-size limits.

Start with exact source-derived read-only `GET`/`OPTIONS` only when the target contract permits them. Queue every mutation, upload, token/login, workflow action, export with a real ID, or cross-account check for its own plan/approval.

Completion criterion: a request plan exists independently of the source inventory.

### 6. Sanitize evidence before promotion

Run:

```bash
python3 scripts/sanitize_har.py \
  --input /path/to/raw.har \
  --output /path/to/sanitized.har
```

The sanitizer redacts:

- all cookie values;
- authentication, API-key, CSRF, token, and secret headers;
- sensitive query parameters;
- JSON/form body fields with sensitive names;
- sensitive response-body fields;
- WebSocket payloads by default;
- email addresses and bearer/JWT/key-like strings in text fields.

Keep raw evidence private with restrictive permissions. Never assume image black bars are irreversible; flatten and visually verify redacted screenshots.

Completion criterion: sanitized artifact passes the script's post-redaction scan and is separately hashed.

### 7. Compare repeated runs correctly

Use `templates/cross-run-delta.yaml` and distinguish:

- `newly_observed` from `newly_introduced`;
- `no_longer_observed` from `fixed`;
- `not_tested` and `test_failed` from `not_observed`;
- `persistent`, `changed`, and `reappeared`.

Only compare runs with equivalent scope, methodology version, parser version, controls, and coverage. A `403`, timeout, or missing artifact does not prove remediation.

## Fixed-Commit Semantic Code-Analysis Loop

For public OSS or acquired source, deterministic inventories are the first pass, not the conclusion:

1. Pin the exact commit/tag, lockfiles, generated assets, and supported runtime configuration.
2. Run an untouched local baseline with services bound to loopback.
3. Identify untrusted sources: remote request fields, file/archive members, IPC, queue messages, environment/config, dependency metadata, and lower-trust repository content.
4. Trace decoding, normalization, validation, authorization, sanitization, type conversion, persistence, and retrieval before the security-sensitive sink or decision.
5. Follow callers/references to the exact route, UI action, CLI, worker, import, build, or deployment entry point; preserve guards and branch conditions.
6. Validate the hypothesis through that supported path with owned canaries and a causal negative control.
7. Review Git history, security patches, tests, dependency changes, and sibling implementations for regressions and incomplete fixes.
8. Record each candidate as `source -> transforms -> sink -> entry point -> runtime effect`; downgrade paths whose framework model, sanitizer, reachability, actor, or version is wrong.

Treat SAST, taint/data-flow, call/control-flow graphs, dependency analysis, history, targeted runtime testing, and narrow local fuzz harnesses as complementary map generators. SAST/taint may over-approximate; dynamic testing covers only exercised paths; CFGs omit data semantics; fuzzers require language/runtime fit, a narrow harness, invariants, coverage, and crash triage. None is proof alone.

### Coverage and falsification closure

Maintain independently derived input/entry-point and sink ledgers, then reconcile them per production module. A module with zero inputs or zero sinks requires targeted review and an explicit disposition. Truncated searches, failed or omitted workers, missing partitions, and timeouts are `coverage_gap`, never `safe`.

Before reporting, flatten every candidate into a manifest and produce exactly one verdict per row. Re-open partitioned results against the full fixed-commit source because shared middleware and defenses may be outside a worker's file scope. Before any downgrade:

- enumerate all production callers of the sink and callers-of-callers where shared;
- enumerate all writers of any supposedly trusted property or store;
- give every co-parameter and distinct source-to-sink path its own disposition;
- verify context-matched defenses from source, authoritative documentation, a faithful local differential, or authorized deployment evidence;
- mark unavailable defense behavior `blocked/unknown` rather than presuming effective or ineffective.

Keep evidence levels distinct: unexecuted model trace or illustrative test = `static_candidate`; immutable code/config behavior = `source_fact`; exact supported path executed with a causal negative control = `runtime_validated`; authorized in-scope reproduction with actor and impact closed = `deployed_proof`. “Mentally executed,” scanner confidence, and LLM consensus are not runtime tool output. Zero findings is valid only when both ledgers and the verdict manifest close.

Do not upload private or in-scope source to hosted scanners, enable extension telemetry, or install mutable IDE plugins without an explicit disclosure/privacy and dependency decision. Prefer local, immutable tools. If a scanner is used, preserve its exact version/query/config and manually validate every promoted path.

When the scanner, agent, fixer, or benchmark repository is itself a learning source, load `argus-securityresearch-workflows` and its `references/external-security-tool-and-methodology-ingestion.md`. Keep the review static unless separately authorized; map executable/publishing side effects, distinguish benchmark scaffolding from retained efficacy metrics, and retain generated or mentally simulated tests as `static_candidate`.

For reusable promotion-gate checks covering OAuth state/account binding, agentic CI prompt injection, proxy/header forwarding, deterministic stub harnesses, and precise hold/kill language, read `references/semantic-candidate-promotion-gates.md`.

For browser-reachable source-to-sink candidates where installing or building the full product is unnecessary or disproportionate, read `references/source-integrated-browser-canaries.md`. It defines how to load exact pinned source under minimal inert shims, preserve the real parser and sink-owning method, dispatch a genuine CDP user gesture, test current main plus a released tag, and retain pre/post controls, screenshots, hashes, and prior-art disposition.

For incomplete file/path/URI validation fixes and loopback local-service file sinks, read `references/oss-incomplete-path-validation-local-service-proof.md`. It defines current-fix direct-vs-link differentials, exact source/harness hash identity, existing-versus-dangling symlink effects, separate lower-privileged local-account and modern-browser actor gates, pre-fix release exclusion, TOCTOU-aware remediation, conservative impact wording, and ledger-before-manifest finalization.

## Static OSS and CI/CD Review

For fixed-commit public repositories, additionally inventory:

- `.github/workflows/*.yml` and trigger types;
- checkout ref and attacker-controlled event fields;
- `pull_request_target` plus PR-head checkout paths;
- job and workflow token permissions;
- self-hosted runner reachability;
- mutable third-party Actions;
- cross-job caches, artifacts, workspace reuse, container volumes, and transferred dot-directories;
- whether PR-controlled code can persist hooks or configuration into `.git/` before a privileged Git command;
- manifests, lockfiles, `.npmrc`, `pip.conf`, Maven/Gradle registry config;
- release scripts, Dockerfiles, SBOMs, and generated artifacts.

Treat `.git/` as executable and credential-affecting state, not harmless commit transport. A fresh privileged checkout is not a clean boundary if an attacker-produced `.git/` cache is restored over it before `git push`, publish, release, or deployment commands. Manual maintainer dispatch is an exploitability downgrade, not an automatic kill, when the workflow is explicitly intended to execute PR code safely after dispatch.

For the complete review matrix, cache-key gates, local bare-repository canary, false-positive controls, and remediation boundary, read `references/ci-git-metadata-trust-crossings.md`.

When a CI crossing exposes a credential but live scopes are not safely observable, read `references/ci-credential-capability-proof.md`. It defines how to count every exact secret occurrence and alias, enumerate credential-bearing sinks plus mutable-code/artifact exposure boundaries, map exact repository/ref targets, separate documented configuration intent from live state, trace release/OIDC/other-token boundaries, model branch-triggered OIDC paths gate by gate, adjudicate contradictory parallel reviews, distinguish public metadata from fixed-source proof, kill unsupported package/protection/private-repository claims, and produce synchronized human plus machine-readable evidence.

When CI authorization is represented by a persistent label, approval, comment command, manually unblocked build, or environment flag, read `references/ci-head-bound-authorization-and-public-lifecycle-controls.md`. It defines exact pinned-executable provenance, temporal grant/dismiss/revoke modeling, no-race multi-object controls, exact sensitive-sink extraction, deterministic raw-to-derived public lifecycle evidence, integrated parser/loader/generator/runner canaries, same-plane agent/API/cache/state escalation, attacker-controlled cross-platform queue expansion, confirmed-versus-IAM-conditional credential claims, expected-untrusted-workload counterfactuals, trusted-versus-untrusted severity bounds, reviewer reconciliation, prior-report direct-source capture, root-cause-isolated duplicate differentials, two-way remediation counterfactuals, report-shape novelty gates, and head-SHA/diff-digest remediation.

Once a serious CI sink is established, read `references/ci-lower-precondition-trigger-breadth.md` before doing more post-compromise enumeration. It defines how to inventory every independent ordinary-code, project-pipeline, module/archive, generated-workspace, and reviewer trigger; compare prerequisite sets; prove exact gates and step generation locally; shift expected untrusted execution to the first unsafe isolation boundary; and lead with the easiest distinct route while preserving harder chains as corroboration.

When lower-trust CI host control may cross into source, trusted workers, release, signing, publication, or user-consumed artifacts, read `references/ci-trusted-plane-capability-gates.md`. It defines current-pin subtree comparison, fixed gate matrices, bounded public CI sampling, opaque registry-token handling, identity-context IAM proof, secret-safe non-mutating checks, local causal revalidation, and High-versus-Critical evidence boundaries.

Require a complete source-to-sink chain before claiming CI compromise or dependency confusion. A mutable Action tag, public workflow, unclaimed package name, or exposed SBOM is not a vulnerability by itself.

## Artifact Templates

- `templates/candidate-disposition.yaml`
- `templates/evidence-manifest.yaml`
- `templates/chain-edge.yaml`
- `templates/cross-run-delta.yaml`

Use them as schemas, not rigid report formats. Reports should still separate observed facts, demonstrated impact, supported inference, conditional impact, and explicit non-claims.

## Common Pitfalls

1. **HTTP 200 source-map false positive.** Require valid JSON, integer `version`, list `sources`, and `mappings` or `sourcesContent`; HTML/SPA fallback is negative.
2. **Regex result becomes a finding.** Public client identifiers, internal IPs, routes, source maps, schemas, and feature flags are leads until capability and impact are proven.
3. **Source-mentioned scope classification error.** Do not treat every referenced host as authorized, but do not treat every cloud-provider/SaaS hostname as out of scope either. Separate directly embedded production backends from analytics, imports, CDNs, identity providers, and unrelated third parties; document the attribution basis and any express exclusion.
4. **Secret leakage through tooling.** Store only candidate type, location, length, and digest by default; never print candidate values.
5. **Method-only mutation gating.** A `GET` can trigger logout, jobs, exports, presigned URLs, imports, or other state changes.
6. **OpenAPI exposure overclaim.** A public specification is usually inventory, not impact.
7. **Schema fuzzing drift.** Feed names recovered from exact source/spec/error context into a bounded plan; do not run generic table or field dictionaries automatically.
8. **Cross-run causality error.** Newly observed does not mean newly introduced, and disappearance does not mean fixed.
9. **Unsafe evidence proof.** Do not collect bulk data, real-user PII, live secrets, or destructive proof merely to satisfy a severity gate.
10. **Third-party code trust.** Do not copy repository agent instructions, install commands, or scanners into this skill.
11. **Bot-identity credential conflation.** Shared account names, commit authors, or public release activity do not prove two separately named secrets have equal scopes or reach; follow each binding independently.
12. **“Working as intended” composition error.** Git hooks, caches, OIDC, and dispatch can each work as documented while their composition defeats an explicit untrusted/trusted CI boundary. Treat maintainer dispatch as a prerequisite/downgrade, not an automatic accepted-behavior verdict.
13. **Runtime RPC guess.** A Resource Timing RPC ID with zero external-source matches stays unresolved. Do not assign a service path from UI wording, neighboring products, or similarity to another ID; preserve the zero-match provenance.
14. **Mixed-boolean verification bug.** Safety schemas often encode both negative retention flags and positive safety flags. Assert exact key/value semantics rather than `all(values())`, and read candidate schemas before checking non-action evidence.
15. **Pre-reauth positive-control error.** An owner component route returning HTTP 200 before a password/passkey challenge does not prove signing or download authorization. Require A->A and B->B to reach the post-reauth signer/archive-byte boundary before spending a foreign-selector probe; otherwise mark it `cross_account_probe_unspent` and inconclusive.
16. **Manifest-before-ledger drift.** Final candidate, matrix, approval, hunt, hypothesis, tested-item, next-step, and finding edits change governed hashes. Update ledgers first, rebuild manifests second, then run phase and full verifiers until every declared hash/byte count is green.
17. **Pre-fix runtime masquerading as mitigation bypass.** If a released binary accepts the direct input the current fix is meant to reject, it does not prove a bypass of that fix. Treat it as historical context and reproduce the direct-reject/link-accept differential against byte-identical current source or a build proven to contain the mitigation.
18. **Loopback-equals-same-user assumption.** TCP loopback is host-local, not necessarily principal-local. When another local process is in the actor model, use a distinct lower-privileged account, victim `0700/0600` controls, server/request principal evidence, and direct-access denial checks.
19. **Curl-Origin equals browser reachability.** A server accepting browser-shaped headers is not proof that current PNA/LNA policy delivers a public/opaque-origin request. Use a real browser and target-side state/hash evidence; kill only the browser branch when delivery is blocked.
20. **Single-prefix chunk-closure error.** An `assets/` regex can miss literal `import("./Chunk.js")`, preload-map, `new URL`, and CSS references. Compute the exact referenced-minus-acquired set across every observed literal form and iterate under a fixed manifest until it is empty before claiming graph exhaustion.
21. **TLS retry by disabling verification.** `curl: (60)` is a stop signal, not a reason to use `-k`. On an authorized retry, inspect the exact SNI chain, validate any AIA intermediate to system roots, verify the leaf hostname with a temporary augmented bundle, and retry only with verification preserved. If any binding fails, stop.
22. **Exact-host-only target dedup.** A zero-hit staging or QA hostname may duplicate an exhausted production sibling. Rank by conservative deployment cluster as well as exact host, preserve the sibling evidence, and require a differentiating signal before calling it a fresh class-level surface.
23. **Provider-domain hard-border error.** An AWS API Gateway, S3, CloudFront, Azure, GCP, or SaaS hostname directly embedded and used as an in-scope application's production backend can be functionally part of that application. Do not stop merely because the provider owns the parent DNS zone. Require tight source/runtime linkage—exact endpoint, product-specific routes, app tokens/audience, and ordinary workflow dependence—and check for an express exclusion. Keep authorization narrow: source-derived application operations only, never provider-wide discovery, neighboring resource IDs, account enumeration, or unrelated infrastructure. Preserve historical “not contacted” facts separately from the current scope interpretation.
24. **Browser fetch mislabeled as SSRF.** Frontend `fetch(user_url)` originates from the user's browser and remains subject to SOP/CORS. Require evidence of a backend-originated request from the server network position before promoting SSRF.
25. **AI registry content equals compromise.** Intended MCP/Skill/Markdown submission is not prompt-injection or supply-chain impact by itself. Require a review/ownership/control failure plus supported-path agent/tool consumption and a deterministic benign unauthorized effect.
26. **Failed Git command equals clean repository.** Empty status output is meaningless when `rev-parse` failed or the vault is not a worktree. Discover the top level first; otherwise report Git checks as not applicable and perform explicit filesystem hygiene instead.
27. **Private raw auth artifacts or derived URL inventories are safe merely because they are `0600`.** Cookie values and opaque login/vouch/OAuth redirect state remain capability material. Keep immutable raw captures private, but sanitize every ordinary derivative: HTML-decode before parsing, strip URL userinfo, replace all query values—not only suspiciously named ones—and redact fragments while preserving origin, path, parameter names, provenance, and a sanitized-artifact hash. If a derivative retained values, fix and test the parser, overwrite all affected derivatives, scan promoted artifacts, and rerun hygiene checks.
28. **Ledger verifier assumes one schema.** Request ledgers may wrap entries under `requests` and use `http_status`/`bytes` rather than `status_code`/`response_bytes`. Inspect types and keys before aggregation; a local `KeyError` is a verifier defect, not target evidence.
29. **Verification report is outside the verification boundary.** Writing the final hygiene artifact can introduce a bad mode or stale count. Rerun mode, secret, JSON, approval, process, and ledger checks after the last write.
30. **Extensionless JS is mislabeled as syntactically invalid.** `node --check 001.body` can reject the filename extension before parsing JavaScript. Feed retained bodies through `node --check -` on stdin; treat filename/loader errors as verifier defects, not target syntax failures.
31. **In-place redaction silently breaks ledger integrity.** When a captured bundle contains a client identifier, preserve original downloaded bytes/hash as provenance, add sanitized retained bytes/hash, and make validators use the correct pair. Scan and redact before printing context, including values assembled through `.concat(...)` or adjacent literals.
32. **Static package review silently becomes execution.** Registry metadata, archive inspection, and owned module execution are separate authorization phases. A request that says “without installation or execution” stops after verified in-place static review. If a later hypothesis needs runtime proof, write a new local-only plan first, execute the smallest exact module with network/dependencies mocked, retain a causal negative control, and describe that phase as dynamic—not static.
33. **Lexical package-path containment is treated as symlink containment.** `path.resolve()` and prefix checks reject `..` but do not constrain repository-controlled intermediate links. Search all wrappers for `lstat`/`realpath`/no-follow checks, then validate a real-directory negative against a one-variable symlink positive in a disposable fake home before promotion.
34. **Technical validity becomes automatic submission readiness.** A real local CLI CWE can still be HOLD when downloadable-client scope is ambiguous, victim interaction and checkout/path/slug prerequisites dominate, or only internal modules—not the installed entry point—were exercised. Preserve separate technical, impact, asset-eligibility, and submission verdicts; retain independent reviewer disagreement and let the strongest invalidity argument control.
35. **Dormant WordPress route becomes a synthesized probe.** A legacy theme bundle can retain `admin-ajax.php` actions whose required DOM container, data attributes, or nonce are absent from the live page. Verify live instantiation first; do not manufacture `type`/`filter`/`page` parameters from dead code.
36. **Reflection jumps directly to an executable payload.** Begin with an alphanumeric canary, classify exact contexts locally, and spend at most one non-executable encoded-delimiter control when an attribute boundary remains plausible. Safe entity encoding or preserved percent encoding closes the branch without script, event-handler, beacon, or browser execution.
37. **Search-result/sidebar advisory becomes affected-version proof.** A title fragment or nearby version table may belong to a different issue. Require the primary advisory, exact affected range, deployed feature prerequisite, and a safe/reportable proof path before target contact; mixed or weak RAG retrieval stays a held lead.
38. **Dismissed review is mistaken for revoked CI authorization.** A persistent label, unblocked-build state, comment command, or environment marker may survive `synchronize` even when GitHub dismisses the approval. Trace grant and revocation independently, bind the decision to the current head, and prove production ordering passively before assuming a later commit is blocked.
39. **Handwritten lifecycle summary outranks raw captures.** Never manually freeze mutable PR hashes, review IDs, timestamps, or status counts. Regenerate from the raw artifacts actually present, use capture-time `observed head` language, disclose missing metadata/files/headers, and scan the final package for superseded exact values.
40. **Intentionally untrusted worker is assumed to have no reusable authority.** Continue through host agent configuration, shared service identity, secret-manager call sites, API-client operations, queue tags, cache namespaces, durable state, and trusted-domain separation. A source-supported same-untrusted-plane control path can exceed one disposable VM without proving trusted/release compromise.
41. **Separate CI controls are mistaken for an integrated reproduction.** When review readiness depends on the full chain, join exact validation, loader, step generator, task selector, and runner in one local harness. Mock SaaS boundaries, allowlist at most one inert temporary canary, and say whether a real process spawned.
42. **A different exploit story is mistaken for a different vulnerability.** When a prior report reaches the same label/skip/command sink, capture its body verbatim and list the overlap before claiming novelty. Isolate the proposed root by taking a valid prior authorization as a precondition and excluding the old chain's grant, actor, self-approval, command, and merge requirements. Require two-way remediation independence and make title, opening, PoC, root cause, and remediation all center the changed authorization subject. If the narrative still leads with known RCE or a broad sink fix blocks both, retain high duplicate risk and use duplicate/no-go when the lifecycle delta cannot stand alone.
43. **Cross-platform breadth is called Critical without a trust crossing.** An attacker-controlled CI config may select Linux, ARM, macOS, and Windows queues and expose a reusable same-organization agent token. Record that breadth, but distinguish confirmed host/token paths from source-only Secret Manager call sites whose worker IAM is unproven. Run the intended-untrusted-job counterfactual, map organization/cluster/cache/artifact separation, and require source write, trusted-worker execution, executable cross-plane state, release, signing, or publication control before promoting beyond High.
44. **Requested registry scope is mistaken for granted writer authority.** An opaque bearer token returned after requesting `pull,push`, a live mutable manifest, authenticated pulls, `configure-docker`, broad OAuth scope, anonymous `401`, or upload-endpoint `OPTIONS` result does not prove the lower-trust worker can push. Compare current pinned subtrees, confirm the trusted consumer, and require authoritative IAM for the exact principal or an explicitly authorized non-mutating identity-context permission check. Bounded zero host/agent overlap is supporting separation evidence, not universal proof.
45. **Sink-depth tunnel vision hides the easiest exploit.** After proving a serious CI sink, do not keep enumerating post-compromise capabilities before inventorying every independent trigger that can reach it. Compare ordinary project pipelines, repository code/build files, module archives/overlays, generated workspaces, and reviewer/config paths by concrete prerequisites. If fork code is intentionally executed, report the first unsafe isolation or reusable-authority boundary—not expected CI execution—and lead with the lowest-precondition distinct route.
46. **Merge-closed lifecycle proof hides a stronger authorization sink.** A mixed-object harness is excellent for isolating marker persistence without racing auto-merge, but it can conceal that the same stale review makes `allApproved=true` when only the historically approved object remains. After the no-race lane, run a same-object lane through the exact bot approval/merge/publication logic plus a dismissal counterfactual. Audit base-ref `edited` events, alternate-base `synchronize` filtering, scheduled reviewer base queries, `review.commit_id` binding, and attacker-controlled author dates. Keep the result conditional until native branch-protection stale-dismissal behavior is known; public rulesets do not disclose legacy protection.
47. **Same-origin OIDC wildcard is called ATO without a code-exfiltration chain.** An accepted alternate path is only a client-registration boundary observation. Test cross-origin/confusion controls, callback canonicalization, fresh state/nonce, PKCE-S256 binding, and a concrete same-origin read/exfiltration primitive before promotion. Never follow an accepted external redirect.
48. **Generic inventory `value` fields are mistaken for leaked secrets.** Routes and object selectors may legitimately use `value`. Validate redaction within `findings.secret_candidates`: require `<REDACTED>` and reject plaintext-bearing `sample`, `literal`, `raw`, or equivalent fields. Inspect the extractor's real `--help`; unsupported provenance flags belong in an adjacent manifest, not an invented invocation.
49. **A cryptographic success result is attributed to every duplicate record.** Ordered claim collections may be normalized with first-wins, last-wins, or any-match semantics and later mark all records sharing a partial key verified. Define the protocol-valid full uniqueness key, test conflicting duplicates in both orders, assert verification on the exact value, and trace downstream policy selection separately. A genuine signed duplicate can otherwise launder an attacker-chosen policy value without forging the signature.
50. **Serial worker execution is mistaken for lifecycle isolation.** `concurrency=1`, clearing a global context in `finally`, or closing a plugin classloader does not stop user-created threads, child processes, timers, or parent-loaded static state from surviving into the next task. Inventory actual restart thresholds and cleanup ownership, prove whether the pool is shared across namespaces, and test a sequential attacker-task → clear → victim-task canary against the real authority-returning read. A patch that authenticates context writes is not proof that stale readers are task-bound.
51. **Malformed URL-like bundle text crashes or leaks through the inventory.** Minified JavaScript can contain strings that begin like URLs but have invalid bracketed hosts or ports. Treat `urlsplit()` and `.port` as untrusted parse operations: catch `ValueError` and emit only a deterministic malformed-URL marker containing length and hash prefix, never the raw candidate.
52. **HTTP 200 on a private Next.js route is called an auth bypass.** Parse `__NEXT_DATA__.page` and the return-path keys first. If the requested private route resolves to the sign-in page, retain it as an authentication-gate control; use the captured `_buildManifest.js` for exact route-chunk closure rather than claiming private page access or giving up on mapping.

## Verification Checklist

- [ ] Every input has source provenance and SHA-256.
- [ ] Parsing was local-only; no network-capable third-party script ran.
- [ ] Source-map candidates passed structured validation.
- [ ] Secret-like values are redacted and represented by digest metadata only.
- [ ] Exact routes retain file/line or spec operation provenance.
- [ ] Source-mentioned hosts are classified as explicit assets, directly embedded functional backends, or unrelated/context-only services; provider-domain naming alone is neither authorization nor a hard border.
- [ ] A functional-backend classification records exact endpoint provenance, product-specific route/workflow linkage, app token/audience linkage where observable, express exclusions, and a narrow source-derived request boundary; unrelated cloud/SaaS resources remain out of contact.
- [ ] Fresh-target ranking records both exact-host history and conservative deployment-cluster sibling history.
- [ ] Browser-side URL import is not labeled SSRF without proof of a backend-originated request.
- [ ] MCP/Skill/prompt-content candidates distinguish intended submission from review bypass, unauthorized distribution, and demonstrated agent/tool impact.
- [ ] Candidate states distinguish mapped, validated, reportable, disproved, and blocked.
- [ ] Any live replay has a separate scope/actor/owned-data/request-budget plan.
- [ ] Evidence was sanitized, post-scanned, hashed, and stored with restrictive permissions.
- [ ] Cross-run conclusions compare equivalent methodology and coverage.
- [ ] Every CI secret reference, alias, credential-bearing sink, target repository/ref, and separate release/OIDC credential was inventoried before impact promotion.
- [ ] After a serious CI sink was proven, every independent ordinary-code, project-pipeline, module/archive/overlay, generated-workspace, and reviewer/config trigger was compared by prerequisites before deeper post-compromise enumeration; the report leads with the easiest distinct route and frames expected untrusted execution at the first unsafe isolation boundary.
- [ ] Persistent CI authorization was tested across a head-changing transition: grant subject, current head, review dismissal, marker revocation, sensitive validation, and worker reachability were traced independently; any public lifecycle claim preserves timestamp ordering and label-origin limits.
- [ ] Base-ref transitions were included in the lifecycle model: `edited` handling, protected-base branch filters, pushes while targeting alternate bases, scheduled reviewer base selection, current `review.commit_id` binding, author/committer timestamp trust, and native legacy branch-protection dismissal were all resolved or recorded as explicit deployment gates.
- [ ] After any merge-closed mixed-object authorization proof, a same-object strongest-sink lane exercised exact bot approval/merge/publication logic and a dismissal/revocation counterfactual; ordinary intended untrusted execution was not promoted as a vulnerability without a separate isolation or reusable-authority boundary.
- [ ] Any decisive prior report was captured verbatim from its direct source and compared in a machine-readable differential that lists shared known mechanisms before the claimed root-cause delta.
- [ ] A distinct-root claim has an isolated control that excludes the prior chain's grant/actor/self-approval/command/merge prerequisites, a two-way remediation counterfactual, and consistent title/opening/PoC/root-cause/remediation framing; otherwise it is duplicate/no-go.
- [ ] Every passive lifecycle summary was regenerated deterministically from the raw artifacts actually present; observed-head wording, missing captures, exact IDs/timestamps/status counts, and superseded-value scans are recorded.
- [ ] When separate controls could leave a review gap, one safe integrated harness exercised exact validation, loader, step generator, task selection, and runner behavior and explicitly recorded whether a real inert local process spawned.
- [ ] Intentionally untrusted CI impact review covered reusable agent material, shared identities, secret/API client call sites, queues, external cache/state persistence, and explicit trusted/release separation before fixing the maximum boundary.
- [ ] Severity review traced attacker-controlled platform/queue/task fields through the exact step generator, distinguished confirmed worker credentials from IAM-conditional token paths, ran the intended-untrusted-job counterfactual, and required a proven trusted/source/release/publication bridge before claiming Critical.
- [ ] Any trusted-plane upgrade compared current workflow pins by subtree/content, tested a fixed organization/identity/cache/artifact/registry/source/publication gate matrix, treated public manifest and bounded host/agent samples only as sink/separation evidence, and required exact-principal IAM or a non-mutating identity-context capability check before claiming registry or trusted-secret authority.
- [ ] Credential claims distinguish source-confirmed operations, configuration intent, conditional paths, disproved paths, and unproven live state.
- [ ] Package publication, protection bypass, and private-repository claims passed an explicit adversarial claim-kill gate.
- [ ] Final evidence schemas were read rather than assumed, and hashes were generated only after the last report/ledger edit.
- [ ] For an incomplete-fix claim, the current mitigation's direct negative control fails closed while the single-variable bypass variant succeeds against byte-identical current source or a proven post-fix build.
- [ ] Local-service actor claims distinguish server principal, requester principal, direct filesystem access, loopback reachability, and browser delivery; a negative in one actor lane does not silently erase or prove another.
- [ ] Path-resolution remediation and tests address dangling/intermediate links and TOCTOU/no-follow behavior, not only lexical basename or one-time canonicalization.
- [ ] Bundled frontend closure records every observed literal reference form and proves `referenced - acquired` is empty; corrected extractor misses remain visible in the evidence trail.
- [ ] Any retry after certificate-chain failure preserves hostname and chain verification; AIA intermediates validate to system roots before entering a temporary CA bundle, and neither `-k` nor forced origin routing is used.
- [ ] Git hygiene begins with a successful worktree/top-level discovery; when no worktree exists, the report says Git checks are not applicable and records explicit filesystem checks instead.
- [ ] Ledger reconciliation reads the observed container and field names before normalizing request counts, status counts, and byte totals.
- [ ] Raw authentication-adjacent evidence is immutable, private, and restrictively permissioned; every promoted derivative has no unredacted cookie, Authorization, opaque redirect-state, query-value, userinfo, or fragment capability material. URL sanitization was applied after HTML decoding, raw-versus-sanitized hashes are distinct, focused parser tests passed, and the final hygiene artifact itself is included in a post-write mode/secret/JSON/process/approval verification pass.
- [ ] Next.js/webpack closure resolves every observed dynamic import ID through the captured runtime filename function—including alias/prefix maps—and proves the derived manifest is fully acquired.
- [ ] For auth-gated Next.js routes, evidence distinguishes the requested URL from `__NEXT_DATA__.page`; sign-in-shell 200 responses are classified as gates, and the captured build manifest's route-specific literal and alias-backed assets are reconciled without treating static source as authorization.
- [ ] Extensionless JavaScript evidence is syntax-checked through stdin rather than rejected by filename extension.
- [ ] Any in-place client-identifier redaction preserves original download bytes/hash separately from retained sanitized bytes/hash, and the full mission root passes a post-redaction signature scan.
- [ ] First-party package work records separate approvals and evidence for metadata, archive-only static review, and any later owned module execution; the final narrative does not call dynamic fixture execution “static.”
- [ ] Package archives pass published-hash and member-type/path/size/duplicate gates before extraction or trust, and package installation/lifecycle/dependency execution remains absent unless explicitly authorized.
- [ ] Filesystem-boundary candidates test lexical and canonical containment separately, search outer wrappers for symlink defenses, and retain a real-directory negative plus one-variable intermediate-symlink positive in a disposable fake home.
- [ ] Public-registry absence is not promoted to dependency confusion or namespace claimability, and generic API errors are not promoted without disclosure or boundary impact.
- [ ] Repository-delivery claims retain a normal-clone `120000`/`lstat`/`readlink` record, not only a source-worktree symlink or verbal assertion.
- [ ] Local CLI filesystem candidates include a plausible source-declared slug/workflow control in addition to synthetic sink proof when reportability depends on natural use.
- [ ] Technical validity, impact validity, asset eligibility, and submission readiness have separate verdicts; independent HOLD/Low review is not overwritten merely because the primitive reproduced.
- [ ] If installed-entrypoint proof is missing, either obtain explicit authorization for an isolated replay or preserve the gap and stop; never broaden a static-only request implicitly.
- [ ] Public WordPress legacy AJAX actions were replayed only when the live source-derived page instantiated their required container/data attributes/nonces; dormant code did not become guessed traffic.
- [ ] Reflected-input testing used the inert-canary → local-context → optional non-executable delimiter ladder, and stopped before executable payload/browser testing when encoding closed the boundary.
- [ ] CVE/technique applicability came from the exact primary advisory or equivalent high-confidence source, not a sidebar/search fragment; affected version, deployed prerequisite, safe proof path, and reportability were all established before contact.
- [ ] Cryptographic or attestation collection verification defines the protocol-valid full uniqueness key, rejects or canonically handles conflicting same-key duplicates, tests both duplicate orders with clean and forged-only controls, binds every per-entry verified state to the exact value used by the signature/proof, and traces downstream policy-selection semantics separately.
- [ ] Final request/byte/file totals were recalculated after closure documents and the verifier existed, then rechecked after the verifier's last write.
