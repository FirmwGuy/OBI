# OBI Crypto AEAD Profile
## OBI Profile: `obi.profile:crypto.aead-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:crypto.aead-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes authenticated encryption with associated data (AEAD):

- encrypt + authenticate (`seal`)
- decrypt + verify (`open`)

Typical providers:

- libsodium wrappers (ChaCha20-Poly1305)
- OpenSSL / libcrypto wrappers (AES-GCM, ChaCha20-Poly1305)
- libgcrypt providers

This profile is intended for building secure protocols and storage formats without binding hosts to
a specific crypto library.

---

## 2. Technical Details

### 2.1 Algorithm selection

Hosts select algorithms by an `algo_id` string.

Examples (non-normative):

- `chacha20-poly1305`
- `aes-256-gcm`

Providers MUST document supported algorithm IDs and their expected key/nonce sizes.

### 2.2 Buffer model

`seal` outputs `ciphertext || tag` in one contiguous buffer.

`open` expects the same concatenated input and returns `out_ok=false` when authentication fails.

### 2.3 Ownership

All input buffers are host-owned and borrowed for the duration of the call only.

Output buffers are host-owned.

---

## 3. Conformance

Required:

- key/nonce/tag size queries
- create/destroy context
- `seal` and `open`

Optional (advertised via caps):

- provider-specific `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_crypto_aead_v0.h`

---

## Global Q&A

**Q: Why append the tag instead of returning it separately?**  
It keeps the ABI small and matches common on-wire/storage formats. Detached tags can be added later
as an optional capability if multiple providers need it.

