# CI Git-Metadata Trust Crossings

Use this reference when an untrusted CI job transfers a repository, cache, workspace, or `.git/` directory into a later job that has secrets, write tokens, release permissions, deployment credentials, or self-hosted access.

## Core rule

Treat `.git/` as **executable and credential-affecting state**, not as a commit-only data container.

It can carry:

- executable hooks such as `pre-push`, `pre-commit`, and `post-checkout`;
- local configuration, including `core.hooksPath`, credential helpers, transport commands, filters, and aliases;
- attacker-chosen refs, objects, index state, and remotes;
- repository metadata that changes the behavior of later `git`, package, build, or release commands.

A clean runner or fresh checkout does not restore the trust boundary if attacker-controlled Git metadata is overlaid afterward.

## Source-to-sink review

Build the complete chain:

1. **Untrusted execution:** identify the exact PR/fork-controlled command (`npm ci`, lifecycle scripts, build scripts, tests, generators, custom actions).
2. **Persistence primitive:** determine whether that command can write `.git/hooks`, `.git/config`, or another transferred path.
3. **Transfer:** inspect caches, artifacts, workspace reuse, container volumes, and job outputs. Record the exact path, key, save timing, restore timing, and branch/ref scope.
4. **Privileged restore:** confirm the attacker-produced archive or directory is restored after or over a nominally clean checkout.
5. **Sensitive sink:** locate the first later `git push`, `git commit`, checkout, package publish, release, deploy, or credential-setup command.
6. **Environment inheritance:** identify secrets and tokens present in that exact process environment. Hooks inherit environment variables from the parent Git process.
7. **Actor/preconditions:** state manual dispatch, collaborator checks, fork-maintainer-edit requirements, environment approvals, cache-key first-write conditions, and branch protection explicitly.

Do not promote a finding from “the workflow caches `.git/`” alone. Require attacker write access to the transferred metadata plus a reachable privileged command that consumes it.

## Cache-specific checks

- Read the workflow and the referenced cache Action implementation. Do not assume the Action filters Git metadata.
- Verify whether configured paths are passed directly to archive code.
- Verify archive/extraction semantics and whether executable mode is preserved on the runner OS.
- Check exact-key behavior and cache immutability. An immutable cache can still be exploitable on the first run for an attacker-selected commit SHA; a new head SHA commonly creates a new key.
- Confirm save and restore jobs share the cache visibility/ref scope and that dependency ordering guarantees save completes before restore.
- Distinguish a cache miss, exact hit, partial restore key, and pre-existing safe entry.

## Deterministic local proof

Use a fake token and local bare Git repository only:

1. Initialize a temporary bare repository and push a benign baseline commit.
2. Clone it as the untrusted job.
3. Create an executable `.git/hooks/pre-push` that writes only a fake canary environment variable to a temporary marker.
4. Create an attacker commit so the later push has work to do.
5. Archive `.git/` using the same family of semantics as the CI cache (on Linux, tar creation and overlay extraction).
6. Clone a fresh trusted checkout and assert the malicious hook is absent.
7. Extract the cached `.git/` over the trusted checkout and assert the hook exists and remains executable.
8. Set a fake token variable and perform a real `git push` to the temporary local bare repository.
9. Assert the hook observed the fake token and that the pushed ref equals the attacker commit.
10. Remove temporary files, verify the pinned source tree is clean, scan artifacts for credential patterns, and hash the final report/evidence bundle.

Safe hook shape:

```sh
#!/bin/sh
printf '%s' "$GH_TOKEN" > "$ARGUS_HOOK_MARKER"
```

Never trigger the real workflow, use a real token, push to GitHub, or exfiltrate anything.

## False-positive and reportability gates

- **Manual maintainer dispatch is a downgrade, not an automatic kill.** Ask whether the workflow is expressly designed to run PR code safely after dispatch and whether the defeated transfer boundary is its stated protection.
- **Fork write permission matters.** If Git cannot reach the pre-push stage, the hook may not execute. State maintainer-edit or authenticated-push requirements precisely.
- **Token impact is conditional.** Quote documented scopes, but do not claim branch-protection bypass or cross-repository reach without proof.
- **Separate exact duplicates from precedent.** A prior workflow vulnerability may establish that the project considers maintainer-triggered CI crossings security-relevant while still using a materially different primitive.
- **Intent evidence is not duplicate evidence.** A refactor claiming a clean trusted/untrusted split can strongly establish the security boundary even when it does not disclose the bypass.
- **Browser/package findings should not be bundled with unrelated CI findings.** Keep distinct actor models and remediation paths in separate reports.

## Remediation boundary

Preferred fix: transfer only validated expected outputs or a narrowly scoped patch, then stage and commit them inside a fresh trusted checkout before exposing credentials.

For generated images or artifacts:

- allow only regular files under exact expected directories;
- reject path traversal, symlinks, unexpected extensions, and extra entries;
- validate counts, sizes, and content signatures;
- let the trusted job create the commit.

Deleting `.git/hooks` alone is incomplete because attacker-controlled `.git/config` and other metadata can still affect command execution and credential handling. Avoid restoring untrusted Git metadata entirely.

## Evidence checklist

- [ ] Exact workflow commit and line-level source trace preserved.
- [ ] Cache/action implementation and resolved ref recorded.
- [ ] Fresh-checkout negative control passed.
- [ ] Restored hook exists and is executable.
- [ ] Fake token observed only by local canary.
- [ ] Local pushed ref equals attacker commit.
- [ ] Manual dispatch and all actor preconditions are prominent.
- [ ] Exact duplicate search saved; analogous precedent labeled separately.
- [ ] No real workflow, secret, network push, or target mutation occurred.
- [ ] Source tree clean; evidence JSON valid; secret scan and SHA-256 audit passed.
