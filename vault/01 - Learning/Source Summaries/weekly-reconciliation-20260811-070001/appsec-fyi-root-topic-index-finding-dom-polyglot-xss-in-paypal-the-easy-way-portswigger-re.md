---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.071169+00:00
source_quality: 9
source_id: appsec-fyi-root-topic-index
source_role: discovery_index
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, evidence_requirement, reportability_criterion, tooling_procedure]
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# Finding DOM Polyglot XSS in PayPal the Easy Way | PortSwigger Research

- URL: `https://portswigger.net/research/finding-dom-polyglot-xss-in-paypal-the-easy-way`
- Source ID / role / trust: `appsec-fyi-root-topic-index` / `discovery_index` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`direct root`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `appsec_fyi_linked_resources`
- Content chars: `9810`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- So we came up with the following vector: burpdomxss input[value='\">\<iframe srcdoc=&lt;script&gt;alert(document.domain)&llt;/script&gt;>\"'] This didn't work initially because of the CSP - but when we disabled this in Burp, we got the alert.
- We recently developed DOM Invader to help tackle this using a combined dynamic+manual approach to vulnerability discovery, and promptly found an interesting polyglot DOM XSS affecting PayPal.
- Overview Core Topics Black Hat XSS Request Smuggling Template Injection Top 10 Hacking Techniques Articles Meet the Researchers James Kettle Gareth Heyes Zakhar Fedotkin Tom Stacey Talks RSS Finding DOM Polyglot XSS in PayPal the Easy Way Gareth Heyes Researcher @garethheyes Published: Wednesday, 30 June 2021 at 16:47 UTC Updated: Wednesday, 7 September 2022 at 09:04 UTC Introduction Finding DOM XSS can be tricky when it's buried in thousands of lines of code.

## Extracted methodology

- Affected surface: Web/API/application surface
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
