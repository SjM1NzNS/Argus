# Filesystem resource-loader symlink confinement and reportability

Use when a library claims that file/resource access is restricted beneath a configured root but accepts a host-backed filesystem such as Go `os.DirFS`.

## Primitive test

Lexical validation is not canonical containment. `path.Clean`, prefix checks such as `references/`, and `fs.Sub` can reject `../` while still allowing a leaf or intermediate symlink to resolve outside the intended root.

For an owned local proof:

1. create a temporary root with a valid resource/skill manifest;
2. create a fake marker outside that root;
3. place a relative symlink under an allowed directory pointing to the marker;
4. call the product's list and load APIs—not `os.ReadFile` directly;
5. assert that listing presents the symlink as an ordinary resource and loading returns the outside marker;
6. if the product has eager/complete preload, construct that wrapper, remove the symlink after initialization, and prove the cached outside-root marker remains readable; this demonstrates that exposure can happen during startup rather than only after a model explicitly requests the resource;
7. use leaf and intermediate-directory symlink negative/regression cases;
8. preserve the probe source/output first, verify the copies, then remove temporary test hooks and rerun package tests;
9. verify a clean clone. Keep evidence-copy and deletion operations separate when deletion is approval-gated so a blocked cleanup does not also prevent evidence preservation.

Use fake canaries only; never read a real credential or non-owned file.

## Data-flow gate

Map the complete flow:

```text
resource path from caller/model
  -> lexical clean/prefix validation
  -> fs.FS Open/Walk/Stat
  -> host filesystem symlink resolution
  -> outside-root bytes
  -> caller/model/tool result
```

Confirm whether content reaches a model-callable function, renderer, archive, build context, or deployment artifact. A low-level `Open` primitive alone is not the final impact claim.

## Trust and actor-model gate

A real confinement bypass can still be unreportable if the same fully trusted application author controls the filesystem tree. Before promoting, establish a lower-trust resource-delivery path such as:

- official gallery/marketplace/install command;
- archive/template/import flow;
- separately cloned skill or plugin pack;
- shared repository/workspace reviewed under a narrower visible root;
- multi-tenant resource store;
- generated or remotely synchronized resource directory.

If no such path exists, record the primitive as **HOLD** rather than claiming arbitrary file read. Model control of `resource_path` does not substitute for explaining how the escape symlink appears.

For local developer tools, also apply two mandatory pre-submission gates:

1. **Intended-boundary gate:** identify evidence that the product or program is designed to enforce the asserted boundary. A cross-UID or OS-permission differential proves incremental filesystem authority mechanically, but it does not by itself prove that the product treats other local users/processes as an in-scope security boundary.
2. **Equivalent-capability gate:** compare the exact prerequisite with the claimed impact. If the attacker already needs general local code execution plus filesystem observation/manipulation and can ordinarily achieve equivalent compromise through simpler means, keep the primitive technically valid but **HOLD** it unless a product-native lower-trust ingress changes that comparison.

Evidence that can reopen such a held primitive includes a realistic remote-origin route, a sandboxed process that cannot otherwise reach the victim data, an imported/shared project or workspace workflow, or a supported multi-user deployment with an explicit isolation expectation. State the strongest likely triager objection in the report package and answer it with evidence instead of only restating the race mechanics.

## Go-specific caution

`os.DirFS(root)` is convenient, but its documentation does not make `root` a symlink-resolving security boundary. A generic `fs.FS` interface also cannot promise host-path containment unless the implementation contract explicitly rejects or safely resolves symlinks.

Safer designs include:

- rejecting symlinks at every path component;
- opening relative to a trusted directory descriptor with no-follow semantics;
- canonicalizing and verifying the final target remains beneath a canonical root, while handling time-of-check/time-of-use races;
- copying/importing resources into a symlink-free immutable store before exposure.

## Report framing

Separate:

- **proven primitive:** allowed lexical resource path returned an owned outside-root marker;
- **data flow:** product API/model/tool received that content;
- **missing or proven ingress:** how a lower-trust actor places the symlink;
- **non-claims:** no real secret, no non-owned data, no universal arbitrary read without a predictable target and delivery path.

External advisories about symlink scope bypasses are methodology context only. The product's own source and runtime proof establish the finding.
