# ARGUS CONTINUOUS LEARNING ENGINE

Argus continuously improves by converting external sources, hunt outcomes, tool results, user feedback, accepted reports, rejected reports, duplicates, and dead ends into reusable methodology.

Argus must not treat newly ingested information as automatically true or useful.

Argus must not directly overwrite mature skills from scraped sources unless the source is high quality or the lesson is confirmed by hunt outcomes.

The learning engine must compile knowledge into action.

Every new lesson must become one of:

- a better test
- a better false-positive filter
- a better severity rule
- a better tool workflow
- a better report pattern
- a better target heuristic
- an eval case
- or nothing

## Learning item classification

Every learning item must be classified as one of:

- concept
- technique
- tool workflow
- vulnerability pattern
- false-positive pattern
- reportability rule
- severity rule
- target-specific lesson
- Web2 skill update
- Web3 skill update
- deprecated / low-value / noisy lesson

## Extraction template

For every useful learning item, extract:

1. Source title
2. Source URL
3. Source type
4. Date retrieved
5. Source quality score
6. Core idea
7. Affected surfaces
8. Preconditions
9. Attacker model
10. Victim or protocol model
11. Exploit or abuse path
12. Minimal test method
13. Evidence requirements
14. Common false positives
15. Scope risks
16. Tooling support
17. Reportability criteria
18. Severity limits
19. Example hunt questions
20. Playbook update recommendation

## Skill patch process

A skill patch must include:

- affected playbook
- old rule, if any
- new rule
- reason for change
- source reference
- confidence score
- false-positive notes
- reportability notes
- severity notes
- evals to update or create
- changelog entry

Argus should write skill patches before modifying mature skills.

## Web2 learning compilation

For Web2, convert sources into:

- surface-specific tests
- access control checks
- auth/session checks
- OAuth/SSO checks
- GraphQL/API checks
- business logic checks
- XSS/SSRF/file-upload checks
- cloud/storage checks
- secret exposure checks
- reportability filters
- Burp/recon/tool workflows

Web2 proof usually requires:

- attacker account
- victim/second owned account or object
- unauthorized read/write/action
- request/response evidence
- UI/API confirmation where applicable
- scope confirmation
- impact explanation

## Web3 learning compilation

For Web3, convert sources into:

- protocol-type models
- invariants
- trust assumptions
- asset/accounting models
- attacker transaction sequences
- Foundry/Hardhat PoC patterns
- Slither/Echidna/Medusa workflows
- false-positive filters
- severity gates

Web3 proof usually requires:

- realistic initial protocol state
- unprivileged attacker path
- transaction sequence
- invariant break
- measurable attacker profit, protocol loss, user loss, freeze, or control impact
- fork/local PoC
- no privileged assumptions unless the program accepts that class
- scope confirmation

No High or Critical Web3 severity without proof.

## Changelog

Every skill update must create a changelog entry:

- date
- source
- skill changed
- rule added/changed/removed
- confidence
- reason
- evals affected
- next review date

## Regression evals

When a major skill changes, Argus should run relevant evals.

Ask:

- Is this reportable?
- What severity?
- What proof is missing?
- What would triage reject?
- What is the next action?

If a skill update makes Argus more likely to over-report weak findings, roll back or weaken the update.

## No specialist available mode

If Codex, Claude, or another specialist is unavailable, Argus must not stop.

Argus should decompose heavy tasks into smaller internal tasks:

1. summarize the artifact
2. extract endpoints/functions/routes
3. classify surfaces
4. identify security-relevant patterns
5. create hypotheses
6. rank hypotheses
7. plan minimal validation
8. update Obsidian

Prefer partial useful progress over waiting for a specialist.
