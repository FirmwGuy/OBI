# OBI Text Shape Profile
## OBI Profile: `obi.profile:text.shape-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:text.shape-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes Unicode text shaping:

- UTF-8 input text
- glyph indices + per-glyph positioning output
- optional bidi paragraph segmentation

It is intended to be implemented by HarfBuzz-style shapers (often with FriBidi for bidi analysis).

This profile does not rasterize glyphs or manage atlases. Pair it with
`obi.profile:text.raster_cache-0` for rasterization and `obi.profile:gfx.render2d-0` for drawing.

---

## 2. Technical Details

### 2.1 Inputs and face identity

Shaping requires a font face. OBI represents faces as opaque provider-owned IDs (`obi_text_face_id_v0`).

Face IDs are only meaningful within the provider instance that created them. Hosts should obtain
faces from the text raster/cache profile (or a future dedicated font-face profile).

### 2.2 Shaping output

The core output is a sequence of glyph records:

- `glyph_index`: provider font glyph index
- `cluster`: byte offset into the input UTF-8
- `x_advance/y_advance`: pen advances in pixels
- `x_offset/y_offset`: per-glyph offsets in pixels

This output is suitable for:

- layout engines (advance sums, cluster mapping),
- renderers that draw glyph bitmaps via a texture atlas.

### 2.3 Direction, script, language, and features

The shaping call accepts:

- direction hint (LTR/RTL/AUTO),
- optional script tag (ISO 15924),
- optional language tag (BCP47),
- optional OpenType feature string (when supported).

Providers MUST document which of these inputs are honored and which are ignored.

### 2.4 Bidi paragraph segmentation (optional)

When supported, providers may expose bidi paragraph run segmentation:

- input: paragraph UTF-8 and a base direction hint
- output: a list of byte ranges with resolved direction (LTR/RTL)

Hosts can then shape each run independently with appropriate direction.

---

## 3. Conformance

Required:

- `shape_utf8`

Optional (advertised via caps):

- `bidi_paragraph_runs_utf8`
- language tags
- OpenType feature strings

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_text_shape_v0.h`

---

## Global Q&A

**Q: Does this guarantee identical shaping across providers?**  
No. Shaping output can differ between engines and versions. OBI standardizes the interface, not
the typography. Deterministic hosts should treat the provider + version as part of the execution
environment and record outputs when replay requires it.

**Q: Where does line breaking live?**  
Line breaking and text layout are host responsibilities (PRAXIS/layout engine). This profile only
shapes glyph runs.

