# MallOS Voxel Object Integration Architecture

**Status:** Design Phase
**Date:** 2025-12-03

---

## The Revelation

**The mall isn't a game. It's an operating system.**

MallOS = A PFLOPS-class HPC masquerading as a 1990s shopping mall

---

## System Architecture Mapping

### MallOS as Computational Substrate

| Component | OS Analogy | Implementation |
|-----------|------------|----------------|
| **Cloud** | Thermal Management + Scheduler | `cloud.py` - Global heat/load distribution (0-100) |
| **Zones** | Processing Nodes | `ZoneMicrostate` - Local compute units with state |
| **QBIT** | Process Priority System | power/charisma/resonance scores (0-6000) |
| **Adjacency** | IPC Routing / Network Topology | Probability-weighted zone connections |
| **NPCs** | Running Processes | State machines with QBIT priority |
| **Entities** | Kernel Objects | Anything with a QBIT score |
| **Bleed Events** | Kernel Panics / System Faults | Reality contradiction = system instability |
| **Contradictions** | Race Conditions | NPC behavior violates spine = deadlock |

---

## Voxel Objects as Hardware Components

### Current Object Catalog

| Object | Behavior | MallOS Function |
|--------|----------|-----------------|
| **PIZZA_SLICE** | `cloud_pressure-3` | **Heat Sink** - Active cooling component |
| **ARCADE_TOKEN** | `cloud_pressure+1` | **Resistor** - Generates load/heat |
| **JANITOR_MOP** | `cloud_pressure+2` (NPC_PROP) | **Shared Resource Lock** - Process contention |
| **SLURPEE_CUP** | Unknown | TBD |
| **TRASH_CAN** | Unknown | TBD |

### Integration Questions (Reframed)

#### 1. **Memory-Mapped I/O or Direct Syscalls?**

When player picks up ARCADE_TOKEN:
```python
# Option A: Memory-mapped device (object modifies zone state)
zone.cloud_pressure += 1
zone.qbit_aggregate += 100  # Token adds compute load to zone

# Option B: Direct syscall (object fires global event)
cloud.adjust_pressure(+1, source="ARCADE_TOKEN", zone="FC-ARCADE")

# Option C: Hardware interrupt (queued for next tick)
event_queue.push(CloudPressureEvent(delta=+1, object_id="ARCADE_TOKEN"))
```

**Decision needed:** Immediate (synchronous) vs. queued (async)?

---

#### 2. **Local vs. Global State Modification**

PIZZA_SLICE cooling effect:
```python
# Local cooling (zone-specific)
current_zone.turbulence -= 5
current_zone.resonance -= 10

# Global cooling (broadcast)
cloud.global_pressure -= 3

# Thermal gradient (adjacency-aware propagation)
for neighbor_zone, probability in adjacency[current_zone].items():
    neighbor_zone.pressure -= 3 * probability
```

**Decision needed:** Spatial propagation model?

---

#### 3. **QBIT Scoring for Objects**

Should objects have compute weight?
```python
voxel_object = {
    "id": "ARCADE_TOKEN",
    "qbit_score": {
        "power": 50,        # Low structural leverage
        "charisma": 800,    # High attention draw
        "resonance": 120,   # Moderate memory stickiness
    },
    "behavior": {
        "on_pickup": [
            "cloud_pressure+1",
            "zone.qbit_aggregate+{self.charisma}",  # Add object's charisma to zone
            "subtitle: 'Something in the arcade wakes up.'"
        ]
    }
}
```

**Implication:** Objects become computational entities in the zone's QBIT aggregate.

---

#### 4. **Process Contention (NPC Props)**

JANITOR_MOP as shared resource:
```python
# Janitor (Unit 7) has reference to mop
janitor.state.equipment = ["JANITOR_MOP"]

# Player picks up mop
player.inventory.add("JANITOR_MOP")
janitor.state.equipment.remove("JANITOR_MOP")  # Resource stolen!

# Janitor state machine detects missing equipment
if "JANITOR_MOP" not in janitor.equipment and cloud.level >= 70:
    trigger_llm_dialogue(janitor, event="EQUIPMENT_STOLEN")
    # "Where's my mop? I need my mop. The E-flat hum is getting louder..."
```

**MallOS interpretation:** Process can't access required resource → triggers contradiction event

---

#### 5. **Routing Table Updates**

When ARCADE_TOKEN picked up:
```python
# Create temporary routing bias
adjacency["FC-ARCADE"]["PLAYER_ZONE"] = 0.85  # Strong pull to arcade
adjacency_decay_timers["FC-ARCADE"] = 10.0    # Lasts 10 ticks

# Or: Modify zone QBIT to make it a stronger attractor
zones["FC-ARCADE"].qbit_aggregate += 500
zones["FC-ARCADE"].resonance += 25
```

**Effect:** Arcade becomes computational "hot spot" - NPCs route toward it, player feels pull

---

#### 6. **Timeline/Era State Management**

4 eras = 4 execution contexts:
```python
# Era as separate state checkpoints
eras = {
    "1981": MallOSState(cloud=0, objects=[...fresh_pizza, shiny_token...]),
    "1995": MallOSState(cloud=11, objects=[...normal_objects...]),
    "2005": MallOSState(cloud=58, objects=[...moldy_pizza, tarnished_token...]),
    "2011": MallOSState(cloud=92, objects=[...deteriorated_objects...]),
}

# Timeline shift = context switch
current_era = eras["1995"]
# Later...
current_era = eras["2011"]  # Load new state, objects transform
```

**Or:** Timeline is continuous, objects mutate in-place based on Cloud level?

---

#### 7. **Object Lifecycle (Spawn/Despawn)**

Static vs dynamic circuit:
```python
# Static: Objects exist for entire session
instantiate_objects(game_state, registry, world)  # Called once at boot

# Dynamic: Objects appear/disappear based on system state
def tick():
    if cloud.level > 70 and "ARCADE_TOKEN" not in active_objects:
        spawn_object("ARCADE_TOKEN", zone="FC-ARCADE")  # Hot-swap component

    if cloud.level < 30 and "ARCADE_TOKEN" in active_objects:
        despawn_object("ARCADE_TOKEN")  # Remove when system cools
```

**MallOS interpretation:** Load-dependent hardware configuration

---

## Proposed Data Flow

```
PLAYER INTERACTS WITH VOXEL OBJECT
    ↓
handle_object_interaction(game_state, voxel_object)
    ↓
Parse behavior.on_pickup actions:
    ↓
    ├─→ cloud_pressure+1 → Cloud.adjust_pressure(+1)
    ├─→ zone.qbit_aggregate+charisma → Zone state update
    ├─→ flag:FOUND_TOKEN=true → Game state flags
    ├─→ subtitle: '...' → Event log / UI message
    └─→ spawn:TODDLER → Trigger entity spawn
    ↓
Cloud pressure change propagates:
    ↓
    ├─→ Update adjacency probabilities (high-QBIT zones become attractors)
    ├─→ Check NPC thresholds (Janitor at Cloud ≥70 → LLM trigger)
    ├─→ Update renderer glitch_intensity (Cloud → visual effects)
    └─→ Check bleed tier (Cloud >80 → reality fault)
```

---

## Implementation Recommendations

### Phase 1: Direct Integration (Simplest)
- Objects modify Cloud pressure directly (synchronous)
- No QBIT scoring for objects yet
- Local zone effects only
- Static spawn (load once)

### Phase 2: Spatial Propagation
- Objects affect zone turbulence/resonance
- Adjacency-weighted propagation
- Objects influence routing probabilities

### Phase 3: Full Computational Model
- Objects have QBIT scores
- NPC process contention (shared resources)
- Dynamic spawn based on Cloud level
- Timeline state management

---

## Architecture Decisions (LOCKED)

### 1. Zone Node Address Space
**Decision:** Tiles = memory addresses within zone's local state
- Zone = compute node / NUMA region
- Tile = `zone.local_state.tiles[(tx, ty)]`
- Global logic uses zones; local interactions use tiles
- Pathfinding/collision uses tiles; Cloud/QBIT uses zones

### 2. Data Flow Topology
**Decision:** Local write (unicast) + periodic propagation
- Object pickup → `zone.cloud_pressure += delta` (unicast to zone node)
- Cloud propagation pass → multicast via adjacency (later)
- NO global broadcast on individual object pickup

### 3. Heat Sink Placement (PIZZA_SLICE -3)
**Decision:** Local cooling only
- `zone.cloud_pressure -= 3` (current zone only)
- Optional: Lower traversal cost for N ticks (zone becomes easier to route through)
- No global AC effect

### 4. Load Balancing Strategy
**Decision:** New sub-driver within player lane
- Keep existing: player: 0.50, NPC: 0.25, QBIT: 0.15, ambient: 0.10
- Split player lane: `player_actions: 0.35` + `object_pickups: 0.15`
- Object effects tracked separately but don't shrink other drivers

### 5. NPC Process Priority (Janitor Mop)
**Decision:** Shared resource contention → pursuit behavior
- Mop has `owner_npc_id = "UNIT_7"`
- Player pickup → `janitor_mop_conflict = true`
- Janitor's process priority increases (scheduler boost)
- Routing probabilities shift toward player
- Unlocks "you've got my mop" dialogue at high Cloud
- NOT a passive QBIT buff - active contention pattern

### 6. Object QBIT Scores
**Decision:** YES - Objects are micro-nodes with QBIT vectors
```python
JANITOR_MOP: power=500, charisma=100
ARCADE_TOKEN: power=50, charisma=800
PIZZA_SLICE: power=20, charisma=50
```
- When spawned: `zone.qbit_aggregate += object.qbit_vector`
- When picked up: Remove from zone, optionally add to player's QBIT aura

### 7. Adjacency Matrix Updates
**Decision:** Temporary routing overrides, not full recalc
- Stable baseline adjacency matrix
- Short-lived "routes of interest" overlays
- Token pickup → 0.8 probability to arcade for N ticks (10-30)
- Decay back to baseline after timeout
- DON'T recalculate full matrix every event

### 8. Timeline State Isolation (4 Eras)
**Decision:** Same circuit, different operating profiles
- Eras = different configs of same HPC fabric
- Each era has:
  - Different adjacency matrix (topology shifts)
  - Different Cloud/QBIT baselines
  - Different object sets/visuals
- NOT parallel universes - profile changes of one system

### 9. Object State Vectors (Behavior Scripts)
**Decision:** Atomic transactions via simple message queue
- On pickup: Enqueue `ObjectEvent` with all actions
- Next tick: Process atomically (or rollback if fails)
- Synchronous per tick, conceptually atomic
- Don't stall the frame

### 10. Spawn/Despawn Circuit Reconfiguration
**Decision:** Static boot + dynamic hot-swap capability
- Boot: `instantiate_objects()` for baseline circuit per era
- Later: Cloud-aware spawning (high Cloud → more tokens)
- Era change → reconfigure topology
- Design for hot-swapping, implement static first

### Bonus: PND3D Integration
**Decision:** Pure renderer (Python core → IPC → PND3D visualization)
- Python = HPC/simulation core (all game logic)
- PND3D = scope, not brain
- Optional spatial query accelerator later (octrees)
- NO game logic in PND3D

---

## Implementation Plan

### Phase 1: Core Integration (NOW)
1. ✅ Tile-based addressing in zone local state
2. ✅ Object → Zone cloud pressure (unicast)
3. ✅ Atomic behavior script processing
4. ✅ Static spawn at boot per era
5. ✅ Basic object-Cloud-NPC feedback loop

### Phase 2: Spatial Effects
1. Zone turbulence/resonance from objects
2. Temporary adjacency overrides (routing bias)
3. Heat sink traversal cost modulation
4. Local-to-global pressure propagation

### Phase 3: Full QBIT Model
1. Object QBIT scoring implementation
2. Zone aggregate calculation with objects
3. NPC resource contention (mop stealing)
4. Dynamic spawn based on Cloud level
5. Era topology switching

---

## Ready to Build

All architecture questions answered. Proceeding to implementation.

---

**The mall is a computer. The voxel objects are the I/O devices. MallOS is the kernel.**

**We're building an operating system you can walk through.**
