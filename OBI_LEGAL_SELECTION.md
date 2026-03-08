# OBI Legal Selection

**Document Type:** Specification Guidance  
**Status:** Draft  
**Last Updated:** 2026-03-08

---

This document defines the legal metadata model and selector semantics used when hosts or runtimes
need to choose between multiple OBI providers at runtime.

It exists because a single coarse "license class" is not enough for real deployments:

- copyleft severity,
- patent posture,
- dependency closure,
- and route-specific backend choices

can all differ independently.

The canonical typed ABI shapes for this model live in `OBI-ABI/include/obi/obi_legal_v0.h`. The
optional provider callback that exposes structured legal metadata is
`obi_provider_api_v0.describe_legal_metadata`.

---

## 1. Terms

### 1.1 Module License

The license of the OBI provider module itself as shipped.

Example: an OBI wrapper module may be MPL-2.0 even when it drives LGPL, GPL, AGPL, Apache-2.0, or
BSD/MIT/Zlib dependencies.

### 1.2 Effective License

The effective legal posture of selecting the provider for execution.

This is the field hosts and runtimes should use for policy decisions when no narrower route has
been selected.

If a provider has materially different legal outcomes for different execution paths, the provider
must either:

- expose route-specific legal metadata, or
- report the provider-wide `effective_license` conservatively (including `unknown` when needed).

### 1.3 Copyleft Class

Copyleft severity is a policy axis of its own:

- `permissive`
- `weak_copyleft`
- `strong_copyleft`
- `unknown`

This axis does not encode patent posture.

### 1.4 Patent Posture

Patent posture is a separate policy axis:

- `ordinary`
- `explicit_grant`
- `sensitive`
- `restricted`
- `unknown`

These are policy hints, not legal advice. The goal is to let hosts express conservative deployment
rules without flattening everything into a single string bucket.

### 1.5 Dependency Closure

Providers should describe the actual dependency closure relevant to the shipped build:

- required build-time linked components,
- required runtime components,
- optional runtime components,
- and route-scoped components.

This matters because a provider may be loadable on a machine but still only have some legal routes
available there.

### 1.6 Route

A route is a narrower execution path whose legal posture differs materially from the provider-wide
default.

Typical examples:

- FFmpeg built with both LGPL-safe and GPL-only codec paths
- GStreamer providers whose actual pipeline depends on installed plugin families or elements
- codec-specific encode/decode paths where H.264/H.265 policy differs from Opus/Vorbis/PNG/JPEG

Routes are provider-local descriptors. They are usually attached to:

- one profile, and
- zero or more generic selector pairs such as `codec=h264`, `container=mp4`, or `backend=gst-libav`.

---

## 2. Built-In Presets

Built-in presets standardize only the copyleft-severity axis:

- `permissive_only`
- `up_to_weak_copyleft`
- `up_to_strong_copyleft`

These presets do not silently decide patent posture or unknown-handling for the host. Those remain
independent policy inputs.

This is intentional. Two hosts may both allow `up_to_weak_copyleft` and still disagree on:

- whether `unknown` is acceptable,
- whether patent-sensitive routes are acceptable,
- or whether optional runtime components are acceptable.

---

## 3. Selectability

A preset or custom legal policy is **selectable** only if every required profile requirement has at
least one satisfying provider/route on the current machine.

That rule is evaluated against:

- the providers actually loaded or discoverable,
- their current dependency closure,
- the routes currently available,
- and the host's requested profile set and optional selectors.

This is the key operational rule:

- If all relevant backends are present, several presets may be selectable.
- If only some backends are present, only the still-satisfiable presets should be reported.
- If one policy-compatible route remains, the runtime should report exactly that.
- `unknown` must never be treated as safe unless the host explicitly opts in.

---

## 4. Route-Sensitive Providers

Providers wrapping route-sensitive stacks (FFmpeg, GStreamer, browser codec APIs, plugin-driven
multimedia frameworks, optional TLS engines, etc.) must not pretend that one provider-wide string
fully captures their legal behavior.

They should follow these rules:

1. `module_license` describes the wrapper module itself.
2. `effective_license` describes provider selection with no narrower route chosen.
3. `routes[]` describes narrower paths when those paths materially differ.
4. If the provider cannot know the actual route yet, use conservative data or `unknown`.
5. If route differences are too large to summarize safely in one provider, split the provider into
   multiple provider IDs/modules.

For example, a provider that can decode:

- `codec=opus` via a permissive/ordinary route, and
- `codec=h264` via a strong-copyleft or patent-sensitive route

must not expose only one flattened "license class" and expect host policy to remain correct.

---

## 5. Structured ABI Model

`obi_legal_v0.h` defines:

- legal fact terms (`obi_legal_term_v0`)
- dependency closure entries (`obi_legal_dependency_v0`)
- route metadata (`obi_legal_route_v0`)
- provider-wide legal metadata (`obi_provider_legal_metadata_v0`)
- selector policy and request/result shapes (`obi_legal_selector_policy_v0`,
  `obi_legal_requirement_v0`, `obi_legal_plan_item_v0`, `obi_legal_plan_v0`)

This lets runtimes implement:

- "show me all available providers and their legal facts"
- "is `permissive_only` selectable for this profile set on this machine?"
- "which provider/route would satisfy `media.av_decode-0` with `codec=h264` under a weak-copyleft
  ceiling?"

without inventing private JSON parsers and one-off policy schemas.

---

## 6. JSON Mapping

`describe_json()` remains useful for tooling, debugging, and older runtimes.

When JSON metadata is emitted, the preferred v0 shape is:

```json
{
  "provider_id": "obi.provider:media.gstreamer",
  "provider_version": "0.2.0",
  "profiles": ["obi.profile:media.av_decode-0", "obi.profile:media.demux-0"],
  "module_license": {
    "spdx_expression": "MPL-2.0",
    "copyleft_class": "weak_copyleft",
    "patent_posture": "ordinary"
  },
  "effective_license": {
    "spdx_expression": "unknown",
    "copyleft_class": "unknown",
    "patent_posture": "unknown"
  },
  "dependency_closure": [
    {
      "dependency_id": "gstreamer-core",
      "name": "gstreamer-1.0",
      "version": "1.24.x",
      "relation": "required_runtime",
      "legal": {
        "spdx_expression": "LGPL-2.1-or-later",
        "copyleft_class": "weak_copyleft",
        "patent_posture": "ordinary"
      }
    }
  ],
  "routes": [
    {
      "route_id": "decode:h264:gst-libav",
      "profile_id": "obi.profile:media.av_decode-0",
      "selectors": [{"key": "codec", "value": "h264"}],
      "availability": "available",
      "effective_license": {
        "spdx_expression": "GPL-2.0-or-later",
        "copyleft_class": "strong_copyleft",
        "patent_posture": "sensitive"
      }
    }
  ]
}
```

Legacy guidance:

- `license` may be treated as a legacy alias for `module_license`
- `deps` may be treated as a legacy alias for `dependency_closure`
- `spdx` may be treated as a legacy alias for `spdx_expression`

New metadata should not use the old overloaded `license_class=patent` convention. Patent posture is
now a separate axis.

---

## 7. Guidance for Runtime Implementations

Runtimes such as `libobi` should expose three distinct layers:

1. provider facts:
   loaded providers and their structured legal metadata
2. policy input:
   built-in preset or custom selector policy
3. feasibility result:
   whether a requested profile set is selectable under that policy on this machine, with the chosen
   provider/route or the blocking reason per requirement

That separation keeps hosts in control while still allowing a standard answer to:

"What can I legally select here right now?"

