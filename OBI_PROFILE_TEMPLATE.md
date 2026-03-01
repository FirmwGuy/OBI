# OBI Profile Template
## A Template for Writing New OBI Profiles and ABIs

**Repository:** OBI  
**Document Type:** Template (informative)  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

OBI works when profiles stay:

- small and implementable,
- explicit about ownership and lifetimes,
- honest about optionality via capability bits,
- versioned with clear compatibility rules.

This document provides a template for new profile documents and their ABI headers.

---

## 2. Templates

### 2.1 Markdown profile spec template

```markdown
# OBI <Profile Name> Profile
## OBI Profile: `obi.profile:<namespace>.<name>-<major>`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:<namespace>.<name>-<major>`  
**Status:** Draft  
**Last Updated:** YYYY-MM-DD

---

## 1. Nontechnical Summary

Explain what the profile is for in plain language.

---

## 2. Technical Details

Define objects/handles, call ordering, threading rules, determinism notes, and failure modes.

---

## 3. Conformance

List required functions and optional capabilities.

---

## 4. ABI Reference

- `abi/profiles/<header>.h`

---

## Global Q&A

Add the most common pitfalls and clarifications.
```

### 2.2 C ABI header skeleton

```c
/* SPDX-License-Identifier: CC-BY-SA-4.0 */
/* SPDX-FileCopyrightText: © 2026–present Victor M. Barrientos <firmw.guy@gmail.com> */

#ifndef OBI_PROFILE_<NAME>_V0_H
#define OBI_PROFILE_<NAME>_V0_H

#include "../obi_core_v0.h"

#ifdef __cplusplus
extern "C" {
#endif

#define OBI_PROFILE_<NAME>_V0 "obi.profile:<namespace>.<name>-0"

enum {
  /* Capability bits */
};

typedef struct obi_<name>_v0 obi_<name>_v0;

typedef struct obi_<name>_api_v0 {
  uint32_t abi_major;
  uint32_t abi_minor;
  uint32_t struct_size;
  uint32_t reserved;
  uint64_t caps;

  /* Function pointers... */
} obi_<name>_api_v0;

struct obi_<name>_v0 {
  const obi_<name>_api_v0* api;
  void* ctx;
};

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif
```

---

## Global Q&A

**Q: When should we mint a new profile?**  
When multiple implementations need a stable, shared contract and the interface shape is clear.

**Q: When should we avoid minting a profile?**  
When the domain semantics are too specific, or you only have one implementation and no credible
need for swapping.

