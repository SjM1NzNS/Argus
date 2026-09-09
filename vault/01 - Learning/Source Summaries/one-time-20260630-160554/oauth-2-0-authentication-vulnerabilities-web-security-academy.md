---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.072677+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: Authentication / Session
---

# OAuth 2.0 authentication vulnerabilities | Web Security Academy

- URL: `https://portswigger.net/web-security/oauth`
- Source group: `backfill_deep_content`
- Content chars: `28064`
- Classification: **Web2 skill update**
- Vulnerability class: **Authentication / Session**

## Source summary

- OAuth grant types OAuth scopes Authorization code grant type Implicit grant type OAuth authentication Identifying Recon of the OAuth service How vulnerabilities arise Exploiting vulnerabilities Improper implementation of the implicit grant type Flawed CSRF protection Leaking authorization codes and access tokens Flawed scope validation Unverified user registration OpenID Connect How does OpenID Connect work?
- Crucially, OAuth allows the user to grant this access without exposing their login credentials to the requesting application.
- Roles Claims and scopes ID token Identifying OpenID Connect Vulnerabilities Unprotected dynamic client registration Allowing authorization requests by reference Preventing vulnerabilities Service providers Client applications View all OAuth authentication labs Web Security Academy OAuth authentication OAuth 2.0 authentication vulnerabilities While browsing the web, you've almost certainly come across sites that let you log in using your social media account.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
