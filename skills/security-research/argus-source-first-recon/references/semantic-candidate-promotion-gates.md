# Semantic Candidate Promotion Gates

Use this reference after a fixed-commit source trace finds a plausible security defect but before drafting a report. It captures reusable lessons from the Site Kit review without turning one repository into its own skill.

## 1. Separate behavioral proof from reportability

A deterministic harness can prove that vulnerable behavior exists while the candidate still fails actor or impact gates. Record these independently:

```text
behavior_confirmed: true|false
attacker_input_control: proven|conditional|unproven
victim_boundary_crossed: proven|conditional|unproven
attacker_observable_effect: proven|conditional|unproven
reportability: promote|hold|kill
```

Do not convert “the implementation omits a standard control” into “an external attacker can exploit it” unless the attacker can supply every prerequisite under the target’s real deployment model.

## 2. OAuth missing-state review

When a callback consumes `code` without visible `state` validation:

1. Trace the outer callback gate: login requirement, capability, nonce, session, redirect route.
2. Search repository-wide for state generation, storage, echo, validation, PKCE, OIDC nonce, and framework/proxy behavior.
3. Prove with synthetic collaborators whether missing and mismatched state are accepted.
4. Add a causal control such as absent client credentials or invalid code rejection.
5. Then prove the attacker can mint a code for the **victim client ID and redirect URI**. A code from the attacker’s separate OAuth client is normally not transferable.
6. Determine who can learn the victim client ID and initiate the flow. “Client IDs are not cryptographic secrets” is not evidence that this installation-specific identifier is publicly reachable.
7. Kill or hold if the only proven actor already has equivalent administrator capability.

A useful local harness may load the actual callback implementation while stubbing only persistence, HTTP/IdP, redirects, and time. Pin synthetic user IDs, codes, tokens, and clocks so reruns are byte-identical. Preserve the actual loaded source path in output.

## 3. Agentic CI and indirect prompt injection

For AI assistants in CI, trace:

```text
untrusted issue/PR text
  -> fetch/parsing command
  -> agent/subagent prompt
  -> allowed tools and approval mode
  -> secret-bearing environment
  -> repository/write job or artifact handoff
```

Check all of the following before claiming compromise:

- Can non-members create content matching the accepted template?
- Is there an author-association or collaborator allowlist?
- Is execution automatic, comment-triggered, or maintainer-dispatched?
- Does the agent have shell/network tools, and are approvals bypassed (`yolo`, auto-approve, etc.)?
- Which secrets exist in the same process as the model/tool runner?
- Are write permissions in the same job or isolated behind an artifact/draft-PR review?
- Can issue/PR text be edited after human review (TOCTOU)?
- Was exact model behavior demonstrated with a no-secret, loopback-only canary?

Environment-output redaction does not necessarily prevent direct shell exfiltration: a model can emit a command containing `$SECRET`, and the shell can expand/send it without the value returning through model-visible stdout. Still, static possibility is not dynamic proof that the model follows the injection.

Use public repository history to test actor reachability, but preserve API responses as evidence and distinguish non-member-authored content from collaborator content.

## 4. Proxy/header forwarding

When a same-origin relay forwards ambient browser headers upstream:

1. Use synthetic cookie, CSRF/nonce, authorization, API-key, host, and custom-header canaries.
2. Capture the exact outbound request with a local request-helper stub; do not contact the real upstream.
3. Include positive and filtered-header controls.
4. Prove destination confinement separately.
5. Do not claim credential theft until a lower-trust actor can read the raw forwarded values. Delivery to fixed first-party infrastructure may be a privacy/hardening issue rather than attacker-readable disclosure.

## 5. Deterministic harness discipline

- Load the actual target file/method whenever practical; identify every stubbed collaborator.
- Keep the target checkout untouched and verify `git status --short` is clean.
- Pin clocks, randomness, IDs, tokens, paths, and ordering.
- Rerun and compare output byte-for-byte.
- Validate structured output and assert every control.
- Hash harness and result only after the final deterministic rerun.
- If a project test stack is unavailable, do not alter global packages merely to force it. A focused executable harness is acceptable if its limitations are explicit.

## 6. Disposition language

Prefer:

- **reviewed, no candidate** — no viable source-to-sink chain;
- **primitive confirmed / hold** — behavior exists, missing actor or impact;
- **behavior confirmed / killed as report candidate** — deployment model collapses the boundary;
- **report-ready** — supported entry point, lower-trust actor, runtime effect, negative control, and concrete impact all proven.

Preserve held/killed branches in the mission disposition and global tested/hypothesis/next-action ledgers so future hunts do not repeat them without new evidence.
