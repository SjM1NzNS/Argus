# Source-first admin/CMS branches and misdirected hosts

Use this reference for exact-listed admin, CMS, portal, or framework-console targets where the initial surface is a stock SPA, authentication gate, redirect, or unrelated service.

## Bounded source-first sequence

1. Confirm the hostname is explicitly in scope and absent from the tested ledger.
2. Start with credential-free `GET /`, `/robots.txt`, and `/sitemap.xml`; do not follow redirects automatically.
3. Treat a same-host redirect target as one exact continuation, not permission to crawl sibling hosts or guess framework routes.
4. Parse literal scripts, styles, modulepreloads, manifests, and source maps locally. Recursively fetch only exact same-origin imports under a documented response-size, request-count, and pacing cap.
5. When a framework build declares hundreds of chunks, rank locally before increasing the request cap:
   - prioritize entry/index, auth, permissions, users, collections/items, files/assets, extensions, settings, and deployment-named chunks;
   - deprioritize locale packs, editor grammars, syntax highlighters, fonts, and recognizable stock libraries;
   - record intentionally skipped low-value exact references rather than pretending the graph was exhausted.
6. Render the already-approved SPA once when static code abstracts bootstrap endpoints. Inspect browser performance resources and console output to identify the application's own successful unauthenticated requests. Preserve only exact successful GET responses; do not replay failed refresh/logout/mutation calls merely because the browser attempted them.
7. Distinguish stock framework behavior from deployment evidence. Public branding, login metadata, framework route constructors, client-side permission fallbacks, bundled sinks, and version strings are leads—not findings—without target-specific data flow or server-side impact.
8. Use independent offline reviews for authentication/authorization, DOM/navigation sinks, and secrets/extensions/maps when the primary bundle is large or minified. Consolidate exact file:line evidence and downgrade generic library matches.
9. A final exact denial check such as anonymous `GET /users/me` is useful only when source-derived. Require `401/403` and absence of user/role data; route guessing and collection-name guessing remain out of bounds.

## TLS mismatch and unrelated-service handling

1. Do not disable certificate validation or force Host/IP routing to obtain content.
2. Record exact DNS resolution and inspect the certificate presented for the target SNI: subject, SANs, validity, issuer, and SHA-256 fingerprint.
3. A certificate and reverse/service identity belonging to an unrelated provider is an ownership/routing signal, not a takeover finding.
4. If useful, queue one plaintext HTTP root GET with redirects disabled. When the execution gate asks, wait for explicit approval; do not retry by another command or tool.
5. If the HTTP response redirects to an out-of-scope provider, preserve the Location and generic body, do not follow it, and classify the branch as `unreachable/misdirected` unless a real unclaimed-provider signature exists.
6. Do not turn unrelated service banners or versions into a target finding without ownership and scope proof.

## Evidence and ledger closure

- Preserve response headers/bodies separately and hash them.
- Record requests that failed before HTTP distinctly from HTTP status responses.
- Keep collector summaries honest when a later approved continuation adds requests.
- Update mission completion, source inventory, approval queue, tested items, hunt log, and checkpoint together.
- Validate JSON and helper scripts before finalizing.
- Final statuses should distinguish `completed-no-finding`, `completed-access-gated-negative`, and `completed-unreachable-misdirected`.

## Pitfalls

- Do not call stock framework endpoints deployment-specific merely because they exist in a minified bundle.
- Do not claim a source map from a `200` response until it parses with source-map keys.
- Do not blindly fetch hundreds of low-value locale/editor chunks to satisfy an artificial exhaustion metric.
- Do not report client-side permission fallback without demonstrating the protected server operation succeeds.
- Do not treat public login branding UUIDs as unauthorized file enumeration.
- Do not let an asynchronous worker completion stand in for the user's answer to an approval prompt; approval must be explicit.
