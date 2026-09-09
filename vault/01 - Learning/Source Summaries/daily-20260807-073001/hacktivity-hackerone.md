---
type: learning-source-summary
compiled_at: 2026-08-07T05:31:28.721860+00:00
source_quality: 6
classification: severity rule
vulnerability_class: API Security
---

# Hacktivity | HackerOne

- URL: `https://hackerone.com/hacktivity/overview`
- Source group: `browser_dom_linked_resources`
- Content chars: `14297`
- Classification: **severity rule**
- Vulnerability class: **API Security**

## Source summary

- 9 Monero Low Resolved `relay_tx` wallet-rpc skips `--restricted-rpc` guard and lets any caller corrupt wallet state via attacker-controlled `pending_tx` Bug reported by benisprlh was disclosed 2 days ago Improper Access Control - Generic The relay_tx wallet-RPC method in Monero was found to bypass the --restricted-rpc guard, allowing any caller to corrupt the wallet state by submitting a malicious pending_tx blob.
- 11 Monero High Resolved wallet-rpc crash via malformed /gettransactions response (empty txs → vector::front() in check_tx_key / check_tx_proof) Bug reported by bebensap was disclosed 2 days ago NULL Pointer Dereference A vulnerability was discovered in the Monero wallet software that could cause the wallet-rpc process to crash when handling a malformed response from the daemon's /gettransactions endpoint.
- Search for reports Filter Sort Disclosed Undisclosed 1 Nintendo Low Duplicate [Wii U/3DS/Switch] Improper bounds check in StationURL in all NEX clients leading to remote crash/RCE Bug reported by jonbarrow was disclosed 4 hrs ago Stack Overflow 110 Mozilla Critical $12,000 Resolved Unauthenticated RCE in Taskcluster web-server via GraphQL filter argument (sift $where) Bug reported by griffinf was disclosed 2 days ago Code Injection A vulnerability was discovered in the Taskcluster web-server that allowed unauthenticated remote code execution through the GraphQL filter argument.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
