---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.019603+00:00
source_quality: 5
source_id: appsec-fyi-idor-resources
source_role: discovery_index
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, validation_technique, evidence_requirement, reportability_criterion, tooling_procedure]
classification: severity rule
vulnerability_class: IDOR / BOLA / Access Control
---

# Insecure Direct Object Reference (IDOR) Resources | appsec.fyi

- URL: `https://appsec.fyi/idor.html`
- Source ID / role / trust: `appsec-fyi-idor-resources` / `discovery_index` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`direct root`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `web2_topic_indexes`
- Content chars: `70664`
- Classification: **severity rule**
- Vulnerability class: **IDOR / BOLA / Access Control**

## Source summary

- Remediation involves enforcing authentication, implementing authorization checks, and avoiding reliance on `robots.txt` for security. → infosecwriteups.com Related (3) IDOR - PortSwigger Web Security Testing for IDORs (PortSwigger Burp docs) Broken Access Control: Advanced IDOR Exploitation 2026-07-29 2026 How I found an IDOR in Google Classroom on Day 3 of my Hunting? beginner 3 min read API Sec Bug Bounty Writeup detailing an Insecure Direct Object Reference (IDOR) vulnerability discovered in Google Classroom.
- Insecure Direct Object Reference (IDOR) Insecure Direct Object Reference (IDOR) is a vulnerability that arises when attackers can access or modify objects by manipulating identifiers used in a web application's URLs or parameters.
- This page collects writeups, tutorials, and tools for finding and exploiting IDOR vulnerabilities, from basic parameter tampering to advanced techniques like BOLA (Broken Object Level Authorization) in modern APIs.

## Extracted methodology

- Affected surface: Object, tenant, account, or authorization boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, validation_technique, evidence_requirement, reportability_criterion, tooling_procedure`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `true`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
