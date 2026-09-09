# Materializing a cross-platform shortlist into target workspaces

Use this reference after a public-program screening note has been saved and the user asks to create folders/workspaces for the selected programs. This is workspace preparation only; a shortlist is not an authorization or scope contract.

## Interpretation and naming

- Unless the user narrows the request, “all these programs” means every selected candidate in the saved shortlist, not rejected or suspended near-misses.
- Recover the exact list from the saved shortlist rather than reconstructing names from memory.
- Use platform-qualified folder names to avoid collisions and preserve provenance:

```text
03 - Targets/<Platform> - <Program>/
$HOME/BurpSuite/<Platform> - <Program>/
```

Keep Unicode and official capitalization when the filesystem supports them. Do not create sibling storefronts that were intentionally excluded as shared-code duplicates.

## Standard target tree

Create this structure for each selected program:

```text
<Platform> - <Program>/
├── target.md
├── scope.md
├── scope-contract.yaml
├── scope-domains.txt
├── surface-map.md
├── hypotheses.md
├── approval-queue.md
├── agent-log.md
├── checkpoint.md
├── evidence/
├── burp/
├── source-notes/
└── tool-output/
    ├── http/
    ├── js/
    ├── github/
    ├── screenshots/
    ├── endpoints/
    ├── secrets/
    ├── scans/
    └── missions/
```

Also create the mirrored Burp directory under `$HOME/BurpSuite/`.

## Initialization state

Populate the command-center files with real shortlist metadata:

- platform, official program name, direct program URL;
- selection date, score, platform rank, and overall rank when present;
- link back to the shortlist;
- the parked first-pass qualification lane;
- an initialization log entry stating that no target contact occurred.

Do **not** copy the directory card into scope. Initialize both `target.md` and `scope-contract.yaml` with:

```yaml
status: draft
hunting_enabled: false
scope_verified_at: null
```

Leave allowed assets, forbidden assets, testing rules, rate limits, account model, and report requirements empty until the live brief is imported and rechecked. `scope-domains.txt` should be empty, not filled with guessed brand domains. A parked qualification lane belongs in `hypotheses.md`, but it is not active until scope is verified.

## Safe bulk creation

For many targets, use an idempotent manifest-driven initializer rather than hand-typing trees:

1. Build a local metadata list from the saved shortlist.
2. Create directories with `exist_ok` semantics.
3. Refuse to overwrite existing command-center files; report skipped paths.
4. Generate all files from one standard template so guards and links remain consistent.
5. Remove temporary initialization artifacts after verification.

This pattern scales without weakening the rule that existing hunt state must never be silently replaced.

## Follow-up: “Are all hunting enabled?”

Do not answer this from the generated `hunting_enabled: false` fields: those fields are local safety guards, not platform state. Load `argus-vault-routing` and follow `references/live-program-hunting-status-verification.md` there. Perform a fresh dated check and distinguish platform submission availability, researcher eligibility/practical access, and local Argus scope activation. Keep every local contract disabled until that target's exact live scope is imported, even when all platform programs are open.

## Inventory and backlink

Write a central inventory beside the shortlist, for example:

```text
03 - Targets/Program Shortlists/target-workspace-inventory-YYYY-MM-DD.md
```

The inventory should list platform, rank, program, score, relative link to `target.md`, and mirrored Burp path. Add a backlink from the shortlist to the inventory and state that every contract remains draft.

## Verification gate

Before reporting success, check deterministically:

- exact expected target count and platform distribution;
- every root, standard subdirectory, command-center file, and mirrored Burp directory exists;
- every scope contract parses as YAML;
- every contract has `hunting_enabled: false`;
- no generated file contains `TODO` or `TBD` placeholders;
- every inventory row resolves to a real `target.md`;
- shortlist and inventory link to each other;
- no pre-existing file was overwritten;
- temporary initializer files were removed.

Report concrete counts: target roots, subdirectories, initialized files, Burp directories, valid contracts, and verification problems. Do not claim the programs are hunt-ready; say the **workspaces** are ready for live-scope import.

## Common pitfalls

1. **Creating empty roots only.** Evidence and tool-output routing should be ready before the first hunt.
2. **Activating every shortlisted target.** Portfolio candidates remain Zone 0 leads until individually scoped.
3. **Treating shortlist URLs as scope.** Reopen the direct live brief and import exact assets/rules.
4. **Flat unqualified names.** Platform prefixes prevent collisions and make inventories legible.
5. **Overwriting existing state.** Bulk initialization must be additive and idempotent.
6. **Populating guessed domains.** An empty scope file is safer and more accurate than brand-based inference.
7. **No central inventory.** Without a backlink, folders become disconnected from the scoring rationale.
