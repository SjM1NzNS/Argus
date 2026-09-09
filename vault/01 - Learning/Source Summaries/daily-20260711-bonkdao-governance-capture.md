---
type: source-summary
source: "https://rekt.news/bonkdao-rekt"
reviewed: "2026-07-11"
promotion: "Web3 Governance / Reporting"
---

# Daily 2026-07-11 — BonkDAO governance-capture lesson

Reviewed from `daily-20260711-073001` actual-content record: Rekt, "BonkDAO - Governance Attack", published 2026-07-10.

## High-signal lesson

The useful class-level lesson is not that low voter turnout is automatically a vulnerability. It is that a governance system can be drained by a rule-compliant attacker when low quorum/proposal thresholds, liquid vote acquisition, opaque proposal wording, and zero/short execution delay combine into a realistic treasury-control path.

Promoted gates:

- Treat governance thresholds/timelocks as security invariants when they guard treasury or protocol-control actions.
- Check whether an attacker can buy/borrow/delegate enough voting power shortly before or during voting to clear quorum/proposal threshold.
- Require proposal-title/description-to-calldata review: harmless/reform language must not obscure full treasury transfers, role grants, upgrades, or parameter sabotage.
- Require an execution-delay/emergency-response gate for high-impact governance payloads.
- Downgrade if the only issue is low participation, social engineering, or legitimate tokenholder voting without a violated target-specific invariant.

## Evidence pattern to preserve

For a future target, collect proposal ID, proposal text, exact payload/calldata, voting period, snapshot/timelock settings, threshold/quorum values, vote distribution, voting-power source and timing, execution transaction, and post-execution movement of funds/control.

## Daily disposition

Promoted into:

- `02 - Vulnerability Playbooks/Web3/Governance/invariants.md`
- `02 - Vulnerability Playbooks/Web3/Governance/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Reporting/reportability.md`
- `06 - Evals/Web3/governance-capture-daily-20260711-eval-scenarios.md`

Deferred: Bug Bounty Daily SPA/import-map text, `uphiago/recon-skills` repository overview, browser-DOM listing pages, seen/skipped links, and thin contest/product metadata.
