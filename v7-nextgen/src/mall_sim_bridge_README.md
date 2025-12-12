# mall_sim_bridge.py

**mall-sim ↔ Mall_OS Integration Bridge**

Bridges the v2/v3 `mall_simulation.py` runtime with Mall_OS Cloud/QBIT systems without modifying mall-sim internals.

## Quick Start

```python
from mall_sim_bridge import MallOSBridge

# Initialize bridge
bridge = MallOSBridge()
bridge.initialize(
    mall_sim=my_mall_simulation,
    cloud=my_cloud_instance,
    spine_dir="canon/entities/"
)

# Game loop - use mall_os_step() instead of mall_sim.update()
while running:
    hints = bridge.mall_os_step(dt, player_action)
    render(hints)

# Save/Load sessions
bridge.save_session("saves/session.json")
bridge.load_session("saves/session.json")
```

## What It Does

| Component | Function | Purpose |
|-----------|----------|---------|
| **QBIT Adapter** | `compute_npc_qbit()` | Attach power/charisma scores to mall-sim NPCs |
| **Spine Overlay** | `attach_spine_to_npc()` | Add "never rules" to anchor NPCs |
| **Zone Wrapper** | `build_zone_from_mall_sim()` | Wrap tiles into Mall_OS microstates |
| **Heat↔Cloud** | `heat_to_cloud()` / `cloud_to_heat()` | Bidirectional pressure sync |
| **Persistence** | `save_mall_session()` | Unified state snapshots |
| **Adjacency** | `build_adjacency_from_mall_sim()` | QBIT-weighted zone transitions |
| **Orchestrator** | `MallOSBridge.mall_os_step()` | Unified update loop |

## Key Conversions

```
Heat 0-5  ←→  Cloud 0-100   (multiply/divide by 20)
Heat 5    ←→  Bleed Tier 3  (reality breaking)
```

## Extension Points

**Add new NPC types:**
```python
# In QBIT_DEFAULTS dict
"arcade_guy": QbitStats(power=1200, charisma=2000, overall=3200),
```

**Add new zones:**
```python
# In _build_zones_from_tiles()
zone_defs = {
    "MY_NEW_ZONE": (x_min, y_min, x_max, y_max),
}
```

**Add spine rules:**
```json
// In canon/entities/my_npc.json
{
  "id": "my-anchor-npc",
  "never_rules": ["never_enter_arcade", "never_speak_to_player"],
  "home_zone": "CORRIDOR"
}
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MallOSBridge                         │
│  ┌─────────────┐    ┌─────────────┐    ┌────────────┐  │
│  │  mall-sim   │───▶│ Heat↔Cloud  │───▶│   Cloud    │  │
│  │  .update()  │    │   Bridge    │    │  .update() │  │
│  └─────────────┘    └─────────────┘    └────────────┘  │
│         │                                     │         │
│         ▼                                     ▼         │
│  ┌─────────────┐                      ┌────────────┐   │
│  │ QBIT Stats  │                      │   Zones    │   │
│  │ per NPC     │                      │ Microstates│   │
│  └─────────────┘                      └────────────┘   │
│         │                                     │         │
│         └──────────────┬──────────────────────┘         │
│                        ▼                                │
│              ┌─────────────────┐                        │
│              │  Merged Hints   │                        │
│              │  (render data)  │                        │
│              └─────────────────┘                        │
└─────────────────────────────────────────────────────────┘
```

## Files

| File | Purpose |
|------|---------|
| `mall_sim_bridge.py` | This module (919 lines) |
| `../docs/MALL_SIM_BRIDGE_INTEGRATION.md` | Full integration doc |

## Testing

Run module self-test:
```bash
cd v7-nextgen/src
python mall_sim_bridge.py
```

Expected output:
```
MALL-SIM ↔ MALL_OS BRIDGE TEST
1. QBIT Adapter Test: ✓
2. Heat ↔ Cloud Adapter Test: ✓
3. ZoneMicrostate Wrapper Test: ✓
4. Persistence Test: ✓
✓ Bridge module test complete
```

## See Also

- [Full Integration Document](../docs/MALL_SIM_BRIDGE_INTEGRATION.md)
- [Cloud System](cloud.py)
- [QBIT Engine](qbit_engine.py)
- [NPC State Machine](npc_state_machine.py)
