# OBI Doc Markup Events Profile
## OBI Profile: `obi.profile:doc.markup_events-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:doc.markup_events-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes an event-based parser interface for markup documents:

- read a document from an `obi_reader_v0` (or optional in-memory bytes)
- iterate parse events: start/end elements, text, and attributes

Typical providers:

- libxml2 wrappers (XML)
- gumbo/lexbor wrappers (HTML)

This profile is intentionally **not** a DOM API. Hosts can build DOMs, query systems, or conversion
pipelines on top of the event stream.

---

## 2. Technical Details

### 2.1 Format selection

Hosts MAY pass a `format_hint` string such as:

- `xml`
- `html`

Providers SHOULD auto-detect when possible.

### 2.2 Event model

The parser yields a sequence of `obi_markup_event_v0` events:

- `START_ELEMENT` with element name and an attribute key/value list
- `END_ELEMENT`
- `TEXT`
- optional secondary events (comments, CDATA, processing instructions, doctype)

Attribute lists are provider-owned views valid until the next `next_event` call (or parser
destruction).

### 2.3 Location (optional)

When supported, providers include:

- byte offset from the start of the document
- 1-based line and column

If location is not supported, providers MUST set location fields to 0.

### 2.4 Ownership

The input reader is borrowed for the duration of `open_reader` only.

All string/attribute views returned in events are provider-owned and have short lifetimes; hosts
MUST copy data they need to keep.

---

## 3. Conformance

Required:

- open from reader
- iterate events (`next_event`)
- destroy parser

Optional (advertised via caps):

- open from bytes
- provider-specific `options_json`
- location reporting
- `last_error_utf8`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_doc_markup_events_v0.h`

---

## Global Q&A

**Q: Why not include XML namespaces in v0?**  
Different backends expose namespaces differently. v0 standardizes the core "tags + attributes"
surface. Namespace-aware APIs can be added later as optional expansion once hosts converge.

