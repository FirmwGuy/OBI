# OBI Media Video Scale/Convert Profile
## OBI Profile: `obi.profile:media.video_scale_convert-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:media.video_scale_convert-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal interface for:

- scaling video frames (resize)
- converting pixel formats (RGBA/BGRA/RGB and common YUV formats)

Typical providers:

- FFmpeg `libswscale` wrappers
- `libyuv` wrappers

This profile is useful in ingest/export pipelines, previews, and tooling where a stable "image
conversion" surface is needed.

---

## 2. Technical Details

### 2.1 Scaler model

The host creates a scaler for a fixed input format and output format (`obi_video_format_v0`).

The host then calls `convert` repeatedly with per-frame plane pointers and strides.

### 2.2 Packed vs planar buffers

For packed formats (RGBA8/BGRA8/RGB8/A8):

- use `planes[0]` only
- `planes[0].stride_bytes` is bytes per row

For planar YUV formats:

- **I420:** `planes[0]=Y`, `planes[1]=U`, `planes[2]=V`  
  Y plane is `width x height` bytes. U/V planes are `(width/2) x (height/2)` bytes.
- **NV12:** `planes[0]=Y`, `planes[1]=UV` (interleaved chroma)  
  Y plane is `width x height` bytes. UV plane is `width x (height/2)` bytes.

Providers MUST document any additional alignment/stride requirements beyond these minima.

### 2.3 Ownership

All input/output buffers are host-owned and borrowed for the duration of each call only.

---

## 3. Conformance

Required:

- create scaler
- `convert`
- destroy

Optional (advertised via caps):

- additional pixel formats
- provider-specific `options_json` (for quality, dithering, colorspace details, etc.)

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_media_video_scale_convert_v0.h`
- `abi/profiles/obi_media_types_v0.h`

---

## Global Q&A

**Q: Why not standardize GPU scaling here (OpenGL/Vulkan)?**  
This profile is CPU-buffer oriented. GPU paths belong in gfx/GPU profiles (or a dedicated media GPU
inter-op profile) to avoid mixing concerns.

