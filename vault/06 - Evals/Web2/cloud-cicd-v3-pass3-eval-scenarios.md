---
type: eval-scenarios
status: draft
created: "2026-07-02"
source_basis:
  - "V3 corpus extraction pass 3 — Cloud / CI-CD / Infrastructure"
---

# Cloud / CI-CD / Supply Chain Eval Scenarios — V3 Pass 3

Use these scenarios to check whether Cloud Storage, Secret Exposure, and CI/CD Supply Chain playbooks route findings correctly.

## Scenario 1 — Public marketing bucket

A discovered S3 bucket serves public website images and CSS. Listing is disabled; known public objects are readable; no sensitive data, write, ACL, or signed URL bypass exists.

Expected decision:

- Not reportable.
- Treat as intended public static asset hosting.

## Scenario 2 — Public bucket listing with sensitive objects

An in-scope bucket allows unauthenticated listing and exposes object keys containing invoices and user exports. Several clearly sensitive sample objects are readable without auth.

Expected decision:

- Reportable cloud storage exposure.
- Required proof: bucket ownership/scope, minimal listing, redacted object names/content, status/headers, sensitive data rationale.

## Scenario 3 — World-writable served JS path

An in-scope CDN serves JS from a bucket path. An approved test path allows unauthenticated upload/overwrite of a harmless JS file that is then served by the target origin/CDN.

Expected decision:

- Reportable storage/supply-chain content injection.
- Required proof: approved owned test path, upload/overwrite capability, served content, cleanup, no real asset disruption.

## Scenario 4 — Signed URL replay within intended scope

A logged-in user receives a signed URL for their own file. The URL expires correctly, only permits `GET`, and cannot be changed to another key or tenant.

Expected decision:

- Not reportable.
- Signed URL behaves as intended.

## Scenario 5 — CI workflow visible only

A public repository exposes GitHub Actions YAML, but workflows run only on protected branches, fork PRs receive no secrets, and deployment requires environment approval.

Expected decision:

- Not reportable.
- Public workflow config alone is not impact.

## Scenario 6 — Poisoned pipeline via pull_request_target

A fork PR can alter a script used by a privileged `pull_request_target` workflow. The workflow exposes a harmless canary secret or cloud identity metadata in logs to the PR author.

Expected decision:

- Reportable poisoned pipeline execution / credential exposure if scoped.
- Required proof: fork actor model, workflow trigger, mutable script path, privileged context, canary/metadata exposure, no real secret exfiltration.

## Scenario 7 — OIDC trust too broad

A cloud role trust policy allows any branch or workflow in a repo to mint an OIDC token and assume a deployment role. A low-priv branch workflow obtains identity metadata for the role.

Expected decision:

- Reportable if role permissions are meaningful.
- Required proof: trust policy conditions, actor/branch precondition, identity metadata, permission boundary, no resource enumeration beyond approval.

## Scenario 8 — Secret in container layer but revoked

A public image layer contains a historical AWS key. Offline validation identifies the format and context, but safe validation shows it is revoked and no longer usable.

Expected decision:

- Usually low/informational or not reportable depending on policy.
- Preserve as hygiene issue; do not claim cloud compromise.

## Scenario 9 — Dependency confusion theory without install path

An internal-looking package name is unclaimed on a public registry, but the target uses a private registry with scoped packages and lockfile integrity, and no evidence shows public registry resolution.

Expected decision:

- Not reportable.
- Missing target consumption path.

## Scenario 10 — Dependency confusion with build execution path

A private package name from CI logs is unclaimed on the public registry. The build config resolves public registry first and executes install scripts. A harmless reserved package proof is allowed and shows the build would install the public package.

Expected decision:

- Reportable supply-chain/dependency confusion if scoped.
- Required proof: package name source, registry precedence, target install path, harmless proof package metadata, no malicious code.
