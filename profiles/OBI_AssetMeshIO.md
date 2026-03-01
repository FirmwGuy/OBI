# OBI Asset Mesh IO Profile
## OBI Profile: `obi.profile:asset.mesh_io-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:asset.mesh_io-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes importing triangle meshes from common asset formats so hosts can swap
mesh loading backends without rewriting glue code.

Typical providers:

- tinyobjloader / obj loaders
- cgltf / tinygltf loaders (mesh-only path)
- assimp (when used specifically for mesh extraction)

This profile is intentionally scoped to:

- positions + optional normals + optional UVs
- optional triangle indices

Materials, animations, and full scene graphs are handled by `obi.profile:asset.scene_io-0`.

---

## 2. Technical Details

### 2.1 Canonical output

Meshes are exposed as canonical CPU arrays:

- positions: `obi_vec3f_v0` (required)
- normals: `obi_vec3f_v0` (optional)
- uvs: `obi_vec2f_v0` (optional)
- indices: `uint32_t` (optional)

The host is responsible for uploading to GPU buffers (via `gfx.gpu_device` or `gfx.render3d`) or
for further processing.

### 2.2 Ownership and buffer sizing

Mesh arrays are copied into host-provided buffers. Functions follow standard OBI sizing rules:

- if dst is NULL or cap is 0, the provider returns OK and sets the required count
- if cap is too small, the provider returns `OBI_STATUS_BUFFER_TOO_SMALL` and sets required count

---

## 3. Conformance

Required:

- open from reader
- asset: mesh count, mesh info, positions getter, destroy

Optional (advertised via caps):

- open from bytes
- normals/uv arrays
- indices

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_asset_mesh_io_v0.h`
- `abi/profiles/obi_geom_types_v0.h`

---

## Global Q&A

**Q: Why not include tangents, colors, skinning, etc.?**  
Because those features are not universally present and quickly bloat the ABI. Add them as optional
capability extensions once multiple providers need the same stable contract.

