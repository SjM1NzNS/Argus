# Private bug-bounty invite inventory and selection

Use this reference when the user pastes or transcribes private/invitation-only program cards from Intigriti or another platform.

This is an **inventory workflow**, not live-status verification, program ranking, workspace initialization, or authorization to test.

## Core distinctions

Always keep these states separate:

1. **Platform card state** — what the pasted invite card says, such as “Open program.”
2. **Researcher eligibility and practical access** — whether this account can open the full brief, submit, satisfy regional/KYC/account/hardware/fee requirements, and reach useful in-scope surfaces.
3. **Local Argus activation** — whether a reviewed scope contract explicitly has `hunting_enabled: true`.

A platform card saying “Open” proves neither researcher-specific access nor local activation.

## Recording workflow

1. Treat the pasted data as a **user-provided platform-UI snapshot**. Timestamp the capture, but do not call it live-verified unless the direct brief and submission controls were checked in the same pass.
2. Search `$HOME/SecurityResearch/03 - Targets/Program Shortlists/` for an existing invite ledger before creating a duplicate.
3. Save a dated note under that directory, normally:

   `intigriti-private-invites-YYYY-MM-DD.md`

   Use a platform-neutral equivalent for other platforms.
4. Preserve displayed company/program names, invite dates, currencies, bounty wording, relative update ages, and card status. Do not silently convert currencies or turn relative ages into invented absolute dates.
5. If locale interpretation is uncertain, preserve the displayed date and label the assumed format rather than normalizing it as fact.
6. Preserve truncated or partial cards as incomplete rows. Use `Not supplied`; never infer the missing bounty, update age, status, or scope.
7. Link the current shortlist, live-status audit, and workspace inventory when they exist, but do not rewrite those historical snapshots merely because a newer invite arrived.
8. Unless the user explicitly asks for ranking or initialization, stop at inventory capture. Do not fetch every brief, score candidates, create target/Burp folders, or enable hunting implicitly.
9. Do not save the invite list to persistent user memory: invite state and program cards are time-sensitive vault state.

## Required note content

Include:

- capture timestamp and source classification;
- explicit statement that direct briefs, submission controls, scope, exclusions, safe harbor, and rewards were not independently verified when that is true;
- one row per invite with company, program, displayed invite date, bounty card, last-updated card, card status, and caveats;
- complete versus partial entry counts;
- explicit statement that target folders, Burp projects, monitoring, and scope contracts were unchanged when applicable;
- a pre-testing verification checklist.

## Transition to prioritization

If the user later asks which invitations to hunt:

1. Verify each direct live brief and researcher-specific submission/access state.
2. Capture exact scope, exclusions, account model, prohibited actions, rate limits, duplicate policy, reward table, safe harbor, regional/KYC/fee/hardware constraints, and update history.
3. Use `references/cross-platform-public-program-screening.md` for competition-adjusted scoring, but label private-invite access as a feasibility/saturation proxy—not proof of low competition.
4. Use `references/live-program-hunting-status-verification.md` to separate platform status, account eligibility, and local activation.
5. Initialize workspaces only for selected candidates and start every scope contract with `hunting_enabled: false`.

## Late authenticated-brief reconciliation

A private brief often arrives after a provisional public-source ranking. Treat it as a ranking-changing event, not a detail to append after the decision:

1. **Classify provenance precisely.** Distinguish an independently opened authenticated brief from a researcher-supplied transcription or screenshot. Both are stronger than product inference, but only the former independently verifies the live page and submission control.
2. **Build an exact asset ledger.** Preserve scheme, host, path, asset type, tier, `no bounty`, and `out of scope` labels exactly. Do not broaden `http` to `https`, a host to sibling subdomains, an app to its backend, or a paid web asset to unlisted API hosts.
3. **Convert exclusions into route filters.** Record excluded paths, object-reference forms, application classes, third-party systems, and vulnerability classes before source mapping. An exclusion such as numeric reservation IDs must suppress every hypothesis that depends on that identifier form, not merely the example URL.
4. **Separate source artifact from bounty asset.** A no-bounty APK/IPA, SDK, public repository, developer portal, or API specification may be used for passive route and object discovery when the rules permit, but it does not make mobile-only behavior, unlisted hosts, partner APIs, or documented sandbox routes reportable.
5. **Re-evaluate practical access.** Public documentation is not an owned control. Sales-provisioned sandboxes, customer agreements, policyholder state, banking identity, business registration, partner tenancy, deposits, purchases, or real fulfilment remain hard feasibility gates unless the private brief supplies an approved test path.
6. **Re-score and re-rank.** Recalculate any access/source/impact component affected by the brief, then reapply the hard feasibility gate. State explicitly when the selected target changes and why.
7. **Propagate the correction.** Patch the inventory backlink, selection note, practical disposition, first-lane instructions, pivot criteria, and any initialized scope contract. Never leave the old winner or broadened scope only in chat history.
8. **Keep activation separate.** A complete brief transcription can raise selection confidence, but hunting remains disabled until live eligibility/submission control is checked and a local exact-scope contract is reviewed.
9. **Validate deterministically.** Check asset count and exact strings, reward rows, no-bounty/out-of-scope labels, rate limits, account rules, score math, reciprocal links, and absence of accidental `hunting_enabled: true`.
10. **Reconcile overview rewards with exact assets.** A positive overview maximum does not prove that any current exact-scope asset pays. If every exact asset is `No Bounty` or `Out Of Scope`, exclude the program fail-closed and record the overview/exact-scope mismatch.
11. **Treat leaderboard page limits as censoring.** If many leaderboards stop at the same round count (for example 100 cached rows), label that value `at least/capped`, never an exact total or active-hunter count.
12. **Label response clocks precisely.** Published validation targets are not observed triage speed or end-to-end response time; where the template says so, the program clock starts only after platform verification.
13. **Fail closed on safe-harbour conflicts.** If a machine-readable safe-harbour field is false while prose appears supportive, disclose the conflict and use `HOLD` until the legal/rules posture is explicitly accepted. Do not treat the prose as silently overriding the field.

When unauthenticated private-route candidates return generic `Forbidden`, do not call the slug canonical: invalid private routes may render or fail identically. Preserve candidate handles as discovery aids and enter through the authenticated invitation UI.

## Path-qualified wildcard API assets

When a private brief lists a wildcard together with a path prefix, such as `*.example.net/v1/product/`, preserve it as a combined host-and-path boundary rather than broadening either dimension:

1. Treat only matching subdomains and the exact listed path prefix/descendants as scope-listed. Do not infer the apex domain, sibling paths, other API versions, unrelated company hosts, redirects outside the boundary, alternate ports, or unspecified protocols.
2. Distinguish **scope-listed** from **operationally actionable**. If the brief says API specifications are supplied case-by-case, references exclusions from another program, or leaves schemes/rate limits/account controls unresolved, import those dependencies before any endpoint request.
3. Do not interpret `Not applicable` in an automation/header field as unlimited permission. Record it literally and obtain a positive rate/automation rule before using scanners or concurrent tooling.
4. Start an approved API lane from the official client, supplied schema/specification, or other explicitly permitted source artifact. Do not compensate for a missing specification with endpoint guessing or broad enumeration.
5. Build the local contract as exact host/path filters and verify redirects remain in scope. Search for activation target-specifically; unrelated targets with `hunting_enabled: true` are not evidence that this target is enabled.
6. Keep disruptive classes separately gated. A brief may call targeted application-level DoS reportable while still forbidding high-volume testing; require an owned/private environment and explicit validation approval before any crash proof.

Phrase the answer clearly: “the API family is listed in scope, but testing is not operationally green until the unresolved brief, access, and local-activation gates are satisfied.”

## Validation

Run a deterministic check that:

- table row count equals the number of supplied entries;
- complete/partial accounting matches the rows;
- every related Obsidian link resolves;
- no `TODO`/`TBD` placeholder remains;
- the note contains `hunting_enabled: false` or an equivalent explicit inactive statement;
- no accidental `hunting_enabled: true` appears;
- no missing card field was guessed.

## Common pitfalls

1. **Invite equals authorization.** An invitation or “Open program” card is selection input, not a reviewed scope contract.
2. **Completing truncated cards from memory.** Preserve `Not supplied` until the user or live brief provides the value.
3. **Premature ranking.** Reward ceiling alone is not enough; access, scope quality, update freshness, duplicate pressure, response metrics, and safe owned controls still matter.
4. **Historical snapshot drift.** Create a new dated inventory rather than rewriting an older shortlist or live-status audit as though it was checked today.
5. **Workspace sprawl.** Do not materialize every invite unless the user asks; wide inventory should still lead to narrow execution.
