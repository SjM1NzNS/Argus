---
type: source-summary
run: daily-20260727-073001
reviewed: "2026-07-27"
promotion: "Web2 log output neutralization"
---

# Daily 2026-07-27 — log output-neutralization promotion

## Run quality

- Reviewed all **3 actual-content records** from **218 combined records** (**1.4%** actual content).
- The run remained discovery-heavy: **71 index/listing records** (**32.6%**) and **134 not-fetched records** (**61.5%**).
- Static ingestion supplied 2 actual-content records; browser-DOM ingestion supplied 1.

## Manual dispositions

1. **Bug Bounty Daily** — rejected as CSS/import-map/base64 application bootstrap. The compiler's AI/LLM label came from bundled MCP/model dependencies, not vulnerability methodology, evidence gates, or reportability guidance.
2. **WordPress official release feed** — no new promotion. WordPress 7.0.2 affected/fixed versions, CVEs, REST batch-route confusion, SQLi/RCE composition, and safe evidence gates were already promoted on 2026-07-17. WordPress 7.1 Beta 3 added testing/release context only.
3. **HackerOne Hacktivity** — manually reviewed as a page of platform-generated summaries, not source-native reports. Promoted only the narrow, target-independent log output-neutralization lesson triggered by the Monero ZMQ summary. The other summaries either repeated existing JWT algorithm-pinning, exact OAuth redirect binding, object/resource-scoped authorization, XSS serializer/export, and cloud confused-deputy gates, or lacked enough original detail for promotion.

## Promoted lesson

The durable boundary is:

```text
attacker-controlled bytes
→ decoding and semantic validation
→ logger/serializer
→ emitted record
→ collector/viewer/automation consumer
```

Logging before semantic validation increases reachability but is not proof. Reportability requires evidence that record delimiters or control data survive output neutralization and corrupt a trusted event/field, parser, audit decision, alert, or separately proven downstream consumer. Visual line wrapping, source concatenation, and hypothetical follow-on execution are kill controls.

This was promoted into [[log-output-neutralization|Log Output Neutralization]], REST API routing/checklist guidance, and four eval scenarios.

## External reference check

The Preview.is wrapper timed out. One direct env-backed API retry succeeded; no key was written to the vault.

- **Query:** `CRLF log injection log forging reportability evidence negative controls parser normalization untrusted log persistence downstream log consumer injection`
- **Retrieved:** `2026-07-27T07:07:43Z`
- [CWE-117: Improper Output Neutralization for Logs](https://cwe.mitre.org/data/definitions/117.html), score `0.9776`, matched CWE impact/mitigation sections: external input can misdirect log interpretation, corrupt automated parsing, or reach a vulnerable log-processing utility.
- [Invicti: CRLF Injection](https://www.invicti.com/learn/crlf-injection), score `0.987`, matched `What is CRLF injection?` and `Example of log poisoning`: distinguish log forging from HTTP response splitting and validate the actual logger/parser behavior.

The retrieval was Zone 0 source support, not target evidence. No raw RAG corpus was promoted.

## Watchlist and noisy sources

- Keep the new HackerOne GitHub App token-scope and Monero log-injection disclosures on the watchlist for source-native report detail; do not infer exact exploit mechanics or severity from auto-generated summaries.
- AppSec.fyi topics, Code4rena/Sherlock/Cantina indexes, repository roots, robots-blocked pages, metadata-only records, and seen/deferred links remained discovery material.
- Solodit emission-cap, provenance, missed-epoch, and emergency-council titles were skipped as seen and supplied no new reviewed mechanics.
