---
type: eval-case
domain: web2
status: populated
name: oauth-open-redirect-low-or-invalid
expected_decision: "discard or hold as open-redirect-only, not OAuth severity"
created: ""
updated: "2026-06-29"
---

# OAuth Open Redirect Low Or Invalid

## Scenario

An OAuth login flow accepts a redirect-like parameter that can bounce the browser to attacker.com after an error. No authorization code, access token, ID token, session cookie, account linking, tenant selection, or role mapping is affected. The IdP remains out of scope.

## 1. Is this reportable?

Not as an OAuth/SSO vulnerability. It may be a low open redirect only if the program accepts that class, but the OAuth playbook requires app-side auth/token/account/session impact.

## 2. What severity?

None/Low unless token/account/session impact is proven

## 3. What proof is missing?

Token/code/session delivery to attacker, login CSRF, account linking, tenant/role confusion, or app-side authorization impact.

## 4. What would triage reject?

Triage rejects severity inflation based on OAuth adjacency alone, public metadata, or out-of-scope IdP behavior.

## 5. What is the next action?

Discard as OAuth issue; optionally hold as low open-redirect lead if program accepts open redirects.

## 6. Should Argus report, hold, or discard?

Decision: discard or hold as open-redirect-only, not OAuth severity.

## Expected Argus reasoning

PASS: OAuth playbook blocks weak open-redirect escalation.
