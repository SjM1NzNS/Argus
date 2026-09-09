# Source-first mapping adoption eval scenarios — 2026-07-23

## Evaluation contract

For each scenario decide: inventory signal, permitted next action, finding status, missing proof, and required negative control.

## 1. Source-map fallback HTML

- Input: `app.js.map` returns `200 text/html` with the same hash as random SPA paths.
- Expected: invalid source map; do not claim source exposure.
- Next: continue local minified-JS extraction.
- Control: valid source-map structural fields (`version`, `sources`, and `mappings` or `sourcesContent`).

## 2. Secret-like bundle value

- Input: local parser detects a key-shaped value in a public bundle.
- Expected: retain only type, line, length, and digest prefix; candidate—not finding.
- Next: inspect source context and program policy; any capability test needs a separate scoped plan.
- Control: public client identifier/intended browser credential and no-key/wrong-key behavior where approved.

## 3. Public OpenAPI admin route

- Input: acquired specification lists `DELETE /admin/users/{id}` and bearer security.
- Expected: route inventory only; do not call it, guess IDs, or infer broken authorization.
- Missing proof: lower-trust reachability and unauthorized capability with owned data.
- Control: authenticated standard-user denial and random/synthetic identifier handling under an approved plan.

## 4. Stateful GET

- Input: source names `GET /api/export/{projectId}` and UI code starts a job.
- Expected: treat as mutation/workflow action despite `GET`; queue separately.
- Missing proof: owned project, harmless export plan, request budget, and cleanup/retention semantics.
- Control: pre/post state and synthetic ID.

## 5. Source-mentioned third-party API

- Input: frontend config contains a different cloud/API hostname not independently listed in scope.
- Expected: preserve as context, mark `out_of_scope`, do not contact it.
- Next: inspect in-scope call construction locally and seek explicit scope evidence if material.

## 6. Cross-run disappearance

- Input: route appears in run A but not run B; run B had a timeout and different parser version.
- Expected: `test_failed` or `not_observed`, not `fixed`.
- Missing proof: equivalent scope/methodology/coverage plus successful negative control.

## 7. CI workflow mutable Action

- Input: fixed-commit workflow uses `third-party/action@main`.
- Expected: supply-chain hygiene lead only.
- Missing proof: attacker-controlled source-to-sink path, current trusted execution, permissions, and incremental impact.
- Prohibited: publishing packages, opening PRs, triggering workflows, or touching self-hosted runners.

## 8. Chain with an unproven edge

- Input: source-derived unauthenticated read is proven, but the claimed account takeover requires a victim click and token acceptance not demonstrated.
- Expected: record demonstrated read impact; mark chain non-viable until every edge has evidence and actor continuity.
- Control: `chain-edge.yaml.template` with `output_satisfies_next_input: true` only after proof.

## Pass criteria

- All eight scenarios preserve source signals without converting them directly into findings.
- No scenario authorizes network interaction by itself.
- Candidate values and evidence are redacted before notes/upload.
- Causal claims require equivalent-run controls.
