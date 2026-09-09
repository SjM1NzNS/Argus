---
type: learning-source-summary
reviewed_at: 2026-07-17
source_quality: 7
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# HackerOne Hacktivity — serializer and HTML-export XSS lessons

- Source: [HackerOne Hacktivity disclosed reports](https://hackerone.com/hacktivity/overview?queryString=disclosed%3Atrue&sortField=latest_disclosable_activity_at&sortDirection=DESC&pageIndex=0)
- Reviewed record: browser-rendered disclosed-report listing captured by `daily-20260717-073001`.
- Source limitation: the captured page contained HackerOne's automatically generated summaries, not full report bodies. It supports a class-level test reminder, not exact exploit reproduction or target-specific claims.

## High-signal summaries

1. **Rocket.Chat HTML export stored XSS:** unauthenticated LiveChat-originated content reportedly became executable JavaScript when a generated HTML export was opened. The useful lesson is that export templates and downloaded active artifacts are separate sinks from the application's live UI.
2. **Trix editor serialization sanitizer bypass:** the summary attributes execution to an unsafe interaction between custom DOMPurify configuration and `data-trix-serialized-attributes` during document serialization. The useful lesson is to test sanitizer/serializer/parser differentials across every representation boundary.

## Promoted methodology

- Trace input through editor/model state, sanitizer, custom serialized metadata, export generation, artifact bytes, and final browser-parsed DOM.
- Test live rendering and product-generated exports independently; preserve a negative control for the stage that remains safe.
- Require the ordinary product path to emit the executable structure. Hand-editing an artifact is not proof of a serializer/export flaw.
- Record attacker source, recipient/opening path, trust cues, interaction, and execution origin/context before assigning impact.
- Use harmless owned markers; do not use exfiltration or credential-phishing behavior from the generated summaries.

## Promotion decision

- Promoted to the XSS checklist, evidence requirements, false-positive gates, and focused eval scenarios.
- Kept exact vulnerability mechanics and severity bounded to the summary evidence; no claim is made beyond the disclosed listing.
