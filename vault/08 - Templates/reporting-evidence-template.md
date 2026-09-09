---
type: template
status: active
created: "2026-07-02"
source_basis:
  - "Legacy Cybersecurity V3: _Operations/Methodology/09 Reporting Evidence Template.md"
---

# Reporting Evidence Template

A good report makes triage boring. Boring is good.

## Pre-submit checklist

- [ ] Summary and business/security impact are clear.
- [ ] Affected asset, endpoint, parameter, account role, and object ID model are identified.
- [ ] Preconditions and owned accounts/objects used are stated.
- [ ] Exact reproduction steps are deterministic and minimal.
- [ ] Raw request/response evidence is included and redacted.
- [ ] Positive and negative controls are included.
- [ ] Scope and program policy fit are explicit.
- [ ] Cleanup/safety notes are included.
- [ ] Severity is justified by demonstrated impact, not only the primitive class.

## Report skeleton

```markdown
# Summary

# Affected asset

# Preconditions

# Account / object model

# Reproduction steps
1.
2.
3.

# Evidence
## Positive control
- Request:
- Response:

## Variant / exploit request
- Request:
- Response:

## Negative control
- Request:
- Response:

# Impact

# Scope and safety notes

# Remediation guidance
```

## Evidence-quality notes

- For access-control and GraphQL findings, include same-user allowed, low-priv denied, and vulnerable allowed/forbidden contrast where possible.
- For crypto/nonce findings, prefer algebraic evidence over claims: e.g., repeated nonce, ciphertext XOR behavior, known-prefix recovery path, and exploit preconditions.
- For XSS/client-side findings, show source-to-sink and a harmless impact proof such as same-origin token read or owned-account state-change capability.
- For SSRF, separate callback-only proof from internal/metadata/data-exfiltration impact.
- For file uploads, show the processing/rendering/download context and why it crosses a trust boundary.
