# OBI Net TLS Profile
## OBI Profile: `obi.profile:net.tls-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:net.tls-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal TLS session interface:

- create a TLS client session over an existing transport (TCP socket abstraction)
- perform a handshake
- read/write encrypted application bytes
- optional ALPN and certificate inspection

Typical providers:

- OpenSSL wrappers
- GnuTLS wrappers
- mbedTLS wrappers

This profile is designed for hosts that need a portable TLS surface for custom protocols beyond
HTTP/WebSocket.

---

## 2. Technical Details

### 2.1 Transport model

The host provides a transport reader/writer implementing the OBI core streaming interfaces
(`obi_reader_v0`, `obi_writer_v0`).

The TLS session retains and uses these transport handles for its lifetime. The transport is
caller-owned and MUST remain valid until the TLS session is destroyed.

TLS providers MUST NOT destroy the transport reader/writer.

### 2.2 Handshake model

The host drives the handshake by calling `handshake(timeout_ns, out_done)` until complete.

Providers MAY block for up to `timeout_ns` depending on the underlying transport implementation.

### 2.3 Read/write model

After the handshake completes, the host calls:

- `read` to obtain decrypted application bytes
- `write` to send encrypted application bytes

Providers MUST document any thread-safety constraints for session handles.

---

## 3. Conformance

Required:

- create client session
- handshake
- read/write
- shutdown (may return `OBI_STATUS_UNSUPPORTED` if not implemented)
- destroy

Optional (advertised via caps):

- ALPN negotiation and retrieval
- custom CA bundles
- client certificates
- peer certificate retrieval
- provider-specific `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_net_tls_v0.h`
- `abi/obi_core_v0.h`

---

## Global Q&A

**Q: Why not embed TCP sockets as part of OBI core?**  
Different hosts have different socket abstractions and policies (blocking vs nonblocking, event
loops, sandboxing). This profile is layered over `obi_reader_v0`/`obi_writer_v0` so hosts can adapt
their transport strategy without changing TLS semantics.

