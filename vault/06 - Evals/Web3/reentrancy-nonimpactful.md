---
type: eval-case
domain: web3
status: populated
name: reentrancy-nonimpactful
expected_decision: "discard or hold as hardening note"
created: ""
updated: "2026-06-29"
---

# Reentrancy Nonimpactful

## Scenario

Static analysis flags an external call before a later state update, but the function is nonReentrant in production or the callback cannot alter relevant state. A local attempt re-enters but produces no balance, share, control, freeze, or accounting impact.

## 1. Is this reportable?

No. The Reentrancy playbook says reentrant control flow alone is not reportable without invariant break and measurable impact.

## 2. What severity?

None / Low if accepted as hardening only

## 3. What proof is missing?

Measurable loss/freeze/control impact, realistic callback-capable path, and invariant failure.

## 4. What would triage reject?

Triage would reject no-impact reentrancy and scanner-only evidence.

## 5. What is the next action?

Discard, or record as hardening if program accepts best-practice notes.

## 6. Should Argus report, hold, or discard?

Decision: discard or hold as hardening note.

## Expected Argus reasoning

The playbook correctly prevents over-reporting scanner/static noise.
