---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.069322+00:00
source_quality: 9
source_id: appsec-fyi-root-topic-index
source_role: discovery_index
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, validation_technique, evidence_requirement, tooling_procedure]
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# CSS:the bomb inside your inbox | PortSwigger Research

- URL: `https://portswigger.net/research/css-the-bomb-inside-your-inbox`
- Source ID / role / trust: `appsec-fyi-root-topic-index` / `discovery_index` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`direct root`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `appsec_fyi_linked_resources`
- Content chars: `62388`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Table of contents Introduction Abusing allowed HTML/CSS Abusing HTML labels to perform UI actions Controlling AI browsers via email Account takeover from pasting into a draft email Exfiltrating tokens when CSP is blocking all external resources Bypassing CSS sanitization Making external requests Syntax quirks Image proxy bypasses Tracking if email is viewed in Fastmail Displaying your IP address in ProtonMail Tracking if email is viewed in Gmail Combining an image proxy bypass with indirect prompt injection CSS mutation in Fastmail Exploitation with CSS Defacing Outlook using CSS gadgets CSS hotwiring in Fastmail Stealing passwords Defences Future attacks HTML only keylogger Chrome real time keylogger References Materials Introduction Webmail has been around for decades and it's always had to solve a very difficult problem of taking untrusted HTML and displaying it to the user in a safe way.
- Controlling AI browsers via email OpenAI released a browser called Atlas when I was researching this topic so I decided to see if I could use sanitized CSS to perform indirect prompt injection from an email message in Fastmail.
- I'll use them to hide text from an AI browser. <style> div:before { content: " Before "; color: orange ; } div:after { content: " After " color: blue ; } </style> <div>Existing text</div> Rendered preview: Before Existing text After I experimented with various properties and noticed something interesting, you could use the :before and :after pseudo-elements to hide the text from the LLM and you could use opacity to hide it from the victim.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, validation_technique, evidence_requirement, tooling_procedure`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `true`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
