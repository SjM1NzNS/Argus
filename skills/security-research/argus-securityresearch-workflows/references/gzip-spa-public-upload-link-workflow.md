# Gzip SPA and public upload-link source-first workflow

Use this pattern when an exact-listed file/upload host returns a public SPA, especially behind S3/CloudFront, while API and object operations remain authentication- or bearer-link-gated.

## Collection and decoding

1. Begin with the approved bounded baseline (`/`, `/robots.txt`, `/sitemap.xml`) with redirects disabled.
2. Compare status, content type, byte length, and body hash. Identical `200 text/html` bodies across unknown paths usually indicate an SPA catch-all, not three distinct resources.
3. Preserve wire bytes. If the body begins with gzip magic `1f 8b`, decode the saved body locally before parsing; do not re-request merely because the first collector omitted decompression.
4. Parse literal same-origin `script`, `modulepreload`, stylesheet, `env.js`, config, manifest, and worker references from the decoded shell.
5. Save both wire metadata and decoded assets so hashing and source analysis remain reproducible.

## Large Angular/chunk graphs

- Set a hard asset cap and expand only literal same-origin imports.
- Prioritize runtime config, `main`, application chunks, upload/API clients, route definitions, auth interceptors, object selectors, source-map declarations, and static policy/config files.
- Deprioritize generated icon/component libraries, locale packs, fonts, vendor SDK internals, and entry-module maps once they stop changing the application attack surface.
- A generated `.entry.js` or `.map` path returning the identical SPA-shell hash is a fallback, not a successful asset/source-map retrieval.
- If a broad import regex yields hundreds of references, stop at the cap and perform local semantic prioritization. Do not treat “remaining refs” as a reason for blind bulk fetching.

## Boundary controls

From source, extract exact:

- API bases and versions;
- request methods and body shapes;
- auth headers/interceptors;
- flow/list/config endpoints;
- upload-link routes and token parameter names;
- multipart initiation, presigned-part, completion/failure, and object retrieval operations;
- static client upload policy.

Use a minimal read-only boundary matrix before mutation:

- API root to distinguish API data from SPA fallback;
- one low-sensitivity configuration/list endpoint;
- one representative object/flow list endpoint without IDs;
- static source-declared config.

Uniform `401` responses on meaningful API endpoints are a negative control, not a lead. Public OAuth client IDs, delegated scopes, and browser telemetry client tokens are expected browser identifiers unless capability/impact proves otherwise.

## Public bearer upload links

A route such as `/public/upload/{opaque-link}` is often intentionally unauthenticated. Public routing alone is not broken authorization.

Require an owned-link positive control before testing link or object boundaries. A reportable result needs at least one of:

- cross-link or cross-object access outside the owned link;
- demonstrably predictable/weak link tokens;
- server-side upload policy overreach beyond the link's intended constraints;
- unintended public retrieval or unsafe inline execution;
- overwrite, modification, cancellation, deletion, or completion outside the authorized link;
- presigned-policy scope that permits access beyond the intended object/key.

Do not invent, enumerate, or substitute real bearer-link tokens. Do not POST/upload bytes until a separate owned-link plan defines harmless content, cleanup, positive/negative controls, and the exact stop condition.

## Closure and ledger state

Close the anonymous branch as `no-finding-owned-link/account-blocked` when:

- application source and relevant request methods are mapped;
- representative anonymous API controls deny access;
- no secret, signed URL, object/file/user metadata, or data is exposed;
- further validation requires an owned link or entitled account.

Record request counts, cap/deprioritization rationale, exact mapped surfaces, negative controls, non-claims, evidence paths, and the prerequisite for later credentialed continuation.
