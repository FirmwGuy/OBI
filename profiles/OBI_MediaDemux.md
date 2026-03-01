# OBI Media Demux Profile
## OBI Profile: `obi.profile:media.demux-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:media.demux-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes container demuxing (extracting encoded packet streams from media files):

- open a container from a reader (file/stream)
- enumerate streams (audio/video/etc.)
- read encoded packets sequentially
- optional seeking

Typical providers:

- FFmpeg / libavformat wrappers
- GStreamer demux wrappers

This profile pairs naturally with `obi.profile:media.av_decode-0`:

- `media.demux` provides packets + codec parameters
- `media.av_decode` decodes packets to audio/video frames

---

## 2. Technical Details

### 2.1 Stream model

Streams are identified by indices `[0..stream_count)`.

Stream info includes:

- stream kind (audio/video/other)
- codec ID string (e.g. `h264`, `aac`)
- optional codec extradata bytes
- optional basic parameters (dimensions, sample rate/channels)

### 2.2 Packet model

Packets are returned as provider-owned byte buffers with timestamps in nanoseconds when available.

### 2.3 Ownership

Packet payload memory is provider-owned and released via a packet release callback.

Stream info views are provider-owned and valid until the demuxer is destroyed (or as documented).

---

## 3. Conformance

Required:

- open from reader
- stream count/info
- read packet
- destroy

Optional (advertised via caps):

- open from bytes
- seeking
- container metadata JSON

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_media_demux_v0.h`

---

## Global Q&A

**Q: Why timestamps in nanoseconds?**  
It is a portable common denominator. Providers can convert from stream timebases internally and
report `-1` when unknown.

