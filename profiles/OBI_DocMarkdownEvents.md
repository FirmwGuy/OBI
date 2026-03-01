# OBI Doc Markdown Events Profile
## OBI Profile: `obi.profile:doc.markdown_events-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:doc.markdown_events-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes an event-based markdown parser interface:

- parse a UTF-8 markdown document
- iterate a stream of enter/exit events for markdown nodes

Typical providers:

- cmark (CommonMark) wrappers
- markdown-it style engines (when exposed via a stable C ABI)

This profile is intentionally not a DOM/AST API. Hosts can build their own ASTs, renderers, or
conversion pipelines on top of the event stream.

---

## 2. Technical Details

### 2.1 Event model

The parser yields `obi_md_event_v0` records with:

- an event kind: `ENTER` or `EXIT`
- a node kind (document, paragraph, heading, link, text, etc.)
- optional literal text for leaf nodes (text/code/html/code-block)
- optional attribute key/value list for `ENTER` events

Providers SHOULD emit a well-nested tree traversal:

- `ENTER DOCUMENT`
- ...
- `EXIT DOCUMENT`

### 2.2 Attributes

Attributes are expressed as key/value strings so v0 stays small.

Common (non-normative) attribute keys:

- heading: `level`
- link/image: `url`, `title`
- list: `ordered`, `start`, `tight`
- code block: `info`

### 2.3 Location (optional)

When supported, providers include:

- byte offset from the start of the markdown input
- 1-based line and column

If location is not supported, providers MUST set location fields to 0.

### 2.4 Ownership

The input markdown buffer is borrowed for the duration of `parse_utf8` only.

All literal/attribute views returned in events are provider-owned and have short lifetimes; hosts
MUST copy data they need to keep.

---

## 3. Conformance

Required:

- parse to an event parser
- iterate events (`next_event`)
- destroy parser

Optional (advertised via caps):

- provider-specific `options_json`
- location reporting
- `last_error_utf8`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_doc_markdown_events_v0.h`

---

## Global Q&A

**Q: Why is this separate from `doc.markdown_commonmark-0`?**  
`doc.markdown_commonmark` standardizes a JSON/HTML output surface. This profile standardizes a
parser event stream so hosts can build their own representations without adopting a provider’s JSON
schema.

