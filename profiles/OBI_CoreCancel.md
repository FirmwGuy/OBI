# OBI Core Cancel Profile
## OBI Profile: `obi.profile:core.cancel-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:core.cancel-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes cancellation primitives for long-running work:

- create a cancellation source
- obtain cancellation tokens from the source
- signal cancellation (optionally with a reason)

Cancellation tokens can then be passed into other APIs (profiles or host subsystems) to allow
cooperative cancellation without having to destroy handles abruptly.

---

## 2. Technical Details

### 2.1 Token model

The core token type is defined in `abi/obi_core_v0.h` as `obi_cancel_token_v0`.

Tokens are queried via:

- `is_cancelled()`
- optional `reason_utf8()`

### 2.2 Source model

A cancellation source:

- produces tokens (`token(out_token)`)
- can be signalled (`cancel(reason)`)

Providers MAY support resetting sources via `reset()`.

### 2.3 Ownership

Tokens returned by a source are provider-owned and destroyed via the token vtable `destroy`.

Sources are provider-owned and destroyed via `obi_cancel_source_v0.destroy`.

---

## 3. Conformance

Required:

- create source
- create token
- cancel
- destroy

Optional (advertised via caps):

- reset

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_cancel_v0.h`
- `abi/obi_core_v0.h` (token type)

---

## Global Q&A

**Q: Why a separate cancel token type instead of using timeouts everywhere?**  
Timeouts handle "give up after N time", but cancellation is often driven by user intent or system
shutdown. Tokens allow consistent cooperative cancellation across unrelated subsystems.

