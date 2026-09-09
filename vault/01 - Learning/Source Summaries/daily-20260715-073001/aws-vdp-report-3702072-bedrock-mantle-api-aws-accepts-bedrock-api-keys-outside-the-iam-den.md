---
type: learning-source-summary
compiled_at: 2026-07-15T05:32:08.230861+00:00
source_quality: 6
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# AWS VDP | Report #3702072 - bedrock-mantle.api.aws accepts Bedrock API keys outside the IAM Deny, CloudTrail signal, and invocation logging AWS publishes for Bedrock keys | HackerOne

- URL: `https://hackerone.com/reports/3702072`
- Source group: `browser_dom_linked_resources`
- Content chars: `28927`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Three customer-deployable defensive controls fail to apply to this plane: (1) the AWS-published SCP/IAM Deny: bedrock:CallWithBearerToken does not match mantle's IAM action prefix, (2) the AWS-published CloudTrail filter additionalEventData.callWithBearerToken = true does not match mantle events (the field is at a different JSON path), (3) put-model-invocation-logging-configuration does not capture mantle prompts and there is no equivalent customer-facing API for mantle today, i.e. customers cannot enable mantle prompt/response logging even if they want to.
- C aws bedrock put-model-invocation-logging-configuration for prompt/response capture Bypassed.
- Mantle inference does not appear in the configured BedrockModelInvocationLogs S3 prefix.

## Extracted methodology

- Affected surface: cloud AI bearer credentials accepted across parallel service/action namespaces.
- Root cause class: customer guidance and controls covered the documented Bedrock plane but not `bedrock-mantle`; the explicit deny used another action prefix, the published CloudTrail detection read another JSON path, and standard invocation logging did not capture alternate-plane prompts/responses.
- Minimal method: in an owned account, compare no-key/wrong-key/valid-key/explicit-deny behavior on the same harmless inference request across both planes, then compare CloudTrail event source/name/field paths and unique canary prompt delivery.
- Evidence requirements: redacted credential class, issuance/managed-policy path, exact IAM actions, billable capability, deny matrix, audit-event schema, invocation-log positive/negative controls, and vendor guidance establishing expected coverage.
- False-positive gates: do not call this total invisibility when alternate-plane CloudTrail events exist; detection-query drift, deny bypass, and missing prompt/response logs are separate impacts. Documentation mismatch without reproduced capability/control failure is weaker.

## Compiler decision

- Promoted on 2026-07-15 into AI/LLM cloud service-plane testing, evidence, downgrade/reportability gates, routing, and eval coverage.
