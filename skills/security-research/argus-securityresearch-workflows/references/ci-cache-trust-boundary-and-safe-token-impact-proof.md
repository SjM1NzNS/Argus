# CI cache trust boundaries and safe token-impact proof

Use this reference when untrusted CI code can write data that a later trusted/secret-bearing job restores, downloads, extracts, sources, executes, or passes to Git/package tooling.

## Core review model

Treat cross-job caches and artifacts as attacker-controlled serialization boundaries, not inert build acceleration. Inventory both ordinary payload files and control-plane state:

- `.git/` metadata, hooks, `core.hooksPath`, remotes, credential helpers, config, and filters;
- package-manager caches with executable or lifecycle content;
- build outputs, generated scripts, tool config, compiler/plugin state, and PATH entries;
- symlinks, hard links, traversal paths, duplicate entries, modes, ownership, and archive extraction behavior.

For each transfer, trace:

1. actor controlling the producer job;
2. exact commands that execute untrusted code;
3. writable paths and archive roots;
4. cache/artifact key, version, scope, immutability, save conditions, and restore behavior;
5. consumer job identity, token/secret introduction point, and trusted sinks;
6. automatic consumers such as Git hooks, package lifecycle scripts, shell sourcing, plugins, and credential helpers.

A fresh checkout is not a security boundary if attacker-controlled metadata is restored over or beside it afterward.

## `.git/` cache primitive

Caching and restoring the entire `.git/` directory can carry executable behavior into a later job. A representative primitive is:

1. untrusted code writes an executable `.git/hooks/pre-push`;
2. a cache/archive preserves the hook and mode;
3. a trusted job performs a fresh checkout and then restores the poisoned `.git/`;
4. the job introduces a secret through `GH_TOKEN` or another environment variable;
5. `git push` automatically executes the restored hook, which inherits the job environment.

Do not reduce the problem to `.git/hooks` alone. `.git/config` may redirect `core.hooksPath`, modify remotes, configure credential helpers, or otherwise alter Git behavior.

## Required false-positive gates

Before promotion, verify all of the following:

- The producer actually executes lower-trust code; checkout alone is not execution.
- The attacker can write the transferred path before save.
- Cache save succeeds and the consumer restores the exact key/version.
- Cache scope permits the producer-to-consumer transfer. For GitHub Actions, distinguish run/ref scope from the commit checked out inside a job.
- Immutable-cache behavior is modeled: an existing same-key/version entry can block poisoning, while a fresh attacker-controlled commit may generate a fresh key.
- The consumer reaches the automatic execution sink after restore.
- The relevant secret is introduced before that sink and is not removed from the environment.
- Fork/head-repository availability, maintainer dispatch/review, approvals, environment gates, and branch protections are stated as prerequisites rather than hidden.
- Mutable external actions such as `owner/action@main` are identified as external dependencies, not treated as cryptographically pinned by the target repository revision.

## Safe proof ladder

Use the highest-fidelity non-destructive proof available, but label each layer precisely.

### Layer 1 — source-confirmed chain

Pin the target revision and cite exact source ranges for untrusted execution, archive creation, cache key/scope, trusted restore, secret introduction, and the final execution sink. Re-check ranges after every report edit. Avoid shorthand such as “maintainer selects a SHA” when the UI accepts a PR number and a separate action resolves the SHA.

### Layer 2 — local primitive reproduction

Use an isolated repository, local archive/cache model, fake canary token, and local bare remote. Prove:

- fresh checkout lacks the hook;
- archive restoration preserves the hook and executable mode;
- a real `git push` invokes it;
- the hook observes only a fake canary environment value;
- the expected commit still reaches the local remote;
- a negative control without the poisoned restore does not execute attacker code.

This supports wording such as:

> Source-confirmed and locally reproduced for archive/restore, Git-hook invocation, and fake-token inheritance primitives.

It does **not** support “end-to-end GitHub Actions confirmed” unless the real platform workflow was executed.

### Layer 3 — coordinated live confirmation

Do not exfiltrate, print, enumerate with, or mutate production using a real token merely to strengthen a bounty report. Exact live facts normally require owner cooperation:

- whether the secret exists and is nonempty;
- classic versus fine-grained token type;
- current scopes and repository allowlist;
- authenticated identity;
- ruleset or branch-protection bypass;
- package/release/deployment authority;
- private-repository visibility.

If the program explicitly authorizes a controlled confirmation, prefer a private fork or sandbox, a temporary least-privilege canary token, metadata-only identity/permission checks, and a harmless marker on a dedicated test branch. Revoke the token afterward. Presence-only output is safer than token output, but still requires authorization because attacker-controlled code is inspecting a production secret context.

## Impact framing

Separate these claims:

1. **Proven boundary impact:** attacker-controlled code executes in a trusted or secret-bearing job.
2. **Conditional credential impact:** the code can read a named secret if it is configured and nonempty.
3. **Documented intended authority:** repository comments or workflows describe expected token access.
4. **Unverified live authority:** actual scopes, repository access, bypass rights, private access, release rights, or package-publish capability.

Do not infer package publication from a GitHub PAT, branch-protection bypass from repository write access, or private-repository access from a broad-looking scope. These may depend on account grants, organization/SSO policy, rulesets, environments, registries, or separate credentials.

A defensible report statement is:

> An attacker can cause lower-trust code to execute where the named bot token is exposed, enabling compromise and abuse of that token up to its live permissions.

Stronger downstream claims require a concrete static consumer path, owner confirmation, or explicitly authorized coordinated proof.

## Report structure

State these separately:

- **The problem:** exact trust-boundary failure and automatic execution mechanism.
- **Impact analysis:** trusted-job code execution and conditional token compromise, bounded by live permissions.
- **Activation prerequisites:** maintainer action, cache save/restore, secret presence, and sink reachability.
- **Proof boundary:** what was source-confirmed, locally reproduced, and not tested live.
- **Negative controls and limitations:** cache miss, pre-existing immutable entry, missing token, failed build, missing head repository, protections not assessed.
- **Public prior:** exact duplicate versus analogous precedent; do not conflate them.

Avoid “technically confirmed” when only source plus local primitives were tested. Prefer explicit evidence labels.

## Remediation

Never transfer an attacker-writable control-plane directory into a secret-bearing job. Prefer:

1. export only exact expected data files or a narrow patch;
2. download/extract outside the repository;
3. reject traversal, absolute paths, symlinks, hard links, devices, duplicate names, unexpected modes, oversized files, and unexpected paths;
4. copy only exact allowlisted regular files into a fresh checkout;
5. fail closed on cache/artifact miss or validation failure;
6. introduce the token only after validation;
7. use least-privilege, repository-limited, short-lived credentials;
8. pin external actions to immutable commits.

“Delete `.git/hooks` after restore” is insufficient because other Git configuration can redirect or alter execution.

## Final adversarial review gate

Before calling the report ready, have a reviewer try to kill or downgrade it. Require explicit answers to:

- Is the actual secret configuration proven or only referenced?
- Are token scopes quoted from documentation, inferred, or live-confirmed?
- Are cache save, key/version match, scope, and restore success modeled?
- Is the external action immutable?
- Are workflow line ranges exact?
- Is PR-controlled execution stated precisely, including package-manager lifecycle prerequisites?
- Does remediation address archive extraction and all `.git` control-plane behavior?
- Do title/status/impact claims distinguish local primitive proof from a live platform run?

Regenerate hashes and final audit artifacts only after all report and ledger corrections are complete.
