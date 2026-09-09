---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:41.981754+00:00
source_quality: 9
classification: severity rule
vulnerability_class: IDOR / BOLA / Access Control
---

# Access control vulnerabilities and privilege escalation | Web Security Academy

- URL: `https://portswigger.net/web-security/access-control`
- Source group: `backfill_deep_content`
- Content chars: `15577`
- Classification: **severity rule**
- Vulnerability class: **IDOR / BOLA / Access Control**

## Source summary

- Vertical access controls Horizontal access controls Context-dependent access controls Vertical privilege escalation Unprotected functionality Parameter-based access control Platform misconfiguration URL-matching discrepancies Horizontal privilege escalation Horizontal to vertical privilege escalation Insecure direct object references (IDOR) Direct references to database objects Direct references to static files Vulnerabilities in multi-step processes Vulnerabilities in Referer-based controls Vulnerabilities in location-based controls Preventing View all access control labs Web Security Academy Access control Access control vulnerabilities and privilege escalation In this section, we describe: Privilege escalation.
- Labs If you're familiar with the basic concepts behind access control vulnerabilities and want to practice exploiting them on some realistic, deliberately vulnerable targets, you can access labs in this topic from the link below.
- Broken access controls are common and often present a critical security vulnerability.

## Extracted methodology

- Affected surface: Object, tenant, account, or authorization boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
