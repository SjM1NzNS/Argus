---
type: eval-case
domain: web2
status: populated
name: ssrf-blind-callback-hold
expected_decision: "hold as testable candidate / queue approval"
created: ""
updated: "2026-06-29"
---

# SSRF Blind Callback Hold

## Scenario

A URL fetcher on an in-scope app calls an owned callback URL. Evidence shows server-side source IP and headers. No internal URL, metadata, file scheme, port scan, or sensitive response disclosure is tested.

## 1. Is this reportable?

Not yet. SSRF playbook says benign callback proves server-side fetch but not meaningful security impact unless accepted blind SSRF impact exists.

## 2. What severity?

None/Low until impact; severity depends on approved validation result

## 3. What proof is missing?

Internal reachability, sensitive response disclosure, cloud metadata, credential leakage, auth bypass, or program policy accepting blind SSRF.

## 4. What would triage reject?

Triage rejects blind callback-only claims as no-impact when program does not accept blind SSRF.

## 5. What is the next action?

Queue Zone 3 approval for metadata/internal validation if scope permits; continue safe branches.

## 6. Should Argus report, hold, or discard?

Decision: hold as testable candidate / queue approval.

## Expected Argus reasoning

PASS with minor patch needed: playbook should explicitly log blind callback as Lead/Testable Candidate, not finding.
