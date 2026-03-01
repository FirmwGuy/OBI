# OBI ABI Artifacts
## Reference C Headers for OBI Core and Profiles

**Document Type:** Reference index (normative)  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

This directory contains reference C headers defining the normative ABI shapes used by OBI:

- `obi_core_v0.h` - core types (status codes, host/provider shape, stream helpers)
- `profiles/` - per-profile handle structs, vtables, and capability bits

Shipped profile ABIs (v0):

- `profiles/obi_pump_v0.h` - `obi.profile:core.pump-0`
- `profiles/obi_gfx_window_input_v0.h` - `obi.profile:gfx.window_input-0`
- `profiles/obi_gfx_render2d_v0.h` - `obi.profile:gfx.render2d-0`
- `profiles/obi_text_shape_v0.h` - `obi.profile:text.shape-0`
- `profiles/obi_text_raster_cache_v0.h` - `obi.profile:text.raster_cache-0`
- `profiles/obi_net_http_client_v0.h` - `obi.profile:net.http_client-0`
- `profiles/obi_net_websocket_v0.h` - `obi.profile:net.websocket-0`
- `profiles/obi_data_compression_v0.h` - `obi.profile:data.compression-0`
- `profiles/obi_data_archive_v0.h` - `obi.profile:data.archive-0`
- `profiles/obi_data_file_type_v0.h` - `obi.profile:data.file_type-0`
- `profiles/obi_crypto_hash_v0.h` - `obi.profile:crypto.hash-0`
- `profiles/obi_math_bigint_v0.h` - `obi.profile:math.bigint-0`
- `profiles/obi_math_bigfloat_v0.h` - `obi.profile:math.bigfloat-0`
- `profiles/obi_math_decimal_v0.h` - `obi.profile:math.decimal-0`
- `profiles/obi_math_scientific_ops_v0.h` - `obi.profile:math.scientific_ops-0`
- `profiles/obi_math_blas_v0.h` - `obi.profile:math.blas-0`
- `profiles/obi_media_types_v0.h` - shared media enums (pixel/audio formats)
- `profiles/obi_media_image_codec_v0.h` - `obi.profile:media.image_codec-0`
- `profiles/obi_media_audio_device_v0.h` - `obi.profile:media.audio_device-0`
- `profiles/obi_media_av_decode_v0.h` - `obi.profile:media.av_decode-0`

These headers are intended to be:

- small, portable, and FFI-friendly,
- stable within their ABI major version,
- directly usable by providers and hosts.
