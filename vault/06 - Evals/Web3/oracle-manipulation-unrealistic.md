---
type: eval-case
domain: web3
status: populated
name: oracle-manipulation-unrealistic
expected_decision: "discard"
created: ""
updated: "2026-06-29"
---

# Oracle Manipulation Unrealistic

## Scenario

A report claims price manipulation is possible by moving a deep Chainlink-backed asset price 50% in one block, but provides no feasible mechanism, ignores heartbeat/deviation checks, and assumes attacker can control oracle output.

## 1. Is this reportable?

No. The Oracles playbook rejects impossible liquidity, ignored adapter checks, privileged oracle assumptions, and fantasy single-block manipulation.

## 2. What severity?

None

## 3. What proof is missing?

Realistic manipulation route, cost model, stale/decimal/adapter flaw, and measurable protocol impact.

## 4. What would triage reject?

Triage would reject impossible market assumptions and no PoC.

## 5. What is the next action?

Discard. Convert to a question checklist only if a concrete adapter weakness is later discovered.

## 6. Should Argus report, hold, or discard?

Decision: discard.

## Expected Argus reasoning

The playbook correctly filters unrealistic oracle narratives.
