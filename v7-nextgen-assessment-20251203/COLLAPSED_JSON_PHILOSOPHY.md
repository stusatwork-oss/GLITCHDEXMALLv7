# Collapsed JSON Philosophy - V7 Design Document

**Core Principle:** The game should compile like perfectly collapsed JSON - minimal, elegant, self-describing.

---

## The Philosophy

### What "Collapsed JSON" Means

**JSON is:**
- Structured
- Minimal (no redundancy)
- Self-describing (keys tell you what values mean)
- Parseable (unambiguous)
- Composable (objects nest cleanly)

**Your game should be:**
- Systems that are simple data structures
- No spaghetti behavior trees - just thresholds and states
- Everything observable from the data
- No hidden complexity
- Emergent gameplay from simple interactions

**Example:**

```json
{
  "cloud": 0,
  "janitor": {
    "position": [50, 0, 0],
    "zone": "SERVICE_HALL",
    "rule": "never_crosses_fc_arcade",
    "threshold": 70
  },
  "if": "cloud >= janitor.threshold",
  "then": "janitor breaks rule"
}
```

That's it. No behavior tree with 50 states. Just: number, threshold, consequence.

---

## V7 Systems as Collapsed JSON

### 1. Cloud System

```json
{
  "cloud": {
    "level": 0,
    "max": 100,
    "phases": {
      "0-30": "calm",
      "30-60": "agitated",
      "60-85": "destructive",
      "85+": "release"
    },
    "cycle": "automatic_at_85"
  }
}
```

**That's the entire system.** One number, four thresholds, one cycle rule.

### 2. NPC Spines

```json
{
  "janitor": {
    "never": ["cross_fc_arcade", "speak_about_wife"],
    "always": ["face_away_from_bookstore"],
    "qbit": {"power": 1478, "charisma": 1308},
    "threshold": 70
  }
}
```

**No pathfinding, no schedules, no complex AI.** Just: constraints and a threshold.

### 3. Credit Card Mechanic

```json
{
  "cards": {
    "VISA": {"cost": 50, "ability": "slow_time"},
    "MASTERCARD": {"cost": 100, "ability": "damage"},
    "AMEX": {"cost": 200, "ability": "shield"}
  },
  "mechanic": "card.cost → cloud.increase",
  "toddler_reaction": "multiplier × 2.0"
}
```

**Diegetic and data-driven.** Use card → number goes up → consequence.

### 4. Era System

```json
{
  "eras": {
    "1981": {"brightness": 1.15, "saturation": 1.1},
    "1995": {"brightness": 1.0, "saturation": 1.0},
    "2005": {"brightness": 0.85, "saturation": 0.8},
    "2011": {"brightness": 0.6, "saturation": 0.5}
  },
  "active_era": "1995",
  "flicker_at": "cloud > 60"
}
```

**Simple modifiers, one active state, one trigger.**

### 5. Contradiction System

```json
{
  "contradiction": {
    "trigger": "cloud >= npc.threshold AND npc breaks rule",
    "effect": {
      "visual": "era_flicker",
      "audio": "escalator_hum_warble",
      "dialogue": "npc_llm_generate"
    },
    "resolution": "cloud_release"
  }
}
```

**If/then logic. No scripts, just: condition → effects.**

---

## Anti-Patterns (What to Avoid)

### ❌ Behavior Tree Spaghetti

```python
# BAD: Complex state machine
class JanitorAI:
    def update(self):
        if self.state == "idle":
            if player.distance < 10 and time > 5pm and has_seen_player:
                if inventory.has("mop") and not is_raining:
                    self.transition_to("patrol_nervous")
                elif random.random() < 0.3:
                    self.transition_to("idle_fidget")
                # ... 47 more conditions
```

### ✅ Collapsed JSON Approach

```python
# GOOD: Simple threshold
class Janitor:
    def update(self, cloud):
        if cloud >= self.threshold and not self.rule_broken:
            self.move_to_forbidden_zone()
            self.rule_broken = True
```

---

### ❌ Hidden State

```python
# BAD: Player can't observe
self.secret_anger_meter += 5
self.hidden_quest_progress = 73
self.invisible_cooldown_timer = 12.5
```

### ✅ Observable State

```python
# GOOD: Everything visible in world
cloud.level = 73  # Visible via lighting/flicker
janitor.in_forbidden_zone = True  # Visible position
toddler.manifestation = 0.8  # Visible opacity
```

---

### ❌ Bloated Systems

```python
# BAD: Over-engineered
class NPCScheduleSystem:
    def __init__(self):
        self.hourly_schedules = {}
        self.location_preferences = {}
        self.mood_modifiers = {}
        self.social_network_graph = {}
        # ... 500 lines of complexity
```

### ✅ Minimal Systems

```python
# GOOD: Threshold-based
class NPC:
    def update(self, cloud):
        if cloud >= self.threshold:
            self.contradict()  # That's it
```

---

## The Food Court Vertical Slice as Collapsed JSON

### Game State (Complete)

```json
{
  "player": {
    "position": [0, 0, -8],
    "zone": "FOOD_COURT_PIT",
    "cards": {
      "VISA": {"equipped": true, "durability": 100},
      "MASTERCARD": {"equipped": false, "durability": 100},
      "AMEX": {"equipped": false, "durability": 100}
    }
  },

  "cloud": {
    "level": 0,
    "phase": "calm",
    "cycle_count": 0
  },

  "toddler": {
    "position": [100, 0, -8],
    "manifestation": 0.0,
    "distance_to_player": 100
  },

  "janitor": {
    "position": [50, 0, 0],
    "zone": "SERVICE_HALL",
    "rule_broken": false,
    "threshold": 70
  },

  "environment": {
    "era": "1995",
    "lighting": {
      "flicker": 0.0,
      "brightness": 1.0
    },
    "textures": {
      "frames": 40,
      "current_sector": 0
    }
  }
}
```

**That's the entire game state.** 50 lines of JSON. Everything else is just:
- Rendering this state
- Updating numbers based on rules
- Checking thresholds

### Game Loop (Collapsed)

```python
def game_loop():
    """Entire game logic in one function"""

    while running:
        # UPDATE
        dt = clock.tick(60) / 1000.0

        # Player input
        if keys[SPACE]:
            cloud.increase(player.active_card.cost * toddler.get_multiplier())

        # Cloud rises passively
        cloud.level += 0.5 * dt * toddler.get_heat_multiplier()

        # Check thresholds
        if cloud.level >= 85:
            cloud.release()  # Drop to 0

        if cloud.level >= janitor.threshold and not janitor.rule_broken:
            janitor.move_to_forbidden_zone()
            janitor.rule_broken = True
            display_subtitle("The arcade machines hum in E-flat...")

        # Toddler manifests based on card usage
        toddler.update_manifestation(cards_used_count)

        # RENDER
        render_world(cloud.phase, environment.era, player.position)

        # That's it. No behavior trees. Just: update numbers, check thresholds, render.
```

**~50 lines for the entire game loop.** The rest is just helpers.

---

## Implementation as Data Files

### The Vision

**Instead of code defining behavior, JSON files define everything:**

```
/v7-nextgen/data/
├── npcs.json           # All NPC definitions
├── zones.json          # Zone geometry and rules
├── cards.json          # Credit card properties
├── dialogue.json       # NPC dialogue trees
├── eras.json           # Era visual modifiers
└── game_config.json    # Global settings
```

**The engine just:**
1. Loads JSON
2. Updates numbers
3. Checks thresholds
4. Renders state

**No hardcoded behavior.** Everything data-driven.

### Example: npcs.json

```json
{
  "janitor": {
    "id": "the-janitor",
    "name": "The Janitor",
    "spawn": {"zone": "SERVICE_HALL", "position": [50, 0, 0]},
    "spine": {
      "never": ["cross_fc_arcade", "speak_about_wife"],
      "always": ["face_away_from_bookstore"]
    },
    "qbit": {"power": 1478, "charisma": 1308},
    "threshold": 70,
    "dialogue": {
      "contradiction": "The arcade machines... they're humming in E-flat."
    },
    "visual": {
      "palette": "JANITOR_UNIT7",
      "jumpsuit": "wall_soft_green",
      "tools": "warning_yellow_dark"
    }
  }
}
```

**Load this file → NPC exists.** No class definitions, no scripts, just data.

---

## Why This Matters

### Benefits of Collapsed JSON Design

**1. Readable**
- Anyone can understand the game by reading JSON files
- No hidden complexity in code
- Game state is transparent

**2. Debuggable**
- Print `game_state` → see everything
- No "why is this NPC doing that?" mysteries
- State is observable

**3. Moddable**
- Change JSON → change game
- No recompilation needed
- Community can tweak values

**4. Testable**
- Set `cloud.level = 70` → verify janitor moves
- Deterministic (same input = same output)
- No complex mocking needed

**5. Maintainable**
- Small functions (check threshold, update number)
- No spaghetti
- Easy to understand months later

**6. Immersive**
- No hidden state = no HUD needed
- Everything observable in world
- Player sees the data structure executing

---

## Development Workflow

### How to Build This

**Phase 1: Define the Data**
```bash
# Create JSON files first
touch data/npcs.json
touch data/zones.json
touch data/cards.json

# Define the structure (collapsed JSON)
# This IS the design document
```

**Phase 2: Load the Data**
```python
# Simple loader
game_state = json.load(open("data/game_config.json"))
npcs = json.load(open("data/npcs.json"))
zones = json.load(open("data/zones.json"))
```

**Phase 3: Update Logic**
```python
# Minimal engine
def update(dt, game_state):
    # Just check thresholds
    for npc in npcs:
        if game_state["cloud"] >= npc["threshold"]:
            npc["rule_broken"] = True

    return game_state
```

**Phase 4: Render State**
```python
# Render what exists in game_state
def render(game_state):
    render_textures(game_state["environment"]["era"])
    render_npcs(npcs)
    render_cloud_effects(game_state["cloud"]["phase"])
```

**That's it.** Load JSON → Update numbers → Render state.

---

## The Food Court Vertical Slice as Perfect JSON

### File Structure

```
/v7-nextgen/
├── data/
│   ├── food_court_slice.json     # Entire demo config
│   ├── janitor.json               # Janitor definition
│   ├── toddler.json               # Toddler definition
│   └── cards.json                 # Credit card properties
├── assets/
│   └── frames/foodcourt-2010/    # 40 photo frames
└── src/
    ├── engine.py                  # Load JSON, update, render
    ├── renderer.py                # Pygame raycaster
    └── main.py                    # Entry point
```

### food_court_slice.json

```json
{
  "title": "Food Court Reactor Pit - Vertical Slice",
  "version": "0.1.0",

  "player": {
    "spawn": {"zone": "FOOD_COURT_PIT", "position": [0, 0, -8]},
    "speed": 10.0,
    "cards": ["VISA", "MASTERCARD", "AMEX"]
  },

  "cloud": {
    "start_level": 0,
    "passive_rate": 0.5,
    "phases": [
      {"range": [0, 30], "name": "calm"},
      {"range": [30, 60], "name": "agitated"},
      {"range": [60, 85], "name": "destructive"},
      {"range": [85, 100], "name": "release"}
    ],
    "cycle": {"release_at": 85, "drop_to": 0, "duration": 1.5}
  },

  "entities": [
    {"type": "npc", "id": "janitor", "file": "data/janitor.json"},
    {"type": "npc", "id": "toddler", "file": "data/toddler.json"}
  ],

  "environment": {
    "zone": "FOOD_COURT_PIT",
    "geometry": {
      "diameter": 120,
      "depth": 8,
      "shape": "circular_pit"
    },
    "textures": {
      "source": "assets/frames/foodcourt-2010/",
      "count": 40,
      "mapping": "radial"
    },
    "audio": {
      "escalator_hum": {"frequency": 311, "note": "E-flat"}
    }
  },

  "demo": {
    "duration": 180,
    "loop": true,
    "objectives": [
      "Explore pit",
      "Use credit cards",
      "Trigger janitor contradiction",
      "Observe cloud cycle"
    ]
  }
}
```

**That's the entire demo specification.** ~60 lines. Everything else derives from this.

---

## The Engine (Minimal)

```python
#!/usr/bin/env python3
"""
V7 Food Court Vertical Slice - Collapsed JSON Engine
Loads game state from JSON, updates numbers, renders state.
"""

import json
import pygame
from pathlib import Path

def load_game_config(path="data/food_court_slice.json"):
    """Load entire game from one JSON file"""
    return json.load(open(path))

def update_game_state(state, dt):
    """Update all game state (threshold checks only)"""

    # Cloud rises passively
    cloud = state["cloud"]
    cloud["level"] += cloud["passive_rate"] * dt

    # Check cloud thresholds → update phase
    for phase_def in cloud["phases"]:
        if phase_def["range"][0] <= cloud["level"] < phase_def["range"][1]:
            cloud["phase"] = phase_def["name"]
            break

    # Release cycle
    if cloud["level"] >= cloud["cycle"]["release_at"]:
        trigger_release(state)

    # Check NPC thresholds
    for entity in state["entities"]:
        if entity["type"] == "npc":
            check_npc_threshold(entity, cloud)

    return state

def check_npc_threshold(npc, cloud):
    """Simple threshold check - no complex AI"""
    if cloud["level"] >= npc.get("threshold", 100):
        if not npc.get("rule_broken", False):
            npc["rule_broken"] = True
            print(f"{npc['id']} breaks rule at Cloud {cloud['level']}")

def trigger_release(state):
    """Cloud pressure release"""
    state["cloud"]["level"] = state["cloud"]["cycle"]["drop_to"]
    state["cloud"]["cycle_count"] = state["cloud"].get("cycle_count", 0) + 1

    # Reset NPCs
    for entity in state["entities"]:
        if entity["type"] == "npc":
            entity["rule_broken"] = False

def render_game_state(state, screen):
    """Render current game state"""
    # Load textures based on state
    # Render based on cloud phase
    # Display NPCs at positions
    # No HUD
    pass

def main():
    """Collapsed JSON game loop"""

    # Load everything from JSON
    game_state = load_game_config()

    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Main loop
    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update (just numbers and thresholds)
        game_state = update_game_state(game_state, dt)

        # Render (visualize the JSON)
        render_game_state(game_state, screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
```

**~80 lines for entire engine.** The game IS the JSON file. The code just executes it.

---

## Summary: Perfectly Collapsed JSON

**Your game design:**
- Simple systems (Cloud, Spines, QBIT, Thresholds)
- No behavior tree spaghetti
- Everything observable (Hudless)
- Diegetic mechanics (Credit cards)
- Data-driven (JSON defines everything)
- Emergent gameplay (Simple rules → Complex interactions)

**The vertical slice proves:**
- 40 photo textures as data
- Cloud cycle as simple state machine
- NPCs as threshold triggers
- Contradictions as if/then logic
- No hidden complexity
- Game state fits in 50 lines of JSON

**Philosophy:**
> "I want my game to compile like perfectly collapsed JSON"

**Meaning:**
- Clean
- Minimal
- Self-describing
- No redundancy
- Elegant

**This is how you build it.**

---

**Next step:** Create `data/food_court_slice.json` and start the engine. The game will emerge from the data structure.
