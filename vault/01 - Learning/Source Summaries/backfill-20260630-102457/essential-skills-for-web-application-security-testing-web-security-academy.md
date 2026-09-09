---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.012749+00:00
source_quality: 8
classification: severity rule
vulnerability_class: API Security
---

# Essential skills for web application security testing | Web Security Academy

- URL: `https://portswigger.net/web-security/essential-skills`
- Source group: `backfill_deep_content`
- Content chars: `4155`
- Classification: **severity rule**
- Vulnerability class: **API Security**

## Source summary

- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification Essential skills Overview Obfuscating attacks using encodings Context-specific decoding Decoding discrepancies URL encoding Double URL encoding HTML encoding XML encoding Unicode escaping Hex escaping Octal escaping Multiple encodings SQL CHAR() function Using Burp Scanner Scanning a specific request Scanning custom insertion points Scanning non-standard data structures Identifying unknown vulnerabilities Mystery lab challenge View all essential skills labs Web Security Academy Essential skills Essential skills We design the labs for the Web Security Academy to be as realistic as possible, but you should keep in mind that each lab demonstrates just one possible variation of a given vulnerability.
- Not only does this reduce the chance of you overlooking things, it can save you valuable time by helping you to rapidly identify potential attack vectors.
- Learn more Obfuscating attacks using encodings LAB SQL injection with filter bypass via XML encoding Using Burp Scanner during manual testing Testing for certain types of vulnerability can be fairly tedious, especially ones that involve trying numerous injection techniques in every controllable input.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
