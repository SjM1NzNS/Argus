# Validating same-origin proxy cookie-boundary leaks

Use this workflow when a trusted web origin reverse-proxies browser requests to user-deployed code, plugins, tenant services, notebooks, jobs, previews, extensions, or another lower-trust upstream. The core risk is not a missing cookie flag: it is a server-side trust-boundary failure where browser session authority survives routing into attacker-influenced code.

## Threat model

Trace the complete path:

```text
browser session cookie
  -> trusted same-origin frontend
  -> frontend middleware / reverse proxy
  -> authentication gateway
  -> tenant- or user-controlled backend
  -> attacker observation
  -> owned-token replay / victim-authority action
```

Record these actors separately:

1. **Service author:** who can deploy or control the lower-trust backend.
2. **Victim caller:** who can invoke that backend and what greater authority their session carries.
3. **Deployment operator:** who selects native login, proxy/IAP/SSO mode, cookie settings, and credential propagation.
4. **Token consumer:** which component accepts replay and whether the token is audience-, client-, device-, or channel-bound.

A developer controlling a backend is not enough if the victim cannot invoke it. A victim reaching the frontend is not enough if the hosted deployment never issues the candidate cookie.

## Source-first header trace

Inspect every hop rather than assuming generic proxy behavior:

1. **Cookie issuance:** name, `Path`, host/domain scope, `Secure`, `HttpOnly`, `SameSite`, expiry, and auth mode.
2. **Browser delivery:** exact same-origin path and whether the browser emits the cookie there.
3. **Frontend mutation:** whether middleware converts the cookie to `Authorization` or another identity header while leaving the original `Cookie` intact.
4. **Proxy version/config:** whether the pinned proxy library copies, rewrites, or strips request headers by default and whether request decorators override that behavior.
5. **Gateway authentication:** which security header is consumed/removed and which raw headers remain.
6. **Backend transport:** any later header allowlist, sanitization, RPC conversion, or runtime wrapper before user code.
7. **User-code observation:** prove the lower-trust backend receives the canary header/value; source absence of a strip is only a candidate.
8. **Replay:** prove the canary grants a distinct victim-only server authorization result, not merely parser acceptance.

Do not describe a component as forwarding a cookie merely because it lacks an obvious strip call. Execute the pinned proxy/gateway path or preserve a deterministic unit/integration test.

## Delivery-path distinction

Separate the root leak from navigation helpers:

- A direct same-origin navigation or subresource request to a proxied user-service path may be sufficient.
- A post-login `redirectUrl` can make delivery realistic, but is usually an auxiliary link rather than the root cause.
- A scheme-relative or external open redirect does not itself leak a host-only `SameSite=Strict` cookie to another site.
- If the candidate works only after the victim deliberately authenticates through an attacker-supplied link, record that user interaction and avoid implying a zero-click attack.

## Why cookie flags may not help

- `HttpOnly` blocks JavaScript reads; it does not stop the browser from attaching the cookie to HTTP requests or a trusted server from forwarding it.
- `SameSite=Strict` controls cross-site delivery; it does not isolate paths or mutually distrusting applications on the same origin.
- `Secure` constrains transport scheme; it does not constrain the receiving upstream behind a trusted HTTPS frontend.
- `Path` is routing scope, not an authorization boundary.

The report should therefore focus on **credential propagation across a server-side trust boundary**, not “missing cookie flags.”

## Safe modular validation

Use only owned canaries and loopback/local services unless a reviewed scope contract permits more.

### A. Frontend proxy canary

- Run the pinned frontend/proxy implementation.
- Send a request with a unique fake cookie to a loopback upstream.
- Record the exact received headers with values redacted to name, digest, and length.
- Add a no-cookie request and an explicit strip configuration as controls.

### B. Gateway canary

- Pass the request through the real authentication handler with a fake valid token fixture.
- Assert which auth header is removed and whether `Cookie` remains.
- Test wrong/absent tokens to ensure the backend is not reached through an unrelated auth bypass.

### C. User-service canary

- Use the real user-service routing/runtime wrapper where feasible.
- Prove the lower-trust handler receives the canary.
- Confirm the victim has the exact execute/invoke permission needed to reach it; otherwise the chain is blocked.

### D. Owned replay control

- Replay only an owned short-lived canary token to a harmless identity endpoint or victim-only read.
- Compare no-token, wrong-token, expired/revoked-token, and original-browser controls.
- Stop at the minimum proof of session/authority reuse; do not preserve plaintext tokens or test real users.

## Product-applicability gate

Open-source source validity and hosted-product applicability are separate verdicts. Confirm:

- the vulnerable frontend/repository is independently in program scope;
- the named hosted product actually deploys the affected proxy path/version;
- the hosted auth mode issues the same cookie rather than using IAP, proxy identity headers, or another SSO boundary;
- outbound/inbound routing reaches user-controlled code;
- default or supported ACLs let a higher-authority victim invoke attacker-controlled code;
- token replay maps to the claimed product account, not a broader identity-provider account unless separately proven.

Do not let an unverified hosted deployment erase explicit OSS eligibility, and do not turn OSS behavior into a hosted-product claim without evidence.

## Severity and wording

Use progressive language:

- **Cookie-forwarding candidate:** source suggests the raw cookie can cross the boundary.
- **Session-token disclosure:** lower-trust code demonstrably receives an owned live token.
- **Session hijacking:** replay yields a victim-only authorization result.
- **Account takeover:** replay grants broad victim account control or a durable takeover action; prove this separately.

Never label a source trace or proxy-only loopback test as ATO. Distinguish product-session takeover from takeover of an upstream Google, GitHub, SSO, or cloud account.

## False-positive and downgrade gates

Downgrade or block when:

- the hosted mode never issues the cookie;
- the backend is not attacker-influenced;
- the victim cannot invoke the backend;
- a later proxy/runtime strips `Cookie` before user code;
- the value is non-authoritative, bound to the original channel/client, or not replayable;
- the attacker already has equivalent victim authority;
- only an external open redirect or generic cookie-flag observation is proven;
- the claimed reproduction has no archived harness/log or ran zero tests.

## Remediation

- Strip browser `Cookie`, `Authorization`, and other frontend credentials before routing to lower-trust upstreams.
- Forward a purpose-built, least-privilege identity/capability with explicit audience and short lifetime when user identity is required.
- Use a strict outbound header allowlist at every trust boundary, not a one-header denylist.
- Separate mutually distrusting user services onto origins/hosts that do not receive frontend session cookies.
- Constrain post-login redirects to an allowlist of UI routes where practical; treat this as defense in depth, not the primary fix.

## Evidence package

Preserve:

- exact source anchors and pinned versions for cookie issuance, proxy routing, gateway sanitization, and user-service routing;
- browser request headers with secret values redacted;
- loopback proxy/gateway/user-service positive and negative controls;
- exact victim invoke permission and attacker deployment permission;
- owned replay authorization result and token invalidation behavior;
- separate OSS-scope and hosted-product applicability verdicts;
- a public duplicate search by proxy class, cookie name, auth handler, and user-service route.
