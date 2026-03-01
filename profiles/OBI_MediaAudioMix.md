# OBI Media Audio Mix Profile
## OBI Profile: `obi.profile:media.audio_mix-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:media.audio_mix-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes mixing multiple PCM streams into one output buffer.

Typical providers:

- small custom mixers
- DSP libraries (soundpipe, etc.) used as mixing engines

This profile is intended to sit above `obi.profile:media.audio_device-0`:

- device profile handles time-based I/O
- mix profile combines N sources into one buffer before output

---

## 2. Technical Details

### 2.1 PCM model

Mixing operates on interleaved PCM frames (`channels` samples per frame).

All inputs for a single mix call MUST use the same format (sample rate, channel count, sample
format). If formats differ, the host should resample/remix first (see `media.audio_resample`).

Providers SHOULD mix up to:

- `min(out_frame_cap, min_i inputs[i].frame_count)`

and MUST report the chosen count via `out_frames_written`.

### 2.2 Gains and clipping

Each input provides a linear gain factor.

Providers MUST document their clipping/saturation behavior for integer formats.

---

## 3. Conformance

Required:

- `mix_interleaved`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_media_audio_mix_v0.h`
- `abi/profiles/obi_media_types_v0.h`

---

## Global Q&A

**Q: Why not include a full audio graph here?**  
Audio graphs are large and engine-specific. Mixing is a common denominator; add graphs as a
separate profile once needed.
