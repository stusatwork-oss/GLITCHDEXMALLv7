# mall-sim → Mall_OS Integration Document v0.1

**Last updated**: 2025-12-12

**Status**: Implemented, pending integration testing.

**Bridge module**: `v7-nextgen/src/mall_sim_bridge.py`

---

## Executive Summary

**Objective**: Turn mall-sim into the basement physics engine for Mall_OS.

**Approach**: Wrap, don't rewrite. mall-sim stays intact as the real-time simulation core. Mall_OS layers Cloud pressure, QBIT scoring, and narrative metaphysics on top.

**Deliverables Implemented**:
- `v7-nextgen/src/mall_sim_bridge.py` - Complete integration module (919 lines)
- 7 bridge systems operational
- Zero modifications to mall-sim internals

**Status**: Ready for integration testing.

---

## Primitive Map

| mall-sim | Mall_OS | Bridge Function |
|----------|---------|-----------------|
| `NPCAgent` | `Synthactor (Swarm)` / `Anchor NPC` | `compute_npc_qbit()`, `attach_spine_to_npc()` |
| `MovementBehavior` | `NPCSpine` | `SpineOverlay` dataclass, `SPINE_REGISTRY` |
| `world_tiles` | `ZoneMicrostate` | `build_zone_from_mall_sim()` |
| `HeatSystem (0-5)` | `Cloud (0-100)` | `heat_to_cloud()`, `cloud_to_heat()` |
| `HeatLevel.REALITY_BREAK` | `Bleed Tier 3+` | `is_reality_breaking()`, `get_bleed_tier()` |
| `Cell.forceField` | `QBIT aggregate` | `ZoneMicrostateWrapper.qbit_aggregate` |
| `Board` | `WorldObjectRegistry` | `ZoneMicrostateWrapper.tiles` |
| `SimLoop.update()` | `Cloud.update()` | `MallOSBridge.mall_os_step()` |

---

## Subsystem Compatibility Table

| Subsystem | mall-sim | Mall_OS | Compatibility |
|-----------|----------|---------|---------------|
| **Pressure** | Heat 0-5, decay/increase | Cloud 0-100, 4 moods | Direct scale (×20) |
| **NPC Spawning** | Random by faction | Spine-based anchors + swarm | Hybrid (generic + spine) |
| **Spatial** | Tile dict (x,y,z) | Zone microstates + QBIT | Wrapped |
| **Events** | `trigger_event()` → heat | `_record_discovery()` → Cloud | Bridged via events list |
| **Persistence** | None | `cloud_state.json` | Unified snapshot |
| **Adjacency** | None | QBIT-weighted matrix | Built from zones |
| **Reality Break** | Heat 5 (4.8+) | Bleed Tier 3 (90+) | Same concept, threshold aligned |

---

## Graft Point Map

| Extension Type | Hook Location | Integration Path |
|---------------|---------------|------------------|
| **New Store Types** | `zone_defs` in `_build_zones_from_tiles()` | Add bounds tuple, zone auto-creates |
| **New Agent Behaviors** | `QBIT_DEFAULTS` dict | Add faction/role → QbitStats mapping |
| **New Event Triggers** | `_extract_npc_events()` | Parse mall_sim_hints, emit to Cloud |
| **New Simulation Loops** | `MallOSBridge.mall_os_step()` | Insert between mall-sim and Cloud updates |
| **New Environment Variables** | `ZoneMicrostateWrapper` dataclass | Add field, update `to_dict()`/`from_dict()` |
| **Glitch Events** | After `sync_heat_to_cloud()` | Check `get_bleed_tier()`, trigger effects |
| **Horror Stack** | `_merge_render_hints()` | Inject horror overlays based on bleed tier |
| **Cinematic Triggers** | `_check_npc_contradictions()` | Fire cutscene when spine violation detected |
| **Cloud Pressure Changes** | `HeatCloudBridge.bidirectional_sync()` | Either system can lead |
| **Clerk Interventions** | `check_spine_contradiction()` | High-QBIT NPCs get early contradiction access |

---

## Minimal-Change Integration Patch

**Files Changed**: 0 in mall-sim core (v2/v3 untouched)

**New Modules Added**:

| File | Lines | Purpose |
|------|-------|---------|
| `v7-nextgen/src/mall_sim_bridge.py` | 919 | Complete bridge implementation |

**How to Use**:

```python
from mall_sim_bridge import MallOSBridge

# Initialize
bridge = MallOSBridge()
bridge.initialize(
    mall_sim=my_mall_simulation,
    cloud=my_cloud_instance,
    spine_dir="canon/entities/"
)

# Game loop
while running:
    hints = bridge.mall_os_step(dt, player_action)
    render(hints)

# Save/Load
bridge.save_session("saves/session.json")
bridge.load_session("saves/session.json")
```

---

## Risk & Stability Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Heat/Cloud desync** | Medium | `HeatCloudBridge` enforces single source of truth |
| **Spine contradiction spam** | Low | 30-second cooldown enforced in `check_spine_contradiction()` |
| **Zone bounds mismatch** | Medium | `zone_defs` must match actual tile layout |
| **QBIT score drift** | Low | QBIT computed once at spawn, stable |
| **Performance (Cloud every frame)** | Medium | Cloud updates every 10 frames, not every tick |
| **Persistence format changes** | Low | Version field in snapshot allows migration |

**Fragile Spots**:
- `_extract_npc_events()` - Relies on specific hint keys from mall-sim
- `_build_zones_from_tiles()` - Hardcoded zone bounds (needs config)

**Safe Extension Patterns**:
- Add new QBIT defaults without touching core
- Add new spine JSONs without code changes
- Add new zone types by extending `zone_defs`

---

## Code Pointers to Key Loops

| System | File:Line | Description |
|--------|-----------|-------------|
| **mall-sim update** | `v2-immersive-sim/src/mall_simulation.py:247-445` | Main `update()` loop |
| **Cloud update** | `v7-nextgen/src/cloud.py:355-405` | Cloud tick with QBIT |
| **Bridge orchestrator** | `v7-nextgen/src/mall_sim_bridge.py:580-650` | `mall_os_step()` |
| **Heat→Cloud sync** | `v7-nextgen/src/mall_sim_bridge.py:280-295` | Bidirectional bridge |
| **NPC event extraction** | `v7-nextgen/src/mall_sim_bridge.py:655-680` | Parse hints for Cloud |
| **Contradiction check** | `v7-nextgen/src/mall_sim_bridge.py:685-700` | Spine violation detection |

---

## Integration Testing Plan

### 1. Baseline Sanity Check (No Cloud / No Spines)

**Goal**: Confirm bridge doesn't break mall-sim when Cloud is "neutral".

**Steps**:
- Initialize `MallOSBridge` with:
  - a real `mall_sim` instance
  - a Cloud instance with neutral config (Cloud=0, no bleed)
  - `spine_dir` set, but with an empty or minimal registry
- Run `mall_os_step(dt, player_action)` for 5–10 minutes of sim time.

**Expected**:
- NPCs behave exactly like vanilla mall-sim.
- Heat system progresses normally.
- Cloud stays near 0–20 and does not inject glitches.
- No exceptions / log spam.

### 2. Heat ↔ Cloud Mapping Test

**Goal**: Validate Heat 0–5 ↔ Cloud 0–100 mapping.

**Steps**:
- Force Heat levels from 0 → 5 using mall-sim debug / forced events.
- After each change:
  - Inspect Cloud value via `bridge.cloud.cloud_level`.

**Expected**:
- Heat 0 → Cloud ≈ 0
- Heat 1 → Cloud ≈ 20
- Heat 2 → Cloud ≈ 40
- Heat 3 → Cloud ≈ 60
- Heat 4 → Cloud ≈ 80
- Heat 5 → Cloud ≈ 100

**Validation**:
- Trigger a "reality break" in mall-sim and confirm:
  - `get_bleed_tier()` returns Tier 3+
  - Horror overlays / glitches fire only at high tiers.

### 3. Spine Overlay / Contradiction Test

**Goal**: Ensure spine-based NPCs behave differently from generic ones.

**Steps**:
- Mark one security NPC as an "anchor" with a spine.
- Give spine `never_rules` that are easy to violate (e.g. "never enter Zone X").
- Lure that NPC into Zone X using normal sim behavior.

**Expected**:
- `check_spine_contradiction()` triggers.
- A contradiction event is logged.
- Optional: a cutscene trigger / visual glitch fires.
- Cooldown stops spam for the next 30s.

### 4. ZoneMicrostate / QBIT Test

**Goal**: Validate zones get QBIT aggregates and microstate.

**Steps**:
- Define 2–3 zones in `_build_zones_from_tiles()`.
- Populate one zone with high-QBIT NPCs (e.g. rare anchor types).
- Inspect:
  - `ZoneMicrostate.qbit_aggregate`
  - `zone.turbulence`, `zone.resonance`

**Expected**:
- "High QBIT" zone shows higher aggregate vs. control.
- Cloud reacts more strongly to events in that zone.

### 5. Save / Load Round Trip

**Goal**: Confirm session persistence works.

**Steps**:
- Run sim for N seconds.
- Call `bridge.save_session("saves/test_session.json")`.
- Restart process.
- Call `bridge.load_session("saves/test_session.json")`.
- Compare:
  - Number and positions of NPCs.
  - Heat / Cloud levels.
  - Active zones / microstates.

**Expected**:
- State is within acceptable tolerance of pre-save snapshot.
- No crash or missing keys on load.

### 6. Performance Check

**Goal**: Ensure Cloud layer doesn't tank FPS.

**Steps**:
- Run mall-sim alone and note avg frame time.
- Run mall-sim via `MallOSBridge.mall_os_step()` with Cloud enabled.
- Measure:
  - Frame time
  - Cloud tick frequency (should be every 10 frames)

**Expected**:
- Overhead exists but remains acceptable for target fps.
- No runaway cost from event extraction or spine checks.

---

## Open Questions / Future Work

- **Cloud ↔ Heat authority**: Should Cloud ever override Heat directly, or only nudge it?
- **Spine vs. swarm ratio**: How many NPCs should be full spines vs. generic swarm, for performance and narrative clarity?
- **External config**: Move hardcoded `zone_defs` into external config (`mall_config.json`)?
- **Event bus**: Add a formal event bus between mall-sim and Cloud instead of ad-hoc hints?
- **Debug UI**: Expose QBIT / Cloud debug UI for tuning thresholds during playtesting.
- **Multi-era support**: How does the bridge handle timeline switching (1981/1995/2005/2011)?
- **Adjacency validation**: Should adjacency matrix respect physical walls or only QBIT gravity?

---

*Document version: 0.1*
*Author: Claude (Opus 4) + Stu*
*Integration: v7-nextgen/src/mall_sim_bridge.py*
