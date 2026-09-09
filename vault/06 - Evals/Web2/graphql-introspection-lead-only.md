---
type: eval-case
domain: web2
status: populated
name: graphql-introspection-lead-only
expected_decision: "hold or discard"
created: ""
updated: "2026-06-29"
---

# GraphQL Introspection Lead Only

## Scenario

GraphQL introspection is enabled and reveals type/field names. No unauthorized resolver data, mutation, hidden operation abuse, or sensitive field values are reproduced.

## 1. Is this reportable?

Usually no. GraphQL playbook states introspection/schema visibility is a lead, not a finding by default.

## 2. What severity?

Informational/None unless policy accepts or impact is demonstrated

## 3. What proof is missing?

Unauthorized read/write/action, sensitive disclosure, exploitable hidden operation, or explicit program policy accepting introspection.

## 4. What would triage reject?

Triage rejects schema-only reports with no impact.

## 5. What is the next action?

Use schema to guide safe owned-account resolver tests; do not report yet.

## 6. Should Argus report, hold, or discard?

Decision: hold or discard.

## Expected Argus reasoning

PASS: GraphQL playbook correctly prevents schema-only overreporting.
