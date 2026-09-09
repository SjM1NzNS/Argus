---
type: technique-extraction
status: draft
created: "2026-06-29 11:53"
domain: web3
run: "2026-06-29-learning-dry-run"
---

# Web3 Technique Extraction — Argus Learning Dry Run

## Top 5 extracted Web3 lessons

### 1. Solidity external calls require explicit state and reentrancy reasoning

- Protocol type: other/reentrancy
- Root cause: reentrancy
- Attacker path: unprivileged or callback-capable caller
- Impact: stolen funds/frozen funds if invariant breaks
- Invariant/test/PoC idea: Model withdraw/transfer hooks and check-effects-interactions; create Foundry callback PoC only against local/fork scope.
- False-positive notes: Non-impactful reentrancy or admin-only path should be downgraded.
- Reportability lesson / skill patch recommendation: Patch Reentrancy playbook with callback/precondition/economic-impact gate.

### 2. Arithmetic and rounding must be tied to economic impact

- Protocol type: vault/lending/AMM
- Root cause: rounding/precision
- Attacker path: unprivileged user can influence share/asset math
- Impact: profit/loss/dust only depending magnitude
- Invariant/test/PoC idea: Invariant: value conservation within expected rounding bound; fuzz decimals and small amounts.
- False-positive notes: Dust-only or unrealistic liquidity assumptions are false positives.
- Reportability lesson / skill patch recommendation: Patch Rounding & Precision and Share Accounting with impact threshold gates.

### 3. Oracle issues require realistic manipulation path

- Protocol type: lending/AMM/oracle
- Root cause: oracle manipulation
- Attacker path: attacker can move referenced price or exploit stale feed
- Impact: stolen funds/insolvency/liquidations
- Invariant/test/PoC idea: Invariant: collateralization remains safe under accepted oracle assumptions; test stale/decimals/TWAP windows.
- False-positive notes: Single-block fantasy manipulation or impossible liquidity should be rejected.
- Reportability lesson / skill patch recommendation: Patch Oracles playbook with liquidity/cost/heartbeat proof requirements.

### 4. Access control findings need non-privileged path or accepted trust-boundary break

- Protocol type: governance/upgradeability/operations
- Root cause: access control
- Attacker path: unprivileged or low-privileged actor reaches sensitive function
- Impact: control compromise or funds at risk
- Invariant/test/PoC idea: Static onlyOwner sightings are not findings; test role boundaries and initializer exposure.
- False-positive notes: Admin can do admin things is invalid unless policy accepts centralization risk.
- Reportability lesson / skill patch recommendation: Patch Web3 Access Control false positives with admin-only rejection rule.

### 5. Incident postmortems are impact realism sources, not direct bounty templates

- Protocol type: bridge/lending/vault/other
- Root cause: economic design flaw/validation failure
- Attacker path: varies by incident
- Impact: real-world loss category
- Invariant/test/PoC idea: Use Rekt/Immunefi to extract invariants, attacker paths, and severity realism; convert to eval cases before playbook updates.
- False-positive notes: Postmortem lacks scoped code and may include privileged/key compromise outside bounty scope.
- Reportability lesson / skill patch recommendation: Patch learning engine/Web3 reporting with postmortem-to-bounty translation filter.

