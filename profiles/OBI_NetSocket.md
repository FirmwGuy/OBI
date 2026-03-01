# OBI Net Socket Profile
## OBI Profile: `obi.profile:net.socket-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:net.socket-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes basic TCP sockets:

- connect to a remote host/port (returning a reader/writer transport)
- optionally connect by explicit IP address + port
- optionally listen and accept incoming connections
- optionally apply timeouts and cancellation

Typical providers:

- POSIX sockets
- WinSock
- libuv wrappers
- WASI socket extensions (when available)

This profile is intended as a transport primitive for higher-level protocols (for example
`obi.profile:net.tls-0`).

---

## 2. Technical Details

### 2.1 Transport shape

TCP connections are returned as:

- an `obi_reader_v0` (read bytes)
- an `obi_writer_v0` (write bytes)

These are suitable as the underlying transport for `obi.profile:net.tls-0`.

Providers MUST ensure the underlying connection remains usable until both the reader and writer are
destroyed.

### 2.2 Connecting

The primary entrypoint is:

- `tcp_connect(host, port, params, out_reader, out_writer)`

When `OBI_SOCKET_CAP_TCP_CONNECT_ADDR` is advertised, providers also support:

- `tcp_connect_addr(remote, params, out_reader, out_writer)`

### 2.3 Listening and accepting (Optional)

When `OBI_SOCKET_CAP_TCP_LISTEN` is advertised, providers support:

- `tcp_listen(params, out_listener)`
- `listener.accept(timeout_ns, cancel_token, ...)`

`accept()` returns `OBI_STATUS_OK` and sets `out_accepted`. When `out_accepted=false`, no
connection was accepted within the timeout.

### 2.4 Timeouts and cancellation (Optional)

`timeout_ns==0` means provider default.

When `OBI_SOCKET_CAP_CANCEL` is advertised and `cancel_token.api != NULL`, providers SHOULD return
`OBI_STATUS_CANCELLED` when cancellation is requested.

---

## 3. Conformance

Required:

- `tcp_connect`

Optional (advertised via caps):

- connect by explicit socket address
- listen/accept
- cancellation support
- provider-specific `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_net_socket_v0.h`
- `abi/profiles/obi_net_types_v0.h`
- `abi/obi_core_v0.h` (reader/writer and cancellation token types)

---

## Global Q&A

**Q: Why does this profile return reader/writer instead of a bespoke socket handle?**  
Readers/writers are already the cross-profile streaming contract in OBI. Returning transports in
that shape keeps the socket profile small and makes it directly usable by TLS and other layers.

