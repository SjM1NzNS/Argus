---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.066635+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# Getting started | Web Security Academy - PortSwigger

- URL: `https://portswigger.net/web-security/getting-started/index.html`
- Source group: `backfill_deep_content`
- Content chars: `3680`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- SQL Injection Authentication Cross-site scripting (XSS) Business logic vulnerabilities Find your way around Burp Suite with our video tutorials We've created a handy set of Burp Suite tutorial videos, to guide you through some of the key tools you'll need when working on the Web Security Academy.
- Burp Scanner Burp Suite's web vulnerability scanner Product comparison What's the difference between Pro and DAST?
- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification Getting started with the Web Security Academy Follow our beginner's guide to web security, to boost your cybersecurity skills one vulnerability at a time.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
