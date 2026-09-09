---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:41.997720+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Automated Web Application Security Testing - PortSwigger

- URL: `https://portswigger.net/solutions/automated-security-testing`
- Source group: `backfill_deep_content`
- Content chars: `3235`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Scale your scanning securely Scale testing to match your application portfolio growth rate with Burp Suite's agent-led scanning model.
- Burp Scanner Burp Suite's web vulnerability scanner Product comparison What's the difference between Pro and DAST?
- With role-based access control (RBAC) and single sign-on as standard, no matter the size of your web estates, access security doesn't have to be an issue.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
