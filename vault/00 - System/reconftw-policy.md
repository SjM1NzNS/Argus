# ARGUS RECONFTW POLICY

reconFTW is a recon automation framework and tool bundle.

Argus treats reconFTW as a surface discovery engine, not a report generator.

Default reconFTW posture:

- passive or low-noise first
- scope contract required
- target-specific output folder
- no broad active scanning unless scope permits
- no vuln-scan mode by default
- no high-volume fuzzing by default
- no out-of-scope assets
- no scans against third-party IdPs/CDNs/support/status pages unless explicitly in scope

Every reconFTW result must pass:

scope check → surface classification → skill routing → hypothesis → validation plan → evidence gate

reconFTW output may create:

- live host inventory
- technology map
- endpoint list
- JS collection
- screenshot set
- takeover candidate
- cloud/storage clue
- public code clue
- hypothesis seed
- approval queue item

reconFTW output must not directly create a report.
