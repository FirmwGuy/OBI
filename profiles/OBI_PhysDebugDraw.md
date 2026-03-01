# OBI Physics Debug Draw Profile
## OBI Profile: `obi.profile:phys.debug_draw-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:phys.debug_draw-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes extracting debug geometry from physics worlds for visualization:

- 2D and/or 3D line primitives
- optional triangles for filled debug views

Typical providers:

- Box2D debug draw wrappers
- Bullet/Jolt debug draw wrappers

The host renders the returned primitives using any renderer (`gfx.render2d`, `gfx.render3d`, or a
custom debug renderer).

---

## 2. Technical Details

### 2.1 World compatibility

Debug draw collection functions accept physics world handles (`phys.world2d` / `phys.world3d`).

The world handle MUST come from the same provider instance that exposes the debug draw profile.

### 2.2 Output model

The provider writes primitives into host-provided arrays. Functions follow standard OBI sizing rules:

- if an output pointer is NULL or cap is 0, the provider returns OK and sets the required count
- if cap is too small, the provider returns `OBI_STATUS_BUFFER_TOO_SMALL` and sets the required count

---

## 3. Conformance

Required:

- at least one collect function (providers must set caps honestly)

Optional (advertised via caps):

- 2D vs 3D support
- triangles

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_phys_debug_draw_v0.h`

---

## Global Q&A

**Q: Why not integrate debug drawing into the world profiles?**  
Keeping debug draw as a separate profile avoids bloating the core physics world ABI. Hosts that
do not need debug visualization can ignore this profile.

