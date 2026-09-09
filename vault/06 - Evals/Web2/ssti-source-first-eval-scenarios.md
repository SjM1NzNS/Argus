---
title: SSTI Source-First Eval Scenarios
status: operational
---

# SSTI Source-First Eval Scenarios

## Scenario 1 — literal reflection

A profile preview returns `{{7*7}}` unchanged in HTML.

- Reportable: no.
- Missing proof: server-side evaluation and template-source data flow.
- Triage rejection: reflection is not SSTI.
- Next action: inspect source/context and use one controlled differential expression.
- Decision: discard unless new evaluation evidence appears.

## Scenario 2 — ambiguous arithmetic

A field containing an arithmetic-looking expression returns `49`, but the application has a calculator feature and engine identity is unknown.

- Reportable: not yet.
- Missing proof: template-engine causality, literal control, and second differential fingerprint.
- Triage rejection: business logic may calculate the value.
- Next action: compare fixed-template data binding and engine-specific differential behavior.
- Decision: hold.

## Scenario 3 — confirmed lower-trust template evaluation

An ordinary tenant user controls an email-template body. Baseline and literal controls differ from an inert expression, and source shows compile-from-string with the user's body.

- Reportable: primitive yes; final impact depends on reachable context and cross-user delivery.
- Missing proof: exact recipient/workflow boundary and safe context capability.
- Triage rejection risk: feature may be intentionally programmable.
- Next action: document intended grammar, use an owned recipient, and test an owned synthetic context variable.
- Decision: validate impact, then report or downgrade.

## Scenario 4 — scanner-only source path

CodeQL reports request data flowing to a render call, but a framework sanitizer converts the value to a constant template name before the sink.

- Reportable: no.
- Missing proof: actual unsanitized source-to-sink path.
- Triage rejection: false-positive framework model.
- Next action: inspect transforms and run the exact local route with controls.
- Decision: disproved if the constant-template control holds.

## Scenario 5 — sandboxed engine with context names

SSTI evaluation is proven and context-variable names can be listed, but no values or callable methods have been accessed.

- Reportable: evaluation may be reportable depending on actor/product contract; secret disclosure or RCE is not proven.
- Missing proof: concrete unauthorized capability and affected boundary.
- Triage rejection risk: names-only inventory and intentionally restricted templates.
- Next action: inspect source/version/policy and use only an owned synthetic context value.
- Decision: hold impact escalation.

## Scenario 6 — historical sandbox bypass

A public payload targets an older engine release; the application lockfile pins a patched version and the payload is inert.

- Reportable: no.
- Missing proof: affected current version/configuration.
- Triage rejection: version mismatch.
- Next action: preserve fixed-version negative evidence and close.
- Decision: discard.

## Scenario 7 — local owned file capability

The supported route is reachable by an ordinary user, compile-from-string is proven, and a loopback local clone reads a researcher-created temporary marker through an exposed helper. Production file access is not exercised.

- Reportable: likely, with conservative framing.
- Proven: lower-trust evaluation plus configuration-specific file capability in the released product path.
- Not proven: production secrets, arbitrary files, or RCE.
- Next action: verify release parity and report the actual capability/non-claims.
- Decision: report if program policy accepts OSS local proof.

## Scenario 8 — trusted administrator template feature

Only the host administrator can upload templates, documentation states templates are executable, and the process has no privilege beyond that administrator's intended capabilities.

- Reportable: usually no.
- Missing proof: lower-trust actor or incremental capability.
- Triage rejection: trusted programmable feature.
- Next action: check for lower-trust import/share/review paths; otherwise close.
- Decision: accepted behavior / actor-model hold.
