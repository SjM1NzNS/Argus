# ARGUS EVIDENCE POLICY

Evidence must be reproducible, scoped, minimal, and triage-resistant.

## Required evidence fields

- Scope source and in-scope asset confirmation.
- Attacker model and account/object ownership.
- Expected secure behavior.
- Actual observed behavior.
- Request/response, transaction, UI, code, log, or local PoC proof as appropriate.
- Minimal changed variable between control and test.
- Impact tied to confidentiality, integrity, availability, authorization, financial loss, protocol loss, or business process abuse.
- Strongest invalidity argument.
- Strongest downgrade argument.
- Missing evidence and safe next step.

## Evidence handling

Store raw sensitive evidence only under `09 - Raw Evidence` or the target evidence folder with restrictive permissions. Redact secrets and private data in notes and report drafts. Do not include unrelated personal files, browser profiles, SSH keys, cookies, credential stores, or out-of-scope artifacts.

## Reportability rule

A reportable finding must survive scope review, false-positive review, impact review, and severity downgrade review. Leads and hypotheses are useful, but they are not vulnerabilities until evidence proves the claim.
