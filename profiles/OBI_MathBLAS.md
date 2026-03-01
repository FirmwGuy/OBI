# OBI Math BLAS Profile
## OBI Profile: `obi.profile:math.blas-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:math.blas-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a small subset of BLAS-style operations so hosts can swap vector/matrix
libraries (OpenBLAS, MKL, Accelerate, BLIS, etc.) behind a stable ABI.

The intent is not to cover the entire BLAS/LAPACK ecosystem in v0, but to provide the core building
block that many higher-level numeric libraries depend on: matrix multiplication (GEMM).

---

## 2. Technical Details

### 2.1 API shape

Operations are "pure" functions: the provider does not own or allocate matrices. Inputs and outputs
are pointers to host-owned memory.

### 2.2 Layout

The ABI uses a CBLAS-style layout enum:

- row-major
- column-major

Providers MUST interpret `lda/ldb/ldc` consistently with the selected layout.

### 2.3 Threading

Threading is provider-defined. Some backends may use internal thread pools.

Hosts that require determinism or strict CPU budgeting SHOULD choose providers accordingly and may
prefer single-threaded backends.

---

## 3. Conformance

Required:

- `sgemm` and `dgemm` (or return `OBI_STATUS_UNSUPPORTED` if a type is unavailable)

Optional (advertised via caps):

- additional BLAS ops (gemv, axpy, etc.) in future minor extensions

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_math_blas_v0.h`

---

## Global Q&A

**Q: Why only GEMM?**  
GEMM is the core primitive that justifies linking a BLAS backend in many systems. The profile can
grow carefully via minor additions as needed.

