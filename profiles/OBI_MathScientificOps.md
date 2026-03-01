# OBI Math Scientific Ops Profile
## OBI Profile: `obi.profile:math.scientific_ops-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:math.scientific_ops-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a small set of "scientific library" operations that are commonly pulled
in via GSL-like dependencies:

- special functions (gamma, erf, bessel, ...)

Typical providers:

- GSL wrappers
- Cephes / Boost-style special function backends
- platform math extensions wrapped behind OBI

This v0 profile is intentionally narrow. Broader scientific computing (ODE solvers, integration,
interpolation, FFT, optimization) should be separate focused profiles once needed.

---

## 2. Technical Details

### 2.1 API shape

Operations are stateless and operate on `double` inputs/outputs.

Providers advertise supported operations via capability bits and MAY leave unsupported function
pointers as NULL.

### 2.2 Error behavior

Domain errors and overflows should be reported via:

- `OBI_STATUS_BAD_ARG` for invalid inputs (example: gamma at a pole)
- `OBI_STATUS_ERROR` for other computation failures

Providers SHOULD avoid relying on global `errno` as a contract.

---

## 3. Conformance

Required:

- capability bits and consistent NULL/unsupported behavior

Optional:

- additional special functions via future minor extensions (append-only vtable growth)

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_math_scientific_ops_v0.h`

---

## Global Q&A

**Q: Why not expose all of GSL?**  
Because it is too large and changes too often for a stable v0 ABI. OBI should standardize small
surfaces that multiple providers can implement and hosts can actually swap.

