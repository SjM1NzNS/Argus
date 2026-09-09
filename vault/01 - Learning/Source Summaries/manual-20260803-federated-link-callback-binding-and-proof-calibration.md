---
type: source-summary
status: promoted
created: "2026-08-03"
domain: web2
source_basis:
  - "RFC 9700 section 4.7.1"
  - "PortSwigger forced OAuth profile linking"
  - "OpenID4Java 1.0.0 checksum-pinned source review"
  - "Argus authorized local-fixture federated-link review"
---

# Federated link callback binding and proof calibration — 2026-08-03

## Promotion decision

Promote four narrow gates into the existing OAuth & SSO playbook and evals:

1. a valid signed callback and fresh nonce do not prove that the receiving browser/session/account initiated an account-link operation;
2. assertion/code/nonce age must be measured from the exact library/configuration and separated from transaction binding;
3. browser cookie-delivery claims must match the actual callback method and navigation context; and
4. compositional source/component proofs must not be labelled browser end-to-end.

No target-specific exploit string, credential, assertion, callback, cookie, or reusable token is retained here.

## Source ledger

### RFC 9700 §4.7.1

- URL: <https://datatracker.ietf.org/doc/html/rfc9700#section-4.7.1>
- Lesson: redirect-response CSRF protection must link the response to the user-agent session with a transaction-bound value. Application state must also resist tampering and swapping.
- Promotion: bind account-link transactions to the initiating session and account, not only to a signed provider response.

### PortSwigger — forced OAuth profile linking

- URL: <https://portswigger.net/web-security/oauth/lab-oauth-forced-oauth-profile-linking>
- Lesson: a missing state/initiator binding on an identity-link callback can let an attacker splice their provider identity into a victim's authenticated application session.
- Promotion: explicit initiator/receiver matrix and durable post-link authentication gate.
- False-positive note: this analogous lab supports the class; it is not proof for any target.

### OpenID4Java 1.0.0 source

- Source JAR: <https://repo1.maven.org/maven2/org/openid4java/openid4java/1.0.0/openid4java-1.0.0-sources.jar>
- Independently observed SHA-256: `49c25c9fcbbaf42f5b9eee2bb884d33a7e89a5039281cc057da2eb63dc02c5a6`
- Relevant source: `ConsumerManager` initializes `new InMemoryNonceVerifier(60)`; `AbstractNonceVerifier` rejects a nonce when its age exceeds `_maxAgeSeconds * 1000`.
- Lesson: a pre-generated response may have a short delivery window, but freshness/replay validation does not correlate a first-use response with the browser that initiated linking.
- Promotion: always record the effective library/configured age window and distinguish pre-generation from an authorized just-in-time provider fixture.

### Adjacent same-product design precedent

- Example URL: <https://gerrit.googlesource.com/gerrit/+/b4a83f54f65f0ac5ac9017e4a9874209251ffbda/java/com/google/gerrit/httpd/auth/oauth/OAuthSession.java#52>
- Lesson: an adjacent session-scoped OAuth implementation can reveal the intended transaction-binding design.
- Promotion: use adjacent implementations as code-review precedent, never as substitute proof for the candidate path.

## Operational matrix

For federated identity linking, preserve these rows where supported:

| Initiation | Callback receiver | Response | Expected |
|---|---|---|---|
| authenticated user/session A | same session A | fresh valid first use | link succeeds after explicit intent checks |
| anonymous/no current user | authenticated session B | fresh valid first use | reject |
| authenticated session A | authenticated session B | fresh valid first use | reject |
| session A | session A or B | operation/return target tampered | reject |
| session A | session A or B | stale response | reject |
| session A | session A or B | exact replay | reject |
| session A | session A | identity already linked elsewhere | reject without remapping |

Record the server-side transaction handle, intended account, operation, expected provider/identity, expiration, atomic consumption, durable external-identity state, and fresh authentication result.

## Browser-delivery gate

- Default-Lax behavior commonly sends cookies on cross-site top-level GET navigation, not ordinary cross-site POST.
- Record actual GET/POST/form/redirect behavior, effective `SameSite`, top-level/subresource context, browser/version, and redacted emitted cookie header.
- Do not call a callback “one-click” or browser-proven when only direct method calls or mocked requests were exercised.

## Evidence-level vocabulary

- `source-traced`: exact product/data-flow proof, no executed candidate path.
- `component`: one or more executed layers, with mocks/direct calls at product seams.
- `HTTP integration`: real routing, cookies/clients, callback transport, persistence; may not use a full browser.
- `browser end-to-end`: separate browser contexts exercise initiation, provider response, callback transport/cookie behavior, persistence, and fresh login in one realistic flow.

A source-traced plus compositional component proof can still justify a strong OSS report when affected configuration and durable impact are established. The report must disclose the unexercised browser assumptions and may not claim a higher evidence level.

## Artifacts promoted

- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/overview.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/reportability.md`
- `06 - Evals/Web2/oauth-oidc-identity-binding-weekly-20260728.md`
