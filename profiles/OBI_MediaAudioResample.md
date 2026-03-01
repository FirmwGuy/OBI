# OBI Media Audio Resample Profile
## OBI Profile: `obi.profile:media.audio_resample-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:media.audio_resample-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal, stateful audio resampler:

- convert sample rate (required)
- optionally convert sample format (S16/F32) and channel count (remix)
- process audio incrementally and drain internal delay

Typical providers:

- libsoxr wrappers
- libsamplerate wrappers
- FFmpeg `swresample` wrappers

This profile pairs naturally with:

- `obi.profile:media.audio_device-0` (device I/O)
- `obi.profile:media.audio_mix-0` (combine sources before output)

---

## 2. Technical Details

### 2.1 Format model

Resampling operates on interleaved PCM frames. A resampler instance is created for a fixed:

- input format (`obi_audio_format_v0`)
- output format (`obi_audio_format_v0`)

Providers MAY reject unsupported conversions via `OBI_STATUS_UNSUPPORTED`.

### 2.2 Streaming model

The host calls:

1) `process_interleaved` repeatedly to convert input frames into output frames
2) `drain_interleaved` to flush any buffered output (filter delay, internal queues)

Providers MUST report:

- how many input frames were consumed
- how many output frames were produced

### 2.3 Ownership

All input/output buffers are host-owned and borrowed for the duration of each call only.

---

## 3. Conformance

Required:

- create resampler
- `process_interleaved`
- `drain_interleaved`
- destroy

Optional (advertised via caps):

- channel remixing (upmix/downmix)
- `reset`
- provider-specific `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_media_audio_resample_v0.h`
- `abi/profiles/obi_media_types_v0.h`

---

## Global Q&A

**Q: Why not standardize channel layouts and speaker mapping in v0?**  
Those rules vary widely across engines. v0 standardizes the mechanics (formats + resampling), and
leaves detailed remix policy to providers (via caps and documentation).

