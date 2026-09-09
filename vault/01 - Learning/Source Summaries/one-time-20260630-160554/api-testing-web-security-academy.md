---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.058542+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: API Security
---

# API testing | Web Security Academy

- URL: `https://portswigger.net/web-security/api-testing`
- Source group: `backfill_deep_content`
- Content chars: `13062`
- Classification: **Web2 skill update**
- Vulnerability class: **API Security**

## Source summary

- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification API testing Overview API recon API documentation Discovering API documentation Using machine-readable API documentation Identifying API endpoints Interacting with API endpoints Identifying supported HTTP methods Identifying supported content types Using Intruder to find hidden endpoints Finding hidden parameters Mass assignment vulnerabilities Identifying hidden parameters Testing mass assignment vulnerabilities Preventing vulnerabilities in APIs Server-side parameter pollution Testing the query string Truncating query strings Injecting invalid parameters Injecting valid parameters Overriding existing parameters Testing REST paths Testing structured data formats Testing with automated tools Preventing server-side parameter pollution Alignment with the OWASP Top 10 API vulnerabilities View all API testing labs Web Security Academy API testing API testing APIs (Application Programming Interfaces) enable software systems and applications to communicate and share data.
- In this topic, we'll teach you how to test APIs that aren't fully used by the website front-end, with a focus on RESTful and JSON APIs.
- Related pages To learn more GraphQL APIs, see our GraphQL API vulnerabilities Academy topic.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
