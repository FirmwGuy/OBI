# OBI GPU Device Profile
## OBI Profile: `obi.profile:gfx.gpu_device-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:gfx.gpu_device-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile defines a portable GPU device interface that can be implemented by multiple
backends:

- OpenGL / OpenGL ES
- Vulkan
- Metal
- Direct3D

The intent is not to mirror any one API, but to standardize a small "render pass + pipeline +
bindings + draw" surface that works across them (similar in spirit to sokol-gfx or WebGPU's
higher-level model).

This profile is suitable for hosts that need:

- explicit GPU resource management
- custom shaders/pipelines
- efficient batched rendering

For hosts that only need "just enough 3D" for tools, prefer `obi.profile:gfx.render3d-0`.

---

## 2. Technical Details

### 2.1 Frame model

Rendering targets a window swapchain via begin/end frame calls. A frame contains one or more
passes.

The window ID passed to begin/end frame is provider-instance-local. Hosts MUST assume it came from
`obi.profile:gfx.window_input-0` on the same provider instance unless the selected provider
explicitly documents a cross-provider bridge.

### 2.2 Shaders

Shader formats vary across ecosystems. This profile supports multiple formats via capability bits
(GLSL, SPIR-V, WGSL, etc.).

Hosts should ship shaders in formats compatible with their selected provider.

### 2.3 Ownership and lifetimes

GPU objects are provider-owned IDs. IDs are scoped to the provider instance.

Inputs to create/update calls are borrowed for the duration of the call only.

---

## 3. Conformance

Required:

- frame begin/end
- buffer/image creation and updates
- pipeline binding and draw calls

Optional (advertised via caps):

- additional shader formats
- MSAA, advanced depth/stencil modes, etc.

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_gfx_gpu_device_v0.h`
- `abi/profiles/obi_gfx_types_v0.h`
- `abi/profiles/obi_geom_types_v0.h`

---

## Global Q&A

**Q: Why not just use Vulkan everywhere?**  
Because many hosts want to remain portable and keep optional dependencies. This profile makes it
possible to choose a backend at runtime while keeping a stable integration contract.
