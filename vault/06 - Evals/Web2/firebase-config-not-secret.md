---
type: eval-case
domain: web2
status: populated
name: firebase-config-not-secret
expected_decision: "discard"
created: ""
updated: "2026-06-29"
---

# Firebase Config Not Secret

## Scenario

A JS bundle exposes `apiKey`, `authDomain`, `projectId`, and `appId` for Firebase. The values are public client configuration. Offline review finds no database/storage rules exposure, no private credential, and no unsafe validation performed.

## 1. Is this reportable?

No. The Secret Exposure playbook marks public SDK/config keys as common false positives unless credential capability or unsafe rules are evidenced.

## 2. What severity?

None / Informational

## 3. What proof is missing?

Evidence of permissive rules, unauthorized read/write, production capability, or program policy saying public config alone is reportable.

## 4. What would triage reject?

Triage would reject public Firebase config without demonstrated security impact.

## 5. What is the next action?

Discard or keep as lead only if later safe rules evidence appears.

## 6. Should Argus report, hold, or discard?

Decision: discard.

## Expected Argus reasoning

The playbook correctly distinguishes public config from credential exposure.
