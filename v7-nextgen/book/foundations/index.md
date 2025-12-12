# Foundations

```{admonition} Governance
:class: warning
This book records observations. It does not define behavior.
```

Physics. Geometry. The rules beneath the rules.

---

## Measurements

Single source of truth for spatial scale. CRD-verified.

| Anchor | Value | Source |
|--------|-------|--------|
| Atrium diameter | 175 feet | Photo analysis, 2.5x correction |
| Food court pit | 8 feet | 12 escalator steps × 8" |
| Mast height | 70 feet | CRD trace |
| Escalator step rise | 8 inches | Building code standard |

| Source | Location |
|--------|----------|
| Loader | [`v8-nextgen/src/measurements_loader.py`](../../v8-nextgen/src/measurements_loader.py) |
| Data | [`v8-nextgen/data/measurements/`](../../v8-nextgen/data/measurements/) (4 JSON) |
| Gaps report | [`v8-nextgen/docs/reference/EASTLAND_MALL_GAPS_REPORT.md`](../../v8-nextgen/docs/reference/EASTLAND_MALL_GAPS_REPORT.md) |

---

## Voxels

Volumetric building blocks. CRD → voxel conversion.

| Source | Location |
|--------|----------|
| Builder | [`v8-nextgen/src/voxel_builder.py`](../../v8-nextgen/src/voxel_builder.py) |
| Object registry | [`v8-nextgen/data/voxel_objects/`](../../v8-nextgen/data/voxel_objects/) (6 JSON) |
| Ninja variants | [`v8-nextgen/assets/voxel_sources/ninja/`](../../v8-nextgen/assets/voxel_sources/ninja/) |
| Standard objects | [`v8-nextgen/assets/voxel_sources/standard/`](../../v8-nextgen/assets/voxel_sources/standard/) |

---

## Zones

9 spatial regions. Adjacency graph. QBIT aggregates.

| Source | Location |
|--------|----------|
| Zone solver | [`v8-nextgen/src/zone_influence_solver.py`](../../v8-nextgen/src/zone_influence_solver.py) |
| Zone lore | [`v8-nextgen/canon/zones/`](../../v8-nextgen/canon/zones/) |
| GeoJSON export | [`v8-nextgen/renpy_output/game/mall_zones.geojson`](../../v8-nextgen/renpy_output/game/mall_zones.geojson) |
| Classification reports | [`v8-nextgen/COORDINATION/`](../../v8-nextgen/COORDINATION/) |

---

## CRD Reconstruction

v5 heritage. Parametric design from Construction Record Documents.

| Source | Location |
|--------|----------|
| Updated specs | [`v8-nextgen/NEW-needs_integration/updated_V5_Specs.py`](../../v8-nextgen/NEW-needs_integration/updated_V5_Specs.py) |
| Grid generator | [`v8-nextgen/src/ninja_grid.py`](../../v8-nextgen/src/ninja_grid.py) |

---

## Palette

Color system. Era-mapped.

| Source | Location |
|--------|----------|
| Comic book palette | [`v8-nextgen/data/palette_COMICBOOK_MALL_V1.json`](../../v8-nextgen/data/palette_COMICBOOK_MALL_V1.json) |

---

*Foundations listed by reference. Measurements are source of truth.*
