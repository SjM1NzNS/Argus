# Next.js / webpack source closure and secret-safe evidence

Use this reference when an approved, redirect-disabled root request yields a same-origin locale path and a Next.js page whose root HTML references hashed chunks.

## 1. Separate each live stage

Create a fixed plan and approval boundary for each stage:

1. one root `GET`, redirects disabled;
2. one exact same-origin `Location` target, with no root cookie replay;
3. only the JS/CSS paths literally present in that captured HTML;
4. only dynamic chunks resolved locally from the acquired webpack runtime.

Do not infer locale paths, image/media URLs, API routes, source maps, environment siblings, or chunk names. Stop on unexpected redirect, authentication state, cookie dependency, non-200 static response, TLS anomaly, or manifest drift.

## 2. Freeze the root-literal manifest

Record:

- source URL and HTML SHA-256;
- exact ordered paths;
- path provenance (`script[src]`, `link[href]`, preload, etc.);
- planned count, pacing, response cap, redirects-disabled rule, and stop conditions.

Fetch sequentially and retain a request ledger with HTTP status, bytes, SHA-256, redirect URL/count, TLS verification result, cookie count, content type, and curl exit status.

## 3. Resolve webpack dynamic chunks to a fixed point

Across every acquired JavaScript body:

1. extract dynamic import IDs from exact runtime call forms such as `.e(<integer>)`;
2. identify the runtime chunk and parse its chunk-filename resolver (commonly `.u=e=>...`);
3. account for a prefix/alias map before the ordinary `id.hash.js` map—some IDs resolve to a non-ID prefix;
4. derive exact same-origin chunk paths locally;
5. freeze those paths in a second manifest bound to the runtime-body SHA-256;
6. fetch that fixed manifest sequentially;
7. recompute dynamic IDs across root-literal plus dynamic chunks;
8. claim closure only when every observed ID resolves and the referenced-minus-acquired set is empty.

Preserve the dynamic ID set and exact resolver-derived filenames in evidence. Never guess filenames from an ID alone.

### Auth-gated route shells

A direct `GET` to a private Next.js route can return HTTP 200 while server-side rendering the sign-in page. Do not classify the status alone as access, and do not stop source closure merely because the requested page chunk was not loaded.

For every source-derived private route sampled within the approved request budget:

1. parse `script#__NEXT_DATA__` locally;
2. record the requested route separately from `__NEXT_DATA__.page`, `query` key names, page-prop key names, and non-sensitive booleans;
3. classify `requested private route -> sign-in page + return-path parameter` as an authentication gate, not a route bypass;
4. compare body hashes and script lists to determine whether several private routes collapse to the same shell;
5. acquire the exact `_buildManifest.js` referenced by that shell;
6. parse route-specific asset arrays from the captured manifest, including literal shared chunks and page chunks not present in the unauthenticated HTML;
7. resolve manifest function aliases from the captured invocation rather than dropping alias-backed dependencies;
8. freeze a manifest-bounded `referenced - already_acquired` set and fetch only those exact same-origin assets at the program-approved pace.

Route chunks recovered this way are still static source leads. They may expose first-party production API bases, bearer-token acquisition, object selectors, reversible versus destructive methods, and verification gates, but they do not authorize replay. Keep identity-provider infrastructure separate from target-owned integration behavior: a custom login domain or bundled SDK does not authorize testing the provider's control plane.

For the authenticated handoff, record the blocker explicitly and preserve the probe budget. Require the user to establish each controlled session manually, one account at a time, without sharing passwords, OTPs, cookies, or tokens. Start with owner-positive A→A and B→B controls, then one cross-account selector substitution and one same-shape random-invalid control. Prefer a reversible mutation with immediate restoration; destructive-only selectors require a disposable owned object and a separate one-shot approval.

## 4. Syntax-check extensionless evidence correctly

Evidence bodies are often stored as `001.body`. `node --check 001.body` can fail because Node treats the unknown extension as invalid input. This is a verifier bug, not a JavaScript syntax failure.

Use stdin instead:

```bash
node --check - < 001.body
```

Or pass the body to `node --check -` via a subprocess. Record per-file failures and require all acquired JS bodies to pass before declaring the graph syntactically sound.

## 5. Inventory source without overclaiming

Extract and attribute:

- API origins and exact scope membership;
- GraphQL operation names and operation type;
- authentication/token refresh flows;
- object, member, group, tenant, or account selectors;
- file/profile/logo/update/newsletter/registration actions;
- environment predicates and preview/draft/unpublished markers;
- browser sinks, `postMessage` listeners, HTML rendering, URL navigation, and dynamic execution primitives.

A public preview-labelled hostname may serve current production content. Require source or response evidence of draft/unpublished material before claiming preview leakage.

Bearer-protected member/group selectors are BOLA/BFLA hypotheses, not findings. Require legitimate controlled roles, owned objects, positive self controls, and negative cross-object controls. Do not approximate anonymously or invoke registration, unsubscribe, upload, or profile/company mutations merely because source maps them.

## 6. Redact client identifiers before contextual inspection

Minified bundles can contain browser-visible Google Maps keys, Gigya/OIDC client identifiers, or similar service configuration. Treat them as candidates, not findings.

Safe order:

1. scan all acquired files by signature without printing values;
2. record candidate type, file/index, count, original bytes, and original SHA-256;
3. redact in place before printing surrounding context;
4. support constructed values split across `.concat(...)` or adjacent literals, not only plain `key: "value"` assignments;
5. record sanitized bytes and current SHA-256;
6. update the request ledger to retain both download provenance and current sanitized state;
7. rerun the secret scan over the entire mission root.

For sanitized records, retain fields equivalent to:

```json
{
  "bytes": 355652,
  "download_sha256": "<original>",
  "sanitized_in_place": true,
  "sanitized_bytes": 355647,
  "sha256": "<current-sanitized>",
  "sanitization_marker": "[REDACTED_CLIENT_IDENTIFIER]"
}
```

Request totals should continue to reconcile against original downloaded bytes; retained-file checks should use `sanitized_bytes` and the current `sha256`.

Do not validate browser/API identifiers against third-party services unless a separate exact-scope, capability, and non-invasive approval plan exists. Public client configuration without demonstrated unauthorized capability, quota/billing exposure, authentication impact, or another deterministic effect fails the reportability gate.

## 7. Close with a schema-aware verifier

Verify after the final report write:

- manifests and ledgers parse;
- counts/statuses/original byte totals reconcile;
- retained current bytes/hashes match, including sanitized records;
- redirect, TLS, and cookie invariants hold;
- every dynamic ID is resolved and acquired;
- every JS body passes syntax via stdin;
- no source-map marker remains unexplained;
- no unredacted cookie, query state, client identifier, JWT-like value, private key, AWS key, or client-secret assignment remains;
- approval rows are closed;
- helper processes are absent;
- all mission files are `0600` and symlinks are absent;
- Git cleanliness is claimed only after successful worktree discovery.

The hygiene artifact itself changes the file count. Add it, then rerun the validator and record the post-write result.