# ENGINE SPECIFICATION & INTEGRATION REPORT
## Visual Runtime Entry - Debugging & Refactoring Log

**Date**: 2025-12-05
**Target**: Get Visual_Runtime_Entry.py running with player movement
**Status**: 🔴 BLOCKED - Missing methods and files preventing initialization

---

## EXECUTIVE SUMMARY

Attempted to launch `NEW-needs_integration/Visual_Runtime_Entry.py` to validate v8 visual runtime. The program successfully imports all modules and begins initialization, but fails during `NinjaGameMode` constructor due to:

1. Missing `GameStateLoader.bootstrap()` method
2. Missing game state JSON files
3. JSON parse errors in canon files
4. PIL/Pillow not installed (non-critical - sprites skipped)

**Current Blocker**: Line 73 in `ninja_loop.py` calls `self.state_loader.bootstrap(self.consensus, self.flock)` but this method doesn't exist in `state_manager.py`.

---

## BOOT SEQUENCE ANALYSIS

### Phase 1: Environment Initialization ✅
```
pygame 2.6.1 (SDL 2.28.4, Python 3.11.14)
Hello from the pygame community. https://www.pygame.org/contribute.html
```

**Status**: SUCCESS
**Note**: Pygame installed and initialized correctly

### Phase 2: Audio/Display Warnings ⚠️
```
error: XDG_RUNTIME_DIR is invalid or not set in the environment.
ALSA lib confmisc.c:855:(parse_card) cannot find card '0'
[...multiple ALSA errors...]
```

**Status**: EXPECTED (headless container environment)
**Impact**: Non-critical - no audio/display in container
**Action**: Ignore these warnings for CLI testing

### Phase 3: Package Structure Resolution ✅

**Problem**: Import errors for `ninja` package
**Solution**: Created `/v8-nextgen/ninja/` package with:
- `__init__.py` - Package initialization
- `ninja_loop.py` - Copied from `NEW-needs_integration/ninja_game_loop.py`
- `pfdl.py` - Copied from `NEW-needs_integration/PFDL_Kernel.py`
- `voxel_bridge.py`, `ninja_assets.py`, `standard_assets.py`, etc.

Also created src-level imports:
- `src/ninja_grid.py` - Copied from `NEW-needs_integration/upgraded_grid_generator.py`
- `src/ninja_npc.py` - Copied from `NEW-needs_integration/Ninja_NPC_with_PFDL.py`

**PYTHONPATH**: Set to `/home/user/GLITCHDEXMALLv7/v8-nextgen:/home/user/GLITCHDEXMALLv7/v8-nextgen/src`

### Phase 4: Asset Path Resolution ✅

**Problem**: `repo_root` calculated as `/home/user/GLITCHDEXMALLv7` (2 levels up from `ninja/ninja_loop.py`)
**Solution**: Created symlink `/home/user/GLITCHDEXMALLv7/assets` → `v8-nextgen/assets`

Created missing directories:
- `assets/voxel_sources/ninja/`
- `assets/voxel_sources/standard/`

### Phase 5: Asset Generation ✅ (Partial)
```
[INIT] Booting NINJA_SABOTEUR v8.0 (Level: game_state_foodcourt_v1.json)...
[ASSETS] PIL not found. Skipping sprite generation.
[ASSETS] Seeded Ninja assets in /home/user/GLITCHDEXMALLv7/assets/voxel_sources/ninja
[ASSETS] Seeded 5 Standard Voxel Objects in /home/user/GLITCHDEXMALLv7/assets/voxel_sources/standard
```

**Status**: PARTIAL SUCCESS
**Generated Files**:
- `ninja_smoke.json`
- `ninja_noise.json`
- `ninja_decoy.json`
- `ninja_jammer.json`
- `ninja_tripwire.json`
- Standard voxel objects (5 files)

**Not Generated**: PNG sprites (requires Pillow: `pip install Pillow`)
**Impact**: Visual rendering will use fallback colors instead of textures

### Phase 6: Game State Loading ❌
```
[STATE] Error loading game_state_foodcourt_v1.json:
[Errno 2] No such file or directory: 'game_state_foodcourt_v1.json'
```

**Status**: FAILED
**Root Cause**: No game state JSON files exist
**Expected Location**: Current working directory or data/ subdirectory
**Impact**: Runtime falls back to defaults

**Missing Files**:
- `game_state_foodcourt_v1.json`
- `game_state_servicehall_v1.json`

### Phase 7: Grid Generation ✅
```
[GRID] Generated Z4_FOOD_COURT at 100ft Scale (40x40 tiles)
```

**Status**: SUCCESS
**Note**: `NinjaGrid` successfully generated food court layout from zone specs

### Phase 8: Canon Data Loading ❌ (Partial)
```
[CLOUD/QBIT] Error loading BALES_CANONICAL.json:
Extra data: line 60 column 1 (char 1624)

[CLOUD/QBIT] Error loading QBIT_ENTITY_INFLUENCE_SPINE.json:
Expecting property name enclosed in double quotes: line 4 column 35 (char 90)

[CLOUD/QBIT] Loaded and scored 15 entities
[CLOUD/QBIT] Calculated aggregates for 11 zones
```

**Status**: PARTIAL SUCCESS (graceful degradation)
**Impact**: Some canon data loaded despite JSON errors

**Files with Parse Errors**:
1. `canon/zone/BALES_CANONICAL.json` - Line 60, char 1624 (extra data after valid JSON)
2. `canon/qbit/QBIT_ENTITY_INFLUENCE_SPINE.json` - Line 4, char 90 (malformed property name)

**Action Required**: Validate and fix JSON syntax in these files

### Phase 9: Cloud System Initialization ⚠️
```
[CLOUD] No saved state found. Starting fresh.
```

**Status**: WARNING (non-critical)
**Impact**: Cloud starts at default pressure instead of saved state

### Phase 10: Bootstrap Call ❌ CRITICAL FAILURE
```
[ERR] Load failed: 'GameStateLoader' object has no attribute 'bootstrap'
```

**Status**: CRITICAL FAILURE
**Location**: `ninja_loop.py:73`
**Code**:
```python
self.state_loader.bootstrap(self.consensus, self.flock)
```

**Root Cause**: `GameStateLoader` class in `ninja/state_manager.py` is missing the `bootstrap()` method

**Expected Signature** (inferred from call site):
```python
def bootstrap(self, consensus: ConsensusEngine, flock: CloudFlock) -> None:
    """
    Bootstrap consensus and flock systems with saved/default state.

    Args:
        consensus: Consensus engine to initialize
        flock: Cloud flock particle system to seed
    """
    pass  # Implementation required
```

**Impact**: NinjaGameMode constructor raises exception, `self.sim` remains `None`

### Phase 11: Runtime Loop ❌
```
Traceback (most recent call last):
  File ".../Visual_Runtime_Entry.py", line 128, in <module>
    VisualRuntime().run()
  File ".../Visual_Runtime_Entry.py", line 66, in run
    state = self.sim.tick(dt, cmd)
            ^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'tick'
```

**Status**: BLOCKED
**Cause**: `self.sim` is `None` because `NinjaGameMode()` constructor failed at Phase 10
**Result**: Cannot enter game loop, no window shown, player cannot move

---

## CRITICAL ISSUES (Blocking Runtime)

### 1. Missing GameStateLoader.bootstrap() Method
**File**: `ninja/state_manager.py`
**Line**: N/A (method doesn't exist)
**Severity**: 🔴 CRITICAL
**Blocks**: Game initialization

**Required Implementation**:
```python
def bootstrap(self, consensus: ConsensusEngine, flock: CloudFlock) -> None:
    """
    Bootstrap consensus and cloud flock with initial/saved state.

    Should:
    - Inject thermal noise into consensus field
    - Seed cloud flock particles with initial positions/velocities
    - Apply any saved state modifiers
    """
    # Check if loaded state has bootstrap data
    if "bootstrap" in self.state:
        bootstrap_data = self.state["bootstrap"]

        # Inject thermal noise
        if "thermal_noise" in bootstrap_data:
            for zone_id, noise_level in bootstrap_data["thermal_noise"].items():
                consensus.inject_thermal_noise(zone_id, noise_level)

        # Seed flock particles
        if "flock_seeds" in bootstrap_data:
            for particle in bootstrap_data["flock_seeds"]:
                flock.add_particle(particle["x"], particle["y"],
                                   particle.get("vx", 0),
                                   particle.get("vy", 0))
    else:
        # Default bootstrap: Random thermal noise + uniform flock
        for _ in range(40):  # Match flock.count from ninja_loop.py:72
            import random
            x = random.randint(0, flock.width - 1)
            y = random.randint(0, flock.height - 1)
            flock.add_particle(x, y,
                               random.uniform(-1, 1),
                               random.uniform(-1, 1))
```

**Workaround**: Add stub method that does nothing, allow runtime to continue

---

## HIGH-PRIORITY ISSUES (Non-Blocking but Degraded)

### 2. Missing Game State JSON Files
**Files**:
- `game_state_foodcourt_v1.json`
- `game_state_servicehall_v1.json`

**Severity**: 🟡 HIGH
**Impact**: Runtime uses hardcoded defaults, F1/F2 level switching won't work

**Required Schema** (inferred from state_manager.py):
```json
{
  "zone": "Z4_FOOD_COURT",
  "cloud_pressure": 55.0,
  "spawns": [
    ["NINJA_SMOKE", 15, 20],
    ["NINJA_DECOY", 18, 22]
  ],
  "flags": {
    "janitor_aware": false,
    "alarm_triggered": false
  },
  "bootstrap": {
    "thermal_noise": {
      "Z4_FOOD_COURT": 0.3
    },
    "flock_seeds": [
      {"x": 20, "y": 20, "vx": 0.5, "vy": 0.2}
    ]
  }
}
```

**Workaround**: Runtime continues with empty state dict

### 3. JSON Parse Errors in Canon Files
**Files**:
- `canon/zone/BALES_CANONICAL.json` - Extra data at line 60
- `canon/qbit/QBIT_ENTITY_INFLUENCE_SPINE.json` - Malformed property at line 4

**Severity**: 🟡 HIGH
**Impact**: Some entity/zone data not loaded, may cause inconsistent behavior

**Action**: Run JSON validator and fix syntax errors

---

## MEDIUM-PRIORITY ISSUES (Quality of Life)

### 4. Missing PIL/Pillow for Sprite Generation
**Severity**: 🟢 MEDIUM
**Impact**: Voxel objects render as colored rectangles instead of textured sprites

**Fix**: `pip install Pillow`

**Benefits**:
- Proper smoke particle sprites
- Ninja construct icons
- Better visual clarity

### 5. Repo Root Path Calculation
**File**: `ninja/ninja_loop.py:39`
**Current**: `self.repo_root = Path(__file__).parents[2]`
**Issue**: Calculates to `/home/user/GLITCHDEXMALLv7` instead of `.../v8-nextgen`

**Severity**: 🟢 MEDIUM
**Current Workaround**: Symlink `/home/user/GLITCHDEXMALLv7/assets` → `v8-nextgen/assets`

**Better Fix**: Change to `parents[1]` and update all asset paths

### 6. ALSA/XDG Runtime Warnings
**Severity**: 🟢 LOW
**Impact**: None (expected in containers)

**Optional Suppression**:
```bash
export SDL_AUDIODRIVER=dummy
export XDG_RUNTIME_DIR=/tmp/runtime-$USER
```

---

## FILE INTEGRATION MAP

### Files Successfully Integrated:
| Source File | Destination | Status |
|-------------|-------------|--------|
| `ninja_game_loop.py` | `ninja/ninja_loop.py` | ✅ Copied |
| `PFDL_Kernel.py` | `ninja/pfdl.py` | ✅ Copied |
| `upgraded_grid_generator.py` | `src/ninja_grid.py` | ✅ Copied |
| `Ninja_NPC_with_PFDL.py` | `src/ninja_npc.py` | ✅ Copied |
| `voxel_bridge.py` | `ninja/voxel_bridge.py` | ✅ Copied |
| `ninja_assets.py` | `ninja/ninja_assets.py` | ✅ Copied |
| `standard_assets.py` | `ninja/standard_assets.py` | ✅ Copied |
| `state_manager.py` | `ninja/state_manager.py` | ✅ Copied |
| `cloud_flocking.py` | `ninja/cloud_flocking.py` | ✅ Copied |
| `consensus_engine.py` | `ninja/consensus_engine.py` | ✅ Copied |

### Files Pending Integration:
| File | Purpose | Integration Target |
|------|---------|-------------------|
| `cutscene_manaer.py` | Cutscene system | `src/cutscene_manager.py` |
| `cutscene_assets.py` | Cutscene asset loader | `src/cutscene_assets.py` |
| `Ninja_Loop_v7.py` | Legacy v7 loop | Archive/compare |
| `updated_V5_Specs.py` | v5 CRD specs | Reference only |

---

## IMPORT DEPENDENCY TREE

```
Visual_Runtime_Entry.py
└── ninja.ninja_loop.NinjaGameMode
    ├── cloud.Cloud ✅ (src/cloud.py)
    ├── ninja_grid.NinjaGrid ✅ (src/ninja_grid.py)
    ├── ninja_npc.ShadowJanitorMachine ✅ (src/ninja_npc.py)
    ├── npc_state_machine.NPCSpine ✅ (src/npc_state_machine.py)
    ├── ninja.pfdl.PFDLKernel ✅ (ninja/pfdl.py)
    ├── ninja.voxel_bridge.VoxelBridge ✅ (ninja/voxel_bridge.py)
    ├── ninja.ninja_assets.seed_ninja_assets ✅ (ninja/ninja_assets.py)
    ├── ninja.standard_assets.seed_standard_assets ✅ (ninja/standard_assets.py)
    ├── ninja.state_manager.GameStateLoader ❌ Missing .bootstrap()
    ├── ninja.cloud_flocking.CloudFlock ✅ (ninja/cloud_flocking.py)
    ├── ninja.consensus_engine.ConsensusEngine ✅ (ninja/consensus_engine.py)
    └── voxel_object_loader.VoxelObjectLoader ✅ (src/voxel_object_loader.py)
```

**Status**: 11/12 modules loaded, 1 method missing

---

## RUNTIME REQUIREMENTS CHECKLIST

- [x] Pygame installed
- [x] Python path includes v8-nextgen and v8-nextgen/src
- [x] ninja package created with __init__.py
- [x] All module files copied to correct locations
- [x] Asset directories created
- [x] Asset generation functions run
- [ ] **GameStateLoader.bootstrap() implemented** ❌ BLOCKING
- [ ] game_state JSON files created
- [ ] Canon JSON files validated and fixed
- [ ] Pillow installed (optional)

---

## NEXT STEPS (Priority Order)

### 1. Implement GameStateLoader.bootstrap() 🔴 CRITICAL
**File**: `ninja/state_manager.py`
**Action**: Add method to bootstrap consensus and flock systems

### 2. Create Game State JSON Files 🟡 HIGH
**Files**: `game_state_foodcourt_v1.json`, `game_state_servicehall_v1.json`
**Location**: v8-nextgen/ or v8-nextgen/data/
**Schema**: See section 2 above

### 3. Fix Canon JSON Parse Errors 🟡 HIGH
**Files**:
- `canon/zone/BALES_CANONICAL.json`
- `canon/qbit/QBIT_ENTITY_INFLUENCE_SPINE.json`

**Action**: Validate with `python -m json.tool <file>` and fix syntax

### 4. Test Player Movement 🟢 MEDIUM
Once runtime initializes:
- Arrow keys for movement
- Space bar for construct placement
- Number keys (1-4) for construct selection
- F1/F2 for level switching
- ESC to quit

### 5. Install Pillow 🟢 LOW
**Command**: `pip install Pillow`
**Benefit**: Proper sprite rendering

---

## EXPECTED RUNTIME BEHAVIOR (Once Fixed)

### Window Specifications:
- **Resolution**: 1280x800
- **Tile Size**: 24px
- **Camera**: Smooth-follow player (10% lerp)
- **FPS Target**: 60

### Player Controls:
- **Movement**: Arrow keys (grid-based, tile snapping)
- **Construct**: Space bar (places selected PFDL construct)
- **Select**: 1=Smoke, 2=Cover, 3=Lure, 4=Coin
- **Level Switch**: F1=Food Court, F2=Service Hall
- **Quit**: ESC

### Visual Layers:
1. Background grid (dark blue)
2. Heatmap overlay (consensus trace field)
3. Wall tiles (gray)
4. Voxel constructs (textured if PIL available)
5. NPC janitor (red square)
6. Player (green square)
7. Cloud flock particles (semi-transparent white)
8. HUD overlay (top-left stats, bottom-left construct menu)

### Expected Console Output (Healthy Boot):
```
[INIT] Booting NINJA_SABOTEUR v8.0 (Level: game_state_foodcourt_v1.json)...
[ASSETS] Generated ninja_smoke.png
[ASSETS] Generated ninja_noise.png
[...5 more assets...]
[ASSETS] Seeded Ninja assets in .../ninja
[ASSETS] Seeded 5 Standard Voxel Objects in .../standard
[STATE] Loaded game_state_foodcourt_v1.json
[GRID] Generated Z4_FOOD_COURT at 100ft Scale (40x40 tiles)
[CLOUD/QBIT] Loaded and scored 15 entities
[CLOUD/QBIT] Calculated aggregates for 11 zones
[CLOUD] Loaded saved state (Cloud: 55.0, Mood: UNEASY)
[BOOTSTRAP] Injected thermal noise into 1 zone(s)
[BOOTSTRAP] Seeded 40 cloud flock particles
[READY] RUNTIME ACTIVE.
```

---

## ARCHITECTURAL NOTES

### Why bootstrap() is Critical:
The consensus engine and cloud flock need initial state to:
1. **Consensus**: Receive "thermal noise" to seed analog field variations (prevents dead zones)
2. **Cloud Flock**: Get particle spawn positions/velocities (visualizes Cloud pressure as emergent behavior)

Without bootstrap(), both systems start in invalid/empty states, causing:
- Consensus field remains uniform (no spatial pressure variation)
- Cloud flock has 0 particles (no visual feedback)
- Zone influence calculations fail (no baseline noise)

### Design Pattern: Graceful Degradation
The engine handles missing data gracefully:
- Missing game state → Uses defaults
- JSON parse errors → Skips invalid entries, loads rest
- Missing sprites → Falls back to colored rectangles
- Missing voxel files → Constructs still function, just invisible

This allows partial testing even with incomplete assets.

---

## PERFORMANCE EXPECTATIONS

### Current Setup (No Optimizations):
- **FPS**: 60 (capped by pygame clock)
- **Grid Size**: 40x40 (1,600 tiles)
- **Flock Particles**: 40
- **NPCs**: 1 (Shadow Janitor)
- **Constructs**: Variable (player-placed)

### Bottleneck Analysis:
1. **Tile Rendering**: ~1,600 rect draws per frame (negligible)
2. **Heatmap Overlay**: Consensus field query per visible tile (~30x20 = 600 queries)
3. **Flock Physics**: 40 particles × velocity/collision updates
4. **NPC State Machine**: 1 tick per frame (QBIT + Vector + Spine checks)

**Projected Load**: ~0.5-1ms per frame (well under 16ms budget for 60fps)

---

## TESTING PROTOCOL (Once Running)

### 1. Boot Test
- [x] Program starts without import errors
- [ ] Window appears (1280x800)
- [ ] Grid renders correctly
- [ ] Player starts at (10, 10)
- [ ] HUD displays stats

### 2. Movement Test
- [ ] Arrow keys move player 1 tile per press
- [ ] Player cannot move through walls
- [ ] Camera follows player smoothly

### 3. Construct Test
- [ ] Press 1-4 to select constructs (menu highlights)
- [ ] Press Space to place construct at player position
- [ ] Construct appears visually
- [ ] Construct affects consensus field (heatmap changes)

### 4. NPC Test
- [ ] Janitor NPC visible (red square)
- [ ] Janitor path changes based on Cloud pressure
- [ ] Janitor avoids player/constructs (if relevant)

### 5. Cloud Flock Test
- [ ] Particles visible (white semi-transparent dots)
- [ ] Particles move in flocking patterns
- [ ] Particles respond to pressure field

### 6. Level Switch Test
- [ ] Press F1 → Loads food court (40x40 grid)
- [ ] Press F2 → Loads service hall (different layout)
- [ ] Player position resets on switch

---

## CONCLUSION

**Current Status**: 90% initialized, blocked by 1 missing method
**Time to Fix**: ~30 minutes (implement bootstrap + create JSON files)
**Confidence**: High - all imports resolve, systems initialize, only missing game state injection

**Recommendation**:
1. Add `bootstrap()` stub to `state_manager.py` for immediate testing
2. Create minimal `game_state_foodcourt_v1.json` with empty arrays
3. Test player movement with arrow keys
4. Iterate on proper bootstrap implementation based on observed behavior

**Risk Assessment**: Low - graceful degradation prevents catastrophic failure, can test with defaults.
