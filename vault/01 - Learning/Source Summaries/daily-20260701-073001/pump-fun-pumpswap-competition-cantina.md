---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.407603+00:00
source_quality: 5
classification: severity rule
vulnerability_class: Authentication / Session
---

# pump.fun / PumpSwap competition | Cantina

- URL: `https://cantina.xyz/competitions/19c5a5a6-f68d-4da8-b185-3f28c7f97bc1`
- Source group: `browser_dom_linked_resources`
- Content chars: `3813`
- Classification: **severity rule**
- Vulnerability class: **Authentication / Session**

## Source summary

- The other code base is the pump swap contracts which facilitates liquidity provisioning and trading using a constant product formula to determine the price and lp tokens to represent liquidity positions.
- All coins created on Pump are fair-launch, meaning everyone has equal access to buy and sell when the coin is first created.
- Severity level Impact: High Impact: Medium Impact: Low Likelihood: High Critical/High (Conditional) High Medium Likelihood: Medium High Medium Low Likelihood: Low Medium Low Informational Critical severity: If an attack can result in a loss of more than 50% of the TVL then this can be considered as a critical severity finding.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
