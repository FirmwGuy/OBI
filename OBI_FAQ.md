# OBI FAQ
## Frequently Asked Questions for Omni Backstage Interface

**Repository:** OBI  
**Document Type:** FAQ (informative)  
**Status:** Draft  
**Last Updated:** 2026-03-06

---

## 1. Nontechnical Summary

OBI exists to make it normal to swap implementations at runtime without rewriting your system:

- use SDL today, raylib tomorrow,
- use libcurl today, libsoup tomorrow,
- use ffmpeg today, gstreamer tomorrow,
- without turning your codebase into `#ifdef` sprawl or a pile of one-off adapters.

OBI does this by specifying small, versioned runtime interfaces ("profiles") and a provider model.

---

## 2. Technical Notes (How to Think About OBI)

### 2.1 OBI is "integration mechanics", not "universal semantics"

OBI standardizes:

- ABI stability rules (versioning + struct sizing)
- ownership and lifetimes
- error reporting and logging surfaces
- capability discovery
- async and "pump" integration

OBI does not try to standardize every domain's semantics. A math profile is not a GUI profile.
Profiles are added only when there is a real need for a stable contract across multiple
implementations.

### 2.2 Interface shapes matter more than domains

Most third-party libraries fall into a small number of interface shapes:

- pure/stateless functions (hashes, compression codecs, some kernels)
- stateful contexts (DB handles, font faces, decoder instances)
- streaming I/O (archives, HTTP bodies, demux/decoders)
- event-loop driven (GLib/libsoup, curl multi, gstreamer)
- pipeline/graph engines (gstreamer pipelines, filter graphs)

OBI profiles are designed around these shapes, so they can be implemented by many libraries.

### 2.3 OBI vs CEP L0 "handles"

CEP L0 already knows how to represent external resources as opaque HANDLE/STREAM cells with
snapshot/restore and effect journaling.

OBI does not replace that. OBI decides:

- which runtime provider is used for a profile,
- how to call it safely,
- how to integrate async/pumps.

CEP decides:

- whether a call is permitted under policy and budgets,
- what gets recorded as deterministic evidence for replay.

### 2.4 OBI vs OGIF

- OGIF is for introspection/control as a graph surface across transports.
- OBI is for in-process runtime interfaces and provider selection.

An OGIF endpoint can report which OBI providers/profiles are active, but OGIF should not embed
OBI's ABI as its core meaning.

---

## 3. Q&A

**Q: Is OBI a plugin system?**  
It can be used like one, but OBI is not *just* dynamic loading. It is a contract: a provider can be
statically linked, dynamically loaded, or built-in. The important part is that callers interact via
versioned profiles with explicit lifetimes and caps.

**Q: Why not just use one "best" library for each domain?**  
Because the "best" library depends on platform, policy, licensing, performance constraints, and
deployment. OBI exists to keep those choices modular and reversible.

**Q: How do hosts select providers under licensing constraints (MIT-only, LGPL-only, GPL allowed, etc.)?**  
Licensing decisions live in the host's configuration and policy plane, not inside profile APIs.
In practice, hosts select providers by:

- choosing which provider modules to ship/load, and
- applying a selection policy (preferred/denied/bindings).

For automation, providers should implement `describe_json` metadata including effective license
information for the provider module and its key dependencies. See `OBI_PROVIDER_GUIDE.md` section
2.7 for recommended fields and coarse `license_class` buckets.

**Q: How should providers report errors, warnings, and debug information without hijacking stderr/stdout?**  
Use `obi_status` as the primary result, then supplement it with host-directed diagnostics:

- structured diagnostics via `obi_host_v0.emit_diagnostic` when available,
- best-effort human-readable logging via `obi_host_v0.log`,
- profile-specific borrowed `last_error_utf8` views only when the profile documents lifetime rules.

Conforming providers should not write unsolicited diagnostics to process-global `stdout`/`stderr`
and should not terminate the embedding host process as an error-reporting mechanism.

**Q: Can hosts reject providers based on operational behavior, not just licensing?**  
Yes. Providers may expose host-safety and diagnostics behavior in `describe_json()` metadata (for
example direct stdio usage, process-termination policy, and whether they emit structured
diagnostics). Hosts may use that metadata as part of provider selection policy.

**Q: How do we avoid "leaky abstractions"?**  
By being honest about what is stable:

- OBI profiles define only the minimal cross-implementation contract.
- Capabilities expose optional features rather than pretending everything is available.
- If a domain truly cannot be abstracted cleanly, it should not be forced into a profile.

**Q: How does OBI handle event loops (curl multi, libsoup/GLib, gstreamer)?**  
OBI uses the `obi.profile:core.pump-0` profile for "step-driven" progress. Providers that require a
loop must expose a pump and document how the host should drive it (thread-affinity, step cadence,
shutdown rules).

**Q: Does OBI guarantee determinism?**  
No. OBI is a runtime interface. Determinism is a host property (for example CEP) that requires
explicit effect logging, replay rules, and policy enforcement. OBI profiles should make it possible
to capture stable bytes/streams/hashes when determinism is required.

**Q: Where do security and authorization live?**  
In the host and its policy planes (CEP enclaves/caps/budgets; OGIF OmniPolicy at the interface).
OBI profiles may expose knobs like "verify TLS peer", but permission to use them is not granted by
OBI.
