# OBI Text Regex Profile
## OBI Profile: `obi.profile:text.regex-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:text.regex-0`  
**Status:** Draft  
**Last Updated:** 2026-03-06

---

## 1. Nontechnical Summary

This profile standardizes a compiled regular-expression interface for UTF-8 text:

- compile a pattern once
- test/match against UTF-8 input
- retrieve capture spans
- iterate matches from a given byte offset
- perform replacement with explicit substitution syntax

Typical providers:

- PCRE2
- Oniguruma

This profile is for text search, token extraction, validation, and editor/tooling workflows. It is
not intended to standardize every engine-specific regex extension.

---

## 2. Technical Details

### 2.1 UTF-8 model

Patterns and haystacks are UTF-8 byte strings.

Rules:

- invalid UTF-8 input is an error
- match start offsets supplied by the host must be at UTF-8 codepoint boundaries
- returned spans are byte offsets into the original haystack

`spans[0]` is the whole match. Subsequent spans correspond to capture groups in left-to-right
order. Unmatched optional captures set `matched == 0`.

### 2.2 Compile and match flags

The profile standardizes a small cross-engine flag set:

- case-insensitive
- multiline
- dotall
- extended/free-spacing
- anchored

Providers MAY support richer engine-specific features internally, but hosts can only rely on the
portable flag surface documented in the ABI.

### 2.3 Replacement syntax

`replace_utf8` uses a portable substitution syntax:

- `$0` for the whole match
- `$1` through `$99` for numbered captures
- `$$` for a literal dollar sign
- `${name}` for named captures when `OBI_REGEX_CAP_NAMED_CAPTURES` is advertised

When `OBI_REGEX_REPLACE_LITERAL` is set, replacement text is copied literally and no substitutions
are interpreted.

### 2.4 Unicode properties

When `OBI_REGEX_CAP_UNICODE_PROPERTIES` is advertised, providers support engine/property features
that depend on Unicode category/property tables (for example `\p{Letter}`-class matching).

Hosts must not assume those features are present unless the cap is set.

### 2.5 Ownership

- Pattern and haystack inputs are borrowed for the duration of each call only.
- Compiled regex handles are provider-owned and released by `destroy`.
- Capture spans are written into host-provided arrays using the standard OBI sizing pattern.

---

## 3. Conformance

Required:

- `compile_utf8`
- regex `group_count`
- regex `match_utf8`
- regex `find_next_utf8`
- regex `replace_utf8`
- regex `destroy`

Optional (advertised via caps):

- named capture lookup (`capture_name_to_index`)
- Unicode property/class support (`OBI_REGEX_CAP_UNICODE_PROPERTIES`)

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_text_regex_v0.h`

---

## Global Q&A

**Q: Why return capture spans instead of copied substrings?**  
Spans avoid unnecessary allocation, preserve exact source slicing, and are easy to use from
multiple FFIs.

**Q: Why not standardize every PCRE/Oniguruma extension?**  
Because that would turn the profile into an engine clone. v0 standardizes the useful common
denominator and exposes richer behavior only through explicit caps.

