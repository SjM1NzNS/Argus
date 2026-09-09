---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.018359+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: Authentication / Session
---

# HTTP Host header attacks | Web Security Academy

- URL: `https://portswigger.net/web-security/host-header`
- Source group: `backfill_deep_content`
- Content chars: `10911`
- Classification: **Web2 skill update**
- Vulnerability class: **Authentication / Session**

## Source summary

- We'll outline the high-level methodology for identifying websites that are vulnerable to HTTP Host header attacks and demonstrate how you can exploit this for the following kinds of attacks: Password reset poisoning LABS Web cache poisoning LABS Exploiting classic server-side vulnerabilities Bypassing authentication LABS Virtual host brute-forcing Routing-based SSRF LABS Connection state attacks LABS Labs If you're already familiar with the basic concepts behind HTTP Host header vulnerabilities and just want to practice exploiting them on some realistic, deliberately vulnerable targets, you can access all of the labs in this topic from the link below.
- How vulnerabilities arise Testing for vulnerabilities Supply an arbitrary Host header Check for flawed validation Send ambiguous requests Inject host override headers Exploiting vulnerabilities Password reset poisoning How does a password reset work?
- Constructing an attack Web cache poisoning Exploiting classic server-side vulnerabilities Bypassing authentication Virtual host brute-forcing Routing-based SSRF Connection state attacks SSRF via a malformed request line Preventing vulnerabilities View all HTTP Host header labs Web Security Academy HTTP Host header attacks HTTP Host header attacks In this section, we'll discuss how misconfigurations and flawed business logic can expose websites to a variety of attacks via the HTTP Host header.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
