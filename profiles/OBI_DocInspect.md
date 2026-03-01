# OBI Document Inspect Profile
## OBI Profile: `obi.profile:doc.inspect-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:doc.inspect-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes "deep probing" of documents beyond simple file type sniffing.

It is designed for hosts that want to:

- detect a canonical MIME type and format ID
- extract basic structural summary (dimensions, page count, duration, track list, etc.)
- extract metadata (EXIF, XMP, ID3, container tags, etc.)

Typical providers:

- libmagic-backed sniffers with extra decoders for richer metadata
- FFmpeg/libavformat probes (streams, durations, tags)
- image metadata libraries (exiftool-style pipelines)

This profile complements `obi.profile:data.file_type-0`:

- `data.file_type` is a lightweight guesser
- `doc.inspect` is a deeper inspector that may parse more of the content

---

## 2. Technical Details

### 2.1 Inputs

Required input form:

- inspect from bytes (for memory buffers / small files)

Optional input form:

- inspect from an OBI reader (for file streams)

Reader probing is intentionally one-way: the provider may consume bytes from the reader and does
not have to rewind it. If the host requires rewind, it should pass a seekable/buffered reader.

### 2.2 Outputs

The inspector returns a single info object containing:

- canonical `mime_type` (UTF-8)
- `format_id` (short stable-ish ID, e.g. `pdf`, `png`, `mp3`, `gltf`, `zip`)
- optional human description and encoding hints
- optional JSON objects:
  - `summary_json` (structural summary; small and predictable)
  - `metadata_json` (metadata tags; may be large)

JSON is used in v0 to keep the ABI small while still enabling rich metadata.

### 2.3 Ownership

All output views are provider-owned and released via the `release` callback on the info object.

---

## 3. Conformance

Required:

- `inspect_from_bytes`

Optional (advertised via caps):

- `inspect_from_reader`
- `summary_json`
- `metadata_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_doc_inspect_v0.h`

---

## Global Q&A

**Q: Why JSON for metadata?**  
Typed metadata is possible, but it balloons ABI surface quickly. JSON keeps v0 implementable and
usable from many languages. A future profile can standardize a typed metadata table once multiple
providers need it.

