---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.053007+00:00
source_quality: 5
source_id: appsec-fyi-root-topic-index
source_role: discovery_index
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, evidence_requirement, reportability_criterion, tooling_procedure]
classification: severity rule
vulnerability_class: File Upload / Media Processing
---

# Server-Side Request Forgery (SSRF) Resources | appsec.fyi

- URL: `https://appsec.fyi/ssrf.html`
- Source ID / role / trust: `appsec-fyi-root-topic-index` / `discovery_index` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`https://appsec.fyi`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `web2_topic_indexes`
- Content chars: `340050`
- Classification: **severity rule**
- Vulnerability class: **File Upload / Media Processing**

## Source summary

- Unauthenticated attackers can write files via WebDialer risking remote #cisco #vulnerability #ssrf #remotecodeexecution Urgent: SonicWall SMA1000 series vulnerability (CVE-2025-40595) allows remote exploitation via encoded URLs.
- From OWASP ⚠ Recently Exploited (CISA KEV) All KEV → CVE-2026-15409 SonicWall — SMA1000 Appliances Server-Side Request Forgery RANSOMWARE added 2026-07-14 CVE-2026-20230 Cisco — Unified Communications Manager Server-Side Request Forgery (SSRF) added 2026-06-25 CVE-2021-22054 Omnissa — Workspace ONE Server-Side Request Forgery added 2026-03-09 📖 Read the SSRF guide A long-form, source-cited deep dive synthesized from every resource below. → 📘 The comprehensive SSRF guide on chs.us A hand-written, in-depth practitioner guide — attacks, testing, and prevention. → Level: All Beginner Intermediate Advanced News & advisories Date Added Link Excerpt 2026-08-10 NEW 2026 Alejandro Cervantes: Para reducir SSRF: allowlists estrictas resolución segura bloqueo de redes internas y controles de salida.
- 1-Click Exploit Generator Audio Alerts Export Evidence Advanced Filtering Repo: #BugBounty #SSRF #Infosec How i found 3 SSRF in one day on different bug bounty targets.

## Extracted methodology

- Affected surface: File upload / media parser / async processing surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, evidence_requirement, reportability_criterion, tooling_procedure`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `true`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
