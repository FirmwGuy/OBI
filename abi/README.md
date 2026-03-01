# OBI ABI Artifacts
## Reference C Headers for OBI Core and Profiles

**Document Type:** Reference index (normative)  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

This directory contains reference C headers defining the normative ABI shapes used by OBI:

- `obi_core_v0.h` - core types (status codes, host/provider shape, stream helpers)
- `profiles/` - per-profile handle structs, vtables, and capability bits

These headers are intended to be:

- small, portable, and FFI-friendly,
- stable within their ABI major version,
- directly usable by providers and hosts.

