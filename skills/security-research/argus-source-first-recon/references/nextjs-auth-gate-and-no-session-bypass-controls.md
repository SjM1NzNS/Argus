# Next.js Auth-Gate and No-Session Bypass Controls

Use this reference when an authorized Next.js application serves private account routes, SSR shells, `_next/data` endpoints, or target-owned account APIs and the question is whether protected data is reachable with **no authenticated session**.

This is a bounded validation method, not authorization to brute-force credentials, fabricate tokens, spray bypass headers, or test identity-provider infrastructure.

## Core invariant

An authentication bypass exists only when a protected operation succeeds without valid credentials and crosses a confidentiality, integrity, or privilege boundary.

Do not promote any of the following alone:

- HTTP `200` containing the sign-in page;
- a redirect to login;
- a generic localized `500` page;
- public configuration or route metadata;
- client bundle strings that mention profile fields;
- a public verification-status response without a meaningful owned-vs-random differential.

## Preconditions

Record before target contact:

1. exact in-scope application and directly embedded target-owned backends;
2. owned account marker and prohibited third-party identities;
3. acquired Next.js build ID, asset prefix, routes, and exact framework version;
4. normal private-route baseline;
5. request count, minimum interval, redirect policy, response-size cap, and stop condition;
6. explicit prohibition on cookies, `Authorization`, passwords, OTP/email codes, and state-changing methods for the no-session lane.

Identity-provider infrastructure remains separate unless explicitly in scope. A custom Clerk/Auth0/Keycloak frontend does not authorize provider-wide testing.

## Source-derived request matrix

Use only paths justified by captured source/runtime artifacts:

1. **Normal private page** — request without credentials and parse `__NEXT_DATA__.page` plus return-path fields.
2. **Standard Pages Router data path** — derive `/_next/data/<buildId>/<private-route>.json` from the captured build ID and exact route.
3. **Asset-prefix data path** — try once only when the captured deployment architecture plausibly serves data under the prefix. A generic error closes that path family unless source shows different routing.
4. **Direct data-mode request** — request the private page with `x-nextjs-data: 1`, no cookie, and no bearer token.
5. **Exact target-owned backend reads** — replay only source-derived read-only operations that represent private account data.
6. **Random/catch-all control** — only when needed to distinguish a real route from middleware applied before routing.

Do not expand from these controls into path normalization fuzzing, arbitrary proxy headers, token mutations, or method confusion without a separate source/CVE prerequisite and approval plan.

## Redirect handling

Disable redirect following for the bypass lane. Preserve:

- original status;
- sanitized `Location` or framework redirect header;
- empty-versus-nonempty body;
- response digest;
- whether the destination is the expected sign-in route.

A followed redirect that ends at HTTP `200` can erase the actual authentication decision.

## Response classification

### Expected denial

- `401` or `403` from a private backend;
- `302`, `303`, `307`, or `308` to sign-in;
- Next data response whose page/redirect metadata resolves to sign-in;
- `404` where the exact deployment does not expose that data-path form.

### Generic error, not bypass

For a `500` response:

1. parse `__NEXT_DATA__` if present;
2. inventory only `props.pageProps`, page identity, error status, stack/trace presence, and owned markers;
3. check for account-specific data or secrets;
4. stop repeating equivalent malformed-path variants.

A generic error page with public navigation/contact/localization props is not private access and normally has no reportable impact.

### Candidate bypass

Stop immediately when a no-session response returns protected account data, a protected state transition, or a session/privilege artifact. Preserve the smallest response necessary, verify it is the owned account, and add a negative/random control before any reportability claim.

## Avoid full-document marker false positives

Next.js HTML commonly embeds application bundles containing strings such as `firstName`, `emailAddress`, `unsafeMetadata`, or `exposes`. Scanning the entire HTML for these words falsely labels a public sign-in/error shell as private data.

Instead:

- parse the `__NEXT_DATA__` JSON;
- inspect only page identity and `props.pageProps` for private markers;
- separately scan for the exact owned canary or account identifier;
- treat client bundle vocabulary as static source, not returned user data.

If a detector trips on full-document bundle strings, fix the detector and rerun classification locally before spending another request.

## CVE and bypass-header gate

Before sending a known framework bypass payload:

1. retrieve the primary advisory or equivalent high-confidence source;
2. establish exact affected and fixed versions;
3. prove the deployed version and required middleware architecture from captured artifacts;
4. confirm the payload is safe and reportable for the program;
5. do not spray a version-inapplicable payload merely to confirm a published patch.

Example: CVE-2025-29927 is fixed for Next.js 15.x from `15.2.3`. A deployment proven to run a later 15.x version should be marked version-inapplicable unless separate evidence shows a regression.

Primary advisory: https://github.com/vercel/next.js/security/advisories/GHSA-f82v-jwr5-mffw

For May 2026 Next.js middleware/proxy bypasses, also version-gate:

- GHSA-267c-6grr-h53f / CVE-2026-44575 — 15.x fixed at `15.5.16`;
- GHSA-26hh-7cqf-hhc6 / CVE-2026-45109 incomplete-fix follow-up — 15.x fixed at `15.5.18`;
- GHSA-36qx-fr4f-26g5 / CVE-2026-44573 — 15.x fixed at `15.5.16`;
- GHSA-492v-c6pp-mqqv / CVE-2026-44574 — 15.x fixed at `15.5.16`.

Use the primary Vercel release note and advisory records, not a search-result version fragment: https://vercel.com/changelog/next-js-may-2026-security-release

## Expanded known-family matrix

When the user explicitly requests broader known-method coverage after the minimal matrix fails, do not claim literal exhaustiveness and do not switch to blind fuzzing. Write a second, fixed-budget plan over the same exact private route/backend and cover only safe one-variable families:

1. **Path normalization:** trailing/duplicate slash, encoded dot segment, semicolon parameter, one encoded route character, and case variation.
2. **Alternate first-party channel:** only exact in-scope sibling/apex hosts already proven by source or ordinary routing.
3. **Trusted path headers:** `X-Original-URL` and `X-Rewrite-URL`, first as a bundled control and then individually if the bundle is denied. Test both protected-actual/public-header and public-actual/protected-header directions.
4. **Owned identity/proxy headers:** use only the controlled account alias; bundle common upstream identity headers once, then isolate individually after denial so one blocked header cannot mask another. A backend `401` remains a negative control.
5. **Client-state fields:** bounded `isVerified`/`authenticated` plus the owned alias on the exact protected route. Never treat client flags as proof unless the backend returns protected data.
6. **Session parsing:** empty, literal-null, and duplicate-conflicting session cookies.
7. **JWT verification:** one unsigned `alg:none` session-shaped token and one bearer token containing only a synthetic subject plus the owned alias; also bounded null/undefined/malformed bearer controls.

Generate credential-shaped values in memory. Persist only the mutation class and digest, never the raw cookie/JWT/header value. Stop the token-parser family on any `5xx` to avoid turning a malformed-token check into repeated per-request denial of service.

### Adaptive mutation rule

Mutation is justified only when it isolates a plausible ambiguity from a prior control. Examples:

- bundled path headers returned `403` → retry each header separately;
- bundled identity headers returned `401` → isolate each identity header;
- one asset-prefixed data path returned a generic `500` → do **not** repeat the equivalent path family;
- unsigned JWT returned `401` → do not escalate to secret brute force, `kid` injection, or `jku`/`x5u` SSRF without separate source prerequisites and authorization.

Record the adaptive reason in the manifest. If every expanded request is redirect/`401`/`403`/`404`/normalization and no `2xx` occurs, close the no-session branch pending new source evidence or a newly applicable advisory.

## Explicit exclusions for the no-session lane

Do not reinterpret “all known methods” as permission for:

- password spraying, credential stuffing, OTP/recovery abuse, token guessing, or signing-secret brute force;
- JWT key-URL SSRF, `kid` file/SQL injection, or identity-provider-wide testing;
- HTTP request smuggling/desynchronization, cache poisoning, or cross-user cache experiments;
- state-changing method overrides, notification workflows, or destructive object actions;
- session fixation or authenticated-cache testing without a legitimate owned session baseline.

These require a different actor/evidence envelope and can affect third parties or shared infrastructure.

## Evidence schema

For each request retain a sanitized record containing:

```json
{
  "id": "AUTH-N1",
  "source_provenance": "captured build manifest or exact client call",
  "request": {
    "method": "GET",
    "url": "query values redacted",
    "cookies": false,
    "authorization": false,
    "headers": ["header names only"]
  },
  "response": {
    "status": 307,
    "location": "sanitized sign-in path",
    "bytes": 0,
    "sha256": "...",
    "next_page": null,
    "page_prop_keys": [],
    "owned_marker_present": false,
    "unexpected_private_response": false
  }
}
```

Raw bodies remain private and immutable. Sanitized manifests must not retain email addresses, cookies, tokens, redirect capabilities, or query values.

## Evidence-validator integrity

Do not hardcode guessed metadata keys such as `ACCOUNT_A_EMAIL`. Inspect the private account-metadata schema first and read the keys actually present (for example, `PRIMARY_ACCOUNT` / `SECONDARY_ACCOUNT`). A leak scan over an empty alias list is a verifier failure, not a passing hygiene result.

For every final evidence pass:

1. assert at least one owned alias was loaded without printing it;
2. scan successful responses separately from non-2xx reflection/error bodies;
3. scan notes, manifests, and scripts for exact aliases and raw JWT-shaped values;
4. validate every JSON manifest and script after the last edit;
5. verify file/directory modes after the last report write;
6. recompute request/status totals from the actual manifests.

If a broad detector initially marks a generic error page private, preserve the original observation and add an explicit adversarial reclassification containing the focused `__NEXT_DATA__` page/prop result. Final aggregators must honor that reclassification rather than silently counting the stale scanner flag.

## Completion gate

Close the unauthenticated branch when:

- normal and alternate source-derived page/data paths redirect or deny;
- exact private backend reads deny;
- no owned marker or private account props appear;
- applicable primary-advisory CVE gates are resolved;
- generic error paths are classified without repetition;
- evidence and dispositions record both positive observations and non-findings.

Then pivot to the highest-yield authenticated authorization matrix rather than inventing more unauthenticated payloads. For two-owned-account BAC, require owner-positive A→A and B→B controls before one reversible A→B selector probe.
