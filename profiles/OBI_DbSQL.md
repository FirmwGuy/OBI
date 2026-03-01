# OBI DB SQL Profile
## OBI Profile: `obi.profile:db.sql-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:db.sql-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a small SQL database interface in the SQLite family:

- open a connection
- prepare statements
- bind parameters
- step through results
- read columns by type

Typical providers:

- SQLite wrappers
- other embeddable engines that support a similar prepare/bind/step model

This profile is for local persistence and tooling; it is not an ORM or a remote SQL protocol.

---

## 2. Technical Details

### 2.1 Connection model

The host opens a connection using a provider-defined path/URI.

The connection supports:

- `prepare` for parameterized statements
- `exec` for one-shot statements that do not return rows

### 2.2 Statement model

Binding is 1-based (SQLite style). Column indexing is 0-based.

`step` advances the statement:

- when a row is available, `out_has_row=true`
- when complete, `out_has_row=false`

Column views returned by `column_text_utf8` / `column_blob` are provider-owned and valid until the
next `step`, `reset`, or statement destruction.

---

## 3. Conformance

Required:

- open connection
- prepare/exec
- bind (at least null/int64/double/text/blob)
- step/reset/clear_bindings
- column_count/column_type and value accessors
- destroy

Optional (advertised via caps):

- named parameter binding (`bind_parameter_index`)
- provider-specific `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_db_sql_v0.h`

---

## Global Q&A

**Q: Why not standardize schema introspection or migrations?**  
Those are higher-level policies and vary by application. v0 focuses on the portable core needed to
execute statements and read results.

