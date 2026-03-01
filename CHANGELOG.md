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

## [0.1.0] - 2026-03-01

### Added

- Initial OBI core spec (`OBI.md`)
- Initial profile guide (`OBI_Profiles.md`)
- Initial profile set under `profiles/` (CorePump, GfxRender2D, NetHTTPClient, stubs for WindowInput/Text)
- Initial reference ABI headers under `abi/`
- Markdown hygiene checker (`tools/check_docs.py`)
