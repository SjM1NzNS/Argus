---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.402326+00:00
source_quality: 5
classification: Web3 skill update
vulnerability_class: Accounting / Invariants
---

# Pashov Audit Group's finding: [L-04] Incorrect asset preview in deepRebalance may prevent expected rebalancing: RegnumAurum_2026-03-26_2026-06-15

- URL: `https://solodit.cyfrin.io/issues/l-04-incorrect-asset-preview-in-deeprebalance-may-prevent-expected-rebalancing-pashov-audit-group-none-regnumaurum_2026-03-26-markdown`
- Source group: `browser_dom_linked_resources`
- Content chars: `4796`
- Classification: **Web3 skill update**
- Vulnerability class: **Accounting / Invariants**

## Source summary

- In practice, the real redemption is performed via: uint256 pmUSDReceived = baseAssetModule.redeem(moduleSharesAmount, address(this), address(this)); Due to factors such as: rounding behavior withdrawal fees exchange rate updates external protocol mechanics previewRedeem Allows an on-chain or off-chain user to simulate the effects of their redeemption at the current block, given current on-chain conditions. ​ MUST return as close to and no more than the exact amount of assets that would be withdrawn in a redeem call in the same transaction.
- I.e. redeem should return the same or more assets as previewRedeem if called in the same transaction. ​ MUST NOT account for redemption limits like those returned from maxRedeem and should always act as though the redemption would be accepted, regardless if the user has enough shares, etc. ​ MUST be inclusive of withdrawal fees.
- Integrators should be aware of the existence of withdrawal fees. ​ MUST NOT revert due to vault specific user/global limits.

## Extracted methodology

- Affected surface: Web3 protocol / smart contract
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
