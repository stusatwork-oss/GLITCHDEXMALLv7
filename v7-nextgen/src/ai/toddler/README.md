# Toddler Reality Catalyst System

**"It's not hostile. It's a catalyst. Its presence accelerates decay."**

The Toddler is an invisible reality catalyst from v2, now integrated into V7 systems.

## What It Is

A mobile entity that:
- Amplifies Cloud pressure wherever it goes (`heat_multiplier`)
- Generates visual/audio glitches (`glitch_multiplier`)
- Creates localized distortion fields (`reality_strain`)
- Agitates zones through QBIT (`zone disturbance`)
- Provides shared dread context for Leon

## Current Status

**Phase 1: Basic System** ✓ Complete
- [x] Toddler system core (`toddler_system.py`)
- [x] Behavioral modes (`toddler_behaviors.py`)
- [x] Configuration (`toddler_config.py`)
- [ ] Integration with MallSimulation
- [ ] Wire into Cloud pressure
- [ ] Wire into renderer strain
- [ ] Add to game_state export

## Quick Start

```python
from ai.toddler import ToddlerSystem, TODDLER_CONFIG

# Initialize
toddler = ToddlerSystem(
    initial_position=(100, 50, 0),
    config=TODDLER_CONFIG
)

# Each tick
effects = toddler.update(
    dt=0.016,
    player_position=player.pos,
    current_cloud=cloud.level,
    player_looking_at_toddler=False,
    npc_contradiction_triggered=False
)

# Apply effects
cloud.add_pressure("TODDLER", effects["heat_multiplier"])
renderer.glitch_intensity = effects["glitch_multiplier"]
qbit.agitate_zone(zone, effects["reality_strain"])
```

## Behavioral Modes

| Mode | Visibility Rate | Movement | Distance Preference |
|------|----------------|----------|---------------------|
| **WANDERING** | Slow (+0.005/s) | Random walk | Any |
| **CURIOUS** | Moderate (+0.02/s) | Follow at distance | 20-40ft |
| **MANIFESTING** | Fast (+0.05/s) | Approach player | 5-15ft |
| **FLEEING** | Rapid loss (-0.1/s) | Away from player | 100+ft |
| **STATIC** | Frozen (0/s) | None | Fixed position |

### Triggers

- **CURIOUS**: Player within 50 feet
- **MANIFESTING**: Cloud ≥ 70 + player nearby
- **FLEEING**: Player looks directly at toddler
- **STATIC**: NPC contradiction triggered

## Effects Output

```python
{
    "heat_multiplier": 1.8,           # Amplify Cloud pressure
    "glitch_multiplier": 2.2,         # Amplify visual glitches
    "in_distortion_field": True,      # Player within effect radius
    "distortion_intensity": 0.75,     # 0-1 strength
    "distortion_radius": 28.0,        # Current effect radius (feet)
    "distance_to_player": 23.0,       # Distance in feet
    "toddler_visible": 0.6,           # 0 (invisible) - 1 (manifested)
    "reality_strain": 0.75,           # Reality warping intensity
    "toddler_position": (x, y, z),    # World coordinates
    "behavior": "CURIOUS",            # Current behavioral mode
    "time_alive": 142.3               # Seconds since spawn
}
```

## Integration with V7 Systems

### Cloud System
```python
def _apply_toddler_to_cloud(self, toddler_effects):
    base_delta = self.cloud.compute_base_delta()
    heat_mult = toddler_effects["heat_multiplier"]

    cloud_delta = base_delta * heat_mult
    self.cloud.add_pressure("TODDLER", cloud_delta)
```

### QBIT/Zones
```python
def _apply_toddler_to_qbit(self, toddler_effects):
    zone = self.zones.get_zone_at(toddler_effects["toddler_position"])
    if zone:
        self.qbit.apply_disturbance(
            zone_id=zone.id,
            intensity=toddler_effects["reality_strain"],
            source="TODDLER"
        )
        zone.tags.add("TODDLER_PRESENT")
```

### Renderer
```python
def _apply_toddler_to_renderer(self, toddler_effects):
    self.renderer_state.glitch_intensity = (
        toddler_effects["glitch_multiplier"] - 1.0
    ) / 3.0
    self.renderer_state.reality_strain = toddler_effects["reality_strain"]
```

### Leon (LLM Layer)
```python
game_state["toddler"] = {
    "visible": toddler_effects["toddler_visible"],
    "distance": toddler_effects["distance_to_player"],
    "reality_strain": toddler_effects["reality_strain"],
    "in_distortion_field": toddler_effects["in_distortion_field"]
}
```

Leon's awareness:
- `visible < 0.3`: "Ambient unease" only
- `visible 0.3-0.7`: "Movement in peripheral vision"
- `visible > 0.7`: Can directly acknowledge entity

## Files

- `__init__.py` - Package initialization
- `toddler_system.py` - Core ToddlerSystem class
- `toddler_behaviors.py` - BehaviorController and movement patterns
- `toddler_config.py` - Configuration parameters
- `README.md` - This file

## See Also

- [TODDLER_V7_INTEGRATION.md](../../docs/TODDLER_V7_INTEGRATION.md) - Full design specification
- [LLM_NPC_LAYER_v1.md](../../docs/LLM_NPC_LAYER_v1.md) - Leon integration
- [API.md](../../docs/API.md) - V7 integration API

## Next Steps

1. Add toddler to MallSimulation
2. Wire `heat_multiplier` → Cloud.add_pressure()
3. Wire `glitch_multiplier` → renderer strain
4. Add toddler to game_state export for Leon
5. Test: Watch Cloud accelerate when toddler is near

**The toddler returns. The mall remembers.**
