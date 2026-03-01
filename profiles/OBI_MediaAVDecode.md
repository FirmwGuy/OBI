# OBI Media AV Decode Profile
## OBI Profile: `obi.profile:media.av_decode-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:media.av_decode-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal codec decoding interface:

- the host feeds encoded packets
- the provider outputs decoded audio or video frames

Typical providers:

- FFmpeg / libavcodec wrappers
- GStreamer-based providers (when used as a decode service)

This profile intentionally does not define demuxing/muxing (containers). A separate profile can
standardize container I/O if/when needed.

---

## 2. Technical Details

### 2.1 Decoder model

The host creates a decoder by specifying:

- stream kind (audio/video)
- codec ID string (examples: `h264`, `hevc`, `vp9`, `aac`, `opus`)
- optional codec extradata (codec headers / initialization data)

The host then:

1) calls `send_packet` with encoded payloads
2) calls `receive_*_frame` until no more frames are available

End of stream is signaled by calling `send_packet(NULL)`.

### 2.2 Output formats

Providers SHOULD support common CPU-friendly outputs:

- video: RGBA8 (baseline)
- audio: interleaved F32 or S16 (baseline)

Providers MAY support additional pixel/sample formats via caps.

### 2.3 Ownership

Decoded frame buffers are provider-owned and released via per-frame release callbacks.

Packet payloads are host-owned and borrowed for the duration of `send_packet` only.

---

## 3. Conformance

Required:

- decoder create/destroy
- `send_packet`
- `receive_video_frame` and/or `receive_audio_frame` (depending on supported kinds)

Optional (advertised via caps):

- additional output formats

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_media_av_decode_v0.h`
- `abi/profiles/obi_media_types_v0.h`

---

## Global Q&A

**Q: Why not define timestamps, timebases, and sync in detail?**  
Those semantics balloon quickly and depend on container/demux policy. v0 focuses on decoding
mechanics. Timestamps are included as best-effort nanoseconds, but robust A/V sync is expected to
be handled by higher layers.

