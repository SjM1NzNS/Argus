# WEB3 SKILL INDEX

Argus uses this index to dynamically load Web3 playbooks based on discovered protocols, contracts, functions, tool output, hypotheses, and evidence gaps.

## ERC4626 / Vaults

Triggers:

- ERC4626
- vault
- deposit
- redeem
- withdraw
- mint
- shares
- totalAssets
- totalSupply
- exchange rate
- donation-sensitive accounting

Load:

- `02 - Vulnerability Playbooks/Web3/ERC4626/overview.md`
- `02 - Vulnerability Playbooks/Web3/ERC4626/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/ERC4626/false-positives.md`
- `02 - Vulnerability Playbooks/Web3/Share Accounting/invariants.md`
- `02 - Vulnerability Playbooks/Web3/Foundry/poc-template.md`

## Lending

Triggers:

- collateral
- borrow
- repay
- liquidate
- health factor
- LTV
- oracle price
- interest accrual
- debt shares
- zero asset value with non-zero debt
- health-check truncation
- caller-supplied swap route
- routed pool mismatch
- extreme-price liquidation liveness
- safety cap revert window

Load:

- `02 - Vulnerability Playbooks/Web3/Lending/overview.md`
- `02 - Vulnerability Playbooks/Web3/Lending/invariants.md`
- `02 - Vulnerability Playbooks/Web3/Lending/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Oracles/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Liquidations/attack-patterns.md`

## AMM / DEX

Triggers:

- swap
- liquidity
- pool
- reserves
- invariant
- slippage
- LP tokens
- fee accounting
- price manipulation

Load:

- `02 - Vulnerability Playbooks/Web3/AMM/overview.md`
- `02 - Vulnerability Playbooks/Web3/AMM/invariants.md`
- `02 - Vulnerability Playbooks/Web3/AMM/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Oracles/false-positives.md`

## Bridges / Cross-chain Messaging

Triggers:

- bridge
- message proof
- relayer
- validator
- chain ID
- domain separator
- replay protection
- finalization
- withdrawal proof

Load:

- `02 - Vulnerability Playbooks/Web3/Bridges/overview.md`
- `02 - Vulnerability Playbooks/Web3/Bridges/invariants.md`
- `02 - Vulnerability Playbooks/Web3/Signatures/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Access Control/false-positives.md`

## ZK / Proof Systems

Triggers:

- zero-knowledge
- ZK
- zk proof
- circuit
- verifier
- public input
- private witness
- nullifier
- membership root
- proof root
- rollup proof
- settlement proof
- shielded pool
- escape hatch
- proof-to-settlement binding
- BLS signature
- pairing precompile
- identity element
- zero public key / zero signature
- committee ID

Load:

- `02 - Vulnerability Playbooks/Web3/Proof Systems/overview.md`
- `02 - Vulnerability Playbooks/Web3/Proof Systems/test-checklist.md`
- `02 - Vulnerability Playbooks/Web3/Proof Systems/invariants.md`
- `02 - Vulnerability Playbooks/Web3/Proof Systems/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web3/Proof Systems/false-positives.md`
- `02 - Vulnerability Playbooks/Web3/Proof Systems/reportability.md`
- `02 - Vulnerability Playbooks/Web3/Proof Systems/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Bridges/invariants.md`
- `02 - Vulnerability Playbooks/Web3/Foundry/poc-template.md`

## Signatures / Permit / Replay

Triggers:

- ecrecover
- signature
- permit
- EIP-712
- nonce
- domain separator
- chain ID
- deadline
- replay

Load:

- `02 - Vulnerability Playbooks/Web3/Signatures/overview.md`
- `02 - Vulnerability Playbooks/Web3/Signatures/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Signatures/false-positives.md`

## Reentrancy

Triggers:

- external call
- call.value
- ERC777
- callback
- hook
- withdraw
- transfer before state update
- unsafe interaction order

Load:

- `02 - Vulnerability Playbooks/Web3/Reentrancy/overview.md`
- `02 - Vulnerability Playbooks/Web3/Reentrancy/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Reentrancy/false-positives.md`
- `02 - Vulnerability Playbooks/Web3/External Calls/unchecked-external-calls.md`
- `02 - Vulnerability Playbooks/Web3/Foundry/poc-template.md`

## External Calls / Unchecked Calls

Triggers:

- unchecked external call
- low-level call
- delegatecall
- staticcall
- send
- transfer return value
- ERC20 false return
- non-returning token
- ERC777 hook
- ERC721 receiver
- ERC1155 receiver
- flash loan callback
- user-supplied callee
- configurable target

Load:

- `02 - Vulnerability Playbooks/Web3/External Calls/unchecked-external-calls.md`
- `02 - Vulnerability Playbooks/Web3/Reentrancy/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Reentrancy/false-positives.md`
- `02 - Vulnerability Playbooks/Web3/Foundry/poc-template.md`

## Flash Loans

Triggers:

- flash loan
- transient capital
- one transaction borrow
- oracle manipulation
- flash loan voting
- same-block voting
- liquidity amplification
- pool state manipulation
- atomic manipulation

Load:

- `02 - Vulnerability Playbooks/Web3/Flash Loans/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Oracles/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/AMM/invariants.md`
- `02 - Vulnerability Playbooks/Web3/Lending/invariants.md`
- `02 - Vulnerability Playbooks/Web3/Share Accounting/invariants.md`
- `02 - Vulnerability Playbooks/Web3/Foundry/poc-template.md`

## Upgradeability / Proxy

Triggers:

- proxy
- delegatecall
- initializer
- implementation
- storage layout
- upgradeTo
- UUPS
- transparent proxy
- beacon proxy
- diamond proxy
- facet
- reinitializer
- proxy admin
- storage gap
- proxiableUUID
- implementation locked

Load:

- `02 - Vulnerability Playbooks/Web3/Upgradeability/overview.md`
- `02 - Vulnerability Playbooks/Web3/Upgradeability/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Upgradeability/false-positives.md`

## Governance

Triggers:

- vote
- proposal
- quorum
- timelock
- delegate
- governor
- voting power
- snapshot
- execution delay
- deprecated governance
- retired protocol authority

Load:

- `02 - Vulnerability Playbooks/Web3/Governance/overview.md`
- `02 - Vulnerability Playbooks/Web3/Governance/invariants.md`
- `02 - Vulnerability Playbooks/Web3/Governance/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Signatures/false-positives.md`

## Oracle / Price Manipulation

Triggers:

- price feed
- TWAP
- Chainlink
- custom oracle
- spot price
- reserve-based pricing
- stale price
- decimals
- heartbeat

Load:

- `02 - Vulnerability Playbooks/Web3/Oracles/overview.md`
- `02 - Vulnerability Playbooks/Web3/Oracles/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Oracles/false-positives.md`
- `02 - Vulnerability Playbooks/Web3/Lending/invariants.md`
- `02 - Vulnerability Playbooks/Web3/AMM/invariants.md`

## Access Control

Triggers:

- onlyOwner
- onlyRole
- admin
- guardian
- pauser
- operator
- minter
- upgrade admin
- access manager
- role grant/revoke

Load:

- `02 - Vulnerability Playbooks/Web3/Access Control/overview.md`
- `02 - Vulnerability Playbooks/Web3/Access Control/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Access Control/false-positives.md`

## Input Validation

Triggers:

- input validation
- out of bounds
- zero address
- max uint
- fee bps
- collateral factor
- malformed calldata
- arbitrary calldata
- unsupported token
- duplicate array
- length mismatch
- cross-chain message
- signed payload
- relayed call
- invalid config
- transformed numeric bound
- downstream representation limit
- intermediate fixed-point overflow or revert

Load:

- `02 - Vulnerability Playbooks/Web3/Input Validation/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Signatures/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Bridges/invariants.md`
- `02 - Vulnerability Playbooks/Web3/Access Control/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Foundry/poc-template.md`

## Rounding & Precision

Triggers:

- division before multiplication
- decimals
- scaling factor
- fixed point math
- share calculation
- fee calculation
- dust
- truncation
- rounding direction
- source-domain safety cap
- fixed-point library bound
- inversion or scaling boundary

Load:

- `02 - Vulnerability Playbooks/Web3/Rounding & Precision/overview.md`
- `02 - Vulnerability Playbooks/Web3/Rounding & Precision/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Rounding & Precision/false-positives.md`
- `02 - Vulnerability Playbooks/Web3/Share Accounting/invariants.md`

## State Machines / Lifecycle

Triggers:

- epoch
- round
- phase
- batch lifecycle
- queue lifecycle
- status enum
- pendingCount
- settlement state
- cancellation flow
- refund flow
- force-pass
- NAV update
- terminal state
- stuck state
- lifecycle invariant

Load:

- `02 - Vulnerability Playbooks/Web3/State Machines/overview.md`
- `02 - Vulnerability Playbooks/Web3/Input Validation/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Reporting/reportability.md`
- `02 - Vulnerability Playbooks/Web3/Foundry/poc-template.md`

## Static Analysis / Tool Output

Triggers:

- Slither
- Aderyn
- static analysis
- detector output
- analyzer report
- reentrancy detector
- unchecked calls detector
- authorization printer
- data dependency
- call graph
- inheritance graph
- SARIF
- detector confidence
- false positive triage
- Foundry proof
- forge test
- DeFiHackLabs

Load:

- `10 - Tools/Web3/static-analysis-pipeline.md`
- `02 - Vulnerability Playbooks/Web3/Reporting/reportability.md`
- `02 - Vulnerability Playbooks/Web3/Foundry/poc-template.md`
- `02 - Vulnerability Playbooks/Web3/OWASP Alignment/scsvs-scstg-top10-map.md`

## OWASP Smart Contract Alignment

Triggers:

- OWASP Smart Contract Top 10
- SCSVS
- SCSTG
- SC01
- SC02
- SC03
- SC04
- SC05
- SC06
- SC07
- SC08
- SC09
- SC10
- smart contract testing guide
- OWASP mapping
- report taxonomy

Load:

- `02 - Vulnerability Playbooks/Web3/OWASP Alignment/scsvs-scstg-top10-map.md`
- `02 - Vulnerability Playbooks/Web3/Reporting/reportability.md`
- `02 - Vulnerability Playbooks/Web3/Foundry/poc-template.md`
