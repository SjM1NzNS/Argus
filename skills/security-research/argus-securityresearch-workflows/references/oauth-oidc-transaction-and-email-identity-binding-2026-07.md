# OAuth/OIDC transaction and email-identity binding

Use this reference for weekly/deep-learning promotion or authorized source/local-fixture review involving OAuth/OIDC mix-up, code injection, account linking, mutable identity claims, email-domain gates, or API token-context confusion.

## Source basis

Prefer RFC 9700, RFC 9207, OpenID Connect Core, official OWASP guidance, and primary research. Use Preview.is only as Zone 0 corroboration under `external-rag-source-policy.md`; independently review the returned source and record wrapper/direct-retry outcomes without retaining credentials or full corpora.

## Workflow

1. Build a transaction-binding matrix instead of checking parameter presence: selected issuer and authorization/token/UserInfo endpoints, browser/session, client, exact redirect URI, state, PKCE method/challenge/verifier, nonce, code origin/use, token resource/audience, OIDC `(iss, sub)`, and resulting local account/tenant/role.
2. Gate authorization-server mix-up on a real multi-server client. Require exact response `iss`/ID Token issuer binding or a proven equivalent such as distinct redirect URIs plus retained issuer/endpoint state. Public metadata or multiple login buttons are not proof.
3. For code injection, use two owned transactions or an authorized local fixture. Cross one value at a time and verify code-to-client-instance binding through PKCE `S256`, exact redirect URI, one-time use, and validated OIDC nonce before tokens are consumed. Token-endpoint client authentication alone does not stop injection through the legitimate client.
4. Key OIDC accounts by `(iss, sub)`. Treat email, display name, preferred username, and phone as mutable attributes; `email_verified=true` proves point-in-time mailbox control, not global uniqueness or permanent organization membership.
5. Make account linking, provider migration, recovery, and tenant/role transitions explicit, authenticated, conflict-aware actions rather than automatic email-string merges.
6. For email-domain authorization, map provider claim -> app parser/canonicalizer -> stored value -> mailer/SMTP envelope recipient -> verification actor -> local account key -> organization/role/resource. Require the same intended mailbox/actor across all stages. Use source review, a local mail sink, or owned mailboxes only; do not import payload corpora or spray live address variants.
7. For API tokens, distinguish a different client ID from a wrong relied-on issuer/resource/audience/tenant context. Report only when the resource server accepts the crossed context and performs an unauthorized protected action.
8. Create eval scenarios that answer reportability, severity, missing proof, likely triage rejection, next action, and report/hold/discard. Include both positive and kill controls.
9. Patch all relevant OAuth/Auth/Access-Control playbooks plus the Web2 routing index and monthly changelog. Verify every index Markdown reference exists and is non-empty, new notes have no TODO/TBD/FIXME, eval labels are complete, and notes contain no assignment-like secrets.
10. Clear only exact reviewed daily/weekly raw and superseded compiler artifacts after verification. Stage exact paths under a unique `/tmp` directory, confirm sources are absent and unrelated/manual samples and logs remain, then delete the staging directory.

## Reportability gates

- **Report:** wrong issuer/endpoint acceptance with code/token or account impact; cross-transaction code injection with a realistic acquisition path; email-based cross-issuer merge/account recovery; parser/delivery split granting restricted organization/role/resource; or wrong token context accepted for protected action.
- **Hold:** source-only missing checks, parser differences without authorization impact, or code-injection hypotheses without acquisition/reachability.
- **Discard:** single-issuer no-ambiguity flow, effective PKCE/nonce rejection, profile-only email use, separate `(iss, sub)` accounts, same-mailbox verification, or wrong-context token denial.

Severity follows the resulting account, tenant, role, or protected-resource boundary—not missing parameters or syntax novelty.
