---
type: eval-case
domain: web3
status: populated
name: reentrancy-valid
expected_decision: "report"
created: ""
updated: "2026-06-29"
---

# Reentrancy Valid

## Scenario

In a local/fork PoC, an unprivileged attacker contract deposits into a vault, calls withdraw, receives a callback before shares are burned, re-enters withdraw, and exits with more assets than deposited. The invariant `vault_assets + user_claims >= deposits - legitimate_fees` breaks with quantified profit.

## 1. Is this reportable?

Yes. The Reentrancy playbook requires callback-capable attacker path, state invariant break, local/fork PoC, and measurable impact; all are present.

## 2. What severity?

High/Critical if measurable fund loss/freeze/control impact is proven; otherwise Medium/hold

## 3. What proof is missing?

Scope confirmation for contract version/deployment, realistic initial state, full transaction trace, and whether mitigations exist in production.

## 4. What would triage reject?

Triage would reject if PoC uses impossible token behavior, privileged setup, or non-production code.

## 5. What is the next action?

Preserve PoC, traces, invariant assertion, and run Impact review before report draft.

## 6. Should Argus report, hold, or discard?

Decision: report.

## Expected Argus reasoning

The playbook correctly allows real, measurable reentrancy findings.
