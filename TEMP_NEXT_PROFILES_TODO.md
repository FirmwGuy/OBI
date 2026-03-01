# TEMP: Next OBI Profiles TODO
## Temporary Checklist for Upcoming Profile Work (Remove After Completion)

**Repository:** OBI  
**Document Type:** Temporary TODO (informative)  
**Status:** Temporary / Working List  
**Last Updated:** 2026-03-01

---

This document is intentionally temporary. Once the items below are implemented (docs + ABI headers)
and wired into indices, delete this file.

## Task List

- [x] Add `obi.profile:core.waitset-0` (OS waitables/deadlines for pump integration)

- [x] Add `obi.profile:doc.inspect-0` (deep probe: canonical MIME + summary + metadata)
- [x] Add `obi.profile:doc.text_decode-0` (bytes/reader -> UTF-8 normalize + encoding detection)
- [x] Add `obi.profile:doc.markdown_commonmark-0` (markdown parse surface)
- [x] Add `obi.profile:doc.paged_document-0` (PDF/SVG-like paged docs: open, page info, rasterize; optional text extract)

- [x] Add `obi.profile:text.spellcheck-0` (aspell/hunspell/enchant-style spellcheck + suggestions)

- [x] Add `obi.profile:asset.mesh_io-0` (OBJ/glTF mesh import/export)
- [x] Add `obi.profile:asset.scene_io-0` (glTF scenes; likely OGIF-oriented output)

- [x] Add `obi.profile:media.demux-0` and `obi.profile:media.mux-0` (containers <-> packet streams)
- [x] Add `obi.profile:media.audio_mix-0` (mix N streams into one)
- [x] Add `obi.profile:media.audio_resample-0` (soxr/libsamplerate/swresample class)
- [x] Add `obi.profile:media.video_scale_convert-0` (swscale/libyuv class)

- [x] Add `obi.profile:db.kv-0` (LMDB/RocksDB transactional KV)
- [x] Add `obi.profile:db.sql-0` (SQLite-style prepare/bind/step/column)

- [x] Add `obi.profile:net.tls-0` (OpenSSL/GNUTLS/mbedTLS session/certs/ALPN)

- [ ] Add `obi.profile:crypto.random-0` (CSPRNG)
- [ ] Add `obi.profile:crypto.aead-0` (AEAD encrypt/decrypt)
- [ ] Add `obi.profile:crypto.sign-0` (sign/verify)
- [ ] Add `obi.profile:crypto.kdf-0` (HKDF/Argon2/etc via caps)

- [ ] Add `obi.profile:os.fs_watch-0` (inotify/FSEvents/ReadDirectoryChangesW)
