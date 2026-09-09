---
type: eval-case
domain: web3
status: populated
name: admin-only-issue-invalid
expected_decision: "discard unless policy accepts centralization/trust risk"
created: ""
updated: "2026-06-29"
---

# Admin Only Issue Invalid

## Scenario

Only the documented owner/admin can pause, upgrade, sweep, or set parameters. No exposed initializer, role mismatch, low-privileged path, governance bypass, or scoped key-management issue is shown.

## 1. Is this reportable?

No. Web3 Access Control playbook explicitly rejects admin-can-admin claims by default.

## 2. What severity?

None by default

## 3. What proof is missing?

Unprivileged/low-privileged path, broken role check, exposed initializer, governance bypass, or policy-accepted centralization impact.

## 4. What would triage reject?

Triage rejects intended privileged behavior.

## 5. What is the next action?

Discard or record as trust assumption if relevant.

## 6. Should Argus report, hold, or discard?

Decision: discard unless policy accepts centralization/trust risk.

## Expected Argus reasoning

PASS: Access Control/Upgradeability playbooks correctly reject admin-only noise.
