# OBI Data Serde Emit Profile
## OBI Profile: `obi.profile:data.serde_emit-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:data.serde_emit-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes emitting structured data formats (JSON/YAML/TOML class) from an event
stream:

- open an emitter for a chosen format
- feed map/sequence/scalar events
- write encoded output to an `obi_writer_v0`

Typical providers:

- JSON/YAML emitters
- TOML emitters
- generic "serde" layers that can target multiple output formats

This profile is the natural counterpart to `obi.profile:data.serde_events-0` (event-based parsing).

---

## 2. Technical Details

### 2.1 Emitter model

The host calls `open_writer(writer, params, out_emitter)` where:

- `writer` is caller-owned and remains valid until emitter destruction
- `format_hint` selects the output format (for example `json`, `yaml`, `toml`)

The host then feeds events via `emitter.emit(ev)` and finalizes via `emitter.finish()`.

### 2.2 Event set

The emitted event set matches `obi_serde_event_v0` from `data.serde_events`:

- `DOC_START` / `DOC_END`
- `BEGIN_MAP` / `END_MAP`
- `BEGIN_SEQ` / `END_SEQ`
- `KEY`
- `STRING` / `NUMBER` / `BOOL` / `NULL`

### 2.3 Errors

When `OBI_SERDE_EMIT_CAP_LAST_ERROR` is advertised, providers return a provider-owned UTF-8 error
view via `last_error_utf8()`.

---

## 3. Conformance

Required:

- `open_writer`
- `emitter.emit`
- `emitter.finish`
- `emitter.destroy`

Optional (advertised via caps):

- multi-document output
- provider-specific `options_json`
- `last_error_utf8`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_data_serde_emit_v0.h`
- `abi/profiles/obi_data_serde_events_v0.h` (shared event struct)
- `abi/obi_core_v0.h` (writer type)

---

## Global Q&A

**Q: Why not emit an AST instead of events?**  
Events are easier to stream across FFIs, avoid host/provider memory ownership issues, and can be
generated incrementally without building a full in-memory tree.

