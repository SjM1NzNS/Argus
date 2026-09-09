---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.062507+00:00
source_quality: 9
classification: false-positive pattern
vulnerability_class: Authentication / Session
---

# What is CSRF (Cross-site request forgery)? Tutorial & Examples | Web Security Academy

- URL: `https://portswigger.net/web-security/csrf`
- Source group: `backfill_deep_content`
- Content chars: `10301`
- Classification: **false-positive pattern**
- Vulnerability class: **Authentication / Session**

## Source summary

- Flaws in CSRF token validation Validation depends on request method Validation depends on token being present Token isn't tied to user session Token is tied to a non-session cookie Token is duplicated in a cookie Bypassing SameSite cookie restrictions What is a site?
- There are no other tokens or mechanisms in place to track user sessions.
- Constructing an attack Delivering an exploit Defences Bypassing CSRF token validation What is a CSRF token?

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
