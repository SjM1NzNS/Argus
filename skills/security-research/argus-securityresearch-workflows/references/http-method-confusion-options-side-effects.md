# HTTP method confusion and destructive `OPTIONS` validation

Use this workflow when an HTTP router maps multiple methods—including `OPTIONS`, `HEAD`, or `GET`—to a state-changing handler, or when middleware and the exported raw handler expose different behavior.

## Source-first route audit

1. Enumerate every route, method set, parser, and state-changing handler.
2. Trace the router mapping into the final service call; do not infer safety from method names.
3. Search for middleware that may intercept the method before routing. Treat the raw exported handler, official launcher, reverse-proxy integration, and examples as distinct product surfaces.
4. Record which surface is documented or shipped. A protective wrapper narrows a raw-handler bug but does not automatically repair a separately exported/directly documented server.

## Owned runtime proof

For destructive `OPTIONS` behavior:

1. Create owned synthetic state through the product API.
2. Read it back as a pre-state control.
3. Send a browser-shaped preflight request to the same path:
   - method `OPTIONS`;
   - `Origin: https://attacker.invalid`;
   - `Access-Control-Request-Method: DELETE` (or the intended state-changing method).
4. Record the actual response status, but use the **before/after state transition** as ground truth.
5. Read state again and prove it is absent or unchanged as appropriate.
6. Test the official middleware/launcher separately and assert whether the destructive handler was called.
7. Preserve exact probe source/output, then remove temporary hooks and verify the clone is clean.

Do not hard-code a status based on source reading or a subagent summary. A destructive handler may return `200` when analysis predicted `204`; a missing-object read may return `500` rather than `404`. Assert the product state and a precise not-found signal, while recording unexpected status behavior as a separate observation.

## Why preflight matters

Browsers send `OPTIONS` before non-safelisted methods or headers. The actual `DELETE` can be blocked by CORS while the preflight has already reached a wrongly destructive handler. CORS response headers are evaluated after the server processes the preflight.

This can also cross method-only reverse-proxy/WAF policies that permit `OPTIONS` but block `DELETE`, provided the destructive raw handler is reachable behind that policy.

Authoritative protocol context should come from current sources such as:

- https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
- https://http.dev/cors

These explain browser behavior; product source and runtime evidence prove the bug.

## Reportability gate

Separate the correctness flaw from attacker impact:

- Strong: the actor can derive the path identifiers, a documented/direct embedding is reachable, or a normal cross-origin client preflights a known resource and loses state.
- Conditional: an upstream method policy treats `OPTIONS` as safe while forwarding it to the raw handler.
- Weak: only attacker-created disposable state can be deleted, identifiers are unguessable, and the official/default launcher always intercepts preflights.

List identifier prerequisites explicitly: app, user, session, artifact name/version, event ID, or tenant namespace. Do not claim arbitrary victim deletion when only owned-state deletion is proven.

A middleware negative control is first-class evidence. If the official launcher blocks the bug but the exported handler and shipped direct-server example remain affected, frame the exact affected integration instead of presenting the whole product as vulnerable.

## Remediation

- Never map `OPTIONS` to destructive handlers.
- Handle preflight in a side-effect-free middleware or dedicated handler.
- Return appropriate `Allow` / CORS headers without invoking business logic.
- Restrict destructive routes to their exact method.
- Add regression tests for raw handler and official wrapper surfaces.
- Keep authentication/authorization checks inside destructive handlers; do not rely only on method filtering upstream.

## Cleanup pitfall

Evidence preservation and cleanup are distinct operations. Copy probe source/output into the evidence directory first and verify the copies. Then request any required approval to delete temporary tests. Do not combine preservation and deletion in one approval-gated command: if deletion is blocked, the entire command may not run and the evidence copy may also be skipped.
