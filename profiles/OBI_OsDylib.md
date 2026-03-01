# OBI OS Dylib Profile
## OBI Profile: `obi.profile:os.dylib-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:os.dylib-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes dynamic library loading and symbol lookup:

- open a shared library by path (or optionally open "self")
- lookup symbols by name
- close the library handle

Typical providers:

- POSIX `dlopen`/`dlsym`/`dlclose`
- Win32 `LoadLibrary`/`GetProcAddress`/`FreeLibrary`
- sandboxed plugin registries that emulate dylib loading

This profile is intentionally small so hosts can build plugin systems and provider discovery
without committing to any one OS API.

---

## 2. Technical Details

### 2.1 Loading model

The host calls `open(path, params, out_lib)`.

- `path` is UTF-8, NUL-terminated
- when `path==NULL` and `OBI_DYLIB_CAP_OPEN_SELF` is advertised, providers open the current process
  module (or equivalent)

`obi_dylib_open_params_v0.flags` contains portable hints such as:

- `OBI_DYLIB_OPEN_NOW` (eager resolution when meaningful)
- `OBI_DYLIB_OPEN_GLOBAL` (export symbols globally when meaningful)

Providers MAY ignore flags that do not apply to their platform, but SHOULD document their behavior.

### 2.2 Symbol lookup

Symbol lookup is performed via `dylib.sym(name, ...)`.

It returns `OBI_STATUS_OK` and sets `out_found`:

- `out_found=true`: `out_sym` is set to a provider-defined symbol address
- `out_found=false`: symbol not present

### 2.3 WASM note

WASM environments commonly do not support OS-level dynamic linking. A provider MAY still implement
this profile by exposing a static registry of "modules" and "symbols" to the host.

---

## 3. Conformance

Required:

- `open`
- `dylib.sym`
- `dylib.destroy`

Optional (advertised via caps):

- open self (`path==NULL`)
- provider-specific `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_os_dylib_v0.h`

---

## Global Q&A

**Q: Why return `out_found` instead of treating missing symbols as an error?**  
It allows feature probing without forcing providers to mint OS-specific error codes or strings.

