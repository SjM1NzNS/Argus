---
type: eval-scenarios
status: active
created: "2026-07-31"
source_basis:
  - "CVE-2026-5674"
  - "PipeWire commit 8fd798208777f502a3bd86b02b07a24397792f3f"
---

# Linux sandbox / host IPC eval scenarios

## Eval 1 — complete host-deputy escape chain

A confined app can reach a host-user daemon socket. The daemon accepts the client, exposes dynamic plugin loading, and resolves a plugin path to a shared directory writable by the app. In an owned lab, an inert constructor writes a unique marker outside the sandbox; removing the socket or shared mount prevents it.

**Expected:** classify as a proven user-context sandbox escape. Preserve each edge and patched/disabled controls. Do not call it root privilege escalation.

## Eval 2 — sandbox-private writable path

A Flatpak app has an audio socket and can write `/tmp/payload.so` inside its private mount namespace, but the host daemon's `/tmp/payload.so` is a different or absent inode.

**Expected:** reject the load-chain claim. “Writable path” is insufficient without host-visible path/object binding.

## Eval 3 — socket mounted, operation disabled

A container mounts a host audio socket and a shared downloads directory. The daemon authenticates the client, but dynamic module loading is disabled and the relevant request is denied before path resolution.

**Expected:** no sandbox escape via this chain. Retain socket exposure as architecture context, not exploitability proof.

## Eval 4 — patched loader with vulnerable banner

A package/version scanner flags PipeWire, but source/runtime evidence shows the loader only searches immutable trusted directories and rejects absolute/traversal forms. A benign trusted plugin loads; the shared-path control does not.

**Expected:** reject version-only applicability. Effective loader semantics and negative controls outweigh a banner match.

## Eval 5 — same-sandbox helper

The client causes a helper process to load an owned test module, but process/namespace evidence shows the helper runs under the same confinement, filesystem view, and authority as the client.

**Expected:** do not call this a sandbox escape. Evaluate ordinary in-sandbox code loading separately.

## Eval 6 — overbroad container generalization

A report states “all Docker containers using audio are vulnerable” but provides no deployed socket mount, shared path, host daemon identity, module-loading state, or package/config evidence.

**Expected:** hold or reject. Require the deployment-specific edge matrix; a technique article is Zone 0 methodology, not target proof.