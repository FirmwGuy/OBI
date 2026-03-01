# OBI Crypto Hash Profile
## OBI Profile: `obi.profile:crypto.hash-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:crypto.hash-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal streaming hashing interface:

- create a hash context for an algorithm ID (example: `blake3`, `sha256`)
- update with bytes
- finalize to a digest

Typical providers:

- BLAKE3 implementation
- OpenSSL/LibreSSL
- libsodium wrappers

The output digest bytes are stable and suitable for deterministic hosts.

---

## 2. Technical Details

### 2.1 Algorithm IDs

Algorithms are selected by UTF-8 ID strings. Providers MUST return `OBI_STATUS_UNSUPPORTED` for
unknown algorithms.

### 2.2 Digest sizing

Digest size is discovered via `digest_size(algo_id, ...)` to avoid hardcoding sizes in the host.

### 2.3 Ownership

Hash contexts are provider-owned objects (nested OBI handles) destroyed via `destroy`.

Inputs to `update` are borrowed for the duration of the call only.

---

## 3. Conformance

Required:

- `digest_size`
- `create`
- hash context: `update`, `final`, `destroy`

Optional (advertised via caps):

- `reset` on hash contexts (reuse after finalization)

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_crypto_hash_v0.h`

---

## Global Q&A

**Q: Why not include HMAC or AEAD?**  
Those are separate primitives with different keying and misuse considerations. A future set of
focused `crypto.*` profiles can cover them when needed.

