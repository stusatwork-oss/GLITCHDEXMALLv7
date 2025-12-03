# Collapsed JSON Specification v1.0

**Contract:** No game logic exists outside these three data structures.

---

## The Three Files

### 1. `game_state_*.json` = World + Thresholds + Triggers

**Contains:**
- Level geometry (zones, dimensions, grid)
- Entity positions and initial state
- Cloud pressure thresholds (calm/agitated/destructive/release)
- Trigger definitions (if/then logic)
- Player spawn and configuration
- Environmental settings (audio, lighting)
- UI configuration

**Does NOT contain:**
- Color definitions (→ palette)
- NPC appearance (→ npc_profiles)
- Rendering logic (→ engine)

**Example:**
```json
{
  "cloud_pressure": {
    "phases": {
      "calm": { "range": [0, 30] },
      "agitated": { "range": [30, 60] }
    }
  },
  "triggers": [
    {
      "id": "JANITOR_THRESHOLD",
      "condition": "cloud >= 70",
      "on_trigger": [
        { "action": "move_npc", "npc": "JANITOR" }
      ]
    }
  ]
}
```

**Rule:** All game state logic goes here. Engine just executes it.

---

### 2. `npc_profiles_*.json` = Skins + Silhouettes

**Contains:**
- NPC visual appearance (body parts → palette references)
- Character color schemes
- Manifestation states (toddler opacity, etc.)
- Visual descriptions

**Does NOT contain:**
- Actual RGB colors (→ palette)
- Behavior logic (→ game_state triggers)
- Position/state (→ game_state entities)

**Example:**
```json
{
  "JANITOR_UNIT7": {
    "head": "ceiling_tile_grey",
    "jumpsuit": "wall_soft_green",
    "boots": "metal_dark",
    "tools": "warning_yellow_dark"
  }
}
```

**Rule:** Purely visual. Engine looks up these palette names and renders voxels.

---

### 3. `palette_*.json` = Era + Mood

**Contains:**
- Color definitions (id, name, hex)
- Single source of truth for all colors
- Era variants (brightness/saturation modifiers)
- Mood tints (Cloud state overlays)

**Does NOT contain:**
- Tile definitions (→ game_state or tileset)
- NPC assignments (→ npc_profiles)
- When to apply colors (→ game_state triggers)

**Example:**
```json
{
  "entries": [
    { "id": 2, "name": "wall_soft_green", "hex": "#AAC7BB" },
    { "id": 13, "name": "warning_yellow_dark", "hex": "#E49E2B" }
  ]
}
```

**Rule:** Colors defined once, referenced everywhere by name.

---

## Engine Contract

### What the Engine DOES:
- ✅ Load JSON files
- ✅ Parse data structures
- ✅ Update numbers (Cloud += 0.5)
- ✅ Check thresholds (if Cloud >= 70)
- ✅ Execute triggers (call actions)
- ✅ Render state (display voxels/sprites)
- ✅ Handle IO (keyboard, mouse, audio)

### What the Engine DOES NOT DO:
- ❌ Hardcode game logic
- ❌ Define colors in code
- ❌ Implement NPC AI behaviors
- ❌ Store entity positions
- ❌ Make design decisions

### The Rule:

**"If you need to change the engine to add a new level, you've failed."**

**Good:**
```bash
# Add new biome
cp game_state_foodcourt_v1.json game_state_atrium_v1.json
# Edit JSON with new triggers/entities
python engine.py --state game_state_atrium_v1.json
# Works with zero engine changes
```

**Bad:**
```python
# Adding new biome requires editing engine.py
if current_level == "atrium":
    special_atrium_logic()
```

---

## Permitted Engine Logic

### Threshold Checking (Good)
```python
if cloud >= threshold:
    execute_trigger()
```

**Why:** Generic. Works for any threshold in any JSON.

### Hardcoded Behavior (Bad)
```python
if npc.name == "JANITOR" and zone == "FC_ARCADE":
    janitor.speak("The arcade machines...")
```

**Why:** Specific to one entity. Should be in JSON trigger.

### Action Interpreter (Good)
```python
def execute_action(action):
    if action["type"] == "move_npc":
        npc = entities[action["npc"]]
        npc.position = action["target"]
```

**Why:** Generic action executor. Any JSON can use it.

### NPC-Specific Code (Bad)
```python
def update_janitor():
    if cloud > 70:
        janitor.walk_to_arcade()
```

**Why:** Should be a trigger in game_state JSON.

---

## Compliance Checklist

**Before committing code, verify:**

- [ ] All game logic is in `game_state_*.json`
- [ ] All colors are in `palette_*.json` (no hex codes in engine)
- [ ] All NPC appearances are in `npc_profiles_*.json`
- [ ] Engine only contains generic systems (load, update, check, render)
- [ ] New levels work with existing engine (no code changes)
- [ ] No entity-specific functions in engine code

**If any check fails, refactor to JSON.**

---

## Expansion Guidelines

### Adding a New Entity

**Wrong way (spaghetti):**
```python
# engine.py
class WifeNPC:
    def __init__(self):
        self.color = (180, 120, 140)  # Hardcoded
        self.behavior = "browsing"    # Hardcoded
        self.threshold = 75           # Hardcoded
```

**Right way (collapsed JSON):**

1. Add to `npc_profiles_v1.json`:
```json
"WIFE_AT_BOOKSTORE": {
  "head": "ceiling_tile_grey",
  "dress": "milo_optics_pink_dark",
  "shoes": "metal_dark"
}
```

2. Add to `game_state_*.json`:
```json
{
  "id": "WIFE",
  "type": "NPC",
  "profile": "WIFE_AT_BOOKSTORE",
  "position": [10, 15, 0],
  "threshold": 75
}
```

3. Add trigger:
```json
{
  "id": "WIFE_REACTS",
  "condition": "cloud >= 75 AND janitor.in_fc_arcade",
  "on_trigger": [
    { "action": "npc_stand", "npc": "WIFE" },
    { "action": "subtitle", "text": "She looks up from the book." }
  ]
}
```

**Engine changes needed:** Zero.

### Adding a New Level

**Wrong way:**
```python
# engine.py
levels = {
    "foodcourt": FoodCourtLevel(),
    "atrium": AtriumLevel()  # New class needed
}
```

**Right way:**
```bash
# Create new JSON
cp game_state_foodcourt_v1.json game_state_atrium_v1.json

# Edit entities, triggers, geometry
# Run with existing engine
python engine.py --state game_state_atrium_v1.json
```

**Engine changes needed:** Zero.

### Adding a New Trigger Action

**This is OK:**
```python
# engine.py
def execute_action(action):
    # ...existing actions...
    elif action["type"] == "screen_shake":  # New generic action
        duration = action["duration"]
        intensity = action["intensity"]
        start_screen_shake(duration, intensity)
```

**Why:** Generic action any JSON can use. Not level-specific.

**Then use in JSON:**
```json
{
  "action": "screen_shake",
  "duration": 0.5,
  "intensity": 0.3
}
```

---

## Validation

### Proof of Spec Compliance

**Test:** Can you run multiple levels with one engine?

```bash
python engine.py --state game_state_foodcourt_v1.json
python engine.py --state game_state_servicehall_v1.json
python engine.py --state game_state_atrium_v1.json
```

**If all three run without engine edits → Spec compliant.**

**If any requires engine changes → Spec violation.**

---

## Philosophy

**"The game compiles like perfectly collapsed JSON."**

**Meaning:**
- Game logic = data (JSON)
- Engine = interpreter
- No spaghetti (behavior trees, hardcoded entities)
- Everything observable (game state is the JSON)
- Moddable (edit JSON = mod game)
- Testable (load JSON, check outputs)

**This spec enforces that philosophy.**

---

## Version History

**v1.0 (2025-12-03)**
- Initial spec
- Three-file architecture defined
- Engine contract established
- Compliance checklist created

---

**Maintained by:** GLITCHDEX MALL V7 Development
**License:** This spec is canon. Violations will be refactored.
