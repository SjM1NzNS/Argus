---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.052101+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: API Security
---

# What is SQL Injection? Tutorial & Examples | Web Security Academy

- URL: `https://portswigger.net/web-security/sql-injection`
- Source group: `backfill_deep_content`
- Content chars: `15925`
- Classification: **Web2 skill update**
- Vulnerability class: **API Security**

## Source summary

- Dashboard Learning paths Latest topics Request smuggling Web cache deception Web LLM attacks API testing NoSQL injection View all topics All content All labs All topics Mystery labs Hall of Fame Leaderboard Interview - Kamil Vavra Interview - Johnny Villarreal Interview - Andres Rauschecker Get started Get certified Get certified How to prepare How it works Practice exam Exam hints and guidance What the exam involves FAQs Validate your certification SQL injection What is SQL injection?
- Detecting SQL injection vulnerabilities In different parts of the query In different contexts Examples of SQL injection Retrieving hidden data Subverting application logic Retrieving data from other tables Examining the database Blind SQL injection Second-order SQL injection Examining the database Querying the type and version Listing the contents UNION attacks Determining the number of columns Finding columns with a useful data type Retrieving interesting data Retrieving multiple values in a single column Blind SQL injection What is blind SQL injection?
- In many cases, an attacker can modify or delete this data, causing persistent changes to the application's content or behavior.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
