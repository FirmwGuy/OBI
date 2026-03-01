# OBI Math BigFloat Profile
## OBI Profile: `obi.profile:math.bigfloat-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:math.bigfloat-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal arbitrary-precision floating-point interface.

Typical providers:

- MPFR wrappers
- other bigfloat engines used for high-precision numerics

The focus is on stable ABI and a small surface: create/destroy values and perform basic arithmetic
with explicit precision and rounding.

---

## 2. Technical Details

### 2.1 Object model

BigFloat values are provider-owned opaque IDs (`obi_bigfloat_id_v0`), scoped to a provider instance.

### 2.2 Precision and rounding

Precision is requested in bits at value creation time.

Rounding modes are specified per operation, so hosts can be explicit about behavior even when a
provider uses different internal defaults.

### 2.3 Serialization

This v0 profile does not attempt to standardize a canonical byte encoding. Use string formatting
(optional) or host-specific snapshotting if a deterministic encoding is required.

---

## 3. Conformance

Required:

- create/destroy
- set/get from f64
- add/sub/mul/div

Optional (advertised via caps):

- string conversion (`set_str`, `get_str`)

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_math_bigfloat_v0.h`

---

## Global Q&A

**Q: Why not mandate a canonical binary encoding?**  
Binary encodings tend to bake in limb sizes, exponent ranges, or library-specific internals.
Standardizing a portable canonical encoding is possible, but should be done deliberately as a
separate profile or a v1 update once multiple providers need it.

