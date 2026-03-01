# OBI Asset Scene IO Profile
## OBI Profile: `obi.profile:asset.scene_io-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:asset.scene_io-0`  
**Status:** Draft  
**Last Updated:** 2026-03-01

---

## 1. Nontechnical Summary

This profile standardizes importing 3D scenes (not just meshes), such as glTF scenes, into a
structured representation plus referenced binary blobs.

Typical providers:

- cgltf / tinygltf (glTF)
- assimp (multi-format scene import)

This profile is designed to interoperate naturally with OGIF: providers can emit a scene graph in
JSON that can be converted to OGIF nodes/edges by the host.

---

## 2. Technical Details

### 2.1 Output model

v0 outputs:

- `scene_json`: a provider-defined JSON document describing the scene graph
- a list of referenced blobs (buffers, images, embedded payloads), each accessible via an
  `obi_reader_v0`

This keeps the ABI small while still enabling real scenes.

### 2.2 Ownership

Scene JSON and blob info views are provider-owned and valid until the asset is destroyed.

Blob readers returned by the asset are provider-owned and must be destroyed by the host.

---

## 3. Conformance

Required:

- open from reader
- asset: get scene JSON, enumerate blobs, open blob reader, destroy

Optional (advertised via caps):

- open from bytes
- export/write (future)

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_asset_scene_io_v0.h`

---

## Global Q&A

**Q: Why JSON instead of a typed scene ABI?**  
Scene graphs are large and vary across formats. JSON keeps v0 implementable. Once hosts converge
on a stable “scene core” contract, a future profile can standardize typed nodes/materials/animation.

