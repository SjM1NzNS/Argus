---
type: learning-source-summary
compiled_at: 2026-08-06T05:31:21.949366+00:00
source_quality: 5
classification: severity rule
vulnerability_class: File Upload / Media Processing
---

# Rocket.Chat | Report #3514640 - Unauthenticated Path Traversal (LFI) via /custom-sounds/ when CustomSounds uses FileSystem storage | HackerOne

- URL: `https://hackerone.com/reports/3514640`
- Source group: `browser_dom_linked_resources`
- Content chars: `1386`
- Classification: **severity rule**
- Vulnerability class: **File Upload / Media Processing**

## Source summary

- Skip to main content > Learn more about HackerOne Log in 19 #3514640 Unauthenticated Path Traversal (LFI) via /custom-sounds/ when CustomSounds uses FileSystem storage Share: Report SUMMARY BY ROCKET.CHAT An unauthenticated path traversal (LFI) vulnerability exists under /custom-sounds/ when CustomSounds storage is configured to FileSystem.
- By including ../ sequences in the request path, an attacker can read arbitrary files outside the base directory.

## Extracted methodology

- Affected surface: File upload / media parser / async processing surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
