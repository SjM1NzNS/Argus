# Daily Web3 lending and governance-lifecycle promotion (2026-07)

Use this reference when one lightweight incident digest contains multiple independent Web3 root causes and the compiler collapses them into the wrong class.

## Promotion pattern

1. Manually inspect every `actual_content` record; eligibility is not classification.
2. Split multi-incident articles by root cause and route each independently through `web3-skill-index.md`.
3. Correct compiler labels before promotion. In the BlockSec BarnBridge/DeFiTuna case, `Bridge / Proof Validation` was wrong; the durable classes were Lending and Governance lifecycle.
4. Promote only source-supported mechanics, evidence gates, negative controls, and reportability rules.
5. Replace generic compiler summaries/proposals with one curated source summary plus class-level evals.
6. Clear only the reviewed daily inbox directories and explicitly superseded compiler artifacts; preserve unrelated manual, Preview.is, and older inbox material.
7. Verify every index `Load:` path, touched-file non-emptiness, absence of placeholders, exact cleanup absence, and preservation samples.

## Lending lesson: degenerate health state plus route/check mismatch

When a lending position is valued after a swap:

- `assetValue == 0` must not imply healthy while debt or fees remain non-zero;
- test positive dust that truncates to zero as a separate case from exact zero;
- bind oracle/pool checks to the route, pool, mints, accounts, and output actually executed;
- caller-supplied aggregator routes need an oracle/debt-derived minimum output or equivalent post-swap value bound;
- a check against a canonical pool does not constrain execution through another low-liquidity or attacker-selected pool.

Minimum eval matrix: normal value, exact zero, dust-to-zero, normal route, hostile route, and a route-bound/min-output negative control. Reportability requires realistic local/fork bad debt or loss, not route control alone.

## Governance lesson: deprecation must retire authority

Treat protocol deprecation as a lifecycle transition, not a no-value label:

- determine whether old governor/timelock/executor modules remain callable;
- map retained configuration, upgrade, treasury, and token-transfer authority;
- include residual balances and usable user approvals in value-at-risk accounting;
- require exact payload reachability plus local/fork or complete on-chain evidence;
- kill the branch when authority is irreversibly disabled and no assets or approvals remain consumable.

## External RAG fallback

For technique/reportability questions, attempt the approved wrapper first. If it times out, perform one direct API retry using the private environment-backed key. Promote nothing when results are weak or off-topic; record that no RAG-derived claim was used and continue from the independently reviewed source plus local playbook gates.

## Pitfalls

- Do not promote an incident article under one class merely because the compiler chose one label.
- Do not infer exploit mechanics from issue titles or listing pages that were not deeply fetched.
- Do not preserve boilerplate compiler methodology after a curated replacement exists.
- Do not clear manual or older inbox paths during a daily cleanup.
