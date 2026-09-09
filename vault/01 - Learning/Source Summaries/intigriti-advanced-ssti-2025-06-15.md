---
type: source-summary
source: https://www.intigriti.com/researchers/blog/hacking-tools/exploiting-server-side-template-injection-ssti
reviewed: "2026-07-23"
status: promoted
---

# Intigriti advanced SSTI guide — source summary

## Source

- Title: *SSTI: A complete guide to exploiting advanced server-side template injections*
- Author: BLACKBIRD-EU
- Published: 2025-06-15
- Reviewed directly in the browser on 2026-07-23.
- Preserved HTML: `01 - Learning/Inbox/manual-articles-20260723/intigriti-ssti.html`
- HTML SHA-256: `0bdeca4c56d8bf85bd2e55037e697993fe08cea9773014a9a9f4e7cdf4d5f693`

## High-signal lessons

1. SSTI begins when untrusted data becomes template source rather than a value supplied to a fixed template.
2. Detection, engine identification, and impact escalation are separate phases. Shared syntax requires differential fingerprinting.
3. Suppressed errors make broad error-character probing unreliable; deterministic evaluated-output controls are stronger.
4. Server-side and client-side template injection must be separated explicitly.
5. Sandboxes do not end analysis: custom globals, objects, filters, and methods define the real capability boundary.
6. Context enumeration and published payloads are leads, not permission to dump secrets, read arbitrary files, execute commands, or initiate callbacks.
7. Reports should distinguish the proven evaluation primitive from configuration- or context-dependent impact.

## Argus promotion

Created a dedicated SSTI playbook set covering source-first tracing, inert confirmation, engine fingerprinting, sandbox/context review, safe impact ladders, false positives, evidence, mitigation, and reportability. Added SSTI routing and eval scenarios.

The article's command/file/secret payloads were not copied into Argus. The promoted workflow uses canaries, local/owned environments, explicit approval gates, and minimal proof.
