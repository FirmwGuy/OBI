# OBI Net DNS Profile
## OBI Profile: `obi.profile:net.dns-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:net.dns-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes DNS hostname resolution:

- resolve a hostname to one or more IP addresses (v4/v6)
- optionally apply timeouts and cancellation

Typical providers:

- POSIX `getaddrinfo`
- c-ares
- platform resolvers (Windows DNS API, macOS resolver)

This is a small "membrane" profile: it lets hosts do deterministic pre-resolution or apply policy
before opening sockets.

---

## 2. Technical Details

### 2.1 Resolution model

The host calls:

- `resolve(name, params, out_addrs, out_cap, out_count)`

`name` is UTF-8 and NUL-terminated. It can be a domain name or a numeric IP literal.

### 2.2 Output buffer semantics

The output is an array of `obi_ip_addr_v0`.

If `out_addrs` is NULL or `out_cap` is too small, providers return:

- `OBI_STATUS_BUFFER_TOO_SMALL`
- `out_count = required_entries`

Otherwise providers fill `out_addrs[0..out_count-1]` and return `OBI_STATUS_OK`.

### 2.3 Timeouts and cancellation

`timeout_ns` is a best-effort upper bound. `timeout_ns==0` means provider default.

When `OBI_DNS_CAP_CANCEL` is advertised and `cancel_token.api != NULL`, providers SHOULD return
`OBI_STATUS_CANCELLED` when cancellation is requested.

---

## 3. Conformance

Required:

- `resolve`

Optional (advertised via caps):

- cancellation support (`OBI_DNS_CAP_CANCEL`)
- provider-specific `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_net_dns_v0.h`
- `abi/profiles/obi_net_types_v0.h`
- `abi/obi_core_v0.h` (cancellation token)

---

## Global Q&A

**Q: Why is DNS split into its own profile instead of being baked into `net.socket`?**  
Some hosts want explicit control of resolution for determinism, caching, policy, or custom DNS
providers (DoH/DoT/etc.). Keeping DNS separate also makes sandboxed/WASM deployments simpler.

