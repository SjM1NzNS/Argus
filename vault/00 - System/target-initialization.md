# ARGUS TARGET INITIALIZATION WORKFLOW

Before any live target work, Argus must create a target-specific scope contract.

Target initialization steps:

1. Read or request the program scope.
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
9. After the scope contract exists, propose or begin the first autonomous Zone 1 plan.
10. If the scope clearly allows it, begin low-noise Zone 1 work.
11. Queue anything Zone 3 or ambiguous.
12. Keep `agent-log.md`.
13. Produce a meaningful checkpoint.

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
