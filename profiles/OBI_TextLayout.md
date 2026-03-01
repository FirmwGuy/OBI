# OBI Text Layout Profile
## OBI Profile: `obi.profile:text.layout-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:text.layout-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes paragraph layout ("text flow"):

- line wrapping given a maximum width
- line metrics (baseline, ascender/descender, line height)
- positioned glyph output suitable for rasterization + atlas rendering

Typical providers:

- Pango (HarfBuzz + FriBidi + fontconfig stack)
- Skia text layout wrappers
- custom layout engines

This profile is intended to work with:

- `obi.profile:text.shape-0` and `obi.profile:text.segmenter-0` (optional building blocks)
- `obi.profile:text.raster_cache-0` for glyph rasterization
- `obi.profile:gfx.render2d-0` for drawing a glyph atlas

---

## 2. Technical Details

### 2.1 Face identity and provider composition

This profile references `obi_text_face_id_v0` in its style spans. Face IDs are provider-owned and
typically created by the same provider via `obi.profile:text.raster_cache-0`.

Hosts should expect to choose one provider that implements:

- `text.font_db` (optional)
- `text.raster_cache`
- `text.shape` (optional)
- `text.layout`

### 2.2 Coordinate system

Positions are returned in pixels in a y-down coordinate system with origin at the paragraph
top-left.

Glyph placement coordinates (`x`, `y`) are baseline pen positions suitable for use with the
`text.raster_cache` bitmap bearing fields (`bitmap_left`, `bitmap_top`).

### 2.3 Buffer sizing

The paragraph object returns lines and glyphs via buffer-sized getters that follow the standard
OBI sizing rules (query count first, then allocate).

---

## 3. Conformance

Required:

- `paragraph_create`
- paragraph getters: `get_metrics`, `get_lines`, `get_glyphs`
- paragraph `destroy`

Optional (advertised via caps):

- multi-span styling
- bidi-aware layout
- alignment modes

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_text_layout_v0.h`
- `abi/profiles/obi_text_types_v0.h`

---

## Global Q&A

**Q: Why not return a GPU-ready glyph atlas?**  
Atlas policy depends on host memory budgets and caching rules. This profile returns positioned
glyphs; the host packs glyph bitmaps into an atlas and draws quads via `gfx.render2d`.

