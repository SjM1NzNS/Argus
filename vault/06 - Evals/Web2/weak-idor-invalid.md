---
type: eval-case
domain: web2
status: populated
name: weak-idor-invalid
expected_decision: "discard"
created: ""
updated: "2026-06-29"
---

# Weak IDOR Invalid

## Scenario

A tester changes `user_id=1001` to `user_id=1002` on an in-scope endpoint and receives HTTP 200, but the response is a generic empty object or attacker-owned public profile metadata. There is no second owned victim account, no proof object 1002 belongs to another user, and no unauthorized read/write/action evidence.

## 1. Is this reportable?

No. The Access Control playbook classifies object IDs and response differences as leads only. There is no server-side authorization failure or owned victim/object model.

## 2. What severity?

None / Informational at most

## 3. What proof is missing?

Victim/second owned account, object ownership proof, sensitive data/action, raw authorized vs unauthorized comparison, and impact.

## 4. What would triage reject?

Triage would reject ID guessing, lack of victim model, no sensitive data, no state change, and no impact.

## 5. What is the next action?

Discard as finding. If scope and accounts allow, create a controlled two-account test plan rather than reporting.

## 6. Should Argus report, hold, or discard?

Decision: discard.

## Expected Argus reasoning

The new playbook correctly blocks over-reporting weak IDOR leads.
