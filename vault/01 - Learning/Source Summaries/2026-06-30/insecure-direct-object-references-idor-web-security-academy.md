---
type: learning-source-summary
compiled_at: 2026-06-30T07:45:38.494115+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: IDOR / BOLA / Access Control
---

# Insecure direct object references (IDOR) | Web Security Academy

- URL: `https://portswigger.net/web-security/access-control/idor`
- Source group: `appsec_fyi_linked_resources`
- Content chars: `3859`
- Classification: **Web2 skill update**
- Vulnerability class: **IDOR / BOLA / Access Control**

## Source summary

- Insecure direct object references (IDOR) are a type of access control vulnerability that arises when an application uses user-supplied input to access objects directly.
- Vertical access controls Horizontal access controls Context-dependent access controls Vertical privilege escalation Unprotected functionality Parameter-based access control Platform misconfiguration URL-matching discrepancies Horizontal privilege escalation Horizontal to vertical privilege escalation Insecure direct object references (IDOR) Direct references to database objects Direct references to static files Vulnerabilities in multi-step processes Vulnerabilities in Referer-based controls Vulnerabilities in location-based controls Preventing View all access control labs Web Security Academy Access control IDOR Insecure direct object references (IDOR) In this section, we will explain what insecure direct object references (IDOR) are and describe some common vulnerabilities.
- IDOR examples There are many examples of access control vulnerabilities where user-controlled parameter values are used to access resources or functions directly.

## Extracted methodology

- Affected surface: Object, tenant, account, or authorization boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
