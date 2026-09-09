# Evidence hygiene when no Git worktree exists

Use this reference when closing a source-first mission, reconciling request ledgers, or checking whether retained evidence is safe to preserve.

## 1. Discover repository state before running Git hygiene

Do not assume the vault or target directory is a Git worktree. Check the exact candidate roots first with `git -C <path> rev-parse --show-toplevel` and preserve the exit code.

- If a worktree exists, run status/diff checks from the returned top level.
- If no worktree exists, state that Git status/diff is **not applicable**. Never interpret empty stdout from a failed Git command as a clean tree.
- A filesystem-hygiene result and a Git-clean result are different claims.

## 2. Filesystem fallback verification

When Git is unavailable or irrelevant, verify the mission directories directly:

1. enumerate the exact governed mission roots;
2. require restrictive file modes for raw/private evidence;
3. flag symlinks and unexpected file types;
4. parse every JSON artifact;
5. reconcile request counts, status counts, and response-byte totals from the actual ledger schema;
6. confirm approval rows have no active/in-progress residue;
7. check that bounded helper processes have exited;
8. write a dated hygiene-verification artifact and rerun the checks after that final write.

Do not call the filesystem “clean” merely because no Git repository exists. Report the checks actually performed.

## 3. Inspect ledger schemas before aggregating

Generated ledgers are not guaranteed to be flat lists. Before arithmetic, inspect types and keys. Common forms include:

```json
{"requests": [{"http_status": 200, "bytes": 123}]}
```

and flat entries using alternate names such as `status_code`, `response_bytes`, or `body_bytes`.

A verifier should normalize only observed aliases, for example:

- status: `http_status` or `status_code`;
- size: `bytes`, `response_bytes`, or `body_bytes`;
- entries: top-level list or a documented `requests` list.

If the schema differs, inspect it and fix the verifier. Do not report a target inconsistency from a local `KeyError`, and do not keep retrying guessed schemas without first reading the structure.

## 4. Sanitize raw authentication-adjacent headers

Mode `0600` is necessary but not sufficient. Before final retention, scan raw headers and bodies for:

- `Authorization` and API-key values;
- `Set-Cookie` values;
- opaque login/vouch/OAuth state in redirect queries;
- CSRF tokens, JWTs, private keys, cloud access-key IDs, and client-secret assignments.

For authentication-adjacent response evidence, preserve the security-relevant structure while redacting volatile capability material:

- cookie name and attributes, but value as `[REDACTED]`;
- redirect scheme, host, and path, but sensitive query/fragment data as `[REDACTED]`;
- header presence and response metadata without printing secret plaintext to terminal output, notes, or reports.

Hash the sanitized retained artifact, keep it restrictive, and update completion notes so they do not claim an artifact is unsanitized after redaction. If an evidentiary original must be retained under an approved procedure, isolate it outside ordinary report/vault promotion paths and never commit or quote it.

## 5. Final closure assertions

A useful closure report records:

- governed roots and file count;
- mode and symlink exceptions;
- JSON/schema validation errors;
- normalized request/status/byte reconciliation;
- sensitive-signature counts after redaction;
- active bounded processes;
- approval rows still in progress;
- whether Git checks ran, were clean, failed, or were not applicable.

Run the final verifier only after the last evidence, completion, checkpoint, and hygiene-report write. The act of writing the verification report can itself introduce a wrong mode or stale manifest, so verify once more afterward.
