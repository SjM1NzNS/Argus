---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.409035+00:00
source_quality: 5
classification: severity rule
vulnerability_class: API Security
---

# Eigenlayer / eigenlayer-contracts competition | Cantina

- URL: `https://cantina.xyz/competitions/e7af4986-183d-4764-8bd2-1d6b47f87d99`
- Source group: `browser_dom_linked_resources`
- Content chars: `5709`
- Classification: **severity rule**
- Vulnerability class: **API Security**

## Source summary

- Opportunities Leaderboard Discover Cantina Log in Sign up eigenlayer-contracts @Eigenlayer Completed Instructions Leaderboard Total reward $2,500,000 No deposit required Status Completed Findings submitted 790 Start date 7 Mar 2025 End date 28 Mar 2025 As a restaking platform, EigenLayer allows stakers to deposit assets and delegate stake to operators.
- This competition will cover the major changes being made to the core restaking protocol.
- The earliest valid submission gets $2453.83, and the rest of the duplicates get $1886.79 each.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
