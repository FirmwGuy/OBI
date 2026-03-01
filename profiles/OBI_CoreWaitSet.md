# OBI Core WaitSet Profile
## OBI Profile: `obi.profile:core.waitset-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:core.waitset-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

Many OBI providers need an event loop to make progress (`obi.profile:core.pump-0`). Some of those
providers can also expose OS-level waitables (file descriptors, Windows handles) so hosts can:

- block efficiently until something becomes ready
- integrate multiple providers into one host wait loop

This profile standardizes a small "waitset hint" surface:

- ask the provider which wait handles it cares about right now
- get a suggested timeout / deadline for the next wakeup

Typical providers:

- curl multi-style providers that expose socket fds
- GLib-based providers that expose poll fds

---

## 2. Technical Details

### 2.1 Relationship to `core.pump`

This profile does not replace the pump. It is a companion:

1) host queries waitset handles + timeout
2) host waits using its OS wait API (poll/epoll/kqueue/WaitForMultipleObjects/etc.)
3) host calls `pump.step(0)` (or with a small timeout) to let the provider make progress

Providers that support this profile SHOULD also implement `obi.profile:core.pump-0`.

### 2.2 Wait handle kinds

This v0 profile supports:

- Unix-like file descriptors (FD)
- Windows HANDLE values (opaque integer/pointer values)

Providers MUST only return kinds they advertise via caps.

### 2.3 Ownership and buffer sizing

Wait handles are returned into a host-provided array, following standard OBI sizing rules:

- if handles is NULL or cap is 0, the provider returns OK and sets required count
- if cap is too small, the provider returns `OBI_STATUS_BUFFER_TOO_SMALL` and sets required count

---

## 3. Conformance

Required:

- `get_wait_handles`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_waitset_v0.h`

---

## Global Q&A

**Q: Why not return readiness events (readable/writable)?**  
To keep v0 minimal and portable. Hosts already have OS-level readiness results; providers typically
only need to be pumped after a wakeup. If event-driven socket_action style integration becomes
important, a future profile can add an explicit "notify readiness" call.

