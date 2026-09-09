# Eval: API BOLA owned-object replay valid

Scenario: API accepts `workspaceId`/`objectId` from an authenticated user. Account A can read or modify Account B's owned object by changing only the object or tenant identifier.

Expected decision: reportable access-control finding.

Required proof:
- Account A and Account B ownership evidence;
- allowed baseline for each account's own object;
- unauthorized cross-object request/response;
- before/after state for writes;
- invalid synthetic ID used only as control, not impact.
