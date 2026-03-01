# OBI DB KV Profile
## OBI Profile: `obi.profile:db.kv-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:db.kv-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal transactional key/value database interface:

- open a DB by path/URI
- begin transactions
- get/put/delete by byte keys
- optional cursor iteration

Typical providers:

- LMDB wrappers
- LevelDB/RocksDB wrappers

This profile is intended for durable local storage and caches where a DB abstraction is useful but
the host does not want to commit to one backend.

---

## 2. Technical Details

### 2.1 Data model

Keys and values are arbitrary byte strings (`obi_bytes_view_v0`).

Providers MUST treat keys as opaque bytes (no encoding assumptions).

### 2.2 Transaction model

All operations occur inside a transaction:

- read-only transactions for consistent reads
- read/write transactions for updates

Providers MUST document concurrency/locking behavior (for example "single writer") as it differs
across backends.

### 2.3 Cursor model (optional)

A cursor provides ordered iteration over the key space with:

- `first`
- `seek_ge`
- `next`

Backends that do not support ordered iteration SHOULD return `OBI_STATUS_UNSUPPORTED` for
cursor-related functions and clear `OBI_DB_KV_CAP_CURSOR`.

---

## 3. Conformance

Required:

- open DB
- begin transaction
- get/put/delete
- commit/abort/destroy

Optional (advertised via caps):

- cursors
- provider-specific `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_db_kv_v0.h`

---

## Global Q&A

**Q: Why no range deletes, snapshots, or column families?**  
Those features are backend-specific and tend to expand the surface quickly. v0 standardizes the
common denominator. Add additional DB profiles (or a v1 expansion) when multiple providers need the
same advanced feature.

