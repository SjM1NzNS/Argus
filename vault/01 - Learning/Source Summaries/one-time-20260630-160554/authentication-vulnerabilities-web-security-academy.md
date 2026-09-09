---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.059381+00:00
source_quality: 8
classification: severity rule
vulnerability_class: Authentication / Session
---

# Authentication vulnerabilities | Web Security Academy

- URL: `https://portswigger.net/web-security/authentication`
- Source group: `backfill_deep_content`
- Content chars: `7242`
- Classification: **severity rule**
- Vulnerability class: **Authentication / Session**

## Source summary

- Authentication vs authorization How vulnerabilities arise Impact of vulnerable authentication Vulnerabilities in password-based authentication Brute-force attacks Brute-forcing usernames Brute-forcing passwords Enumerating usernames Flaws in brute-force protection Account locking User rate limiting Exploiting HTTP basic authentication Vulnerabilities in multi-factor authentication Two-factor authentication tokens Bypassing two-factor authentication Bypassing two-factor authentication with flawed verification Brute-forcing two-factor authentication codes Vulnerabilities in other authentication mechanisms Keeping users logged in Resetting user passwords Sending passwords by email Resetting passwords using a URL Changing user passwords Vulnerabilities in OAuth authentication Securing your authentication mechanisms View all authentication labs Web Security Academy Authentication vulnerabilities Authentication vulnerabilities Conceptually, authentication vulnerabilities are easy to understand.
- Something you have , This is a physical object such as a mobile phone or security token.
- These are sometimes called "possession factors".

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
