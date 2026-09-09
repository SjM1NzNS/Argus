# ARGUS SPECIALIST DISPATCHER

Codex is the main reasoning backend.

External specialists and tools are optional. They are not the hunt manager.

Available specialist backends may include:

- Codex / GPT
- local models
- static analyzers
- custom scripts
- reconFTW
- Burp
- Semgrep
- Slither
- future Claude-like tools if available

Specialists produce leads, not truth.

Argus must:

1. define a bounded task
2. provide only relevant context
3. define output format
4. validate output against scope
5. validate output against evidence
6. convert useful output into hypotheses/tests/notes
7. discard unsupported speculation

If a specialist is unavailable, Argus must decompose the task into smaller internal tasks and continue.
