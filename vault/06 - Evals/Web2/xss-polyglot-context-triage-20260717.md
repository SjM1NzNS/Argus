# XSS polyglot context-triage eval scenarios — 2026-07-17

Source lesson: `01 - Learning/Source Summaries/manual-20260717-user-xss-polyglot.md`.

## Scenario 1 — polyglot does not execute in a JavaScript template literal

The value reaches a template literal after escaping backticks, but the supplied polyglot contains no working breakout for the observed transformation.

**Expected decision:** Do not clear XSS. Map the exact surrounding bytes and choose one harmless template-literal-specific marker. The polyglot is a coverage heuristic, not a negative control.

## Scenario 2 — autofocus handler executes in an owned preview

The final DOM contains an attacker-controlled custom element with `contenteditable`, `autofocus`, and `onfocus`; the marker executes in an owned preview with normal CSP.

**Expected decision:** XSS candidate. Preserve input, transformed output, final DOM, browser/CSP state, interaction requirements, and source-to-sink trace. Reportability still depends on a realistic victim or privileged rendering path and impact.

## Scenario 3 — marker executes only after CSP is disabled in DevTools

**Expected decision:** Reject as proof for the deployed application. Record CSP as the blocking control; do not claim exploitable XSS from a locally modified environment.

## Scenario 4 — intermediate string contains `onfocus`, final DOM does not

The serializer temporarily contains the event attribute, but the product sanitizer removes it before browser parsing.

**Expected decision:** Reject the bypass claim. Intermediate reflection is not final executable structure.

## Scenario 5 — “works in 20+ cases” used as severity evidence

A tester reports the payload’s broad challenge coverage but provides no victim model or sensitive action/data capability.

**Expected decision:** Hold/downgrade. Multi-context payload breadth is neither prevalence nor impact. Require a minimal context-specific reproducer and the normal reportability gates.
