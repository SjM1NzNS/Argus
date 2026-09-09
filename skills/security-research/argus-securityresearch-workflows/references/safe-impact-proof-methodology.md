# Safe impact proof methodology

Use this for Argus bug-bounty/security-research work when validating impact for RCE, credential exposure, data access, deploy compromise, CI/CD, developer-tool, or supply-chain findings.

## Core standard

Do **not** stop at speculation when a higher-fidelity safe proof is available. Prove the highest realistic impact with the minimum safe, non-destructive action, then stop.

A plausible RCE path gets an active disposition: **prove**, **safely kill with a negative control**, or **record the exact unavailable prerequisite**. Do not leave it untested merely because execution depends on a configured tool, model choice, MCP server, plugin, or development-mode application. Conditional execution can be the most useful impact evidence when its dependencies are stated precisely.

Safe impact proof is expected and valuable; destructive exploitation, broad collection, persistence, or unnecessary access expansion is not.

## Acceptable proof boundaries

### RCE / code execution

Prefer one harmless proof and stop:

```text
whoami
id
hostname
pwd
touch /tmp/<owned-marker>
print/write an owned marker
```

Avoid commands that dump environment, credential files, SSH keys, cloud metadata, or broad host state unless the program explicitly permits and the proof is necessary.

### Credential / secret exposure

Acceptable proof patterns:

- attacker-owned canary secret is loaded or selected;
- secret class/source/path is identified without printing the value;
- metadata-only validation such as identity/scope/expiry, where authorized;
- prefix/suffix redaction when a value is already exposed and showing partial proof is necessary.

Do not dump full secrets. Do not use a credential to enumerate resources or access data unless explicitly in scope and necessary for a safe proof.

### Data access

Prefer owned canary data. If real sensitive data is unexpectedly exposed, capture the minimum redacted evidence needed to prove class/scope, then stop. Do not bulk collect.

### Deploy / CI-CD / supply-chain compromise

Good proof steps:

1. show attacker-controlled input reaches trusted build/deploy/artifact/runtime boundary;
2. use local/owned staging first;
3. monkeypatch or dry-run external deploy calls when possible;
4. prove runtime execution with `whoami`/marker or canary values;
5. explicitly state non-claims: no real cloud mutation, no production RCE, no real secrets/data unless safely validated.

## Report framing

Separate:

- **proven impact**;
- **safe proof boundary**;
- **negative controls**;
- **non-claims**;
- **escalation conditions** that would raise severity.

Avoid underclaiming real safe impact, but also avoid saying “production RCE”, “secret theft”, “data breach”, or “drive-by” unless directly proven under default/in-scope conditions.

## Escalation checklist

Before submitting, consider safe variants:

- deployed-style local runtime proof;
- owned throwaway deploy only if explicitly approved;
- fake credential/config-source canary;
- owned canary data;
- real-browser/default-vs-unsafe-config checks;
- official delivery/actor-model evidence;
- platform realism checks such as Git symlink preservation;
- additional deploy target staging propagation with cloud calls monkeypatched.

## Pitfalls

- Do not treat “safe testing” as “no impact proof.” The user expects strong, safe impact proof.
- Do not stop at `whoami` if a safe deployed-runtime or canary propagation proof would materially clarify impact.
- Do not use absence of real secret/data access as a reason to omit credential/data-source poisoning evidence; use canaries, redaction, or metadata-only validation.
- Do not turn environment-specific failures into durable methodology. Capture the reusable technique or workaround instead.