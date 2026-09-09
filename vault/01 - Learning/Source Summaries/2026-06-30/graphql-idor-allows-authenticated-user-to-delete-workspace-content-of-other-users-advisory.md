---
type: learning-source-summary
compiled_at: 2026-06-30T07:45:38.492561+00:00
source_quality: 8
classification: severity rule
vulnerability_class: IDOR / BOLA / Access Control
---

# GraphQL IDOR allows authenticated user to delete workspace content of other users · Advisory · OpenCTI-Platform/opencti · GitHub

- URL: `https://github.com/OpenCTI-Platform/opencti/security/advisories/GHSA-pr6m-q4g7-342c`
- Source group: `appsec_fyi_linked_resources`
- Content chars: `6350`
- Classification: **severity rule**
- Vulnerability class: **IDOR / BOLA / Access Control**

## Source summary

- Weakness CWE-566 Authorization Bypass Through User-Controlled SQL Primary Key The product uses a database table that includes records that should not be accessible to an actor, but it executes a SQL statement with a primary key that can be controlled by that actor.
- OpenCTI-Platform / opencti Public Notifications You must be signed in to change notification settings Fork 1.4k Star 9.6k Code Issues 1.8k Pull requests 198 Discussions Actions Projects Security and quality 17 Insights Additional navigation options Code Issues Pull requests Discussions Actions Projects Security and quality Insights opencti Security Advisories GHSA-pr6m-q4g7-342c GraphQL IDOR allows authenticated user to delete workspace content of other users High aHenryJard published GHSA-pr6m-q4g7-342c Jan 5, 2026 Package No package listed Affected versions < 6.8.1 Patched versions >= 6.8.1 Description Summary The GraphQL mutation " WorkspacePopoverDeletionMutation " allows users to delete workspace-related objects such as dashboards and investigation cases.
- CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H CVE ID CVE-2025-61781 Weaknesses Weakness CWE-285 Improper Authorization The product does not perform or incorrectly performs an authorization check when an actor attempts to access a resource or perform an action.

## Extracted methodology

- Affected surface: Object, tenant, account, or authorization boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
