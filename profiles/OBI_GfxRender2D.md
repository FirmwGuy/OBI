# OBI 2D Rendering Profile
## OBI Profile: `obi.profile:gfx.render2d-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:gfx.render2d-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Purpose

This profile defines a minimal 2D rendering surface for GUI and tooling:

- textures (create/update/destroy),
- scissor (clip),
- solid rectangles,
- textured quads (enough to render a glyph atlas).

This profile intentionally avoids text shaping/rasterization. Text is expected to be rendered by
building a glyph atlas and drawing quads.

---

## 2. Coordinate System

- Coordinates are in framebuffer pixels (float values allowed for subpixel placement).
- The origin is top-left.

---

## 3. Conformance

Required:

- texture create/update/destroy for RGBA8
- scissor enable/disable
- draw rect filled
- draw textured quad

Optional capabilities are reported via the profile capability bitset.

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_gfx_render2d_v0.h`

