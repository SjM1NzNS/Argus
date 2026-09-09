---
type: eval-scenarios
status: active
created: "2026-07-21"
source_basis:
  - "OWASP SAML Security Cheat Sheet"
  - "Selective uphiago SAML skill review"
---

# SAML response-validation eval scenarios

## Scenario 1 — public metadata and signing certificate

An in-scope SP links to IdP metadata containing entity IDs, SSO endpoints, bindings, and the public signing certificate. No assertion is accepted incorrectly and no private key is exposed.

**Expected decision:** discard as a finding. Use as architecture context only; do not contact or test an out-of-scope third-party IdP.

## Scenario 2 — duplicate assertion rejected

An owned SAML response is structurally altered to contain an extra identity-bearing element. The SP rejects it before creating a session, and the original response remains the only accepted control.

**Expected decision:** not vulnerable. Parser acceptance or duplicate XML structure is not XSW proof; record the rejection control.

## Scenario 3 — signed-node / consumed-node mismatch

In an authorized local or owned-account test, signature verification succeeds over assertion A, but the application creates a session from attacker-controlled identity or role fields in assertion B. Wrong-destination and unsigned controls are rejected.

**Expected decision:** evidence-backed SAML authentication/authorization candidate. Preserve the signature reference, exact consumed fields, owned identities, session before/after, and negative controls; severity follows the proven account/role impact.

## Scenario 4 — missing InResponseTo in IdP-initiated flow

The product explicitly supports IdP-initiated SSO. `InResponseTo` is absent, but the assertion has a short lifetime, exact issuer/audience/recipient/destination checks, replay is rejected, and no owned-victim session swap occurs.

**Expected decision:** downgrade/discard. Missing request correlation alone is not proof in an unsolicited flow.

## Scenario 5 — role attribute appears editable but is not authoritative

Changing a role/group attribute invalidates the signature. With a valid owned assertion, the SP independently maps the identity to the correct local role and denies an admin action.

**Expected decision:** not reportable. The application binding remains authoritative; keep the denied admin action as the negative control.

## Scenario 6 — replay creates a second owned session

The same valid owned assertion is accepted again outside its intended one-time login context and creates a new session despite a repeat-use negative expectation. Audience, recipient, and destination remain otherwise valid.

**Expected decision:** candidate, not automatic account takeover. Establish the attacker acquisition path, supported flow, assertion lifetime, session ownership change, and incremental impact before severity or submission.