---
type: eval-scenarios
domain: web2
status: populated
created: "2026-07-10"
source_basis:
  - "daily-20260710 lightweight review"
  - "https://chs.us/guides/idor/"
---

# Access Control Variant Surface Eval Scenarios

These scenarios verify that Argus treats parser/protocol/route variants as useful access-control leads without over-reporting them before owned-boundary proof exists.

## Scenario 1 — duplicate body ID reaches another owned object

A normal owner request is `PATCH /api/projects/proj_A/task` with JSON `{ "task_id": "task_A", "title": "x" }`. Account B owns `task_B`. Account A sends one controlled variant with duplicate task selectors where the server applies `task_B` during authorization but updates `task_B` using Account A's session. Before/after reads by Account B show the owned task changed.

- Reportable: Yes, if all objects/accounts are owned and the raw request proves duplicate-selector parser precedence.
- Severity: Medium by default; higher only if the same primitive reaches tenant/admin/business-critical actions.
- Missing proof: canonical route baseline, Account B ownership proof, raw duplicate-ID request, post-change verification, rollback note.
- Triage rejection reason: would be rejected if the response is only `200` with no unauthorized state change or if `task_B` is attacker-owned/public.
- Next action: preserve request/response pairs and run false-positive review.
- Decision: report after scope and impact review.

## Scenario 2 — method/content-type variant accepted but no boundary crossed

A tester changes `GET /api/users/me/export` to `POST /api/users/123/export` and switches JSON to form encoding. The API returns `202 queued`, but the generated export belongs to the tester's own account and no second owned account receives or exposes data.

- Reportable: No.
- Severity: None / informational lead only.
- Missing proof: second owned account/object, unauthorized export content or delivery, and evidence that authorization used the wrong identity/context.
- Triage rejection reason: parser or method variance alone is not impact.
- Next action: hold only if a safe owned two-account export matrix is available; otherwise discard.
- Decision: discard as finding.

## Scenario 3 — alias/context selector crosses workspace boundary

Two owned accounts are in separate workspaces. A source-derived mobile route accepts `X-Workspace-ID` plus the path alias `/api/current/invoices/latest`. Account A sets the header to Account B's owned workspace and receives B's latest invoice details, while Account A's normal `current` request returns its own invoice.

- Reportable: Yes, if workspace membership and invoice ownership are proven with owned accounts.
- Severity: Medium; consider High only for broad tenant-wide or sensitive financial/business exposure.
- Missing proof: selector-resolution notes for `current`, Account A/B baselines, minimal header-only delta, and impact statement.
- Triage rejection reason: downgrade if the invoice was shared, public, test-only, or the account relationship permits access.
- Next action: capture clean evidence and document false-positive gates.
- Decision: report if scope allows this class.

## Scenario 4 — second-order notification IDOR without downstream evidence

Account A submits an approval request with `recipient_user_id` changed to Account B's owned user ID. The response says `200 notification scheduled`, but Account B does not receive a notification and no audit/event/readback confirms cross-account delivery.

- Reportable: No.
- Severity: None until downstream effect exists.
- Missing proof: observable effect in B's owned account, message contents, unauthorized action, or state transition.
- Triage rejection reason: accepted queue/scheduled responses are leads, not evidence.
- Next action: if safe, observe only owned downstream channels; do not enumerate real recipients.
- Decision: hold as lead or discard if no effect appears.
