---
type: eval-case
domain: web3
status: populated
name: postmortem-translation-not-report-evidence
expected_decision: "do not report; create hypothesis/test plan"
created: ""
updated: "2026-06-29"
---

# Postmortem Translation Not Report Evidence

## Scenario

A Rekt/Immunefi/Solodit item describes an exploit in another protocol. A scoped target has similar function names, but no scoped invariant break, transaction sequence, local/fork PoC, or measurable impact is shown.

## 1. Is this reportable?

No. Reporting playbook says postmortems are realism sources, not report evidence.

## 2. What severity?

None until scoped PoC and impact

## 3. What proof is missing?

Scoped code path, realistic protocol state, unprivileged transaction sequence, invariant break, and measurable impact.

## 4. What would triage reject?

Triage rejects analogy-only reports and unsupported exploit narratives.

## 5. What is the next action?

Create hypothesis, identify matching playbooks, build local/fork test before any report claim.

## 6. Should Argus report, hold, or discard?

Decision: do not report; create hypothesis/test plan.

## Expected Argus reasoning

PASS: Reporting playbook blocks postmortem analogy reports.
