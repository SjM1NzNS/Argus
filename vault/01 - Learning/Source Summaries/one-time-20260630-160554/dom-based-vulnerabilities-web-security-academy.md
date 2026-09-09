---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.063158+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# DOM-based vulnerabilities | Web Security Academy

- URL: `https://portswigger.net/web-security/dom-based`
- Source group: `backfill_deep_content`
- Content chars: `8350`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Taint flow Sources Reflected and stored data Web messages Example sinks DOM-based XSS Open redirection Impact Sinks Preventing Cookie manipulation Impact Sinks Preventing JavaScript injection Impact Sinks Preventing Document-domain manipulation Sinks Preventing WebSocket-URL poisoning Impact Sinks Preventing Link manipulation Impact Sinks Preventing Web message manipulation Sinks Preventing Ajax request-header manipulation Impact Sinks Preventing Local file-path manipulation Impact Sinks Preventing Client-side SQL injection Impact Sinks Preventing HTML5-storage manipulation Sinks Preventing Client-side XPath injection Impact Sinks Preventing Client-side JSON injection Impact Sinks Preventing DOM-data manipulation Impact Sinks Preventing Denial of service Sinks Preventing Web message vulnerabilities Impact Constructing an attack Origin verification Sinks DOM clobbering Exploiting Preventing Preventing vulnerabilities View all DOM-based vulnerability labs Web Security Academy DOM-based DOM-based vulnerabilities In this section, we will describe what the DOM is, explain how insecure processing of DOM data can introduce vulnerabilities, and suggest how you can prevent DOM-based vulnerabilities on your websites.
- DOM-based vulnerabilities arise when a website contains JavaScript that takes an attacker-controllable value, known as a source, and passes it into a dangerous function, known as a sink.
- Sinks A sink is a potentially dangerous JavaScript function or DOM object that can cause undesirable effects if attacker-controlled data is passed to it.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
