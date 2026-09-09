---
type: eval-case
domain: web3
status: populated
name: rounding-low-impact
expected_decision: "hold or discard; do not escalate"
created: ""
updated: "2026-06-29"
---

# Rounding Low Impact

## Scenario

A vault rounds in the attacker’s favor by 1 wei on certain deposits. Fuzzing confirms the maximum extractable value across realistic liquidity is below gas cost and cannot be amplified through loops, integrations, or large positions.

## 1. Is this reportable?

Usually no. The Share Accounting invariant playbook requires value-conservation break with quantified impact beyond dust/gas.

## 2. What severity?

Informational/Low at most unless amplified

## 3. What proof is missing?

Amplification path, realistic profit, user/protocol loss, or integration effect.

## 4. What would triage reject?

Triage would reject dust-only math findings without economic impact.

## 5. What is the next action?

Discard or hold as low-priority hardening; add an eval to ensure Argus does not over-severity rounding dust.

## 6. Should Argus report, hold, or discard?

Decision: hold or discard; do not escalate.

## Expected Argus reasoning

The new playbooks are conservative enough, but need an explicit rounding severity threshold section.
