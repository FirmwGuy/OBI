# OBI IPC Bus Profile
## OBI Profile: `obi.profile:ipc.bus-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:ipc.bus-0`  
**Status:** Draft  
**Last Updated:** 2026-03-06

---

## 1. Nontechnical Summary

This profile standardizes a minimal message-bus client/service surface for local IPC:

- connect to a session, system, or custom bus endpoint
- call methods on named objects/interfaces
- subscribe to incoming signals/events
- optionally emit signals
- optionally request/release a well-known bus name

Typical providers:

- `sd-bus` / libsystemd
- `libdbus-1`
- platform shims mapping to XPC, named pipes, or similar local IPC systems

This profile is intentionally smaller than native D-Bus. v0 focuses on the portable control-plane
mechanics needed by hosts, tools, and service coordinators.

---

## 2. Technical Details

### 2.1 Connection scopes

`connect` supports three endpoint kinds:

- session bus
- system bus
- custom address

When `OBI_IPC_BUS_CAP_CUSTOM_ADDRESS` is not advertised, providers may reject custom-address
connects with `OBI_STATUS_UNSUPPORTED`.

### 2.2 Call model

Calls are described by:

- destination name
- object path
- interface name
- member (method) name
- `args_json`

`args_json` is a UTF-8 JSON array representing positional arguments. For example:

```json
["org.example.service", 7, true]
```

Replies return:

- `results_json`: a UTF-8 JSON array of return values
- `remote_error_name`: optional backend-native remote error identifier
- `error_details_json`: optional JSON detail payload for remote failures

This keeps v0 language-neutral and portable without standardizing the full native D-Bus type
system.

### 2.3 Signal model

Hosts subscribe with a filter over:

- sender name
- object path
- interface name
- member name

Empty fields are wildcards.

Subscriptions yield provider-owned signal events containing:

- sender name
- object path
- interface name
- member name
- `args_json` as a UTF-8 JSON array

### 2.4 Optional service-side features

When advertised via caps, providers may support:

- `emit_signal_json`
- `request_name`
- `release_name`

These are useful for hosts that need to participate as named services or broadcasters, not only as
clients.

### 2.5 Cancellation and pumps

When `OBI_IPC_BUS_CAP_CANCEL` is advertised, providers SHOULD honor cancellation tokens for
connect/call/wait operations.

When `OBI_IPC_BUS_CAP_REQUIRES_PUMP` is advertised, progress may depend on an accompanying
`obi.profile:core.pump-0` provider.

### 2.6 Deliberate non-goals for v0

This version does not standardize:

- native variant/signature trees
- file-descriptor passing
- object export/introspection metadata
- authentication policy beyond whatever the backend bus already requires

Those can be added in a future profile revision once hosts converge on real portability needs.

### 2.7 Ownership

- Connect/call/filter inputs are borrowed for the duration of the call only.
- Bus connections and subscriptions are provider-owned handles released by `destroy`.
- Reply and signal payload strings are provider-owned and released by their `release` callback.

---

## 3. Conformance

Required:

- `connect`
- connection `call_json`
- connection `subscribe_signals`
- subscription `next`
- subscription `destroy`
- connection `destroy`

Optional (advertised via caps):

- custom addresses
- signal emission
- well-known name ownership
- provider-specific `options_json`
- cancellation support
- pump-driven progress

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_ipc_bus_v0.h`
- `abi/obi_core_v0.h` (cancellation token and diagnostic types)

---

## Global Q&A

**Q: Why JSON arrays instead of native D-Bus signatures and variants?**  
Because JSON arrays are easy to produce/consume from many languages and runtimes. v0 standardizes
portable bus mechanics first; richer type fidelity can be added later if needed.

**Q: Does this replace full D-Bus bindings for advanced services?**  
No. If a host needs full native type systems, FD passing, or introspection/export mechanics, it may
still use a backend-specific layer. This profile covers the common portable subset.

