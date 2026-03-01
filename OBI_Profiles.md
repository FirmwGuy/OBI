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
- Text: shaping (bidi/harfbuzz), glyph rasterization + atlas caching
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
   Glyph rasterization + dynamic atlas caching (usually LRU) with explicit eviction policy.

### Networking baseline (needed for internet services)

6) **HTTP Client** (`obi.profile:net.http_client-0`)  
   A request/response interface with optional async/pump integration, compatible with curl/libsoup.

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

