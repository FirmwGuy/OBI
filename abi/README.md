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
- `profiles/obi_waitset_v0.h` - `obi.profile:core.waitset-0`
- `profiles/obi_cancel_v0.h` - `obi.profile:core.cancel-0`
- `profiles/obi_os_fs_watch_v0.h` - `obi.profile:os.fs_watch-0`
- `profiles/obi_gfx_types_v0.h` - shared gfx types (window IDs)
- `profiles/obi_geom_types_v0.h` - shared geometry types (vec/mat/color/rect)
- `profiles/obi_gfx_window_input_v0.h` - `obi.profile:gfx.window_input-0`
- `profiles/obi_gfx_render2d_v0.h` - `obi.profile:gfx.render2d-0`
- `profiles/obi_gfx_gpu_device_v0.h` - `obi.profile:gfx.gpu_device-0`
- `profiles/obi_gfx_render3d_v0.h` - `obi.profile:gfx.render3d-0`
- `profiles/obi_phys_world2d_v0.h` - `obi.profile:phys.world2d-0`
- `profiles/obi_phys_world3d_v0.h` - `obi.profile:phys.world3d-0`
- `profiles/obi_phys_debug_draw_v0.h` - `obi.profile:phys.debug_draw-0`
- `profiles/obi_text_segmenter_v0.h` - `obi.profile:text.segmenter-0`
- `profiles/obi_text_font_db_v0.h` - `obi.profile:text.font_db-0`
- `profiles/obi_text_shape_v0.h` - `obi.profile:text.shape-0`
- `profiles/obi_text_raster_cache_v0.h` - `obi.profile:text.raster_cache-0`
- `profiles/obi_text_layout_v0.h` - `obi.profile:text.layout-0`
- `profiles/obi_text_spellcheck_v0.h` - `obi.profile:text.spellcheck-0`
- `profiles/obi_doc_inspect_v0.h` - `obi.profile:doc.inspect-0`
- `profiles/obi_doc_text_decode_v0.h` - `obi.profile:doc.text_decode-0`
- `profiles/obi_doc_markup_events_v0.h` - `obi.profile:doc.markup_events-0`
- `profiles/obi_doc_markdown_commonmark_v0.h` - `obi.profile:doc.markdown_commonmark-0`
- `profiles/obi_doc_markdown_events_v0.h` - `obi.profile:doc.markdown_events-0`
- `profiles/obi_doc_paged_document_v0.h` - `obi.profile:doc.paged_document-0`
- `profiles/obi_asset_mesh_io_v0.h` - `obi.profile:asset.mesh_io-0`
- `profiles/obi_asset_scene_io_v0.h` - `obi.profile:asset.scene_io-0`
- `profiles/obi_net_http_client_v0.h` - `obi.profile:net.http_client-0`
- `profiles/obi_net_websocket_v0.h` - `obi.profile:net.websocket-0`
- `profiles/obi_net_tls_v0.h` - `obi.profile:net.tls-0`
- `profiles/obi_data_compression_v0.h` - `obi.profile:data.compression-0`
- `profiles/obi_data_archive_v0.h` - `obi.profile:data.archive-0`
- `profiles/obi_data_file_type_v0.h` - `obi.profile:data.file_type-0`
- `profiles/obi_data_serde_events_v0.h` - `obi.profile:data.serde_events-0`
- `profiles/obi_db_kv_v0.h` - `obi.profile:db.kv-0`
- `profiles/obi_db_sql_v0.h` - `obi.profile:db.sql-0`
- `profiles/obi_crypto_random_v0.h` - `obi.profile:crypto.random-0`
- `profiles/obi_crypto_hash_v0.h` - `obi.profile:crypto.hash-0`
- `profiles/obi_crypto_aead_v0.h` - `obi.profile:crypto.aead-0`
- `profiles/obi_crypto_sign_v0.h` - `obi.profile:crypto.sign-0`
- `profiles/obi_crypto_kdf_v0.h` - `obi.profile:crypto.kdf-0`
- `profiles/obi_math_bigint_v0.h` - `obi.profile:math.bigint-0`
- `profiles/obi_math_bigfloat_v0.h` - `obi.profile:math.bigfloat-0`
- `profiles/obi_math_decimal_v0.h` - `obi.profile:math.decimal-0`
- `profiles/obi_math_scientific_ops_v0.h` - `obi.profile:math.scientific_ops-0`
- `profiles/obi_math_blas_v0.h` - `obi.profile:math.blas-0`
- `profiles/obi_media_types_v0.h` - shared media enums (pixel/audio formats)
- `profiles/obi_media_image_codec_v0.h` - `obi.profile:media.image_codec-0`
- `profiles/obi_media_audio_device_v0.h` - `obi.profile:media.audio_device-0`
- `profiles/obi_media_audio_mix_v0.h` - `obi.profile:media.audio_mix-0`
- `profiles/obi_media_audio_resample_v0.h` - `obi.profile:media.audio_resample-0`
- `profiles/obi_media_demux_v0.h` - `obi.profile:media.demux-0`
- `profiles/obi_media_av_decode_v0.h` - `obi.profile:media.av_decode-0`
- `profiles/obi_media_video_scale_convert_v0.h` - `obi.profile:media.video_scale_convert-0`
- `profiles/obi_media_mux_v0.h` - `obi.profile:media.mux-0`

These headers are intended to be:

- small, portable, and FFI-friendly,
- stable within their ABI major version,
- directly usable by providers and hosts.
