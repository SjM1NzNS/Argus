---
type: learning-source-summary
compiled_at: 2026-08-05T05:31:36.646495+00:00
source_quality: 6
classification: Web2 skill update
vulnerability_class: API Security
---

# Biggest Crypto Payment Hacks & the Attack Surface Beneath Them

- URL: `https://blocksec.com/blog/crypto-payment-hacks-attack-surface`
- Source group: `browser_dom_linked_resources`
- Content chars: `18719`
- Classification: **Web2 skill update**
- Vulnerability class: **API Security**

## Source summary

- The attacker impersonated a well-known figure and used typosquatting to spoof the sender address — swapping a capital "I" for a lowercase "l," nearly invisible in a sans-serif font — to lure MoonPay executives into transferring USDT to an attacker-controlled address.
- Four things had to fail at once for that to work: Endpoint security — the signers' web UI came from a third party, with no independent verification.
- That last point is worth sitting with: even a well-resourced exchange can lose $1.5 billion when several safeguards fail at once — endpoint security, transaction verification, contract design, and operational isolation.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
