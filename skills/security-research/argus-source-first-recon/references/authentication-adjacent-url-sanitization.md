# Authentication-Adjacent URL Sanitization

Use this reference when HTML, HAR, headers, JavaScript, source maps, or inventories contain OAuth/OIDC, SAML, password-reset, registration, magic-link, signed-download, presigned-upload, or session-bridging URLs.

## Principle

A URL can be capability material even when it has no obvious `token=` parameter. Transaction values such as `state`, `nonce`, `session_code`, `client_data`, `code`, `ticket`, `key`, signatures, and opaque redirect-state blobs can advance or replay an authentication workflow. File mode `0600` is necessary for raw evidence but does not make these values safe for ordinary derived inventories.

Derived inventories normally need route shape, origin, path, parameter names, and provenance—not parameter values.

## Sanitization algorithm

For every absolute URL candidate before it enters a derived inventory:

1. HTML-decode the candidate first so `&amp;` becomes `&` before query parsing.
2. Parse with a URL parser rather than regular-expression splitting.
3. Preserve only:
   - scheme;
   - hostname and explicit port;
   - path;
   - ordered query parameter names;
   - whether a fragment existed.
4. Remove userinfo entirely. `user:pass@host` and opaque identity-looking userinfo must never survive.
5. Replace every query value with a constant placeholder such as `<REDACTED>`, including values whose names appear harmless.
6. Replace any non-empty fragment with `<REDACTED>`; fragments can contain tokens or client-side router state.
7. Preserve duplicate parameter names when ordering or multiplicity matters to the parser, but never preserve their values.
8. Store candidate-secret metadata separately as type, source, line, length, and digest prefix only.

Raw evidence remains private and immutable with restrictive permissions and a hash. Regenerate the sanitized derivative instead of modifying the raw capture.

## Required tests

Before trusting a parser change, test at least:

```text
https://user:researcher@example.invalid/cb?state=abc&session_code=def#frag
https://example.test/cb?state=abc&amp;nonce=def
https://example.test/cb?a=1&a=2&blank=
```

Assert:

- no userinfo remains;
- every parsed query value equals the redaction placeholder;
- the fragment is absent or replaced;
- HTML-encoded separators do not collapse multiple parameters into one value;
- duplicate names and blank-value parameter presence remain represented;
- output JSON is mode `0600`;
- a post-generation scan finds none of the raw capability values.

## Recovery when a derivative leaked values

1. Stop printing or promoting the derivative.
2. Keep the raw capture private; do not destroy provenance.
3. Fix and syntax-check the parser.
4. Add a focused unit/smoke test for the observed URL shape.
5. Overwrite every affected derivative with sanitized output.
6. Scan notes, reports, logs, manifests, and tool output for the raw values.
7. Re-hash and re-run final hygiene checks after the last write.

A redaction defect is a tooling defect, not target evidence. Do not count its repair as target progress or report it as a vulnerability.