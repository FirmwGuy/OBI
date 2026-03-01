# OBI Core Pump Profile
## OBI Profile: `obi.profile:core.pump-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:core.pump-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Purpose

Many libraries require a pump or main loop to make progress (curl multi, GLib/libsoup, gstreamer).
This profile standardizes a minimal stepping interface so hosts can integrate those providers
without importing a specific event-loop framework.

---

## 2. Conformance

An implementation of this profile MUST provide:

- `step(timeout_ns)` to advance internal work

An implementation MAY also provide:

- `get_wait_hint()` to help hosts integrate stepping efficiently

---

## 3. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_pump_v0.h`

---

## Global Q&A

**Q: Does this replace epoll/kqueue integration?**  
No. This is the lowest common denominator. A future profile may provide OS-level wait handles, but
`step()` is enough for correctness and simple integration.

