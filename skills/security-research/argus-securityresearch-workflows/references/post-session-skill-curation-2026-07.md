---
type: skill-reference
status: active
created: "2026-07-07"
---

# Post-Session Skill Curation Pattern

Use this when the user asks to review a conversation and update the skill library.

## Core posture

Be active. Most substantial Argus sessions produce at least one skill update: a patch to a loaded umbrella skill, a support reference under that umbrella, or a small workflow/pitfall addition. "Nothing to save" is valid only when there was genuinely no durable technique, correction, preference, or missing step.

## Preferred update order

1. Patch a skill loaded during the session if it governs the learning.
2. If no loaded skill fits, patch an existing class-level umbrella.
3. Add a support file under `references/`, `templates/`, or `scripts/` when session-specific detail is valuable but too bulky for `SKILL.md`.
4. Create a new skill only when no class-level umbrella exists.

## What to capture

- User corrections to workflow, sequence, tone, formatting, or style.
- Non-trivial task patterns that worked after iteration.
- Missing skill steps or pitfalls discovered while using the skill.
- Reusable templates, verification scripts, or source-review patterns.
- Durable source-handling rules, especially for Argus learning, target isolation, mission-mode branches, and candidate-finding verification.

## What not to capture

- One-off task narratives.
- Temporary environment failures or missing binaries.
- Negative permanent claims about tools being broken.
- Session-specific data such as PR IDs, commit hashes, one-time targets, or stale artifact counts.
- Raw source mirrors; keep concise summaries and references instead.

## Argus-specific defaults

For Argus bug bounty sessions, prefer updating `argus-securityresearch-workflows` unless a narrower loaded skill clearly owns the behavior. Use class-level workflow sections and put session-specific detail in `references/`.

After updating, verify mentally that future sessions can discover the reference from `SKILL.md`; add a one-line pointer if needed.
