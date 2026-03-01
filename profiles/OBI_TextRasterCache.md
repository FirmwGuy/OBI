# OBI Text Raster Cache Profile
## OBI Profile: `obi.profile:text.raster_cache-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:text.raster_cache-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes:

- loading font faces from bytes (TTF/OTF/TTC),
- querying font metrics at a given pixel size,
- rasterizing glyph indices into bitmaps.

The "cache" in the name is intentional: providers may internally cache glyphs, but the ABI is
designed so hosts can also cache and build their own atlas strategies.

This profile does not require a GPU. It returns CPU bitmaps and metrics suitable for hosts that
pack glyphs into a texture atlas and draw quads via `obi.profile:gfx.render2d-0`.

---

## 2. Technical Details

### 2.1 Face identity

Font faces are provider-owned opaque IDs (`obi_text_face_id_v0`) created from font bytes.

Face IDs are only meaningful within the provider instance that created them.

### 2.2 Metrics

For a given face and pixel size, providers return a `obi_text_metrics_v0`:

- ascender/descender
- line gap
- recommended line height

Hosts SHOULD use these for baseline alignment and line spacing (not raw bitmap bounds).

### 2.3 Rasterization output

Rasterization returns a bitmap and positioning fields:

- bitmap format (A8 or RGBA8)
- dimensions + stride
- bearing/advance information for placing the bitmap relative to the pen position

Bitmap pixels are provider-owned. If a release callback is present, hosts MUST call it once they
finish using the bitmap.

### 2.4 Mapping codepoints to glyph indices (optional)

Some hosts want to rasterize by Unicode codepoint directly. Providers may expose a cmap lookup to
map codepoints to glyph indices.

Shaping engines typically produce glyph indices; for shaped text rendering, cmap lookup is not
required.

---

## 3. Conformance

Required:

- `face_create_from_bytes`
- `face_destroy`
- `face_get_metrics`
- `rasterize_glyph`

Optional (advertised via caps):

- cmap lookup (`face_get_glyph_index`)
- additional bitmap formats (A8 vs RGBA8)

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_text_raster_cache_v0.h`

---

## Global Q&A

**Q: Why not standardize GPU atlas management here?**  
Atlas policy is application-specific (eviction, Unicode coverage, memory budgets, stable glyph
handles). OBI keeps v0 focused on portable rasterization so hosts (CEP/PRAXIS) can implement their
own atlas and caching rules, while still allowing providers to cache internally.

**Q: Should bitmaps be premultiplied alpha?**  
For RGBA8 bitmaps, premultiplied alpha is recommended. Providers should document the exact pixel
semantics.

