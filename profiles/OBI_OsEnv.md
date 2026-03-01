# OBI OS Env Profile
## OBI Profile: `obi.profile:os.env-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:os.env-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a small set of environment and process-context queries:

- read environment variables
- optionally set/unset environment variables
- optionally query/change the current working directory
- optionally obtain common "known directories" (home, temp, config, cache, data)
- optionally enumerate environment variables

Typical providers:

- POSIX (`getenv`, `setenv`, `unsetenv`, `getcwd`, `chdir`)
- Win32 (`GetEnvironmentVariableW`, `SetEnvironmentVariableW`, `GetCurrentDirectoryW`)
- WASI-like environments (host-defined env vars and preopened dirs)

The goal is to provide enough OS context for tooling and portability layers without committing to
any single OS API or path convention.

---

## 2. Technical Details

### 2.1 Environment variables

`getenv_utf8(name, ...)` returns `OBI_STATUS_OK` and sets `out_found`:

- `out_found=false`: variable not found, `out_size` MUST be 0
- `out_found=true`: variable found

When found, if `out_value` is NULL or too small, providers return `OBI_STATUS_BUFFER_TOO_SMALL`
and set `out_size` to the required byte count (UTF-8 bytes, excluding any trailing NUL).

### 2.2 Setting and unsetting (Optional)

When `OBI_ENV_CAP_SET` is advertised, providers implement:

- `setenv_utf8(name, value, flags)`
- `unsetenv(name)`

If `OBI_ENV_SET_NO_OVERWRITE` is set, providers SHOULD fail when the variable already exists.

### 2.3 Current working directory (Optional)

When `OBI_ENV_CAP_CWD` is advertised, providers implement `get_cwd_utf8(...)`.

When `OBI_ENV_CAP_CHDIR` is advertised, providers implement `chdir(path)`.

### 2.4 Known directories (Optional)

When `OBI_ENV_CAP_KNOWN_DIRS` is advertised, providers implement:

- `known_dir_utf8(kind, ...)` returning a provider-defined path for the requested directory kind

If a directory kind is not available, providers return `OBI_STATUS_OK` with `out_found=false`.

### 2.5 Enumerating variables (Optional)

When `OBI_ENV_CAP_ENUM` is advertised, providers implement `env_iter_open()` returning an iterator.

The iterator yields `(name, value)` pairs as provider-owned UTF-8 views, valid until the next call
or iterator destruction.

---

## 3. Conformance

Required:

- `getenv_utf8`

Optional (advertised via caps):

- `OBI_ENV_CAP_SET` => `setenv_utf8`, `unsetenv`
- `OBI_ENV_CAP_CWD` => `get_cwd_utf8`
- `OBI_ENV_CAP_CHDIR` => `chdir`
- `OBI_ENV_CAP_KNOWN_DIRS` => `known_dir_utf8`
- `OBI_ENV_CAP_ENUM` => `env_iter_open` and iterator

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_os_env_v0.h`

---

## Global Q&A

**Q: Why does this profile use output buffers for some strings?**  
It avoids cross-FFI ownership of heap memory while still supporting arbitrarily long values.
Hosts can call once to get the required size, allocate, then call again.

