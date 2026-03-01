# OBI 2D Rendering Profile
## OBI Profile: `obi.profile:gfx.render2d-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:gfx.render2d-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile defines a minimal 2D rendering surface for GUI and tooling:

- textures (create/update/destroy),
- scissor (clip),
- solid rectangles,
- textured quads (enough to render a glyph atlas).

This profile intentionally avoids text shaping/rasterization. Text is expected to be rendered by
building a glyph atlas and drawing quads.

---

## 2. Technical Details

### 2.1 Coordinate system

- Coordinates are in framebuffer pixels (float values allowed for subpixel placement).
- The origin is top-left.

---

### 2.2 Frame boundaries and presentation (optional)

OBI separates window creation from rendering, but a practical GUI baseline needs a way to present
frames.

Providers MAY implement `begin_frame/end_frame` on this profile (advertised via
`OBI_RENDER2D_CAP_WINDOW_TARGET`), where the target window ID comes from `obi.profile:gfx.window_input-0`.

If these functions are not implemented, presentation is provider-defined and must be handled by
non-OBI glue in the host (not recommended for long-term use).

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

---

## Global Q&A

**Q: Why not require begin/end frame?**  
Some render backends are already framed elsewhere, or are purely offscreen. OBI keeps it optional
but strongly recommended for interactive GUI hosts.

