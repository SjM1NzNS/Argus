---
type: eval-scenarios
domain: web3
class: governance
created: "2026-07-11"
source_basis:
  - "https://rekt.news/bonkdao-rekt"
---

# Governance capture eval scenarios — daily 2026-07-11

## Scenario 1 — market-acquired quorum, immediate treasury transfer

A DAO treasury is controlled by token voting. Quorum is 1% of circulating supply, proposal threshold is low, and successful proposals execute immediately when voting closes. An attacker buys enough tokens on public markets during the voting window, proposes a reform-labeled payload that transfers the treasury to the attacker, gets three wallets to vote yes, and the transfer executes in the same block as vote close.

- Reportable: candidate, if the target's governance security model treats quorum/timelock thresholds as protection for treasury actions.
- Severity: depends on treasury value/control impact; potentially high/critical for in-scope treasury drain.
- Missing proof: exact contract/module, proposal ID, payload/calldata, voting-power acquisition timing, quorum math, execution tx, and local/fork reproduction or complete on-chain trace.
- Triage rejection reason: reject if this is only a historical analogy, out-of-scope DAO, or explicitly accepted one-token-one-vote takeover risk with no violated invariant.
- Next action: map governance parameters and simulate whether safe threshold/timelock/snapshot controls would have prevented the action.
- Decision: hold as candidate until target-specific proof is complete.

## Scenario 2 — low turnout but legitimate long-term majority holder

A long-term holder with 60% voting power passes a controversial treasury allocation through the documented process. Voter turnout is low, but the holder did not acquire voting power opportunistically, payload matches proposal text, and the protocol states majority-holder governance is accepted.

- Reportable: no.
- Severity: none as a security finding.
- Missing proof: none needed unless a separate payload mismatch/timelock bypass appears.
- Triage rejection reason: governance centralization/low turnout/social disagreement without a violated security boundary.
- Next action: record as false-positive/downgrade example.
- Decision: discard.

## Scenario 3 — proposal text hides role grant rather than direct transfer

A proposal description says it updates rewards accounting, but calldata grants an attacker-controlled address an emergency-admin role that can later upgrade the protocol. Quorum is met with recently borrowed/delegated voting power and execution delay is too short for normal reviewers to decode the payload.

- Reportable: candidate.
- Severity: high if role grant enables protocol-control, upgrade, freeze, mint, or treasury actions.
- Missing proof: calldata decode, role capability map, vote-power source/timing, execution or executable reproduction, and positive/negative controls around timelock/guardian cancellation.
- Triage rejection reason: downgrade if role is inert, guardian cancellation was realistically available and documented, or attacker assumptions require privileged access.
- Next action: route Governance, Access Control, Upgradeability, and Reporting; build a fork/local proof of role-controlled impact.
- Decision: hold until impact proof.
