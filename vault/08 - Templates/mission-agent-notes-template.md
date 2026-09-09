---
type: mission-template
status: active
created_utc: "2026-07-07T19:44:02Z"
---

# Mission Agent Notes Template

Store a copy under:

```text
03 - Targets/<Program>/tool-output/missions/<branch>/agent-notes.md
```

## Inputs reviewed

- Scope contract:
- Playbooks:
- Source files / JS / binaries / docs:
- Prior tool output:
- User-provided context:

## Specialist notes

### Static/source reviewer

- What was reviewed:
- Security-relevant routes/functions/classes:
- Guard clauses / authZ checks:
- Data-flow notes:
- Candidate leads:
- Reasons to reject:

### API/schema mapper

- Endpoints / operations:
- Request shapes:
- Object IDs / ownership model:
- Auth/session/token model:
- State-changing operations:
- Safe controls:

### AuthZ/threat model reviewer

- Actors:
- Assets/data:
- Trust boundaries:
- Expected enforcement points:
- Likely false positives:

### Report drafter

- Candidate summary:
- Missing evidence:
- Report blockers:

## Side-effect log

This file should normally contain only local reasoning. If a side effect occurred, record why it was allowed by `plan.md` and `scope-contract.md`.

| UTC | Action | Tool | Asset | Scope basis | Result |
|---|---|---|---|---|---|
