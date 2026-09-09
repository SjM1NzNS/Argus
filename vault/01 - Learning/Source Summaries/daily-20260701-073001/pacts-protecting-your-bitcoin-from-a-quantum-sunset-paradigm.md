---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.418187+00:00
source_quality: 6
classification: Web2 skill update
vulnerability_class: Authentication / Session
---

# PACTs: Protecting Your Bitcoin From a Quantum Sunset - Paradigm

- URL: `https://www.paradigm.xyz/2026/05/pacts-protecting-your-bitcoin-from-a-quantum-sunset`
- Source group: `browser_dom_linked_resources`
- Content chars: `17884`
- Classification: **Web2 skill update**
- Vulnerability class: **Authentication / Session**

## Source summary

- For an early holder like Satoshi, this would be a massive revelation—they would have to tell the world that they are alive and still in possession of their keys.
- For example, if a private key was derived from a parent key (as in the BIP-32 standard), the holder may be able to provide a zero-knowledge proof that they knew that parent key, which is something a quantum attacker could not have.
- About Team Portfolio Writing Open Source Careers Research PACTs: Protecting Your Bitcoin From a Quantum Sunset 05.01.2026|Dan Robinson An attacker with a powerful enough quantum computer could steal hundreds of billions of dollars of Bitcoin.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
