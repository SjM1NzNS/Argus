# Descriptor-Stable Offline Run Phases

Use this note when an offline research cascade reads an existing run directory and later creates phase outputs such as ledgers, ingestion manifests, or closure manifests.

## Core invariant

Path validation is not a stable authorization boundary. Resolving or checking a run-directory pathname and then reopening files through that pathname leaves a replacement window. Every phase must retain descriptor identity from admission through its final write and success check.

This is a fail-closed transaction boundary, not a sandbox between mutually hostile processes sharing one effective UID. A same-UID process already has equivalent authority over the user-owned private tree and may race after any final identity check. Claims must therefore stay narrow: no write through the declared run name before atomic publication; detected run/parent replacement fails the phase; rollback touches only still-owned inodes; and success binds the identities observed at the final checks.

## Required phase boundary

### New-run publication

1. Open and validate the private parent component-by-component with `O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC`; retain its descriptor and `(st_dev, st_ino)`.
2. Create an unpredictable staging directory relative to that descriptor, record its no-follow `(st_dev, st_ino)`, force that exact entry to mode `0700` despite caller `umask`, then open it with `O_DIRECTORY | O_NOFOLLOW` and require descriptor identity to match. Track the inode before open so pre-open failures can remove only the exact invocation-owned empty entry; never remove a replacement.
3. Write every prepared artifact relative to the staging descriptor. Do not create or open the caller-declared run name for writes.
4. Verify the staging name still identifies the retained inode, then publish it with an atomic no-replace rename such as Linux `renameat2(RENAME_NOREPLACE)`. Fail closed if this primitive is unavailable or the destination exists; never emulate it with check-then-rename.
5. Revalidate both the published run entry and the parent pathname identity before success. On failure, remove only invocation-owned artifacts and the exact staging/published inode through retained descriptors.

### Existing-run phases

1. Lexically normalize the requested run path without resolving through symlinks.
2. Open the parent path component-by-component with `O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC`.
3. Verify the parent is owned by the effective user and has no group/other permission bits; retain its `(st_dev, st_ino)`.
4. Open the run entry relative to the retained parent descriptor with `O_DIRECTORY | O_NOFOLLOW`.
5. Verify the run directory is owned by the effective user and mode-private; retain `(st_dev, st_ino)` from `fstat`.
6. Perform **all** run-local reads and writes relative to the retained run descriptor. This includes pinned manifests, prepared artifacts, ledgers, nested evidence manifests, and evidence artifacts.
7. For nested relative paths, reject absolute paths plus `.`/`..`; open each intermediate directory relative to the prior descriptor with `O_DIRECTORY | O_NOFOLLOW`, then open the final regular file with `O_NOFOLLOW`. Do not fall back to `run_path / reference`.
8. Create phase outputs with `O_CREAT | O_EXCL | O_NOFOLLOW`, mode `0600`, relative to the retained run descriptor.
9. Immediately before reporting success, require both: the run entry relative to the retained parent still identifies the original run `(st_dev, st_ino)`; and reopening the lexical parent pathname identifies the retained parent inode.
10. Track every invocation-owned output by the `(st_dev, st_ino)` returned from its open descriptor. On failure, remove that name only if a fresh descriptor-relative no-follow stat still identifies the same inode. Never unlink via the possibly replaced pathname, remove a concurrent replacement, or remove a pre-existing file.
11. Close descriptors in `finally` blocks.

## Same-buffer integrity

Open each untrusted regular file once, enforce its byte ceiling while reading, and parse plus hash the same admitted byte buffer. Descriptor stability does not replace exact-byte pinning; both are required.

## TDD race probes

For prepare, inject a concurrent private directory at the caller-declared run name after staging begins but before publication. Assert atomic no-replace publication fails, the concurrent sentinel survives, no prepared artifact enters the concurrent directory, and the invocation-owned staging inode is cleaned. Separately replace the published run entry before final verification.

For every phase, rename the already-open private parent aside and recreate a private directory at the original parent pathname before the phase's final write or verification:

- Assert the phase fails on parent-identity change rather than returning a stale pathname.
- Assert no output appears in the replacement parent.
- Assert invocation-owned output is removed from the displaced original through retained descriptors.

For existing-run phases, also inject run-entry replacement immediately before the first phase output write:

- Rename the original run directory aside.
- Move a private replacement directory into the original pathname.
- Put a sentinel in the replacement.
- Assert the phase fails with an identity-change error.
- Assert no output appears in the replacement.
- Assert the replacement sentinel survives.
- Assert invocation-owned outputs are removed from the displaced original directory.
- Assert pre-existing artifacts in either directory survive.

Cover run-entry and parent-path replacement independently for ingestion and closure. Also inject a post-first-write exception to exercise rollback rather than only the success-time identity check.

## Release-seal discipline

A checksum seal is valid only after all blocker probes and the complete verification matrix are green. If a blocker is found after sealing:

1. Delete or explicitly invalidate the seal immediately.
2. Treat every audit dispatched against it as obsolete.
3. Complete RED-GREEN-REFACTOR and rerun the full matrix.
4. Generate a new external checksum manifest.
5. Verify it with `sha256sum -c`.
6. Dispatch fresh-context, read-only audits that stop on any checksum mismatch.

Never describe an invalidated or pre-fix audit as release approval.
