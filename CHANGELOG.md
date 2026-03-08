# Changelog
## Omni Backstage Interface (OBI) Specification Documents

**Document Type:** Changelog  
**Status:** Draft  
**Last Updated:** 2026-03-08

---

This file tracks notable changes to the specification documents in this repository.

The canonical spec version is defined in `OBI.md`.

## [Unreleased]

### Added

- Added FAQ and provider guidance docs (`OBI_FAQ.md`, `OBI_PROVIDER_GUIDE.md`)
- Added legal-selection guidance doc (`OBI_LEGAL_SELECTION.md`) covering module-vs-effective
  license, dependency closure, route-sensitive backends, and preset selectability rules
- Added ABI conventions and conformance guidance docs
- Added a profile inventory index (`profiles/INDEX.md`)
- Added normative ABI headers for window/input and text profiles
- Expanded `net.http_client` profile with extended request entrypoints (`request_ex`)
- Extended `gfx.render2d` ABI with optional `begin_frame/end_frame` window targeting
- Added data profiles for compression and archive containers
- Added database profiles for transactional KV and SQL backends (LMDB/SQLite-style)
- Added media profiles for image codecs, audio device I/O, and A/V decoding
- Added an A/V encoding profile (frame-in / packet-out)
- Added media container and processing profiles (demux/mux, audio mix/resample, video scale/convert)
- Extended shared media types with basic audio/video format structs and planar YUV buffer layouts
- Added math profiles for BigInt, BigFloat, and a BLAS subset
- Added a websocket client profile
- Added a TLS session profile (OpenSSL/GNUTLS/mbedTLS-style)
- Added DNS and socket profiles plus shared net address types
- Added a crypto hash profile
- Added crypto profiles for CSPRNG, AEAD encryption, signing, and KDFs
- Added a decimal arithmetic profile (mpdecimal-style)
- Added a small scientific-ops profile (special functions, GSL-like)
- Added a file type detection profile (libmagic-style)
- Added text segmentation, font DB, and text layout profiles
- Added an IME composition profile for complex text input events
- Added 2D/3D physics world profiles and a physics debug draw profile
- Added a portable GPU device profile and a minimal 3D rendering profile
- Added shared gfx/geometry ABI headers and removed duplicate window-id typedefs between gfx profiles
- Added a core waitset profile for OS-level waitable integration with pump-driven providers
- Added core cancellation token support and a cancel-source profile
- Added an OS filesystem profile (open/read/write/stat/mkdir/remove/rename, optional directory iteration)
- Added an OS environment profile (env vars, cwd, portable known directories)
- Added an OS process profile (spawn, wait, optional stdio pipes and env/cwd overrides)
- Added an OS dynamic library profile (dlopen/dlsym style)
- Added an OS filesystem watch profile (inotify/FSEvents/ReadDirectoryChangesW-style)
- Added document profiles for deep inspection, text decoding, markdown parsing, and paged document rasterization
- Added event-based parser profiles for markup (XML/HTML), markdown, and structured data (JSON/YAML/TOML)
- Added an event-based structured data emitter profile (JSON/YAML/TOML output)
- Added a spellcheck profile (aspell/hunspell/enchant-style)
- Added asset import profiles for meshes and scenes (OBJ/glTF/assimp-style integrations)
- Added tooling to keep mirrored ABI headers in sync with the canonical `OBI-ABI` repository

### Changed

- Expanded provider metadata guidance to separate copyleft severity from patent posture and to
  standardize provider-wide vs route-specific legal facts for hosts/runtimes that need legal
  selection plans
- Clarified that `obi_window_id_v0` is a provider-instance-local handle by default across
  `gfx.window_input-0`, `gfx.gpu_device-0`, and `gfx.render3d-0`; cross-provider window-handle
  interop now requires an explicit future contract or provider-documented bridge.
- Clarified that `obi_text_face_id_v0` is provider-local and must not be exchanged across text
  providers as if it were globally portable.
- Defined the split text-provider interoperability contract around `font bytes + face_index`,
  allowing `text.font_db-0` sources to be consumed independently by `text.raster_cache-0` and
  `text.shape-0` without sharing raw face IDs.
- Documented optional face-loading support in `text.shape-0` so shaping and rasterization providers
  may load equivalent provider-local faces from the same source bytes.
- Clarified that shaped `glyph_index` values refer to the loaded font face's glyph numbering rather
  than provider-private remapped handles.
- Clarified that `text.layout-0` remains a same-provider composition surface in v0 even though
  split shaping+rasterization interop is now defined separately.
- Expanded provider guidance with concrete provider-local handle examples (`obi_window_id_v0`,
  `obi_text_face_id_v0`) to prevent accidental cross-provider assumptions.

## [0.1.0] - 2026-03-01

### Added

- Initial OBI core spec (`OBI.md`)
- Initial profile guide (`OBI_Profiles.md`)
- Initial profile set under `profiles/` (CorePump, GfxRender2D, NetHTTPClient, stubs for WindowInput/Text)
- Initial reference ABI headers under `abi/`
- Markdown hygiene checker (`tools/check_docs.py`)
