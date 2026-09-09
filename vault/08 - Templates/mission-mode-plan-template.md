---
type: mission-template
status: active
created_utc: "2026-07-07T19:44:02Z"
---

# Mission Mode Plan Template

Use this template for focused, authorized hunt branches that need mission-mode work. Store a copy under the selected private target workspace only:

```text
03 - Targets/<Program>/tool-output/missions/<branch>/plan.md
```

## Mission identity

| Field | Value |
|---|---|
| Program | `<authorized-program>` |
| Dedicated agent | `<agent-or-workflow-name>` |
| Mission ID | |
| Branch name | |
| Created UTC | |
| Owner / director | Argus + user |
| Status | proposed / active / blocked / killed / candidate-finding / complete |

## Scope gate

- Scope contract read: yes / no
- `hunting_enabled: true`: yes / no
- In-scope asset(s):
- Out-of-scope constraints:
- Program exclusions relevant to this mission:
- Automation/rate limits:
- Confirmation-gated actions:

If the scope gate is incomplete, stop. Only local planning is allowed.

## Objective

State one narrow objective. Avoid “test everything.”

## Hypothesis

```text
If [attacker-controlled condition], then [security boundary] may fail, causing [impact].
```

## Required playbooks / routes

List every relevant Web2/Web3 index route and playbook loaded before action.

## Allowed actions

- Local-only analysis:
- Low-noise live actions, if already in scope:
- Explicitly user-confirmed actions:

## Forbidden actions for this mission

- Non-owned data access:
- Mutations/uploads/deletes without approval:
- Broad recon/scanning/fuzzing:
- Credential/token validation:
- Other program-specific restrictions:

## Specialist workstreams

| Specialist | Scope | Inputs | Output file | Side effects allowed? |
|---|---|---|---|---|
| Static/source reviewer | | | `agent-notes.md` | No |
| API/schema mapper | | | `agent-notes.md` | No unless approved |
| AuthZ/threat model reviewer | | | `synthesis.md` | No |
| Hypothesis killer | | | `verification.md` | No |
| Report drafter | | | `findings-draft.md` | No |

## Evidence targets

- Positive control:
- Negative control:
- Expected request/response evidence:
- Screenshots/video needed:
- Logs/files to preserve:

## Stop conditions

- Kill if:
- Pause if:
- Escalate if:
- Convert to draft finding if:

## Human-final-judgment gate

No report recommendation until Argus completes `verification.md` and `findings-draft.md` with triager objections and final recommendation.
