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
- Text: shaping (bidi/harfbuzz), glyph rasterization + host-managed atlas caching
- Networking: HTTP clients (curl/libsoup), websockets, etc.
- Media: demux/decode/filter (ffmpeg/gstreamer), resampling
- Data: DB handles/transactions (sqlite/lmdb), compression/archives
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

### GUI baseline (common for tools and POCs)

2) **Window + Input** (`obi.profile:gfx.window_input-0`)  
   Window creation, event pump, input events, clipboard, DPI/framebuffer sizing.

3) **2D Render** (`obi.profile:gfx.render2d-0`)  
   Textures + scissor + rectangles + textured quads (enough to render a glyph atlas).

### Text baseline (recommended once you need correct Unicode)

4) **Text Shape** (`obi.profile:text.shape-0`)  
   FriBidi + HarfBuzz style shaping: UTF-8 in, glyph indices + positions out.

5) **Text Raster Cache** (`obi.profile:text.raster_cache-0`)  
   Glyph rasterization + optional internal caching. Hosts typically pack glyphs into their own atlas
   using `obi.profile:gfx.render2d-0`.

### Networking baseline (needed for internet services)

6) **HTTP Client** (`obi.profile:net.http_client-0`)  
   A request/response interface with optional async/pump integration, compatible with curl/libsoup.

7) **WebSocket Client** (`obi.profile:net.websocket-0`)  
   Duplex messaging (send/receive) with optional async/pump integration.

### Crypto baseline (common for integrity/content addressing)

8) **Hash** (`obi.profile:crypto.hash-0`)  
   Streaming hashes (blake3/sha256/etc.) for integrity checks and content addressing.

### Data baseline (common once you ingest or ship artifacts)

9) **Data Compression** (`obi.profile:data.compression-0`)  
   Streaming compression/decompression (zlib/zstd/brotli/lz4 style) via OBI readers/writers.

10) **Archive Containers** (`obi.profile:data.archive-0`)  
   Stream archive entries in/out (libarchive/libzip style).

### Media baseline (common for tools, ingestion, and playback)

11) **Image Codec** (`obi.profile:media.image_codec-0`)  
   Decode images to CPU pixel buffers and encode pixels back out (stb_image/libpng/libjpeg/etc.).

12) **Audio Device** (`obi.profile:media.audio_device-0`)  
    Open playback/capture streams and write/read PCM frames (SDL/PortAudio/platform backends).

13) **AV Decode** (`obi.profile:media.av_decode-0`)  
    Minimal packet-in / frame-out decoding surface (FFmpeg/libavcodec, gstreamer wrappers).

### Math baseline (only when you need these semantics)

14) **Big Integers** (`obi.profile:math.bigint-0`)  
    Arbitrary precision integer values (GMP-style).

15) **Big Floats** (`obi.profile:math.bigfloat-0`)  
    Arbitrary precision floating-point values (MPFR-style).

16) **BLAS Subset** (`obi.profile:math.blas-0`)  
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
