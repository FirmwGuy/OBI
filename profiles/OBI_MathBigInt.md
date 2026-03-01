# OBI Math BigInt Profile
## OBI Profile: `obi.profile:math.bigint-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:math.bigint-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal big integer (arbitrary precision integer) interface.

Typical providers:

- GMP (`mpz_t`) wrappers
- other big integer engines used for crypto, number theory, or exact arithmetic

The goal is not to replace domain math libraries, but to make it possible for hosts to swap
implementations while keeping a stable ABI and deterministic serialization hooks (import/export).

---

## 2. Technical Details

### 2.1 Object model

BigInt values are provider-owned opaque IDs (`obi_bigint_id_v0`). They are only meaningful within
the provider instance that created them.

### 2.2 Import/export

This profile standardizes a big-endian magnitude byte encoding plus an explicit sign flag:

- magnitude bytes are unsigned big-endian without a required leading sign byte
- sign is provided separately (`is_negative`)

This is designed to integrate with deterministic hosts (CEP) that need stable binary snapshots.

### 2.3 Aliasing

Arithmetic functions accept an explicit `out` ID.

Providers SHOULD support in-place operations (where `out` equals `a` and/or `b`) for basic ops.
If a provider cannot support a particular aliasing pattern, it MUST return `OBI_STATUS_BAD_ARG`.

---

## 3. Conformance

Required:

- create/destroy
- set/get i64/u64
- set/get bytes (big-endian magnitude + sign)
- copy, compare
- add/sub/mul

Optional (advertised via caps):

- division/mod (`div_mod`)
- string conversion (`set_str`, `get_str`)

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_math_bigint_v0.h`

---

## Global Q&A

**Q: Why bytes + sign instead of two's complement?**  
Magnitude+sign is simpler to specify and stable across libraries, and avoids ambiguity about
sign-extension and minimal length encodings.

**Q: Why not define a full bignum/crypto API here?**  
Because semantics diverge quickly (constant-time requirements, side-channels, modular arithmetic
primitives). OBI should add focused profiles only when multiple providers need the same contract.

