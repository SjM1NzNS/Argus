---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.073843+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: Race Conditions / TOCTOU
---

# Race conditions | Web Security Academy

- URL: `https://portswigger.net/web-security/race-conditions`
- Source group: `backfill_deep_content`
- Content chars: `22223`
- Classification: **Web2 skill update**
- Vulnerability class: **Race Conditions / TOCTOU**

## Source summary

- There are many variations of this kind of attack, including: Redeeming a gift card multiple times Rating a product multiple times Withdrawing or transferring cash in excess of your account balance Reusing a single CAPTCHA solution Bypassing an anti-brute-force rate limit Limit overruns are a subtype of so-called "time-of-check to time-of-use" (TOCTOU) flaws.
- Limit overrun race conditions Detecting and exploiting with Burp Repeater Detecting and exploiting with Turbo Intruder Hidden multi-step sequences Methodology 1 - Predict potential collisions 2 - Probe for clues 3 - Prove the concept Multi-endpoint race conditions Aligning multi-endpoint race windows Connection warming Abusing rate or resource limits Single-endpoint race conditions Session-based locking mechanisms Partial construction race conditions Time-sensitive attacks Preventing race conditions View all race condition labs Web Security Academy Race conditions Race conditions Race conditions are a common type of vulnerability closely related to business logic flaws.
- A race condition attack uses carefully timed requests to cause intentional collisions and exploit this unintended behavior for malicious purposes.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
