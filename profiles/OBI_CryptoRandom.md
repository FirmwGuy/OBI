# OBI Crypto Random Profile
## OBI Profile: `obi.profile:crypto.random-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:crypto.random-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes access to a cryptographically secure random number generator (CSPRNG):

- fill a caller-provided buffer with random bytes

Typical providers:

- libsodium randombytes wrappers
- OS-backed RNG providers (`getrandom`, `arc4random`, `BCryptGenRandom`, etc.)

---

## 2. Technical Details

### 2.1 Output model

The host calls `fill(dst, dst_size)` to obtain random bytes.

Providers MUST return `OBI_STATUS_UNAVAILABLE` if the system RNG is not available (for example in a
restricted sandbox), and SHOULD return `OBI_STATUS_ERROR` for other failures.

### 2.2 Ownership

The output buffer is host-owned and borrowed for the duration of the call only.

---

## 3. Conformance

Required:

- `fill`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_crypto_random_v0.h`

---

## Global Q&A

**Q: Why not standardize RNG seeding?**  
For CSPRNG use, the provider should manage seeding internally and prefer OS entropy sources.
Deterministic PRNGs for simulation/tests belong in a different profile.

