---
type: source-summary
status: promoted
created: "2026-07-04"
source_run: daily-20260704-073001
---

# Daily 2026-07-04 Web3 source summary — BlockSec / Solodit

Reviewed latest daily ingest records under `01 - Learning/Inbox/daily-20260704-073001*`.

## Content-quality audit

- Static run: 146 records; 1 `actual_content` record, 56 index/listing metadata records, 84 not-fetched/skipped records.
- Browser DOM run: 56 records; 2 `actual_content` records, 13 index/listing records, 38 seen/skipped records.
- Actual deep content ratio across combined records: 3 / 202. Most records were discovery metadata or previously seen URLs, so promotion was limited to concrete methodology from the two Web3 deep pages.

## Promoted sources

### BlockSec — Newsletter June 2026

URL: `https://blocksec.com/blog/efi-security-incidents-jaredfromsubway-aztec`

High-signal lessons extracted:

- MEV/bot or automation logic must not trust wrapper/pool events or apparent simulation profit without verifying allowance consumption, spender allowlists, code hash expectations, and residual approval cleanup.
- ZK/rollup proof validity is insufficient by itself: every settlement-critical value must be constrained to the exact public state and root consumed by settlement logic.
- Private witnesses, membership roots, nullifiers, transaction counts, and public roots must be bound together; a valid proof over a different state can still authorize an unsafe settlement if bindings are missing.
- Wallet signing implementations must include the secret nonce/prefix input; deterministic nonce derivation from only public transaction data can leak private keys from public signatures.
- Zcash Orchard-style missing equality constraints reinforce that circuit security is about what constraints actually prove, not what surrounding protocol code assumes.

### Solodit / Cyfrin checklist

URL: `https://solodit.cyfrin.io/checklist`

Promoted only as a light routing/checklist reinforcement, not as primary source authority. Useful extracted themes: pull-payment withdrawal pattern for DoS resistance, minimum amount/dust checks, blacklisting-token handling, forced-queue DoS, low-decimal-token DoS, and safe external contract interactions.

## Deferred material

- Bug Bounty Daily was labeled `actual_content` but content was primarily application/bootstrap/import-map text and did not contain extractable vulnerability methodology for this pass.
- AppSec/index/listing and skipped/seen records were not promoted.
