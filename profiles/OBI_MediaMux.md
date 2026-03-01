# OBI Media Mux Profile
## OBI Profile: `obi.profile:media.mux-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:media.mux-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes muxing encoded packet streams into container files:

- open a container writer
- add audio/video streams (codec parameters)
- write encoded packets with timestamps
- finalize the container

Typical providers:

- FFmpeg / libavformat wrappers
- GStreamer mux wrappers

This profile is intentionally minimal and meant for tools and export pipelines.

---

## 2. Technical Details

### 2.1 Stream model

Streams are created by the host and receive an assigned stream index.

Each stream specifies:

- stream kind (audio/video/other)
- codec ID string (e.g. `h264`, `aac`)
- optional codec extradata bytes
- basic parameters (dimensions or sample rate/channels)

### 2.2 Packet model

Packets are host-owned bytes borrowed for the duration of `write_packet` only.

Timestamps are specified in nanoseconds when known; providers may rescale internally.

---

## 3. Conformance

Required:

- open writer
- add stream
- write packet
- finish/destroy

Optional (advertised via caps):

- open from format hints / options json

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_media_mux_v0.h`

---

## Global Q&A

**Q: Is this meant to be used for realtime streaming?**  
Not in v0. This is a file/container writing interface. Realtime transport would need separate
profiles for RTSP/WebRTC/etc.

