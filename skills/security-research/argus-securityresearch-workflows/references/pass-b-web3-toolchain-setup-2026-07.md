---
type: skill-reference
status: active
created: "2026-07-03"
---

# Pass B Web3 Toolchain Setup Pattern

Use this reference when repeating or repairing Pass B-style Web3 toolchain/source promotion.

## Sources

- `crytic/slither`
- `Cyfrin/aderyn`
- `SunWeb3Sec/DeFiHackLabs`
- `Cyfrin/solskill`

## Safe install pattern

Prefer verified local-user installs:

```bash
uv tool install slither-analyzer
```

For Aderyn and Foundry, prefer release tarballs with checksum verification over piping remote installers to shell.

Working baseline from 2026-07-03:

- Slither `0.11.5`
- Aderyn `0.6.8`
- Foundry `1.7.1`

Aderyn `cargo install aderyn --locked` failed on this host because upstream `svm-rs-builds` generated duplicate Solidity version constants. Use the verified binary release path instead.

## Promotion checklist

1. Fetch selected source docs/tree excerpts into `01 - Learning/Inbox/<run-label>/`.
2. Create a source summary under `01 - Learning/Source Summaries/`.
3. Create a system source review note under `00 - System/`.
4. Add/update `10 - Tools/Web3/static-analysis-pipeline.md`.
5. Patch `00 - System/web3-skill-index.md` with static-analysis/tool-output triggers.
6. Patch Web3 reportability and Foundry proof templates.
7. Add eval scenarios under `06 - Evals/Web3/`.
8. Update changelog.
9. Verify all `Load:` references exist, files are non-empty, no placeholders remain, and tool versions execute.

## Reportability rule

Static-analysis output is a lead. A reportable Web3 finding still needs realistic actor model, in-scope deployment/version, manual source review, executable Foundry/local/fork proof, positive and negative controls, and measurable protocol/user/control impact.
