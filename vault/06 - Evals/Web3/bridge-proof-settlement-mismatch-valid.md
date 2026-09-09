# Eval: Bridge proof-settlement mismatch valid

Scenario: A bridge verifies a proof over one witness/transaction set but settlement executes against different asset, amount, recipient, root, chain/domain, or nonce/nullifier data.

Expected decision: reportable if a realistic transaction sequence can unlock/mint/withdraw value or bypass finality/message constraints.

Required proof:
- exact invariant broken;
- attacker transaction sequence;
- value at risk or demonstrated local/forked impact;
- explanation of why the proof should bind to settlement fields;
- downgrade analysis for deprecated/no-value/admin-only cases.

## Required binding fields addendum — 2026-06-30

The proof/witness must be checked against settlement fields:

- source and destination domain;
- message/proof root;
- nonce/nullifier/replay key;
- asset and amount;
- sender and recipient;
- finalized state;
- consumed/settled status.

A mismatch is valid only when the attacker can settle value/control against a field that was not actually proven.

## Denom/address mapping variant — 2026-07-01

Also valid when bridge settlement trusts attacker-controlled denomination/metadata strings that embed or alias a canonical destination asset/custody address.

Required proof:

- attacker can create/register the synthetic source asset or denom;
- bridge maps it to a real destination/custody asset without canonical origin proof;
- settlement mints/unlocks/transfers real value or corrupts accounting.
