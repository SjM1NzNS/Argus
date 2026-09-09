---
type: source-summary
status: promoted
created: "2026-07-03"
pass: "B"
sources:
  - "https://github.com/crytic/slither"
  - "https://github.com/Cyfrin/aderyn"
  - "https://github.com/SunWeb3Sec/DeFiHackLabs"
  - "https://github.com/Cyfrin/solskill"
---

# Pass B Web3 Toolchain Source Summary

## Scope

Pass B reviewed Web3 tooling and corpus sources for Argus class-level promotion:

- Slither: Solidity/Vyper static analysis and detector/printer taxonomy.
- Aderyn: Cyfrin static analyzer and report-oriented workflow.
- DeFiHackLabs: Foundry reproductions of real exploit classes.
- Solskill: Solidity/security workflow guidance and skill-structured audit lessons.

Selected source files were saved under:

`01 - Learning/Inbox/manual-20260703-pass-b-web3-toolchain/`

## Promoted lessons

1. Static-analysis output is a routing and triage accelerator, not proof by itself.
2. Slither and Aderyn should be run as independent opinions; agreement increases confidence, disagreement creates manual-review tasks.
3. Detector findings must map to Argus Web3 playbooks and then to executable proof requirements.
4. DeFiHackLabs should be used as a root-cause and invariant corpus, not copied as exploit recipes.
5. Solskill-style secure-development rules are useful for review checklists, but reportability still requires unprivileged path plus impact.
6. Foundry is the default executable proof harness for Web3 findings.

## Tool install result

Installed/verified locally:

- Slither `0.11.5` via `uv tool install slither-analyzer`.
- Aderyn `0.6.8` via checksum-verified GitHub release tarball.
- Foundry `1.7.1` (`forge`, `cast`, `anvil`) via checksum-verified GitHub release tarball.

## Promotion outputs

- `10 - Tools/Web3/static-analysis-pipeline.md`
- `00 - System/external-web3-toolchain-source-review-2026-07-03.md`
- `06 - Evals/Web3/web3-static-analysis-toolchain-eval-scenarios.md`
- Web3 skill-index static-analysis routing triggers.
