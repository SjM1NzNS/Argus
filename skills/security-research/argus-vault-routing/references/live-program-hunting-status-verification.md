# Live program hunting-status verification

Use this reference when a user asks whether all shortlisted or initialized bug-bounty programs have “hunting enabled,” especially after target folders were created. The phrase is ambiguous; resolve it with evidence rather than answering from folder state or directory visibility.

## Three-state model

Always report these states separately:

1. **Platform accepting submissions** — the current direct program brief and platform data show an open paid program with an active vulnerability-report path and no pause/closure banner.
2. **Researcher eligible and practically accessible** — the researcher has any required invitation/application approval, account, geography, KYC, phone, hardware, test tenant, or no-fee path needed for authorized testing.
3. **Argus scope activated** — the exact current assets, exclusions, testing rules, rate limits, account model, and report requirements have been imported into the local scope contract and `hunting_enabled` has deliberately been changed from `false` to `true` for that target only.

Never collapse these into one boolean. A program can be platform-open while application-gated, impractical for the researcher, or locally disabled pending scope import. A locally initialized workspace with `hunting_enabled: false` says nothing about whether the platform program is paused.

## Verification sequence

1. Recover the exact selected-program list and canonical direct URLs from the saved shortlist or workspace inventory.
2. Check every direct live brief and the strongest current platform status source; do not rely on the original screening date or a marketing directory card.
3. Require positive submission evidence where the platform exposes it, plus absence of an explicit paused/closed/not-accepting state.
4. Record access gates separately from program status: application approval, invitation, researcher account, residency/sanctions, KYC, regional phone, subscription, hardware, chain fees, or designated test objects.
5. Timestamp the result and save a dated central snapshot beside the shortlist. State that only program pages/APIs were read and no target testing occurred.
6. Do not bulk-enable local contracts. Import and activate one exact scope at a time when that hunt starts.

## Platform evidence patterns

### Intigriti

- Open the direct rendered detail or terms page and capture the human-readable visibility/access label and state, such as `Public / Open` or `Application / Open`.
- Use the public preview API as corroboration, but do not assign permanent meanings to undocumented numeric status enums from memory. Map a code to rendered state during the same check; a known suspended page may be used as a control.
- `Application / Open` means the program accepts applications, not that the researcher is authorized to test. Classify it as **conditional until accepted**.
- A terms-gated or access-controlled preview API response is not proof of closure. Fall back to the rendered direct page.

### YesWeHack

- Check the detail API for a current public paid record and no closure timestamp.
- Confirm the rendered direct page displays `Bug bounty`, `Public`, and `SUBMIT REPORT`, with no paused/suspended banner.
- Do not treat an API visibility code alone as submission proof; pair it with the rendered control.

### HackerOne

- HTTP `200` and the static HTML shell are insufficient; rendered program content may load client-side.
- Confirm an active vulnerability-report route, normally ending in `/reports/new?type=team&report_type=vulnerability`, and no explicit program-paused/not-accepting banner.
- Avoid broad substring checks such as `closed`, which false-positive on `Closed Scope` and `disclosed`. Match exact program-state phrases or inspect line-normalized labels.
- `Closed Scope` means only listed assets are accepted; it does not mean the program is closed.

### Bugcrowd

- Use the current public bug-bounty directory API and require the direct engagement to have `accessStatus: open`; record `isPrivate` and any explicit service level.
- Open the direct brief when access, eligibility, or submission availability is unclear. A direct URL returning `200` alone is not sufficient.
- `Priority Triage` is a service-level signal, not an authorization state.

## Output and persistence

Create a dated note such as:

```text
03 - Targets/Program Shortlists/live-hunting-status-verification-YYYY-MM-DD.md
```

Include:

- check timestamp and the three status definitions;
- exact expected and verified program count;
- one row per program with direct URL, live platform state, submission evidence, access caveat, and disposition;
- totals for platform-open, application/invitation-gated, and locally enabled targets;
- a statement that no target testing occurred;
- the local contract posture (`hunting_enabled: false` until exact scope import).

Link the workspace inventory to the dated status snapshot. Do not overwrite the original shortlist’s historical selection evidence.

## Verification gate

Before reporting the result:

- every selected program appears exactly once;
- direct program URLs are unique and match the saved shortlist;
- every “open” claim has current direct/API evidence appropriate to that platform;
- every application/invitation/account/eligibility gate is visible in the disposition;
- generic text matching did not confuse `Closed Scope` or `disclosed` with a closed program;
- no local contract was activated merely because the platform is open;
- the saved snapshot has a timestamp, no TODO/TBD placeholders, and a backlink from the inventory.

## Common pitfalls

1. **Answering from local flags.** Draft Argus contracts are intentionally disabled and are not platform status evidence.
2. **Answering from directory presence.** Stale or suspended programs can remain listed.
3. **Treating HTTP 200 as submission availability.** Rendered controls or current API state are required.
4. **Equating application-open with hunt-authorized.** Acceptance must occur first.
5. **Calling access friction a pause.** KYC, regional accounts, test tenants, or eligibility can block the researcher while the program remains open.
6. **Bulk-enabling the portfolio.** Scope and rules change; activate only the target whose live brief has been imported.
7. **Omitting the timestamp.** Hunting status is volatile and every answer is a dated snapshot.
