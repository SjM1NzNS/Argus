# OSS incomplete path validation and local-service proof

Use this reference when a security patch constrains a caller-supplied file path, URI, archive member, resource name, or local-service endpoint but may validate only lexical text rather than the resolved filesystem object.

## Core principle

Prove the **current mitigation differential**, not merely that an older release still has the original bug:

1. Pin the current product commit and the mitigation commit/PR.
2. Hash-compare every security-relevant product file copied into a harness.
3. Show the direct formerly-dangerous input is now rejected.
4. Change only the path-resolution property—leaf symlink, intermediate symlink, dangling link, junction/reparse point, mount alias, or race—and show the sink still reaches a disallowed resolved target.
5. Preserve an independent target/control pair and before/after hashes.

A packaged release that accepts the direct invalid control predates or lacks the mitigation. It is historical context, **not** evidence of a current-fix bypass. Use current source or a build proven to contain the fix.

## Source-to-sink map

Record the complete chain:

```text
request field / config path
  -> URI/path parser
  -> lexical scheme/host/basename/containment check
  -> unresolved path passed onward
  -> exists/create/read/parse/write operation
  -> OS link resolution
  -> resolved target effect
```

Inspect both existing-target and nonexistent-target branches. APIs often use different calls for them:

- existing target: `exists` -> read/parse -> rewrite;
- missing target: `create(recursive)` -> default content -> rewrite.

A dangling symlink can therefore prove arbitrary-path **creation** even when an existing-file proof only shows constrained rewriting.

## Current-fix differential harness

Use the exact product dispatcher or sink-owning method under a minimal inert listener/harness. Keep product files byte-identical; isolate only dependency/workspace plumbing.

Required controls:

| Case | Expected mitigation result |
|---|---|
| Direct path with invalid basename/location | Rejected; target absent |
| Ordinary legitimate path | Accepted |
| Attacker-owned link with approved lexical name to disallowed basename/location | Must be rejected; acceptance is bypass evidence |
| Independent negative-control file | Hash unchanged |

For each case retain:

- request method/path/query names, with sensitive values redacted;
- HTTP/status/body or direct API return;
- link owner and link target;
- server/request UID or equivalent principal;
- victim directory/file mode;
- target existence, owner, content class, and SHA-256;
- negative-control SHA-256.

Do not call a constrained serializer an arbitrary-byte write. State the exact grammar/content the attacker controls and what pre-existing target types the parser accepts.

## Local-service actor gate

Loopback TCP is host-local, not automatically user-local. When the original security model names “another local process,” test a separate lower-privileged account rather than only issuing requests as the server user.

Safe Linux pattern:

1. Run the synthetic server as the researcher account.
2. Create a victim directory mode `0700` and target mode `0600`.
3. Confirm the lower-privileged account cannot traverse/read/write the victim path.
4. Let that account create only a traversable attacker directory and symlink under `/tmp`.
5. Send the request as that account.
6. Confirm the write/create occurred with the server UID while direct lower-user access stayed denied.
7. Remove the temporary link/directory and stop the listener; verify ports closed.

Do not infer cross-user reachability merely from source. Conversely, do not dismiss a loopback endpoint as same-user-only without testing the OS socket boundary.

## Browser actor is a separate branch

Server acceptance of an `Origin` header through `curl` does not prove a modern browser will deliver a public/opaque-origin request to loopback. Test browser delivery separately under current Local/Private Network Access behavior.

- Use target-side state or hashes as ground truth; image `onerror` may mean either blocked delivery or a delivered non-image response.
- If the browser target hash is unchanged, kill the remote-webpage branch for that browser/version.
- Keep the lower-privileged local-process actor if independently proven.
- CORS response readability, Origin checks, CSRF, PNA/LNA, Fetch Metadata, and local-user authorization are distinct controls.

## Mitigation review

Lexical basename checks, `realpath` checks followed by ordinary reopen, and “reject symlink if seen” checks can remain TOCTOU-prone.

Prefer, in order:

1. do not accept raw client filesystem locations—map opaque capability handles to server-discovered legitimate files;
2. require an unguessable per-server capability for state-changing local APIs;
3. use race-resistant no-follow/open-at style file operations and validate the opened object, not only a prior pathname;
4. use `POST` plus browser request-integrity controls as defense in depth, not as local-user authorization.

Regression tests should cover leaf links, dangling links, intermediate-directory links, platform link types, and link-swap races.

## Report framing

Split the report into `The problem` and `Impact analysis`.

Use precise labels such as:

- `victim-context arbitrary-path creation with constrained content`;
- `existing valid-document reserialization and field modification`;
- `local cross-user confused deputy`;
- `incomplete resolved-path validation`.

Explicitly list non-claims: arbitrary bytes, RCE, credential disclosure, remote-web delivery, or hosted-service compromise unless separately proven.

Prior-art review must inspect the mitigation PR/body/comments/tests plus public issue/PR searches for symlink, canonicalization, path resolution, and the endpoint/sink name. The original fix is security-intent evidence; a matching follow-up may create duplicate risk.

## Finalization order

1. Complete current-source and actor differentials.
2. Run browser reachability separately and record negatives.
3. Clean listeners, temporary identities/links, and source-clone modifications.
4. Update authoritative target ledgers.
5. Generate verification results and evidence manifest.
6. Build the compact review/submission bundle last and verify its checksum/archive integrity.

A verifier should assert semantics, not `all(values())`: direct target absent, symlink target present, principals differ, requester access denied, positive hash changed, negative hash unchanged, source/harness hashes equal, duplicate queries recorded, and cleanup complete.

## Worked-example provenance

The 2026 Flutter DevTools review that produced this pattern used:

- mitigation intent: https://github.com/flutter/devtools/pull/9834
- current lexical validation: `devtoolsOptionsUri` local-file plus exact-basename check;
- sink: Dart `File.fromUri` / `existsSync` / `createSync` / `writeAsStringSync`;
- current-source direct control: HTTP 400 and no target;
- same current dispatcher with attacker-owned approved-name symlink: HTTP 200 and victim-context target creation;
- separate Chrome 150 opaque-origin negative control;
- released DevTools 2.57.0 classified as pre-current-fix context because it accepted even the direct invalid basename.

Retain the method, not the one repository, as the reusable lesson.
