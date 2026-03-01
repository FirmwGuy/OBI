# OBI HTTP Client Profile
## OBI Profile: `obi.profile:net.http_client-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:net.http_client-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Purpose

This profile standardizes a minimal HTTP client surface suitable for multiple implementations:

- libcurl (easy or multi)
- libsoup (GLib main loop)

The profile supports:

- synchronous request/response as the baseline
- optional async requests, either via provider threads or via the Core Pump profile

---

## 2. Technical Details

### 2.1 Request model

Requests include:

- `method` (defaults to GET)
- `url` (required)
- optional header key/value pairs
- optional request body:
  - no body
  - bytes
  - reader stream (upload)

The baseline ABI (`obi_http_request_v0`) is intentionally small.

For common network knobs (timeouts, redirects, TLS verification), providers may expose the extended
request entrypoints (`request_ex` / `request_async_ex`) and the extended request struct
`obi_http_request_ex_v0`.

### 2.2 Response model

Responses include:

- integer status code
- response headers (provider-owned views)
- response body reader (provider-owned)
- a `release` callback that frees provider-owned response resources

The host MUST call `resp.release(...)` exactly once when done with the response. After release,
embedded header views and the body reader are invalid.

### 2.3 Streaming rules

- For synchronous requests, a request-body reader is allowed; the provider consumes it during the
  call and MUST NOT retain it after returning.
- For async requests, providers MAY refuse BODY_READER uploads unless they advertise
  `OBI_HTTP_CAP_ASYNC_BODY_READER`.
- Response bodies are exposed as a reader to support streaming downloads without buffering.

### 2.4 Async model and pumps

If `request_async` (or `request_async_ex`) is supported, the provider returns an HTTP job:

- `poll(timeout_ns, out_done)` checks progress
- once done, `take_response` transfers a response into an output struct
- `cancel` requests cancellation
- `destroy` frees the job

Providers may implement async in two styles:

1) **Threaded async:** the provider makes progress internally (threads). `poll` observes completion.
2) **Pump-driven async:** progress occurs only when the host drives a pump (curl multi, GLib).

Pump-driven async should advertise `OBI_HTTP_CAP_REQUIRES_PUMP` and also expose the pump profile
(`obi.profile:core.pump-0`) from the same provider instance.

### 2.5 TLS and redirects (extended requests)

Extended requests allow the host to request common behavior:

- timeout (`timeout_ns`)
- follow redirects and cap redirect depth
- enable/disable TLS verification

Providers MUST document defaults and how they map these knobs onto the underlying library.

---

## 3. Conformance

Required:

- synchronous request (`request`)

Optional (advertised via caps):

- async requests (`request_async` and the job interface)
- extended requests (`request_ex`, `request_async_ex`)
- async streaming uploads (BODY_READER with async)

---

## 4. Determinism Notes (CEP integration)

HTTP is inherently nondeterministic. When used under a deterministic host (CEP), the host must
record request intents and response outcomes and define replay behavior (simulate vs re-apply).
This profile must make it possible to capture the request/response bytes and metadata.

---

## 5. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_net_http_client_v0.h`

---

## Global Q&A

**Q: Why not standardize every HTTP feature (cookies, proxy auth, HTTP/3, etc.)?**  
OBI profiles are meant to be minimal and stable. This profile aims to cover the common core needed
by CEP/PRAXIS-style systems. More specialized features can be added via capability bits and
extended entrypoints, or via separate profiles when needed.

**Q: Where do idempotency and replay policies live?**  
In the host (for example CEP) and its effect logging/replay policies. This profile provides a
runtime mechanism, not the governance semantics.
