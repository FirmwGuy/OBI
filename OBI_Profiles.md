# OBI Profile Guide
## Recommended Profiles for Omni Backstage Interface Deployments

**Document Type:** Informative companion (non-normative)  
**Applies To:** OBI v0.1.0 (Draft)  
**Last Updated:** 2026-03-01

---

## 1. Why Profiles Exist

OBI Core defines the *mechanics* for integrating providers (versioning, capabilities, lifetimes).
Profiles define the *domain surface*:

- GUI: windows, input, 2D rendering
- GPU/3D: portable GPU backends and minimal 3D rendering for tools
- Text: shaping (bidi/harfbuzz), glyph rasterization + host-managed atlas caching
- Documents: inspection, decoding, markdown, XML/HTML markup, PDF and other open standards
- Assets: mesh/scene import/export (OBJ/glTF/etc.)
- Networking: HTTP clients (curl/libsoup), websockets, etc.
- Crypto: hashes, CSPRNG, AEAD, signatures, and KDFs
- Media: demux/decode/filter (ffmpeg/gstreamer), resampling
- Data: DB handles/transactions (sqlite/lmdb), compression/archives, JSON/YAML/TOML parsing
- OS: filesystem watching and other platform services
- Physics: 2D/3D rigid body worlds (box2d/bullet/jolt)
- Math: big integers/float contexts (gmp/mpfr), matrix ops (lapack)

Different domains have different semantics, but most integrations fall into a few interface shapes:

- pure/stateless functions,
- stateful contexts (handles),
- streaming I/O,
- event-loop-driven services (pump),
- pipeline/graph engines.

Profiles exist so we can standardize *only what we need*, when we need it.

---

## 2. Recommended Baseline Profile Set

This section is a recommended "menu" of commonly deployed profiles. Most hosts will implement only
the profiles they need.

### Cross-cutting (strongly recommended)

1) **Core Pump** (`obi.profile:core.pump-0`)  
   A minimal "step" interface for providers that need an event loop to make progress.

2) **Core WaitSet** (`obi.profile:core.waitset-0`)  
   Optional OS-level waitable hints (fds/handles) to integrate pump-driven providers efficiently.

2b) **Core Cancel** (`obi.profile:core.cancel-0`)  
   Cancellation sources/tokens for cooperative cancellation across long-running work.

### OS baseline (optional for toolchains)

3) **Filesystem Watch** (`obi.profile:os.fs_watch-0`)  
   Watch filesystem paths and receive change events (inotify/FSEvents/ReadDirectoryChangesW class).

3b) **Filesystem** (`obi.profile:os.fs-0`)  
   Open files for streaming reads/writes, stat paths, create/remove/rename, and optionally iterate
   directories.

3c) **Environment** (`obi.profile:os.env-0`)  
   Read environment variables and query portable known directories (home/temp/config/cache/data),
   optionally set/unset variables and change the working directory.

3d) **Process** (`obi.profile:os.process-0`)  
   Spawn and supervise external processes with optional stdio pipes (toolchains, build steps,
   media pipelines).

3e) **Dynamic Libraries** (`obi.profile:os.dylib-0`)  
   Load shared libraries and lookup symbols (plugin/provider discovery).

### GUI baseline (common for tools and POCs)

4) **Window + Input** (`obi.profile:gfx.window_input-0`)  
   Window creation, event pump, input events, clipboard, DPI/framebuffer sizing.

5) **2D Render** (`obi.profile:gfx.render2d-0`)  
   Textures + scissor + rectangles + textured quads (enough to render a glyph atlas).

### GPU/3D baseline (optional for 3D tools)

6) **GPU Device** (`obi.profile:gfx.gpu_device-0`)  
   Portable GPU abstraction (OpenGL/Vulkan/Metal/D3D style backends).

7) **3D Render** (`obi.profile:gfx.render3d-0`)  
   Minimal 3D rendering for tools and POCs (meshes, textures, camera, draw).

### Text baseline (recommended once you need correct Unicode)

8) **Text Segmenter** (`obi.profile:text.segmenter-0`)  
   Unicode segmentation and break opportunities (grapheme/word/line/bidi).

9) **Font DB** (`obi.profile:text.font_db-0`)  
   System font discovery and fallback (fontconfig/CoreText/DirectWrite style).

10) **Text Shape** (`obi.profile:text.shape-0`)  
   FriBidi + HarfBuzz style shaping: UTF-8 in, glyph indices + positions out.

11) **Text Raster Cache** (`obi.profile:text.raster_cache-0`)  
   Glyph rasterization + optional internal caching. Hosts typically pack glyphs into their own atlas
   using `obi.profile:gfx.render2d-0`.

12) **Text Layout** (`obi.profile:text.layout-0`)  
    Paragraph layout and positioned glyph output ("text flow") for rendering via an atlas.

13) **Spellcheck** (`obi.profile:text.spellcheck-0`)  
    Spellchecking and suggestions (aspell/hunspell/enchant style) for editors and tooling.

### Networking baseline (needed for internet services)

14) **HTTP Client** (`obi.profile:net.http_client-0`)  
   A request/response interface with optional async/pump integration, compatible with curl/libsoup.

15) **WebSocket Client** (`obi.profile:net.websocket-0`)  
   Duplex messaging (send/receive) with optional async/pump integration.

16) **TLS Session** (`obi.profile:net.tls-0`)  
   A portable TLS client session surface for non-HTTP protocols (OpenSSL/GNUTLS/mbedTLS class).

### Crypto baseline (common for integrity and secure protocols)

17) **Random Bytes** (`obi.profile:crypto.random-0`)  
   Cryptographically secure random bytes (CSPRNG) for keys, nonces, and salts.

18) **Hash** (`obi.profile:crypto.hash-0`)  
   Streaming hashes (blake3/sha256/etc.) for integrity checks and content addressing.

19) **AEAD** (`obi.profile:crypto.aead-0`)  
   Authenticated encryption for secure channels and storage (`seal`/`open`).

20) **Signatures** (`obi.profile:crypto.sign-0`)  
   Sign/verify primitives with key import and optional key generation/export.

21) **KDFs** (`obi.profile:crypto.kdf-0`)  
   Key derivation functions (HKDF/PBKDF2/Argon2id family) for deriving keys from inputs.

### Data baseline (common once you ingest or ship artifacts)

22) **KV Database** (`obi.profile:db.kv-0`)  
   Transactional key/value stores (LMDB/RocksDB/LevelDB class).

23) **SQL Database** (`obi.profile:db.sql-0`)  
   SQLite-style prepare/bind/step interfaces for embeddable SQL backends.

24) **Data Compression** (`obi.profile:data.compression-0`)  
   Streaming compression/decompression (zlib/zstd/brotli/lz4 style) via OBI readers/writers.

25) **Archive Containers** (`obi.profile:data.archive-0`)  
   Stream archive entries in/out (libarchive/libzip style).

26) **File Type Detection** (`obi.profile:data.file_type-0`)  
    Magic/signature-based file type guessing (libmagic-style) to pick handlers before parsing.

26b) **Serde Events** (`obi.profile:data.serde_events-0`)  
    Event-based parsing for JSON/YAML/TOML-style formats (maps/sequences/scalars).

### Document baseline (optional for content ingestion and open standards)

27) **Document Inspect** (`obi.profile:doc.inspect-0`)  
    Deep inspection of documents (canonical MIME + JSON summary + JSON metadata).

28) **Text Decode** (`obi.profile:doc.text_decode-0`)  
    Decode arbitrary bytes/readers into UTF-8 (iconv/ICU style).

28b) **Markup Events** (`obi.profile:doc.markup_events-0`)  
    Event-based parsing for XML/HTML-like markup (tags + attributes + text).

29) **Markdown Parse** (`obi.profile:doc.markdown_commonmark-0`)  
    Parse markdown to a structured representation (JSON baseline).

29b) **Markdown Events** (`obi.profile:doc.markdown_events-0`)  
    Event-based markdown parsing for hosts that want to build their own AST/renderer.

30) **Paged Documents** (`obi.profile:doc.paged_document-0`)  
    Open and rasterize PDF/SVG-like paged docs; optional text extraction.

### Asset baseline (optional for 3D ingestion)

31) **Mesh Import** (`obi.profile:asset.mesh_io-0`)  
    Import triangle meshes (positions/normals/uvs/indices) from common formats.

32) **Scene Import** (`obi.profile:asset.scene_io-0`)  
    Import 3D scenes and referenced blobs (glTF/assimp-style).

### Media baseline (common for tools, ingestion, and playback)

33) **Image Codec** (`obi.profile:media.image_codec-0`)  
   Decode images to CPU pixel buffers and encode pixels back out (stb_image/libpng/libjpeg/etc.).

34) **Audio Device** (`obi.profile:media.audio_device-0`)  
    Open playback/capture streams and write/read PCM frames (SDL/PortAudio/platform backends).

35) **Audio Mix** (`obi.profile:media.audio_mix-0`)  
    Mix N interleaved PCM sources into one output buffer for playback/export.

36) **Audio Resample** (`obi.profile:media.audio_resample-0`)  
    Resample and convert PCM formats (soxr/libsamplerate/swresample class).

37) **Container Demux** (`obi.profile:media.demux-0`)  
    Extract encoded packet streams from containers (FFmpeg/libavformat/gstreamer demux wrappers).

38) **AV Decode** (`obi.profile:media.av_decode-0`)  
    Minimal packet-in / frame-out decoding surface (FFmpeg/libavcodec, gstreamer wrappers).

39) **Video Scale/Convert** (`obi.profile:media.video_scale_convert-0`)  
    CPU scaling and pixel format conversion (libswscale/libyuv class).

40) **Container Mux** (`obi.profile:media.mux-0`)  
    Write encoded packet streams into containers for export workflows.

### Physics baseline (optional for simulation and games)

41) **2D Physics World** (`obi.profile:phys.world2d-0`)  
    A minimal 2D rigid-body world (Box2D/Chipmunk2D class).

42) **3D Physics World** (`obi.profile:phys.world3d-0`)  
    A minimal 3D rigid-body world (Bullet/Jolt/PhysX class).

43) **Physics Debug Draw** (`obi.profile:phys.debug_draw-0`)  
    Extract debug line/tri primitives for visualization.

### Math baseline (only when you need these semantics)

44) **Big Integers** (`obi.profile:math.bigint-0`)  
    Arbitrary precision integer values (GMP-style).

45) **Big Floats** (`obi.profile:math.bigfloat-0`)  
    Arbitrary precision floating-point values (MPFR-style).

46) **Decimal Arithmetic** (`obi.profile:math.decimal-0`)  
    Base-10 decimal contexts and operations (mpdecimal-style).

47) **Scientific Ops** (`obi.profile:math.scientific_ops-0`)  
    A small special-functions surface suitable for GSL-like providers.

48) **BLAS Subset** (`obi.profile:math.blas-0`)  
    A small BLAS surface (GEMM) for swapping matrix backends (OpenBLAS/MKL/etc.).

---

## 3. Composition Pattern

Providers often implement multiple profiles:

- `provider:sdl` => window_input + render2d + pump (if needed)
- `provider:curl` => http_client (+ pump optional)
- `provider:libsoup` => http_client + pump (GLib main loop style)
- `provider:openssl` => tls + hash + aead + sign + kdf
- `provider:sqlite` => db.sql
- `provider:ffmpeg` => demux + av_decode + video_scale_convert + mux + audio_resample
- `provider:libxml2` => markup_events
- `provider:simdjson` => serde_events
- `provider:cmark` => markdown_commonmark + markdown_events

The host selects providers per profile at runtime (CLI flags, config, policy), and then higher layers
build systems (GUI, ingestion, media pipelines) on top.

---

## Global Q&A

**Q: Why not put this in OGIF?**  
OGIF is an interchange membrane and should remain declarative. OBI is imperative and focused on
runtime ABI and integration mechanics.

**Q: Do we need a profile for every library?**  
No. Many libraries can be wrapped behind existing profiles (handles + streams + pump). Add a new
profile only when you need a stable domain contract across multiple implementations.
