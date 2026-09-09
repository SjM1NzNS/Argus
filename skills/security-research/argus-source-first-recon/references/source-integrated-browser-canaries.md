# Source-integrated browser canaries

Use this pattern when a browser-reachable candidate can be proven with exact pinned source, but a full product build would add unrelated dependency/setup risk. The goal is stronger than a primitive-only demo: preserve the real source parser and the real sink-owning method while replacing only surrounding infrastructure with inert collaborators.

## Promotion standard

A source-integrated canary should prove this chain:

```text
attacker-shaped input
  -> exact pinned parser/normalizer
  -> exact product field/object
  -> exact sink-owning product method
  -> genuine browser interaction
  -> observable owned canary effect
```

Do not call a standalone `window.open`, `innerHTML`, navigation, or fetch primitive proof a product reproduction. Keep that as a browser-behavior control until the exact source chain also passes.

## Build the minimal harness

1. **Pin provenance first.** Record repository URL, commit, tested release tag, acquisition time, and source hashes.
2. **Serve only loopback.** Use a temporary loopback HTTP server rooted at the mission directory. Derive safe-control URLs from `location.origin`; do not hard-code a transient port.
3. **Load exact source files directly.** Include only the parser, utility, and sink-owner files required for the chain. For Closure-style or namespace-based projects, provide a minimal namespace/`require` shim rather than rebuilding the entire application.
4. **Stub infrastructure, not security logic.** Replace logging, event dispatch, timers, tracking, media state, and constructors with inert collaborators only when they are not part of the suspected boundary. Never reimplement the parser, validator, sanitizer, URL assignment, or sink.
5. **Avoid constructor noise when safe.** For a large manager class, instantiate with `Object.create(Class.prototype)` and populate only fields used by the target method. This preserves the exact method body without triggering unrelated services. Document every stub.
6. **Prove source identity.** Record `typeof`/namespace presence, parsed field values, and source file hashes. Anonymous assigned classes may have an empty `.name`; do not treat that as absence.
7. **Give positioned overlays a containing block.** Product overlay code often uses absolute positioning. Separate controls with `position: relative` containers and add `role`, `tabindex`, stable IDs, and labels after product rendering so automation can target the real rendered element.

## Browser interaction and controls

Use CDP or a real browser driver to dispatch an actual mouse event at the rendered product element. A direct DOM `.click()` or direct invocation of the handler may not preserve user-activation behavior for popups, clipboard, fullscreen, or autoplay.

Required controls:

- pre-interaction canary remains unchanged;
- attacker and safe resources both load;
- an intended-scheme loopback control behaves normally and does not trigger the attacker canary;
- the candidate input survives the exact parser/normalizer unchanged where that is the claim;
- the post-interaction effect is observed in the correct context;
- popup/iframe opener, parent, origin, and target state are explicitly inspected when relevant;
- no non-loopback traffic occurs.

For popup findings, retain both the opener page state and popup target metadata. Browser automation may switch to the popup; close it or attach to the original target before taking the final screenshot.

## Reproducible CDP artifact

Prefer a one-command script that:

1. allocates ephemeral loopback HTTP and debugging ports;
2. launches a clean temporary Chrome profile;
3. opens the harness through CDP;
4. waits for source files and rendered controls;
5. records structured pre-state;
6. dispatches `Input.dispatchMouseEvent` at the product-rendered element;
7. records structured post-state and target metadata;
8. captures a screenshot;
9. writes deterministic JSON and exits nonzero unless all assertions pass;
10. terminates Chrome, the temporary server, and the profile in `finally` cleanup.

Parameterize the source root, expected commit, and output suffix. Run the same harness against the pinned development commit and the latest affected release tag when practical. This distinguishes an unreleased regression from a shipped issue without duplicating harness logic.

## Prior-art and reportability gate

Delay public issue/PR duplicate search until the candidate is technically validated and immediately before final drafting. This reduces confirmation bias during exploration while still preventing novelty overclaims.

Search several semantic forms, not only the proposed title:

- field or API name;
- exact sink plus subsystem;
- vulnerability class plus parser/protocol;
- dangerous scheme or encoding;
- original feature-introduction PR.

When prior art appears, inspect the full state, diff, comments, reviews, merge status, and released code. A closed or unmerged fix can mean rejected premise, incomplete coverage, duplicate private handling, or unresolved risk. Record separately:

```text
technical impact: confirmed | disproved
same sink covered: yes | no | partial
same source covered: yes | no | partial
released fix present: yes | no
novelty risk: low | medium | high
submission posture: private report | notification | park
```

A prior patch for one URI field does not automatically cover an adjacent click-through or redirect field. Conversely, a public discussion of the same working source-to-sink class materially raises duplicate risk even if its proposed patch was incomplete.

## Evidence hygiene and closure

Before promotion:

- run the canary again after every harness change;
- parse result JSON and assert pre-state, post-state, revision, and control URL;
- hash scripts, harnesses, JSON, screenshots, and report drafts;
- verify main and release worktrees are clean;
- scan promoted artifacts for credentials and API keys;
- stop temporary listeners and browser processes;
- preserve a branch-exhaustion ledger with killed alternatives;
- separate **The problem** from **Impact analysis** and state actor, required interaction, deployment dependence, prior art, and non-claims.

## Common pitfalls

1. **Primitive-only overclaim.** Browser behavior is not product reachability.
2. **Over-stubbing.** Reimplementing the suspected parser or sink invalidates the proof.
3. **Synthetic-click false negative/positive.** Use a real CDP mouse event for user-activation-sensitive behavior.
4. **Hard-coded loopback port.** Safe controls silently stop being comparable on rerun.
5. **Overlay collision.** Absolute product styles can stack attacker and control elements; isolate containing blocks.
6. **Popup context confusion.** Automation may inspect the new blank page instead of the modified opener.
7. **Main-only evidence.** Verify a released revision before claiming affected users.
8. **Title-only duplicate search.** Read disposition and diff; an incomplete closed PR can both raise duplicate risk and leave a distinct sink unfixed.
9. **Transient harness fix captured as product behavior.** Record the durable pattern, not one environment's missing package, port, or origin mismatch.
