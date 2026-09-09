# Federated identity-linking report finalization

Use this reference when reviewing or packaging OAuth, OIDC, SAML, or OpenID account-linking findings whose callback may execute under a different browser session or account than the initiator.

## Security invariant

A provider-valid response is not sufficient authorization to mutate an account. A link callback must be bound to a pending, authenticated, single-use transaction containing at least:

- initiating browser session;
- initiating account;
- intended operation (link, sign-in, registration, reauthentication);
- expected provider and external identity constraints;
- expiration and atomic consumption state.

Provider signatures protect response integrity. Nonces normally provide freshness/replay resistance. Neither proves that the browser/account receiving the callback initiated the linking transaction.

## Required proof decomposition

Keep these layers separate in notes and reports:

1. **Source-level defect:** where initiation, callback reconstruction, current-session lookup, and identity mutation occur.
2. **Attacker prerequisites:** accepted provider/identity, unused external ID, reachability, configured domain/PAPE/email/trust constraints, and cluster association state.
3. **Executed component behavior:** exact real and mocked boundaries in each test.
4. **Browser delivery mechanism:** HTTP method, redirect chain, cookie policy, and whether a real browser/cookie jar exercised them.
5. **Persistence and subsequent authentication:** durable external-ID write and a fresh authentication resolving to the victim account.
6. **Impact:** only the victim account's effective permissions; do not infer administrator access or unrelated privilege escalation.

Call the result **browser end-to-end** only when one execution covers the exact provider interaction, callback method, redirects, cookies, victim session, persistent mutation, and later attacker login. Otherwise use **source-traced component** or **compositional** proof.

## Freshness and provider timing

1. Pin the relying party and federated library versions.
2. Inspect the checksum-pinned library source, not only documentation, for the effective nonce/timestamp verifier and default age.
3. Record the exact source artifact checksum and the code that applies the age boundary.
4. Demonstrate a fresh, first-use callback. Keep stale and exact-replay rejection as negative controls only.
5. If policy permits an attacker-controlled provider, model a just-in-time response: retain the legitimate RP request, mint a fresh signed assertion when the victim interacts, and redirect immediately.
6. Treat a pre-generated response from an ordinary provider as a separate, timing-constrained variant. Do not give both variants the same practicality claim without evidence.

## Browser and cookie boundary

- Identify the callback servlet's accepted methods from source.
- Match the claimed delivery to the tested method. Default-Lax cookies may accompany top-level GET navigation but generally not a cross-site POST/form.
- Account for explicit `SameSite=Strict`, custom domains, redirect hops, secure-cookie requirements, and proxy rewrites.
- If no real browser/cookie jar ran the chain, describe delivery as source-derived and disclose it as an assumption.

### HTTP/browser-equivalent acceptance-test pattern

When triage asks for one deterministic end-to-end reproduction, prefer a daemon-level HTTP acceptance test over another mocked service test:

1. Start the real local application daemon and a loopback protocol provider that performs actual discovery, association, and signed response generation.
2. Use three independent cookie stores: an authenticated victim, an anonymous attacker initiator, and a fresh post-link attacker login.
3. Traverse the production initiation, callback, and authenticated self-lookup routes. If the relying party emits an auto-submit HTML form, parse and submit it so the harness follows the same HTTP method and parameters as a JavaScript-capable browser.
4. Assert the attacker initiator has no application session, the callback receiver has the victim session, the external-ID mapping is absent before callback and points to the victim after callback, and the fresh attacker login's self endpoint returns the victim account.
5. Keep the provider response fresh and first-use; capture it immediately before callback delivery rather than replaying a stored old response.

An ordinary HTTP cookie store does not implement browser `SameSite` enforcement or prove a cross-origin top-level navigation. Label this proof **HTTP/browser-equivalent end-to-end**, not full browser end-to-end, unless a real browser also exercises those semantics. Preserve `SameSite=Strict` and related delivery constraints as explicit caveats.

## Minimum controls

- Initiation succeeds without consulting an authenticated user only if that is the claimed defect; make the test fail if an initiator user is unexpectedly accessed.
- A real provider-signed first-use assertion reaches the intended link sink under a distinct receiver user context.
- Post-signing mode/state tampering is rejected before mutation.
- Exact replay is rejected and performs no second mutation/login.
- Stale responses are rejected when the library enforces age.
- Cross-session/account mismatch is rejected by the proposed fix.
- No account mutation occurs before transaction validation and atomic consumption.
- A real persistence layer records the external ID.
- A fresh authentication by only that external ID resolves to the expected account.

## Evidence packaging workflow

1. Keep production source unchanged when the artifact is only a reproduction patch; make the test-only scope explicit.
2. Format changed source and run `git diff --check`.
3. Run focused controls uncached, then complete affected test targets uncached.
4. Parse JUnit XML and report cases, failures, errors, and skipped counts separately.
5. Regenerate the patch from the exact tested tree and compare it byte-for-byte.
6. Apply it in a detached clean worktree at the pinned commit.
7. Initialize pinned submodules before building (`git submodule update --init --recursive` or the minimal required submodule set).
8. Record `CLEAN_HEAD`, submodule SHAs, `TEST_CWD`, patch SHA-256, and clean-apply success in the replay log. This prevents a harness from applying in one worktree but accidentally testing another.
9. Do not rely on `git diff --stat` alone: it can omit untracked files created by a patch. Validate patch paths plus `git status --short`.
10. If packaging itself hits a transient permission/copy error, fix permissions and produce a clean rerun transcript rather than shipping a log containing a misleading failed operation.
11. Redact only local path prefixes and secrets; state the narrow redaction and preserve commands, revisions, invocation IDs, and results.
12. Complete all redaction, README, runner, and log edits **before** generating the checksum manifest or archive. Any post-archive content change invalidates both the member manifest and the archive checksum.
13. Freeze attachment checksums, extract the finished archive into a fresh directory, run `sha256sum -c`, verify archive member paths/digests and executable bits, and scan the exact extracted submission set for credentials and owned-account identifiers.
14. If the reply embeds the archive checksum, compare that string programmatically with the final archive hash after the last rebuild; do not rely on a visually copied value.

## Scope and duplicate review

- Reconfirm program eligibility from the current authoritative scope source immediately before submission. Save the exact repository identifier, tier, scope flag, date, and source URL.
- Also preserve a commit-pinned or immutable copy of the scope record, its SHA-256, and the rules language that links the record to tier eligibility. Phrase the conclusion as the **current published classification**, not as a guarantee that the panel cannot apply a different internal tier.
- Distinguish source eligibility from proof that a hosted production service enables the vulnerable configuration.
- Search exact public advisories/issues and adjacent historical changes. Treat an adjacent identity-linking fix as prior art unless it addresses the same missing transaction/session binding.
- Never claim novelty from public search. Private duplicate risk remains unknown.
- If a reviewer rejects solely on a tier that conflicts with the preserved exact public record, do not reargue severity or the exploit. Preserve the rejection, re-fetch the live source, and send one factual tier correction with the exact repository, commit-pinned lines, pre-submission date, and rules excerpt. Follow `argus-vault-routing/references/program-triage-outcomes-and-canonical-differentiation.md` for status synchronization and the stop condition.

## Report language checklist

- State the exact affected auth mode and policy prerequisites.
- Explain that a signed operation parameter is integrity protection, not initiator-session authorization.
- State the effective freshness window and primary delivery variant.
- Label every executed and unexecuted boundary.
- Keep severity conditional on the documented primary scenario.
- Recommend authenticated initiation plus random, single-use, server-side transaction binding consumed before every callback-driven mutation, including delegated-identity paths.
- Include immediate mitigations separately from the complete fix.
