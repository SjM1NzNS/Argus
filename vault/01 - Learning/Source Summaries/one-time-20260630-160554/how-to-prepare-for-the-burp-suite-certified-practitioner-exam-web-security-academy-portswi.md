---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.079314+00:00
source_quality: 8
classification: severity rule
vulnerability_class: Client-Side / XSS
---

# How to prepare for the Burp Suite Certified Practitioner exam | Web Security Academy - PortSwigger

- URL: `https://portswigger.net/web-security/certification/how-to-prepare/index.html`
- Source group: `backfill_deep_content`
- Content chars: `5170`
- Classification: **severity rule**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Exploiting cross-site scripting to steal cookies Blind SQL injection with out-of-band data exfiltration Forced OAuth profile linking Brute-forcing a stay-logged-in cookie Exploiting HTTP request smuggling to capture other users' requests SSRF with blacklist-based input filter SQL injection with filter bypass via XML encoding Discovering vulnerabilities quickly with targeted scanning Step 3: Complete five mystery lab challenges Use the mystery lab challenge below to spin up five practitioner-level randomized lab challenges - you'll have to try and work out how to solve each challenge with no context, exactly as you would when performing recon in a real-world testing environment.
- Obtaining this certification proves that you have a deep knowledge of web vulnerability classes, and the skills required to discover and exploit them.
- Refresh your knowledge of how to demonstrate security impact, turning vulnerabilities into high-severity exploits.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
