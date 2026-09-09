---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:41.993244+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: File Upload / Media Processing
---

# Careers — PortSwigger

- URL: `https://portswigger.net/careers`
- Source group: `backfill_deep_content`
- Content chars: `4749`
- Classification: **Web2 skill update**
- Vulnerability class: **File Upload / Media Processing**

## Source summary

- My work gets recognised beyond my immediate team.

## Extracted methodology

- Affected surface: File upload / media parser / async processing surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
