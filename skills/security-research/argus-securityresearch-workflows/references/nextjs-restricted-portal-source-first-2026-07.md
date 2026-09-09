# Next.js restricted-portal source-first pattern — 2026-07

Use this reference when an exact-listed portal returns redirects/login gating but saved HTML or framework error pages expose a public Next.js source graph.

## Durable collection pattern

1. Baseline `/`, `/robots.txt`, and `/sitemap.xml` without following redirects.
2. Treat status and body semantics separately. A substantial `404` HTML response can be a fully rendered Next.js error shell with valid exact `<script>` and stylesheet references; do not discard it merely because the status is non-200.
3. Follow only an explicit same-host redirect destination such as `/login?callbackUrl=%2F`, without following any later IdP redirect.
4. Merge literal same-origin assets from the login shell and framework error shell.
5. Fetch `/_next/static/.../_buildManifest.js`, parse its literal `static/chunks/...js` entries, and make a second exact-reference pass over declared page/shared chunks. HTML-only collection misses these lazy routes.
6. Inventory `__NEXT_DATA__`, build ID, sorted pages, auth providers, API paths, object selectors, upload/download flows, source-map references, secrets, internal hosts, and dangerous DOM/navigation sinks locally.
7. For a callback/open-redirect lead, locate the exact helper module and inspect its allow/deny logic before live payload testing. A helper that accepts only single-leading-slash relative paths and rejects `//` and `/\\` should downgrade the lead without traffic.
8. A source-declared `POST` is not automatically mutating. For search/query endpoints, use one minimal read-only request only when the exact endpoint, method, index/request shape, and low result cap are source-derived and the scope plan allows it. Send no Cookie/Authorization, do not follow redirects, and stop immediately on records.
9. Evidence gate for an anonymous content-read candidate:
   - restricted/login-gated portal context;
   - exact source-derived request shape;
   - anonymous response contains actual non-public records, not merely `200` or public static content;
   - response preserved with hashes and no bulk collection;
   - repeat/control only if needed to distinguish cache/public-content behavior.
10. If the read-only request redirects to login and returns no records, close the unauthenticated-read hypothesis. Do not brute-force the credentials provider, invent object IDs, or probe stock NextAuth endpoints without a target-specific lead.

## Request accounting and closure

Count baseline, explicit login continuation, HTML-declared assets, manifest-declared chunks, and focused API validation separately. Close the branch with:

- exact request count;
- fetched graph count and remaining references;
- auth/callback findings;
- API denial or data result;
- secrets/source-map/sink review;
- explicit blocked prerequisite for authenticated continuation.

## Pitfalls

- Do not equate a large `404` body with a generic error until its HTML/framework references are inspected.
- Do not stop after HTML-declared chunks when a build manifest declares lazy page chunks.
- Do not infer an open redirect from a `callbackUrl` parameter before resolving the sanitizer implementation.
- Do not call public route names, static chunks, or intended public CMS content unauthorized disclosure.
- Do not treat all POST requests as mutations, but require an exact source-derived read-only shape and a bounded proof plan before sending one.
