---
type: source-summary
status: promoted
created: "2026-07-17"
source_group: "Intigriti bug bounty classics — five write-ups"
sources:
  - "https://rhinosecuritylabs.com/research/java-deserializationusing-ysoserial/"
  - "https://palant.info/2020/06/22/exploiting-bitdefender-antivirus-rce-from-any-website/"
  - "https://medium.com/@win3zz/simple-story-of-some-complicated-xss-on-facebook-8a9c0d80969d"
  - "https://blog.r0b.re/hacking/pentesting/bugbounty/recon/web/python/bash/2020/06/25/Crafting-a-custom-wordlist-for-flask-webservers.html"
  - "https://web.archive.org/web/20200627103005/https://r2c.dev/blog/2020/hardcoded-secrets-unverified-tokens-and-other-common-jwt-mistakes/"
---

# Intigriti bug bounty classics — five-article promotion

## 1. Customized ysoserial / Java deserialization

**Historical chain:** a Base64 field decoded to a deflate-compressed Java object. A generated gadget failed because the wrapper had to be produced inside the serialization workflow and the target’s dependency `serialVersionUID` differed from the generator’s class version.

**Promoted lesson:** preserve every transformation boundary and separate native-deserialization reachability, integrity checks, filters, classpath, dependency/version compatibility, environmental trigger, and safe impact. A version mismatch is evidence—not permission to force compatibility or proof of RCE. Prefer source/classpath evidence and inert controls; do not spray gadget chains.

**Artifact:** `02 - Vulnerability Playbooks/Web2/Deserialization/overview.md`.

## 2. Bitdefender CVE-2020-8102

**Historical chain:** antivirus-generated certificate-error content remained readable under the website’s origin; session values from that content authorized a local product command surface; a banking-browser launcher accepted attacker-influenced input; unsafe command-line construction allowed flag injection and code execution.

**Promoted lesson:** map remote-origin → product-injected/replaced content → token exposure → browser-reachable local command API → argument construction → process capability. Each small weakness may be non-reportable alone; the chain requires every link, browser/version behavior, installed product/version, and a minimum safe local proof. Modern CORS/PNA/browser changes and product patches are mandatory negative controls.

## 3. Facebook/MicroStrategy reflected XSS

**Historical chains:**

- an unauthenticated file-processing task reflected uploaded file contents without encoding, but exploitability initially failed because a manual proxy upload did not prove that an attacker website could choose a victim’s local file; the researcher then established a browser-deliverable multipart path;
- a server-side scraper accepted an attacker URL only when the fetched page matched parser prerequisites, then reflected attacker-hosted content without encoding.

**Promoted lesson:** reflection plus manual request editing is insufficient. Prove that an attacker controls the carrier bytes and can drive the ordinary browser/server workflow. For remote-content renderers, preserve fetch ownership, parser prerequisites, transformation, response context, CSP, and victim navigation. File acceptance and XSS are separate gates.

## 4. Flask framework route corpus

**Historical method:** search public GitHub code for `@app.route`, extract literal paths, normalize variable converters, and build a Flask-specific discovery list.

**Promoted lesson:** framework-specific source mining can outperform generic wordlists, but modern extraction must include blueprints, prefixes, `add_url_rule`, aliases, converters, multiline/dynamic declarations, methods, and provenance. Exact target-derived routes remain first priority; corpus guesses are bounded candidates and uniform 200/catch-all responses are negatives.

**Artifact:** `10 - Tools/Web2/framework-derived-route-corpus.md`.

## 5. Common JWT mistakes

The review of 2,000 npm modules highlighted hardcoded signing keys, explicit `none` acceptance, decode-without-verify flows, unverified claims used before validation, and accidental sensitive claims from signing entire ORM objects.

**Promoted lesson:** model JWT trust as parse-untrusted → select trusted algorithm/key policy → verify signature → validate issuer/audience/time/type/token-use → authorize. Header and claims are untrusted until validation. Hardcoded keys are capability leads only if exposed and active; sensitive JWT claims matter because signed JWTs are typically readable, not encrypted. Use owned tokens and authorization-state controls—never brute-force secrets.

## Cross-source lesson

The strongest common pattern is **feasibility before payload sophistication**:

- exact transformation pipeline before gadget changes;
- browser-attacker control before reflected-XSS claims;
- every local-product chain link before RCE severity;
- target/framework fit before corpus discovery;
- cryptographic verification and authorization change before JWT findings.
