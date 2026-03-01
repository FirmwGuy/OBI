# OBI OS FS Profile
## OBI Profile: `obi.profile:os.fs-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:os.fs-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes basic filesystem operations:

- open files for streaming reads/writes
- stat paths (type/size/mtime)
- create directories
- remove files (or empty directories)
- rename/move paths
- optionally enumerate directory entries

Typical providers:

- POSIX (`open`, `read`, `write`, `stat`, `rename`, `mkdir`, `unlink`, `opendir`)
- Win32 (`CreateFile`, `GetFileAttributesEx`, `MoveFileEx`, `CreateDirectory`)
- WASI-ish environments (when a host offers filesystem mounts)
- virtual filesystems (zipfs, project workspaces, content-addressed stores)

The primary goal is to make "read/write/stat/list" portable for tools and hosts without baking in
any one OS API.

---

## 2. Technical Details

### 2.1 Paths

All paths are passed as UTF-8, NUL-terminated `const char*`.

The profile does not standardize path syntax. Providers MAY interpret paths as:

- OS-native paths (common)
- provider-defined URIs (for virtual filesystems)

### 2.2 Streaming I/O

`open_reader()` returns a provider-owned `obi_reader_v0` for the given path.

`open_writer()` returns a provider-owned `obi_writer_v0` for the given path. Writer creation
semantics are controlled by `obi_fs_open_writer_params_v0.flags`:

- `OBI_FS_OPEN_WRITE_CREATE`: create the file if missing
- `OBI_FS_OPEN_WRITE_TRUNCATE`: truncate the file on open
- `OBI_FS_OPEN_WRITE_APPEND`: append writes to end-of-file
- `OBI_FS_OPEN_WRITE_EXCLUSIVE`: fail if the file already exists (when used with `CREATE`)

Providers SHOULD return `OBI_STATUS_BAD_ARG` for contradictory flag combinations (for example
`TRUNCATE|APPEND`).

### 2.3 Stat

`stat()` returns `OBI_STATUS_OK` and sets `out_found`:

- `out_found=false`: path does not exist (or is not visible to the provider)
- `out_found=true`: `out_stat` is filled

### 2.4 Directory Creation

`mkdir(path, flags)` creates a directory.

If `OBI_FS_MKDIR_RECURSIVE` is set, providers SHOULD create intermediate directories as needed.

### 2.5 Removal

`remove()` removes a file or an empty directory.

It returns `OBI_STATUS_OK` and sets `out_removed`:

- `out_removed=false`: nothing was removed (missing path, non-empty dir, etc.)
- `out_removed=true`: the path was removed

### 2.6 Rename / Move

`rename(from, to, flags)` renames or moves a filesystem entry.

If `OBI_FS_RENAME_REPLACE` is set, providers SHOULD replace an existing destination when the
backend supports it. If clear, providers SHOULD fail when `to` already exists.

### 2.7 Directory Iteration (Optional)

When `OBI_FS_CAP_DIR_ITER` is advertised, providers support `open_dir_iter()`.

The returned iterator exposes `next_entry()` which yields `obi_fs_dir_entry_v0` records until
`out_has_entry=false`.

Ownership/lifetime rules:

- `obi_fs_dir_entry_v0.name` and `.full_path` are provider-owned views
- these views are valid until the next `next_entry()` call or iterator destruction

Providers MAY leave `.full_path` empty if it is expensive or ambiguous to compute.

### 2.8 Provider Options (Optional)

When `OBI_FS_CAP_OPTIONS_JSON` is advertised, providers accept `options_json` fields in open/iter
params as a JSON object string.

Hosts SHOULD pass an empty view when the capability is not present.

---

## 3. Conformance

Required:

- `open_reader`
- `open_writer`
- `stat`
- `mkdir`
- `remove`
- `rename`

Optional (advertised via caps):

- `OBI_FS_CAP_DIR_ITER` => `open_dir_iter`
- `OBI_FS_CAP_OPTIONS_JSON` => `options_json` accepted in params

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_os_fs_v0.h`
- `abi/obi_core_v0.h` (reader/writer types)

---

## Global Q&A

**Q: Why not include "read entire file" and "write entire file" helpers?**  
Streaming is the common denominator. Hosts can layer convenience APIs on top of readers/writers
without expanding the stable ABI surface.

