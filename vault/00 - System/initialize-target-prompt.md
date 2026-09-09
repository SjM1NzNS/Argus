Initialize target: <Program Name>

Program URL / scope source:

<paste program policy or URL here>

Before doing anything else:

1. Read the program scope.
2. Create `~/SecurityResearch/03 - Targets/<Program Name>/`.
3. Create `scope.md`.
4. Create `scope-contract.yaml`.
5. Extract:
   - allowed domains/assets
   - forbidden domains/assets
   - allowed testing
   - forbidden testing
   - rate limits
   - account model
   - required confirmation actions
   - explicit out-of-scope issues
   - report requirements
6. Create target folders:
   - evidence
   - tool-output/http
   - tool-output/js
   - tool-output/github
   - tool-output/screenshots
   - tool-output/endpoints
   - tool-output/secrets
   - tool-output/scans
   - burp
7. Link or create Burp project path under `~/BurpSuite/<Program Name>/`.
8. Do not run recon until the scope contract exists.
9. After the scope contract exists, propose the first autonomous Zone 1 plan.
10. If the scope clearly allows it, begin low-noise Zone 1 work.
11. Queue anything Zone 3 or ambiguous.
12. Keep `agent-log.md`.
13. Produce a meaningful checkpoint.

## Automatic skill routing requirement

After creating the first surface map, Argus must run skill routing.

For every discovered surface:

1. Classify the surface.
2. Identify whether it is Web2, Web3, mobile, cloud, public-code, secret-exposure, or mixed.
3. Identify relevant vulnerability classes.
4. Read `~/SecurityResearch/00 - System/skill-router.md`.
5. Read the relevant skill index:
   - `~/SecurityResearch/00 - System/web2-skill-index.md`
   - `~/SecurityResearch/00 - System/web3-skill-index.md`
6. Load the minimum necessary playbooks.
7. Extract:
   - test checklist
   - evidence requirements
   - false positives
   - reportability rules
   - severity gates
   - tooling workflow
8. Create or update hypotheses using the loaded skills.
9. Record all loaded skills in `agent-log.md`.
10. Record missing skills as skill gaps under:
    `~/SecurityResearch/01 - Learning/Skill Patch Proposals/`
11. If the missing skill is not required to safely continue, keep working another safe branch.

## Required loaded-skills log format

In `agent-log.md`, log skill routing like this:

skill_routing:
  timestamp: YYYY-MM-DD HH:MM
  surface: "<surface name>"
  classification: "<web2/web3/cloud/mobile/secret/etc>"
  triggers:
    - "<trigger>"
  loaded_skills:
    - "<path/to/playbook>"
  missing_skills:
    - "<skill gap if any>"
  next_action: "<hypothesis/test/update>"

## Hypothesis creation rule

Every meaningful hypothesis must cite the playbook or skill that generated it.

Hypothesis format:

hypothesis: "<short hypothesis>"
domain: "<web2/web3>"
surface: "<surface>"
vuln_class:
  - "<class>"
source_skills:
  - "<playbook path>"
evidence_needed:
  - "<evidence item>"
false_positive_checks:
  - "<check>"
reportability_gate:
  - "<gate>"
zone: "<0/1/2/3>"
status: "<lead/hypothesis/testable/evidence-backed/reportable>"
priority: "<1-10>"

## Test planning rule

Before running any Zone 2 test, Argus must answer:

1. Which loaded playbook supports this test?
2. What is the minimal safe validation?
3. What evidence is required?
4. What false positive would invalidate this?
5. What would triage reject?
6. Does the scope contract allow this?
7. Is this Zone 2 or Zone 3?

If the answer is unclear, queue the test instead of running it.

## Report drafting rule

Before drafting any report, Argus must reload or consult the relevant playbook and verify:

1. Evidence requirements are satisfied.
2. False-positive checks are addressed.
3. Impact matches the severity claim.
4. Downgrade argument is weaker than severity argument.
5. Scope contract supports the report.
6. No real user data was accessed.
7. Reproduction steps are clean and minimal.
