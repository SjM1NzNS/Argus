---
type: eval-scenarios
status: active
created: "2026-07-28"
domain: web2
source_basis:
  - "RFC 9700"
  - "RFC 9207"
  - "OpenID Connect Core 1.0"
  - "PortSwigger OAuth guidance"
  - "PortSwigger Research: Splitting the email atom"
---

# OAuth/OIDC identity-binding eval scenarios — weekly 2026-07-28

## Scenario 1 — single issuer, missing authorization-response `iss`

An application supports one statically configured authorization server. Its callback has no RFC 9207 `iss` parameter, but the server-side transaction fixes the endpoint tuple, PKCE `S256` and OIDC nonce mismatches are rejected, and no other issuer is usable.

- **Reportable:** no.
- **Severity:** none.
- **Missing proof:** a second usable authorization server and a crossed response accepted under the wrong issuer/endpoint transaction.
- **Likely triage rejection:** parameter absence without a mix-up precondition or impact.
- **Next action:** preserve the PKCE/nonce rejection controls; do not invent a second issuer.
- **Decision:** discard as a finding.

## Scenario 2 — multi-issuer mix-up crosses the token endpoint

An authorized local fixture supports an honest and an attacker-controlled test issuer. The client starts with one issuer, accepts the other's response without exact issuer binding, and sends the owned honest authorization code to the wrong token endpoint. A distinct-redirect-URI control prevents the crossing after remediation.

- **Reportable:** yes as a strong candidate when the supported configuration and attacker issuer precondition are realistic.
- **Severity:** High if the code/token yields victim identity or protected resources; otherwise Medium pending impact.
- **Missing proof:** for a live report, exact deployment reachability, code acquisition/use, and owned account/session impact.
- **Likely triage rejection:** synthetic malicious provider with no supported registration/configuration path, or code exposure without usable impact.
- **Next action:** prove the real provider-selection path and smallest owned identity/resource impact; retain exact issuer/endpoint and redirect-URI controls.
- **Decision:** report only after reachable configuration and impact; otherwise hold.

## Scenario 3 — authorization-code substitution rejected by PKCE

Two owned browser transactions use fresh PKCE `S256` verifiers. A code from transaction A is substituted into transaction B; the token endpoint rejects B's verifier, no token is used, and replay also fails.

- **Reportable:** no.
- **Severity:** none.
- **Missing proof:** acceptance of the crossed code or another code-to-client-instance binding failure.
- **Likely triage rejection:** visible/missing `state` is over-weighted despite an effective injection control.
- **Next action:** record wrong/missing/cross-verifier rejection and close the branch.
- **Decision:** discard; PKCE is an effective negative control.

## Scenario 4 — code injection creates the wrong owned identity session

A confidential web client authenticates correctly at the token endpoint but does not use transaction-bound PKCE or a validated OIDC nonce. A code acquired from owned victim transaction A is accepted in attacker transaction B and B receives a session mapped to A's identity.

- **Reportable:** yes if a realistic attacker code-acquisition path exists.
- **Severity:** High for victim account takeover; Medium if the only effect is constrained session/account confusion.
- **Missing proof:** how the attacker obtains a usable code before redemption, one-time-use behavior, and final unauthorized capability.
- **Likely triage rejection:** assuming client authentication prevents injection, or using a researcher-created code path with no real acquisition route.
- **Next action:** establish acquisition, crossed transaction matrix, before/after identity, and one protected owned action; stop there.
- **Decision:** report after acquisition and impact gates; otherwise hold.

## Scenario 5 — same email, separate `(iss, sub)` accounts

Two providers return the same owned email string. The application keys users by `(iss, sub)`, creates separate accounts, marks email as a mutable profile attribute, and requires explicit reauthentication to link them.

- **Reportable:** no.
- **Severity:** none.
- **Missing proof:** an unintended merge, recovery, role, tenant, or authorization result.
- **Likely triage rejection:** treating equal email text as an account collision when the authoritative keys remain separate.
- **Next action:** keep the explicit-link negative control and close.
- **Decision:** discard as not vulnerable.

## Scenario 6 — cross-issuer email auto-merge

A local fixture shows that the relying party ignores issuer/subject and selects an existing account solely by email. A second owned provider identity with the same unverified or attacker-controlled email is silently merged into the first account and receives its privileges.

- **Reportable:** yes.
- **Severity:** High for account takeover or privileged tenant access; otherwise follows the merged account's capability.
- **Missing proof:** provider claim provenance/verification semantics, actual local lookup key, conflict/linking path, and final owned account capability.
- **Likely triage rejection:** email is actually verified under authoritative provider policy, linking requires current-user reauthentication, or the source-only branch has no reachable collision.
- **Next action:** preserve both `(iss, sub)` pairs, email-verification semantics, local-account mapping, session before/after, and one minimal protected action.
- **Decision:** report when the owned collision is reproduced; source-only logic remains hold.

## Scenario 7 — unusual email syntax but same mailbox controls verification

A domain-restricted signup accepts an unusual address representation. The same canonical allowed-domain mailbox receives and completes verification; a conventional disallowed-domain control is denied and no external actor can obtain organization access.

- **Reportable:** no.
- **Severity:** none.
- **Missing proof:** a parser/delivery split controlled by an unauthorized actor and a restricted authorization result.
- **Likely triage rejection:** syntax novelty or parser difference without boundary impact.
- **Next action:** record app-parsed domain, stored value, envelope recipient, and same-mailbox control; close.
- **Decision:** discard.

## Scenario 8 — email parser/delivery split grants organization access

In an authorized local mail-sink fixture, the application authorizes an allowlisted domain from one parse while the mail component sends verification to a different owned attacker mailbox. Completing that verification creates membership in a restricted test organization and permits one synthetic protected-resource read. No raw exploit string is retained in the playbook.

- **Reportable:** yes when the same supported production code path is reachable in scope.
- **Severity:** High for restricted enterprise/tenant or sensitive data access; Medium for low-impact restricted registration.
- **Missing proof:** exact parser chain, actual envelope recipient/controller, same-fixture allowed and disallowed controls, and final role/resource effect.
- **Likely triage rejection:** only library fingerprinting, a historical patched vector, or verification that still reaches the intended allowed-domain mailbox.
- **Next action:** produce the redacted divergence ledger and smallest protected outcome, then stop.
- **Decision:** report after code-path and impact gates; otherwise hold.

## Scenario 9 — token for another context is rejected by the API

A structurally valid owned token from a different protected resource or tenant is sent to the API. The API validates issuer plus the context it relies on and denies access before data or state change.

- **Reportable:** no.
- **Severity:** none.
- **Missing proof:** acceptance under a wrong relied-on audience/resource/tenant/security context and unauthorized protected impact.
- **Likely triage rejection:** a different OAuth client ID alone is not proof that the token is invalid for the same resource.
- **Next action:** retain the denied wrong-context and successful correct-context controls; close.
- **Decision:** discard.

## Scenario 10 — first-use signed link response is accepted in another session

An authorized local fixture has two owned browser contexts. The attacker context starts an account-link flow for its own allowed provider identity and obtains a fresh, valid first-use response. The relying party validates the provider signature, signed return target, and nonce, but takes the target local account from the different authenticated victim context that receives the callback. The identity persists and a fresh authentication resolves to the victim account. Mode tampering and exact replay are rejected.

- **Reportable:** yes.
- **Severity:** High when the added identity becomes a durable login method with the victim's effective sensitive permissions; otherwise follow the proven account capability.
- **Missing proof:** affected configuration, realistic fresh-response acquisition, callback method/cookie delivery, durable mapping, and fresh-auth account result.
- **Likely triage rejection:** reporting unsigned parameter tampering, nonce replay, or an attacker-to-attacker link instead of the first unused cross-session splice.
- **Next action:** preserve the initiator/receiver matrix, exact library freshness window, GET/POST cookie evidence, persistence, and fresh-auth result; stop after the smallest owned impact.
- **Decision:** report after those gates; a source-level OSS candidate may proceed with browser delivery clearly labeled as an assumption.

## Scenario 11 — only stale and replayed link responses are rejected

A candidate shows a missing-looking session state parameter, but the only tested provider responses are older than the library's effective age limit or already consumed. All are rejected. No timely first-use response, just-in-time local provider path, or victim cookie delivery is established.

- **Reportable:** not yet.
- **Severity:** none pending a realistic first-use path.
- **Missing proof:** fresh acquisition, wrong-session first use, actual callback transport/cookie, and durable account effect.
- **Likely triage rejection:** assuming that parameter absence alone defeats freshness/replay checks or that an expired captured response remains usable.
- **Next action:** measure the exact library/configured window and test one fresh first-use owned transaction. If no realistic acquisition/delivery path exists, close.
- **Decision:** hold, then discard if the first-use path cannot be established.

## Scenario 12 — compositional source proof is mislabeled browser end-to-end

Source review proves a missing initiator binding. One component test verifies a real provider-signed callback against a mocked link sink; a separate acceptance test proves that direct linking persists and fresh account-manager authentication resolves to the victim. No real servlet routing, cookie jar, callback GET/POST, redirect chain, or full provider login is exercised.

- **Reportable:** potentially yes for an eligible OSS/source program when the source bridge, affected stock configuration, and durable impact are strong.
- **Severity:** follows proven impact and disclosed prerequisites; do not lower solely because the proof is compositional, and do not raise based on an untested browser path.
- **Missing proof:** browser/HTTP delivery and one uninterrupted callback-to-persistence-to-fresh-login run.
- **Likely triage rejection:** calling this a browser end-to-end or demonstrated one-click takeover.
- **Next action:** label artifacts `source-traced` and `component`; state browser delivery assumptions. Add a two-cookie-jar HTTP/browser test if feasible.
- **Decision:** report conservatively when source and durable impact gates are met; hold only the unsupported browser-level wording.
