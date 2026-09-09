---
type: learning-source-summary
compiled_at: 2026-08-05T05:31:36.644999+00:00
source_quality: 5
classification: severity rule
vulnerability_class: AI / LLM Security
---

# AWS VDP | Report #3478646 - GitHub Retired UsernameTakeover From [aws/████████] | HackerOne

- URL: `https://hackerone.com/reports/3478646`
- Source group: `browser_dom_linked_resources`
- Content chars: `1684`
- Classification: **severity rule**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Description I have found a link which was ████████ and it was throwing 404 Not Found , i went on to register the unclaimed (retired) username and host PoC Repo with my own content Steps To Reproduce Navigate to: ████████ Search For ████████ Navigate to this Account & Open the PoC Reporistory Notice that the repo is taken over and saying Taken Over By ████████ PoC ████████ Recommendations All Links assosicated with this retired username should be removed from the repository Reference https://hackerone.com/reports/1434967 https://hackerone.com/reports/1212853 Regards ████████ Impact Users accessing the link from Your Official GitHub are serving content from an attacker-controlled repository, breaking the trust model.
- This allows an attacker to easily convince users to take actions that could be malicious.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
