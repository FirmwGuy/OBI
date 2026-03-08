# OBI Provider Guide
## Authoring, Packaging, and Hosting OBI Providers

**Repository:** OBI  
**Document Type:** Implementation guidance (informative)  
**Status:** Draft  
**Last Updated:** 2026-03-06

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
- prefer the host diagnostic callback when available for warnings/errors/fatal conditions,
- use the host log callback (if provided) for human-oriented text instead of process-global stderr,
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

Rules:

- do not write unsolicited diagnostics to the embedding host process's `stdout` or `stderr`,
- do not terminate the embedding host process as an error-reporting strategy,
- do not encode machine-required state only in logs or free-form strings.

When the host exposes `obi_host_v0.emit_diagnostic` (detected via `struct_size`), providers SHOULD
prefer it for structured diagnostics. When only `log` is available, providers MAY emit best-effort
human-readable text there. If neither callback is present, providers should remain silent except for
return values and documented profile-specific error views.

### 2.7 Provider metadata (`describe_json`) and licensing

Providers MAY implement `obi_provider_api_v0.describe_json` to return tool-friendly metadata as a
JSON object string.

This is optional at the ABI level, but providers intended for redistribution SHOULD provide it so
hosts can make informed choices about:

- platform constraints,
- feature completeness,
- and **licensing policy** (for example "permissive only" builds).

Recommended top-level keys (v0 guidance):

- `provider_id` (string, stable)
- `provider_version` (string, semver recommended)
- `profiles` (array of strings; implemented profile IDs)
- `deps` (array of objects): `{ "name", "version", "spdx", "license_class" }`
- `license` (object): `{ "spdx", "license_class" }` for the provider module as shipped
- `behavior` (object): host-safety and diagnostics policy summary

Where:

- `spdx` is an SPDX license expression (example: `MIT`, `LGPL-2.1-or-later`, `GPL-2.0-or-later`).
- `license_class` is a coarse bucket for policy, one of:
  - `permissive` (MIT/BSD/ISC/zlib/public-domain/etc.)
  - `patent` (Apache-2.0/MPL-2.0/etc.)
  - `weak_copyleft` (LGPL/MPL file-level copyleft)
  - `strong_copyleft` (GPL/AGPL)

Providers that wrap dual-license or build-option-sensitive libraries (example: FFmpeg configured as
LGPL vs GPL) MUST report the **effective** license expression of the built artifact they ship.

Recommended `behavior` shape:

- `host_stdio`: object with `stdout` and `stderr` fields; conforming providers should report
  `"never"` for both
- `host_process_termination`: string; conforming providers should report `"never"`
- `diagnostics`: object with booleans and/or strings describing which channels are implemented:
  `status_codes`, `structured_callback`, `log_callback`, `last_error_utf8`

Recommended `last_error_utf8` values:

- `"none"` if the provider exposes no profile-specific borrowed error strings
- `"borrowed_until_next_call_or_destroy"` if it exposes short-lived borrowed UTF-8 views
- `"caller_buffer_copyout"` if text is returned via caller-owned buffers

Hosts MAY reject providers whose declared behavior is incompatible with host policy, even before
considering licensing.

Example (shape only; values are illustrative):

```json
{
  "provider_id": "obi.provider:net.http.curl",
  "provider_version": "0.1.0",
  "profiles": ["obi.profile:net.http_client-0"],
  "license": {"spdx": "MPL-2.0", "license_class": "patent"},
  "behavior": {
    "host_stdio": {"stdout": "never", "stderr": "never"},
    "host_process_termination": "never",
    "diagnostics": {
      "status_codes": true,
      "structured_callback": true,
      "log_callback": true,
      "last_error_utf8": "borrowed_until_next_call_or_destroy"
    }
  },
  "deps": [
    {"name": "libcurl", "version": "8.6.0", "spdx": "curl", "license_class": "permissive"},
    {"name": "OpenSSL", "version": "3.2.0", "spdx": "Apache-2.0", "license_class": "patent"}
  ]
}
```

Hosts and runtimes MAY enforce policy at provider load/selection time using this metadata (allow
lists, deny lists, and/or license profiles).

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
