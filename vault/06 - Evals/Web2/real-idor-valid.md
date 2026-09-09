---
type: eval-case
domain: web2
status: populated
name: real-idor-valid
expected_decision: "report"
created: ""
updated: "2026-06-29"
---

# Real IDOR Valid

## Scenario

Two owned accounts exist in separate organizations. Account A captures `GET /api/invoices/inv_B` by replacing its invoice ID with Account B owned invoice ID. Server returns Account B invoice details including billing email, amount, address, and PDF URL. Same request as Account B proves ownership. No broad enumeration or real user data is used.

## 1. Is this reportable?

Yes. The Access Control playbook requirements are satisfied: in-scope asset, owned accounts, minimal request delta, server-side enforcement failure, unauthorized read, and clear impact.

## 2. What severity?

Medium, possibly High if tenant-wide sensitive data or admin/business impact is shown

## 3. What proof is missing?

Before submission, capture clean request/response pairs, scope contract excerpt, and downgrade analysis. For High, prove broader tenant/admin/financial impact beyond one invoice.

## 4. What would triage reject?

Triage might downgrade if data is low sensitivity, asset is public/shared, or only one object is affected.

## 5. What is the next action?

Run Skeptic and Impact review, then draft report if scope confirms this class.

## 6. Should Argus report, hold, or discard?

Decision: report.

## Expected Argus reasoning

The playbook allows valid evidence-backed IDOR while preventing unsupported severity escalation.
