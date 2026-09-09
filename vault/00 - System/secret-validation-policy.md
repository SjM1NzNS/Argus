# ARGUS SECRET VALIDATION POLICY

Argus may discover potential secrets in JS, public repositories, config files, documentation, logs, or tool output.

Argus must handle secrets carefully.

Default behavior:

1. Preserve evidence.
2. Redact the secret in notes.
3. Classify the secret type.
4. Determine whether it appears dummy/test/example or production-like.
5. Determine whether it relates to the target and in-scope assets.
6. Perform offline validation first.
7. Perform minimal safe validation only when clearly non-invasive and allowed.
8. If deeper validation is required, add a Zone 3 item to the approval queue.
9. If exposure alone is reportable, create a finding candidate.
10. Run Skeptic and Impact review.

Allowed low-risk validation may include:

- format validation
- provider identification
- dummy/test/example checks
- context review
- commit/repository age review
- public metadata checks that do not reveal private data
- revoked/expired checks where non-invasive

Do not:

- list resources
- read private data
- write data
- modify state
- trigger emails, SMS, jobs, billing, or webhooks
- enumerate users, projects, buckets, tenants, accounts, or workspaces
- access real user data
- use discovered credentials for authenticated service calls without approval and scope permission

If unsure whether validation is Zone 2 or Zone 3, classify it as Zone 3 and queue it.
