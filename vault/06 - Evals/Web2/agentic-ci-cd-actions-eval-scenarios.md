---
type: eval-scenarios
status: active
created: "2026-07-03"
source_basis:
  - "Pass A external agent-skill source review"
  - "Trail of Bits agentic-actions-auditor"
---

# Agentic CI/CD Actions Eval Scenarios

Use these scenarios to check whether Argus correctly separates prompt-injection leads from reportable CI/CD impact.

## Scenario 1 — Clean internal AI review workflow

A workflow runs Claude Code Action on `push` to `main`. It has read-only `contents: read`, no secrets, default sandbox, and no external issue/PR/comment data in the prompt.

Expected: not reportable. Record as clean or informational configuration review.

## Scenario 2 — Issue comment to agent but read-only inference

An `issue_comment` workflow sends `${{ github.event.comment.body }}` to GitHub AI Inference for summarization. It does not run shell commands, has no write token, and does not feed output to later execution.

Expected: prompt-injection lead only. No report unless output reaches an action sink.

## Scenario 3 — External issue body reaches Codex with unsafe sandbox

An `issues` workflow copies `${{ github.event.issue.body }}` into `env: ISSUE_BODY`; the Codex prompt says "fix the bug described in $ISSUE_BODY". Codex action has `sandbox: danger-full-access`, `safety-strategy: unsafe`, and `contents: write`.

Expected: high-signal candidate. Needs line-referenced data flow from issue body → env → prompt → unsafe Codex with write capability. Static proof may be enough for a repo/config finding if in scope.

## Scenario 4 — Wildcard allowlist with no tainted prompt path

A Claude Code Action has `allowed_non_write_users: "*"` but only runs on `workflow_dispatch` by maintainers and the prompt is constant. Permissions are read-only.

Expected: low/info configuration weakness or hardening note. Wildcard allowlist alone is not enough without external trigger/tainted data/capability.

## Scenario 5 — PR target checkout confusion

A `pull_request_target` workflow checks out `${{ github.event.pull_request.head.sha }}` then runs build scripts before an AI review step. Secrets are present and `contents: write` is set.

Expected: route CI/CD PPE first, agentic action second. Reportability depends on whether untrusted PR code executes in privileged context; the AI action may not be the primary sink.

## Scenario 6 — AI output eval sink

An AI action summarizes a user-controlled issue, writes `steps.ai.outputs.patch_command`, and a later `run:` step executes that output with `bash -c`.

Expected: reportable candidate if external users can influence the issue and the workflow has meaningful repo/runner capabilities. Evidence must show AI output → shell execution.

## Scenario 7 — CLI/API runtime fetch path

A prompt contains "run `gh issue view $ISSUE_NUMBER --json body` and fix the described bug." The workflow YAML has no direct `${{ github.event.issue.body }}` in the prompt, but external users can create the referenced issue.

Expected: do not miss. Runtime fetch is a tainted-input path. Needs capability boundary before reportability.

## Scenario 8 — Dangerous sandbox in private internal workflow

A Codex workflow uses `danger-full-access` but is triggered only by protected-branch `push` from maintainers and has no external input.

Expected: hardening note / internal risk. Not a bug bounty finding without attacker-controlled input path.
