---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.053611+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# NoSQL injection | Web Security Academy

- URL: `https://portswigger.net/web-security/nosql-injection`
- Source group: `backfill_deep_content`
- Content chars: `16921`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification NoSQL injection Overview NoSQL databases NoSQL database models NoSQL syntax injection Detecting syntax injection in MongoDB Determining which characters are processed Confirming conditional behavior Overriding existing conditions NoSQL operator injection Submitting query operators Detecting operator injection in MongoDB Exploiting syntax injection to extract data Exfiltrating data in MongoDB Identifying field names Exploiting NoSQL operator injection to extract data Injecting operators in MongoDB Extracting field names Exfiltrating data using operators Timing based injection Preventing NoSQL injection View all NoSQL labs Web Security Academy NoSQL injection NoSQL injection NoSQL injection is a vulnerability where an attacker is able to interfere with the queries that an application makes to a NoSQL database.
- NoSQL injection may enable an attacker to: Bypass authentication or protection mechanisms.
- Burp Scanner Burp Suite's web vulnerability scanner Product comparison What's the difference between Pro and DAST?

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
