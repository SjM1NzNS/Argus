---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:41.987448+00:00
source_quality: 8
classification: false-positive pattern
vulnerability_class: API Security
---

# Burp Suite DAST | PortSwigger

- URL: `https://portswigger.net/burp/enterprise`
- Source group: `backfill_deep_content`
- Content chars: `4925`
- Classification: **false-positive pattern**
- Vulnerability class: **API Security**

## Source summary

- DevSecOps integration Easy integration with any CI/CD platform, native support for Jira, GitLab, and Trello, and a rich GraphQL API - to easily incorporate security within your existing software development processes.
- CI/CD, issue tracking platforms, and a rich GraphQL API) mean you can bake security into your software development.
- Secure your apps and APIs across the SDLC, before they hit production.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
