# OBI Data File Type Profile
## OBI Profile: `obi.profile:data.file_type-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:data.file_type-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes file type detection (content sniffing) so hosts can choose the correct
decoder/handler before committing to parsing.

Typical providers:

- libmagic (file(1) "magic" database)
- lightweight signature sniffers (custom tables)

The interface supports detecting from:

- bytes (required)
- optional readers (for file streams) with a provider-defined maximum probe size

---

## 2. Technical Details

### 2.1 Output fields

Providers return:

- MIME type (example: `image/png`)
- a human-readable description (example: `PNG image data, 256 x 256`)
- optional encoding (example: `utf-8`)
- optional confidence score

Strings are returned as provider-owned UTF-8 views and released via a callback.

### 2.2 Probe limits

When detecting from an OBI reader, the provider may read up to `max_probe_bytes`.

Hosts should treat readers as consumed: this profile does not attempt to rewind the reader after
probing. If rewind is required, the host should provide a seekable reader or a buffered wrapper.

---

## 3. Conformance

Required:

- `detect_from_bytes`

Optional (advertised via caps):

- `detect_from_reader`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_data_file_type_v0.h`

---

## Global Q&A

**Q: Why not just use filename extensions?**  
Extensions are cheap hints but unreliable. This profile standardizes content-based detection so
hosts can choose correct handlers even when filenames are missing or untrusted.

