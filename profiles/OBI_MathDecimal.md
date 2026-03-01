# OBI Math Decimal Profile
## OBI Profile: `obi.profile:math.decimal-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:math.decimal-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal decimal arithmetic interface (base-10 floating point), useful
for:

- financial computations
- human-facing exact decimal math (avoid binary float surprises)
- decimal interchange formats

Typical providers:

- libmpdec (mpdecimal)
- decNumber-style engines

This profile provides:

- explicit decimal contexts (precision/rounding/exponent limits)
- decimal values as provider-owned opaque IDs
- conversions to/from strings

---

## 2. Technical Details

### 2.1 Contexts and signals

Decimal arithmetic is governed by a context:

- precision (decimal digits)
- rounding mode
- exponent limits (emin/emax)

Operations can also raise IEEE-754-style signals (inexact, rounded, overflow, div-by-zero, etc.).
This profile exposes those signals as a bitmask output so hosts can choose whether to ignore or
record them.

### 2.2 Serialization

This v0 profile standardizes string conversion. It does not attempt to standardize a canonical
binary encoding.

Deterministic hosts should snapshot decimal values via `get_str` (or a future canonical encoding
extension).

---

## 3. Conformance

Required:

- context create/destroy
- decimal create/destroy, copy
- set/get from string
- add/sub/mul/div

Optional (advertised via caps):

- quantize/rescale helpers
- to/from f64 conversions

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_math_decimal_v0.h`

---

## Global Q&A

**Q: Why a dedicated decimal profile when we already have BigFloat?**  
Decimal and binary floating point serve different needs. Decimal arithmetic is the practical tool
for money and human-scale exactness, and implementations (mpdecimal) have different context rules
and signaling than MPFR-style bigfloats.

