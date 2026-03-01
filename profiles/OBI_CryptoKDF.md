# OBI Crypto KDF Profile
## OBI Profile: `obi.profile:crypto.kdf-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:crypto.kdf-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes key derivation functions (KDFs) used to derive keys from inputs such as:

- input key material (HKDF)
- passwords (PBKDF2, Argon2id)

Typical providers:

- libsodium wrappers (HKDF-ish building blocks, Argon2)
- OpenSSL / libcrypto wrappers (HKDF, PBKDF2)
- standalone Argon2 implementations

---

## 2. Technical Details

### 2.1 KDF kinds

v0 standardizes a small set of common KDF families via `obi_kdf_kind_v0`:

- HKDF
- PBKDF2
- Argon2id

Providers MUST document supported hashes (`hash_id`) and parameter constraints.

### 2.2 Output model

The host calls `derive_bytes(input, params, ...)` to obtain derived bytes.

Providers MUST use the BUFFER_TOO_SMALL pattern for output sizing.

### 2.3 Ownership

All inputs are host-owned and borrowed for the duration of the call only.

---

## 3. Conformance

Required:

- `derive_bytes`

Optional (advertised via caps):

- support for specific KDF kinds (HKDF/PBKDF2/Argon2id)
- provider-specific `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_crypto_kdf_v0.h`

---

## Global Q&A

**Q: Why is HKDF parameterized by a hash string instead of a fixed set?**  
Different deployments standardize on different hashes. Using `hash_id` keeps the surface small
while still enabling strict policy at higher layers.

