# WordPress Source-First Fixed-Point and REST Contract Validation

Use this pattern for authorized, low-noise review of WordPress/Elementor/Crocoblock-style public frontends where scripts, inline settings, AJAX actions, REST routes, and plugin-version leads coexist.

## 1. Build the executable graph to a real fixed point

Do not define the graph as `<script src>` tags only.

1. Hash-bind the canonical HTML before extraction.
2. Freeze exact same-origin script-tag URLs and fetch them sequentially with redirects disabled and per-response/mission caps.
3. Parse loaded webpack/runtime maps for exact emitted chunk filenames; freeze those references before a second pass.
4. Parse **all inline configuration objects and whole-HTML URL literals** for executable URLs such as mobile/menu runtimes that are configured but not loaded in the current viewport.
5. Subtract every already fetched URL and inspect each apparent gap in source context before contact.
6. Stop only when the corrected subtraction yields zero unfetched same-origin executable.

### Literal false-positive reduction

Reject a candidate when `.js` is only a prefix inside a longer non-script token, for example:

- `default.json` truncated to `default.js`;
- `.jquery.plugin.min.js` truncated at the internal `.js` substring;
- a tail such as `/sdk.js` concatenated onto a proven external base URL and locale.

Document the source context and why no request is justified. Do not “confirm” parser artifacts with network traffic.

## 2. Verify every acquisition phase before expansion

For each frozen pass:

- compile/read back the runner before execution;
- require exact planned/executed request counts;
- retain byte count, status, SHA-256, truncation, sanitized headers, and body path per request;
- syntax-check every retained JavaScript file in a JavaScript context rather than relying on a misleading retained extension;
- distinguish an unavailable third-party source map from a missing application executable;
- rerun local closure after every new source file.

A `200` source-map URL is not proof of a source map; require valid JSON plus source-map keys. A `404` exact third-party map does not break application executable closure.

## 3. Redact inline configuration before contextual inspection

Raw evidence may remain private, but derived analysis must be metadata-first.

- Redact sensitive-key values regardless of type: strings, numbers, nested mappings, arrays, IDs, nonces, tokens, client identifiers, and keys.
- For a sensitive nested mapping, preserve only type and key names when useful.
- For URLs, preserve scheme/origin/path and query-key names, not query values.
- Preserve public booleans/enums/action names only when needed for trust-boundary reasoning.
- Represent values by type, length, and hash prefix when provenance is needed.
- Never let public-browser identifiers drift into notes merely because they are not server credentials.

## 4. Use the REST index as a contract map, not authorization evidence

When the frontend exactly advertises `/wp-json/`, one passive credential-free index GET can replace endpoint guessing.

Reduce the retained index locally to:

- namespaces and route patterns;
- methods;
- argument **names**, required flags, and types;
- custom/plugin namespaces;
- mutating contracts;
- CVE prerequisite markers.

Do not preserve argument defaults or response values unless required and non-sensitive. Registered `POST`, `DELETE`, admin, MCP, plugin-manager, or CRUD routes do **not** prove anonymous access because the index does not expose the runtime result of `permission_callback`.

Choose the smallest representative safe control:

- prefer a parameterless read-only administrative/schema GET;
- a `401/403` closes that callback without object access;
- a `200` is still only metadata exposure until sensitivity or dangerous capability is proven;
- do not execute MCP tools, submit forms, invoke writes, or use invalid destructive methods merely to test registration;
- decline read-only endpoints that may return user-entered searches, suggestions, or customer data when impact is weak.

## 5. Gate WordPress/plugin CVEs on three independent proofs

A version string alone is a lead. Require:

1. **Affected version:** exact target version is within the authoritative affected range.
2. **Feature prerequisite:** the vulnerable module/feature is enabled and reachable, such as CCT REST search or Listing Grid Load More.
3. **Exact sink:** source/index evidence shows the vulnerable action, route, or parameter on this deployment.

Examples of prerequisite markers to classify locally include `_cct_search`, `filtered_query`, `listing_load_more`, and CCT route namespaces. If the feature/sink is absent, reject the lead without sending SQL syntax or exploit payloads. If RAG returns a different CVE than queried, discard the unsupported identifier and re-query the supported advisory; never blend identifiers.

## 6. Separate browser co-occurrence from data flow

Minified Elementor/vendor code frequently contains both browser-controlled sources and sensitive sinks.

- Co-occurrence is triage only.
- Trace the application-specific source through transformations into the sink.
- If custom code escapes every server-returned field before `innerHTML`, record the escaping chain and close DOM XSS for that path.
- Generic vendor `innerHTML`, URL, storage, and message markers do not establish a target-specific exploit.

## 7. Reconcile request accounting precisely

Keep phase counts separate from whole-mission counts. Include every request status—not only `200` bodies—in final hash and byte accounting:

- canonical redirects;
- successful assets;
- denied `401/403` controls;
- unavailable `404` maps.

Before closure, run one reproducible verifier that checks:

- planned/executed totals and status histogram;
- body byte counts and SHA-256 for every retained response;
- JavaScript syntax count;
- JSON parse count;
- zero executable gaps;
- zero secret candidates in derived analyses;
- zero CVE prerequisite markers claimed absent;
- expected anonymous-denial statuses;
- restrictive mission permissions.

Then synchronize approval queue, hypothesis ledger, tested items, hunt log, surface map, checkpoint, and next steps. Search for stale `pending/approved` entries and stale fallback targets before declaring completion.

## Reportability boundary

Close the branch as no-finding when the complete source graph is at fixed point, serious version/feature/sink hypotheses are rejected, representative administrative reads fail closed, and no authenticated/owned-object or stateful workflow exists. Reopen only for materially new source, target-version-proven advisories with their feature prerequisite present, or an authorized owned-object workflow.
