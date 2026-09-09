---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:41.984140+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: API Security
---

# GraphQL API vulnerabilities | Web Security Academy

- URL: `https://portswigger.net/web-security/graphql`
- Source group: `backfill_deep_content`
- Content chars: `17875`
- Classification: **Web2 skill update**
- Vulnerability class: **API Security**

## Source summary

- Components of queries and mutations Subscriptions Introspection Finding GraphQL endpoints Universal queries Common endpoint names Request methods Initial testing Exploiting unsanitized arguments Discovering schema information Using introspection Probing for introspection Running a full introspection query Visualizing introspection results Suggestions Bypassing GraphQL introspection defenses Bypassing rate limiting using aliases GraphQL CSRF Preventing GraphQL attacks Preventing GraphQL brute force attacks Preventing CSRF over GraphQL View all GraphQL labs Web Security Academy GraphQL API vulnerabilities GraphQL API vulnerabilities GraphQL vulnerabilities generally arise due to implementation and design flaws.
- Finding GraphQL endpoints Before you can test a GraphQL API, you first need to find its endpoint.
- As GraphQL APIs use the same endpoint for all requests, this is a valuable piece of information.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
