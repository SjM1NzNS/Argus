# Immunefi Web3 Program Selection Before Target Initialization

Use this reference when choosing a first or next Immunefi program. This is Zone 0 program reconnaissance, not authorization to hunt. Do not create an active target or touch deployed contracts until the selected program has a current scope contract with `hunting_enabled: true`.

## Selection objective

Optimize for a program that can exercise the full Argus source → invariant → static-analysis → Foundry/local-fork → adversarial-reportability workflow. Do not rank solely by maximum bounty or novelty.

Score each candidate on:

1. **Scope tractability** — exact repositories/files/addresses, manageable component count, explicit live-vs-audited labels.
2. **Build readiness** — public source, reproducible dependencies, Foundry/Hardhat tests, locked versions, deployment mapping.
3. **PoC alignment** — local-fork or production-equivalent proof accepted, assertion-based impact can be reproduced, mock-only PoCs not required/encouraged.
4. **Architecture fit** — understandable asset/accounting/authorization invariants; penalize bridges, ZK, custom crypto, multichain routing, and many third-party integrations for a first pilot.
5. **Known-issue subtraction** — official audits, QA corpus, disclosed findings, and explicit exclusions are available.
6. **Researcher safeguards/friction** — Safe Harbor, arbitration, managed triage, KYC/payment requirements, submission eligibility by the researcher's current Whitehat level, paid-submission fee/stake, chain/gas costs, refund/forfeiture terms, and disclosure terms.
7. **Freshness vs saturation** — recent launch/update can reduce stale-scope risk, but never overrides architecture and evidence complexity.

Keep scores explicitly subjective and publish criteria/weights. Treat the ranking as a selection aid, not an objective security rating.

## Official-source workflow

1. Read the live Immunefi directory and candidate `information/`, `scope/`, and `resources/` pages.
2. Record maximum bounty, live/updated dates, PoC requirement, KYC, Primacy of Impact vs Primacy of Rules, triage, arbitration, and displayed Safe Harbor terms.
3. Enumerate scope rows and exact links. A short visible table may still hide pagination; inspect the complete table/count before calling a scope narrow.
4. Open official repositories and record default branch, build system, lockfiles, tests, static-analysis config, deployments, and audit directories.
5. Read program-specific audit/known-issue and exclusion material before estimating opportunity.
6. Review the platform's official social account for launches and scope expansions, then cross-check every social claim against the live program page. Social posts are discovery, not authoritative scope.
7. Separate candidates into `pilot`, `second`, `watch`, and `avoid-first` rather than pretending every fresh/high-bounty program is equally suitable.

## Mandatory submission-economics gate

Public program reconnaissance cannot reliably establish account-specific submission economics. Paid-submission restrictions may be absent from the public `information/`, `scope/`, and `resources/` pages and appear only for a signed-in researcher or inside the submission flow. **Absence from a public scan is not evidence that submission is free.**

Use a staged gate:

1. During public selection, record submission economics as `confirmed-free`, `confirmed-paid`, or `unknown`. Do not automatically reject `unknown`; allow inexpensive shortlist reconnaissance, but do not represent the program as financially cleared.
2. Before deep architecture review, extensive code analysis, or target activation, use the researcher's already-signed-in Immunefi session to inspect the candidate's program card and `Submit a Bug` flow for account-specific eligibility. Advance only as far as needed to reveal requirements; stop before wallet connection, transaction approval, signing, or submission.
3. If the platform does not reveal payment requirements until a later report-review step, try a non-submitted private draft/preview only when the UI permits it without making a report submission. Otherwise record `unknown until submission review` and ask official support or obtain the user's explicit approval for that uncertainty before committing substantial hunt time.
4. Record:
   - current Whitehat/researcher level;
   - levels allowed or blocked from free submission;
   - exact submission fee or stake, token, chain, and likely transaction costs;
   - whether the platform calls it a fee, stake, bond, or deposit;
   - official refund/forfeiture treatment for accepted, rejected, invalid, duplicate, known-issue, and out-of-scope outcomes;
   - realistic **base/minimum** reward for the likely impact class, not the advertised maximum.
5. If refund treatment is absent or ambiguous, model the full payment and gas as a sunk loss.
6. Default a **confirmed-paid** candidate to `watch` or `avoid-first` when any of these apply:
   - the user has not explicitly approved the payment risk;
   - the fee is greater than or equal to the likely base reward;
   - duplicate/known-issue material is unavailable;
   - impact mapping or economic materiality is unresolved;
   - the likely payout depends mainly on discretionary upside above the base reward.
7. Keep an `unknown` candidate in an explicit `economics-unverified` state rather than misclassifying it as free or paid. Cap work at low-cost reconnaissance until the gate is resolved or the user knowingly approves proceeding despite uncertainty.
8. For a fee-gated exception, write a short expected-value note covering fee-at-risk, base payouts, duplicate risk, impact uncertainty, and the evidence needed to justify paying. Obtain explicit user approval **before substantial hunt investment** whenever the restriction is discoverable—not retroactively after report preparation.
9. Never connect a wallet, sign a message, approve a token, or pay a submission fee as part of reconnaissance. Those are separate user-authorized actions.

A program is not financially cleared for `hunting_enabled: true` until submission economics are confirmed or the user explicitly accepts that they remain undiscoverable.

## UI and data-quality pitfalls

- Dynamic directory filter drawers may render duplicate hidden controls. Do not trust a click or query string unless the resulting count and rows visibly change.
- A directory filter result is not program-specific proof. In one observed case, a program appeared under a Safe Harbor-filtered directory result while its header had no Safe Harbor badge/tab and its `/safe-harbor/` route returned `Not Found`. Mark such status **unconfirmed** and resolve it from authenticated terms or official support before activation.
- Shared page bundles may contain generic strings such as `SafeHarbor`; these do not prove the current program opted in.
- Program-wide summaries can make a target look broad while the actual scope contains a small list of pinned files—or the reverse. Rank from the asset table, not marketing copy.
- `Primacy of Impact` can make a narrow source scope useful; `Primacy of Rules` can make a familiar protocol unforgiving. Capture exact listed impacts and exclusions.

## First-pilot preference

Prefer:

- one public Solidity repository;
- Foundry-native build with lockfile and tests;
- pinned source files or clearly mapped deployed contracts;
- local-fork-only testing required or explicitly accepted;
- no KYC if otherwise comparable;
- managed triage;
- audit/QA corpus available;
- accounting, queue, share, access-control, or upgrade invariants that can be isolated.

Defer initially:

- bridge/cross-chain finality;
- L3 or many-chain deployments;
- eight-repository ecosystems;
- ZK/custom cryptography;
- extensive oracle/third-party integration assumptions;
- mainnet-only proof requirements;
- large mature deployment sets where known-issue subtraction dominates the exercise.

## Pre-activation capture

Before cloning for an active hunt, capture:

```text
platform/program URL and verification date
repository + exact branch/commit
in-scope files/addresses and live/latest-audited labels
listed impacts and exclusions
PoC and local-fork rules
mainnet/public-testnet prohibitions
oracle/third-party restrictions
Safe Harbor/arbitration/triage status
KYC/payment requirements
current account submission eligibility and Whitehat level
paid-submission fee/stake, token, chain, and transaction cost
refund/forfeiture terms by outcome (or explicit `unknown; modeled as sunk`)
likely impact class and base/minimum payout versus fee-at-risk
known audits/findings
responsible-disclosure channel
```

Only then initialize an isolated target folder and set `hunting_enabled: true`. Never request or store the user's account password, 2FA seed, recovery codes, cookies, or session tokens; a public profile handle or user-confirmed logged-in browser state is sufficient for coordination.