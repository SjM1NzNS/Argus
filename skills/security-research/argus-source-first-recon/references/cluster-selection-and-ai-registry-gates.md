# Cluster-aware target selection and AI registry gates

Use this reference when an exact-scope Web/SPAs hunt must choose the next untouched surface or when source reveals an MCP, agent Skill, prompt-content, or AI capability registry.

## 1. Select by deployment cluster, not exact hostname alone

A hostname with zero exact historical hits may still duplicate an exhausted sibling. Before ranking:

1. Load the current official exact scope and verify its provenance/hash.
2. Build local history from tested items, hypotheses, hunt logs, mission names, and source-derived host inventories.
3. Normalize candidates into deployment clusters using conservative lexical and source evidence:
   - strip only well-understood environment labels such as `dev`, `d`, `qa`, `q`, `stage`, `staging`, `prod`, or `production`;
   - preserve the registrable domain and application stem;
   - do not merge merely similar product names without source or routing evidence.
4. Mark a candidate `exact_untouched` and separately mark its cluster `cluster_touched`, `cluster_blocked`, or `cluster_exhausted`.
5. Rank distinct production clusters ahead of staging/dev siblings unless the lower environment is independently exact-listed and materially different.
6. Penalize known corporate-auth gateways, dead deployment siblings, and already mapped API families.
7. Preserve the ranking inputs, score/reasons, and excluded siblings in a selection artifact.

### Heuristic safeguards

Treat environment and gateway detection as token-aware, not substring-naive:

- inspect dot- and hyphen-delimited labels, including compact suffixes such as `-d`, `-q`, `-s`, and names such as `design` that commonly mark non-production variants;
- apply a strong independent penalty to `login`/`auth` roots and known GitHub Pages, Akamai/Entra, BigIP, or other corporate-auth boundaries even when the hostname lacks a dev/stage label;
- do not let attractive keywords such as `admin`, `dbt`, `proof`, or `partner` cancel a known-auth-gateway penalty;
- treat email-service subdomains such as `em<digits>.<root>` as context-only siblings unless routing/source shows an independent application;
- after every thin cut, add the exact and cluster result to history and rerun the scorer rather than continuing down a stale ranking;
- manually review the top few scored candidates before contact and document any override with a deterministic reason.

A prior production sibling does not prove staging is identical, but it defeats the claim that staging is a fresh class-level surface. Require a differentiating signal before spending requests.

## 2. Cut thin branches and continue locally

For each selected production root, use a separate bounded plan: one credential-free root GET, redirects disabled, no cookies/body/auth/path guessing, then local literal-reference extraction.

Cut immediately when the root yields only:

- a known corporate authentication gateway with no source;
- an S3 `NoSuchKey` deployment response with no bucket/object capability;
- an unreachable endpoint before HTTP;
- a generic dynamic-link boundary requiring a guessed path.

Record the negative, close the approval row, synchronize the tested/hypothesis/hunt ledgers, and rerun cluster-aware selection. Do not turn a thin negative into path guessing.

## 3. Classify every source-declared cloud/provider origin

A same-product SPA may declare an API or storage resource on AWS, Azure, GCP, a CDN, or another provider-owned DNS zone. Source provenance is attribution evidence, not blanket authorization—but provider-domain naming is not a hard scope border either.

Classify the exact endpoint before contact:

### A. Explicit asset

The exact host or a governing wildcard/application clause is listed. Apply the ordinary per-action plan.

### B. Directly embedded functional application backend

Treat the endpoint as part of the in-scope application unless the program expressly excludes it when several strong bindings hold:

- the in-scope production client embeds the exact endpoint as its production API/storage origin;
- routes and response models are specific to the scoped product rather than a generic third-party service;
- the application sends its own session/OIDC bearer token or a product-specific audience/scope to it;
- ordinary application workflows depend on it;
- there is no signal that the proposed request would target another customer, provider control plane, or unrelated tenant.

This is the same attribution model used for an application-linked S3 bucket or API Gateway deployment. The cloud provider owns the parent DNS zone; the tenant application owns or controls the deployed resource and business impact.

Operational boundary for class B:

- use only exact source-derived product routes and ordinary app semantics;
- keep owned-account/object, rate, redirect, and state-change gates;
- do not enumerate neighboring API IDs, buckets, accounts, regions, tenants, provider metadata, internal networks, or unrelated cloud resources;
- preserve the evidence that established functional linkage;
- treat explicit program exclusions as controlling.

Do not require separate scope confirmation solely because the endpoint ends in `amazonaws.com`, `azure.com`, `googleapis.com`, a CDN zone, or another provider namespace. Clarify only when ownership, tenant linkage, or an express exclusion is genuinely ambiguous.

### C. Context-only third party or unrelated provider surface

Analytics, generic identity providers, imported content, payment processors, public CDNs, SaaS APIs, and other references that lack the direct product-backend bindings above remain context-only unless independently scoped. Do not let the browser contact them merely to render a page when static analysis suffices.

Keep historical execution facts separate from interpretation: “not contacted during mission X” can remain true even if later review classifies the endpoint as a functional backend eligible for a new bounded plan.

## 4. AI/MCP/Skill registry trust-boundary map

When source reveals contributor, reviewer, catalog, CLI, or agent-content workflows, inventory four independent boundaries:

### Authorization

- contributor versus ordinary reader versus reviewer/admin;
- owned versus foreign submissions and published objects;
- read-content, edit, remove, approve, reject, and transition operations;
- frontend navigation/group checks versus backend enforcement.

Client-side role gating is a lead, never proof. BFLA/BOLA requires controlled roles, owned objects, positive controls, and a stable backend differential.

### Validation

Record client-side extension, path, count, size, schema, and normalization controls. A report requires evidence that the backend accepts a safely mutated violation and that the mismatch causes concrete impact. Client validation alone is not a vulnerability.

### Agent supply chain and stored prompt content

The intended ability to submit Markdown, MCP metadata, prompts, or tools is not itself a finding. Promotion requires a controlled chain such as:

1. attacker-controlled content crosses a review or ownership boundary;
2. the content becomes approved/trusted or reaches a victim/runtime unexpectedly;
3. an agent/tool consumes it through the supported path;
4. a benign canary demonstrates a deterministic unauthorized effect;
5. warnings, required non-default actions, and reviewer controls are included in reportability analysis.

Do not claim command execution, exfiltration, or prompt injection from source strings alone.

### Rendering and import

- Distinguish application raw-HTML sinks from library-internal entity decoding.
- Browser `fetch(user_url)` is not SSRF: the request originates from the user's browser and response visibility is governed by SOP/CORS.
- SSRF requires proof that a backend fetches the attacker-controlled URL from the server's network position.
- A browser importer may still justify separate CORS, CSRF, or internal-network analysis, but only with a real victim/request-delivery model and demonstrated data/action impact.

## 5. Public SPA metadata false-positive gates

Treat these as expected unless paired with a capability:

- OIDC tenant, authority, public client ID, redirect URI, and requested scopes;
- API route names and predictable IDs/slugs;
- group or role display names;
- preview/fallback catalog records;
- CLI commands and public repository URLs.

Fallback mutations that only update local UI state are not server-side impact.

## 6. Required evidence package

Preserve:

- exact scope proof and cluster-dedup selection artifact;
- root/static request budgets and ledgers;
- full fixed-point JS graph with `referenced - acquired = empty`;
- route, operation, actor, object, and state-transition map;
- cloud/provider origin classification with exact functional-linkage evidence, express exclusions, and the unrelated/context-only hosts that remained out of contact;
- client/server validation distinctions;
- confirmed facts, blocked hypotheses, false positives, and explicit non-claims;
- synchronized approval, tested-item, hypothesis, hunt-log, checkpoint, and next-step records.

Completion should state whether the branch is `exhausted`, `blocked`, `disproved`, or `reportable`; do not collapse those states.
