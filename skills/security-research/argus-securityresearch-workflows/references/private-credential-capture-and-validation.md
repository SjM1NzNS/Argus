# Private credential capture and validation

Use this when configuring PATs/API keys for an approved Argus integration under `~/.config/argus/`.

## Safe workflow

1. Never ask the user to paste a secret into chat, tool input, notes, reports, or committed files.
2. Inspect only metadata and booleans: file existence, owner/mode, expected assignment prefix, and whether the value is non-empty. Do not print the value, hashes, prefixes/suffixes, or full environment.
3. Identify the user's actual interactive shell before providing shell-specific `read` syntax.
4. Put `umask 077` before directory/file creation; enforce the private directory as `0700` and secret file as `0600`.
5. Refuse to overwrite a valid credential with an empty read. Unset the temporary shell variable afterward.
6. Verify the file non-destructively after capture. Authentication testing is a separate step and should use the least-privileged read-only endpoint.
7. An arbitrary `.env` file is not automatically available to Hermes or child programs. Explicitly source or parse it in the command that needs it; export only when the client reads `os.environ`.

## Bash versus zsh prompt pitfall

Bash commonly uses:

```bash
read -rsp 'PAT: ' PAT
```

Do not give this unchanged to zsh. In zsh, `read -p` means “read from the coprocess” and can fail with `read: -p: no coprocess`, leaving an empty variable that later gets written as `PAT=`.

A robust zsh pattern uses `/dev/tty` explicitly, which also avoids pasted script text being consumed as credential input:

```zsh
umask 077
mkdir -p ~/.config/argus
chmod 700 ~/.config/argus

printf 'PAT: ' >/dev/tty
IFS= read -rs PAT </dev/tty
printf '\n' >/dev/tty

if [[ -z "$PAT" ]]; then
  print -u2 'No PAT entered; file not updated.'
else
  printf 'PAT=%q\n' "$PAT" >| ~/.config/argus/service.env
  chmod 600 ~/.config/argus/service.env
  print 'PAT stored successfully.'
fi
unset PAT
```

Adapt the variable and filename to the integration. `%q` makes the assignment source-safe in zsh; confirm the intended consumer can parse shell quoting. For cross-shell clients, prefer a small `getpass` helper that writes the exact format the client expects.

## Interaction and UX pitfalls

- In instructions, clearly say that a code-fence language label such as `zsh` is not a command to paste. A literal leading `zsh` starts a nested shell and makes debugging confusing.
- Silent input intentionally shows no typed characters. State this immediately next to the command and tell the user to press Enter after typing.
- If the shell appears stuck ambiguously, have the user press Ctrl-C once, then rerun the explicit `/dev/tty` version.
- Do not launch an agent-owned background PTY and expect the user to enter a secret into it; the user cannot safely interact with that isolated process. Any dummy PTY test must be labeled as isolated, must not write the real config, and should be closed promptly so its completion notification is not mistaken for successful credential capture.

## Non-secret verification example

```zsh
(
  source ~/.config/argus/service.env
  [[ -n "$PAT" ]] && print 'PAT is present and non-empty.' \
                    || print -u2 'PAT is empty or missing.'
)
```

Prefer a parser-based boolean check when shell sourcing is not the consumer's real behavior. Never display the stored assignment while diagnosing it.
