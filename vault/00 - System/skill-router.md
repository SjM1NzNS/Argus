# ARGUS SKILL ROUTER

Argus must dynamically load relevant skills during hunts.

Skills are not passive notes. They are operational playbooks.

Argus must consult relevant skills when:

1. A new surface is discovered.
2. A new hypothesis is created.
3. Tool output suggests a vulnerability class.
4. A test plan is prepared.
5. A finding candidate is triaged.
6. A report is drafted.
7. A learning item proposes a skill update.
8. A triager objection or rejection is reviewed.

Argus should not load every skill by default.

Argus should load skills based on:

- target type
- discovered surface
- endpoint/function behavior
- technology stack
- vulnerability class
- protocol type
- tool output
- current hypothesis
- evidence gap
- triager objection

For each discovered surface or hypothesis:

1. Classify the surface.
2. Identify likely vulnerability classes.
3. Read the relevant Web2 or Web3 skill index.
4. Load only the relevant playbooks.
5. Extract:
   - test checklist
   - evidence requirements
   - false positives
   - reportability rules
   - severity gates
   - tooling workflow
6. Apply those skills to the current target.
7. Record loaded skills in `agent-log.md`.
8. Record missing skills as skill gaps.

Before running a test, Argus must ask:

- Which playbook applies?
- What evidence does this playbook require?
- What false positives does this playbook warn about?
- What would triage reject?
- What is the minimal safe test?

Before drafting a report, Argus must ask:

- Which playbook supports this finding?
- Did the finding satisfy the playbook’s evidence requirements?
- Did the Skeptic Agent apply the playbook’s false-positive checks?
- Did the Impact Agent apply the playbook’s severity gates?

Context control:

Argus should prefer loading:

1. `overview.md`
2. `test-checklist.md`
3. `false-positives.md`
4. `evidence-requirements.md`
5. `reportability.md`
6. detailed examples only when needed

Do not load massive notes unless required.

If context is limited, summarize the relevant skill before applying it.
