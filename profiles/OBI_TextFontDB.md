# OBI Text Font DB Profile
## OBI Profile: `obi.profile:text.font_db-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:text.font_db-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes system font discovery and font fallback so hosts can:

- match fonts by family/style
- select fallback fonts for specific Unicode codepoints
- obtain a font source (bytes or file path) suitable for loading faces in
  `obi.profile:text.raster_cache-0` and `obi.profile:text.shape-0`

Typical providers:

- fontconfig (Linux)
- CoreText (macOS)
- DirectWrite (Windows)

---

## 2. Technical Details

### 2.1 Font sources

Font matches return a `obi_font_source_v0` which may provide:

- font bytes (provider-owned), or
- a UTF-8 file path to the font on disk, plus face index for collections (TTC/OTC)

Providers advertise which source kinds are supported via capability bits.

The portable interop contract for split text providers is `font bytes + face_index`. If a font DB
provider returns a file path, the host may read that file into bytes and pass the bytes into face
creation APIs exposed by rasterization/shaping providers.

### 2.2 Fallback

Hosts may specify a `codepoint` to request a font capable of rendering that character.

Providers MAY ignore fallback hints if unsupported, but must report caps honestly.

### 2.3 Ownership and determinism notes

Font source outputs are provider-owned and released via `release(...)`.

Deterministic hosts should treat system font selection as an environmental dependency and may
prefer shipping font assets (load via `text.raster_cache` from bytes) for strict reproducibility.

---

## 3. Conformance

Required:

- `match_face`

Optional (advertised via caps):

- return bytes
- return file paths
- match by codepoint fallback hints

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_text_font_db_v0.h`

---

## Global Q&A

**Q: Why not return face IDs directly?**  
Face IDs are provider-scoped objects created by consumer profiles such as `text.raster_cache` or
`text.shape`. This profile focuses on font selection and source discovery; hosts request a font
source and then create provider-local faces in the consumer profiles they actually use.
