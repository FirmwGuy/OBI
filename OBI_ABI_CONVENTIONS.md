# OBI ABI Conventions
## Stable C ABI Rules for Hosts and Providers

**Repository:** OBI  
**Document Type:** ABI conventions (normative)  
**Status:** Draft  
**Last Updated:** 2026-03-06

---

## 1. Nontechnical Summary

OBI is intended to be usable from many languages and runtimes (C, C++, Rust, Zig, Python FFI). To
make that realistic, OBI profiles use a small set of ABI rules:

- fixed layouts,
- explicit sizes and ownership,
- clear optionality and capability discovery.

This document captures the common conventions used across OBI headers.

---

## 2. Technical Rules

### 2.1 Use fixed-size types in ABI-visible structs

In public structs and vtables:

- use `uint32_t`, `uint64_t`, etc.
- avoid C bitfields
- avoid `long`, `size_t` for semantic fields (use for buffer sizes only)

### 2.2 Prefer `uint8_t` to `bool` for ABI-visible booleans

`bool` is generally safe in C, but FFI bindings often do better with explicit-width integer
booleans. If a boolean is part of an ABI-visible struct payload, prefer:

- `uint8_t field; /* 0 or 1 */`

Returning `bool` from a function is acceptable when it is not embedded in a struct.

### 2.3 Vtables must be self-describing

Every profile vtable begins with:

- `abi_major`, `abi_minor`
- `struct_size`
- `caps`

Hosts MUST:

- validate ABI major before calling,
- use `struct_size` to detect whether optional function pointers exist.

Providers MUST:

- set `struct_size` to `sizeof(vtable_struct)` they compiled with,
- set capability bits consistently with the functions they expose.

### 2.4 Output buffers: use the "buffer too small" pattern

For functions that write into caller-provided buffers, the preferred pattern is:

- always return the required size in an `out_*` parameter,
- return `OBI_STATUS_BUFFER_TOO_SMALL` when the provided capacity is insufficient.

### 2.5 Ownership must be explicit

Every pointer returned across the interface must have one of these lifetimes:

1) **Borrowed:** valid only for the duration of the call.
2) **Caller-owned:** allocated via host allocator hooks (or specified allocator) and freed by the
   caller.
3) **Provider-owned:** released by a documented `release` callback or a vtable `destroy/release`
   function.

If ownership is not specified, hosts MUST assume "borrowed" and providers MUST assume "caller does
not free".

### 2.6 Error text and diagnostics must have explicit lifetime

`obi_status` is the primary machine-readable error channel.

Supplementary human-readable diagnostics must use one of these patterns:

- a structured callback payload documented in the ABI (for example `obi_diagnostic_v0` delivered via
  `obi_host_v0.emit_diagnostic`)
- a borrowed `obi_utf8_view_v0` whose lifetime is explicitly documented
- a caller-owned buffer using the standard `OBI_STATUS_BUFFER_TOO_SMALL` retry pattern

Forbidden patterns:

- returning heap-owned `char*` error strings without an ABI-specified free rule
- requiring callers to infer ownership from library-specific conventions
- relying on process-global `stdout` or `stderr` as the only error channel

Strings delivered through a host diagnostic callback are borrowed for the duration of the callback
only unless a profile or core ABI document explicitly states otherwise.

### 2.7 Async calls must not retain borrowed pointers

For any async submission API:

- the provider must copy any needed input data before returning, or
- the ABI must explicitly transfer ownership of the input object(s).

"Borrowed but used later" is forbidden.

### 2.8 Reserved fields are required

ABI-visible structs SHOULD include reserved fields to allow future expansion without breaking ABI.
Reserved fields MUST be zeroed by callers and ignored by providers unless specified otherwise.

---

## Global Q&A

**Q: Why not auto-generate all ABIs from a schema?**  
That can be added later, but C headers are the simplest interoperability substrate today and match
how most third-party libraries expose stable interfaces.

**Q: Why use vtables instead of linking directly?**  
Vtables make provider selection and swapping explicit, reduce symbol collisions, and allow runtime
capability checks without build-time coupling.
