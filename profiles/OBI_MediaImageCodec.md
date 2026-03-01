# OBI Media Image Codec Profile
## OBI Profile: `obi.profile:media.image_codec-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:media.image_codec-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes decoding and encoding common image formats without locking the host to a
single library.

Typical providers:

- stb_image / stb_image_write
- libpng, libjpeg-turbo, libwebp, etc.
- libvips / ImageMagick frontends (when used as a codec service)

The output is a CPU pixel buffer suitable for:

- immediate use (save/transform),
- upload to a GPU via `obi.profile:gfx.render2d-0` textures.

---

## 2. Technical Details

### 2.1 Decode inputs

Decoding supports:

- decode from bytes (required)
- decode from an OBI reader (optional)

Providers SHOULD auto-detect image formats from magic bytes. Hosts MAY pass a `format_hint` to help
or to select behavior when auto-detection is unavailable.

### 2.2 Pixel formats and color

The profile uses shared media types:

- pixel formats: `obi_pixel_format_v0` (RGBA8/BGRA8/RGB8/A8)
- color spaces: `obi_color_space_v0` (sRGB/linear/unknown)
- alpha modes: `obi_alpha_mode_v0` (straight/premultiplied/opaque/unknown)

Providers SHOULD default to `RGBA8` output for general use unless a preferred format is requested.

### 2.3 Ownership

Decoded pixels are provider-owned and released via the `obi_image_v0.release(...)` callback.

Encoders borrow host-owned pixel pointers for the duration of the encode call only.

### 2.4 Encoding

Encoding writes to an OBI writer (so large images need not be fully buffered).

The `codec_id` string selects the output format (examples: `png`, `jpeg`, `webp`).

---

## 3. Conformance

Required:

- `decode_from_bytes`

Optional (advertised via caps):

- `decode_from_reader`
- `encode_to_writer`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_media_image_codec_v0.h`
- `abi/profiles/obi_media_types_v0.h`

---

## Global Q&A

**Q: Why not standardize EXIF, ICC, metadata, animated formats, etc.?**  
OBI profiles stay minimal and portable. Advanced features can be added via capabilities or
separate profiles once multiple providers need the same contract.

**Q: Why not GPU textures directly?**  
GPU interop is backend-dependent. OBI keeps codec outputs on CPU and relies on `gfx.render2d` for
texture upload and drawing.

