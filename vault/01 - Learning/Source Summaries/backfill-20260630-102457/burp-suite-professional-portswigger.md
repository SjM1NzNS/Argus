---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:41.992559+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: Authentication / Session
---

# Burp Suite Professional - PortSwigger

- URL: `https://portswigger.net/burp/pro`
- Source group: `backfill_deep_content`
- Content chars: `3614`
- Classification: **Web2 skill update**
- Vulnerability class: **Authentication / Session**

## Source summary

- Gain access to members-only events, including live demos, deep dives and Q&A sessions with our developers and security researchers.
- Burp Scanner Burp Suite's web vulnerability scanner Product comparison What's the difference between Pro and DAST?

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
