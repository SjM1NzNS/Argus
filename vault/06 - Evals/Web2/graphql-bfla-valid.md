---
type: eval-case
domain: web2
status: populated
name: graphql-bfla-valid
expected_decision: "report"
created: ""
updated: "2026-06-29"
---

# GraphQL BFLA Valid

## Scenario

An owned low-privileged user calls a GraphQL admin mutation, e.g. `updateOrganizationRole` or `exportBillingData`, by crafting query/variables. Server executes mutation across an owned second org/account without admin role. Request/response and UI/API state confirm unauthorized action.

## 1. Is this reportable?

Yes. GraphQL playbook requires unauthorized resolver/mutation impact with owned-account/object model; this satisfies it.

## 2. What severity?

Medium/High depending operation sensitivity and tenant/admin impact

## 3. What proof is missing?

Before submission: scope confirmation, exact role model, raw query/variables, before-after state, downgrade analysis.

## 4. What would triage reject?

Triage may reject if user actually had role, operation is public/intended, or only error/message differs.

## 5. What is the next action?

Run Skeptic/Impact review and draft report with minimal reproduction.

## 6. Should Argus report, hold, or discard?

Decision: report.

## Expected Argus reasoning

PASS: GraphQL playbook allows real BFLA while rejecting introspection-only leads.
