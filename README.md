# Omni Backstage Interface (OBI)
## Runtime Profiles for Modular Execution Paths in the TCA Stack

**Repository:** OBI  
**Document Type:** Repository overview (informative)  
**Status:** Experimental / Proposed Standard  
**Last Updated:** 2026-03-01

---

Omni Backstage Interface (OBI) is a draft specification for **versioned runtime interfaces**
("profiles") used to integrate third-party libraries behind stable, swappable provider
boundaries.

OBI complements:

- **OGIF** (frontstage membrane): declarative graph introspection + control contracts across
  transports.
- **CEP / PRAXIS** (execution): deterministic scheduling, storage, and higher-layer systems.

OBI is the *backstage* contract: imperative, handle-based, capability-negotiated interfaces for
modules that need to swap implementations at runtime (SDL vs raylib, curl vs libsoup, ffmpeg vs
gstreamer, etc.).

### Start Here

- `OBI.md` - OBI Core specification (v0.1.0 draft)
- `OBI_Profiles.md` - Profile guide (informative companion)
- `OBI_FAQ.md` - FAQ (informative companion)
- `OBI_PROVIDER_GUIDE.md` - Provider authoring/packaging guidance (informative companion)
- `profiles/` - Individual profile specifications and extensions
- `abi/` - Reference C headers (normative ABI shapes)

### Repo Hygiene

- Validate Markdown invariants: `python3 tools/check_docs.py`
  - UTF-8, LF-only newlines
  - Balanced triple-backtick code fences
  - Presence of self-describing doc headers (e.g., `**Last Updated:**`)

### License

Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0), same as the TCA and
OGIF projects. See `LICENSE`.
