# OBI Document Text Decode Profile
## OBI Profile: `obi.profile:doc.text_decode-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:doc.text_decode-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes decoding arbitrary text bytes into UTF-8.

It is meant for hosts that need to ingest files with unknown or legacy encodings and normalize
them to UTF-8 before further processing (tokenizing, parsing, indexing, layout).

Typical providers:

- iconv-based decoders
- ICU converters
- libraries that combine encoding detection + conversion

---

## 2. Technical Details

### 2.1 Inputs

Required:

- decode from bytes to a UTF-8 writer

Optional:

- decode from an OBI reader to a UTF-8 writer

### 2.2 Encoding detection

Providers MAY:

- use an explicit `encoding_hint` when supplied
- otherwise perform best-effort detection using a probe prefix (up to `max_probe_bytes`)

Providers should report the detected encoding ID and an optional confidence score.

### 2.3 Error handling

Providers MUST support at least one of:

- strict decoding (fail on invalid sequences)
- replacement decoding (substitute invalid sequences with U+FFFD)

Hosts select behavior via flags.

---

## 3. Conformance

Required:

- `decode_bytes_to_utf8_writer`

Optional (advertised via caps):

- `decode_reader_to_utf8_writer`
- encoding confidence reporting

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_doc_text_decode_v0.h`

---

## Global Q&A

**Q: Why not just assume UTF-8?**  
Many real-world files are not UTF-8 (legacy encodings, mislabeled content, BOM variants). A
standard decode profile makes ingestion robust and keeps encoding glue swappable.

