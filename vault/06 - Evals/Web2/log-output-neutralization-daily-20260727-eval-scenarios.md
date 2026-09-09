---
type: eval-scenarios
status: active
created: "2026-07-27"
source_basis:
  - "HackerOne Hacktivity platform-generated Monero log-injection summary"
  - "CWE-117 Improper Output Neutralization for Logs"
  - "Preview.is RAG corroboration reviewed 2026-07-27"
---

# Log output-neutralization eval scenarios

## Scenario 1 — attacker input becomes a second trusted audit record

A remotely reachable request field is written before semantic rejection. A minimal inert delimiter canary is stored by the real collector as two records, and the second record can set a trusted-looking actor, action, timestamp, or status field consumed by operators.

- **Reportable:** Yes, after proving the attacker path and trusted record boundary.
- **Severity:** Low candidate for operator confusion alone; Medium candidate if a real audit, alert, attribution, or response decision is corrupted.
- **Missing proof:** Ordinary/escaped controls, raw emitted bytes, collector event count/fields, viewer/query result, affected operator or automation, and incremental capability.
- **Triage rejection risk:** A terminal line wrap or application string is presented without collector evidence or a relied-upon trust distinction.
- **Next action:** Reproduce only in an owned/local log lane and preserve one-record versus two-record controls.
- **Decision:** HOLD until the real consumer and impact are proven; REPORT when the trusted record boundary is demonstrably corrupted.

## Scenario 2 — structured logger preserves one escaped field

The same delimiter canary appears on multiple visual lines in a terminal, but the structured logger and collector retain one event with an escaped string field. Searches, alerts, and audit views do not interpret a second actor, action, timestamp, or event.

- **Reportable:** No.
- **Severity:** None.
- **Missing proof:** None if raw/collector controls confirm one event and no consumer confusion.
- **Triage rejection reason:** Visual formatting did not corrupt a trusted record or decision.
- **Next action:** Preserve as the safe negative control.
- **Decision:** DISCARD.

## Scenario 3 — pre-validation logging without sink proof

Source shows that an RPC or API path logs the raw request before semantic validation, but runtime output is unavailable and the deployed logger/collector escaping behavior is unknown.

- **Reportable:** Not yet.
- **Severity:** Unrated lead.
- **Missing proof:** Attacker reachability, exact decoded value, emitted bytes, collector behavior, and a corrupted field/event or downstream effect.
- **Triage rejection reason:** Call order and source concatenation alone do not prove log injection.
- **Next action:** Build a local or owned fixture using the exact logger/serialization path and compare ordinary, delimiter, and escaped controls.
- **Decision:** HOLD.

## Scenario 4 — forged text is claimed to execute in a downstream consumer

A forged-looking log line is created, and the report claims command execution, template injection, XSS, or AI-agent action because another system may process logs. The actual consumer has not parsed or acted on the canary.

- **Reportable:** Only the proven log-integrity primitive, if that primitive independently passes its impact gate.
- **Severity:** Do not escalate for the hypothetical consumer.
- **Missing proof:** Exact consumer, parser/input path, active sink, harmless end-to-end canary, authorization context, and negative controls.
- **Triage rejection reason:** Potential composition is presented as demonstrated impact.
- **Next action:** Route the consumer to its specialized playbook and validate it separately in an owned/local lane.
- **Decision:** HOLD the chain; REPORT only the evidence-backed primitive.
