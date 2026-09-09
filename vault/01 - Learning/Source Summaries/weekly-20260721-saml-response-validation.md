---
type: source-summary
status: promoted
created: "2026-07-21"
domain: web2
topics: [saml, sso, authentication, authorization, xml-signature]
---

# Weekly promotion — SAML response validation and application binding

## Sources reviewed

- [OWASP SAML Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html), retrieved from the official CheatSheetSeries repository.
- [uphiago/recon-skills — SAML SSO Attack Skill](https://github.com/uphiago/recon-skills/blob/main/auth/saml-sso-attack/SKILL.md), selected from the configured external skill source rather than bulk-importing the repository.
- Preview.is was queried twice for SAML validation/reportability material. The wrapper timed out and the direct API retry returned HTTP 504, so no RAG text or URL was promoted.

Raw reviewed files were held temporarily under `01 - Learning/Inbox/weekly-20260721-saml-review/` and removed after promotion verification.

## Promoted methodology

1. Treat SAML security as four linked validation layers: parser/schema, signature/trust, protocol binding, and application identity/role binding.
2. Require the XML node covered by the valid signature to be the same node whose identity and authorization fields the SP consumes. Assertion-level signing is not itself proof of XML Signature Wrapping.
3. Build a response-consumption matrix for issuer, destination/ACS, recipient, audience, `InResponseTo`, subject confirmation, validity window, replay behavior, NameID, attributes, and resulting account/tenant/role.
4. Distinguish SP-initiated request correlation from supported unsolicited IdP-initiated SSO. Missing `InResponseTo` alone is not enough; require replay or login/session impact with owned accounts.
5. Treat public metadata, certificates, endpoints, decode success, and product fingerprints as discovery context, not findings.
6. Require owned-account before/after proof for identity substitution, session swapping, replay, role/tenant confusion, or authorization impact.

## Rejected or quarantined material

- No broad endpoint probing, user timing enumeration, credential testing, third-party IdP contact, or insecure TLS (`curl -k`) was adopted.
- No exploit payload or forged assertion recipe was imported.
- The external skill's suggestion that assertion-level signing makes XSW possible was narrowed: reportability requires a demonstrated signed-node/consumed-node mismatch and resulting session or authorization impact.
- Its fixed `>200ms` timing threshold was rejected; timing claims need controlled distributions and a lawful in-scope identity-disclosure model.

## Hunt relevance

- **Google:** useful for OSS or product SAML consumers and enterprise admin surfaces; begin with source-level response-consumption tracing and trust-anchor/config review, not live IdP interaction.
- **authorized program:** useful for corporate-SSO-gated portals only after entitlement and scope checks; public ADFS/SAML metadata does not justify testing the IdP or enumerating employees.

## Files promoted

- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/overview.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/OAuth & SSO/evidence-requirements.md`
- `06 - Evals/Web2/saml-response-validation-weekly-20260721.md`
- `00 - System/web2-skill-index.md`
- `07 - Skill Changelog/2026-07.md`