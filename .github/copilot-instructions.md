# GLITCHDEX MALL - AI Agent Instructions

## Project Identity

**GLITCHDEX MALL** is an AI-native, multi-era simulation of Eastland Mall (Tulsa, 1981-2011) treated as a **civic-scale interior megastructure** (~1M+ sq ft), not a simple game level. This is a reconstruction project using evidence-based CRD (Classification-Reference-Document) workflow combined with Cloud-driven simulation systems.

**Philosophy:** Reconstruction > Hallucination. Canon emerges from evidence + resonance.

---

## Critical Architecture Knowledge

### Version Chronology (DO NOT IGNORE)

- **v1-doofenstein**: Original Wolf3D-style prototype (frozen, playable)
- **v2-immersive-sim**: Advanced AI architecture experiment (frozen, playable)
- **v3-eastland**: Pygame graphical engine - **WRONG SCALE** (kept for historical reference, DO NOT base new work on v3 geometry)
- **v4-renderist**: Cloud-driven semantic world (introduces Cloud + Renderist theology)
- **v5-eastland**: **CRD reconstruction** - geometric/structural ground truth (measurements, zones, photo evidence)
- **v6-nextgen**: Placeholder for future canonical implementation
- **v7-nextgen**: **CURRENT ACTIVE VERSION** - Integration of v5 evidence + v6 QBIT systems

**Work in v7-nextgen/**, use v5 as ground truth for geometry, ignore v3 scale.

### Scale Anchors (NON-NEGOTIABLE)

Eastland Mall is **civic-scale** (airport concourse / space station with parking lot):
- **Total footprint:** ~1,000,000+ sq ft (~15-17 football fields)
- **Atrium diameter:** 175 feet (verified via glass block wall counting)
- **Tensile roof masts:** 60-80+ feet (KKT white lattice towers)
- **Food court pit depth:** 8 feet (escalator standard: 8" step height × 24 steps visible)
- **Escalator geometry:** 30° incline, ~31-32 ft horizontal run, 16 ft vertical drop

**Primary metrology anchor:** Escalator standards (never Coca-Cola machines - those are secondary validation only).

**DO NOT shrink to "building scale."** Preserve civic-scale architecture.

### Core Systems Architecture

**QBIT Engine** (`v7-nextgen/src/qbit_engine.py`)
- Entity influence scoring: power (0-3000) + charisma (0-3000) = overall (0-6000)
- Power = structural leverage (backing, resources, network reach)
- Charisma = attention gravity (resonance, engagement, trust)
- Zone aggregates create personality gravity fields

**Cloud System** (`v7-nextgen/src/cloud.py`)
- Global pressure: 0-100 (drives mood + bleed tier)
- Moods: CALM (0-24), TENSION (25-49), SURGE (50-74), CRITICAL (75+)
- Bleed tiers: 0 (none), 1 (shifts), 2 (drifts), 3 (tears)
- QBIT-weighted: Entity influence affects Cloud pressure (0.15 weight)
- Zone microstates: Local turbulence + resonance + QBIT aggregates

**Measurements Loader** (`v7-nextgen/src/measurements_loader.py`)
- Single source of truth for ALL spatial data
- Loads from `data/measurements/` (CRD traceability preserved)
- Access via: `ml.get_spatial("atrium.diameter_feet.value")` → 175

**Adjacency System** (`v7-nextgen/src/adjacency.py`)
- QBIT-weighted zone transitions
- High-QBIT zones become narrative/spatial attractors
- Dynamic probability matrix for NPC pathfinding + bleed propagation

**Bridge Server** (`v7-nextgen/src/bridge_server.py`)
- Flask HTTP wrapper for UE5/external engine integration
- Endpoints: `/init`, `/tick`, `/status`, `/reset`
- Stateful world simulation via `sim_bridge.py`

### Entity Canon System

**Entity definitions:** `v7-nextgen/canon/entities/*.json`
- Structured JSON with QBIT metrics pre-computed
- Fields: `id`, `name`, `role`, `type`, `tags`, `metrics`, `computed`, `meta`
- Example: `the-janitor.json` - Primary anchor NPC with behavioral constraints

**Entity types:**
- `npc`: Characters (Janitor, Leon, Wife)
- `zone`: Spatial entities (Food Court, Atrium)
- `artifact`: Items (Credit Cards, Mirror Maze Token)
- `anomaly`: Reality glitches (Tensile Roof Mast, Escalator Hum)

### Multi-Era Timeline

**Four canonical eras (ALL valid, contradictions are CANON):**
- **1981**: Opening (pristine, optimistic)
- **1995**: Peak (bustling, thriving) ← Starting era
- **2005**: Decline (vacant, flickering)
- **2011**: Closure (abandoned, temporal horror)

**Timeline system:** `v7-nextgen/src/timeline_system.py`
Triggers: Cloud pressure, player discoveries, NPC interactions

---

## Development Workflows

### Running Demos

```bash
cd v7-nextgen/src

# Integrated demo (mock LLM)
python v7_integrated_demo.py

# With real LLM (requires ANTHROPIC_API_KEY)
python v7_integrated_demo.py --with-llm

# Specific scenarios
python v7_integrated_demo.py --scenario toddler_manifests
python v7_integrated_demo.py --scenario critical_spiral
```

### Building Voxel Meshes

```bash
cd v7-nextgen/src
python voxel_builder.py  # Generates v7_mall_doom.json
```

### Running Bridge Server (UE5 Integration)

```bash
cd v7-nextgen/src
python bridge_server.py  # Flask server on port 5000
```

### Testing

Tests use pytest patterns:
```bash
cd v7-nextgen/src
python test_qbit_integration.py
python test_adjacency_integration.py
python test_janitor_contradiction_sequence.py
```

### Shareware Launcher (Historical Context)

```bash
# From repo root
./LAUNCH_GUI.sh   # Mid-90s GUI launcher (mouse + keyboard)
./LAUNCH.sh       # Text launcher (keyboard only)
```

---

## Key Conventions

### CRD Workflow (Classification-Reference-Document)

When adding/modifying spatial data:
1. **Classify:** Identify the feature type (zone, measurement, entity)
2. **Reference:** Link to photo evidence or source documentation
3. **Document:** Add to structured JSON with confidence level + traceability

**Example:** See `data/measurements/crd_traceability.json`

### File Organization

```
v7-nextgen/
├── canon/           # Authoritative entity definitions (JSON)
├── src/             # Python source code
├── data/            # Measurements, zone data, game data
├── assets/          # Photos, maps, media (evidence base)
└── docs/            # Documentation, LLM guides
```

### Naming Patterns

- **Zones:** `Z1_WEST_WING`, `Z4_FOOD_COURT`, `Z9_SUBTERRANEAN` (use zone IDs, not descriptions)
- **Entities:** `the-janitor`, `leisurely-leon`, `coca-cola-store` (kebab-case)
- **Files:** `snake_case.py`, `kebab-case.json`, `SCREAMING_SNAKE.md` (context-dependent)

### JSON Schema Consistency

Entity spines (`canon/entities/*.json`):
```json
{
  "id": "entity-id",
  "name": "Display Name",
  "role": "Primary|Secondary",
  "type": "npc|zone|artifact|anomaly",
  "metrics": { /* QBIT metrics */ },
  "computed": { /* power, charisma, overall, rarity */ },
  "meta": { "universe": "mallos-v6", "source": "manual|generated" }
}
```

### Behavioral Rules (From Entity Definitions)

Some NPCs have hard constraints (defined in JSON, enforced in code):
- **Janitor:** Never crosses FC-ARCADE threshold, never speaks about wife
- **Leon:** Aware of game_state, ready for narration hooks
- **Wife:** Always at bookstore, Janitor always faces away

Preserve these when implementing NPC logic.

---

## Integration Points

### LLM Integration (Janitor Dialogue)

Triggers at Cloud ≥ 70 when Janitor in forbidden zone:
```python
from ai.toddler.prompts import build_janitor_prompt

system, user = build_janitor_prompt(
    janitor=janitor_state,
    cloud=cloud_state,
    zone=zone_state,
    metadata=mall_metadata
)
```

### Discord Narration Hooks

Future system: `src/ai/npc_llm/discord_dm.py`
LLM acts as dungeon master, narrating Cloud events + entity behaviors

### External Rendering (UE5/Godot)

Use Bridge Server HTTP API:
```python
POST /init   # Load world from config
POST /tick   # Advance simulation one frame
GET /status  # Query Cloud/zone/NPC state
POST /reset  # Reset world
```

---

## What NOT to Do

❌ **Don't shrink the mall to building scale** - Preserve civic-scale architecture
❌ **Don't use v3-eastland geometry as reference** - v3 has wrong ruler/scale
❌ **Don't bypass measurements_loader** - Use it as single source of truth
❌ **Don't ignore version chronology** - Each version has specific purpose
❌ **Don't "fix" intentional contradictions** - Multi-era variance is canon
❌ **Don't add entities without QBIT metrics** - Use `qbit_engine.score_entity()`
❌ **Don't modify CRD data without photo traceability** - Evidence-based only

---

## Quick Reference

**Key files to understand the project:**
- `README.md` - Project overview
- `VERSION_GUIDE.md` - Detailed version history
- `docs/AI_INTENT.md` - AI philosophy
- `docs/AI_MEMORY.md` - Core facts & constraints
- `v7-nextgen/README.md` - v7 integration summary
- `v7-nextgen/V7_INTEGRATED_DEMO_README.md` - Demo walkthrough
- `RECONSTRUCTION_NOTES.md` - Photo analysis + architectural signatures

**When in doubt:**
1. Check `measurements_loader` for spatial data
2. Check `canon/entities/` for entity definitions
3. Check `docs/AI_MEMORY.md` for non-negotiables
4. Preserve civic-scale architecture
5. Prefer reconstruction over hallucination
