# Public Release Audit

Audit timestamp: `2026-09-09T12:46:55Z`

This file records the checks performed on this sanitized snapshot before its fresh Git history was created. It is a release record, not a claim that future changes are safe.

## Scope

The release contains the reusable subset of the Argus framework:

- selected Obsidian system policy and routing documents;
- curated public-source summaries;
- Web2 and Web3 class-level playbooks;
- generic evaluations and templates;
- deterministic framework scripts and tests;
- five sanitized Hermes skills and supporting assets;
- a public learning-source registry.

The release was built by allowlist into a new directory. No source Git history was copied.

## Human/context audit

The live vault and original skill bundle were reviewed for more than credential-shaped strings. The review identified and excluded or generalized:

- active-program and target-specific skill references;
- program scope, account, entitlement, mission, and report state;
- unpublished candidate/finding narratives and internal identifiers;
- local home-directory and browser-profile paths;
- private invite inventories and runtime records;
- reports, raw evidence, logs, captures, workspace state, and tool output;
- the bulk third-party XSS payload corpus.

Generic safety procedures for credential handling, private-review package integrity, and private-invite state separation remain included because they contain no actual credentials, invitations, target records, or account data.

Publicly disclosed report numbers and public author/project names may remain as citations. They are source attribution, not local operator identity or private engagement data.

## Automated checks

Commands were run from the repository root.

### Built-in publication gate

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_public_release.py .
```

Result before Git initialization: `PASS` — 880 files scanned. The gate checks approved text-only file classes, forbidden runtime paths, source-machine paths, private-program identifiers, common credential formats, non-reserved email addresses, Hermes skill frontmatter, Markdown file links, and linked skill assets.

### Secret scanning

```bash
gitleaks detect --source . --no-git --redact --exit-code 1
trufflehog filesystem . --no-update --fail --only-verified
```

Final result: `PASS` — no Gitleaks findings and no verified TruffleHog findings. Gitleaks version: `8.30.1`. The installed TruffleHog build identifies itself as `dev`.

An earlier Gitleaks pass found three synthetic test/document fixtures that resembled secrets. The fixtures were rewritten to preserve their tests without storing contiguous credential-shaped strings, then both scanners were rerun.

### Syntax and data parsing

- Python parse: `PASS` — 31 files.
- Shell `bash -n`: `PASS` — 13 files.
- YAML parse: `PASS` — 6 files.

### Unit tests

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s 'vault/11 - Scripts/learning/tests' -p 'test_*.py'
```

Result: `PASS` — 152 tests, 2 skipped.

### Installer isolation test

`scripts/install.py` was exercised against temporary Hermes/config directories. Dry-run, clean copy installation of all five skills plus the registry, installed-file checks, and overwrite-guard dry-run all passed. No live Hermes or Argus configuration was modified.

### Integrity

`SOURCE-MANIFEST.json` records each included source file using source and sanitized SHA-256 digests. `CHECKSUMS.sha256` covers every public repository file except itself and `.git/`. Verify with:

```bash
python3 scripts/update_checksums.py --check
```

### Repository history

The release uses a newly initialized Git repository created only after sanitization. It does not inherit history from the operational vault or Hermes skill directory. No remote is configured by this backup process.

## Important limits

Secret scanners do not prove that prose is non-confidential, and a clean release can become unsafe after one edit. Before every public push:

1. inspect the complete staged diff;
2. rerun the publication gate and both external secret scanners;
3. regenerate and verify checksums;
4. confirm target, account, evidence, browser, and runtime directories remain absent;
5. confirm no private information exists in commit messages, author metadata, branch names, tags, or remotes.
