# OBI Text IME Profile
## OBI Profile: `obi.profile:text.ime-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:text.ime-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes IME (Input Method Editor) composition events for complex text input:

- start/stop IME for a window
- receive composition start/update/commit/end events
- optionally set the cursor rectangle for candidate window placement

Typical providers:

- SDL IME/text editing events
- platform IME APIs (Windows TSF/IMM, macOS input methods, X11/Wayland IME layers)

This profile complements `obi.profile:gfx.window_input-0` which provides basic text input events
but does not model IME preedit/composition state.

---

## 2. Technical Details

### 2.1 Event model

IME events are produced by polling:

- `poll_event(...)` (non-blocking)
- `wait_event(...)` (optional; blocking up to a timeout)

Event types include:

- composition start
- composition update (preedit text)
- composition commit (final inserted text)
- composition end

Composition text is UTF-8 and may be split across multiple events when it exceeds the fixed event
buffer capacity.

### 2.2 Cursor rectangle (Optional)

When `OBI_IME_CAP_CURSOR_RECT` is advertised, hosts may call `set_cursor_rect(window, rect)` to
position IME candidate UI near the caret.

---

## 3. Conformance

Required:

- `start`
- `stop`
- `poll_event`

Optional (advertised via caps):

- `wait_event`
- `set_cursor_rect`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_text_ime_v0.h`
- `abi/profiles/obi_gfx_types_v0.h` (window IDs)
- `abi/profiles/obi_geom_types_v0.h` (rect type)

---

## Global Q&A

**Q: Why not extend `gfx.window_input` to include IME composition?**  
Keeping IME separate avoids breaking the stable window/input event ABI and lets hosts opt into IME
only when they need composition-aware editors.

