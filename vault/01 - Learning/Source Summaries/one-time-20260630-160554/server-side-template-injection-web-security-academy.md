---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.055304+00:00
source_quality: 9
classification: false-positive pattern
vulnerability_class: API Security
---

# Server-side template injection | Web Security Academy

- URL: `https://portswigger.net/web-security/server-side-template-injection`
- Source group: `backfill_deep_content`
- Content chars: `13762`
- Classification: **false-positive pattern**
- Vulnerability class: **API Security**

## Source summary

- If you're interested in how we were able to exploit some of these vulnerabilities on live websites, a full write-up is available on our research page.
- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification Server-side template injection What is server-side template injection?
- Impact of server-side template injection How vulnerabilities arise Constructing an attack Detecting vulnerabilities Identifying the template engine Exploiting the vulnerability Read the documentation Learn the basic template syntax Security documentation Documented exploits Explore the environment Developer-supplied objects Create a custom attack Using an object chain Using developer-supplied objects Preventing vulnerabilities View all server-side template injection labs Web Security Academy Server-side template injection Server-side template injection This technique was first documented by PortSwigger Research in the conference presentation Server-Side Template Injection: RCE for the Modern Web App .

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
