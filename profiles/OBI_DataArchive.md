# OBI Data Archive Profile
## OBI Profile: `obi.profile:data.archive-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:data.archive-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal interface for working with archive containers:

- reading archives (list entries, stream file contents)
- optionally writing archives (create entries, stream payloads)

Typical providers:

- libarchive (tar/zip/7z readers, tar writers, etc.)
- libzip (zip read/write)

The intent is to make "extract archive" and "build archive" workflows swappable without forcing
any specific archive library into the host.

---

## 2. Technical Details

### 2.1 Streaming model

Archives are opened from an OBI reader or written to an OBI writer:

- `open_reader(src_reader)` returns an archive reader handle
- (optional) `open_writer(dst_writer)` returns an archive writer handle

Entry payloads are exposed as:

- an `obi_reader_v0` returned by `open_entry_reader()` (read mode)
- an `obi_writer_v0` returned by `begin_entry()` (write mode)

This allows processing large archives without full buffering.

### 2.2 Entry enumeration

Archive readers iterate entries sequentially via `next_entry(...)`.

Minimum metadata includes:

- entry kind (file/dir/symlink/other)
- UTF-8 entry path
- uncompressed size (if known)

Providers SHOULD supply mtime and permissions when available.

### 2.3 Ownership and lifetimes

- The `open_reader/open_writer` calls borrow the provided `obi_reader_v0`/`obi_writer_v0` for the
  duration of the call.
- The returned archive reader/writer handles are provider-owned and must be destroyed with their
  `destroy` functions.
- Entry readers/writers returned for payload streaming are provider-owned and must be destroyed by
  the caller when finished.

Providers MUST document how destroying an entry reader/writer interacts with enumeration (for
example: destroying the entry reader implicitly drains/skips the remaining bytes for the entry).

### 2.4 Format selection

Providers SHOULD auto-detect formats when possible.

Hosts MAY pass `format_hint` strings (examples: `zip`, `tar`, `7z`) to guide providers when
auto-detection is ambiguous or disabled.

---

## 3. Conformance

Required:

- `open_reader`
- archive reader: `next_entry`, `open_entry_reader`, `destroy`

Optional (advertised via caps):

- archive writer support (`open_writer` and writer object)
- `skip_entry` convenience
- provider-specific options_json

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_data_archive_v0.h`

---

## Global Q&A

**Q: Why sequential enumeration instead of random-access APIs?**  
Sequential iteration is the lowest common denominator and maps naturally to streaming libraries
like libarchive. Random-access can be added later as an optional capability without breaking v0.

**Q: Why not expose per-entry file descriptors?**  
OBI aims to be portable and FFI-friendly. Reader/writer streaming is the core interoperability
mechanism.

