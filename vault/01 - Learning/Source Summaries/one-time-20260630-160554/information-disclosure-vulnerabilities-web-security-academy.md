---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.070196+00:00
source_quality: 9
classification: severity rule
vulnerability_class: API Security
---

# Information disclosure vulnerabilities | Web Security Academy

- URL: `https://portswigger.net/web-security/information-disclosure`
- Source group: `backfill_deep_content`
- Content chars: `8971`
- Classification: **severity rule**
- Vulnerability class: **API Security**

## Source summary

- Examples of information disclosure Some basic examples of information disclosure are as follows: Revealing the names of hidden directories, their structure, and their contents via a robots.txt file or directory listing Providing access to source code files via temporary backups Explicitly mentioning database table or column names in error messages Unnecessarily exposing highly sensitive information, such as credit card details Hard-coding API keys, IP addresses, database credentials, and so on in the source code Hinting at the existence or absence of resources, usernames, and so on via subtle differences in application behavior In this topic, you will learn how to find and exploit some of these examples and more.
- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification Information disclosure What is information disclosure?
- Although some of this information will be of limited use, it can potentially be a starting point for exposing an additional attack surface, which may contain other interesting vulnerabilities.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
