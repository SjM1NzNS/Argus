---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.044012+00:00
source_quality: 5
source_id: appsec-fyi-root-topic-index
source_role: discovery_index
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, validation_technique, evidence_requirement, reportability_criterion, hunting_methodology, tooling_procedure]
classification: Web2 skill update
vulnerability_class: IDOR / BOLA / Access Control
---

# Authorization / Broken Access Control Resources | appsec.fyi

- URL: `https://appsec.fyi/authz.html`
- Source ID / role / trust: `appsec-fyi-root-topic-index` / `discovery_index` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`https://appsec.fyi`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `web2_topic_indexes`
- Content chars: `166251`
- Classification: **Web2 skill update**
- Vulnerability class: **IDOR / BOLA / Access Control**

## Source summary

- appsec.fyi Authorization / Broken Access Control Resources A curated AppSec resource library covering XSS, SQLi, SSRF, IDOR, RCE, XXE, OSINT, and more.
- Broken Access Control consistently ranks as the #1 risk in the OWASP Top 10, encompassing issues like privilege escalation (both vertical and horizontal), missing function-level access controls, and insecure direct object references at the authorization layer.
- Authorization / Broken Access Control Authorization vulnerabilities occur when applications fail to properly enforce access controls, allowing users to perform actions or access resources beyond their intended permissions.

## Extracted methodology

- Affected surface: Object, tenant, account, or authorization boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, validation_technique, evidence_requirement, reportability_criterion, hunting_methodology, tooling_procedure`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `true`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
