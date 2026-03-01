# Changelog
## Omni Backstage Interface (OBI) Specification Documents

**Document Type:** Changelog  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

This file tracks notable changes to the specification documents in this repository.

The canonical spec version is defined in `OBI.md`.

## [Unreleased]

### Added

- Added FAQ and provider guidance docs (`OBI_FAQ.md`, `OBI_PROVIDER_GUIDE.md`)
- Added ABI conventions and conformance guidance docs
- Added a profile inventory index (`profiles/INDEX.md`)
- Added normative ABI headers for window/input and text profiles
- Expanded `net.http_client` profile with extended request entrypoints (`request_ex`)
- Extended `gfx.render2d` ABI with optional `begin_frame/end_frame` window targeting
- Added data profiles for compression and archive containers
- Added database profiles for transactional KV and SQL backends (LMDB/SQLite-style)
- Added media profiles for image codecs, audio device I/O, and A/V decoding
- Added media container and processing profiles (demux/mux, audio mix/resample, video scale/convert)
- Extended shared media types with basic audio/video format structs and planar YUV buffer layouts
- Added math profiles for BigInt, BigFloat, and a BLAS subset
- Added a websocket client profile
- Added a TLS session profile (OpenSSL/GNUTLS/mbedTLS-style)
- Added a crypto hash profile
- Added crypto profiles for CSPRNG, AEAD encryption, signing, and KDFs
- Added a decimal arithmetic profile (mpdecimal-style)
- Added a small scientific-ops profile (special functions, GSL-like)
- Added a file type detection profile (libmagic-style)
- Added text segmentation, font DB, and text layout profiles
- Added 2D/3D physics world profiles and a physics debug draw profile
- Added a portable GPU device profile and a minimal 3D rendering profile
- Added shared gfx/geometry ABI headers and removed duplicate window-id typedefs between gfx profiles
- Added a core waitset profile for OS-level waitable integration with pump-driven providers
- Added document profiles for deep inspection, text decoding, markdown parsing, and paged document rasterization
- Added a spellcheck profile (aspell/hunspell/enchant-style)
- Added asset import profiles for meshes and scenes (OBJ/glTF/assimp-style integrations)

## [0.1.0] - 2026-03-01

### Added

- Initial OBI core spec (`OBI.md`)
- Initial profile guide (`OBI_Profiles.md`)
- Initial profile set under `profiles/` (CorePump, GfxRender2D, NetHTTPClient, stubs for WindowInput/Text)
- Initial reference ABI headers under `abi/`
- Markdown hygiene checker (`tools/check_docs.py`)
