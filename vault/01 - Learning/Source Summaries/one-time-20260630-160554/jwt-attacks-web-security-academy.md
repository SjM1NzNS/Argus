---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.070891+00:00
source_quality: 9
classification: severity rule
vulnerability_class: Authentication / Session
---

# JWT attacks | Web Security Academy

- URL: `https://portswigger.net/web-security/jwt`
- Source group: `backfill_deep_content`
- Content chars: `21323`
- Classification: **severity rule**
- Vulnerability class: **Authentication / Session**

## Source summary

- Impact of JWT attacks How vulnerabilities arise Working with JWTs in Burp Suite Exploiting flawed JWT signature verification Accepting arbitrary signatures Accepting tokens with no signature Brute-forcing secret keys Using hashcat JWT header parameter injections jwk parameter jku parameter kid parameter Other parameters Algorithm confusion attacks Symmetric vs asymmetric algorithms How algorithm confusion vulnerabilities arise Performing an attack Obtain the server's public key Convert the public key to a suitable format Modify your JWT Sign the JWT with the public key Deriving public keys from existing tokens Preventing attacks View all JWT labs Web Security Academy JWT attacks JWT attacks In this section, we'll look at how design issues and flawed handling of JSON web tokens (JWTs) can leave websites vulnerable to a variety of high-severity attacks.
- Unlike with classic session tokens, all of the data that a server needs is stored client-side within the JWT itself.
- As JWTs are most commonly used in authentication, session management, and access control mechanisms, these vulnerabilities can potentially compromise the entire website and its users.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
