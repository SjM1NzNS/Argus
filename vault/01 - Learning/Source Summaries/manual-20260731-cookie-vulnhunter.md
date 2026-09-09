---
title: Manual promotion — insecure cookie policies and VulnHunter
created: "2026-07-31"
status: promoted-with-corrections
---

# Manual promotion — insecure cookie policies and VulnHunter

Reviewed and hash-preserved:

- [Intigriti — Exploiting insecure cookie policies](https://www.intigriti.com/researchers/blog/hacking-tools/exploiting-insecure-cookie-policies), published 2026-06-27;
- [Capital One — VulnHunter](https://github.com/capitalone/vulnhunter) at immutable commit `8c2e20a3dd2d1f529c51811fe3d272f83cb6a254`.

Full provenance, claim matrices, hashes, and evidence boundaries are in:

`01 - Learning/Inbox/manual-articles-20260731-cookie-vulnhunter/source-summary.md`

## Durable lessons

### Cookie security

A cookie attribute maps to one threat, not generic “cookie security”:

- `Secure` limits transport; it is not CSRF protection.
- `HttpOnly` limits non-HTTP API visibility but not XSS acting through the browser.
- `SameSite=Strict` suppresses cross-site, not same-site, delivery; site is not origin.
- host/`Domain`/`Path`/prefix rules govern scope and overwrite conditions, not authorization.

A missing attribute is a lead. Promotion requires the exact sensitive cookie, effective browser behavior, attacker prerequisite, owned-session state/replay impact, and a one-variable negative control. Missing `Secure` does not prove plaintext theft until a matching HTTP request actually carries authority under current HSTS/upgrade state; missing `HttpOnly` does not prove ATO until a live readable value creates a new replayable capability.

### Agentic source review

Independently derive input/entry-point and sink ledgers, reconcile them per production module, and flatten every candidate into a verdict manifest. Re-check partitioned candidates against full fixed-commit source. One safe caller/writer does not clear a shared sink/property; every co-parameter and distinct source→sink flow needs disposition. Failed/truncated workers are coverage gaps.

Keep evidence levels distinct:

1. `static_candidate` — unexecuted trace/model/illustrative test;
2. `source_fact` — immutable code/config behavior;
3. `runtime_validated` — exact path executed with causal negative control;
4. `deployed_proof` — authorized in-scope behavior with actor and impact closed.

Mental execution, LLM consensus, or scanner confidence is not runtime proof. Missing defense evidence is `unknown`, not automatically effective or ineffective. No VulnHunter efficacy claim was adopted because the checked-in benchmark has an LLM judge, a minimal synthetic example, and no retained scorecard.

## Promoted artifacts

- `02 - Vulnerability Playbooks/Web2/Authentication & Session/cookie-security.md`
- `00 - System/external-agent-skill-source-review-capitalone-vulnhunter-2026-07-31.md`
- `06 - Evals/Web2/cookie-security-agentic-source-review-20260731-eval-scenarios.md`
- Source-First Mapping coverage/falsification gates
- `argus-source-first-recon` v1.3.17
- Web2 routing and July changelog

## Outcome

**0 target-specific findings.** No payload, live target, credential, dependency, repository code, model, scanner, exploit test, fixer, publisher, issue, or PR action was run.
