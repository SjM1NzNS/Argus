---
type: learning-source-summary
compiled_at: 2026-06-30T07:45:38.491399+00:00
source_quality: 8
classification: vulnerability pattern
vulnerability_class: IDOR / BOLA / Access Control
---

# IDOR Vulnerabilities in ZITADEL's Organization API allows Cross-Tenant Data Tempering | GitLab Advisory Database (GLAD) Mobile menu

- URL: `https://advisories.gitlab.com/golang/github.com/zitadel/zitadel/CVE-2025-64431/`
- Source group: `appsec_fyi_linked_resources`
- Content chars: `1494`
- Classification: **vulnerability pattern**
- Vulnerability class: **IDOR / BOLA / Access Control**

## Source summary

- Advisories Dependency Scanning golang › github.com/zitadel/zitadel › CVE-2025-64431 CVE-2025-64431: IDOR Vulnerabilities in ZITADEL's Organization API allows Cross-Tenant Data Tempering November 5, 2025 (updated November 7, 2025 ) ZITADEL’s Organization V2Beta API contains Insecure Direct Object Reference (IDOR) vulnerabilities that allow authenticated users with specific administrator roles within one organization to access and modify data belonging to other organizations.
- Weakness CWE-639 : Authorization Bypass Through User-Controlled Key Source file go/github.com/zitadel/zitadel/CVE-2025-64431.yml Spotted a mistake?
- Learn more about Dependency Scanning → Affected versions All versions starting from 4.0.0-rc.1 before 4.6.3 Fixed versions 4.6.3 Solution Upgrade to version 4.6.3 or above.

## Extracted methodology

- Affected surface: Object, tenant, account, or authorization boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
