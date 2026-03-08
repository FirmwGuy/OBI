# OBI Conformance
## What It Means to Conform to OBI Core and Profiles

**Repository:** OBI  
**Document Type:** Conformance guidance (informative)  
**Status:** Draft  
**Last Updated:** 2026-03-06

---

## 1. Nontechnical Summary

OBI conformance is not just "it compiles." It means:

- providers implement the required functions for profiles they claim,
- hosts call into providers safely (version checks, caps checks, lifetimes),
- both sides agree on ownership, error codes, and threading rules.

This document provides checklists for hosts and providers.

---

## 2. Provider Conformance Checklist

For each provider instance:

1. Provider identity
   - returns stable `provider_id()` and `provider_version()`
2. ABI compatibility
   - sets vtable `abi_major/abi_minor/struct_size` correctly
3. Profile discovery
   - returns `OBI_STATUS_UNSUPPORTED` for unknown profiles
   - validates output handle buffer sizes
4. Capability honesty
   - capability bits match implemented functions and behavior
5. Ownership and lifetimes
   - does not retain borrowed pointers
   - provides release/destroy functions for provider-owned resources
6. Threading clarity
   - documents thread affinity and concurrency rules
7. Error behavior
   - returns `obi_status` codes consistently
   - does not write unsolicited diagnostics to process-global `stdout` or `stderr`
   - does not terminate the embedding host process as an error-reporting mechanism
   - uses host diagnostic/log callbacks when supplied instead of ad-hoc global output

---

## 3. Host Conformance Checklist

For each host integrating providers:

1. ABI validation
   - checks profile ABI major before calling
   - checks vtable `struct_size` before calling optional functions
2. Capability checks
   - does not assume optional features without checking caps
3. Ownership correctness
   - calls release/destroy exactly once where required
   - does not free provider-owned memory with host allocators
4. Buffer sizing
   - handles `OBI_STATUS_BUFFER_TOO_SMALL` and retries with adequate buffers
5. Threading correctness
   - obeys provider thread-affinity rules
   - serializes calls when thread-safety is not guaranteed
6. Shutdown correctness
   - destroys jobs/readers/responses before destroying the provider (unless documented otherwise)
7. Diagnostics correctness
   - does not assume logs are parseable or stable
   - copies borrowed error/diagnostic strings before the next provider call if it needs to retain them

---

## Global Q&A

**Q: Do we need an automated conformance test suite?**  
Probably, but it should live in a host repo (or a dedicated harness repo) because conformance is
about behavior, not just headers. This spec repo provides the checklists and ABI shapes first.

**Q: What is the minimum a host should do?**  
Validate ABI majors, check `struct_size` for optional calls, obey ownership, and follow threading
rules. Those four prevent most integration failures.
