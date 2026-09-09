---
type: mission-template
status: active
created_utc: "2026-07-07T19:44:02Z"
---

# Hypothesis-Kill / Verification Template

Store a copy under:

```text
03 - Targets/<Program>/tool-output/missions/<branch>/verification.md
```

## Hypothesis under test

```text
If [condition], then [boundary] fails, causing [impact].
```

## Scope verification

- Asset in scope:
- Policy exclusions checked:
- Account/test-data constraints:
- Automation/rate limit constraints:
- Confirmation-gated steps:

## Kill checks

| Check | Result | Evidence |
|---|---|---|
| Is there a guard clause or authZ check that already blocks this? | | |
| Is the behavior intended or documented? | | |
| Is the class excluded by the program? | | |
| Is impact only missing header, verbose error, scanner output, self-only issue, or best practice? | | |
| Does proof require non-owned data or risky mutation? | | |
| Is the exploit path realistic for a triager? | | |
| Is this likely duplicate-prone/common known behavior? | | |
| Are positive and negative controls possible? | | |

## Positive control

- Control:
- Expected result:
- Actual result:
- Evidence:

## Negative control

- Control:
- Expected result:
- Actual result:
- Evidence:

## Human-final-judgment checklist

1. Asset in scope?
2. Reproducible?
3. Real security impact?
4. Not excluded?
5. Not duplicate-prone / known behavior?
6. Realistic exploit path?
7. Evidence sufficient?
8. No user-data/disruption/legal risk beyond approved test?
9. Severity justified?
10. Skeptical triager likely to accept?

## Decision

- Final recommendation: report / needs more evidence / do not report
- Reason:
- Next action:
