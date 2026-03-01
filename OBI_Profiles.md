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
- Documents: inspection, decoding, markdown/PDF and other open standards
- Networking: HTTP clients (curl/libsoup), websockets, etc.
- Media: demux/decode/filter (ffmpeg/gstreamer), resampling
- Data: DB handles/transactions (sqlite/lmdb), compression/archives
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

### Cross-cutting (strongly recommended)

1) **Core Pump** (`obi.profile:core.pump-0`)  
   A minimal "step" interface for providers that need an event loop to make progress.

2) **Core WaitSet** (`obi.profile:core.waitset-0`)  
   Optional OS-level waitable hints (fds/handles) to integrate pump-driven providers efficiently.

### GUI baseline (common for tools and POCs)

3) **Window + Input** (`obi.profile:gfx.window_input-0`)  
   Window creation, event pump, input events, clipboard, DPI/framebuffer sizing.

4) **2D Render** (`obi.profile:gfx.render2d-0`)  
   Textures + scissor + rectangles + textured quads (enough to render a glyph atlas).

### GPU/3D baseline (optional for 3D tools)

5) **GPU Device** (`obi.profile:gfx.gpu_device-0`)  
   Portable GPU abstraction (OpenGL/Vulkan/Metal/D3D style backends).

6) **3D Render** (`obi.profile:gfx.render3d-0`)  
   Minimal 3D rendering for tools and POCs (meshes, textures, camera, draw).

### Text baseline (recommended once you need correct Unicode)

7) **Text Segmenter** (`obi.profile:text.segmenter-0`)  
   Unicode segmentation and break opportunities (grapheme/word/line/bidi).

8) **Font DB** (`obi.profile:text.font_db-0`)  
   System font discovery and fallback (fontconfig/CoreText/DirectWrite style).

9) **Text Shape** (`obi.profile:text.shape-0`)  
   FriBidi + HarfBuzz style shaping: UTF-8 in, glyph indices + positions out.

10) **Text Raster Cache** (`obi.profile:text.raster_cache-0`)  
   Glyph rasterization + optional internal caching. Hosts typically pack glyphs into their own atlas
   using `obi.profile:gfx.render2d-0`.

11) **Text Layout** (`obi.profile:text.layout-0`)  
    Paragraph layout and positioned glyph output ("text flow") for rendering via an atlas.

12) **Spellcheck** (`obi.profile:text.spellcheck-0`)  
    Spellchecking and suggestions (aspell/hunspell/enchant style) for editors and tooling.

### Networking baseline (needed for internet services)

13) **HTTP Client** (`obi.profile:net.http_client-0`)  
   A request/response interface with optional async/pump integration, compatible with curl/libsoup.

14) **WebSocket Client** (`obi.profile:net.websocket-0`)  
   Duplex messaging (send/receive) with optional async/pump integration.

### Crypto baseline (common for integrity/content addressing)

15) **Hash** (`obi.profile:crypto.hash-0`)  
   Streaming hashes (blake3/sha256/etc.) for integrity checks and content addressing.

### Data baseline (common once you ingest or ship artifacts)

16) **Data Compression** (`obi.profile:data.compression-0`)  
   Streaming compression/decompression (zlib/zstd/brotli/lz4 style) via OBI readers/writers.

17) **Archive Containers** (`obi.profile:data.archive-0`)  
   Stream archive entries in/out (libarchive/libzip style).

18) **File Type Detection** (`obi.profile:data.file_type-0`)  
    Magic/signature-based file type guessing (libmagic-style) to pick handlers before parsing.

### Document baseline (optional for content ingestion and open standards)

19) **Document Inspect** (`obi.profile:doc.inspect-0`)  
    Deep inspection of documents (canonical MIME + JSON summary + JSON metadata).

20) **Text Decode** (`obi.profile:doc.text_decode-0`)  
    Decode arbitrary bytes/readers into UTF-8 (iconv/ICU style).

21) **Markdown Parse** (`obi.profile:doc.markdown_commonmark-0`)  
    Parse markdown to a structured representation (JSON baseline).

22) **Paged Documents** (`obi.profile:doc.paged_document-0`)  
    Open and rasterize PDF/SVG-like paged docs; optional text extraction.

### Media baseline (common for tools, ingestion, and playback)

23) **Image Codec** (`obi.profile:media.image_codec-0`)  
   Decode images to CPU pixel buffers and encode pixels back out (stb_image/libpng/libjpeg/etc.).

24) **Audio Device** (`obi.profile:media.audio_device-0`)  
    Open playback/capture streams and write/read PCM frames (SDL/PortAudio/platform backends).

25) **AV Decode** (`obi.profile:media.av_decode-0`)  
    Minimal packet-in / frame-out decoding surface (FFmpeg/libavcodec, gstreamer wrappers).

### Physics baseline (optional for simulation and games)

26) **2D Physics World** (`obi.profile:phys.world2d-0`)  
    A minimal 2D rigid-body world (Box2D/Chipmunk2D class).

27) **3D Physics World** (`obi.profile:phys.world3d-0`)  
    A minimal 3D rigid-body world (Bullet/Jolt/PhysX class).

28) **Physics Debug Draw** (`obi.profile:phys.debug_draw-0`)  
    Extract debug line/tri primitives for visualization.

### Math baseline (only when you need these semantics)

29) **Big Integers** (`obi.profile:math.bigint-0`)  
    Arbitrary precision integer values (GMP-style).

30) **Big Floats** (`obi.profile:math.bigfloat-0`)  
    Arbitrary precision floating-point values (MPFR-style).

31) **Decimal Arithmetic** (`obi.profile:math.decimal-0`)  
    Base-10 decimal contexts and operations (mpdecimal-style).

32) **Scientific Ops** (`obi.profile:math.scientific_ops-0`)  
    A small special-functions surface suitable for GSL-like providers.

33) **BLAS Subset** (`obi.profile:math.blas-0`)  
    A small BLAS surface (GEMM) for swapping matrix backends (OpenBLAS/MKL/etc.).

---

## 3. Composition Pattern

Providers often implement multiple profiles:

- `provider:sdl` => window_input + render2d + pump (if needed)
- `provider:curl` => http_client (+ pump optional)
- `provider:libsoup` => http_client + pump (GLib main loop style)

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
