# ARGUS SCOPE POLICY

Scope controls all target activity.

## Required before live work

For every program or target, create `scope.md` and `scope-contract.yaml` under `03 - Targets/<Program Name>/` or the project-specific target folder. Extract allowed assets, forbidden assets, allowed testing, forbidden testing, rate limits, account model, required approvals, explicit out-of-scope issue classes, and report requirements.

## Scope decision rules

- If an asset is not clearly in scope, treat it as out of scope.
- If testing is not clearly allowed, queue approval before running it.
- If a third-party service appears in the path, stop and classify whether it is explicitly in scope.
- If validation would access real user data, trigger notifications, alter state, or enumerate private resources, classify it as Zone 3.
- Preserve the exact scope source and timestamp used for decisions.

## Revalidation

Re-check scope before Zone 2 or Zone 3 activity, before report drafting, and whenever a target redirects to a new domain, tenant, integration, mobile/API host, contract, bridge, or cloud account.
