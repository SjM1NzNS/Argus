---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.011514+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Dashboard | Web Security Academy - PortSwigger

- URL: `https://portswigger.net/web-security/dashboard`
- Source group: `backfill_deep_content`
- Content chars: `2331`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification New labs: AI-powered scanner vulnerabilities Learn how indirect prompt injection can be used to manipulate AI-powered web application scanners into performing unintended actions, exfiltrating sensitive data, and making unauthorized internal requests.
- Web cache deception Web LLM attacks API testing NoSQL injection Learning paths Guided learning paths through the Web Security Academy Can we help you get started?
- Burp AI Your on-demand AI testing partner Cut through repetitive tasks, validate findings faster, and get expert agentic AI insight - so you can spend more time chasing the bugs that matter.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
