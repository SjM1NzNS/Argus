---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.060376+00:00
source_quality: 10
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# Security Considerations — Solidity 0.8.36-develop documentation

- URL: `https://docs.soliditylang.org/en/latest/security-considerations.html`
- Source group: `web3_core_theory`
- Content chars: `20361`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Basics Introduction to Smart Contracts Solidity by Example Installing the Solidity Compiler Language Description Layout of a Solidity Source File Structure of a Contract Types Units and Globally Available Variables Expressions and Control Structures Contracts Inline Assembly Cheatsheet Language Grammar Compiler Using the Compiler Analysing the Compiler Output Solidity IR-based Codegen Changes Internals Layout of State Variables in Storage and Transient Storage Layout in Memory Layout of Call Data Cleaning Up Variables Source Mappings The Optimizer Contract Metadata Contract ABI Specification Advisory content Security Considerations Pitfalls Private Information and Randomness Reentrancy Gas Limit and Loops Sending and Receiving Ether Call Stack Depth Authorized Proxies tx.origin Two’s Complement / Underflows / Overflows Clearing Mappings Internal Function Pointers in Upgradeable Contracts Minor Details Recommendations Take Warnings Seriously Restrict the Amount of Ether Keep it Small and Modular Use the Checks-Effects-Interactions Pattern Include a Fail-Safe Mode Ask for Peer Review List of Known Bugs Solidity v0.5.0 Breaking Changes Solidity v0.6.0 Breaking Changes Solidity v0.7.0 Breaking Changes Solidity v0.8.0 Breaking Changes Additional Material NatSpec Format SMTChecker and Formal Verification Yul Import Path Resolution Resources Style Guide Common Patterns Resources Contributing Language Influences Solidity Brand Guide Keyword Index Solidity Security Considerations Edit on GitHub Security Considerations  While it is usually quite easy to build software that works as expected, it is much harder to check that nobody can use it in a way that was not anticipated.
- Pitfalls  Private Information and Randomness  Everything you use in a smart contract is publicly visible, even local variables and state variables marked private .
- Using random numbers in smart contracts is quite tricky if you do not want block builders to be able to cheat.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
