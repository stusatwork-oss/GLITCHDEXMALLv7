# GLITCHDEX MALL V8 - LAB BUILD (ACTIVE DEV)

**Version:** 8.0.0-lab
**Status:** ACTIVE INTEGRATION - Integrating Visual Runtime & Game Loop
**Philosophy:** v7 Canon + Visual Runtime + Ninja Mechanics = v8 Playable Game

---

## 🎯 WHAT IS V8?

**V8 is the "Playable Game" integration phase.**

While **v7-nextgen** established the canonical systems (Cloud, QBIT, CRD), V8 introduces the actual runtime layer:

- **Visual Runtime**: Pygame-based rendering (Grid, Walls, HUD).
- **Ninja Game Loop**: Player control, item usage, resource management.
- **Cutscene System**: Triggered narrative events (Sora prompts).
- **Consensus Engine**: Mechanics for trap/object placement validation.

**Goal:** Turn the v7 simulation backend into a playable experience.

---

## 🏗️ INTEGRATION SUMMARY

### From V5 (CRD Reconstruction)
✅ **Scale Corrections** - Space station scale (1M+ sq ft, 175' atrium, 70' masts)
✅ **Measured Geometry** - 15 verified measurements with photo traceability
✅ **Architectural Context** - KKT design intent, tensile sail technology
✅ **Zone Graph** - 9 structural zones with adjacency logic
✅ **New Entities** - Coca-Cola store, FOOD COURT neon sign
✅ **Timeline Contradictions** - Multi-era variance preserved as canon

### From V6 (Simulation Systems)
✅ **QBIT Engine** - Entity scoring (power, charisma, resonance)
✅ **Cloud System** - Global mood states with zone microstates
✅ **NPC State Machines** - Behavioral AI with contradictions
✅ **Bridge Server** - UE5 integration layer (HTTP/JSON)
✅ **Entity Canon** - Structured JSON definitions
✅ **Adjacency System** - QBIT-weighted zone transitions

### NEW in V7 (Integration Features)
✅ **Measurements Loader** - Single source of truth for all dimensions
✅ **Voxel Builder** - Doom-alike construction from CRD blueprints
✅ **Timeline System** - Multi-era support (1981/1995/2005/2011)
✅ **LLM DM Guide** - Discord hooks narration system
✅ **Z7 Placeholder** - Subterranean zone (exterior access only)

---

## 🎮 VOXEL DOOM-ALIKE VISION

### The Concept
**3 credit cards as weapons in a 1,000,000+ sq ft mall dungeon.**

- Fast-paced voxel combat in cathedral-scale spaces
- 175-foot atrium gives massive room for maneuver
- Vertical gameplay (60-80 foot ceilings, 8-foot pit descents)
- Credit cards as keys/weapons in consumer nightmare

### Voxel Construction Workflow

```bash
# 1. Build voxel mesh from CRD measurements
python src/voxel_builder.py
# Generates: v7_mall_doom.json

# 2. Import into your voxel engine
# 3. DOOM in the mall
```

---

## 🕰️ MULTI-ERA TIMELINE

**Four Eras (All Canon):**
- **1981** - Opening (pristine, optimistic)
- **1995** - Peak (bustling, thriving) ⭐ Starting Era
- **2005** - Decline (vacant, flickering)
- **2011** - Closure (abandoned, temporal horror)

**Era Triggers:** Cloud pressure, player discoveries, NPC interactions

**Contradictions between eras are CANON, not errors.**

---

## 🛠️ QUICK START

### For Voxel Construction
```bash
python src/voxel_builder.py
```

### For Measurements
```python
from measurements_loader import load_measurements

ml = load_measurements()
atrium_diameter = ml.get_spatial("atrium.diameter_feet.value")  # 175
```

### For Timeline/Era System
```python
from timeline_system import TimelineManager

tm = TimelineManager()
tm.transition_to_era(MallEra.DECLINE_2005)
```

---

## 📏 SCALE CORRECTIONS FROM V5

**CRITICAL: Space Station Scale**

- Atrium: 175' diameter (2.5x correction from v6)
- Masts: 70' tall (2.0x correction from v6)
- Design: "Space station with a parking lot"

**See:** `data/measurements/spatial_measurements.json`

---

## 📊 MEASUREMENTS SUMMARY

**HIGH Confidence:**
- Food court pit: 8 feet
- Fountain tiers: 4 levels
- Tensile cables: 32 radial

**All measurements linked to photo evidence.**

**See:** `data/measurements/crd_traceability.json`

---

## 📞 STATUS

**Version:** 7.0.0-alpha
**Status:** Integration Complete - Ready for Voxel Construction

**Everything but visuals: READY.**
**3 credit cards: LOADED.**
**Mall dungeon: AWAITS.**

---

*Last Updated: 2025-11-28*
*v5 CRD + v6 QBIT = v7 Integration*
