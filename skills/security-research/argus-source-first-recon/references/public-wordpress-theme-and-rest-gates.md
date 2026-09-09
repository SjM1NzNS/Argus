# Public WordPress Theme and REST Gates

Use this reference for an authorized public WordPress/custom-theme surface when the root HTML exposes exact first-party scripts, REST metadata, archive/search routes, or a first-party tag-manager proxy. It is a class-level workflow; retain target-specific URLs, hashes, versions, and approval IDs only in the mission evidence.

## 1. Establish provenance without version overclaim

- Record apex-to-canonical handoffs as separate, redirect-disabled requests when both hosts are in scope.
- Treat `?ver=` asset values as **version hints**, not definitive core/plugin fingerprints. Corroborate with another target-owned signal before claiming the deployed version.
- Classify every referenced host as exact asset, directly embedded application backend, first-party analytics proxy, or third-party context-only destination.

## 2. Reach executable fixed point

1. Hash-bind canonical HTML.
2. Acquire only exact same-origin executable references declared by retained source.
3. Syntax-check JavaScript and inventory nested executable URLs, routes, source maps, object selectors, secrets, and stateful methods locally.
4. If canonical HTML declares a first-party GTM/proxy script on another exact asset, fetch only the literal script URLs. Analyze locally; do not contact Google Ads, Analytics, YouTube, GitHub, or other runtime destinations merely because the container mentions them.
5. Stop when `referenced first-party executable - acquired = empty`.

A first-party analytics proxy is not automatically an application backend. Promote it only when it exposes target-specific routes, capabilities, secrets, or sensitive dataflows.

## 3. Gate legacy AJAX code on live instantiation

Theme bundles often retain dormant handlers such as `admin-ajax.php?action=...`.

Before any request:

- identify the exact DOM selector/data attributes/nonces required by the handler;
- fetch only a literal public page that source says instantiates the component;
- verify those prerequisites exist in the live HTML;
- classify whether the action is public pagination/content rendering or a privileged boundary.

If the live page lacks the required container/data attributes, record the code as dormant or unreachable and do not synthesize parameters. A route string plus field names is not reachability.

## 4. Use the REST index as a contract inventory, not a finding

For a source-derived `/wp-json/` index:

- inventory namespaces, methods, required arguments, permission-bearing descriptions, and custom/plugin versus core ownership;
- do not automatically replay every route;
- prioritize exact parameterless read contracts whose unauthorized success would disclose sensitive administrative metadata;
- use one or two representative anonymous controls, then stop when explicit capability errors establish the boundary.

Core-only namespaces and public post reads are expected behavior. Public route schemas are mapping evidence, not unauthorized data access.

## 5. Reflected-XSS context probe ladder

When exact application source constructs `/search/` plus `encodeURIComponent(term)`:

1. Send an alphanumeric inert canary only.
2. Count reflections and inspect exact surrounding bytes locally.
3. If and only if a quoted attribute boundary remains plausible, send one non-executable encoded delimiter canary such as `%22` embedded between alphanumeric text.
4. Classify each context: HTML text/title, URL, quoted attribute, script, style, or JSON.
5. Stop if HTML contexts render `&quot;` and URL contexts preserve `%22`; no payload or browser execution is justified.

Never begin with markup, an event handler, script, scheme, external beacon, or victim interaction. Reflection alone is not XSS. Promote only after a demonstrated executable context, attacker delivery model, CSP/browser assessment, and victim impact.

## 6. Separate author-trust content from public attacker input

`x-html` or `innerHTML` rendering of WordPress post titles/excerpts is not a public XSS finding by itself. Establish:

- who can author or modify the stored value;
- WordPress capability and sanitization behavior for that role;
- a lower-trust-to-higher-trust victim crossing;
- an owned publication/rendering control.

Without a low-privilege content source or authorization defect, retain it as an authenticated workflow hypothesis, not a public exploit.

## 7. Advisory and external-RAG gate

For a CVE/technique lead:

- retrieve the primary advisory or a high-confidence source for the exact issue;
- distinguish an exact advisory body from a sidebar/title/search-result fragment;
- require affected-version range plus the deployed feature prerequisite;
- treat mixed results from older similarly named CVEs as ambiguous;
- do not turn weak retrieval into a live probe.

For callbacks, XML-RPC pingbacks, imports, or other requests that may create moderation/state artifacts, require a separate owned-callback/state-change plan and reportability gate. Known standard-product behavior or poor bounty precedent can justify stopping before live contact.

## 8. Closure and accounting order

Use this order:

1. Write source graph, trust-boundary map, candidate matrix, completion record, and target ledgers.
2. Recalculate request/status/byte totals from observed ledger schemas.
3. Recalculate the mission file count **after** closure documents and the verifier itself exist.
4. Update accounting and narrative counts.
5. Run final JSON/hash/mode/approval/ledger-marker/Markdown-table verification.
6. If the verifier writes or changes a file, confirm the count remains stable and rerun once.

Do not cite a pre-closure file count. A correct network ledger can still produce a stale final narrative when report and verifier files are added afterward.

## Suggested disposition matrix

At minimum include:

- anonymous administrative REST reads;
- reflected search context;
- stored/DOM rendering with actor model;
- legacy AJAX reachability;
- custom/plugin REST namespaces;
- JavaScript/GTM secrets or backend routes;
- each version-correlated advisory;
- generic outdated-version/header observations;
- callback/stateful leads rejected before contact.

For every row preserve source, smallest control, observed result, and reportability disposition.
