# OBI Text Segmenter Profile
## OBI Profile: `obi.profile:text.segmenter-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:text.segmenter-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes Unicode text segmentation and break analysis:

- grapheme cluster boundaries (cursor movement)
- word boundaries (selection, tokenization)
- sentence boundaries (optional)
- line break opportunities (wrapping)
- bidi paragraph run segmentation (optional)

Typical providers:

- ICU
- libunibreak (line/word/grapheme)
- FriBidi (bidi paragraph runs)

This profile does not shape glyphs. Pair it with `obi.profile:text.shape-0` and
`obi.profile:text.layout-0` as needed.

---

## 2. Technical Details

### 2.1 Inputs and encoding

All input text is UTF-8 (`obi_utf8_view_v0`). Break offsets are returned as byte offsets into the
same UTF-8 buffer.

### 2.2 Output model

Breaks are returned as a list of `obi_text_break_v0` records.

For grapheme/word/sentence segmentation, the `kind` field is typically `ALLOW` for all returned
boundaries. For line breaking, providers may return `MUST` breaks (for example explicit newlines).

### 2.3 Buffer sizing

All list-returning functions follow the OBI sizing rule:

- if the output pointer is NULL or cap is 0, the provider returns OK and sets the required count
- if cap is too small, the provider returns `OBI_STATUS_BUFFER_TOO_SMALL` and sets the required
  count

---

## 3. Conformance

Required:

- at least one segmentation function (providers must set caps honestly)

Optional (advertised via caps):

- grapheme boundaries
- word boundaries
- sentence boundaries
- line break opportunities
- bidi paragraph runs

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_text_segmenter_v0.h`

---

## Global Q&A

**Q: Why do we need this when HarfBuzz/FriBidi exist?**  
Because hosts often need segmentation independently of shaping (cursor movement, selection, wrap
decisions). This profile standardizes the integration mechanics so providers can be swapped.

