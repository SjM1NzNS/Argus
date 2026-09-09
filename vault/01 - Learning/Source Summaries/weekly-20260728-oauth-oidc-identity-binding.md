---
type: source-summary
status: promoted
created: "2026-07-28"
domain: web2
topics: [oauth, oidc, authentication, authorization, account-linking, email, api-security]
---

# Weekly promotion — OAuth/OIDC transaction, identity, and email-domain binding

## Sources reviewed

- [RFC 9700 — Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700): multi-authorization-server mix-up defenses, exact redirect-URI handling, PKCE, authorization-code injection, nonce checks, and access-token audience restriction.
- [RFC 9207 — OAuth 2.0 Authorization Server Issuer Identification](https://www.rfc-editor.org/rfc/rfc9207): exact authorization-response `iss` validation and rejection behavior.
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html): ID Token/nonce validation, `email_verified` semantics, and Section 5.7's stable identity key `(iss, sub)`.
- [OWASP OAuth 2.0 Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html): practical BCP-aligned defensive summary.
- [PortSwigger Web Security Academy — OAuth 2.0 authentication vulnerabilities](https://portswigger.net/web-security/oauth): practical account-linking, CSRF, redirect, scope, and unverified-provider-email impact framing.
- [PortSwigger Research — Splitting the email atom](https://portswigger.net/research/splitting-the-email-atom): parser/delivery discrepancies where a validated textual domain and the actual verification mailbox diverge.

Raw reviewed files were held temporarily under `01 - Learning/Inbox/weekly-20260728-oauth-oidc-binding/` and cleared only after promotion verification.

## Preview.is RAG outcome

Two exact technique lookups were run under the external-RAG policy. The durable reviewed output came from one direct API call per query. The email-parser wrapper attempt timed out and its single direct retry succeeded; the earlier OAuth wrapper output was not relied on for any promoted claim.

- OAuth/OIDC issuer mix-up/account-linking query: [RFC 9207](https://www.rfc-editor.org/rfc/rfc9207) was the strongest on-topic result (`0.9904`).
- Email parser/domain-authorization query: [Splitting the email atom](https://portswigger.net/research/splitting-the-email-atom) was a strong on-topic result (`0.9463`).

The direct sources were independently reviewed. No unique claim was promoted from lower-ranked secondary RAG matches, and no retrieved corpus or credential was copied into the vault.

## Promoted methodology

1. Replace parameter-presence checks with a transaction-binding matrix: selected issuer and endpoint tuple, browser/session, client, exact redirect URI, state, PKCE, nonce, code, token resource/audience, `(iss, sub)`, and final account/tenant/role.
2. Gate mix-up findings on a real multi-authorization-server client and exact crossed-issuer behavior. Validate RFC 9207 `iss` by exact string comparison when supported; distinct redirect URIs plus retained issuer/endpoint state can be an equivalent negative control.
3. Treat authorization-code injection separately from token-endpoint client authentication. Use two owned transactions and prove or kill code-to-client-instance binding with PKCE `S256`, exact redirect URI, one-time use, and—where OIDC is used—validated nonce before any token is consumed.
4. Use `(iss, sub)` as the OIDC account key. Email, phone, display name, and preferred username are mutable attributes; `email_verified=true` is point-in-time mailbox-control evidence, not global identity uniqueness.
5. Make account linking, provider migration, and recovery explicit authenticated transitions with conflict handling; never silently merge identities only because email strings match.
6. Add the same-mailbox invariant for domain-gated access: the IdP claim, application parser/canonicalizer, stored address, mailer's envelope recipient, verifier, and final organization/role decision must identify the same intended actor.
7. Promote parser-differential classes only as source-first/local-fixture hypotheses. No encoded payload corpus or live spray procedure was imported.
8. Separate token structure from authorization context. A different client ID alone may be legitimate; report only when the API accepts a token outside a relied-on issuer/resource/audience/tenant context and performs an unauthorized action.
9. Add explicit false-positive gates for single-issuer flows, effective PKCE/nonce rejection, profile-only email use, separately keyed issuer subjects, same-mailbox verification, and wrong-context token rejection.
10. Tie severity to owned account, enterprise/tenant, role, or protected-API impact—not missing parameters or parser novelty.

## Rejected or qualified material

- Missing `iss`, PKCE, `nonce`, or `state` is not independently reportable when another correct binding blocks the attacker path and no owned impact survives.
- Multiple IdP buttons or public metadata do not establish mix-up.
- `email_verified=true` does not justify cross-provider account merging, while an unverified email claim is not a finding unless the application trusts it across a security boundary.
- The PortSwigger article's broad warning against domain authorization was converted into evidence-gated Argus guidance: authoritative issuer-specific tenant/group claims can be valid, and mailbox-based gates require proof of a real parser/delivery/authorization split.
- Payloads, automated address-variant spraying, third-party-domain tests, live IdP abuse, token retention, and target interaction were not adopted.

## Daily-run review

The preceding daily run (`daily-20260728-073001`) produced 218 canonical combined records but only 9 `actual_content` records (`4.1%`). Manual review found its compiler summaries generic, duplicated, off-lane, or classifier-noise, so none were promoted directly. One discovery-only PortSwigger URL was reacquired as substantial source-native content, independently reviewed in this weekly run, and promoted under the stronger workflow above. The durable rejection decision is recorded in `01 - Learning/Rejected Lessons/daily-20260728-073001-manual-review.md`.

## Hunt relevance

- **Google:** prioritize source review of OSS OAuth/OIDC clients, callback/transaction stores, account lookup/linking code, and API audience/resource checks. A local fixture can safely prove exact issuer, code, and identity binding before any program-specific validation.
- **authorized program:** corporate SSO/admin portals make issuer/subject keys, email-domain organization gates, and provider claim semantics especially relevant. Public corporate IdP metadata remains context only; any future validation requires an in-scope app, an owned entitled account/mailbox, and no third-party IdP testing.
- **Both:** the fastest kill test is to trace what actually selects the local account/tenant and identify whether every issuer, code, token, email, and verification stage remains bound to that same transaction and actor.

## Files promoted

- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/overview.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/reportability.md`
- `02 - Vulnerability Playbooks/Web2/Authentication & Session/email-identity-and-domain-authorization.md`
- `06 - Evals/Web2/oauth-oidc-identity-binding-weekly-20260728.md`
- `00 - System/web2-skill-index.md`
- `07 - Skill Changelog/2026-07.md`
