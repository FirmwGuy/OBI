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

## 2. Determinism Notes (CEP integration)

HTTP is inherently nondeterministic. When used under a deterministic host (CEP), the host must
record request intents and response outcomes and define replay behavior (simulate vs re-apply).
This profile must make it possible to capture the request/response bytes and metadata.

---

## 3. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_net_http_client_v0.h`

