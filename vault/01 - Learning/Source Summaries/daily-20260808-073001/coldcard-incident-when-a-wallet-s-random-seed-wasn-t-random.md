---
type: learning-source-summary
compiled_at: 2026-08-08T05:31:23.160926+00:00
source_quality: 6
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# COLDCARD Incident: When a Wallet's "Random" Seed Wasn't Random

- URL: `https://blocksec.com/blog/coldcard-entropy-failure-seed-recovery`
- Source group: `browser_dom_linked_resources`
- Content chars: `24351`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- COLDCARD spans the Mk1 through Mk5 hardware revisions and the Q model.
- Because the weakness was in the seeds themselves, the attack ran offline with no on-chain exploit transaction, collapsing seed recovery to ~40 bits on Mk2/Mk3 and ~72 bits on Mk4/Q/Mk5; the only on-chain activity was the sweeps of stolen funds.
- As of 7 August 2026, on-chain tracking had verified a floor of about 1,405 BTC (~$91M at the $64,700 7 August price) drained from roughly 4,925 addresses [1], wave-level attribution reached about 1,433 BTC across ten waves [2], and private-channel reconciliation with victims put the figure as high as 2,055 BTC (~$133M) [3].

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
