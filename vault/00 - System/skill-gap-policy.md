# ARGUS SKILL GAP POLICY

If Argus discovers an important surface, vulnerability class, tool output pattern, protocol type, or triager objection that does not map cleanly to an existing skill, Argus must create a skill-gap note.

Skill gaps should be created under:

`~/SecurityResearch/01 - Learning/Skill Patch Proposals/`

A skill-gap note must include:

- date
- target, if applicable
- discovered surface
- missing skill
- why the skill is needed
- related sources, if any
- related tool output, if any
- suggested playbook path
- initial test ideas
- evidence requirements to research
- false-positive concerns
- priority
- recommended next action

Skill gaps should not block the hunt unless the missing skill is required to safely proceed.

When possible, Argus should continue another safe branch while logging the gap.
