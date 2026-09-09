# Deployment source-archive, generated-build, and cleanup validation

Use when a deployment CLI packages a workspace, generates a Dockerfile/build script, or uploads inline source to a cloud builder.

## Source trace

Map each input through four layers:

```text
CLI/default path or workspace contents
  -> archive/build-context selection and exclusions
  -> generated Dockerfile/build command
  -> upload/API request and retained cloud artifact
```

Inspect:

- default source root (especially current working directory);
- archive operands and exact exclusions;
- `.gitignore`, `.dockerignore`, platform-ignore, and secret-pattern behavior;
- symlink and hard-link handling;
- duplicate archive entries and extraction normalization;
- generated Dockerfile quoting/JSON escaping;
- shell-form `RUN` concatenation;
- downstream option injection even when `exec.Command` avoids shell injection;
- temp-directory creation, permissions, and cleanup on every failure path.

## Exact local archive proof

Do not deploy merely to prove packaging behavior. Reproduce the product's exact archive command against an owned temporary source tree containing:

- fake `.env` canary;
- fake service-account-shaped JSON with no real credential;
- normal source file;
- excluded `.git/` control;
- every product-specific exclusion control.

List the resulting archive and extract only the fake canaries. Assert both positive inclusion and negative exclusions. Preserve the command, entry list, fake content, and a machine-readable result.

Avoid real credentials and do not infer cloud readability from archive inclusion alone.

## Generated-build injection gate

Distinguish sinks from actor models:

- `exec.Command` argument arrays prevent local shell splitting but do not prevent downstream option injection (`go build`, `tar`, `gcloud`) or later shell interpretation in generated Dockerfiles.
- Shell-form `RUN ... <concatenated input>` needs quoting/character validation.
- JSON-form `CMD [...]` needs JSON serialization, not string concatenation.
- Newlines can inject Dockerfile directives even when shell metacharacters are irrelevant.

A direct deployer-controlled `--entry_point_path` or URL is usually self-injection. Promote only if a lower-trust source realistically controls it through a checked-in wrapper/config, repository filename, template, CI variable, or product-managed metadata that a privileged deployer normally consumes.

## Secret-inclusion reportability gate

Archive inclusion is a primitive, not automatically a vulnerability. Establish at least one meaningful boundary:

- documentation or normal workflow places local credentials inside the default source tree;
- the CLI claims or implies ignore-file behavior but does not honor it;
- uploaded source archives are retained/readable to a broader principal set;
- attacker-controlled build code can observe files that should have been excluded;
- a shared-repository actor can predictably plant or route sensitive local files into the context;
- logs/errors expose archived content.

Downgrade when users explicitly select the directory, the cloud builder is the expected recipient, no lower-trust reader exists, and the effect is merely “deployment uploads source.”

## Temp cleanup

Immediately after successful `MkdirTemp`, register cleanup with `defer` unless retained artifacts are an explicit opt-in debug feature. Test failures at compilation, Dockerfile generation, archive creation, client initialization, upload, and operation polling.

A `0700` temp directory limits other local users but does not solve secret persistence, disk growth, backup/indexing, or later process access. Record leftover-artifact behavior separately from remote impact.

## Evidence and framing

Report separately:

1. exact included/excluded entries;
2. generated-build parsing sink;
3. realistic lower-trust input source;
4. who can read or execute the resulting artifact;
5. cleanup behavior;
6. non-claims—no real secret, no cloud deployment, no production compromise.

Do not merge independent archive overbreadth, build-command injection, option injection, and cleanup failures into one inflated finding unless one proven chain genuinely connects them.
