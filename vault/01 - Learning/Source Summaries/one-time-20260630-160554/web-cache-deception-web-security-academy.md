---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.075864+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: API Security
---

# Web cache deception | Web Security Academy

- URL: `https://portswigger.net/web-security/web-cache-deception`
- Source group: `backfill_deep_content`
- Content chars: `30472`
- Classification: **Web2 skill update**
- Vulnerability class: **API Security**

## Source summary

- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification Web cache deception Overview Web caches Cache keys Cache rules Constructing an attack Using a cache buster Detecting cached responses Exploiting static extension cache rules Path mapping discrepancies Exploiting path mapping discrepancies Delimiter discrepancies Exploiting delimiter discrepancies Delimiter decoding discrepancies Exploiting delimiter decoding discrepancies Exploiting static directory cache rules Normalization discrepancies Detecting normalization by the origin server Detecting normalization by the cache server Exploiting normalization by the origin server Exploiting normalization by the cache server Exploiting file name cache rules Detecting normalization discrepancies Exploiting normalization discrepancies Preventing vulnerabilities Research View all web cache deception labs Web Security Academy Web cache deception Web cache deception Web cache deception is a vulnerability that enables an attacker to trick a web cache into storing sensitive, dynamic content.
- Web cache deception exploits cache rules to trick the cache into storing sensitive or private content, which the attacker can then access.
- The attacker can then request the same URL to access the cached response, gaining unauthorized access to private information.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
