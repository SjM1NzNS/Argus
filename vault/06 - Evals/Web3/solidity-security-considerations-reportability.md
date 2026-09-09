# Eval: Solidity security considerations reportability

Valid when:

- deployed in-scope contract/version is identified;
- vulnerable Solidity/EVM behavior is tied to real protocol state;
- attacker path is unprivileged or accepted low-privileged;
- transaction sequence or executable PoC demonstrates invariant break;
- impact is measurable value loss, freeze, insolvency, unauthorized control, or protocol-specific accepted impact.

Reject or downgrade when:

- finding is compiler-theory only with no deployed impact;
- admin-only or expected privileged behavior;
- unrealistic oracle/liquidity/timing assumptions;
- gas-only/dust-only impact;
- no transaction sequence or state proof.
