# Security Video PoC Production and Validation

Use this reference when a program requests a video for an already-submitted finding. The goal is a concise recording of a **fresh verified execution**, not a narrated animation or a replay of stale screenshots.

## 1. Lock the claim before recording

- Start from the submitted title, reference ID, strongest portable reproducer, and current non-claims.
- Record only the demonstrated trust-boundary chain. Do not add a stronger conditional branch merely because it is visually dramatic.
- Prefer a harmless unique canary and owned/local state.
- Decide the visual proof gates in advance: prerequisite/target, attacker action, request metadata, before state, after state, exact assertion result, and limitations.

## 2. Re-run the untouched proof first

Before changing timing or presentation:

1. Execute the original portable harness against the current tested runtime.
2. Write results to a new path rather than overwriting preserved submission evidence.
3. Require a machine-readable `overallPassed` value plus every decisive assertion.
4. Stop if the fresh run fails. A prior positive result is not permission to manufacture a successful video.

Keep the original reproducer untouched. Put countdowns, headed-browser flags, result dashboards, and recording delays in a clearly named recording-only copy.

## 3. Isolate the recording environment

Prefer a dedicated virtual display and disposable browser profile so recording does not expose or disturb the user's desktop:

```text
Xvfb / isolated display
→ minimal window manager
→ terminal showing the exact run
→ headed browser with disposable profile
→ ffmpeg screen capture
```

Use a matching browser/driver pair. Keep the product server, attacker page, and browser automation in one self-cleaning harness where practical. Terminate temporary tunnels, browser sessions, profiles, servers, and recorders in `finally`/trap cleanup.

## 4. Make the proof legible without changing it

A useful video should visibly show:

1. report/reference identifier and local target startup;
2. attacker-controlled origin and secure-context status where relevant;
3. exact request primitive and destination;
4. automatic action/countdown when proving no-click behavior;
5. the target-side request class (`Content-Type`, `Origin`, Fetch Metadata, method/path);
6. compact before/after state using the same unique canary;
7. explicit true/false assertions and a clear overall result;
8. material limitations or provider errors that occur after the proven side effect.

Presentation code may delay submission, style pages, or render live JSON, but it must not alter the exploit request, target behavior, or success predicate. Label browser automation honestly; do not hide automation banners to imply manual execution.

## 5. Fail closed on orchestration

Do not trust a wrapper's exit code alone. GUI launchers and terminal emulators may return zero even when the child harness failed.

After recording, require all of:

- expected live-result file exists and is non-empty;
- `overallPassed == true`;
- every decisive assertion is true;
- the before/after canary relationship is exact;
- preserved sentinel/control state remains intact;
- browser/runtime provenance matches the claimed run.

For temporary public-host infrastructure, retry with a fresh hostname or alternate authoritative/public DNS resolution path when propagation is delayed. Treat this as delivery infrastructure recovery only; never replace the public-origin proof with a weaker local simulation without disclosing the change.

## 6. Video QA gates

Run both machine and visual checks:

### Machine checks

- inspect codec, dimensions, frame rate, duration, and size;
- decode the entire video to a null sink to catch corruption;
- verify the live result independently of the video;
- scan scripts/results/logs for JWTs, API keys, private-key blocks, credentials, and private IDs;
- hash the final upload artifact.

### Visual checks

Sample frames from semantic phases, not only fixed timestamps:

- opening/prerequisite;
- attacker page immediately before action;
- navigation/transition;
- compact result screen;
- ending assertion output.

When setup duration varies, derive sample times relative to the end or identify transitions first. Check legibility, clipping, secrets, misleading labels, stale canaries, and whether before/after values are actually visible above the fold.

## 7. Trim only idle time

Long tunnel/build/startup waits can be removed after a successful continuous recording, provided the edit preserves:

- opening target/provenance evidence;
- the complete attacker action/countdown;
- browser transition;
- complete result screen;
- terminal/live assertion output.

Use a visible cut rather than fabricating continuity. Never splice successful phases from different runs while presenting them as one execution.

After any trim or transcode:

1. decode the final video again;
2. re-sample visual frames;
3. recompute SHA-256;
4. replace the upload-package copy;
5. regenerate the manifest;
6. update every note that embeds the old hash or duration.

## 8. Upload package and response

Keep the initial package small:

```text
<reference>-video-poc/
├── concise-reference-video.mp4
├── README.md
└── manifest.json
```

The README should state what is proven, the exact non-claims, runtime/browser provenance, media metadata, result status, and final hash. Provide a short portal reply describing the attachment without escalating impact. Do not upload or post externally unless the user explicitly asks.

## Pitfalls

- Producing a polished video from stale JSON without a fresh live run.
- Letting recording-only code replace the original success predicate.
- Declaring success from the recorder/wrapper exit code while the child harness failed.
- Showing only an opaque browser error and omitting target-side state evidence.
- Showing before/after headings while the actual values are clipped below the fold.
- Treating CORS response opacity as evidence that a write-only request failed.
- Leaving a minute of idle setup when it can be transparently trimmed.
- Updating the MP4 but leaving stale hashes in the README, manifest, or target ledger.
- Including conditional RCE/tool behavior in a video for a narrower session-integrity report.
