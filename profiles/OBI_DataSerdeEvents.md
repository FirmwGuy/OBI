# OBI Data Serde Events Profile
## OBI Profile: `obi.profile:data.serde_events-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:data.serde_events-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes an event-based parser interface for common structured data formats:

- open a document from an `obi_reader_v0` (or optional in-memory bytes)
- iterate tokens representing maps, sequences, and scalars

Typical providers:

- simdjson / rapidjson wrappers (JSON)
- libyaml / yaml-cpp wrappers (YAML)
- toml parsers (TOML)

This profile is not a DOM/tree API. Hosts can build their own in-memory representations or
stream-convert data to other formats.

---

## 2. Technical Details

### 2.1 Format selection

Hosts MAY pass a `format_hint` such as:

- `json`
- `yaml`
- `toml`

Providers SHOULD auto-detect when possible.

### 2.2 Event model

The parser yields a sequence of `obi_serde_event_v0` tokens:

- document start/end (optional for formats that support streams)
- begin/end map
- begin/end sequence
- key (UTF-8)
- scalar values: string, number (as text), bool, null

Numeric values are represented as text to avoid forcing a specific numeric policy onto hosts.

### 2.3 Key constraints

Map keys are represented as UTF-8 strings.

Providers that parse formats with non-string keys (some YAML cases) MUST either:

- stringify the key, or
- return `OBI_STATUS_UNSUPPORTED` (or an error) as documented.

### 2.4 Ownership

The input reader is borrowed for the duration of `open_reader` only.

Scalar/key text views are provider-owned and valid until the next `next_event` call (or parser
destruction). Hosts MUST copy data they need to keep.

---

## 3. Conformance

Required:

- open from reader
- iterate events (`next_event`)
- destroy parser

Optional (advertised via caps):

- open from bytes
- multi-document streams (`DOC_START`/`DOC_END`)
- provider-specific `options_json`
- location reporting
- `last_error_utf8`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_data_serde_events_v0.h`

---

## Global Q&A

**Q: Why not standardize a typed JSON AST or YAML node graph?**  
Those representations vary and can become large. An event stream is the common denominator and can
feed either a DOM builder or a streaming transformer.

