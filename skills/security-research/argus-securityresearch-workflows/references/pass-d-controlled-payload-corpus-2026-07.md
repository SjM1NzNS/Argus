---
type: skill-reference
status: active
created: "2026-07-07"
---

# Pass D Controlled Payload Corpus Promotion Pattern

Use this reference when importing or using large payload corpora such as PayloadsAllTheThings.

## Source

- `swisskyrepo/PayloadsAllTheThings`

## Promotion rules

1. Fetch selected high-signal README/methodology sections into `01 - Learning/Inbox/<run-label>/`; do not mirror the repository or bulk import payload lists.
2. Create source summary and system review notes documenting selected sections and do-not-promote content.
3. Promote a class-level controlled payload guidance note, not raw payload dumps.
4. Patch relevant playbooks with context-first payload selection gates.
5. Update `web2-skill-index.md` with a payload-corpus routing section and the controlled guidance note.
6. Add eval scenarios that reject spraying, exfiltration, internal probing, and taxonomy/payload-only reportability.
7. Verify all touched files are non-empty, no placeholders remain, and index `Load:` references exist.

## Core rule

Do not begin with a payload list. Begin with:

```text
source/input → parser/normalizer → sink/behavior → boundary/impact
```

Then select the smallest harmless payload shape that proves the specific context.

## Safety gates

Remove or avoid payload behavior involving credential theft, keylogging, token exfiltration, shell/RCE, malware, parser bombs, destructive writes, real-user interaction, third-party callbacks, cloud metadata/internal probing, or broad fuzzing unless explicit scope and approval permit that exact validation step.

## Reportability rule

A payload firing is not a finding by itself. The finding must satisfy the relevant Argus class playbook: unauthorized data/action, cross-account/tenant impact, token/session/code impact, sensitive cache/browser effect, server-side fetch boundary, parser side effect, or program-accepted impact.
