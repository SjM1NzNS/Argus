---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.400785+00:00
source_quality: 5
classification: severity rule
vulnerability_class: Accounting / Invariants
---

# Pashov Audit Group's finding — [L-01] `RateProvider` assumes savings token and underlying token have the same decimals — RegnumAurum review

- URL: `https://solodit.cyfrin.io/issues/l-01-rateprovider-assumes-savings-token-and-underlying-token-have-same-decimal-pashov-audit-group-none-regnumaurum_2026-03-26-markdown`
- Source group: `browser_dom_linked_resources`
- Content chars: `4178`
- Classification: **severity rule**
- Vulnerability class: **Accounting / Invariants**

## Source summary

- This makes the assumption that share decimals equal underlying decimals a documented but violated contract invariant.
- Overview Impact Low Quality 0.0 (0) Rarity 0.0 (0) Full report https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2026-03-26.md Categories Tags Author(s) Pashov Audit Group Cyfrin Private Audits Public Reports Pricing Aderyn Updraft Blockchain Basics Solidity 101 Foundry 101 All courses CodeHawks Competitions First Flights Leaderboard Solodit Docs Findings Audits Checklist Resources Blog Case Studies Success Stories Glossary Support Powered by Cyfrin Give us feedback!

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
