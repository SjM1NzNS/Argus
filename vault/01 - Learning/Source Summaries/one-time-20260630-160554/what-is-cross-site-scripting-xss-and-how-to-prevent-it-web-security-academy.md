---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.056228+00:00
source_quality: 9
classification: technique
vulnerability_class: Client-Side / XSS
---

# What is cross-site scripting (XSS) and how to prevent it? | Web Security Academy

- URL: `https://portswigger.net/web-security/cross-site-scripting`
- Source group: `backfill_deep_content`
- Content chars: `13975`
- Classification: **technique**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Impact of an attack Proof of concept Testing Reflected XSS Impact Contexts Testing FAQs Stored XSS Impact Contexts Testing for vulnerabilities DOM-based XSS Testing HTML sinks JavaScript execution sinks Using DOM Invader Exploiting In third-party dependencies jQuery AngularJS DOM XSS combined with reflected and stored data Sinks Preventing XSS contexts Between HTML tags In HTML tag attributes JavaScript Terminating the existing script Breaking out of a string Using HTML-encoding Template literals Client-side template injection AngularJS sandbox AngularJS sandbox escape Constructing an advanced escape AngularJS CSP bypass Bypassing a CSP with an AngularJS sandbox escape Preventing Exploiting XSS vulnerabilities To steal cookies To capture passwords To perform CSRF Dangling markup injection Preventing attacks Content security policy (CSP) Mitigating XSS attacks Mitigating dangling markup attacks Bypassing CSP Protecting against clickjacking Preventing XSS attacks Encode data on output Validate input on arrival Whitelisting vs blacklisting Allowing "safe" HTML Using a template engine In PHP In JavaScript In jQuery Using CSP Cheat sheet View all XSS labs Web Security Academy Cross-site scripting Cross-site scripting In this section, we'll explain what cross-site scripting is, describe the different varieties of cross-site scripting vulnerabilities, and spell out how to find and prevent cross-site scripting.
- Cross-site scripting (also known as XSS) is a web security vulnerability that allows an attacker to compromise the interactions that users have with a vulnerable application.
- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification Cross-site scripting (XSS) What is XSS?

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
