---
type: learning-source-summary
compiled_at: 2026-08-06T05:31:21.948086+00:00
source_quality: 9
classification: severity rule
vulnerability_class: Client-Side / XSS
---

# CRLF-Powered Desync Attacks: Beheading HTTP Streams | PortSwigger Research

- URL: `https://portswigger.net/research/crlf-powered-desync-attacks`
- Source group: `daily_deep_content`
- Content chars: `41737`
- Classification: **severity rule**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Forget open redirects or Cross-Site Scripting and instead, embrace the catastrophic potential of the CRLF-Powered Desync Worm.
- Research Origins HTTP Request Smuggling Request Header Injection Detecting Request Header Injection HTTP Request Splitting Response Queue Poisoning via Request Splitting RQP Inside the Infrastructure of a CDN Header Injection via Custom Upstream Header Header Injection via Non-Path Insertion Points AI-Generated Detection Techniques CRLF-Powered CL.TE Desync Attacks The Desync Disaster The Nested Response Mystery Cache Poisoning & AI-Generated HEAD Gadget Browser-Powered CRLF Desync Attacks CRLF-Powered Desync Worms HTTP Request Tunnelling Bypassing Blind Request Tunnelling Bypassing Access Controls via Request Tunnelling Browser-Powered Connection-Locked Desyncs Browser-Powered 0.CL Browser-Powered IP-Locked Desyncs Browser-Powered Request Splitting - HEAD + Range Browser-Powered Request Splitting - Stealing HTTPOnly Cookies Bypassing Response Header Removal Response Header Injection Cookie Tossing - TikTok XSS on a Redirect Reverse Desync Attacks Defence Tooling Further Research Key Takeaways Conclusion Research Origins Around 1 year ago, we came across this post on Bluesky which mentioned an attack technique we’d heard of, but never come across in the wild.
- Next, we’ll introduce novel methods to detect and exploit IP and connection-locked desyncs which prevent cross-network exploitation by shifting the desync’s execution into the victim's browser to generate an XSS out of thin air and steal HTTPOnly cookies.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
