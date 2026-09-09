# Frontend chunk closure and verified TLS-chain retry

Use this reference when a source-first SPA pass must prove that its exact executable graph is closed, or when an approved HTTPS request fails because the server omits an intermediate CA certificate.

## 1. Close frontend graphs to a fixed point

Do not equate one asset-prefix regex with graph exhaustion. Production bundlers may encode the same lazy graph through several literal forms:

- root HTML `<script src>` and `<link href>` references;
- `/assets/chunk.js` or `assets/chunk.js` strings;
- relative `import("./Chunk.js")` calls inside an entry or lazy chunk;
- bundler preload arrays and module maps;
- `new URL("./asset", import.meta.url)`;
- CSS `@import` and `url(...)` references when relevant to the security surface.

Safe closure loop:

1. Hash and inventory the already-approved acquired files.
2. Extract each literal reference class separately and preserve the source file/offset or line.
3. Normalize only against the exact known same-origin base; never infer siblings or guessed paths.
4. Compute `referenced - acquired` locally.
5. If the set is non-empty, create a fixed manifest, request budget, pace, redirect policy, and stop conditions before retrieval.
6. Retrieve only that manifest under the target's approval contract.
7. Repeat until the fixed-point set is empty.
8. Record the parser version/pattern classes and any corrected miss. Do not hide a first-pass extractor limitation.

Completion evidence should state both the number of acquired artifacts and `missing_literal_references: 0`. A successful first batch is not graph exhaustion if another literal form remains.

## 2. Retry an omitted-intermediate TLS chain without bypassing verification

A curl/OpenSSL failure such as `unable to get local issuer certificate` is a stop signal, not permission to add `-k`. If the user or target contract authorizes a retry, distinguish an omitted server intermediate from a bad hostname, untrusted root, or local trust-store problem.

### Diagnostic sequence

```bash
openssl s_client \
  -connect "$HOST:443" \
  -servername "$HOST" \
  -showcerts </dev/null > tls-handshake.txt 2>&1
```

Record only public certificate metadata:

- number and order of served certificates;
- leaf subject/SAN, issuer, validity, and SHA-256 fingerprint;
- OpenSSL verify errors/return code;
- Authority Information Access CA Issuers URL.

If the server supplied only a valid hostname-matching leaf and the leaf exposes an AIA issuer URL:

1. Retrieve that exact public CA artifact. An HTTP AIA response is **untrusted input** until cryptographically validated.
2. Convert DER/PEM as required.
3. Confirm the intermediate subject exactly matches the leaf issuer.
4. Validate the intermediate to the system trust roots:

```bash
openssl verify \
  -CAfile /etc/ssl/certs/ca-certificates.crt \
  intermediate.pem
```

5. Build a temporary/private augmented CA bundle containing the unchanged system roots plus the validated intermediate.
6. Extract the leaf and verify both chain and hostname:

```bash
openssl verify \
  -verify_hostname "$HOST" \
  -CAfile augmented-ca-bundle.pem \
  leaf.pem
```

7. Retry the originally approved request using `curl --cacert augmented-ca-bundle.pem ...` with the original redirect, method, body-size, pacing, and stop controls unchanged.

### Hard stops

Do not retry if:

- the leaf hostname does not match;
- the retrieved intermediate fails system-root validation;
- subject/issuer binding does not match;
- the chain terminates at an untrusted/private root;
- the target contract forbids the extra handshake or retry;
- the retry would require `-k`, `--insecure`, disabled hostname verification, forced IP/Host routing, or a different origin.

### Disposition

Treat an omitted intermediate as a deployment/interoperability observation unless a concrete security impact is demonstrated. Browser success through cached/AIA-fetched intermediates does not erase the server-chain defect, but the defect alone is generally not an authorization, confidentiality, or integrity finding.

Keep the handshake, public certificates, augmented bundle, request metadata, and response evidence private and hashable. Sanitize cookies and authorization headers exactly as in ordinary live evidence handling.
