# V3 corpus extraction pass 2 — Mobile

Session-specific reference for the successful Mobile pass over `~/Downloads/Cybersecurity - V3/Topics/Mobile/` into the active Argus SecurityResearch vault.

## Trigger

Use when continuing the legacy V3 corpus extraction sequence or enriching mobile bug-bounty methodology from old vault material.

## Source families used

- YesWeHack Android guides: APK acquisition, Android recon, Genymotion/lab setup, MobSF/jadx/static analysis, Frida/pinning runtime context.
- YesWeHack iOS guides: IPA extraction, static/dynamic analysis, proxy setup, jailbreak/pinning/local-auth context.
- Hacker101 mobile tracks: iOS filesystem, inter-app communication, app transport, WebViews; Android quickstart/common bugs.
- OWASP MASVS/MASWE and Mobile Top 10: STORAGE, AUTH, NETWORK, PLATFORM, CODE, PRIVACY, RESILIENCE.

## Active vault outputs from the pass

Created:

- `02 - Vulnerability Playbooks/Web2/Mobile API/android-static-recon.md`
- `02 - Vulnerability Playbooks/Web2/Mobile API/ios-platform-testing.md`
- `02 - Vulnerability Playbooks/Web2/Mobile API/reportability.md`
- `06 - Evals/Web2/mobile-api-v3-pass2-eval-scenarios.md`
- `00 - System/v3-corpus-extraction-pass-2-mobile-2026-07-02.md`

Patched:

- `02 - Vulnerability Playbooks/Web2/Mobile API/overview.md`
- `02 - Vulnerability Playbooks/Web2/Mobile API/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Mobile API/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Mobile API/false-positives.md`
- `00 - System/web2-skill-index.md`
- `07 - Skill Changelog/2026-07.md`

## Key extraction lessons

### Do not collapse mobile into API-only

The existing target area was `Mobile API`, but V3 mobile material covered full app/platform testing. Preserve mobile-app coverage even if the active folder remains under Web2/Mobile API:

- Android APK/static recon and exported components;
- iOS IPA/platform testing;
- deep links, app links, universal links, URL schemes;
- local storage, Keychain, pasteboard, backups, logs, screenshots;
- WebViews and native bridges;
- network security config and ATS;
- certificate pinning/root/jailbreak/RASP as context, not automatic findings.

### Mobile artifact provenance is mandatory

For APK/IPA-derived leads, record:

- package/bundle ID;
- version;
- source (official store, device extraction, mirror, TestFlight/internal if authorized);
- split APK/app-bundle components or IPA structure;
- architecture/feature/language split if relevant;
- artifact hash.

Historical/mirror artifacts are good for recon and diffing, but live reportability requires the current backend/app path still accepts the behavior.

### Reportability gates

Report mobile findings when there is concrete impact:

- mobile-only backend authorization bypass;
- embedded production secret with validated unauthorized capability;
- Firebase/cloud/storage config plus weak rules/scopes enabling read/write/list/action;
- deep-link/OAuth token/code leak or sensitive action;
- exported Android component leaking sensitive data or triggering protected functionality;
- iOS scheme/universal-link/pasteboard issue crossing auth/data/action boundaries;
- local storage exposure with realistic attacker access and sensitive data;
- WebView bridge reachable from untrusted content with native data/action impact;
- weak transport only when sensitive scoped traffic can be intercepted/modified and backend accepts the flow.

Reject or downgrade:

- decompilation-only;
- missing obfuscation/RASP/pinning/jailbreak detection only;
- public IDs/API bases/Firebase config with locked rules;
- deep links that only open screens with normal confirmation/server auth;
- pinning bypass only on the researcher's controlled device;
- dead historical endpoints.

### Eval scenarios added

The pass added eval coverage for:

1. public Firebase config with locked rules;
2. embedded mobile key granting object read;
3. certificate pinning bypass only;
4. exported activity with confirmation preserved;
5. exported content provider leaking token;
6. iOS custom URL scheme OAuth hijack;
7. ATS exception without impact;
8. WebView bridge to native action;
9. historical APK route still working against live backend.

## Verification pattern

After each V3 pass, verify touched files are non-empty and contain no `TODO`/`TBD` placeholders. For pass 2, the verification list included all created/modified Mobile API notes, the eval scenarios, the Web2 skill index, changelog, and pass report.
