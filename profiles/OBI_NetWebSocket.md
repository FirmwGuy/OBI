# OBI WebSocket Profile
## OBI Profile: `obi.profile:net.websocket-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:net.websocket-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal WebSocket client interface:

- connect to a WebSocket URL
- send text/binary messages
- receive incoming messages
- close the connection

Typical providers:

- libsoup (GLib main loop)
- libcurl websockets (where available)
- dedicated websocket libraries wrapped behind OBI

This profile is designed to coexist with `obi.profile:core.pump-0` so providers can be integrated
without importing a specific event loop.

---

## 2. Technical Details

### 2.1 Connect model

Providers MUST support a synchronous `connect`. Providers MAY also support `connect_async` if they
need explicit progress via polling/pumps.

### 2.2 Message model

Incoming messages are returned as:

- a message opcode (text/binary/ping/pong/close)
- a provider-owned payload reader (so large payloads do not require buffering)

### 2.3 Ownership

- Outgoing payload bytes/readers are borrowed for the duration of the send call only.
- Incoming message payload readers are provider-owned and must be destroyed by the host when done.
- Connection handles are provider-owned and destroyed by `destroy`.

---

## 3. Conformance

Required:

- `connect`
- connection: `send`, `receive`, `close`, `destroy`

Optional (advertised via caps):

- `connect_async` with a connect job
- pump-driven progress (`OBI_WS_CAP_REQUIRES_PUMP`)

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_net_websocket_v0.h`

---

## Global Q&A

**Q: Why payloads as readers instead of a byte buffer?**  
To avoid forcing buffering in the provider for large messages and to simplify streaming.

**Q: Where do reconnection policies live?**  
In the host. This profile defines the runtime mechanics, not the policy.

