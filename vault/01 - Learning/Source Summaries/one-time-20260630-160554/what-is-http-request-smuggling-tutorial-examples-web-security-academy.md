---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.074516+00:00
source_quality: 9
classification: severity rule
vulnerability_class: API Security
---

# What is HTTP request smuggling? Tutorial & Examples | Web Security Academy

- URL: `https://portswigger.net/web-security/request-smuggling`
- Source group: `backfill_deep_content`
- Content chars: `17190`
- Classification: **severity rule**
- Vulnerability class: **API Security**

## Source summary

- How vulnerabilities arise Performing an attack CL.TE vulnerabilities TE.CL vulnerabilities TE.TE vulnerabilities Identifying vulnerabilities CL.TE vulnerabilities TE.CL vulnerabilities Confirming vulnerabilities CL.TE vulnerabilities TE.CL vulnerabilities Exploiting vulnerabilities Bypassing front-end security controls Revealing front-end request rewriting Bypassing client authentication Capturing other users' requests Exploiting reflected XSS Turning an on-site redirect into an open redirect Turning root-relative redirects into open redirects Web cache poisoning Web cache deception Advanced request smuggling HTTP/2 request smuggling Message length HTTP/2 downgrading H2.CL vulnerabilities H2.TE vulnerabilities HTTP/2-exclusive vectors Request smuggling via CRLF injection Injecting via header names Injecting via pseudo-headers Supplying an ambiguous host Supplying an ambiguous path Injecting a full request line Injecting a URL prefix Injecting newlines Hidden HTTP/2 support Response queue poisoning Impact Constructing an attack Understanding the aftermath of request smuggling Smuggling a complete request Desynchronizing the response queue Stealing other users' responses HTTP/2 request splitting Accounting for front-end rewriting HTTP request tunnelling HTTP/2 request tunnelling Leaking internal headers Blind request tunnelling Non-blind request tunnelling using HEAD requests Web cache poisoning 0.CL request smuggling Browser-powered request smuggling CL.0 request smuggling Testing for CL.0 vulnerabilities Eliciting CL.0 behavior Exploiting CL.0 vulnerabilities H2.0 vulnerabilities Client-side desync attacks What is a client-side desync attack?
- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification HTTP request smuggling What is HTTP request smuggling?
- Request smuggling vulnerabilities are often critical in nature, allowing an attacker to bypass security controls, gain unauthorized access to sensitive data, and directly compromise other application users.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
