# OBI Paged Document Profile
## OBI Profile: `obi.profile:doc.paged_document-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:doc.paged_document-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes opening and rasterizing "paged documents" such as:

- PDF
- SVG (treated as a single-page document)
- other page-based vector or fixed-layout formats

Typical providers:

- MuPDF
- Poppler
- PDFium

The baseline goal is: given a document reader, get page count/sizes and render pages to CPU pixel
buffers for display or thumbnailing.

Optional capabilities can add:

- text extraction
- metadata access

---

## 2. Technical Details

### 2.1 Inputs

Documents are opened from an OBI reader (file/stream).

Providers may also support opening directly from bytes (memory buffers).

### 2.2 Page sizes

Page sizes are returned in "points" (1/72 inch), matching common document conventions.

### 2.3 Rasterization

Pages are rendered to CPU pixel buffers (RGBA8 baseline). Output buffers are provider-owned and
released via a callback.

Rasterization parameters include a DPI target and optional background color.

### 2.4 Ownership and lifetimes

- The provider borrows the input reader for the duration of open only (unless documented otherwise).
- The document handle remains valid until destroyed.
- Rendered page pixel buffers are provider-owned until released.

---

## 3. Conformance

Required:

- open from reader
- document: page count, page size, render page, destroy

Optional (advertised via caps):

- open from bytes
- metadata JSON
- text extraction

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_doc_paged_document_v0.h`
- `abi/profiles/obi_media_types_v0.h`

---

## Global Q&A

**Q: Why not return vector primitives instead of pixels?**  
Vector extraction is format- and renderer-specific and tends to explode the ABI. Pixels are the
portable baseline. A future profile can add optional vector scene extraction if needed.

