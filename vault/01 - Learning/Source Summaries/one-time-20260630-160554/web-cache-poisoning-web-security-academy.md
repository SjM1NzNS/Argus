---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.076535+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# Web cache poisoning | Web Security Academy

- URL: `https://portswigger.net/web-security/web-cache-poisoning`
- Source group: `backfill_deep_content`
- Content chars: `13677`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Impact of web cache poisoning Constructing an attack Identify and evaluate unkeyed inputs Param Miner Elicit a harmful response Get the response cached Exploiting cache design flaws Delivering an XSS attack Exploit unsafe handling of resource imports Exploit cookie-handling vulnerabilities Using multiple headers Responses that expose too much information Cache-control directives Vary header Exploiting DOM-based vulnerabilities Chaining web-cache poisoning vulnerabilities Exploiting cache implementation flaws Key flaws Probing for flaws Identifying a suitable cache oracle Probe key handling Identifying an exploitable gadget Exploiting cache key flaws Unkeyed port Unkeyed query string Cache parameter cloaking Normalized cache keys Cache key injection Poisoning internal caches Preventing vulnerabilities Research View all web cache poisoning labs Web Security Academy Web cache poisoning Web cache poisoning In this section, we'll talk about what web cache poisoning is and what behaviors can lead to web cache poisoning vulnerabilities.
- A poisoned web cache can potentially be a devastating means of distributing numerous different attacks, exploiting vulnerabilities such as XSS, JavaScript injection, open redirection, and so on.
- If you're interested in a detailed description of how we discovered and exploited these vulnerabilities in the wild, the full write-ups are available on our research page.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
