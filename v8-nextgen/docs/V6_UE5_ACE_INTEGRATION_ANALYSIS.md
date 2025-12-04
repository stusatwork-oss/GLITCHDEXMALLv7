# V6 UE5 ACE Integration Analysis
**GLITCHDEX MALL - Engine Integration Gap Report**

**Generated:** 2025-11-26
**Purpose:** Bridge existing Python simulation to UE5 AI Character Engine (ACE)
**Approach:** Python-as-Brain, UE5-as-Renderer (pragmatic path)

---

## Executive Summary

**Status:** V6 has a sophisticated Python-based simulation core (QBIT, Cloud, Zone topology, NPC spines) but lacks the **bridge layer** to integrate with UE5's ACE systems.

**Recommendation:** Keep Python as the simulation director. Build a thin bridge layer that exposes a clean tick-based API to UE5. This avoids expensive C++ porting while leveraging existing mature systems.

**Missing:** Config serialization, tick interface contract, example integration payloads, UE5 binding spec.

---

## 1. SIMULATION CORE (What Already Exists)

### ✅ **QBIT / Influence Engine**
- **Location:** `ai/spynt/engine.js`, `ai/spynt/entity_influence_spine.json`
- **Capability:** Entity influence scoring, narrative physics
- **State:** Conceptual framework defined, needs production implementation

### ✅ **Zone / Adjacency Topology**
- **Location:** `ai/mallOS/ZONE_GUIDE.md`, `ai/mallOS/SUBLEVEL_TOPOLOGY_MAP.md`
- **Capability:** Recursive architecture, zone relationships, impossible geometry
- **State:** Well-documented, needs runtime loader

### ✅ **Cloud State System**
- **Location:** `v4-renderist/src/cloud.py`
- **Capability:**
  - Global pressure (0-100)
  - 4 mood states (CALM, UNEASY, STRAINED, CRITICAL)
  - Zone microstates with turbulence/resonance
  - Persistent state across sessions
- **State:** ✅ **PRODUCTION READY**

### ✅ **NPC State Machines**
- **Location:** `v2-immersive-sim/src/npc_intelligence.py`, `v4-renderist/src/anchor_npcs.py`
- **Capability:**
  - **V2 System:** A* pathfinding, GOAP, personal memory, awareness levels
  - **V4 System:** Domain locks, Never-Lists, Contradiction triggers, Visual anchors
  - **MallOS System:** Spine templates, prop anchors, ritual behaviors
- **State:** ✅ **TWO PRODUCTION SYSTEMS** (need unification decision)

### ✅ **Character Spine Framework**
- **Location:** `ai/spynt/CHARACTER_SPINE_TEMPLATES.md`, `ai/mallOS/NPC_SPINE_INDEX.md`
- **Capability:**
  - Domain Lock (identity gravity)
  - Never-List (hard constraints)
  - Ritual Motion (repeated patterns)
  - Prop Anchors (object dependencies)
  - Cloud Influence (mood modifiers)
- **State:** ✅ **CANONICAL STRUCTURE DEFINED**

### ✅ **Faction & Stealth Systems**
- **Location:** `v2-immersive-sim/src/faction_system.py`, `v2-immersive-sim/src/stealth_system.py`
- **Capability:**
  - Complex faction relationships
  - Vision cones, noise propagation
  - Alert states, gossip system
- **State:** ✅ **V2 PRODUCTION READY** (optional for V6)

### ✅ **Heat / Reality Break System**
- **Location:** `v2-immersive-sim/src/heat_system.py`, `v2-immersive-sim/src/heat5_revelation.py`
- **Capability:** GTA-style wanted system that breaks the fourth wall at max heat
- **State:** ✅ **V2 COMPLETE** (meta-commentary feature)

### ✅ **Test Harnesses**
- **Location:** Various `test_*.py` files in v4
- **State:** Basic validation exists, needs UE5 integration tests

---

## 2. BRIDGE LAYER (What You Probably Lack)

This is the critical gap. From UE5's perspective, all the above collapses into:

> **"Given player + world events, tell me what the world + NPCs do this tick."**

### 🔴 **MISSING: Stable Config Format for Content**

**Need:** Data-driven NPC definitions, not Python code

#### NPC Spine JSON Schema
```json
{
  "npcs": [
    {
      "id": "janitor_al",
      "name": "Al Gorithm",
      "role": "Maintenance Loop Guardian",
      "home_zone": "SERVICE_CORRIDOR",
      "visual": {
        "uniform": "Gray coveralls",
        "iconic_detail": "Clipboard with impossible diagrams",
        "silhouette": "Hunched, methodical",
        "text_anchor": "clipboard janitor loop"
      },
      "spine": {
        "domain_lock": "Maintenance loops must complete",
        "never_list": [
          "NEVER skip a task on the clipboard",
          "NEVER acknowledge impossibility",
          "NEVER leave clipboard behind"
        ],
        "rituals": [
          "Clipboard check every 30 seconds",
          "Mutter task names under breath",
          "Tap vents three times before moving"
        ],
        "props": ["clipboard", "flashlight", "tool_belt"],
        "contradiction_trigger": 75.0,
        "contradiction_action": "Loop becomes visible infinite recursion"
      },
      "dialogue": {
        "normal": [
          "Vent 47-B, check. Vent 47-B, check.",
          "Next task: fluorescent grid inspection, sub-sector 3.",
          "Hmm. That's... that's fine. That's fine."
        ],
        "stressed": [
          "Wait. Did I already— no. Not yet. Not yet.",
          "The list is longer than it was. That's not right.",
          "I should be done by now. Why aren't I done?"
        ],
        "contradiction": [
          "I've been here before. I'm always here. I'll always be here.",
          "[Muttering the same task name in an infinite whisper]",
          "[Clipboard shows identical tasks repeated endlessly]"
        ]
      }
    }
  ]
}
```

#### Zone Topology JSON Schema
```json
{
  "zones": [
    {
      "id": "FC-ARCADE",
      "name": "Food Court - Arcade Zone",
      "level": -1,
      "tags": ["food_court", "entertainment", "noise", "entropy"],
      "neighbors": ["FC-CORE", "SERVICE_CORRIDOR", "HARD_COPY_CORRIDOR"],
      "initial_turbulence": 2.5,
      "cloud_modifiers": {
        "base": 0,
        "on_player_enter": 1,
        "on_discovery": 3
      },
      "spawn_points": [
        {"type": "anchor_npc", "id": "janitor_al", "weight": 0.8},
        {"type": "swarm", "count": "3-7", "weight": 1.0}
      ]
    }
  ]
}
```

**Status:** 🔴 **NOT IMPLEMENTED**
**Priority:** 🔥 **CRITICAL** - Without this, UE5 has nowhere to load content from

---

### 🔴 **MISSING: Clearly Defined Tick Interface**

**Need:** A single Python entry point that UE5 can call

#### Proposed API Contract

```python
# sim_bridge.py

def init_world(config_path: str) -> WorldState:
    """
    Load world configuration and initialize simulation.

    Args:
        config_path: Path to JSON config with zones, NPCs, rules

    Returns:
        WorldState object with initial state
    """
    pass

def tick_world(
    world: WorldState,
    dt: float,
    player_event: dict | None = None
) -> FrameUpdate:
    """
    Advance simulation by one tick.

    Args:
        world: Current world state
        dt: Delta time in seconds (e.g., 0.25)
        player_event: Optional player action this frame
            Examples:
            {"type": "move", "to_zone": "FC-ARCADE"}
            {"type": "interact", "target": "bag_of_screams"}
            {"type": "wait"}

    Returns:
        FrameUpdate with NPC states, Cloud values, zone changes
    """
    pass
```

#### Frame Update Schema
```json
{
  "timestamp": 1234.56,
  "cloud": {
    "level": 67.3,
    "mood": "STRAINED",
    "trend": "RISING"
  },
  "npcs": [
    {
      "id": "janitor_al",
      "state": "STRESSED",
      "zone": "SERVICE_CORRIDOR",
      "hint": "pace_near_player",
      "dialogue": "Wait. Did I already— no. Not yet.",
      "stress_level": 0.73,
      "should_trigger_contradiction": false
    },
    {
      "id": "uncle_danny",
      "state": "NORMAL",
      "zone": "FC-CORE",
      "hint": "cooking_idle",
      "dialogue": "Grilled cheese fixes everything, kid.",
      "stress_level": 0.12
    }
  ],
  "zones": {
    "FC-ARCADE": {
      "turbulence": 4.2,
      "resonance": 1.1,
      "swarm_count": 5
    }
  },
  "events": [
    {
      "type": "contradiction_triggered",
      "npc": "janitor_al",
      "severity": "MINOR"
    }
  ]
}
```

**Status:** 🔴 **NOT IMPLEMENTED**
**Priority:** 🔥 **CRITICAL** - This IS the bridge

---

### 🟡 **DECISION NEEDED: Interop Strategy**

Two realistic paths:

#### **Option A: Python-as-Service (RECOMMENDED)**

**Architecture:**
```
┌─────────────────────────────────────────────┐
│  UE5 Game Instance                          │
│  ┌────────────────────────────────────────┐ │
│  │  MallSimulationSubsystem (C++)         │ │
│  │  - Connects to Python via HTTP/TCP     │ │
│  │  - Sends player events                 │ │
│  │  - Receives NPC updates                │ │
│  └─────────────────┬──────────────────────┘ │
└────────────────────┼────────────────────────┘
                     │ JSON over HTTP
                     ▼
┌─────────────────────────────────────────────┐
│  Python Simulation Server                   │
│  ┌────────────────────────────────────────┐ │
│  │  sim_bridge.py                         │ │
│  │  - Runs Cloud.tick()                   │ │
│  │  - Updates NPC states                  │ │
│  │  - Returns frame updates               │ │
│  └────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────┐ │
│  │  Existing Systems                      │ │
│  │  - cloud.py                            │ │
│  │  - anchor_npcs.py                      │ │
│  │  - npc_intelligence.py                 │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

**Pros:**
- ✅ Keeps all existing Python code
- ✅ Fast iteration (no C++ recompile)
- ✅ Easy debugging (Python REPL)
- ✅ Can run sim standalone for testing

**Cons:**
- ⚠️ Network latency (mitigate: localhost, binary protocol)
- ⚠️ Deployment complexity (ship Python runtime)

**Recommendation:** ✅ **USE THIS for V6 prototype**

---

#### **Option B: Port to C++/Blueprint**

**Architecture:**
```
┌─────────────────────────────────────────────┐
│  UE5 Native Implementation                  │
│  ┌────────────────────────────────────────┐ │
│  │  UCloudStateSubsystem (C++)            │ │
│  │  UNPCSpineComponent (C++)              │ │
│  │  Behavior Trees + EQS                  │ │
│  │  Data Assets (JSON → DataTables)       │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

**Pros:**
- ✅ No network overhead
- ✅ Native UE5 debugging tools
- ✅ Easier for non-Python teams

**Cons:**
- ❌ Expensive porting effort (2-4 weeks minimum)
- ❌ Slower iteration (C++ recompile cycles)
- ❌ Lose Python prototyping speed

**Recommendation:** ⏸️ **DEFER to production phase** (if needed)

---

### 🔴 **MISSING: Timing Decision**

**Question:** How often does UE5 call `tick_world()`?

#### Option 1: Fixed Interval (Recommended)
```cpp
// UE5 C++ - GameInstance Subsystem
void UMallSimSubsystem::Tick(float DeltaTime)
{
    SimAccumulator += DeltaTime;

    if (SimAccumulator >= 0.25f)  // 4 Hz simulation tick
    {
        SendTickToSimulation(SimAccumulator);
        SimAccumulator = 0.0f;
    }
}
```

**Recommendation:** **0.25s (4 Hz)** - smooth enough, low overhead

#### Option 2: Event-Driven Only
Only call `tick_world()` when player does something significant.

**Pros:** Lower overhead
**Cons:** NPCs freeze between player actions (not immersive)

**Recommendation:** ❌ **DON'T USE** - breaks ambient life

---

## 3. UE5 SIDE: What a Dev Actually Needs

### 🔴 **MISSING: Engine Contract Document**

**Need:** One-page spec for UE5 developers

#### Proposed "Mall Simulation Contract v1.0"

```markdown
# Mall Simulation Engine Contract

## Initialization
POST /init
Body: {"config_path": "content/mall_config_v6.json"}
Returns: {"world_id": "abc123", "status": "ready"}

## Tick Update
POST /tick
Body: {
    "world_id": "abc123",
    "dt": 0.25,
    "player_event": {
        "type": "move",
        "from_zone": "FC-CORE",
        "to_zone": "FC-ARCADE",
        "timestamp": 123.45
    }
}
Returns: {
    "cloud": {...},
    "npcs": [...],
    "zones": {...},
    "events": [...]
}

## Timing
- Call /tick every 0.25s of game time
- Or on discrete player actions (move, interact, wait)
- Simulation is deterministic given same inputs

## Player Event Types
- {"type": "move", "to_zone": "ZONE_ID"}
- {"type": "interact", "target": "OBJECT_ID"}
- {"type": "discover", "document": "DOC_ID"}
- {"type": "wait"}
```

**Status:** 🔴 **NOT WRITTEN**
**Priority:** 🔥 **HIGH** - Devs can't integrate without this

---

### 🔴 **MISSING: Minimal Content Pack**

**Need:** Example data to test integration

#### Proposed Content Pack v6.0-minimal

**File:** `v6-nextgen/data/config/minimal_content_pack.json`

```json
{
  "version": "6.0-minimal",
  "npcs": [
    "janitor_al",      // The loop man
    "uncle_danny",     // Grilled cheese priest
    "security_wolf",   // Security sergeant
    "swarm_shopper_01" // Generic customer
  ],
  "zones": [
    "FC-CORE",         // Food court center
    "FC-ARCADE",       // Arcade zone (entropy)
    "SERVICE_CORRIDOR", // Janitor domain
    "MAIN_HALL"        // Upper level
  ],
  "scenarios": [
    {
      "id": "janitor_loop_demo",
      "description": "Janitor gets stuck in maintenance loop as Cloud rises",
      "initial_cloud": 60.0,
      "player_start": "SERVICE_CORRIDOR",
      "trigger": {
        "type": "cloud_threshold",
        "value": 75.0
      },
      "expected_outcome": "Janitor contradiction triggers, loop becomes visible"
    }
  ]
}
```

**Status:** 🔴 **NOT CREATED**
**Priority:** 🔥 **HIGH** - Can't test without sample data

---

### 🔴 **MISSING: UE5 Binding Specification**

**Need:** How UE5 interprets simulation responses

#### Proposed Binding Spec

**File:** `v6-nextgen/docs/UE5_BINDING_SPEC.md`

```markdown
# UE5 Response Binding Specification

## NPC State → UE5 Actions

| NPC State | Blackboard Key | Animation State | Audio Cue |
|-----------|----------------|-----------------|-----------|
| NORMAL | NPC_State=0 | Idle_Casual | None |
| STRESSED | NPC_State=1 | Fidget_Loop | Mutter_Stressed |
| CONTRADICTED | NPC_State=2 | Glitch_Anim | Contradiction_SFX |

## NPC Hint → Behavior Tree Task

| Hint | BT Task Node |
|------|--------------|
| "pace_near_player" | BTTask_PaceAroundTarget |
| "cooking_idle" | BTTask_CookingAnimation |
| "patrol_route" | BTTask_FollowPatrolRoute |
| "freeze_loop" | BTTask_RepeatInPlace |

## Cloud Mood → Environment

| Mood | Post-Process | Audio Mix | Light Intensity |
|------|--------------|-----------|-----------------|
| CALM | PP_Normal | Mix_Ambient | 1.0 |
| UNEASY | PP_SlightGrain | Mix_Tense | 0.95 |
| STRAINED | PP_ChromaShift | Mix_Strained | 0.85 |
| CRITICAL | PP_Glitch | Mix_Critical | 0.7 (flicker) |

## Zone Turbulence → VFX

| Turbulence | VFX Particle System |
|------------|---------------------|
| 0-3 | None |
| 3-6 | VFX_AirShimmer_Subtle |
| 6-8 | VFX_SpaceDistortion_Medium |
| 8+ | VFX_RealityTear_Heavy |
```

**Status:** 🔴 **NOT WRITTEN**
**Priority:** 🟡 **MEDIUM** - Helpful but not blocking

---

## 4. MISSING IMPLEMENTATION FILES

### 🔴 **Bridge Implementation**

**File:** `v6-nextgen/src/sim_bridge.py`
**Status:** 🔴 **DOES NOT EXIST**
**Contents Should Include:**
- `init_world(config_path: str) -> WorldState`
- `tick_world(world, dt, player_event) -> FrameUpdate`
- JSON schema validation
- State serialization/deserialization

---

### 🔴 **HTTP/TCP Server (if using Option A)**

**File:** `v6-nextgen/src/sim_server.py`
**Status:** 🔴 **DOES NOT EXIST**
**Contents Should Include:**
- Flask/FastAPI REST endpoints
- `/init`, `/tick`, `/shutdown` routes
- Request/response validation
- Error handling

---

### 🔴 **Config Loader**

**File:** `v6-nextgen/src/config_loader.py`
**Status:** 🔴 **DOES NOT EXIST**
**Contents Should Include:**
- Load NPC definitions from JSON
- Load zone topology from JSON
- Validate schemas
- Hot-reload support (dev mode)

---

### 🔴 **Unified NPC System**

**Current State:** Two separate systems (v2 and v4)
**Need:** Decide which to use or merge them

**Decision Matrix:**

| Feature | V2 System | V4 System |
|---------|-----------|-----------|
| Pathfinding | ✅ A* | ❌ No |
| Memory | ✅ Personal memory | ❌ No |
| Stealth | ✅ Vision cones | ❌ No |
| Spines | ❌ Basic states | ✅ Domain locks |
| Cloud Integration | ❌ No | ✅ Yes |
| Production Ready | ✅ Yes | ✅ Yes |

**Recommendation:**
- Use **V4 spine system** for character identity
- Add **V2 pathfinding** as optional module
- Create **v6-nextgen/src/unified_npc.py** that combines both

---

## 5. CRITICAL PATH TO UE5 INTEGRATION

### Phase 1: Bridge Layer (Week 1-2)
- [ ] Create `sim_bridge.py` with init/tick API
- [ ] Define JSON schemas for NPCs, zones
- [ ] Implement `tick_world()` core loop
- [ ] Write unit tests for bridge

### Phase 2: Content Pack (Week 2-3)
- [ ] Export 4-5 NPCs to JSON (janitor, danny, security, shoppers)
- [ ] Export 4-6 zones to JSON
- [ ] Create minimal config pack
- [ ] Validate against schemas

### Phase 3: Server Option (Week 3-4)
- [ ] Implement Flask/FastAPI server
- [ ] Add `/init`, `/tick` endpoints
- [ ] Test with curl/Postman
- [ ] Write integration tests

### Phase 4: UE5 Test Harness (Week 4-5)
- [ ] Create minimal UE5 project
- [ ] Implement C++ subsystem that calls Python
- [ ] Bind one NPC (janitor) to test
- [ ] Verify Cloud → lighting binding
- [ ] Document results

### Phase 5: Documentation (Week 5-6)
- [ ] Write Engine Contract document
- [ ] Write UE5 Binding Spec
- [ ] Create example payloads
- [ ] Record video walkthrough

---

## 6. LONG-TERM GAPS (Production Polish)

These are NOT blocking for prototype but needed for shipping:

### 🟡 **Performance Optimization**
- Binary protocol instead of JSON (Protocol Buffers, MessagePack)
- Caching/memoization in tick loop
- Multithreading for independent NPCs
- LOD system for distant NPCs

### 🟡 **UE5 Native Features**
- Behavior Trees (replace Python state machines)
- EQS (Environment Query System) for spatial queries
- Navigation Mesh integration
- Animation Blueprint bindings
- Gameplay Ability System (GAS) for NPC actions

### 🟡 **Content Authoring Tools**
- Visual editor for NPC spines (UMG tool)
- Zone topology graph editor
- Cloud state debugger (realtime visualization)
- Contradiction scenario editor

### 🟡 **Deployment**
- Package Python runtime with game
- Or: Compile Python to C++ (Cython, Nuitka)
- Or: Full C++ port (expensive, defer)

---

## 7. EXISTING ASSETS THAT HELP

### ✅ **You Already Have:**

1. **Cloud System** (`v4-renderist/src/cloud.py`)
   - Drop-in ready for bridge layer
   - Just needs JSON config loader

2. **NPC Spine Framework** (`ai/mallOS/`, `ai/spynt/`)
   - Templates exist, need JSON export
   - Domain locks, Never-Lists are production-grade

3. **Zone Topology** (`ai/mallOS/ZONE_GUIDE.md`)
   - Well-documented, needs JSON format

4. **Character Examples** (`ai/mallOS/NPC_SPINE_INDEX.md`)
   - 13+ NPCs defined
   - Can export to JSON directly

5. **Test Scenarios** (V4 demo, V2 systems)
   - Janitor loop exists
   - Uncle Danny grilled cheese logic exists
   - Can become test cases

---

## 8. RECOMMENDED NEXT STEPS

### Immediate (This Week)
1. ✅ **Read this document** - you are here
2. 🔴 **Create `sim_bridge.py` stub** - 100 lines, just API surface
3. 🔴 **Export 1 NPC to JSON** - janitor_al.json with full spine
4. 🔴 **Write example tick payload** - show what UE5 would send/receive

### Short-Term (Next 2 Weeks)
5. 🔴 **Implement `tick_world()` minimal** - Cloud + 1 NPC
6. 🔴 **Create Flask server** - `/init`, `/tick` endpoints
7. 🔴 **Test with curl** - prove it works standalone
8. 🔴 **Document Engine Contract** - one-page spec for devs

### Medium-Term (Next Month)
9. 🟡 **UE5 test project** - blank project + HTTP client
10. 🟡 **Bind janitor NPC** - prove end-to-end works
11. 🟡 **Add Cloud → lighting** - prove environment responds
12. 🟡 **Record demo video** - show it working

---

## 9. CONCLUSION

**You have:** A sophisticated simulation brain (Python)
**You lack:** The bridge to UE5's body

**Gap severity:** 🔴 **CRITICAL** for integration, but **NOT COMPLEX** to fix

**Effort estimate:**
- Bridge layer: 40-60 hours
- Content export: 20-30 hours
- UE5 test harness: 30-40 hours
- **Total: 90-130 hours** (3-4 weeks full-time)

**Blocker risk:** ⚠️ **MEDIUM**
- Python-as-service is proven tech (games use it)
- Flask/HTTP is well-understood
- No exotic dependencies

**Recommended path:**
1. Build bridge layer in Python (this week)
2. Test standalone (next week)
3. UE5 prototype (week 3-4)
4. Evaluate if full C++ port needed (probably not)

**Key insight:** Your simulation is **MORE SOPHISTICATED** than most UE5 ACE implementations. Don't throw it away by porting. Wrap it in a thin API and let UE5 consume it as a service.

---

**End of Report**

**Next Document:** `V6_BRIDGE_IMPLEMENTATION_SPEC.md` (API details + code examples)
**Related:** `UE5_INTEGRATION_COOKBOOK.md` (step-by-step UE5 setup)
