---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.066561+00:00
source_quality: 9
source_id: appsec-fyi-root-topic-index
source_role: discovery_index
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, validation_technique, evidence_requirement, tooling_procedure]
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# Cross-site leaks (XS-Leaks) - Security | MDN MDN MDN Mozilla

- URL: `https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/XS-Leaks`
- Source ID / role / trust: `appsec-fyi-root-topic-index` / `discovery_index` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`direct root`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `appsec_fyi_linked_resources`
- Content chars: `18420`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Skip to main content Skip to search HTML: Markup language Elements Global attributes Attributes See all… Responsive images HTML cheatsheet Date & time formats See all… SVG MathML XML CSS: Styling language Properties Selectors At-rules Values See all… Box model Animations Flexbox Colors See all… Column layouts Centering an element Card component See all… JavaScript: Scripting language Standard built-in objects Expressions & operators Statements & declarations Functions See all… Control flow & error handing Loops and iteration Working with objects Using classes See all… Web APIs: Programming interfaces File system API Fetch API Geolocation API HTML DOM API Push API Service worker API See all… Using the Web animation API Using the Fetch API Working with the History API Using the Web speech API Using web workers All web technology Accessibility HTTP URI Web extensions WebAssembly WebDriver See all… Media Performance Privacy Security Progressive web apps Learn web development Getting started modules Core modules MDN Curriculum Check out the video course from Scrimba, our partner Structuring content with HTML module CSS styling basics module CSS layout module Dynamic scripting with JavaScript module Discover our tools Playground HTTP Observatory Border-image generator Border-radius generator Box-shadow generator Color format converter Color mixer Shape generator Get to know MDN better About MDN Advertise with us Community MDN on GitHub Web Security Attacks Cross-site leaks (XS-Leaks) OS default Light Dark Deutsch English (US) 日本語 Cross-site leaks (XS-Leaks) Cross-site leaks (also called XS-Leaks) are a class of attack in which an attacker's site can derive information about the target site, or about the user's relationship with the target site, by using web platform APIs that enable sites to interact with one another.
- This might seem to be a much less damaging problem than, for example, a cross-site scripting attack, but it can still have serious consequences for users.
- Unlike other attacks such as XSS or Clickjacking , cross-site leaks are not a single technique.

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
