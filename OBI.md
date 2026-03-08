# Omni Backstage Interface (OBI)
## Versioned Runtime Profiles for Modular Integrations

**Repository:** OBI  
**Document Type:** Core specification (normative)  
**Status:** Draft / Experimental  
**Spec Version:** v0.1.0 (Draft)  
**Last Updated:** 2026-03-06

---

## 1. Nontechnical Summary

OBI standardizes how a system integrates third-party libraries and subsystems behind
**swappable runtime providers**, using **versioned profiles** with explicit contracts for:

- capability discovery (what is supported),
- lifetimes and ownership (who frees what),
- error reporting (status-first, host-directed diagnostics, no ad-hoc stderr logging),
- threading and event-loop requirements,
- minimal, stable ABI shapes (C-compatible).

OBI is meant to be used across the TCA family:

- **OGIF** is the frontstage membrane (declarative graph interface).
- **OBI** is the backstage membrane (imperative runtime interfaces).
- **CEP** can use OBI providers to perform real work while keeping determinism via its own
  effect logging / replay discipline.

OBI is not an attempt to "unify all semantics" (math, media, GUI, networking, DBs). It
standardizes the *integration mechanics* so each domain can define a profile only when it
actually needs one.

---

## 2. Relationship to OGIF and CEP

### 2.1 OGIF vs OBI

- OGIF answers: "What exists, what relationships exist, what can be invoked, what happened?"
- OBI answers: "Which implementation do we run, and how do we call it correctly at runtime?"

In a typical stack:

- OGIF exposes introspection/control for tools and AIs.
- OBI is used internally by the runtime to swap providers (SDL vs raylib, curl vs libsoup, etc.).

### 2.2 CEP L0 vs OBI

CEP L0 already provides:

- opaque external resources as `HANDLE` / `STREAM` cells,
- adapter vtables (`cepLibraryOps`) with snapshot/restore and journaling,
- deterministic serialization and replay plumbing.

OBI is complementary:

- OBI selects and binds *runtime implementations* as providers/profiles.
- CEP decides which OBI calls are allowed and how to record them as deterministic effects.

---

## 3. Core Concepts

### 3.1 Provider

A **provider** is an implementation module that can serve one or more profiles. Examples:

- a "curl provider" implementing `obi.profile:net.http_client-0`,
- an "SDL provider" implementing `obi.profile:gfx.window_input-0` and `obi.profile:gfx.render2d-0`.

Providers are expected to:

- publish a stable provider ID string,
- implement profile discovery,
- declare capability bits for each profile,
- obey ownership and threading contracts.

### 3.2 Profile

A **profile** is a versioned interface for one domain slice (for example HTTP, 2D rendering,
text shaping).

Profiles have:

- a **profile ID** string (example: `obi.profile:net.http_client-0`),
- an **ABI major** (breaking changes bump major and change the ID suffix),
- a capability bitset (fine-grained optional features),
- a vtable whose first fields support size/version checks.

### 3.3 Host

The **host** is the runtime embedding OBI providers (CEP, a test harness, an app). The host:

- supplies allocator/log/diagnostic/time callbacks (so providers do not assume `malloc`/stderr),
- loads providers (statically or dynamically),
- selects which provider(s) to use per profile at runtime.

### 3.4 Capabilities

OBI uses capability bitsets for:

- optional API functions (async vs sync, streaming support, scissor, etc.),
- behavior declarations (thread-safe, requires pump, spawns threads).

Capabilities are not "permissions". Authorization and policy live elsewhere (CEP policy, OGIF
policy plane, etc.).

### 3.5 Lifetimes and Ownership

OBI requires explicit ownership rules:

- Inputs are borrowed for the duration of the call unless explicitly stated.
- Outputs either:
  - are caller-owned (caller frees via host allocator), or
  - are provider-owned and must be released by a release callback or vtable function.

Profiles MUST document:

- what must be copied before returning (especially for async work),
- which objects can be used concurrently and on which threads,
- whether a pump is required to make progress.

---

## 4. ABI and Versioning Rules

### 4.1 ABI shape conventions

OBI reference headers live under `abi/`. The conventions are:

- Profile "handle" structs are shallow (typically `{ api, ctx }`).
- Vtables include `abi_major`, `abi_minor`, and `struct_size` fields.
- Callers MUST check ABI major and struct sizes before invoking optional fields.

### 4.2 Compatibility rules

- **Major bump** (and profile ID suffix bump) is required for:
  - changing function signatures,
  - changing struct layout without `struct_size` protection,
  - changing meaning of existing fields in a breaking way.

- **Minor bump** is allowed for:
  - adding new functions at the end of a vtable,
  - adding new capability bits,
  - clarifying semantics without breaking existing implementations.

### 4.3 Strings and encodings

- OBI strings are UTF-8, NUL-terminated.
- Profile IDs are ASCII and treated as stable identifiers.

---

## 5. Error Model

OBI APIs return an `obi_status` code (see `abi/obi_core_v0.h`). This is the authoritative
machine-readable result channel.

Supplementary diagnostics MAY be emitted through host callbacks or profile-specific UTF-8 error
views, but they do not replace `obi_status`.

Providers MUST NOT:

- write unsolicited diagnostics to the embedding process's `stdout` or `stderr`,
- terminate the embedding host process (`exit`, `abort`, `quick_exit`, etc.) as an error-reporting
  mechanism,
- require callers to free ad-hoc heap-allocated error strings through undocumented conventions.

Providers SHOULD:

- emit structured diagnostics through the host diagnostic callback when available,
- use the host log callback only for human-oriented best-effort text,
- expose profile-specific `last_error_utf8` or equivalent views only when the profile documents the
  exact lifetime and ownership rules.

An OBI "fatal" condition means the current call, object, provider instance, or runtime can no
longer proceed safely. It never means "terminate the host process."

---

## 6. Threading and Event-Loop Integration

Many libraries require a pump or a main loop (GLib/libsoup, curl multi, gstreamer). OBI standardizes
this via the `obi.profile:core.pump-0` profile.

Rules:

- If a provider requires pumping to make progress, it MUST expose the pump profile and document it.
- Providers MUST declare whether they are thread-safe; if not, the host MUST serialize calls.

---

## 7. Reference ABI Artifacts

This repository includes reference C headers under `abi/`:

- They are normative for field layouts and profile IDs.
- They are not a full SDK and do not include implementations.

Companion documents in this repository:

- `OBI_Profiles.md` (recommended baseline profile set)
- `OBI_FAQ.md` (FAQ and common clarifications)
- `OBI_PROVIDER_GUIDE.md` (provider authoring and hosting guidance)
- `OBI_ABI_CONVENTIONS.md` (stable ABI rules and patterns)
- `OBI_CONFORMANCE.md` (host/provider conformance checklists)

---

## Global Q&A

**Q: Is OBI a replacement for OGIF?**  
No. OGIF is for declarative introspection/control across transports. OBI is for imperative runtime
integration inside implementations.

**Q: Is OBI trying to abstract every library in the world?**  
No. OBI defines stable integration mechanics and only adds domain profiles when needed.

**Q: How does this relate to CEP determinism?**  
OBI does not make external effects deterministic by itself. CEP (or another host) must decide when
effects are allowed and how to record/replay them. OBI profiles must make it *possible* to capture
inputs/outputs in stable forms (bytes/streams/hashes) when determinism is required.
