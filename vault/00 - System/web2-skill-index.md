# WEB2 SKILL INDEX

Argus uses this index to dynamically load Web2 playbooks based on discovered surfaces, tool output, hypotheses, and evidence gaps.

## Access Control / IDOR / BOLA / BFLA

Triggers:

- object IDs
- user IDs
- organization IDs
- project IDs
- tenant IDs
- role changes
- invite flows
- admin-only endpoints
- cross-account access
- API response differences between users
- PDF, CSV, or report export
- generated artifact or alternate representation
- projection, per-record, or per-field visibility
- email-domain allowlist
- organization or tenant membership derived from an email string
- verification delivered to a different mailbox than the application authorized

Load:

- `02 - Vulnerability Playbooks/Web2/Access Control/overview.md`
- `02 - Vulnerability Playbooks/Web2/Access Control/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Access Control/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/Access Control/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Access Control/reportability.md`
- `02 - Vulnerability Playbooks/Web2/Authentication & Session/email-identity-and-domain-authorization.md`

## Authentication & Session

Triggers:

- login
- logout
- password reset
- email change
- MFA
- 2FA / two-factor authentication
- OTP / factor challenge
- pre-MFA or provisional session
- backup/recovery code
- remembered device / device trust bypass
- authentication assurance state
- session cookie
- cookie policy / missing cookie flags
- `Secure`, `HttpOnly`, `SameSite`, `Domain`, `Path`
- `__Host-` / `__Secure-` prefix
- cross-site cookie delivery, sibling-subdomain same-site behavior, or cookie shadowing
- remember-me token
- device trust
- account recovery
- invitation acceptance
- JWT
- JSON Web Token
- hardcoded signing key
- decode without verify
- alg:none
- email-domain allowlists or organization membership inferred from email
- mailbox verification and email parser/canonicalization differences
- encoded-word or IDNA handling at an identity boundary

Load:

- `02 - Vulnerability Playbooks/Web2/Authentication & Session/overview.md`
- `02 - Vulnerability Playbooks/Web2/Authentication & Session/cookie-security.md` for cookie flags, delivery, scope, prefix, CSRF/XSS, plaintext, or shadowing claims
- `02 - Vulnerability Playbooks/Web2/Authentication & Session/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Authentication & Session/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/Authentication & Session/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Authentication & Session/email-identity-and-domain-authorization.md`

## OAuth / SSO

Triggers:

- OAuth login
- SAML
- OIDC
- redirect_uri
- state
- nonce
- PKCE
- account linking
- social login
- SSO role mapping
- SAMLResponse
- Assertion Consumer Service / ACS
- InResponseTo
- SubjectConfirmationData
- Destination / Recipient / Audience
- XML Signature Wrapping / XSW
- IdP-initiated SSO
- RelayState
- SAML assertion replay
- authorization-server mix-up
- authorization response `iss`
- multiple authorization servers or crossed issuer/token endpoint
- authorization-code injection or substitution
- `code_challenge` / `code_verifier`
- OIDC `(iss, sub)` identity key
- `email_verified` and unverified provider registration
- email-domain SSO access gates

Load:

- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/overview.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/reportability.md`
- `02 - Vulnerability Playbooks/Web2/Authentication & Session/email-identity-and-domain-authorization.md`

## GraphQL

Triggers:

- `/graphql`
- GraphQL introspection
- mutations
- node IDs
- batching
- role-sensitive queries
- hidden operations
- schema leaks

Load:

- `02 - Vulnerability Playbooks/Web2/GraphQL/overview.md`
- `02 - Vulnerability Playbooks/Web2/GraphQL/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/GraphQL/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/GraphQL/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Access Control/test-checklist.md`

## Source-First Artifact Mapping

Triggers:

- saved HTML, JavaScript, TypeScript, runtime config, build manifest, or service worker
- JavaScript-discovered endpoints or object selectors
- source maps or `sourcesContent`
- OpenAPI / Swagger specifications
- structured API validation errors
- HAR sanitization or evidence manifests
- candidate disposition or cross-run delta review
- Certificate Transparency / CT log / certificate SAN monitoring
- newly logged certificate names, passive DNS deltas, or wildcard certificate expansion
- SAST/taint/scanner/agent output, unexecuted PoCs, or claims of verified/clean source review
- per-module input/sink inventory, all-callers/all-writers downgrade, or coverage-gap reconciliation
- fixed-commit CI workflow, manifest, lockfile, registry, SBOM, or release review

Load:

- `02 - Vulnerability Playbooks/Web2/Source-First Mapping/overview.md`
- `00 - System/external-agent-skill-source-review-capitalone-vulnhunter-2026-07-31.md` when evaluating VulnHunter or borrowing agentic review methodology
- Hermes skill `argus-source-first-recon` for local-only extraction and sanitization scripts
- `08 - Templates/candidate-disposition.yaml.template`
- `08 - Templates/evidence-manifest.yaml.template`
- `08 - Templates/chain-edge.yaml.template`
- `08 - Templates/cross-run-delta.yaml.template`

## Server-Side Template Injection / SSTI

Triggers:

- SSTI / server-side template injection
- template engine / template renderer
- Jinja2 / Mako
- Twig / Smarty
- ERB / HAML / Slim
- EJS / Handlebars / Pug
- Thymeleaf / FreeMarker / Pebble
- Razor
- compile-from-string / render-from-string
- dynamic template source, include, expression, or template path
- custom template globals, filters, helpers, objects, or sandbox
- user-authored email, PDF, document, notification, invoice, or report templates

Load:

- `02 - Vulnerability Playbooks/Web2/Server-Side Template Injection/overview.md`
- `02 - Vulnerability Playbooks/Web2/Server-Side Template Injection/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Server-Side Template Injection/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/Server-Side Template Injection/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Server-Side Template Injection/reportability.md`
- `02 - Vulnerability Playbooks/Web2/Source-First Mapping/overview.md` when source is available

## REST API / Business Logic

Triggers:

- REST API endpoints
- hidden endpoints
- JavaScript-discovered endpoints
- hidden parameters
- mass assignment / over-posting / automatic object binding
- unexpected JSON properties or backend-only fields
- role, tenant, owner, approval, price, quota, verification, or workflow fields accepted from a lower-trust actor
- WAF bypass
- SQL injection / SQLi parser signals
- state transitions
- invite flows
- billing flows
- organization/project workflows
- role workflows
- approval flows
- trial/coupon flows
- `NaN`, `Infinity`, `-Infinity`, exponent overflow, or non-finite numeric values
- range/limit guards, ranking, bids, ratings, quotas, pricing, or numeric policy decisions
- JSON/parser disagreement about special floating-point values

Load:

- `02 - Vulnerability Playbooks/Web2/REST API/overview.md`
- `02 - Vulnerability Playbooks/Web2/REST API/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Business Logic/overview.md`
- `02 - Vulnerability Playbooks/Web2/Business Logic/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/REST API/numeric-special-values.md` for non-finite numeric input
- `02 - Vulnerability Playbooks/Web2/Access Control/evidence-requirements.md`

## HTTP Request Smuggling / Desynchronization

Triggers:

- HTTP request smuggling
- HTTP desynchronization / HTTP desync
- CL.TE / TE.CL / TE.TE
- H2.CL / H2.TE
- HTTP/2 downgrade ambiguity
- conflicting Content-Length and Transfer-Encoding
- duplicate or obfuscated framing header
- response queue poisoning
- front-end/back-end request-boundary disagreement
- backend connection poisoning

Load:

- `02 - Vulnerability Playbooks/Web2/HTTP Request Smuggling/overview.md`
- `00 - System/offline-research-cascade.md` when converting a reviewed full paper/RFC into fresh-context, proposal-only hypotheses for owned deterministic evaluation
- Hermes skill `ai-security-research-cascade` for orchestration and HTTP Terminator adoption gates
- `08 - Templates/research-cascade-contract.json.template`
- `02 - Vulnerability Playbooks/Web2/REST API/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Attack Chains/overview.md` when cross-user, cache, auth, routing, or state impact is claimed
- `02 - Vulnerability Playbooks/Web2/Authentication & Session/evidence-requirements.md` when session or account impact is claimed

## Text Protocol Injection / Response Correlation

Triggers:

- Memcached / memcache ASCII protocol
- CRLF or newline injection into an internal protocol
- delimiter-sensitive cache, queue, mail, lookup, or routing client
- attacker-controlled text concatenated into backend commands
- arbitrary cache-entry overwrite or route-cache poisoning
- shared persistent backend connection
- response queue/FIFO mismatch or surplus backend response
- missing request ID, key, type, or length binding
- cross-user response misassociation
- CVE-2022-27924

Load:

- `02 - Vulnerability Playbooks/Web2/Text Protocol Injection/overview.md`
- `02 - Vulnerability Playbooks/Web2/Attack Chains/overview.md` when routing, credential, cross-user, or authentication impact is claimed
- `02 - Vulnerability Playbooks/Web2/Authentication & Session/evidence-requirements.md` when credentials or sessions are involved
- `02 - Vulnerability Playbooks/Web2/HTTP Request Smuggling/overview.md` only when an HTTP framing/connection boundary is also present

## Log Injection / Output Neutralization

Triggers:

- log injection
- log forging
- log poisoning
- CRLF or newline injection into logs
- CWE-117
- improper output neutralization for logs
- untrusted payload persistence in logs
- audit-log corruption
- control characters in log fields
- log collector or parser confusion
- forged event, timestamp, actor, severity, or status
- logs consumed by alerts, automation, templates, commands, or AI agents

Load:

- `02 - Vulnerability Playbooks/Web2/REST API/log-output-neutralization.md`
- `02 - Vulnerability Playbooks/Web2/REST API/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/CI-CD & Supply Chain/agentic-ai-actions.md` when logs enter an AI/agent workflow
- `02 - Vulnerability Playbooks/Web2/Attack Chains/overview.md` when a downstream consumer or security-control bypass is claimed

## Native Parser & Streaming Interfaces

Triggers:

- native parser or compiler front end
- C/C++/Rust parser binding
- stream parser / parse_stream / `stdin`
- file versus string versus stream entry point
- fixed native buffer / unchecked copy / terminator
- soft read limit / `gets(limit)`
- multibyte or encoding-boundary expansion
- post-transformation length mismatch
- parser crash / sanitizer finding / stack buffer overflow
- Ruby Prism / `pm_parse_stream_read` / `parse_stream_fgets`
- ruby/prism PR #4172 / commit `70147e5b449eac2e5c0ef614db6ee89ea9288cb3`
- linter, formatter, IDE/LSP, CI analyzer parsing untrusted source

Load:

- `02 - Vulnerability Playbooks/Web2/Native Parser & Streaming Interfaces/overview.md`
- `02 - Vulnerability Playbooks/Web2/Native Parser & Streaming Interfaces/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Native Parser & Streaming Interfaces/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/Native Parser & Streaming Interfaces/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Attack Chains/overview.md` only when service availability, source-supply-chain, execution, or sandbox impact is separately claimed

## Native Object Deserialization

Triggers:

- Java serialization
- ObjectInputStream
- `AC ED 00 05`
- `rO0`
- ysoserial
- serialVersionUID
- serialized object
- native deserialization
- gadget chain

Load:

- `02 - Vulnerability Playbooks/Web2/Deserialization/overview.md`
- `02 - Vulnerability Playbooks/Web2/REST API/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Attack Chains/overview.md`

## AI / LLM Security

Triggers:

- LLM
- AI assistant
- chatbot
- agent
- prompt injection
- jailbreak
- input/output guardrail
- automated red teaming
- LLM judge
- indirect prompt injection
- RAG
- vector search
- tool calls
- function calling
- model memory
- AI workflow automation
- MCP server/tool
- model context protocol
- vector database
- embedding store
- RAG
- agent memory
- tool manifest/schema
- plugin boundary
- excessive agency
- model/tool token
- PIT-N-06
- PIT-N-11
- PIT-T-42
- PIT-T-43
- PIT-T-46
- PIT-T-47
- PIT-T-53
- PIT-T-64
- PIT-T-65
- PIT-I-19
- PIT-I-27
- tool-definition injection
- MCP tool poisoning
- tool rug pull
- tool-call spoofing
- tool squatting
- retrieval ranking manipulation
- RAG poisoning
- prompt worm
- sleeper prompt
- rules-file backdoor
- AGENTS.md injection
- CLAUDE.md injection
- copilot-instructions
- .cursor/rules
- ANSI prompt injection
- Trojan Source prompt injection
- cross-tenant RAG
- Bedrock API key
- alternate inference plane
- model invocation logging
- cross-site agent forgery / XSAF
- agent builder deep link / initialization URL
- auto-submitted initial prompt
- agent lifecycle integrity
- connector inheritance / pre-authorized connector
- approval policy downgrade / never-ask tool
- Preview Mode tool execution
- agent publish / install / share
- scheduled or autonomous agent
- external agent command channel
- agent disable / delete / token revocation

Load:

- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/overview.md`
- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/reportability.md`
- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/rag-vector-memory.md`
- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/mcp-security.md`
- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/agent-lifecycle-security.md`
- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/prompt-injection-taxonomy.md`
- `00 - System/offline-research-cascade.md` for reviewed source-to-hypothesis research that uses fresh-context workers, strict lineage, deterministic evaluation, and terminal disposition
- Hermes skill `ai-security-research-cascade`
- `08 - Templates/research-cascade-contract.json.template`

## Browser Integration / Web Share / External Handlers

Triggers:

- `navigator.share` / Web Share API
- share sheet or receiving application
- `file:` or custom URL schemes
- webarchive / saved webpage origin assignment
- UXSS / universal cross-site scripting
- Gatekeeper / quarantine / downloaded-file provenance
- shared mutable file or object approved once and changed later
- shortcut, alias, mount, archive, helper app, or Launch Services deputy
- CVE-2021-30861 / CVE-2021-30975
- external protocol/application handlers
- browser-to-OS intent dispatch
- local-file attachment or browser integration boundary

Load:

- `02 - Vulnerability Playbooks/Web2/Browser Integration/overview.md`

## Linux Sandbox / Host IPC / Local Service Deputies

Triggers:

- Flatpak
- PipeWire / PulseAudio
- Unix socket exposed to a sandbox or container
- `$XDG_RUNTIME_DIR` socket mount
- host-visible writable path or shared mount
- desktop portal / D-Bus / local service boundary
- sandbox escape / container escape through a host daemon
- dynamic module, plugin, codec, filter, or library loading by a host process
- local helper or compatibility protocol with greater authority
- CVE-2026-5674

Load:

- `02 - Vulnerability Playbooks/Web2/Linux Sandbox & Host IPC/overview.md`
- `02 - Vulnerability Playbooks/Web2/Attack Chains/overview.md`

## XSS

Triggers:

- reflected parameters
- rich text
- markdown
- file previews
- SVG upload
- HTML rendering
- postMessage
- DOM sinks
- URL fragment/query decoded into a settings object
- object spread/merge into a DOM, jQuery, widget, template, or lightbox factory
- incomplete XSS fix, sibling renderer branch, or property-blocklist variant
- CVE-2022-29455
- user profile fields
- comments/descriptions

Load:

- `02 - Vulnerability Playbooks/Web2/XSS/overview.md`
- `02 - Vulnerability Playbooks/Web2/XSS/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/XSS/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/XSS/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/XSS/reportability.md`

## SSRF / Webhooks

Triggers:

- URL fetchers
- webhooks
- uptime checks
- health checks
- monitor configuration
- import-by-URL
- image fetch
- PDF generation
- callback URLs
- integrations
- reverse-proxy SSRF that forwards incoming browser headers
- broadly scoped `Domain` cookies on sibling hosts
- client-side credential exposure through an attacker-selected upstream
- metadata service risk
- DNS rebinding
- DNS pinning
- URL validation-to-connect TOCTOU
- redirect target revalidation

Load:

- `02 - Vulnerability Playbooks/Web2/SSRF/overview.md`
- `02 - Vulnerability Playbooks/Web2/SSRF/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Webhooks/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/SSRF/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/SSRF/evidence-requirements.md`

## File Upload

Triggers:

- upload endpoint
- file preview
- avatar upload
- document upload
- SVG
- PDF generation
- image processing
- Rails Active Storage
- libvips / ruby-vips
- CVE-2026-66066 / GHSA-xr9x-r78c-5hrm
- image analysis / variant / preview processor
- unfuzzed or untrusted image loader/saver
- ImageMagick delegate behind libvips
- HDF5 / MATLAB v7.3 / MAT
- `matload` / external storage / external reference
- transformed-output file read
- VIPS_BLOCK_UNTRUSTED / Vips.block_untrusted / Vips.block
- object storage
- public file URLs

Load:

- `02 - Vulnerability Playbooks/Web2/File Upload/overview.md`
- `02 - Vulnerability Playbooks/Web2/File Upload/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/File Upload/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/File Upload/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Cloud Storage/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Secret Exposure/evidence-requirements.md` when file-read or process-readable secret impact is claimed
- `00 - System/secret-validation-policy.md` before any identity, token, cloud, database, or service capability validation

## Cloud Storage

Triggers:

- bucket URL
- signed URL
- object key
- CDN asset
- upload policy
- public file
- storage permission
- predictable object path
- S3 ACL
- GCS bucket
- Azure Blob
- public listing
- object overwrite
- READ_ACP
- WRITE_ACP

Load:

- `02 - Vulnerability Playbooks/Web2/Cloud Storage/overview.md`
- `02 - Vulnerability Playbooks/Web2/Cloud Storage/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Cloud Storage/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/Cloud Storage/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Cloud Storage/s3-permission-matrix.md`

## Secret Exposure

Triggers:

- API keys
- Google API keys, Gemini-enabled keys, application restrictions, or API restrictions
- tokens
- `.env`
- GitHub hits
- JS secrets
- Firebase config
- Sentry keys
- Datadog keys
- New Relic keys
- cloud keys
- OAuth client secrets
- GCP IAM public principals
- allUsers / allAuthenticatedUsers
- service account JSON keys
- OIDC-derived credentials
- webhook URLs
- CI variable
- CI log
- build artifact
- container layer
- image history
- deploy key
- service account JSON
- kubeconfig
- Terraform state
- OIDC token
- package registry token
- Bedrock API key
- cloud AI bearer token
- Spring Boot Actuator, `/actuator`, management endpoints, `env`, `configprops`, `heapdump`, or `logfile`

Load:

- `02 - Vulnerability Playbooks/Web2/Secret Exposure/overview.md`
- `02 - Vulnerability Playbooks/Web2/Secret Exposure/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/Secret Exposure/evidence-requirements.md`
- `00 - System/secret-validation-policy.md`

## CI/CD and Supply Chain

Triggers:

- CI/CD
- GitHub Actions
- GitLab CI
- Jenkins
- TeamCity
- build runner
- self-hosted runner
- workflow YAML
- pull_request_target
- poisoned pipeline
- OIDC trust
- cloud role assumption
- artifact signing
- SBOM
- container registry
- Docker image layer
- package registry
- dependency confusion
- typosquatting
- mutable image tag
- deployment pipeline
- AI coding action
- agentic action
- Claude Code Action
- OpenAI Codex action
- Gemini CLI action
- GitHub AI Inference
- issue_comment workflow
- prompt-file
- prompt in workflow
- wildcard allowlist
- allow-users: "*"
- allowed_non_write_users: "*"
- danger-full-access
- safety-strategy unsafe
- --yolo
- Bash(*)

Load:

- `02 - Vulnerability Playbooks/Web2/CI-CD & Supply Chain/overview.md`
- `02 - Vulnerability Playbooks/Web2/CI-CD & Supply Chain/artifact-dependency-provenance.md`
- `02 - Vulnerability Playbooks/Web2/CI-CD & Supply Chain/agentic-ai-actions.md`
- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/overview.md`
- `02 - Vulnerability Playbooks/Web2/Secret Exposure/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Cloud Storage/s3-permission-matrix.md`

## Mobile API

Triggers:

- mobile app
- APK/IPA
- mobile-only endpoint
- deep link
- app secrets
- certificate pinning
- device headers
- mobile OAuth
- APK
- IPA
- split APK
- AndroidManifest.xml
- exported activity
- exported receiver
- exported provider
- deep link
- app link
- universal link
- URL scheme
- WebView
- Keychain
- ATS exception
- network security config
- Firebase config
- mobile local storage

Load:

- `02 - Vulnerability Playbooks/Web2/Mobile API/overview.md`
- `02 - Vulnerability Playbooks/Web2/Mobile API/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Mobile API/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/Mobile API/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Mobile API/reportability.md`
- `02 - Vulnerability Playbooks/Web2/Mobile API/android-static-recon.md`
- `02 - Vulnerability Playbooks/Web2/Mobile API/ios-platform-testing.md`

## Rate Limits & Abuse

Triggers:

- password reset
- OTP
- invite
- email send
- SMS send
- coupon/trial abuse
- enumeration
- automation risk

Load:

- `02 - Vulnerability Playbooks/Web2/Rate Limits & Abuse/overview.md`
- `02 - Vulnerability Playbooks/Web2/Rate Limits & Abuse/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Rate Limits & Abuse/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/Rate Limits & Abuse/evidence-requirements.md`

## Race Conditions / TOCTOU

Triggers:

- race condition
- TOCTOU
- concurrent requests
- double submit
- one-time token
- coupon redemption
- quota/limit bypass
- balance update
- check/use window
- async processing
- idempotency

Load:

- `02 - Vulnerability Playbooks/Web2/Race Conditions/overview.md`
- `02 - Vulnerability Playbooks/Web2/Race Conditions/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Race Conditions/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Race Conditions/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/Business Logic/test-checklist.md`

## WordPress CVE Intelligence

Triggers:

- WordPress
- wp-content/plugins
- WordPress plugin
- plugin CVE
- Patchstack
- Wordfence
- WPScan
- wordpress.org plugin slug
- Nuclei WordPress template
- WordPress REST route
- admin-ajax.php action
- shortcode vulnerability
- vulnerable plugin version
- WordPress Core security release
- WP2Shell
- CVE-2022-29455 / Elementor `<=3.5.5`
- incomplete plugin XSS fix or sibling renderer/type branch
- WordPress SVN vulnerable/fixed tag diff
- CVE-2026-63030
- CVE-2026-60137
- REST batch-route confusion
- `author__not_in`
- nested REST dispatch

Load:

- `02 - Vulnerability Playbooks/Web2/WordPress CVE Intelligence/overview.md`
- relevant primitive playbook from this index, such as XSS, SSRF, File Upload, Access Control, Authentication & Session, REST API, Secret Exposure, or Attack Chains

## Attack Chains / Severity Escalation

Triggers:

- low severity primitive with possible follow-on impact
- open redirect on OAuth/SSO client
- XSS on authenticated or admin-viewed pages
- SSRF with metadata/internal-service possibility
- upload leading to parser/preview/storage impact
- IDOR on account, role, billing, export, or workflow state
- chained impact hypothesis

Load:

- `02 - Vulnerability Playbooks/Web2/Attack Chains/overview.md`
- `08 - Templates/reporting-evidence-template.md`
- relevant primitive playbook from this index

## Controlled Payload Corpus / Methodology Reference

Triggers:

- PayloadsAllTheThings
- payload corpus
- payload selection
- bypass payload
- polyglot payload
- XSS payload
- SSRF payload
- XXE payload
- SQL injection payload
- NoSQL injection payload
- GraphQL injection payload
- file upload payload
- path traversal payload
- JWT payload
- OAuth misconfiguration payload
- open redirect payload
- CORS misconfiguration payload
- clickjacking payload
- CRLF payload
- cache deception payload

Load:

- `10 - Tools/Web2/controlled-payload-corpus.md`
- `00 - System/external-payloadsallthethings-controlled-review-2026-07-07.md`
- relevant primitive playbook from this index

## Tooling / Burp Workflow

Triggers:

- authorization replay
- hidden parameter discovery
- GraphQL schema mapping
- passive SSRF callback discovery
- high-speed race/fuzz approval
- Burp/Caido workflow setup
- framework-specific wordlist
- Flask route corpus
- `app.route`
- blueprint route
- source-derived endpoint corpus

Load:

- `10 - Tools/Burp Suite Extension Tooling.md`
- `10 - Tools/Web2/framework-derived-route-corpus.md`
