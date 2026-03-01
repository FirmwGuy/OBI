# OBI OS FS Watch Profile
## OBI Profile: `obi.profile:os.fs_watch-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:os.fs_watch-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes filesystem watching:

- watch a path (optionally recursively)
- receive batches of change events (create/modify/remove/rename/etc.)

Typical providers:

- inotify (Linux)
- FSEvents (macOS)
- ReadDirectoryChangesW (Windows)
- libuv-based wrappers

This profile is intended for tools (asset pipelines, editors, live-reload) and host services that
need to react to filesystem changes portably.

---

## 2. Technical Details

### 2.1 Watch model

The host opens a watcher, then adds one or more watches via `add_watch(path, ...)`, receiving a
provider-defined `watch_id` for later removal.

### 2.2 Event model

Events are returned in batches via `poll_events(timeout_ns, ...)`.

Providers MAY coalesce events, drop fine-grained detail, or emit `OTHER` for backend-specific
conditions. If events are dropped due to overflow, providers SHOULD set the `OVERFLOW` flag.

Rename events may be represented as:

- a single `RENAME` event with only `path` populated, or
- a paired rename with both `path` and `path2` (when supported)

### 2.3 Ownership

Event batches are provider-owned and released via the batch `release` callback.

---

## 3. Conformance

Required:

- open watcher
- add/remove watch
- poll events
- destroy

Optional (advertised via caps):

- recursive watches
- paired rename events
- provider-specific `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_os_fs_watch_v0.h`

---

## Global Q&A

**Q: Why batches instead of a callback registration model?**  
Batch polling is the most portable shape across event loops and FFIs. Hosts can adapt polling to
their own scheduling strategy (pump-driven, threads, select/epoll, etc.).

