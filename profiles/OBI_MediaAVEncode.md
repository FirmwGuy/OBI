# OBI Media AV Encode Profile
## OBI Profile: `obi.profile:media.av_encode-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:media.av_encode-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal audio/video encoding surface:

- create an encoder for a codec (audio or video)
- send raw frames (PCM audio or RGBA video)
- receive encoded packets
- optionally obtain codec extradata (SPS/PPS/etc.)

Typical providers:

- FFmpeg/libavcodec wrappers
- platform encoders (MediaFoundation, VideoToolbox)
- GStreamer encoder wrappers

This profile complements:

- `obi.profile:media.av_decode-0` (decode)
- `obi.profile:media.mux-0` (container output)

---

## 2. Technical Details

### 2.1 Encoder model

The host creates an encoder via:

- `encoder_create(kind, codec_id, params, out_encoder)`

Then the host sends frames:

- `send_video_frame(frame)` for video encoders
- `send_audio_frame(frame)` for audio encoders

After sending, the host drains encoded output via:

- `receive_packet(out_packet, out_has_packet)`

To flush at end-of-stream, the host calls `send_*_frame(NULL)` and continues calling
`receive_packet()` until it reports no more packets.

### 2.2 Ownership

Input frames are caller-owned and borrowed for the duration of the call.

Output packets are provider-owned and released via the packet `release` callback.

### 2.3 Extradata (Optional)

When `OBI_AV_ENC_CAP_EXTRADATA` is advertised, providers implement `get_extradata()` to return codec
configuration bytes for muxers (for example H.264 SPS/PPS).

### 2.4 Options JSON (Optional)

When `OBI_AV_ENC_CAP_OPTIONS_JSON` is advertised, providers accept `options_json` as a provider-
specific JSON object string for codec tuning.

---

## 3. Conformance

Required:

- `encoder_create`
- `send_*_frame` (for the created encoder kind)
- `receive_packet`
- `encoder.destroy`

Optional (advertised via caps):

- extradata
- `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_media_av_encode_v0.h`
- `abi/profiles/obi_media_av_decode_v0.h` (shared stream kind and packet flags)
- `abi/profiles/obi_media_types_v0.h` (audio/video format enums)

---

## Global Q&A

**Q: Why does this profile use packets rather than writing directly to a muxer?**  
Packet surfaces keep concerns separate: encode produces codec packets, mux writes container bytes.
Hosts can wire them together with `obi.profile:media.mux-0` or custom pipelines.

