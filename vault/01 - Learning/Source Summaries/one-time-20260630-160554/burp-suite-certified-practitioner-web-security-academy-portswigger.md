---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.090328+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: API Security
---

# Burp Suite Certified Practitioner | Web Security Academy - PortSwigger

- URL: `https://portswigger.net/web-security/certification`
- Source group: `backfill_deep_content`
- Content chars: `3474`
- Classification: **Web2 skill update**
- Vulnerability class: **API Security**

## Source summary

- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification A web security certification , from the makers of Burp Suite What is a Burp Suite Certified Practitioner?
- Prove your proficiency Demonstrate a deep knowledge of the latest vulnerability classes and how to exploit them.
- Develop your team's expertise with knowledge of the latest vulnerability classes and how to exploit them.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
