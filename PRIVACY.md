# Privacy and Publication Policy

This repository is a deliberately reduced public export. A live security-research workspace must never be pushed wholesale.

## Threat model

A public backup can leak more than API keys. Sensitive material includes target names, private-program scope, unpublished findings, request/response captures, usernames, email addresses, local paths, account identifiers, browser state, report drafts, and Git history that once contained any of those items.

## Data classes

### Allowed

- Generic security methodology and safety policy
- Public-source citations and curated summaries
- Reusable playbooks, templates, evals, and deterministic scripts
- Placeholder values using RFC-reserved domains such as `example.invalid`
- Framework names and public tool/project names

### Never publish

- `.env`, OAuth/auth stores, API keys, tokens, passwords, cookies, TOTP seeds, recovery codes
- Personal names/contact details or source-machine home paths
- Private program names, briefs, domains, or invitations
- Target folders, reports, hypotheses, surface maps, approval queues, or hunt logs
- Raw evidence, HAR/HTTP captures, screenshots, browser profiles, Burp projects, tool output
- Hermes `USER.md`, `MEMORY.md`, session databases/transcripts, cron jobs, or gateway state
- Obsidian workspace/layout state or local plugin databases
- A Git history that predates sanitation

## Release process

1. Export from an explicit allowlist into a new directory.
2. Replace source-machine paths with portable environment-based paths.
3. Redact personal emails and target/program identifiers.
4. Review every included file class and the `SOURCE-MANIFEST.json`.
5. Run `scripts/verify_public_release.py`.
6. Run Gitleaks and TruffleHog against the working tree.
7. Initialize a brand-new Git repository only after sanitation.
8. Review `git status`, the staged diff, and scanner output before adding a remote.
9. Never reuse the live vault's Git history.

## Scanner limitations

Secret scanners primarily find credential-shaped strings. They do not reliably detect confidential prose, unpublished vulnerability details, target context, or every form of personal information. Human review is required.

## Reporting an accidental disclosure

Do not merely delete the file in a later commit. Rotate any exposed credential, remove sensitive Git history with an appropriate history-rewrite tool, force-push the rewritten repository where safe, and follow the affected platform/program's disclosure procedures.
