---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.078343+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# All labs | Web Security Academy

- URL: `https://portswigger.net/web-security/all-labs`
- Source group: `backfill_deep_content`
- Content chars: `2438`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification All labs SQL injection Cross-site scripting Cross-site request forgery (CSRF) Clickjacking DOM-based vulnerabilities Cross-origin resource sharing (CORS) XML external entity (XXE) injection Server-side request forgery (SSRF) HTTP request smuggling OS command injection Server-side template injection Path traversal Access control vulnerabilities Authentication WebSockets Web cache poisoning Insecure deserialization Information disclosure Business logic vulnerabilities HTTP Host header attacks OAuth authentication File upload vulnerabilities JWT Essential skills Prototype pollution GraphQL API vulnerabilities Race conditions NoSQL injection API testing Web LLM attacks Web cache deception Web Security Academy All labs All labs Mystery lab challenge Try solving a random lab with the title and description hidden.
- Take me to the mystery lab challenge SQL injection Cross-site scripting Cross-site request forgery (CSRF) Clickjacking DOM-based vulnerabilities Cross-origin resource sharing (CORS) XML external entity (XXE) injection Server-side request forgery (SSRF) HTTP request smuggling OS command injection Server-side template injection Path traversal Access control vulnerabilities Authentication WebSockets Web cache poisoning Insecure deserialization Information disclosure Business logic vulnerabilities HTTP Host header attacks OAuth authentication File upload vulnerabilities JWT Essential skills Prototype pollution GraphQL API vulnerabilities Race conditions NoSQL injection API testing Web LLM attacks Web cache deception Find vulnerabilities using Burp Suite Try for free Burp Suite Vulnerabilities Customers Company Insights © 2026 PortSwigger Ltd.
- As you'll have no prior knowledge of the type of vulnerability that you need to find and exploit, this is great for practicing recon and analysis.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
