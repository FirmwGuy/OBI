# OBI Physics World2D Profile
## OBI Profile: `obi.profile:phys.world2d-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:phys.world2d-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal 2D rigid-body physics world:

- create/destroy a physics world
- step simulation
- create/destroy bodies and colliders
- apply forces/impulses and query transforms
- optional raycasts and contact events

Typical providers:

- Box2D
- Chipmunk2D

This profile is designed to be small enough for tools and gameplay prototypes, while still being
swappable across engines.

---

## 2. Technical Details

### 2.1 Object model

The profile provides a factory that creates a world handle. Within a world:

- bodies and colliders are identified by provider-owned IDs
- IDs are only meaningful within the world instance that created them

### 2.2 Coordinate system

Coordinates are expressed in "world units" (floating point). Units are host-defined (meters,
pixels, etc.) and must be used consistently by the host.

Angles are in radians.

### 2.3 Contact events (optional)

Providers may expose a drainable contact event queue (begin/end contact).

Event queues are useful for integrating physics into deterministic hosts: the host can record the
events as effects if needed.

---

## 3. Conformance

Required:

- world create/destroy
- `step`
- body create/destroy and transform get/set
- collider create/destroy

Optional (advertised via caps):

- raycast
- contact events

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_phys_world2d_v0.h`
- `abi/profiles/obi_geom_types_v0.h`

---

## Global Q&A

**Q: Why not include every joint and shape type?**  
To keep v0 implementable and stable. Add joints/shapes as optional capability extensions once
multiple providers need the same contract.

