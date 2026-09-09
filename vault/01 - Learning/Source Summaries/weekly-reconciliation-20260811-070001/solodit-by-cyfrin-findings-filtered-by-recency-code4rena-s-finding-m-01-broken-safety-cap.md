---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.089892+00:00
source_quality: 4
source_id: solodit-by-cyfrin-findings-filtered-by-recency
source_role: report_repository
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [validation_technique, evidence_requirement, reportability_criterion]
classification: severity rule
vulnerability_class: Oracle / Economic
---

# Code4rena's finding: [M-01] Broken safety cap in `liquidate.rs` causes permanent DoS of liquidation engine during market crashes, leading to insolvency.: Jupiter Lend_2026-07-11

- URL: `https://solodit.cyfrin.io/issues/m-01-broken-safety-cap-in-liquidaters-causes-permanent-dos-of-liquidation-engine-during-market-crashes-leading-to-insolvency-code4rena-jupiter-lend-jupiter-lend-git`
- Source ID / role / trust: `solodit-by-cyfrin-findings-filtered-by-recency` / `report_repository` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://solodit.cyfrin.io/?i=HIGH%2CMEDIUM%2CLOW%2CGAS&maxf=&minf=&rf=alltime&sd=Desc&sf=Recency`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `7386`
- Classification: **severity rule**
- Vulnerability class: **Oracle / Economic**

## Source summary

- Since liquidation_max_limit can be close to 100% (e.g., 950/1000 = 95%), the cap must satisfy: ​ cap * 2^48 / 1e15 * (LML / 1000) ≤ MAX_RATIOX48 For LML = 999 (near 100%, worst case): ​ cap ≤ MAX_RATIOX48 * 1e15 / 2^48 * 1000 / 999 ≈ 4.62e25 Apply the fix in both liquidate.rs and operate.rs: ​ // liquidate.rs - get_ticks_from_oracle_price - if debt_per_col > 10u128.pow(26) { - debt_per_col = 10u128.pow(26); + // Cap derived from MAX_RATIOX48 * 1e15 / 2^48 ≈ 4.62e25 + // Rounded down for safety margin + if debt_per_col > 46_000_000_000_000_000_000_000_000 { + debt_per_col = 46_000_000_000_000_000_000_000_000; } ​ // operate.rs - get_sanitized_exchange_rate - if exchange_rate > 10u128.pow(26) { - exchange_rate = 10u128.pow(26); + if exchange_rate > 46_000_000_000_000_000_000_000_000 { + exchange_rate = 46_000_000_000_000_000_000_000_000; } Proof of Concept The vulnerability is a pure arithmetic overflow that can be demonstrated with a calculation trace.
- Impact Liquidation DoS: When extreme market divergence pushes debt_per_col into the range [~4.62e25, 1e26], calls to get_ticks_from_oracle_price() revert with LibraryTickRatioOutOfBounds.
- Jupiter Lend ・ Jul 11, 2026 AI Summary programs/vaults/src/utils/liquidate.rs [# L152-L154](https://github.com/Instadapp/fluid-solana-programs/blob/626b177f235224bc5d074d39439cd2558f542886/programs/vaults/src/utils/liquidate.rs# L152-L154programs/vaults/src/utils/liquidate.rs# L152-L154) programs/vaults/src/utils/operate.rs [# L41-L42](https://github.com/Instadapp/fluid-solana-programs/blob/626b177f235224bc5d074d39439cd2558f542886/programs/vaults/src/utils/liquidate.rs# L152-L154programs/vaults/src/utils/operate.rs# L41-L42) In get_ticks_from_oracle_price() (liquidate.rs) and get_sanitized_exchange_rate() (operate.rs), the protocol caps debt_per_col / exchange_rate at 10u128.pow(26) (1e26) to prevent precision loss.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `validation_technique, evidence_requirement, reportability_criterion`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `true`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
