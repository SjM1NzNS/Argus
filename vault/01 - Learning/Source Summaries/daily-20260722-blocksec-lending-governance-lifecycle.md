---
type: learning-source-summary
status: promoted
reviewed: "2026-07-22"
source_url: "https://blocksec.com/blog/web3-security-barnbridge-defituna-exploits"
source_group: browser_dom_linked_resources
---

# BlockSec BarnBridge and DeFiTuna incident lessons — 2026-07-22

## Review scope

- Daily run: `daily-20260722-073001`
- Combined records: 217
- Actual content: 4 (1.8%)
- Index/listing: 71
- Not fetched: 134
- Manually reviewed all four actual-content records.

## Promoted lessons

### DeFiTuna — degenerate lending health state and route/check mismatch

BlockSec reports that a positive but negligible position balance truncated to zero, while the health check treated `total == 0` as healthy without requiring debt to be zero. Caller-supplied Jupiter route data could execute against a separate low-liquidity/extreme-price pool, while the pre-swap check validated the normal market pool and no oracle/debt-derived minimum output bound constrained the executed route.

Durable checks:

- zero or truncated-to-zero asset value must fail closed when debt remains;
- validate the actual executed route/pool/accounts, not a separate reference pool;
- bind post-swap output/value to debt and oracle expectations;
- test exact-zero, dust-to-zero, normal route, hostile route, and route-bound negative controls;
- require measurable bad debt/loss in a local/fork proof before reportability.

### BarnBridge — deprecation must retire authority

BlockSec reports that a deprecated but still-active governance system could pass a malicious proposal, modify critical configuration, and drain user-approved funds. The durable lesson is lifecycle-oriented: a deprecated label does not prove zero value or zero authority.

Durable checks:

- establish whether old governor/timelock/executor modules remain callable;
- map retained proposal/execution, configuration, upgrade, treasury, and transfer authority;
- include residual balances and usable user approvals in value-at-risk accounting;
- require an exact payload path plus local/fork or complete on-chain proof;
- kill the lead when authority is irreversibly disabled and no assets/approvals remain consumable.

## Rejected or deferred actual-content records

- `Bug Bounty Daily`: SPA/import-map/bootstrap capture, not vulnerability methodology.
- `uphiago/recon-skills`: repository catalog only; targeted SAML material was separately reviewed and promoted on 2026-07-21.
- WordPress release feed: WordPress 7.0.2/CVE material was already promoted on 2026-07-17.

## External RAG note

Preview.is wrapper queries timed out. Direct retries returned low-score generic lending results and an off-topic high-score governance result; no RAG-derived claim was promoted.
