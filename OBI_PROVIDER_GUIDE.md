# OBI Provider Guide
## Authoring, Packaging, and Hosting OBI Providers

**Repository:** OBI  
**Document Type:** Implementation guidance (informative)  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

An OBI **provider** is a module that implements one or more OBI profiles (HTTP, window/input, 2D
rendering, text shaping, etc.).

This guide explains how providers should be packaged and what hosts should expect, so we can swap
libraries without rewriting the system.

---

## 2. Technical Guidance

### 2.1 Provider identity and stability

Providers MUST expose a stable provider ID string (examples: `provider:curl`, `provider:libsoup`,
`provider:sdl3`, `provider:raylib`).

Provider IDs are used for:

- runtime selection (CLI/config/policy),
- observability and debug,
- export/import of host configuration.

Changing the provider ID is a breaking change for any host configuration that references it.

### 2.2 Hosting model: static or dynamic

OBI does not require dynamic loading, but supports it.

Hosting patterns:

- **Static providers:** compiled and linked into the host. The host constructs providers directly.
- **Dynamic providers:** loaded from shared libraries. The host finds and calls the factory symbol
  `OBI_PROVIDER_FACTORY_SYMBOL_V0` (`obi_provider_factory_v0`).

Dynamic loading is intentionally underspecified (paths, search rules, signing). Those are host
policy choices.

### 2.3 ABI handshake

Providers receive an `obi_host_v0` from the host. They MUST:

- use host allocators when returning host-owned memory (unless the profile specifies otherwise),
- use the host log callback (if provided) instead of stderr,
- tolerate optional NULL hooks (host may omit logging or wallclock).

### 2.4 `get_profile` rules

Providers implement `get_profile(profile_id, profile_abi_major, out_profile, out_profile_size)`.

Rules:

- The provider MUST NOT store pointers to `out_profile`.
- The provider MUST validate `out_profile_size` and fail with `OBI_STATUS_BAD_ARG` if the buffer is
  too small.
- The provider MUST return `OBI_STATUS_UNSUPPORTED` if the profile is not implemented.
- Profile handles are typically `{ api, ctx }` where `ctx` is provider-owned.

### 2.5 Threading and pumps

Providers MUST document thread rules per profile:

- whether functions can be called concurrently,
- whether calls must happen on the same thread that created the provider,
- whether progress requires a pump (`obi.profile:core.pump-0`).

If a provider requires a pump to make progress for a profile, it SHOULD set the relevant profile
capability bits (profile-specific) and, where appropriate, the provider caps in
`obi_provider_api_v0.caps`.

Provider-level caps are defined in `abi/obi_core_v0.h`:

- `OBI_PROVIDER_CAP_THREAD_SAFE`
- `OBI_PROVIDER_CAP_SPAWNS_THREADS`
- `OBI_PROVIDER_CAP_REQUIRES_PUMP`

### 2.6 Error reporting

Providers should treat `obi_status` codes as the authoritative error channel.

Logging is best-effort diagnostics, not a contract. Do not encode parseable state only in logs.

---

## 3. Q&A

**Q: Do providers have to be one library each?**  
No. A single provider may wrap multiple libraries or subsystems, as long as it presents coherent
profiles and honors lifetime/threading rules.

**Q: Can a provider implement multiple profiles that share internal objects?**  
Yes, and this is common (for example window_input + render2d sharing a GPU context). Cross-profile
handle interoperability is only guaranteed within the same provider instance.

**Q: How do we handle licensing or platform constraints?**  
Those decisions live in host configuration and policy. OBI makes it cheap to swap providers when
constraints change.
