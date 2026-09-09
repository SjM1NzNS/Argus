---
type: eval-update-proposal
status: draft
created: "2026-06-29 11:53"
domain: web2
run: "2026-06-29-learning-dry-run"
---

# Web2 Eval Update Proposals — Learning Dry Run

## Proposed new/updated eval cases

1. `xss-context-impact.md` — reflected/DOM XSS should be held unless executable context, browser/CSP feasibility, victim model, and meaningful impact exist.
2. `oauth-open-redirect-low-or-invalid.md` — OAuth-adjacent open redirect without token/account impact should not be escalated.
3. `graphql-introspection-lead-only.md` — introspection/schema visibility is a lead unless unauthorized resolver/mutation impact is reproduced.
4. `secret-public-config-invalid.md` — public SDK/Firebase/Sentry-style config should be rejected unless credential capability and impact are shown.
5. `idor-owned-account-comparison-required.md` — access-control claims need two owned principals/objects and server-side enforcement failure.

## Required questions for each eval

- Is this reportable?
- What severity?
- What proof is missing?
- What would triage reject?
- What is the next action?
- Should Argus report, hold, or discard?
