# OBI Media Audio Device Profile
## OBI Profile: `obi.profile:media.audio_device-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:media.audio_device-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal interface for audio I/O devices:

- open an output stream (playback)
- optionally open an input stream (capture)
- write/read PCM frames

Typical providers:

- SDL audio backend
- PortAudio
- platform backends (ALSA/CoreAudio/WASAPI) wrapped into an OBI provider

This profile intentionally avoids DSP graphs, mixers, and codecs. Those belong in separate profiles.

---

## 2. Technical Details

### 2.1 Sample format

This profile uses shared media types (`obi_audio_sample_format_v0`) and defines:

- interleaved PCM frames
- `frame_count` is always "frames", not bytes

### 2.2 Blocking behavior

Audio devices are inherently time-based. Providers MUST document:

- whether `write_frames` blocks until space is available,
- whether it buffers internally,
- how underflow/overrun is handled.

### 2.3 Ownership

Audio buffers passed to `write_frames`/`read_frames` are host-owned and borrowed for the duration
of the call only.

Stream handles are provider-owned and destroyed by stream `destroy`.

---

## 3. Conformance

Required:

- output stream open (`open_output`) and output stream write (`write_frames`)

Optional (advertised via caps):

- input stream open/read
- latency queries

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_media_audio_device_v0.h`
- `abi/profiles/obi_media_types_v0.h`

---

## Global Q&A

**Q: Why not use callbacks (pull-based audio)?**  
Push/pull calls are easier to integrate with deterministic hosts and language bindings. Providers
can still implement callbacks internally.

**Q: What about resampling/channel mixing?**  
Those are separate concerns. A future `media.audio_resample` or `media.audio_mix` profile can sit
above this device profile.

