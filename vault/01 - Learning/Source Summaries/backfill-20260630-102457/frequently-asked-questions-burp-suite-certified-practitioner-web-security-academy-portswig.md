---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.004545+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# Frequently asked questions - Burp Suite Certified Practitioner | Web Security Academy - PortSwigger

- URL: `https://portswigger.net/web-security/certification/frequently-asked-questions/index.html`
- Source group: `backfill_deep_content`
- Content chars: `7886`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- In addition, we strongly advise that you fully familiarize yourself with the exploiting XSS labs within the XSS topic.
- If you have a Burp Suite Professional license, but it is registered under an email domain of the company you work for rather than your personal email address, you will still be absolutely fine, from a technical perspective, to use that license for taking the exam.
- While exploiting each application, you will gain access to powerful functionality.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
