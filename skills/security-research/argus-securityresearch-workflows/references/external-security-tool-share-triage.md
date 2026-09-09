# External security tool-share triage and adoption

Use this pattern when a researcher, social account, newsletter, or image list recommends security tools and the user asks which ones belong in Argus.

## Goal

Convert social discovery into a small, source-backed adoption decision. Do not mirror a generic tool list or install software because a post calls it useful.

## Workflow

1. **Inspect the original source first.** Read the supplied profile/post when accessible. If a logged-out social page hides posts, use public RSS/index/search copies only to locate the item, then cite the original post URL and verify claims against the project's repository/docs.
2. **Extract exact identities.** Record tool name, original post URL, canonical project URL, stated purpose, and whether the item is an original post, repost, article, or image-only list. Treat screenshots and captions as discovery, not technical authority.
3. **Resolve the user's intended frame before ranking.** If the user asks what is useful “for us” or “for Argus” generally, rank broad Argus value first. Put active-hunt relevance in a separately labeled secondary section only when useful; do not let current-session context silently redefine a general tooling question. If the user explicitly asks about the current evidence gap, lead with that gap. Classify every candidate as:
   - generally useful for Argus;
   - directly useful for the current evidence gap, when that frame was requested;
   - conditional on a discovered surface;
   - already covered by installed capability;
   - low-value, noisy, privacy-sensitive, or unrelated.
4. **Verify current project state.** Check the canonical repository/docs for maintenance, release/commit recency, archive status, runtime, dependencies, license, installation model, and exact functionality. Do not infer quality from stars alone.
5. **Check capability overlap.** Determine whether Argus already has the tool or an equivalent. Recommend a new dependency only when it adds material capability, fidelity, or workflow integration.
6. **Smoke-test shared commands locally.** Parse or run a no-target/empty-input control against the live CLI. Validate flag values and output modes. Social screenshots often contain stale flags, omitted required values, typos, or options that are ineffective without another mode. Preserve the corrected concept, not the broken command.
7. **Review extension/plugin trust before installation.** For Burp/browser/IDE plugins, inspect dependencies and code for outbound requests, remote UI assets, update checks, filesystem writes, process execution, and target-data handling. Prefer a dedicated profile or isolated environment for first use.
8. **Apply scope and privacy gates.** Third-party URL analyzers, hosted scanners, dork UIs, and cloud services may disclose private target names, DOMs, screenshots, requests, or search intent. Prefer local equivalents for private bounty work. A discovered hostname or historical URL is not automatic authorization.
9. **Preserve the established research mainline.** Historical URL tools, crawlers, regex endpoint extractors, and wordlists are secondary enrichment. They do not replace source-derived JS/config/API mapping, exact consumer tracing, evidence controls, or reportability gates.
10. **Adopt selectively.** Produce a ranked recommendation: add now, pilot in isolation, keep on-demand, already present, or skip. Store a concise curated review with provenance; do not ingest the full social feed or generic list.
11. **Harden before operational use.** Prefer checksum-verified release assets or immutable commits, isolated virtual environments/profiles, exact dependency records, and local inert fixtures. Review for disabled TLS verification, warning suppression, automatic redirects, outbound assets, auto-update behavior, and stress/DoS tests enabled by default. Where justified, expose a safe wrapper with risky modes opt-in and document the local delta from upstream.
12. **Verify claim level explicitly.** Distinguish source reviewed, installed, checksum verified, dependency imports passed, local fixture passed, application loaded, and UI feature observed. A staged Burp extension that compiles under Jython is not “loaded successfully” until Burp reports no extension error and the extension UI/tab is observed. If GUI accessibility is unavailable, preserve the manual verification gate instead of upgrading the claim.

For a concrete reusable installation and verification recipe—including safe wrappers, legacy Jython dependencies, hosted-tool launchers, and claim-level evidence—see `third-party-security-tool-adoption-hardening.md`.

## Security-research relevance gate

A tool is not useful merely because it is security-related. Tie it to the missing proof:

- For CI/CD findings, prioritize workflow/revision resolution, Actions call graphs, output consumers, runner semantics, and protected-decision evidence.
- Web crawlers, DNS resolvers, GraphQL scanners, command-injection exploiters, and wordlists do not upgrade a CI/CD finding unless they address a concrete missing gate.
- Prevalence tooling proves deployment/reachability, not incremental attacker capability. Always run the intended-authority counterfactual before using prevalence as the reportability argument.

## Command-review example class

For crawler screenshots:

- verify every flag against `--help` on the installed version;
- test with an empty target list or local inert fixture;
- check whether a flag requires a value;
- check whether extraction flags require JSONL or another output mode;
- review extension filters for typos;
- add explicit scope controls before any authorized live use.

## Adoption output format

Use a compact table:

| Tool | Decision | Marginal capability | Risks/conditions | Source |
|---|---|---|---|---|

Then state:

- which tool, if any, helps the current task;
- what Argus already has;
- what should be piloted or installed;
- what should be skipped and why;
- whether any project code/command was actually reviewed or smoke-tested.

## Pitfalls

- Do not repeat a social post's marketing language as a technical conclusion.
- Do not treat an image list as a curated/versioned toolchain.
- Do not install a large generic stack when one missing capability is enough.
- Do not send private target material to third-party analysis platforms without explicit approval and policy fit.
- Do not equate “actively maintained” with “safe to load into Burp/browser/IDE.”
- Do not preserve transient environment failures as durable tool limitations; preserve the source-fallback or verification method that worked.
