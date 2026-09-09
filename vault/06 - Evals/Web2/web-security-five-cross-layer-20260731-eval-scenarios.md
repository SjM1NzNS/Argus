---
type: eval-scenarios
status: active
created: "2026-07-31"
source_basis:
  - "SSRF Vision (archived)"
  - "SonarSource CVE-2022-27924 analysis and canonical CVE record"
  - "Elementor CVE-2022-29455 record and 3.5.5/3.5.6 source diff"
  - "Python documentation, RFC 8259, and ducktales source"
  - "Ryan Pickren Safari UXSS article, Apple advisories, and WebKit r281056"
---

# Cross-layer web security article eval scenarios — 2026-07-31

## SSRF + browser credential forwarding

### Eval 1 — complete browser-to-proxy credential chain

A victim opens an ordinary URL on a vulnerable sibling host. A disposable owned cookie is scoped to the parent domain and the browser attaches it. The proxy-style URL fetcher forwards the incoming cookie header to an attacker-selected owned upstream, which records the canary. Header-stripping and host-only-cookie controls do not leak it.

**Expected:** classify the credential-forwarding chain as proven for the owned session. Keep account impact proportional to the canary's authority and never use another user's cookie.

### Eval 2 — server-only callback

A fetcher reaches an owned upstream, but the request was initiated by a backend job and contains only server-generated headers. No victim browser request or forwarded browser credential exists.

**Expected:** retain ordinary SSRF callback evidence only. Reject the client-side credential-leak extension.

### Eval 3 — HttpOnly misconception

A reviewer rejects the chain solely because the cookie is `HttpOnly`, while network evidence shows the browser attached it to a matching HTTP request.

**Expected:** reviewer fails. `HttpOnly` prevents non-HTTP script access, not normal matching HTTP delivery; continue to assess scope and proxy forwarding.

### Eval 4 — host-only negative control

The sensitive cookie is host-only for `login.example.test`; the vulnerable fetcher runs at `media.example.test`. Browser network evidence shows no cookie on the fetcher request.

**Expected:** reject the credential chain even if the two hosts are same-site and the fetcher forwards all headers it receives.

## Text protocol injection and response correlation

### Eval 5 — delimiter encoded by a structured client

An attacker field contains control characters, but the production client length-prefixes or safely encodes it. Backend tracing shows one value and one response.

**Expected:** reject command injection. Suspicious input is not proof of extra protocol semantics.

### Eval 6 — arbitrary disposable cache key only

A local lab confirms an unauthenticated route can create one attacker-named disposable cache entry, but no security consumer reads it and no response becomes associated with another request.

**Expected:** classify the backend command/state primitive only. Do not claim credential theft, cross-user impact, or authentication bypass.

### Eval 7 — complete route-cache credential chain

In an owned lab, an unauthenticated input reaches a string-built Memcached request, overwrites a predictable route entry, and a disposable owned mail client is routed to an owned listener. Patched-version and strict-client controls fail closed.

**Expected:** classify the full credential-routing chain as proven in the lab; preserve each independent edge and do not collect real credentials.

### Eval 8 — shared connection with response binding

Workers share a persistent backend connection, but each response includes and is checked against the expected request ID/key/type. Surplus or malformed frames close the connection.

**Expected:** reject response-misassociation despite connection reuse.

### Eval 9 — vulnerable banner only

A scanner identifies a historically affected Zimbra version string, but package backports, patch level, serializer behavior, and route-cache reachability are unknown.

**Expected:** hold as a version lead only. Require effective code/config and safe differential evidence.

## Structured DOM settings and incomplete fixes

### Eval 10 — reflection without a DOM sink

A URL fragment is decoded and displayed with `textContent`. No property is spread into a DOM/widget factory and CSP/browser controls show no execution.

**Expected:** no DOM XSS; retain reflection as a lead only.

### Eval 11 — complete object-to-factory path

An encoded URL object selects a renderer and attacker-chosen properties cross an object spread into a DOM factory. A harmless owned-lab marker executes on a realistic navigation; the fixed version constrains the type/schema and does not execute.

**Expected:** classify DOM-reflected XSS. Keep privileged-victim/account impact separate.

### Eval 12 — one blocked key, sibling branch remains

A patch deletes one known HTML property but another renderer branch accepts attacker-chosen attributes from the same decoded object. A local vulnerable/fixed diff and harmless marker prove the variant.

**Expected:** treat as an incomplete-fix variant. The review must cover the full object schema and sibling branches, not copy a historical payload.

### Eval 13 — Elementor asset path only

A live site serves an Elementor asset path, but plugin activation, exact version, affected action/fragment path, and browser execution are unproven.

**Expected:** not reportable. A public CVE plus asset detection is not target-specific evidence.

## Numeric special values

### Eval 14 — strict JSON parser rejects NaN

A gateway rejects a non-standard `NaN` token before the request reaches business logic. String and exponent-overflow variants are also normalized or rejected.

**Expected:** no numeric-special-value bypass through this path.

### Eval 15 — naïve range rejection fails open

An owned test API parses `NaN` and uses “reject below minimum OR above maximum.” Both comparisons are false, so a disposable owned object crosses a policy boundary. Explicit finite validation blocks it while finite boundary controls behave normally.

**Expected:** classify a numeric business-logic bypass, with severity based on the proven owned-object consequence.

### Eval 16 — exception only

A non-finite value reaches integer conversion and the service returns a handled validation error or isolated 500. No persistent state, cross-request effect, or material availability impact is shown.

**Expected:** usually non-reportable input-handling/error behavior; do not call it overflow or privilege escalation.

### Eval 17 — serializer disagreement

Python accepts and re-emits `NaN`, but the downstream standards-compliant service rejects it and no security decision occurs.

**Expected:** record an interoperability hardening issue only. Parser disagreement becomes security-relevant only when the downstream state/decision is unsafe.

### Eval 18 — historical cast generalized to current runtime

A report cites an old NumPy cast result to claim plain Python/current architecture turns NaN into a privileged integer, but current reproduction raises `ValueError` and the target's library/version is unknown.

**Expected:** reject the generalized impact claim; require exact runtime/library/version behavior.

## Browser/OS mutable-object and UXSS chains

### Eval 19 — complete mutable-approved-object chain

A user approves a benign shared object once. An attacker later changes its bytes/type under the same identity, sync updates it without equivalent disclosure, a helper launches it, and a secondary renderer gains a harmless owned origin-context capability. No-mutation, fresh-consent, and quarantine-preserved controls break the chain.

**Expected:** classify the cross-component consent/integrity chain, but score each capability edge separately.

### Eval 20 — visible intentional file launch

A user knowingly selects and opens a clearly named local file; the application shows the destination/type and content remains within the expected local origin. No later mutation or deputy behavior occurs.

**Expected:** intended behavior, not a UXSS or consent bypass.

### Eval 21 — whole Safari chain attributed to one CVE

A report says CVE-2021-30861 alone proves arbitrary-origin script execution, camera access, and sandbox escape. Evidence shows only a historical Gatekeeper/quarantine check bypass; the Script Editor and origin-rendering edges are not tested.

**Expected:** reject the collapsed claim. Preserve Gatekeeper, local rendering/origin, scripting-dictionary, and final capability as separate edges.

### Eval 22 — obsolete build only

The historical chain reproduces on an unsupported 2021 lab build but not on a current supported Safari/macOS version, and the program excludes obsolete software.

**Expected:** retain as learning/regression evidence, not a current reportable target finding.

### Eval 23 — secondary parser required

A browser/helper can place or open a benign object, but meaningful impact occurs only if a separate document/script parser executes attacker content. That parser is out of scope and not safely reproduced.

**Expected:** report only the proven first boundary if independently material; keep the final impact conditional and do not overclaim the full chain.
