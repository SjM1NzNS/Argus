# Argus Security Research Framework

Argus is an authorization-first security-research command center built from three cooperating layers:

1. an **Obsidian knowledge base** containing operating policy, Web2/Web3 vulnerability playbooks, evidence gates, reusable templates, evaluations, and curated source summaries;
2. **Hermes Agent skills** that turn that knowledge into progressively disclosed, repeatable workflows; and
3. **deterministic scripts** for bounded learning ingestion, evidence handling, browser isolation, and offline research cascades.

This repository is a sanitized public backup of the reusable framework. It is not a backup of active hunts. It deliberately excludes targets, accounts, raw evidence, browser profiles, Burp projects, secrets, private program data, reports, agent logs, and local Hermes memory/session state.

> Use only on systems and programs you own or are explicitly authorized to test. Program scope and rules always override this repository.

## Why Argus exists

Security research often fails because reconnaissance, hypotheses, tests, evidence, and reporting are kept in disconnected tools. Argus keeps them in one routed knowledge system. The framework emphasizes:

- scope and authorization before testing;
- source-first surface mapping rather than broad endpoint guessing;
- hypothesis-driven tests with one changed variable and a negative control;
- minimal, reproducible, triage-resistant evidence;
- independent skeptic and impact review before calling a lead a vulnerability;
- progressive disclosure, so an agent loads only the playbooks relevant to the current surface;
- learning from authoritative and practitioner sources without auto-promoting unreviewed material; and
- strict separation between reusable knowledge and sensitive runtime evidence.

Argus does **not** make a finding true merely because a scanner, model, or payload produced an interesting result. A reportable finding must survive scope, false-positive, exploitability, impact, and downgrade review.

## Capabilities

### Research orchestration

- Scope intake, asset classification, authorization zones, and stop conditions
- Target initialization templates and evidence-directory conventions
- Dynamic Web2/Web3 playbook routing from a discovered surface or hypothesis
- Specialist-agent dispatch with bounded context and structured output
- Source-first JavaScript/config/source-map analysis for modern web applications
- Evidence, secret-handling, reportability, and false-positive policies
- Skeptic/impact review gates and reproducibility requirements
- Skill-gap capture when an uncovered technology or technique is encountered

### Web2 playbooks (27 classes)

- AI & LLM Security
- Access Control
- Attack Chains
- Authentication & Session
- Browser Integration
- Business Logic
- CI-CD & Supply Chain
- Cloud Storage
- Deserialization
- File Upload
- GraphQL
- HTTP Request Smuggling
- Linux Sandbox & Host IPC
- Mobile API
- Native Parser & Streaming Interfaces
- OAuth & SSO
- REST API
- Race Conditions
- Rate Limits & Abuse
- SSRF
- Secret Exposure
- Server-Side Template Injection
- Source-First Mapping
- Text Protocol Injection
- Webhooks
- WordPress CVE Intelligence
- XSS

Each mature class can include an overview, safe test checklist, evidence requirements, false-positive controls, and reportability criteria.

### Web3 playbooks (21 classes)

- AMM
- Access Control
- Bridges
- ERC4626
- External Calls
- Flash Loans
- Foundry
- Governance
- Input Validation
- Lending
- Liquidations
- OWASP Alignment
- Oracles
- Proof Systems
- Reentrancy
- Reporting
- Rounding & Precision
- Share Accounting
- Signatures
- State Machines
- Upgradeability

The Web3 layer is designed for source review, local reproduction, invariant reasoning, differential validation, and evidence-first triage. Live transaction or fund-impacting actions require separate authorization.

### Learning and knowledge maintenance

- A versioned public learning-source registry with cadence, trust, acquisition, and promotion policy
- Static and browser-assisted ingestion lanes
- Deduplication and provenance tracking
- Proposal-only promotion: ingestion never silently rewrites operational playbooks
- Offline multi-lane research cascades for novelty, criticism, evidence, and synthesis
- Reusable Web2/Web3 evaluation rubrics

### Included Hermes skills

- ai-security-research-cascade
- argus-security-research-workspace
- argus-securityresearch-workflows
- argus-source-first-recon
- argus-vault-routing

Hermes skills are stored under `skills/security-research/`. Each `SKILL.md` has YAML frontmatter and supporting references/scripts where appropriate.

## Repository layout

```text
.
├── README.md
├── AGENTS.md
├── PRIVACY.md
├── RELEASE-AUDIT.md
├── config/
│   ├── learning-sources.yaml
│   ├── learning-cron-jobs.example.yaml
│   └── preview-is.env.example
├── skills/security-research/       # reusable Hermes skills
├── vault/                          # open this directory as an Obsidian vault
│   ├── 00 - System/                # policies, routers, indexes
│   ├── 01 - Learning/              # curated summaries only
│   ├── 02 - Vulnerability Playbooks/
│   ├── 06 - Evals/
│   ├── 08 - Templates/
│   └── 11 - Scripts/
├── scripts/
│   ├── install.py                  # safe local installer
│   ├── verify_public_release.py    # publication/privacy gate
│   └── update_checksums.py
├── SOURCE-MANIFEST.json
└── CHECKSUMS.sha256
```

The numbered vault layout intentionally leaves gaps. Private runtime zones are either omitted or represented only by tracked sentinel `README.md` files; their actual contents are ignored by Git and are not backup data.

## Quick setup

### 1. Clone

```bash
git clone https://github.com/SjM1NzNS/Argus.git argus-framework
cd argus-framework
```

### 2. Install Hermes Agent

Follow the current official instructions at <https://hermes-agent.nousresearch.com/docs/>. A common installation path is:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
hermes doctor
```

Hermes is optional for reading the Obsidian knowledge base, but required to use the included agent skills directly.

### 3. Install the Argus skills and public configuration

Preview the installer first:

```bash
python3 scripts/install.py --dry-run
```

Then install the skills into the active Hermes home and the public learning registry into the Argus config directory:

```bash
python3 scripts/install.py
```

Defaults:

- Hermes home: `$HERMES_HOME` or `~/.hermes`
- skill destination: `<Hermes home>/skills/security-research/`
- Argus config: `$ARGUS_CONFIG` or `~/.config/argus`
- working vault: this repository's `vault/` directory

For editable skill links rather than copies:

```bash
python3 scripts/install.py --mode symlink
```

The installer refuses to overwrite existing skills/config unless `--force` is supplied. Inspect any existing local modifications before using `--force`.

Start a new Hermes session after installation so the skill catalog is reloaded:

```bash
hermes skills list
hermes -s argus-securityresearch-workflows
```

### 4. Open the knowledge base in Obsidian

1. Start Obsidian.
2. Choose **Open folder as vault**.
3. Select this repository's `vault/` directory.
4. Start with `00 - System/web2-skill-index.md`, `00 - System/web3-skill-index.md`, and `00 - System/agent-operating-policy.md`.

No `.obsidian/workspace*.json`, community-plugin state, or local UI history is included. Obsidian creates local settings on first open.

### 5. Optional script dependencies

Most policy and verification scripts use Python's standard library. Learning/browser workflows may also require:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium   # only for browser-assisted learning
```

Set runtime paths explicitly when your layout differs:

```bash
export ARGUS_VAULT="$PWD/vault"
export ARGUS_SECURITY_RESEARCH="$ARGUS_VAULT"
export ARGUS_CONFIG="$HOME/.config/argus"
```

### 6. Recreate the optional learning schedules

`config/learning-cron-jobs.example.yaml` preserves the daily and weekly
learning schedules, prompts, skill order, and restricted toolsets in a
public-safe form. It intentionally contains no live job IDs, delivery targets,
provider/model pins, run history, or personal paths.

Set `ARGUS_VAULT` to the absolute path of this repository's `vault/` directory,
then ask Hermes to create the two jobs from the template while substituting that
value for `${ARGUS_VAULT}`. Review the prompts and schedules before approving
creation:

```bash
export ARGUS_VAULT="$(pwd)/vault"
hermes
```

Example request inside Hermes:

```text
Create the two Hermes cron jobs described in
config/learning-cron-jobs.example.yaml. Substitute the current ARGUS_VAULT
value for ${ARGUS_VAULT}. Preserve the schedules, prompts, skills, workdir, and
enabled toolsets. Do not add a delivery target or provider/model override.
```

Verify the resulting local jobs:

```bash
hermes cron list
```

The installer does not create scheduled jobs automatically. Cron creation is an
explicit local action, and the live `~/.hermes/cron/jobs.json` remains private.

Optional Preview.is RAG integration uses `PREVIEW_RAG_API_KEY` or `PREVIEW_IS_API_KEY`. Copy the example file, add the key locally, lock its permissions, and never commit it:

```bash
cp config/preview-is.env.example "$HOME/.config/argus/preview-is.env"
chmod 600 "$HOME/.config/argus/preview-is.env"
```

### 7. Verify before use or publication

```bash
python3 scripts/verify_public_release.py .
python3 scripts/update_checksums.py --check
```

If `gitleaks` and `trufflehog` are installed, run the same external scanners used for this backup:

```bash
gitleaks detect --source . --no-git --redact --exit-code 1
trufflehog filesystem . --no-update --fail --only-verified
```

## Operating model

### 1. Confirm authorization

Record the exact scope source, in-scope asset, account/object ownership, prohibited actions, and stop conditions. If authorization is ambiguous, do not test.

### 2. Build a source-derived map

For web/SPAs, collect only explicitly referenced JavaScript, runtime configuration, manifests, and source maps permitted by scope. Derive routes, API bases, auth headers, feature flags, object selectors, and trust boundaries from that material.

### 3. Route to focused playbooks

Use the Web2 or Web3 skill index. Load the smallest relevant set: overview, test checklist, false positives, evidence requirements, and reportability criteria.

### 4. Create a bounded hypothesis

State attacker capability, expected secure behavior, observed behavior, the one variable changed between control and test, the safe proof, and the stop condition.

### 5. Validate safely

Prefer local/offline reproduction and owned controls. Avoid real-user data, destructive actions, persistence, spam, billing effects, and high-volume automation.

### 6. Apply adversarial review

Ask what benign explanation could produce the same result, what evidence is missing, what would make triage reject or downgrade the claim, and whether the impact actually crosses a security boundary.

### 7. Report only proven outcomes

Keep leads, hypotheses, candidates, and reportable findings as distinct states. Preserve minimal reproducible evidence and redact sensitive material.

## Public-backup boundary

Included:

- reusable policies and routing logic;
- promoted Web2/Web3 playbooks;
- generic templates and evaluation rubrics;
- curated public-source summaries after sanitation;
- deterministic framework scripts and tests;
- reusable Hermes skills and generic supporting references;
- a public learning-source registry.

Excluded:

- all target directories and program briefs;
- account data, cookies, browser profiles, tokens, and credentials;
- raw HTTP responses, HAR files, Burp projects, screenshots, and raw evidence;
- reports, hypotheses, approval queues, hunt logs, and agent logs;
- inboxes, triage runs, generated learning candidates, and lock/state files;
- Hermes memory, user profiles, sessions, auth files, cron state, and `.env` files;
- Obsidian workspace state and community-plugin data;
- target/portfolio/session-specific skill derivations;
- bulk third-party payload corpora.

See `PRIVACY.md` for the release threat model and pre-push checklist.
See `RELEASE-AUDIT.md` for the checks and observed results for this snapshot.

## Status and limitations

- This is a reusable framework snapshot, not a turnkey autonomous vulnerability scanner.
- The source registry contains external links whose availability and terms can change.
- Some scripts require optional local tools or browser dependencies.
- Playbooks are decision support, not permission to test an asset.
- Public summaries may become stale; verify techniques against current primary sources and program rules.

## Acknowledgements

Argus builds on public security standards, research, tools, and write-ups. Source summaries and playbooks retain citations where present. External material remains subject to its original authors' terms and licenses.
