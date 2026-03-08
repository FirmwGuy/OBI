# OBI Data URI Profile
## OBI Profile: `obi.profile:data.uri-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:data.uri-0`  
**Status:** Draft  
**Last Updated:** 2026-03-06

---

## 1. Nontechnical Summary

This profile standardizes practical URI handling for hosts that need to:

- parse a URI into components
- normalize URI text without committing to a specific library
- parse query parameters while preserving order and duplicates
- perform UTF-8 percent-encoding/decoding for common URI components
- optionally resolve relative references against a base URI

Typical providers:

- uriparser
- GLib `GUri`

This profile is intentionally scoped to RFC 3986-style URI handling plus optional IRI-like UTF-8
decoding. It is not a full browser URL standard.

---

## 2. Technical Details

### 2.1 Component model

`parse_utf8` returns the standard URI pieces:

- scheme
- userinfo
- host
- port
- path
- query
- fragment

Returned components preserve URI syntax. In particular, percent-encoding is preserved rather than
automatically decoded.

`host` excludes userinfo, port delimiters, and enclosing IPv6 literal brackets. `port == -1`
indicates that no explicit port was present.

### 2.2 Query parameter model

`query_items_utf8` parses a raw query component into ordered key/value pairs:

- duplicate keys are preserved
- original order is preserved
- `has_value == 0` distinguishes `?flag` from `?flag=`

The input is the raw query string without the leading `?` unless
`OBI_URI_QUERY_ALLOW_LEADING_QMARK` is set.

### 2.3 Percent encoding and UTF-8

`percent_encode_utf8` and `percent_decode_utf8` operate on UTF-8 text.

Rules:

- invalid `%xx` escapes are errors
- decoded bytes that are not valid UTF-8 are errors
- component-specific escaping rules are selected via `obi_uri_component_kind_v0`

When `OBI_URI_CAP_FORM_URLENCODED` is advertised, providers support the common
`application/x-www-form-urlencoded` convention where `+` is treated as a space in query
key/value contexts via `OBI_URI_PERCENT_SPACE_AS_PLUS`.

When `OBI_URI_CAP_IRI_UTF8` is advertised, providers commit to round-tripping UTF-8 through
percent-decoded URI components for IRI-like usage.

### 2.4 Normalization and resolution

`normalize_utf8` performs syntax-preserving normalization suitable for policy/comparison tasks.
Providers SHOULD, at minimum:

- case-normalize scheme and host
- canonicalize percent-escape hex digits
- remove dot-segments where RFC 3986 resolution rules permit

Providers MUST preserve query parameter order and MUST NOT reorder semantically significant
components.

When `OBI_URI_CAP_RESOLVE` is advertised, `resolve_utf8` resolves a relative reference against a
base URI using RFC 3986 reference-resolution rules.

### 2.5 Ownership

- Input views are borrowed for the duration of the call only.
- Returned strings, parsed URI structs, and query-item lists are provider-owned and released via
  their `release` callback.

---

## 3. Conformance

Required:

- `parse_utf8`
- `normalize_utf8`
- `query_items_utf8`
- `percent_encode_utf8`
- `percent_decode_utf8`

Optional (advertised via caps):

- relative URI resolution (`resolve_utf8`)
- `+`/space query-form handling (`OBI_URI_CAP_FORM_URLENCODED`)
- UTF-8 IRI-oriented decoding guarantees (`OBI_URI_CAP_IRI_UTF8`)

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_data_uri_v0.h`

---

## Global Q&A

**Q: Why not use browser-style URL semantics here?**  
Those semantics are useful, but they are not the common denominator across `uriparser`, GLib
`GUri`, system libraries, and non-browser runtimes. Keep v0 on portable URI rules.

**Q: Why are parsed components returned without automatic percent-decoding?**  
Because hosts often need the raw syntax for comparison, reserialization, or policy decisions.
Decoding is explicit so ownership and UTF-8 error handling stay clear.

