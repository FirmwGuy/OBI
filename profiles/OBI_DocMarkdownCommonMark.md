# OBI Markdown (CommonMark) Profile
## OBI Profile: `obi.profile:doc.markdown_commonmark-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:doc.markdown_commonmark-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes parsing Markdown into a structured representation.

Typical providers:

- cmark / cmark-gfm (CommonMark family)
- md4c

This profile is intentionally focused on parsing. Rendering (to HTML, to layout blocks) can be
added as optional capabilities or separate profiles.

---

## 2. Technical Details

### 2.1 Input

Markdown input is UTF-8 (`obi_utf8_view_v0`).

### 2.2 Output

v0 uses JSON output to keep the ABI small while still returning rich structure.

The provider writes an UTF-8 JSON document to an OBI writer. The JSON schema is provider-defined
but SHOULD be stable within provider versions (for host tooling).

### 2.3 Ownership

Inputs are borrowed for the duration of the call.

The provider borrows the writer for the duration of the call and must not destroy it.

---

## 3. Conformance

Required:

- `parse_to_json_writer`

Optional (advertised via caps):

- render HTML
- provider-specific parse options JSON

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_doc_markdown_commonmark_v0.h`

---

## Global Q&A

**Q: Why JSON instead of an AST ABI?**  
AST ABIs tend to be large and hard to keep stable across languages. JSON keeps v0 implementable.
If multiple hosts need a typed AST, a future profile can standardize it.

