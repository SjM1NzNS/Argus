---
type: learning-source-summary
compiled_at: 2026-08-05T05:31:36.647975+00:00
source_quality: 6
classification: Web2 skill update
vulnerability_class: API Security
---

# Global Crypto Payment License Map: MSB, MiCA, MPI

- URL: `https://blocksec.com/blog/crypto-payment-license-map`
- Source group: `browser_dom_linked_resources`
- Content chars: `17467`
- Classification: **Web2 skill update**
- Vulnerability class: **API Security**

## Source summary

- It's not one license — it's a different regime in nearly every jurisdiction, each with its own name, capital threshold, and timeline, and getting it wrong doesn't just mean a fine.
- Quick-Reference: Payment Licenses by Jurisdiction Here's the main license for payment companies (not stablecoin issuers) in each jurisdiction covered below: Jurisdiction Main license for payment companies Capital / threshold Key point United States Federal MSB registration + state MTLs Varies by state; nationwide coverage takes years and millions MSB is an AML registration, not a state license; Circle holds 46 state MTLs European Union CASP (moving EMT usually also needs EMI/PI) Depends on the license The CASP transition period ended 2026-07-01; end-to-end payments often need two licenses Singapore SPI / MPI under the PSA (DPT services) SPI SGD 100K / MPI SGD 250K Approval takes 9-18 months; MPI must segregate customer assets, ~90% in cold wallets Hong Kong MSO (exchange/remittance) / SVF (stored value) MSO no minimum capital / SVF HKD 25M Exchange and remittance mostly fall under MSO; holding customer balances may trigger SVF United Kingdom FCA authorization (2026 regime) Depends on activity Authorization window 2026.9-2027.2, rules in force 2027.10; stablecoins and e-money kept separate UAE Dubai VARA / Abu Dhabi ADGM Depends on activity VARA issues 8 activity licenses; ADGM requires separate entities per license Two Kinds of Crypto License, Easy to Confuse Before you map jurisdictions, it helps to separate two license types that get conflated constantly: Stablecoin issuance licenses — if you want to issue your own stablecoin, you need an issuer framework like the GENIUS Act / OCC Charter in the US or MiCA's EMT in the EU.
- The core requirements here are capital, AML/CFT, and segregation of customer funds.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
