---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.067571+00:00
source_quality: 8
source_id: appsec-fyi-root-topic-index
source_role: discovery_index
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, evidence_requirement, tooling_procedure]
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Bypassing DOMPurify again with mutation XSS | PortSwigger Research

- URL: `https://portswigger.net/research/bypassing-dompurify-again-with-mutation-xss`
- Source ID / role / trust: `appsec-fyi-root-topic-index` / `discovery_index` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`direct root`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `appsec_fyi_linked_resources`
- Content chars: `3056`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Back to all articles Related Research Cookie Chaos: How to bypass __Host and __Secure cookie prefixes Stealing HttpOnly cookies with the cookie sandwich technique Bypassing WAFs with the phantom $Version cookie Concealing payloads in URL credentials Burp Suite Vulnerabilities Customers Company Insights © 2026 PortSwigger Ltd.
- Burp Scanner Burp Suite's web vulnerability scanner Product comparison What's the difference between Pro and DAST?
- Overview Core Topics Black Hat XSS Request Smuggling Template Injection Top 10 Hacking Techniques Articles Meet the Researchers James Kettle Gareth Heyes Zakhar Fedotkin Tom Stacey Talks RSS Bypassing DOMPurify again with mutation XSS Gareth Heyes Researcher @garethheyes Published: Wednesday, 7 October 2020 at 14:17 UTC Updated: Wednesday, 7 October 2020 at 15:02 UTC After seeing Michał Bentkowski's DOMPurify bypass and the resulting patch, I was inspired to try and crack the patched version myself.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, evidence_requirement, tooling_procedure`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `true`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
