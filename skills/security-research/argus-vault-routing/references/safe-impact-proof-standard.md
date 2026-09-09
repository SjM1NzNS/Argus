# Safe impact proof standard

Use this reference when deciding how far to validate a bug bounty finding before reporting.

## Core rule

Argus standard is **not** “avoid proving impact.” It is:

> Prove the highest realistic impact with the minimum safe, non-destructive action, then stop.

The report should contain concrete capability evidence, not speculation, but the proof must avoid unnecessary data collection, destructive mutation, persistence, or pivoting.

When a safe validation path depends on local tooling and installation is feasible, do not stop at “tool missing.” Install/configure the needed tool (for example a container runtime for generated-image proof), record exact commands/output, and keep testing. Capture durable setup/fix steps, not transient absence.

Keep submission artifacts impact-focused. Discuss numeric/categorical severity separately with the user when useful, but do not include a severity/rating section in report artifacts unless the user explicitly asks for one.

## Safe proof patterns

| Impact class | Safe proof examples | Stop before |
|---|---|---|
| RCE / code execution | `whoami`, `id`, `hostname`, `pwd`, harmless marker file/output, owned canary read/write | shell persistence, env dumps, credential file reads, network pivoting |
| Credential exposure | fake canary secret, key class/source, masked presence, metadata-only identity/scope/expiry, redacted prefix/suffix | full token dumps, using keys to list/read production resources |
| Data access | owned/canary object, one smallest redacted sample if unexpectedly exposed | bulk collection, non-owned data mining, privacy-impacting screenshots |
| Deployment / supply chain | attacker-controlled input reaches trusted build/deploy/artifact staging; local/owned runtime marker | shipping malicious artifacts, mutating production deployments, public abuse |
| AI/agent tool impact | deterministic local tool trace, harmless tool call, marker output, owned canary | real secrets, cross-user data, persistent memory/tool poisoning beyond proof |

## Report wording

Use precise non-claims:

- “No real cloud deploy was performed.”
- “No real credentials were used; the key was an owned fake canary and is redacted.”
- “The RCE-style proof stops at `whoami`/marker output.”
- “No non-owned data was accessed or collected.”
- “If real sensitive data appears unexpectedly, the proof should stop and include only minimal redacted evidence.”

## Pitfall

Do not downgrade a finding merely because the proof is safe. A safe `whoami`/marker or metadata-only credential validation can be the correct end line for a high-impact capability. Conversely, do not overclaim beyond the safe proof: distinguish local/owned deployed-runtime execution from hosted production RCE, fake credential-source control from real secret access, and owned canary data from non-owned data disclosure.
