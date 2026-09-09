---
type: learning-source-summary
compiled_at: 2026-07-15T05:32:08.229671+00:00
source_quality: 8
classification: vulnerability pattern
vulnerability_class: Bridge / Proof Validation
---

# Rekt - <!-- -->Bonzo Finance - Rekt

- URL: `https://rekt.news/bonzo-finance-rekt`
- Source group: `daily_deep_content`
- Content chars: `13901`
- Classification: **vulnerability pattern**
- Vulnerability class: **Bridge / Proof Validation**

## Source summary

- That was the entire cryptographic proof standing between Hedera's largest lending market and a $9.05 million bleed-out .
- Supra's pull oracle lets anyone submit a price update , provided the accompanying proof passes a BLS signature check run through Hedera's pairing precompile.
- Onchain Investigator Specter got there first with the initial details : There appears to be an ongoing hack involving Hedera Network, with over $3.7 million already bridged to Ethereum through LayerZero, stolen funds swapping from WBTC into ETH.

## Extracted methodology

- Affected surface: signed pull-oracle/verifier wrappers around BLS pairing precompiles.
- Root cause: an attacker-selected out-of-range committee ID returned an all-zero/default public key; an all-zero signature and key were identity elements, so the pairing equation held although no authorized signer was checked.
- Minimal method: local/fork matrix over a valid non-zero update, out-of-range committee ID, zero/identity key and signature, malformed point, and wrong signer set; record both precompile-call success and semantic verification result.
- Evidence requirements: lookup bounds, exact encodings, accepted malformed update, before/after consumed oracle state, downstream borrow/liquidation/value path, and a patched negative control rejecting the input before the primitive.
- False-positive gates: a mathematically correct precompile result is not itself a bug; require missing wrapper validation plus unauthorized state/economic impact. Bridging stolen proceeds was post-exploit movement, not the root vulnerability.

## Compiler decision

- Promoted on 2026-07-15 into Proof Systems, Oracles, Web3 routing, and eval coverage after class-level review.
