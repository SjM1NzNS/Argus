---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.398429+00:00
source_quality: 5
classification: severity rule
vulnerability_class: Race Conditions / TOCTOU
---

# Node.js | Report #3582376 - HTTP Response Queue Poisoning via TOCTOU Race Condition in `http.Agent` | HackerOne

- URL: `https://hackerone.com/reports/3582376`
- Source group: `browser_dom_linked_resources`
- Content chars: `1525`
- Classification: **severity rule**
- Vulnerability class: **Race Conditions / TOCTOU**

## Source summary

- 6 days ago Reported on March 3, 2026, 8:08am UTC Reported by yushengchen Reported to Node.js Participants Report Id #3582376 Resolved Severity Low (3.7) Disclosed June 25, 2026, 5:03am UTC Weakness Time-of-check Time-of-use (TOCTOU) Race Condition CVE ID CVE-2026-48931 Bounty None Retest None Total reward None Account details None
- Skip to main content > Learn more about HackerOne Log in 5 #3582376 HTTP Response Queue Poisoning via TOCTOU Race Condition in `http.Agent` Share: Report SUMMARY BY NODE.JS A flaw in Node.js HTTP Agent can cause a client to accept as valid a response that is send before the client has sent the request.
- This vulnerability affects all supported release lines: Node.js 22, Node.js 24, and Node.js 26.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
