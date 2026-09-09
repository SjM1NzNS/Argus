# Federated identity account-linking CSRF validation

Use this reference for OpenID/OIDC/OAuth/SAML callbacks that can select an account-linking, attach-identity, merge-account, or sign-in mode.

## Core invariant

A valid identity-provider signature proves the provider authenticated the asserted external identity. It does **not** prove that the current relying-party browser session initiated or approved the account-linking operation.

Account linking must require an unpredictable, single-use, server-side intent bound to:

- the current authenticated relying-party session;
- the exact operation (`link`, not merely `login`);
- the expected provider/client and callback;
- a short lifetime;
- one-time consumption.

Do not accept callback-controlled `mode`, `action`, `link`, or equivalent fields as a substitute.

## Source-first trace

Trace these edges separately:

1. **Initiation:** route/query that chooses sign-in versus link mode.
2. **Provider request:** how mode and continuation data enter `redirect_uri`, `return_to`, `RelayState`, or provider state.
3. **Callback verification:** signature, issuer, audience/realm, nonce, redirect binding, and replay checks.
4. **RP intent verification:** whether callback state is bound to the victim's authenticated browser session and exact link operation.
5. **Security sink:** external-ID insertion, account merge, credential attachment, or account lookup.
6. **Fresh login:** whether the newly attached attacker identity resolves to the victim account after persistence.

A correct provider signature or nonce check can coexist with login CSRF when step 4 is absent.

## Minimum faithful local proof

Prefer a supported-path harness over manually constructed callback fields.

1. Pin the exact product and identity-library revisions.
2. Run a real loopback provider implementation supplied by the identity library or a protocol-faithful local provider.
3. Initiate discovery/association using a distinct attacker HTTP request object.
4. Have the provider generate the signed assertion; do not fabricate signature parameters.
5. Deliver the assertion using a distinct victim callback request under an authenticated victim session.
6. Preserve the application's deployed object lifetime. If the consumer/service is a process-wide singleton, use one singleton across browser requests; creating separate application consumers may introduce false negatives through association or RP-state differences.
7. Assert the exact sink arguments: victim account ID plus attacker external identity.
8. Persist through the real account/external-ID store when feasible.
9. Perform a fresh authentication using only the attacker identity and assert that it resolves to the victim account.
10. Replay the same assertion and assert rejection with no second link/login.

## Required controls

| Control | Purpose |
|---|---|
| Normal victim-owned link | Confirms the feature and harness work |
| Distinct attacker-initiation and victim-callback requests | Proves browser-session crossing |
| Real provider signature | Eliminates unsigned/mock-only callback objections |
| Wrong or tampered callback state | Confirms protocol/RP verification is active |
| Replay | Distinguishes first-use CSRF from replay weakness |
| Identity already linked | Defines uniqueness/conflict behavior |
| Restrictive provider allowlist/trust policy | Bounds affected configurations and permission impact |
| Fresh attacker authentication after persistence | Closes the ATO chain rather than stopping at a method call |

## Deployment and browser gates

Record, do not assume:

- which auth modes actually mount the callback in WAR, daemon, embedded, or clustered deployments;
- whether normal UI suppression leaves a directly reachable callback mounted;
- provider allowlist and identity trust semantics;
- SameSite setting and callback method (top-level GET under Lax differs from Strict or cross-site POST);
- nonce lifetime and user interaction;
- singleton/per-node association and RP-state storage, plus load-balancer affinity/shared-state behavior;
- whether the victim's resulting permissions are preserved, downgraded, or re-evaluated after linking.

Keep single-node or affinity proof separate from universal cluster claims.

## Reportability and severity

Separate four verdicts:

1. **Technical validity:** callback can attach attacker identity cross-session.
2. **Impact validity:** fresh attacker login reaches the victim account and concrete privileges/data.
3. **Asset eligibility:** repository/product is in the applicable program.
4. **Deployed proof:** a named production service exposes the affected callback/configuration.

An OSS repository can be reportable even when a specific hosted production deployment is not proven affected. Conversely, source-level exploitability does not prove a live service uses that auth mode.

Use conservative severity wording. Full victim permissions may depend on identity trust configuration; document ordinary-account and privileged-account bounds rather than assuming admin takeover.

## Evidence package

Retain:

- exact source and dependency commits;
- test patch including untracked new files (plain `git diff` omits them; use intent-to-add or append a no-index diff);
- uncached test log and JUnit XML;
- sink/persistence/fresh-login assertions;
- safe live route/config evidence, if any, with throttling or auth ambiguity preserved as `unknown`;
- SHA-256 manifests generated only after the final report edit;
- fresh-worktree `git apply --check` verification;
- distinct upstream/OSS-program/production-service dispositions.

## Common pitfalls

1. **Mock-only success.** A mocked `ConsumerManager.verify()` proves control flow, not protocol exploitability.
2. **One request called cross-session.** Use distinct attacker and victim HTTP request objects; explain dynamic session resolution.
3. **Separate application consumers used as browser sessions.** Browser sessions normally share the deployed singleton consumer. A new consumer can reject valid assertions for unrelated association/state reasons.
4. **Replay rejection treated as CSRF defense.** One-time nonces stop replay after first use, not first-use cross-session linking.
5. **Link sink treated as complete ATO.** Prove persistence and fresh authentication resolution.
6. **UI route absence treated as callback absence.** Verify module wiring for each deployment mode.
7. **Source finding treated as production proof.** Require live route/config evidence for the named service.
8. **Production no-go treated as program no-go.** Independently check repository/program tier and product-vulnerability scope before final routing.
9. **Untracked test omitted from reproduction patch.** Verify marker coverage and apply the patch to a clean worktree.
10. **Report edited after checksums.** Regenerate and verify manifests after the last wording change.
