---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.010197+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# What is CORS (cross-origin resource sharing)? Tutorial & Examples | Web Security Academy

- URL: `https://portswigger.net/web-security/cors`
- Source group: `backfill_deep_content`
- Content chars: `14263`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Vulnerabilities Server-generated ACAO header from client-specified Origin header Errors parsing Origin headers Whitelisted null Origin value Exploiting XSS via CORS trust relationships Breaking TLS with poorly configured CORS Intranets and CORS without credentials Preventing attacks URL validation bypass cheat sheet View all CORS labs Web Security Academy CORS Cross-origin resource sharing (CORS) In this section, we will explain what cross-origin resource sharing (CORS) is, describe some common examples of cross-origin resource sharing based attacks, and discuss how to protect against these attacks.
- Cross-origin resource sharing (CORS) is a browser mechanism which enables controlled access to resources located outside of a given domain.
- It generally allows a domain to issue requests to other domains, but not to access the responses.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
