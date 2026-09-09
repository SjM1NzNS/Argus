---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.401374+00:00
source_quality: 5
classification: Web3 skill update
vulnerability_class: Accounting / Invariants
---

# Pashov Audit Group's finding: [L-03] Ghost voting power due to rounding error in expired locks: RegnumAurum_2026-03-21_2026-06-15

- URL: `https://solodit.cyfrin.io/issues/l-03-ghost-voting-power-due-to-rounding-error-in-expired-locks-pashov-audit-group-none-regnumaurum_2026-03-21-markdown`
- Source group: `browser_dom_linked_resources`
- Content chars: `2446`
- Classification: **Web3 skill update**
- Vulnerability class: **Accounting / Invariants**

## Source summary

- However, this breaks the invariant that zero locked tokens should yield zero voting power, potentially allowing dust-weight votes in governance or reward calculations.
- Recommendation Add a zero-check before the early return: if (currentTimestamp == endTimestamp) { if (effectiveTotalLocked == 0) decayedBias = 0; return (decayedBias < 0 ? (int128(0), remainder, effectiveTotalLocked) : (decayedBias, remainder, effectiveTotalLocked)); } Overview Impact Low Quality 0.0 (0) Rarity 0.0 (0) Full report https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2026-03-21.md Categories Tags Author(s) Pashov Audit Group Cyfrin Private Audits Public Reports Pricing Aderyn Updraft Blockchain Basics Solidity 101 Foundry 101 All courses CodeHawks Competitions First Flights Leaderboard Solodit Docs Findings Audits Checklist Resources Blog Case Studies Success Stories Glossary Support Powered by Cyfrin Give us feedback!
- Start researching Findings #66596 [L-03] Ghost voting power due to rounding error in expired locks RegnumAurum_2026-03-21 ・ Jun 15, 2026 Resolved Description In _decayBias, when the query timestamp equals the final epoch boundary (currentTimestamp == endTimestamp), the function returns early without checking if effectiveTotalLocked has reached zero.

## Extracted methodology

- Affected surface: Web3 protocol / smart contract
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
