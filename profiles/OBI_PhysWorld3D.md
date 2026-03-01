# OBI Physics World3D Profile
## OBI Profile: `obi.profile:phys.world3d-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:phys.world3d-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes a minimal 3D rigid-body physics world:

- create/destroy a physics world
- step simulation
- create/destroy bodies and colliders
- apply impulses and query transforms
- optional raycasts and contact events

Typical providers:

- Bullet
- Jolt Physics
- PhysX (when wrapped behind a provider)

---

## 2. Technical Details

### 2.1 Object model

The profile provides a factory that creates a world handle. Within a world:

- bodies and colliders are identified by provider-owned IDs
- IDs are only meaningful within the world instance that created them

### 2.2 Coordinate system

Coordinates are expressed in "world units" (floating point). Units are host-defined.

Orientations use quaternions.

---

## 3. Conformance

Required:

- world create/destroy
- `step`
- body create/destroy and transform get/set
- collider create/destroy (at least sphere and box)

Optional (advertised via caps):

- raycast
- contact events

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_phys_world3d_v0.h`
- `abi/profiles/obi_geom_types_v0.h`

---

## Global Q&A

**Q: Why not standardize character controllers and vehicles here?**  
Those add significant semantic surface area and tend to be engine-specific. Add focused profiles
later once multiple providers need the same stable contract.

