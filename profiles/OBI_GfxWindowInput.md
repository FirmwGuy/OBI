# OBI Window + Input Profile
## OBI Profile: `obi.profile:gfx.window_input-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:gfx.window_input-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile provides a minimal cross-platform surface for:

- creating and destroying windows,
- polling input and window events,
- obtaining framebuffer sizing and DPI/content scaling,
- optional clipboard and text input mode.

Rendering is intentionally out of scope. Pair this profile with `obi.profile:gfx.render2d-0` (or a
future 3D profile) for drawing.

---

## 2. Technical Details

### 2.1 Objects

- The host obtains an `obi_window_input_v0` handle from a provider.
- Windows are identified by an opaque `obi_window_id_v0`.

Window IDs are provider-defined and provider-instance-local. They are only valid with gfx profile
handles obtained from the same provider instance, unless a future profile revision or a
provider-documented bridge says otherwise.

### 2.2 Event model

Events are produced by polling:

- `poll_event(...)` (non-blocking)
- `wait_event(...)` (optional; blocking up to a timeout)

Events are returned in FIFO order. Each event includes:

- an event type,
- a monotonic timestamp when available,
- the associated window ID when applicable,
- a type-specific payload.

### 2.3 Keyboard vs text input

This profile separates:

- **key events**: physical key presses using USB HID keycodes (layout-independent),
- **text input events**: UTF-8 text after IME/layout composition (layout-dependent).

Hosts SHOULD treat key events as controls/shortcuts and text input as the source of user text.

### 2.4 Coordinates and sizing

- Mouse coordinates are in framebuffer pixels (origin top-left).
- `window_get_framebuffer_size` returns the authoritative size for rendering targets.
- `window_get_content_scale` (optional) reports UI scaling factors for high-DPI setups.

### 2.5 Determinism notes (CEP integration)

Input is inherently nondeterministic. Deterministic hosts (such as CEP-driven systems) should:

- record input events (type + payload + ordering) as evidence,
- replay by feeding the same event stream rather than re-polling the OS.

This profile is designed to make event encoding stable enough for capture/replay pipelines.

### 2.6 Threading notes

Most window/input libraries are thread-affine. Providers MUST document:

- which thread owns the window system,
- whether polling may happen on other threads,
- which calls may block.

Hosts MUST assume thread-affinity unless the provider explicitly documents otherwise.

---

## 3. Conformance

Required:

- `create_window`
- `destroy_window`
- `poll_event`
- `window_get_framebuffer_size`

Optional (advertised via caps):

- `wait_event`
- `window_get_content_scale`
- clipboard UTF-8 helpers
- text input mode helpers

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_gfx_window_input_v0.h`

---

## Global Q&A

**Q: Why keycodes as USB HID usages?**  
They are a widely supported, stable encoding for physical keys across platforms and libraries.
Text input is handled separately via UTF-8 events.

**Q: Does this profile support gamepads?**  
Not in v0. A future `obi.profile:input.gamepad-*` profile can cover that without bloating the window
surface.
