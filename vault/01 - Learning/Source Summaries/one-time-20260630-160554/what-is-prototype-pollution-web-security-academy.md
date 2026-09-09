---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.073351+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# What is prototype pollution? | Web Security Academy

- URL: `https://portswigger.net/web-security/prototype-pollution`
- Source group: `backfill_deep_content`
- Content chars: `10839`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- In client-side JavaScript, this commonly leads to DOM XSS , while server-side prototype pollution can even result in remote code execution.
- Object inheritance Prototype chain Accessing an object's prototype Modifying prototypes How vulnerabilities arise Sources URL JSON input Sinks Gadgets Client-side prototype pollution Finding sources manually Finding sources using DOM Invader Finding gadgets manually Finding gadgets using DOM Invader Prototype pollution via the constructor Bypassing flawed key sanitization Prototype pollution in external libraries Prototype pollution via browser APIs fetch() method Object.defineProperty() method Server-side prototype pollution Why is server-side prototype pollution more difficult to detect?
- A sink - In other words, a JavaScript function or DOM element that enables arbitrary code execution.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
