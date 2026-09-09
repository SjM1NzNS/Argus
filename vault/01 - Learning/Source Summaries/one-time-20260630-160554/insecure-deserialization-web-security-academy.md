---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.056999+00:00
source_quality: 9
classification: severity rule
vulnerability_class: API Security
---

# Insecure deserialization | Web Security Academy

- URL: `https://portswigger.net/web-security/deserialization`
- Source group: `backfill_deep_content`
- Content chars: `8993`
- Classification: **severity rule**
- Vulnerability class: **API Security**

## Source summary

- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification Insecure deserialization What is serialization?
- Serializing data makes it much simpler to: Write complex data to inter-process memory, a file, or a database Send complex data, for example, over a network, between different components of an application, or in an API call Crucially, when serializing an object, its state is also persisted.
- Serialization vs deserialization Deserialization is the process of restoring this byte stream to a fully functional replica of the original object, in the exact state as when it was serialized.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
