# OBI 3D Rendering Profile
## OBI Profile: `obi.profile:gfx.render3d-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:gfx.render3d-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile defines a minimal 3D rendering surface suitable for tools and POCs:

- begin/end a frame targeting a window
- set camera (view/projection matrices)
- create/destroy meshes and textures
- draw meshes with transforms

Typical providers:

- raylib 3D wrappers
- a small OpenGL/Vulkan renderer wrapped behind an OBI provider

This profile is intentionally higher-level than a GPU API. For lower-level control, pair it with
`obi.profile:gfx.gpu_device-0` (portable GPU device profile).

---

## 2. Technical Details

### 2.1 Coordinate system

3D coordinates and matrices are host-defined. The ABI uses float matrices and vectors; providers
must document whether they assume right-handed vs left-handed conventions.

### 2.2 Resources and ownership

Meshes, textures, and materials are provider-owned IDs. IDs are scoped to the provider instance.

Input vertex/index data passed to create calls is borrowed for the duration of the call only.

---

## 3. Conformance

Required:

- `begin_frame` / `end_frame`
- mesh create/destroy
- texture create/destroy
- `set_camera`
- `draw_mesh`

Optional (advertised via caps):

- indexed meshes
- per-material textures
- debug line drawing

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_gfx_render3d_v0.h`
- `abi/profiles/obi_gfx_types_v0.h`
- `abi/profiles/obi_geom_types_v0.h`

---

## Global Q&A

**Q: Why have both render3d and gpu_device?**  
Because many tools need "just enough 3D" without adopting a full GPU abstraction. `render3d` can
be implemented by simple engines, while `gpu_device` is for hosts that need more control.

