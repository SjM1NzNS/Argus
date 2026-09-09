---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.401785+00:00
source_quality: 5
classification: Web3 skill update
vulnerability_class: Access Control / Admin Key
---

# Pashov Audit Group's finding: [L-03] MaxDeposit and maxRedeem do not reflect paused state: RegnumAurum_2026-03-26_2026-06-15

- URL: `https://solodit.cyfrin.io/issues/l-03-maxdeposit-and-maxredeem-do-not-reflect-paused-state-pashov-audit-group-none-regnumaurum_2026-03-26-markdown`
- Source group: `browser_dom_linked_resources`
- Content chars: `3420`
- Classification: **Web3 skill update**
- Vulnerability class: **Access Control / Admin Key**

## Source summary

- Recommended fix: function maxDeposit(address) external view returns (uint256) { if (paused()) return 0; ​ uint256 currentBalance = savingsToken.balanceOf(address(this)); if (currentBalance >= depositCap) return 0; return depositCap - currentBalance; } function maxRedeem(address owner) public view returns (uint256) { if (paused()) return 0; ​ RedeemRequest storage req = redeemRequests[owner]; uint256 exitTime = req.exitTime; if (exitTime == 0 || block.timestamp < exitTime) return 0; if (block.timestamp > exitTime + withdrawTimeLimit) return 0; return req.shares; } This ensures that: View functions accurately reflect the vault's operational state.
- Currently, both functions only enforce internal constraints such as caps and timing conditions: function maxDeposit(address) external view returns (uint256) { uint256 currentBalance = savingsToken.balanceOf(address(this)); if (currentBalance >= depositCap) return 0; return depositCap - currentBalance; } function maxRedeem(address owner) public view returns (uint256) { RedeemRequest storage req = redeemRequests[owner]; uint256 exitTime = req.exitTime; if (exitTime == 0 || block.timestamp < exitTime) return 0; if (block.timestamp > exitTime + withdrawTimeLimit) return 0; return req.shares; } However, neither function checks whether the vault is paused.
- Overview Impact Low Quality 0.0 (0) Rarity 0.0 (0) Full report https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2026-03-26.md Categories Tags Author(s) Pashov Audit Group Cyfrin Private Audits Public Reports Pricing Aderyn Updraft Blockchain Basics Solidity 101 Foundry 101 All courses CodeHawks Competitions First Flights Leaderboard Solodit Docs Findings Audits Checklist Resources Blog Case Studies Success Stories Glossary Support Powered by Cyfrin Give us feedback!

## Extracted methodology

- Affected surface: Object, tenant, account, or authorization boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
