---
type: source-summary
status: promoted
created: "2026-07-07"
pass: "D"
sources:
  - "https://github.com/swisskyrepo/PayloadsAllTheThings"
  - "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection"
  - "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery"
  - "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files"
  - "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal"
  - "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection"
  - "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/JSON%20Web%20Token"
  - "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/OAuth%20Misconfiguration"
  - "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Open%20Redirect"
  - "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/CORS%20Misconfiguration"
  - "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection"
external_rag_support:
  - "https://rodoassis.medium.com/top-10-xss-payloads-e4774a43e285"
  - "https://blog.ostorlab.co/polyglot-xss.html"
  - "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Clickjacking/README.md"
  - "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/README.md"
---

# Pass D PayloadsAllTheThings Controlled Source Summary

## Scope

Pass D reviewed selected `swisskyrepo/PayloadsAllTheThings` sections as a controlled methodology/payload-reference source. Raw selected files were stored under:

`01 - Learning/Inbox/manual-20260707-pass-d-payloadsallthethings-controlled/`

This pass deliberately avoids copying large payload lists into active playbooks.

## Selected sections

- XSS Injection
- SQL Injection
- Server-Side Request Forgery
- Upload Insecure Files
- Directory Traversal
- Open Redirect
- OAuth Misconfiguration
- JSON Web Token
- GraphQL Injection
- CORS Misconfiguration
- CRLF Injection
- Web Cache Deception
- Clickjacking
- NoSQL Injection
- XXE Injection

`Web Cache Poisoning` was not present as a current top-level README in the fetched tree; use existing Web Security Academy/cache notes for cache-poisoning methodology.

## Promotion rule

PayloadsAllTheThings is a payload/methodology index, not a test plan to spray against targets.

Argus should use it to:

1. identify the vulnerability class and sink/parser context;
2. pick one or two harmless, context-matched proof shapes;
3. remove exfiltration, beaconing, destructive, malware-like, or broad-fuzzing behavior;
4. apply local playbook evidence/reportability gates;
5. save raw evidence only for the selected proof path.

## Promoted class lessons

| Class | Controlled Argus use |
|---|---|
| XSS | Select payload by sink context; use owned-context marker; no credential theft/beaconing. |
| SSRF / XXE | Start with owned callback and parser primitive; metadata/internal/protocol tests require approval. |
| File Upload / Traversal | Test validation layers and canonicalization with harmless synthetic filenames/files. |
| OAuth / Open Redirect / JWT | Use as chain seeds; require auth/session/token impact, not redirect or decode behavior alone. |
| GraphQL / SQL / NoSQL | Use detection payloads only after endpoint/schema/input is mapped; require unauthorized data/action impact. |
| CORS / Clickjacking / CRLF / Cache Deception | Require browser/cache/victim-path evidence and sensitive data/action impact. |

## External RAG check

Preview.is returned relevant source support for payload-selection discipline, including XSS payload selection writeups, polyglot XSS discussion, and PayloadsAllTheThings sections for Clickjacking and Directory Traversal. These results are Zone 0 support only and do not authorize live target payloading.
