# MallOS - Cloud State & Simulation Orchestration

Simulation state management following v4-renderist Cloud architecture.

## Purpose

MallOS is the orchestration layer that manages:
- Global Cloud state (pressure 0-100, mood, bleed tier)
- Zone activation and cooldown logic
- NPC swarm population curves
- Contradiction cascade triggers
- 60fps simulation tick with Cloud interpolation

## Architecture

```
MallOS
├── cloud/
│   ├── state.json           # Current cloud pressure/mood/tier
│   ├── tick_logic.py        # 60fps loop, Cloud updates every 10 frames
│   └── interpolation.py     # Smooth state transitions
│
├── zones/
│   ├── zone_graph.json      # From v5 CRD, enhanced for v6
│   ├── cooldown_rules.json  # 30s zone cooldown after bleed
│   └── activation.py        # Zone state machine
│
├── bleed_rules/
│   ├── tier1_shifts.json    # Minor inconsistencies
│   ├── tier2_drifts.json    # Noticeable contradictions
│   ├── tier3_tears.json     # Reality fractures
│   └── cascade_logic.py     # How bleeds propagate
│
└── swarm/
    ├── population_curves.json  # Crowd density per pressure
    ├── movement_rules.json     # Flow patterns
    └── spawning.py             # Dynamic NPC generation
```

## Cloud State Schema

```json
{
  "cloud": {
    "pressure": 0-100,
    "mood": "tension | wander | surge | bleed",
    "bleed_tier": 0-3,
    "last_bleed": "ISO timestamp"
  },
  "zones": {
    "zone_id": {
      "active": boolean,
      "cooldown_remaining": 0-30,
      "population": 0-100,
      "last_contradiction": "ISO timestamp"
    }
  },
  "tick": {
    "frame": 0-59,
    "cloud_update_frame": 0 | 10 | 20 | 30 | 40 | 50,
    "interpolation_phase": 0.0-1.0
  }
}
```

## Integration

- Consumed by: `v6-nextgen/src/mallos/` (simulation engine)
- References: `v6-nextgen/canon/zones/`, `ai/spynt/` for NPC behavior
- Output: Real-time state for rendering/video generation

## Key Principles (from v4-renderist)

1. **Cloud is global, zones are local**
2. **Swarm confirms Cloud, never contradicts**
3. **Bleed events have cooldown (prevent spam)**
4. **Anchor NPCs trigger contradictions, swarm reacts**
5. **60fps loop, Cloud tick every 10 frames**

## Usage

```python
from ai.mallOS.cloud import CloudState

cloud = CloudState()
cloud.update_pressure(delta=+5)  # Player action increases pressure
cloud.check_bleed_threshold()     # May trigger tier 1-3 event

if cloud.mood == "bleed":
    zone = cloud.select_bleed_zone()
    zone.apply_contradiction()
    zone.start_cooldown(30)  # 30 second cooldown
```

---

*The Cloud remembers what you break.*
