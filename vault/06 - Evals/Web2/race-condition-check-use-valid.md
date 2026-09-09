# Eval: Valid Web2 race condition / check-use window

Valid when:

- target is in scope;
- attacker uses owned account/object/resource;
- serial baseline shows intended invariant;
- concurrent sequence violates the invariant;
- durable state or authorization/business impact changes;
- request/response/timing evidence and before/after state are preserved.

Reject when:

- only transient 500s or duplicate responses occur;
- impact is DoS/noise only;
- test requires high-volume stress;
- operation is privileged/admin-only;
- financial/notification/destructive side effects were triggered without approval.

## HTTP response queue poisoning variant — 2026-07-01

Also valid when a race/check-use window in an HTTP client, proxy, pool, or agent lets one logical request consume a response intended for another request.

Required extra proof:

- attacker can influence timing, socket reuse, upstream response, or queued request state;
- evidence maps each sent request to the response it incorrectly consumed;
- security impact crosses an auth, tenant, cache, or trust boundary.
