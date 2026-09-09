---
type: technique-extraction
status: draft
created: "2026-06-29 11:53"
domain: web2
run: "2026-06-29-learning-dry-run"
---

# Web2 Technique Extraction — Argus Learning Dry Run

## Top 10 extracted Web2 lessons

### 1. Access control evidence must compare two owned principals

- Affected surfaces: Access Control
- Lesson: For IDOR/BOLA/BFLA, require attacker and victim/second owned account, same request shape, server-side authorization failure, and unauthorized read/write/action evidence. UI differences alone are not enough.
- Evidence requirements: in-scope asset, reproducible request/response, clear attacker/victim or object model where applicable, and downgrade analysis.
- False-positive guard: do not treat source/scanner/index output as proof.

### 2. API object identifiers are leads, not findings

- Affected surfaces: REST API / Access Control
- Lesson: Numeric IDs, UUIDs, org IDs, project IDs, node IDs, and tenant IDs should seed hypotheses; they become reportable only after cross-account impact is reproduced.
- Evidence requirements: in-scope asset, reproducible request/response, clear attacker/victim or object model where applicable, and downgrade analysis.
- False-positive guard: do not treat source/scanner/index output as proof.

### 3. Auth/session tests need state-transition evidence

- Affected surfaces: Authentication & Session
- Lesson: Password reset, email change, MFA, invite, and remember-me checks need before/after state evidence and replay details, not only token-decoding observations.
- Evidence requirements: in-scope asset, reproducible request/response, clear attacker/victim or object model where applicable, and downgrade analysis.
- False-positive guard: do not treat source/scanner/index output as proof.

### 4. OAuth/SSO must preserve state, redirect, nonce, PKCE, and account-linking invariants

- Affected surfaces: OAuth & SSO
- Lesson: OAuth issues are reportable when an attacker can bind/login/redirect/authorize across accounts or clients; open redirects without token or account impact are usually downgraded.
- Evidence requirements: in-scope asset, reproducible request/response, clear attacker/victim or object model where applicable, and downgrade analysis.
- False-positive guard: do not treat source/scanner/index output as proof.

### 5. GraphQL authorization is per resolver and mutation, not per endpoint

- Affected surfaces: GraphQL
- Lesson: Schema visibility and introspection are leads; reportability usually requires unauthorized resolver data, mutation impact, batching bypass, or hidden operation abuse.
- Evidence requirements: in-scope asset, reproducible request/response, clear attacker/victim or object model where applicable, and downgrade analysis.
- False-positive guard: do not treat source/scanner/index output as proof.

### 6. XSS reportability depends on context, exploitability, and meaningful impact

- Affected surfaces: XSS
- Lesson: Reflection is not enough: require executable context or realistic DOM sink, CSP/browser constraints, victim interaction model, and impact such as account action, token/session exposure, or privileged context.
- Evidence requirements: in-scope asset, reproducible request/response, clear attacker/victim or object model where applicable, and downgrade analysis.
- False-positive guard: do not treat source/scanner/index output as proof.

### 7. SSRF/webhooks are high-risk tests and need safe validation design

- Affected surfaces: SSRF / Webhooks
- Lesson: URL fetchers and callbacks need minimal non-sensitive proof; metadata access, internal scans, or webhook triggering should be Zone 3 unless explicitly allowed.
- Evidence requirements: in-scope asset, reproducible request/response, clear attacker/victim or object model where applicable, and downgrade analysis.
- False-positive guard: do not treat source/scanner/index output as proof.

### 8. File upload tests must distinguish storage issues from execution issues

- Affected surfaces: File Upload / Cloud Storage
- Lesson: Public object URLs, MIME confusion, SVG/HTML rendering, and signed URL leakage each need separate evidence and false-positive checks.
- Evidence requirements: in-scope asset, reproducible request/response, clear attacker/victim or object model where applicable, and downgrade analysis.
- False-positive guard: do not treat source/scanner/index output as proof.

### 9. Secrets require offline-first validation and redaction

- Affected surfaces: Secret Exposure
- Lesson: Format hits, JS config, Firebase/Sentry/public keys, and GitHub matches must be classified and redacted; never list/read/write cloud resources without approval and scope permission.
- Evidence requirements: in-scope asset, reproducible request/response, clear attacker/victim or object model where applicable, and downgrade analysis.
- False-positive guard: do not treat source/scanner/index output as proof.

### 10. Scanner and index output are triage inputs only

- Affected surfaces: Reporting
- Lesson: PortSwigger/HackTricks/AppSec.fyi/scanners can guide tests, but reports need in-scope reproduction, impact, evidence, downgrade analysis, and scope contract support.
- Evidence requirements: in-scope asset, reproducible request/response, clear attacker/victim or object model where applicable, and downgrade analysis.
- False-positive guard: do not treat source/scanner/index output as proof.

