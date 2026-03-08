# OBI Time Date/Time Profile
## OBI Profile: `obi.profile:time.datetime-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:time.datetime-0`  
**Status:** Draft  
**Last Updated:** 2026-03-05

---

## 1. Nontechnical Summary

This profile provides a portable, deterministic way to:

- parse and format RFC3339 timestamps,
- convert between Unix epoch nanoseconds and civil (broken-down) time,
- apply time zones when supported.

The intent is to let hosts avoid platform-specific time APIs for common app needs (logging, file
formats, protocol timestamps) while keeping the ABI small and FFI-friendly.

---

## 2. Technical Details

### 2.1 Data model

- An instant in time is represented as `int64_t unix_ns`: nanoseconds since the Unix epoch
  (1970-01-01T00:00:00Z).
- A civil time is represented by `obi_time_civil_v0` (year/month/day hour/minute/second/nanosecond).
- A time zone is specified by `obi_time_zone_spec_v0`:
  - `UTC`
  - fixed numeric offset in minutes
  - optional IANA name (e.g. `America/Chicago`)
  - optional local system zone

### 2.2 RFC3339 parse/format

Providers MUST implement:

- `parse_rfc3339()` for strict RFC3339 timestamps
- `format_rfc3339()` which preserves full nanosecond precision (no rounding), so parsing the
  formatted output can round-trip exactly.

### 2.3 Civil <-> instant conversion

Providers MUST implement:

- `unix_ns_to_civil()` at least for:
  - `OBI_TIME_ZONE_UTC`
  - `OBI_TIME_ZONE_FIXED_OFFSET_MINUTES`
- `civil_to_unix_ns()` at least for:
  - `OBI_TIME_ZONE_UTC`
  - `OBI_TIME_ZONE_FIXED_OFFSET_MINUTES`

For IANA or local time zones, civil-to-instant conversion can be ambiguous or invalid during DST
transitions. Providers MUST honor `OBI_TIME_CIVIL_TO_UNIX_*` flags to disambiguate or fail.

### 2.4 Determinism notes

- RFC3339 parse/format is deterministic.
- Time zone conversion based on the IANA time zone database may vary by tzdb version. Hosts SHOULD
  treat IANA-zone support as optional and rely on fixed offsets for strict reproducibility.

---

## 3. Conformance

Required:

- RFC3339 parse + format
- Unix ns <-> civil conversion for UTC and fixed offsets
- arithmetic helpers: `add_ns`, `diff_ns`, `cmp`

Optional (advertised via caps):

- IANA time zones by name: `OBI_TIME_DATETIME_CAP_TZ_IANA`
- local system time zone: `OBI_TIME_DATETIME_CAP_TZ_LOCAL`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_time_datetime_v0.h`

---

## Global Q&A

**Q: Why not rely only on `obi_host_v0.now_ns()`?**  
`now_ns()` provides monotonic/wall timestamps, but applications still need parsing/formatting and
civil-time conversions for file formats and user-facing timestamps.

**Q: Why require fixed-offset conversions?**  
Fixed offsets are predictable, deterministic, and sufficient for most interchange formats.
IANA time zone support is valuable but necessarily depends on tzdb versioning.

