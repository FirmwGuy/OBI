# OBI Data Compression Profile
## OBI Profile: `obi.profile:data.compression-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:data.compression-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal "compress/decompress bytes" interface so hosts can swap
compression backends without rewriting glue code.

Typical providers:

- zlib (deflate/gzip)
- zstd
- brotli
- lz4

This profile is intentionally streaming-friendly by using the OBI core `obi_reader_v0` and
`obi_writer_v0` interfaces, so large payloads do not require full buffering.

---

## 2. Technical Details

### 2.1 Codec IDs

Codecs are selected by UTF-8 codec ID strings (examples: `deflate`, `gzip`, `zstd`, `brotli`).

Providers MUST return `OBI_STATUS_UNSUPPORTED` for unknown codec IDs.

### 2.2 Parameters

The parameters struct (`obi_compression_params_v0`) supports:

- `level` (provider-defined meaning; `-1` means provider default)
- optional `dictionary` bytes (if the provider supports dictionaries)
- optional `options_json` (provider-specific JSON object string)

Providers MUST ignore fields beyond `struct_size` for forward compatibility.

### 2.3 Streaming and ownership

`compress/decompress` consume bytes from a caller-supplied reader and emit bytes to a caller-supplied
writer.

Ownership rules:

- The provider borrows `src` and `dst` for the duration of the call only.
- The provider MUST NOT destroy `src` or `dst`.

Blocking rules:

- This v0 profile is synchronous. Providers SHOULD complete the operation in one call.
- Hosts SHOULD supply blocking readers/writers (file readers, memory buffers, etc.).

### 2.4 Error handling

Providers SHOULD return:

- `OBI_STATUS_OK` on success,
- `OBI_STATUS_BAD_ARG` for invalid parameters,
- `OBI_STATUS_UNSUPPORTED` for unknown codecs or unsupported options,
- `OBI_STATUS_IO_ERROR` for corrupted inputs or writer failures,
- `OBI_STATUS_OUT_OF_MEMORY` if allocation fails.

---

## 3. Conformance

Required:

- `compress`
- `decompress`

Optional (advertised via caps):

- dictionary support
- provider-specific `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_data_compression_v0.h`

---

## Global Q&A

**Q: Why codec IDs as strings instead of enums?**  
To allow hosts to request common codecs without re-releasing this profile whenever a new codec is
added. Providers can accept extra IDs and reject unknown ones.

**Q: Why not define a full streaming job API (step/poll)?**  
Many compression use-cases are synchronous and file/memory-based. If nonblocking/pump-driven
transcoding becomes common, a future profile version can add a job API without breaking v0.

