# OBI OS Process Profile
## OBI Profile: `obi.profile:os.process-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:os.process-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes spawning and supervising child processes:

- spawn a process with argv
- optionally override environment variables and working directory
- optionally capture stdin/stdout/stderr as streams
- wait for exit with timeout (and optional cancellation)
- optionally terminate a process

Typical providers:

- POSIX (`posix_spawn`, `fork/exec`, `waitpid`)
- Win32 (`CreateProcessW`, `WaitForSingleObject`, `TerminateProcess`)
- sandboxed runtimes that expose a restricted "process host" surface

This profile is useful for toolchains, pipelines, and "driver" hosts that orchestrate external
commands.

---

## 2. Technical Details

### 2.1 Spawn model

The host calls `spawn(params, ...)` with:

- `program`: the executable to run
- `argv`: an argument vector (borrowed for the duration of the call)
- optional `working_dir`
- optional `env_overrides`

`argv[0]` is treated as a display name when present, but providers MUST use `program` to locate the
executable.

### 2.2 Environment overrides (Optional)

When `OBI_PROCESS_CAP_ENV_OVERRIDES` is advertised, providers apply `env_overrides`:

- setting a key/value sets the variable
- an entry with `value.data==NULL && value.size==0` removes the variable

If `OBI_PROCESS_SPAWN_CLEAR_ENV` is set, providers SHOULD start from an empty environment before
applying overrides.

### 2.3 Working directory (Optional)

When `OBI_PROCESS_CAP_WORKING_DIR` is advertised, providers use `working_dir` as the child process
working directory.

### 2.4 Stdio piping (Optional)

When `OBI_PROCESS_CAP_STDIO_PIPES` is advertised, the host may request pipes via spawn flags:

- `OBI_PROCESS_SPAWN_STDIN_PIPE` => provider returns a writer for the child's stdin
- `OBI_PROCESS_SPAWN_STDOUT_PIPE` => provider returns a reader for the child's stdout
- `OBI_PROCESS_SPAWN_STDERR_PIPE` => provider returns a reader for the child's stderr
- `OBI_PROCESS_SPAWN_STDERR_TO_STDOUT` => stderr is redirected into stdout (provider-defined)

If a pipe is not requested or not supported, providers set the corresponding out stream to
`{ .api=NULL, .ctx=NULL }`.

### 2.5 Waiting and cancellation

Process waiting is performed via `process.wait(timeout_ns, cancel_token, ...)`.

The wait call:

- MUST be non-blocking when `timeout_ns==0` (poll semantics)
- otherwise MAY block up to `timeout_ns`

When `OBI_PROCESS_CAP_CANCEL` is advertised and `cancel_token.api != NULL`, providers SHOULD return
`OBI_STATUS_CANCELLED` when cancellation is requested.

### 2.6 Termination (Optional)

When `OBI_PROCESS_CAP_KILL` is advertised, providers implement `process.kill()` as a best-effort
termination request.

---

## 3. Conformance

Required:

- `spawn`
- `process.wait`
- `process.destroy`

Optional (advertised via caps):

- stdio pipes
- working directory
- environment overrides
- termination (`kill`)
- cancellation support (`cancel_token`)
- provider-specific spawn options via `options_json`

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_os_process_v0.h`
- `abi/obi_core_v0.h` (reader/writer and cancellation token types)

---

## Global Q&A

**Q: Why is `wait(timeout_ns=0)` required to be non-blocking?**  
It gives hosts a portable "poll" primitive so they can integrate process supervision into their own
schedulers and event loops without dedicating threads.

