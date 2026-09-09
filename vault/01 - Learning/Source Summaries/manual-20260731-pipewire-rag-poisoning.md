---
type: learning-source-summary
status: promoted-selectively
created: "2026-07-31"
source_run: "manual-articles-20260731"
trust_zone: 0
mapped_playbooks:
  - "Web2/Linux Sandbox & Host IPC"
  - "Web2/AI & LLM Security/RAG, Vector, Memory, and Embedding Security"
  - "Web2/Attack Chains"
---

# PipeWire sandbox escape and RAG poisoning — promoted lessons

## Sources reviewed

1. Johann Rehberger, [Escaping Linux Sandboxes via PipeWire (CVE-2026-5674)](https://embracethered.com/blog/posts/2026/pipewire-flatpak-linux-sandbox-escape-cve-2026-5674/), 2026-07-30.
2. Eleanor Barlow / Intigriti, [RAG and ruin: why your existing controls may miss AI poisoning attacks](https://www.intigriti.com/blog/business-insights/why-your-existing-controls-may-miss-ai-poisoning-attacks), 2026-07-28.

Both pages were fetched directly and classified as source-native `actual_content`. Clean reviewed captures are preserved under `01 - Learning/Inbox/manual-articles-20260731/` while promotion is validated. The PipeWire extracted article hash is `4609f03961477cd5a2278aacbd0a0ce4e7f7fb3bbe1de28c8c9a2d87dc9145e3`. The Intigriti downloadable PDF hash is `9398b1ad47ae8c21dfdc68d031d8ca74e989e2811116d419167b048429f55237` and its extracted text hash is `d2e60878752c7ed011151c27d17ffa1227adaa700a59bf58728a1f60a65fd503`.

These are Zone 0 learning sources. They do not establish any current target's version, scope, exploitability, authorization, or reportability.

## 1. CVE-2026-5674 — host service as a sandbox deputy

### Primary-source assessment

The author describes a Flatpak client reaching a host PipeWire/PulseAudio compatibility socket, being accepted by the protocol layer, requesting module loading, and causing the host-user PipeWire process to load attacker-controlled library content from a host-visible writable path.

Primary sources corroborate the core security result:

- [CVE-2026-5674](https://www.cve.org/CVERecord?id=CVE-2026-5674) classifies the flaw as CWE-427, assigns CVSS 8.8 (`AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H`), and describes arbitrary code execution outside a sandbox.
- [Red Hat's CVE record](https://access.redhat.com/security/cve/CVE-2026-5674) calls the issue Important and identifies PipeWire's PulseAudio compatibility layer and malicious library loading as the affected boundary.
- The upstream [PipeWire fix](https://gitlab.freedesktop.org/pipewire/pipewire/-/commit/8fd798208777f502a3bd86b02b07a24397792f3f) removes direct absolute-path loading and constrains LADSPA/JACK/module/plugin loading to defined search paths while stripping parent traversal.
- [Flatpak's sandbox-permissions documentation](https://docs.flatpak.org/en/latest/sandbox-permissions.html) confirms that host-service access is absent by default and is selectively added as an application permission.

The direct source and primary records support **user-context sandbox escape**, not root privilege escalation. `S:C` reflects crossing the sandbox boundary; the host service still runs as the desktop user.

### Promoted invariant

A functional host IPC permission must not implicitly grant the confined client the host daemon's extension-loader or code-loading authority.

Reusable chain:

```text
confined attacker-controlled process
  -> reachable host IPC socket
  -> protocol/authentication acceptance
  -> dangerous host operation enabled
  -> host-visible attacker-writable artifact/path
  -> host daemon loads or interprets it
  -> execution as host daemon/user outside the sandbox
```

Every edge is required. The durable lesson is the composition of individually plausible permissions, not the audio protocol alone.

### Applicability and evidence gates

Retain a candidate only when all relevant deployment gates are proven:

1. The sandbox can reach the actual host daemon socket or mediated equivalent.
2. The deployed protocol accepts the client and exposes the dangerous operation.
3. Module/extension loading is enabled and reachable for that client.
4. The attacker can place content at a path or object identity that the host daemon resolves to the same bytes. “Writable inside the sandbox” is insufficient; the path must be **host-visible**.
5. The host process, not a same-sandbox helper, loads or interprets the artifact.
6. The deployed package/configuration is affected; a vulnerable-version banner alone is not enough.
7. A harmless owned marker proves changed execution context; root, credential, or persistence claims remain separate.

A Flatpak audio permission plus an arbitrary sandbox-private writable directory does not satisfy the chain. Container claims likewise require the real socket mount and path/volume visibility under the deployed namespace/mount model.

### Mitigation hierarchy

Break the earliest feasible edge:

- remove host socket exposure when the feature does not need it;
- mediate capability-specific operations through a portal instead of exposing a broad compatibility protocol;
- validate peer identity/authentication and authorize operations, not merely connection length/shape;
- default dynamic module loading off for untrusted clients;
- canonicalize and confine every loader path to trusted directories, rejecting absolute and traversal forms;
- prevent shared writable mounts/paths from becoming loader inputs;
- update affected PipeWire packages and verify effective configuration after restart.

### Held or rejected

- The article's “any host-writable path” phrasing is narrowed to a path whose bytes and pathname are actually visible to the host loader.
- Generic “Docker is exploitable” claims are held unless socket, mount, protocol, version, and host-process edges are demonstrated.
- The broken cookie check and default module-loading behavior are retained as contributing observations from the article, but the official CVE classification and shipped patch center the uncontrolled loader search/path boundary.
- No exploit payload, malicious shared object, credential access, persistence, or live target action was reproduced.
- Preview.is run `manual-preview-is-20260731-013444` returned only two unrelated, low-score results (`0.1263`–`0.1354`); no RAG-derived PipeWire claim was promoted.

## 2. RAG poisoning — staged corpus-to-impact proof

### Source and corroboration assessment

The Intigriti article correctly frames RAG as an expanded trust boundary: external mutable content becomes retrieved model context. It also distinguishes the likely consequences of simple QA systems (misinformation/unsafe recommendations) from agentic systems with tools or permissions (data access or unauthorized action).

Primary and high-confidence corroboration:

- [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/) identifies poisoning from insiders, prompts, data seeding, or unverified providers and recommends permission-aware stores, source authentication, validation, classification, and immutable retrieval logs.
- [MITRE ATLAS AML.T0070](https://atlas.mitre.org/techniques/AML.T0070) defines RAG poisoning as malicious content placed where a RAG system indexes it so that it contaminates later RAG results.
- [PoisonedRAG, USENIX Security 2025](https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag) reports a 90% attack success rate after injecting five malicious texts per target question into a million-text database **under its defined experimental setup**.
- Preview.is run `manual-preview-is-20260731-013450` returned five relevant results at `0.9819`–`0.9959`, including [HiddenLayer's RAG injection discussion](https://www.hiddenlayer.com/research/prompt-injection-attacks-on-llms) and the [OWASP Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html). These corroborate the attack class only; direct primary sources control promoted claims.

### Promoted distinctions

Do not collapse four different classes:

| Class | What changes | Minimum proof |
|---|---|---|
| Training/fine-tuning poisoning | model parameters or training behavior | influence over the training/fine-tune supply chain plus changed model behavior |
| RAG poisoning | indexed corpus/retrieval result | attacker-controlled source is ingested, selected, and shown to the model |
| Indirect prompt injection | model treats retrieved data as instruction | model-visible injected text changes behavior relative to a benign equivalent |
| Memory poisoning | harmful state persists into later context | a later session/user/run recalls the state and changes behavior |

These may chain, but none proves the others automatically. Poisoned misinformation can manipulate answers without being an instruction; indirect injection can occur without durable corpus poisoning; memory persistence is a later edge.

### Six-stage proof model

```text
attacker-writable source
  -> ingestion eligibility and successful indexing
  -> retrieval/reranking into top-k context
  -> model interpretation or answer steering
  -> downstream data/tool/memory authority
  -> concrete victim or security impact
```

Capture each edge independently:

1. **Source control:** who can write/publish the document, field, metadata, page, email, ticket, or message?
2. **Ingestion:** exact crawler/connector, index revision/time, parser/chunker result, source provenance, ACL/tenant labels.
3. **Retrieval:** query, chunk/document ID, score/rank/top-k/reranker trace, and benign equivalent/unrelated-query controls.
4. **Interpretation:** exact model-visible context and output delta; distinguish quotation/discussion from instruction following.
5. **Authority:** available tools, permissions, memory writes, connected data, confirmations, and server-side authorization.
6. **Impact:** another user/tenant, unauthorized data/action, durable persistence, or a program-accepted safety consequence.

### Control and detection lessons

Traditional WAF/network controls may not inspect delayed, source-to-index-to-model semantics, but “WAF miss” is not itself a vulnerability. Evaluate controls at the stage they can enforce:

- source allowlisting, signatures/authentication, provenance, and ownership;
- parser normalization and hidden-content detection;
- document/chunk ACL propagation and tenant partitioning;
- ingestion review/quarantine and content-addressed version history;
- retrieval score/rank anomaly detection and source diversity;
- clear instruction-versus-data boundaries and prompt/context isolation;
- least-privilege tools, server-side authZ, confirmation, recipient/egress policy;
- immutable logs joining source version, chunk, query, retrieval rank, model/run, tool call, and resulting state;
- deletion/revocation tests that prove poisoned chunks and memory are no longer retrievable.

### False-positive and overclaim gates

Reject or hold when:

- public attacker content is writable but there is no proof the target indexes it;
- content is indexed but never retrieved for a realistic query;
- retrieved content is only quoted/summarized and causes no boundary effect;
- the attacker controls both source and querying user and no victim/shared-system boundary is crossed;
- a WAF or scanner misses natural language but another ingestion/retrieval control blocks it;
- a one-off model response is called durable poisoning without index/memory persistence;
- the PoisonedRAG five-text/90% result is generalized beyond its models, retrievers, corpus, target questions, or trial setup;
- misinformation or undesirable output has no target-specific security or accepted safety impact.

## Vault promotion

Promoted into:

- `02 - Vulnerability Playbooks/Web2/Linux Sandbox & Host IPC/overview.md`
- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/rag-vector-memory.md`
- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/Attack Chains/overview.md`
- `00 - System/web2-skill-index.md`
- two focused eval-scenario files under `06 - Evals/Web2/`

`Embrace The Red Blog` is already registered in the learning-source manifest. The broader Intigriti business-insights lane was not added as a recurring source because it is mixed marketing/business content; the supplied article remains a manually reviewed source.