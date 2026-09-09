---
type: learning-source-summary
compiled_at: 2026-08-04T05:31:30.065779+00:00
source_quality: 6
classification: Web2 skill update
vulnerability_class: API Security
---

# Stablecoins That Cannot Be Frozen: 2026 Map

- URL: `https://blocksec.com/blog/stablecoins-that-cannot-be-frozen`
- Source group: `browser_dom_linked_resources`
- Content chars: `16752`
- Classification: **Web2 skill update**
- Vulnerability class: **API Security**

## Source summary

- LUSD (Liquity v1) and RAI (Reflexer) are the two clearest cases, thanks to immutable, admin-less contracts.
- Peg mechanism Circulating supply (approx.) Trade-off USDT Yes (Tether owner multisig) Yes Fiat-backed Largest of the seven Most liquid, most freezable USDC Yes (Circle admin) Yes Fiat-backed Second-largest US-regulated, similarly freezable DAI (Sky, formerly Maker) No single-address freeze; governance can act Governance-controlled Crypto-collateralized + RWA Third-largest Not admin-freezable; governance-mutable LUSD (Liquity v1) No None; immutable ETH-collateralized 100 to 1,000 times smaller than USDT Truly unfreezable, thin liquidity Frax (frxUSD, post-2023) Yes Yes Fiat-backed Mid-sized Now similar to USDC RAI (Reflexer) No None Non-pegged reflex index Very small Not pegged to $1, price floats Ethena USDe Base token no; sUSDe yes Base no; sUSDe yes Synthetic delta-neutral Growing rapidly Freezable if staked Issuer freeze is a single company's ability to block your address on demand.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
