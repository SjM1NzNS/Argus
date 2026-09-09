---
type: eval-case
domain: web2
status: populated
name: oauth-csrf-medium
expected_decision: "report if owned-account session/account impact is proven; otherwise hold"
created: ""
updated: "2026-06-29"
---

# OAuth CSRF Medium

## Scenario

Missing/broken state allows attacker to force an owned victim browser to complete OAuth login as the attacker or link attacker IdP identity to victim app account. Test uses owned attacker/victim accounts and captures final session/account-link state.

## 1. Is this reportable?

Yes if the flow creates login CSRF, account confusion, or attacker-controlled account linking in the in-scope app. The OAuth playbook requires owned-account proof and final session/account state evidence.

## 2. What severity?

Medium by default; higher only with account takeover or broad tenant impact

## 3. What proof is missing?

If absent: browser/session before-after evidence, exact auth/callback URLs, token redaction, and proof that the victim account/session is affected.

## 4. What would triage reject?

Triage rejects missing-state claims where another binding prevents impact, or where only attacker logs into attacker account.

## 5. What is the next action?

Run Skeptic/Impact review and draft only if account/session impact is reproduced.

## 6. Should Argus report, hold, or discard?

Decision: report if owned-account session/account impact is proven; otherwise hold.

## Expected Argus reasoning

PASS: OAuth playbook allows real CSRF/account-linking impact while holding missing-impact claims.
