# V7 INTEGRATED DEMO - The Horror Stack in Motion 🧸🧹💳

**The mall is screaming.**

This demo wires together the complete V7 horror stack:
- **Toddler** → Cloud amplification
- **Cloud** → Mood/pressure system
- **Janitor** → LLM dialogue (triggers at Cloud 70+)
- **Leon** → game_state awareness (ready for narration)
- **Renderer** → Glitch/strain tracking

---

## Quick Start

### Run with Mock LLM (No API key needed)

```bash
cd v7-nextgen/src
python3 v7_integrated_demo.py
```

### Run with Real LLM (Requires Anthropic API key)

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python3 v7_integrated_demo.py --with-llm
```

### Run Specific Scenarios

```bash
# Default: Normal Cloud progression until Janitor speaks
python3 v7_integrated_demo.py --scenario default

# Toddler Manifests: Accelerated Cloud, toddler becomes visible faster
python3 v7_integrated_demo.py --scenario toddler_manifests

# Critical Spiral: Rapid progression to critical mood
python3 v7_integrated_demo.py --scenario critical_spiral
```

---

## What It Does

### 1. Toddler → Cloud Amplification

Every tick:
```python
toddler_effects = toddler.update(
    dt=1.0,
    player_position=player.pos,
    current_cloud=cloud.level,
    player_looking_at_toddler=False
)

# Amplify Cloud pressure
base_delta = 0.5  # Passive gain
amplified_delta = base_delta * toddler_effects["heat_multiplier"]  # 1.0-3.0x
cloud.level += amplified_delta
```

**Result:** Cloud rises faster when toddler is near/visible.

### 2. Janitor → LLM Dialogue

Trigger: `cloud.level >= 70` AND `janitor.in_forbidden_zone == True`

When triggered:
```python
# Build prompt
system, user = build_janitor_prompt(
    janitor=janitor_state,
    cloud=cloud_state,
    zone=zone_state,
    metadata=mall_metadata,
    event={"type": "RULE_BROKEN", "zone": "FC-ARCADE"}
)

# Call LLM
response = llm.chat(system, user)

# Parse response
dialogue = parse_npc_response(response)
# {
#   "utterance": "The arcade machines... they're humming in E-flat...",
#   "emotional_state": "obsessed",
#   "tags": ["arcade", "escalators", "fountain"],
#   "action_hint": "touching cabinet, listening intently"
# }
```

**Result:** Janitor speaks with Cloud-aware tone, zone-specific topics, reality strain context.

### 3. Leon → game_state Output

Every tick, full game_state is built:
```python
game_state = {
    "game_time": 66.0,
    "tick_count": 65,
    "player": {"position": (0, 0, 0), "zone": "Z1_CENTRAL_ATRIUM"},
    "cloud": {"level": 70.8, "mood": "strained", "pressure_trend": "rising"},
    "toddler": {
        "visible": 1.0,
        "distance": 107.0,
        "reality_strain": 1.0,
        "in_distortion_field": False,
        "behavior": "wandering",
        "position": (100, 0, -8)
    },
    "janitor": {
        "zone": "FC-ARCADE",
        "in_forbidden_zone": True,
        "power": 1478,
        "threshold": 70.0
    },
    "renderer": {
        "glitch_intensity": 1.0,
        "reality_strain": 1.0,
        "camera_shake": 0.0
    }
}
```

**Ready for:** Leon to read and narrate ("Something's wrong in the food court...")

### 4. Renderer → Glitch/Strain Tracking

Every tick:
```python
renderer.glitch_intensity = (toddler_effects["glitch_multiplier"] - 1.0) / 3.0
renderer.reality_strain = toddler_effects["reality_strain"]

# Use for:
# - Chromatic aberration
# - Screen vignette
# - Sprite jitter
# - Color shifts
# - Camera shake
```

---

## Example Output (Default Scenario)

```
============================================================
  V7 INTEGRATED SIMULATION
  The Horror Stack: ONLINE
============================================================

[SIM] Systems initialized:
  - Cloud: 0.0 (calm)
  - Toddler: (100, 0, -8) (invisible)
  - Player: (0, 0, 0) (Atrium)
  - Janitor: (50, 0, 0) (Service Hall)
  - LLM: MOCK

[SCENARIO] Running: default

Tick   0 | Time 1.0s
  Cloud:   0.5 (     calm)
  Toddler: vis=0.01 dist=100.3ft behavior=wandering
  Janitor: SERVICE_HALL (rule: intact)
  Renderer: glitch=0.00 strain=0.00

Tick  10 | Time 11.0s
  Cloud:   8.1 (     calm)
  Toddler: vis=0.87 dist=101.2ft behavior=wandering
  Janitor: SERVICE_HALL (rule: intact)
  Renderer: glitch=0.61 strain=0.31

[... Cloud rises ...]

Tick  65 | Time 66.0s
  Cloud:  70.8 ( strained)
  Toddler: vis=1.00 dist=107.0ft behavior=wandering
  Janitor: FC-ARCADE (rule: BROKEN)
  Renderer: glitch=1.00 strain=1.00

  [!] Janitor BREAKS RULE: Enters FC-ARCADE (Cloud 70.8)

============================================================
  [LLM TRIGGER] Janitor breaks rule - generating dialogue
============================================================

[LLM] Sending prompt to model...
  System: 901 chars
  User: 468 chars

============================================================
  JANITOR (Cloud 70.8, strained)
============================================================

  "The arcade machines... they're humming in E-flat. Same as
   the escalators. Same as the fountain pump. It's all
   connected."

  [Emotional state: obsessed]
  [touching arcade cabinet, listening intently]
  Tags: arcade_machines, escalators, fountain, E-flat

============================================================

[DEMO] Complete. The mall spoke.
```

---

## What's Wired

### ✅ Complete

1. **Toddler System**
   - Updates every tick
   - Generates heat_multiplier (1.0-3.0x)
   - Generates glitch_multiplier (1.0-4.0x)
   - Generates reality_strain (0-1)
   - Auto-transitions between 5 behavioral modes

2. **Cloud Integration**
   - Receives toddler heat amplification
   - Updates mood (calm → uneasy → strained → critical)
   - Tracks pressure trend

3. **Janitor LLM Hook**
   - Detects rule break (Cloud ≥ 70, enters forbidden zone)
   - Builds Cloud-aware prompt
   - Calls LLM (mock or real Anthropic API)
   - Parses JSON response
   - Displays dialogue

4. **game_state Export**
   - Complete state for Leon
   - Includes toddler visibility/strain
   - Includes janitor contradiction status
   - Includes renderer glitch levels
   - Ready for narration

5. **Renderer Tracking**
   - Glitch intensity (0-1)
   - Reality strain (0-1)
   - Camera shake (distance-based)

### ⏳ To Wire (Optional)

- **Leon narration loop** - Call LLM with game_state every N ticks
- **QBIT zone disturbance** - Currently commented out, can be enabled
- **Player movement** - Currently stationary, could add input
- **Multiple NPCs** - Wife, Al-Gorithm LLM hooks
- **Zone geometry** - Real zone detection vs hardcoded

---

## The Stack (Fully Operational)

```
PLAYER (stationary)
  ↓
TODDLER (wandering, manifesting at Cloud 70+)
  ↓ heat_multiplier (1.0-3.0x)
  ↓
CLOUD (0 → 70.8 in 66 seconds)
  ↓ mood: calm → uneasy → strained
  ↓
JANITOR (breaks rule at Cloud 70)
  ↓ triggers LLM dialogue
  ↓
LLM (Anthropic Claude 3.5 Haiku)
  ↓ JSON response
  ↓
DIALOGUE ("The arcade machines hum E-flat...")
  ↓
game_state (toddler + cloud + janitor + renderer)
  ↓
LEON (ready to narrate)
  ↓
RENDERER (glitch 1.0, strain 1.0)
```

---

## Mock vs Real LLM

### Mock LLM (Default)
- No API key needed
- Returns canned responses based on context
- Good for testing integration
- Fast

### Real LLM (--with-llm flag)
- Requires `ANTHROPIC_API_KEY` environment variable
- Requires `anthropic` Python package: `pip install anthropic`
- Uses Claude 3.5 Haiku
- Returns actual context-aware dialogue
- ~$0.001 per utterance

---

## Next Steps

### Add Leon Narration Loop

```python
# In V7IntegratedSim.tick()

if self.tick_count % 20 == 0:  # Every 20 ticks
    leon_prompt = build_leon_prompt(game_state)
    leon_response = self.llm.chat(system=leon_prompt, user="What do I see?")
    print(f"\n[LEON] {leon_response}\n")
```

### Add Player Input

```python
# In main loop
while running:
    direction = get_player_input()  # WASD keys
    sim.player.update(dt, direction)
    game_state = sim.tick(dt)
```

### Add Multiple NPCs

```python
# Wire Wife and Al-Gorithm
if wife.in_event_zone and cloud.level >= wife.threshold:
    wife_dialogue = trigger_wife_llm(...)

if algoritmo.correlation_detected:
    algoritmo_dialogue = trigger_algoritmo_llm(...)
```

### Add Render Output

```python
# Use game_state renderer values for visual effects
if renderer.glitch_intensity > 0.5:
    apply_chromatic_aberration()

if renderer.reality_strain > 0.7:
    apply_vignette(intensity=renderer.reality_strain)
```

---

## Files

**Main Demo:**
- `src/v7_integrated_demo.py` - The horror stack in motion

**Dependencies:**
- `src/cloud.py` - Cloud system with QBIT
- `src/ai/toddler/toddler_system.py` - Toddler reality catalyst
- `src/ai/npc_llm/janitor_llm.py` - Janitor LLM dialogue

---

## The Moment

**Before:** Design docs, specs, separate systems

**After:** Integrated loop where:
- Toddler amplifies Cloud
- Cloud triggers Janitor
- Janitor speaks via LLM
- game_state ready for Leon
- Renderer tracks strain

**The infrastructure is no longer theoretical. It's code. It's running. It's screaming.**

---

*The mall spoke. It said "The arcade machines hum in E-flat."*

*And it was right. They do.*
