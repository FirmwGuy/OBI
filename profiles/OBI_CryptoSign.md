# OBI Crypto Sign Profile
## OBI Profile: `obi.profile:crypto.sign-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:crypto.sign-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes digital signatures:

- import public/private keys
- sign messages
- verify signatures
- optional keypair generation and key export

Typical providers:

- libsodium wrappers (Ed25519)
- OpenSSL / libcrypto wrappers (RSA/ECDSA/EdDSA)
- libgcrypt providers

---

## 2. Technical Details

### 2.1 Algorithm and key formats

Hosts select algorithms by an `algo_id` string.

Examples (non-normative):

- `ed25519`
- `rsa-pss-sha256`
- `ecdsa-p256-sha256`

Keys are imported from a provider-defined `key_format` encoding.

Examples (non-normative):

- `raw` (algorithm-specific raw key bytes)
- `pem` (PEM text)
- `pkcs8_der` (private keys)
- `spki_der` (public keys)

Providers MUST document supported `algo_id` and `key_format` strings.

### 2.2 Sign/verify semantics

`sign` produces a signature into a caller-provided buffer, using the BUFFER_TOO_SMALL sizing
pattern.

`verify` returns `out_ok=false` when the signature is invalid.

### 2.3 Ownership

Key bytes are borrowed for the duration of the import call only.

Key handles are provider-owned and destroyed via their `destroy` functions.

---

## 3. Conformance

Required:

- import public/private key
- sign/verify
- destroy keys

Optional (advertised via caps):

- keypair generation
- key export
- provider-specific `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_crypto_sign_v0.h`

---

## Global Q&A

**Q: Why not standardize certificate/X.509 signing here?**  
That expands into PKI policy. This profile focuses on raw signature primitives; certificate and
PKI workflows can be standardized separately if needed.

