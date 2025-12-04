# V6 Bridge Implementation Specification
**Python Simulation ↔ UE5 Integration Layer**

**Generated:** 2025-11-26
**Status:** Reference Implementation
**Purpose:** Concrete code examples for bridge layer

---

## Overview

This document provides **copy-paste ready** code for the bridge layer between Python simulation and UE5.

**Architecture:**
```
UE5 (C++) → HTTP/JSON → Python Bridge → Existing Sim Systems
```

---

## 1. Core Bridge API

### File: `v6-nextgen/src/sim_bridge.py`

```python
#!/usr/bin/env python3
"""
MALL SIMULATION BRIDGE - V6 NextGen
Core API for UE5 integration.

This module provides the stable interface between UE5 and the Python simulation.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import time


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class MallMood(Enum):
    """Global mall mood states."""
    CALM = "calm"
    UNEASY = "uneasy"
    STRAINED = "strained"
    CRITICAL = "critical"


class NPCStateEnum(Enum):
    """NPC behavioral states."""
    NORMAL = "normal"
    STRESSED = "stressed"
    AVOIDING = "avoiding"
    CONTRADICTED = "contradicted"


@dataclass
class CloudState:
    """Current cloud/mood state."""
    level: float          # 0-100
    mood: str             # CALM, UNEASY, STRAINED, CRITICAL
    trend: str            # STABLE, RISING, FALLING, SPIKING
    pressure_rate: float  # Change per second


@dataclass
class NPCUpdate:
    """NPC state for a single tick."""
    id: str
    name: str
    state: str                    # NORMAL, STRESSED, etc.
    zone: str
    hint: str                     # Animation/behavior hint for UE5
    dialogue: Optional[str]       # Current dialogue line (if any)
    stress_level: float           # 0.0-1.0
    should_trigger_contradiction: bool
    position_hint: Optional[Dict[str, float]] = None  # {"x": 0, "y": 0, "z": 0}


@dataclass
class ZoneUpdate:
    """Zone microstate for a single tick."""
    zone_id: str
    turbulence: float      # 0-10
    resonance: float       # 0-10
    swarm_count: int       # Number of ambient NPCs
    is_active: bool        # Player or important NPC present


@dataclass
class GameEvent:
    """Discrete event that occurred this tick."""
    type: str              # "contradiction", "discovery", "npc_alert", etc.
    timestamp: float
    details: Dict[str, Any]


@dataclass
class FrameUpdate:
    """
    Complete simulation state for one frame.
    This is what gets sent back to UE5.
    """
    timestamp: float
    cloud: CloudState
    npcs: List[NPCUpdate]
    zones: Dict[str, ZoneUpdate]
    events: List[GameEvent]

    def to_dict(self) -> Dict:
        """Convert to JSON-serializable dict."""
        return {
            "timestamp": self.timestamp,
            "cloud": asdict(self.cloud),
            "npcs": [asdict(npc) for npc in self.npcs],
            "zones": {k: asdict(v) for k, v in self.zones.items()},
            "events": [asdict(e) for e in self.events]
        }


@dataclass
class PlayerEvent:
    """Player action sent from UE5."""
    type: str              # "move", "interact", "discover", "wait"
    timestamp: float
    data: Dict[str, Any]   # Event-specific payload


@dataclass
class WorldState:
    """
    Persistent world state.
    This is the simulation's memory.
    """
    world_id: str
    created_at: float
    last_tick: float
    tick_count: int

    # Simulation state (imported from v4 systems)
    cloud: Any             # Cloud instance from v4-renderist/src/cloud.py
    npcs: Dict[str, Any]   # NPC instances
    zones: Dict[str, Any]  # Zone states

    # Configuration
    config: Dict[str, Any]


# ============================================================================
# CORE API FUNCTIONS
# ============================================================================

def init_world(config_path: str) -> WorldState:
    """
    Initialize simulation from config file.

    Args:
        config_path: Path to JSON config file containing:
            - NPC definitions
            - Zone topology
            - Initial cloud state
            - Game rules

    Returns:
        WorldState ready for ticking

    Example:
        >>> world = init_world("data/config/mall_v6_minimal.json")
        >>> print(world.world_id)
        "mall_abc123"
    """
    import uuid
    from pathlib import Path

    # Load config
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    with open(config_file, 'r') as f:
        config = json.load(f)

    # Create world ID
    world_id = f"mall_{uuid.uuid4().hex[:8]}"

    # Import existing systems
    # TODO: Adjust imports based on final structure
    # from v4_renderist.src.cloud import Cloud
    # from v4_renderist.src.anchor_npcs import AnchorNPCSystem

    # For now, create stubs
    cloud = _create_cloud_from_config(config)
    npcs = _create_npcs_from_config(config)
    zones = _create_zones_from_config(config)

    world = WorldState(
        world_id=world_id,
        created_at=time.time(),
        last_tick=time.time(),
        tick_count=0,
        cloud=cloud,
        npcs=npcs,
        zones=zones,
        config=config
    )

    return world


def tick_world(
    world: WorldState,
    dt: float,
    player_event: Optional[Dict] = None
) -> FrameUpdate:
    """
    Advance simulation by one tick.

    Args:
        world: Current world state
        dt: Delta time in seconds (typically 0.25)
        player_event: Optional player action
            Examples:
            {"type": "move", "to_zone": "FC-ARCADE", "from_zone": "FC-CORE"}
            {"type": "interact", "target": "bag_of_screams"}
            {"type": "discover", "document": "log_017"}
            {"type": "wait"}

    Returns:
        FrameUpdate with current state for UE5 to render

    Example:
        >>> update = tick_world(world, 0.25, {"type": "move", "to_zone": "FC-ARCADE"})
        >>> print(update.cloud.mood)
        "UNEASY"
    """
    current_time = time.time()
    world.tick_count += 1
    world.last_tick = current_time

    # Parse player event
    event = None
    if player_event:
        event = PlayerEvent(
            type=player_event.get("type", "wait"),
            timestamp=current_time,
            data=player_event
        )

    # Update cloud state
    cloud_state = _tick_cloud(world, dt, event)

    # Update NPCs
    npc_updates = _tick_npcs(world, dt, event, cloud_state)

    # Update zones
    zone_updates = _tick_zones(world, dt, event)

    # Collect events that occurred
    game_events = _collect_events(world, cloud_state, npc_updates)

    # Build frame update
    frame = FrameUpdate(
        timestamp=current_time,
        cloud=cloud_state,
        npcs=npc_updates,
        zones=zone_updates,
        events=game_events
    )

    return frame


# ============================================================================
# INTERNAL TICK FUNCTIONS
# ============================================================================

def _tick_cloud(
    world: WorldState,
    dt: float,
    player_event: Optional[PlayerEvent]
) -> CloudState:
    """
    Update cloud state based on events.

    This wraps the existing v4 Cloud system.
    """
    # TODO: Call actual Cloud.tick() from v4-renderist/src/cloud.py
    # For now, stub implementation

    cloud = world.cloud
    level = cloud.get("level", 50.0)

    # Apply player event influence
    if player_event:
        if player_event.type == "discover":
            level += 5.0  # Discoveries raise cloud
        elif player_event.type == "move":
            level += 0.5  # Movement creates subtle tension

    # Natural drift
    level += dt * 0.1  # Slow rise over time

    # Clamp
    level = max(0.0, min(100.0, level))

    # Determine mood
    if level < 25:
        mood = "CALM"
    elif level < 50:
        mood = "UNEASY"
    elif level < 75:
        mood = "STRAINED"
    else:
        mood = "CRITICAL"

    # Update world state
    cloud["level"] = level
    cloud["mood"] = mood

    return CloudState(
        level=level,
        mood=mood,
        trend="RISING" if level > cloud.get("prev_level", 50) else "STABLE",
        pressure_rate=0.1
    )


def _tick_npcs(
    world: WorldState,
    dt: float,
    player_event: Optional[PlayerEvent],
    cloud_state: CloudState
) -> List[NPCUpdate]:
    """
    Update all NPC states.

    This wraps existing v2/v4 NPC systems.
    """
    updates = []

    for npc_id, npc_data in world.npcs.items():
        # Determine stress based on cloud
        stress = cloud_state.level / 100.0

        # Determine state
        if stress < 0.5:
            state = "NORMAL"
        elif stress < 0.75:
            state = "STRESSED"
        else:
            state = "CONTRADICTED"

        # Pick dialogue
        dialogue = None
        if state == "NORMAL" and npc_data.get("dialogue_normal"):
            dialogue = npc_data["dialogue_normal"][0]
        elif state == "STRESSED" and npc_data.get("dialogue_stressed"):
            dialogue = npc_data["dialogue_stressed"][0]

        # Pick animation hint
        hint = npc_data.get("hints", {}).get(state, "idle")

        # Should trigger contradiction?
        should_contradict = (
            cloud_state.level >= npc_data.get("contradiction_trigger", 80.0)
            and not npc_data.get("contradiction_used", False)
        )

        update = NPCUpdate(
            id=npc_id,
            name=npc_data.get("name", npc_id),
            state=state,
            zone=npc_data.get("zone", "UNKNOWN"),
            hint=hint,
            dialogue=dialogue,
            stress_level=stress,
            should_trigger_contradiction=should_contradict
        )

        updates.append(update)

    return updates


def _tick_zones(
    world: WorldState,
    dt: float,
    player_event: Optional[PlayerEvent]
) -> Dict[str, ZoneUpdate]:
    """
    Update zone microstates.
    """
    updates = {}

    for zone_id, zone_data in world.zones.items():
        turbulence = zone_data.get("turbulence", 0.0)

        # Increase turbulence if player just entered
        if player_event and player_event.type == "move":
            if player_event.data.get("to_zone") == zone_id:
                turbulence += 1.0

        # Decay turbulence over time
        turbulence = max(0.0, turbulence - dt * 0.5)

        zone_data["turbulence"] = turbulence

        updates[zone_id] = ZoneUpdate(
            zone_id=zone_id,
            turbulence=turbulence,
            resonance=zone_data.get("resonance", 0.0),
            swarm_count=zone_data.get("swarm_count", 3),
            is_active=turbulence > 0.1
        )

    return updates


def _collect_events(
    world: WorldState,
    cloud_state: CloudState,
    npc_updates: List[NPCUpdate]
) -> List[GameEvent]:
    """
    Collect discrete events that occurred this tick.
    """
    events = []

    # Check for NPC contradictions
    for npc in npc_updates:
        if npc.should_trigger_contradiction:
            events.append(GameEvent(
                type="contradiction_triggered",
                timestamp=time.time(),
                details={
                    "npc_id": npc.id,
                    "npc_name": npc.name,
                    "cloud_level": cloud_state.level
                }
            ))

    # Check for cloud mood changes
    prev_mood = world.cloud.get("prev_mood")
    if prev_mood and prev_mood != cloud_state.mood:
        events.append(GameEvent(
            type="cloud_mood_changed",
            timestamp=time.time(),
            details={
                "from": prev_mood,
                "to": cloud_state.mood,
                "level": cloud_state.level
            }
        ))

    world.cloud["prev_mood"] = cloud_state.mood

    return events


# ============================================================================
# HELPER FUNCTIONS (Config Loading)
# ============================================================================

def _create_cloud_from_config(config: Dict) -> Dict:
    """Initialize cloud state from config."""
    cloud_config = config.get("cloud", {})
    return {
        "level": cloud_config.get("initial_level", 50.0),
        "mood": "UNEASY",
        "prev_level": 50.0,
        "prev_mood": "UNEASY"
    }


def _create_npcs_from_config(config: Dict) -> Dict[str, Any]:
    """Load NPCs from config."""
    npcs = {}
    for npc_def in config.get("npcs", []):
        npc_id = npc_def["id"]
        npcs[npc_id] = {
            "id": npc_id,
            "name": npc_def.get("name", npc_id),
            "zone": npc_def.get("home_zone", "UNKNOWN"),
            "contradiction_trigger": npc_def.get("spine", {}).get("contradiction_trigger", 80.0),
            "contradiction_used": False,
            "dialogue_normal": npc_def.get("dialogue", {}).get("normal", []),
            "dialogue_stressed": npc_def.get("dialogue", {}).get("stressed", []),
            "hints": {
                "NORMAL": npc_def.get("hints", {}).get("normal", "idle"),
                "STRESSED": npc_def.get("hints", {}).get("stressed", "fidget"),
                "CONTRADICTED": npc_def.get("hints", {}).get("contradicted", "glitch")
            }
        }
    return npcs


def _create_zones_from_config(config: Dict) -> Dict[str, Any]:
    """Load zones from config."""
    zones = {}
    for zone_def in config.get("zones", []):
        zone_id = zone_def["id"]
        zones[zone_id] = {
            "id": zone_id,
            "name": zone_def.get("name", zone_id),
            "turbulence": zone_def.get("initial_turbulence", 0.0),
            "resonance": 0.0,
            "swarm_count": 3
        }
    return zones


# ============================================================================
# SERIALIZATION HELPERS
# ============================================================================

def serialize_frame(frame: FrameUpdate) -> str:
    """Convert FrameUpdate to JSON string."""
    return json.dumps(frame.to_dict(), indent=2)


def deserialize_player_event(json_str: str) -> Dict:
    """Parse player event from JSON string."""
    return json.loads(json_str)
```

---

## 2. HTTP Server Wrapper

### File: `v6-nextgen/src/sim_server.py`

```python
#!/usr/bin/env python3
"""
MALL SIMULATION HTTP SERVER - V6 NextGen
Flask-based REST API for UE5 integration.

Endpoints:
- POST /init - Initialize world
- POST /tick - Advance simulation
- GET /status - Health check
- POST /shutdown - Graceful shutdown
"""

from flask import Flask, request, jsonify
from sim_bridge import init_world, tick_world, WorldState, serialize_frame
from typing import Dict, Optional
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Global world state (in production, use session management)
WORLDS: Dict[str, WorldState] = {}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "mall-sim-v6"})


@app.route('/init', methods=['POST'])
def initialize_world():
    """
    Initialize a new world.

    Request:
    {
        "config_path": "data/config/mall_v6_minimal.json"
    }

    Response:
    {
        "world_id": "mall_abc123",
        "status": "initialized",
        "config": {...}
    }
    """
    try:
        data = request.get_json()
        config_path = data.get("config_path")

        if not config_path:
            return jsonify({"error": "config_path required"}), 400

        # Initialize world
        world = init_world(config_path)
        WORLDS[world.world_id] = world

        logging.info(f"Initialized world: {world.world_id}")

        return jsonify({
            "world_id": world.world_id,
            "status": "initialized",
            "config": world.config
        })

    except Exception as e:
        logging.error(f"Init error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/tick', methods=['POST'])
def tick():
    """
    Advance simulation by one tick.

    Request:
    {
        "world_id": "mall_abc123",
        "dt": 0.25,
        "player_event": {
            "type": "move",
            "to_zone": "FC-ARCADE"
        }
    }

    Response:
    {
        "timestamp": 1234.56,
        "cloud": {...},
        "npcs": [...],
        "zones": {...},
        "events": [...]
    }
    """
    try:
        data = request.get_json()
        world_id = data.get("world_id")
        dt = data.get("dt", 0.25)
        player_event = data.get("player_event")

        if not world_id:
            return jsonify({"error": "world_id required"}), 400

        if world_id not in WORLDS:
            return jsonify({"error": f"world {world_id} not found"}), 404

        # Tick simulation
        world = WORLDS[world_id]
        frame = tick_world(world, dt, player_event)

        return jsonify(frame.to_dict())

    except Exception as e:
        logging.error(f"Tick error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Graceful shutdown."""
    logging.info("Shutdown requested")
    # TODO: Save world states
    return jsonify({"status": "shutting down"})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
```

**Run server:**
```bash
cd v6-nextgen
python src/sim_server.py
```

**Test with curl:**
```bash
# Health check
curl http://localhost:5000/health

# Initialize
curl -X POST http://localhost:5000/init \
  -H "Content-Type: application/json" \
  -d '{"config_path": "data/config/mall_v6_minimal.json"}'

# Tick
curl -X POST http://localhost:5000/tick \
  -H "Content-Type: application/json" \
  -d '{
    "world_id": "mall_abc123",
    "dt": 0.25,
    "player_event": {"type": "move", "to_zone": "FC-ARCADE"}
  }'
```

---

## 3. Example Config File

### File: `v6-nextgen/data/config/mall_v6_minimal.json`

```json
{
  "version": "6.0-minimal",
  "metadata": {
    "name": "Mall V6 Minimal Test Pack",
    "description": "4 NPCs, 4 zones, 1 contradiction scenario",
    "created": "2025-11-26"
  },

  "cloud": {
    "initial_level": 45.0,
    "drift_rate": 0.1,
    "discovery_impact": 5.0
  },

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
      },
      "hints": {
        "normal": "patrol_route",
        "stressed": "pace_near_player",
        "contradicted": "freeze_loop"
      }
    },

    {
      "id": "uncle_danny",
      "name": "Uncle Danny",
      "role": "Grilled Cheese Priest",
      "home_zone": "FC-CORE",
      "visual": {
        "uniform": "White apron, food service",
        "iconic_detail": "Frying pan, always",
        "silhouette": "Wide, warm, solid",
        "text_anchor": "grilled cheese uncle"
      },
      "spine": {
        "domain_lock": "All food resolves to grilled cheese",
        "never_list": [
          "NEVER cook without grilled cheese involved",
          "NEVER disrespect bread or cheese",
          "NEVER act with malice"
        ],
        "rituals": [
          "Tilt pan while explaining",
          "Hold sandwich up like a verdict",
          "Taste, nod, give life advice"
        ],
        "props": ["frying_pan", "spatula", "cheese_slices"],
        "contradiction_trigger": 90.0,
        "contradiction_action": "Infinite grilled cheese loop"
      },
      "dialogue": {
        "normal": [
          "Grilled cheese fixes everything, kid.",
          "You want extra butter? Always extra butter.",
          "See this golden crust? That's patience."
        ],
        "stressed": [
          "Even grilled cheese can't fix some things.",
          "I don't know. Maybe... maybe more cheese?",
          "This batch isn't coming out right."
        ],
        "contradiction": [
          "It's all grilled cheese. Always has been.",
          "[Flips the same sandwich eternally]"
        ]
      },
      "hints": {
        "normal": "cooking_idle",
        "stressed": "fidget_with_pan",
        "contradicted": "cooking_loop"
      }
    },

    {
      "id": "security_wolf",
      "name": "Wolf Sergeant",
      "role": "Security Patrol Lead",
      "home_zone": "MAIN_HALL",
      "visual": {
        "uniform": "Black security uniform, tailored",
        "iconic_detail": "Radio, always on belt",
        "silhouette": "Upright, disciplined",
        "text_anchor": "security wolf radio"
      },
      "spine": {
        "domain_lock": "Order through presence and posture",
        "never_list": [
          "NEVER carry weapons",
          "NEVER break formation casually",
          "NEVER enter Maintenance sublevels"
        ],
        "rituals": [
          "Patrol loop every 2 minutes",
          "Radio check-in every 5 minutes",
          "Posture correction when Cloud rises"
        ],
        "props": ["radio", "keys", "clipboard_optional"],
        "contradiction_trigger": 80.0,
        "contradiction_action": "Patrol loop becomes infinite"
      },
      "dialogue": {
        "normal": [
          "All clear, sector three.",
          "Radio check. Copy.",
          "Keep moving, please."
        ],
        "stressed": [
          "Something's... off. Can't place it.",
          "Did you see that? No. Never mind.",
          "I should be at checkpoint C. I think."
        ],
        "contradiction": [
          "I've been here before. Loop A-7.",
          "[Radio static: 'All clear, sector three. All clear...']"
        ]
      },
      "hints": {
        "normal": "patrol_route",
        "stressed": "scan_area",
        "contradicted": "patrol_loop_infinite"
      }
    },

    {
      "id": "swarm_shopper_01",
      "name": "Generic Shopper",
      "role": "Ambient Swarm NPC",
      "home_zone": "MAIN_HALL",
      "visual": {
        "uniform": "Beige clothes, nondescript",
        "iconic_detail": "Shopping bag, always",
        "silhouette": "Average height, forgettable",
        "text_anchor": "beige shopper bag"
      },
      "spine": {
        "domain_lock": "Wander, shop, blend",
        "never_list": [],
        "rituals": ["Walk slowly", "Look at storefronts", "Avoid eye contact"],
        "props": ["shopping_bag"],
        "contradiction_trigger": 999.0,
        "contradiction_action": "none"
      },
      "dialogue": {
        "normal": ["...", "Oh.", "Hmm."],
        "stressed": [],
        "contradiction": []
      },
      "hints": {
        "normal": "wander_idle",
        "stressed": "wander_idle",
        "contradicted": "wander_idle"
      }
    }
  ],

  "zones": [
    {
      "id": "FC-CORE",
      "name": "Food Court - Central Area",
      "level": -1,
      "tags": ["food_court", "social", "loud"],
      "neighbors": ["FC-ARCADE", "MAIN_HALL"],
      "initial_turbulence": 1.0,
      "cloud_modifiers": {
        "base": 0,
        "on_player_enter": 1,
        "on_discovery": 3
      }
    },

    {
      "id": "FC-ARCADE",
      "name": "Food Court - Arcade Zone",
      "level": -1,
      "tags": ["food_court", "entertainment", "noise", "entropy"],
      "neighbors": ["FC-CORE", "SERVICE_CORRIDOR"],
      "initial_turbulence": 2.5,
      "cloud_modifiers": {
        "base": 1,
        "on_player_enter": 2,
        "on_discovery": 5
      }
    },

    {
      "id": "SERVICE_CORRIDOR",
      "name": "Service Corridor - Janitor Domain",
      "level": 0,
      "tags": ["service", "quiet", "loops", "maintenance"],
      "neighbors": ["FC-ARCADE", "MAIN_HALL"],
      "initial_turbulence": 0.5,
      "cloud_modifiers": {
        "base": 0,
        "on_player_enter": 3,
        "on_discovery": 8
      }
    },

    {
      "id": "MAIN_HALL",
      "name": "Main Hall - Upper Level",
      "level": 0,
      "tags": ["retail", "public", "bright"],
      "neighbors": ["FC-CORE", "SERVICE_CORRIDOR"],
      "initial_turbulence": 0.0,
      "cloud_modifiers": {
        "base": 0,
        "on_player_enter": 0.5,
        "on_discovery": 2
      }
    }
  ],

  "scenarios": [
    {
      "id": "janitor_loop_demo",
      "name": "Janitor Contradiction Demo",
      "description": "Raise Cloud to 75+ to trigger janitor loop contradiction",
      "initial_conditions": {
        "cloud_level": 60.0,
        "player_zone": "SERVICE_CORRIDOR"
      },
      "triggers": [
        {
          "type": "cloud_threshold",
          "value": 75.0,
          "action": "janitor_contradiction"
        }
      ],
      "expected_outcome": "Janitor's maintenance loop becomes visible infinite recursion"
    }
  ]
}
```

---

## 4. UE5 C++ Client Example

### File: `UE5_Project/Source/MallGame/MallSimSubsystem.h`

```cpp
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "Http.h"
#include "MallSimSubsystem.generated.h"

USTRUCT(BlueprintType)
struct FCloudState
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly)
    float Level = 50.0f;

    UPROPERTY(BlueprintReadOnly)
    FString Mood = TEXT("UNEASY");

    UPROPERTY(BlueprintReadOnly)
    FString Trend = TEXT("STABLE");
};

USTRUCT(BlueprintType)
struct FNPCUpdate
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly)
    FString ID;

    UPROPERTY(BlueprintReadOnly)
    FString Name;

    UPROPERTY(BlueprintReadOnly)
    FString State;

    UPROPERTY(BlueprintReadOnly)
    FString Zone;

    UPROPERTY(BlueprintReadOnly)
    FString Hint;

    UPROPERTY(BlueprintReadOnly)
    FString Dialogue;

    UPROPERTY(BlueprintReadOnly)
    float StressLevel = 0.0f;
};

UCLASS()
class MALLGAME_API UMallSimSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    UFUNCTION(BlueprintCallable, Category = "Mall Simulation")
    void InitializeSimulation(const FString& ConfigPath);

    UFUNCTION(BlueprintCallable, Category = "Mall Simulation")
    void TickSimulation(float DeltaTime, const FString& PlayerEventType, const FString& PlayerEventData);

    UFUNCTION(BlueprintPure, Category = "Mall Simulation")
    FCloudState GetCloudState() const { return CurrentCloudState; }

    UFUNCTION(BlueprintPure, Category = "Mall Simulation")
    TArray<FNPCUpdate> GetNPCUpdates() const { return CurrentNPCUpdates; }

private:
    void SendInitRequest(const FString& ConfigPath);
    void SendTickRequest(float DeltaTime, const FString& EventType, const FString& EventData);

    void OnInitResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful);
    void OnTickResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful);

    FString WorldID;
    FString SimulationServerURL = TEXT("http://127.0.0.1:5000");

    FCloudState CurrentCloudState;
    TArray<FNPCUpdate> CurrentNPCUpdates;

    float SimAccumulator = 0.0f;
    const float SimTickRate = 0.25f; // 4 Hz
};
```

### File: `UE5_Project/Source/MallGame/MallSimSubsystem.cpp`

```cpp
#include "MallSimSubsystem.h"
#include "HttpModule.h"
#include "Json.h"
#include "JsonUtilities.h"

void UMallSimSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    UE_LOG(LogTemp, Log, TEXT("MallSimSubsystem initialized"));
}

void UMallSimSubsystem::Deinitialize()
{
    Super::Deinitialize();
    UE_LOG(LogTemp, Log, TEXT("MallSimSubsystem deinitialized"));
}

void UMallSimSubsystem::InitializeSimulation(const FString& ConfigPath)
{
    SendInitRequest(ConfigPath);
}

void UMallSimSubsystem::TickSimulation(float DeltaTime, const FString& PlayerEventType, const FString& PlayerEventData)
{
    SimAccumulator += DeltaTime;

    if (SimAccumulator >= SimTickRate)
    {
        SendTickRequest(SimAccumulator, PlayerEventType, PlayerEventData);
        SimAccumulator = 0.0f;
    }
}

void UMallSimSubsystem::SendInitRequest(const FString& ConfigPath)
{
    TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
    Request->OnProcessRequestComplete().BindUObject(this, &UMallSimSubsystem::OnInitResponseReceived);
    Request->SetURL(SimulationServerURL + TEXT("/init"));
    Request->SetVerb(TEXT("POST"));
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("config_path"), ConfigPath);

    FString RequestBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&RequestBody);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    Request->SetContentAsString(RequestBody);
    Request->ProcessRequest();
}

void UMallSimSubsystem::SendTickRequest(float DeltaTime, const FString& EventType, const FString& EventData)
{
    if (WorldID.IsEmpty())
    {
        UE_LOG(LogTemp, Warning, TEXT("Cannot tick: WorldID not set"));
        return;
    }

    TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
    Request->OnProcessRequestComplete().BindUObject(this, &UMallSimSubsystem::OnTickResponseReceived);
    Request->SetURL(SimulationServerURL + TEXT("/tick"));
    Request->SetVerb(TEXT("POST"));
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("world_id"), WorldID);
    JsonObject->SetNumberField(TEXT("dt"), DeltaTime);

    if (!EventType.IsEmpty())
    {
        TSharedPtr<FJsonObject> PlayerEvent = MakeShareable(new FJsonObject);
        PlayerEvent->SetStringField(TEXT("type"), EventType);
        PlayerEvent->SetStringField(TEXT("to_zone"), EventData); // Simplified
        JsonObject->SetObjectField(TEXT("player_event"), PlayerEvent);
    }

    FString RequestBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&RequestBody);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    Request->SetContentAsString(RequestBody);
    Request->ProcessRequest();
}

void UMallSimSubsystem::OnInitResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
{
    if (!bWasSuccessful || !Response.IsValid())
    {
        UE_LOG(LogTemp, Error, TEXT("Init request failed"));
        return;
    }

    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Response->GetContentAsString());

    if (FJsonSerializer::Deserialize(Reader, JsonObject))
    {
        WorldID = JsonObject->GetStringField(TEXT("world_id"));
        UE_LOG(LogTemp, Log, TEXT("Simulation initialized: %s"), *WorldID);
    }
}

void UMallSimSubsystem::OnTickResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
{
    if (!bWasSuccessful || !Response.IsValid())
    {
        UE_LOG(LogTemp, Error, TEXT("Tick request failed"));
        return;
    }

    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Response->GetContentAsString());

    if (FJsonSerializer::Deserialize(Reader, JsonObject))
    {
        // Parse Cloud
        const TSharedPtr<FJsonObject>* CloudObj;
        if (JsonObject->TryGetObjectField(TEXT("cloud"), CloudObj))
        {
            CurrentCloudState.Level = (*CloudObj)->GetNumberField(TEXT("level"));
            CurrentCloudState.Mood = (*CloudObj)->GetStringField(TEXT("mood"));
            CurrentCloudState.Trend = (*CloudObj)->GetStringField(TEXT("trend"));
        }

        // Parse NPCs
        const TArray<TSharedPtr<FJsonValue>>* NPCArray;
        if (JsonObject->TryGetArrayField(TEXT("npcs"), NPCArray))
        {
            CurrentNPCUpdates.Empty();

            for (const TSharedPtr<FJsonValue>& NPCValue : *NPCArray)
            {
                const TSharedPtr<FJsonObject>& NPCObj = NPCValue->AsObject();

                FNPCUpdate Update;
                Update.ID = NPCObj->GetStringField(TEXT("id"));
                Update.Name = NPCObj->GetStringField(TEXT("name"));
                Update.State = NPCObj->GetStringField(TEXT("state"));
                Update.Zone = NPCObj->GetStringField(TEXT("zone"));
                Update.Hint = NPCObj->GetStringField(TEXT("hint"));
                Update.Dialogue = NPCObj->GetStringField(TEXT("dialogue"));
                Update.StressLevel = NPCObj->GetNumberField(TEXT("stress_level"));

                CurrentNPCUpdates.Add(Update);
            }

            UE_LOG(LogTemp, Log, TEXT("Received %d NPC updates"), CurrentNPCUpdates.Num());
        }
    }
}
```

---

## 5. Testing Workflow

### Step 1: Start Python Server
```bash
cd v6-nextgen
python src/sim_server.py
```

### Step 2: Test Init
```bash
curl -X POST http://localhost:5000/init \
  -H "Content-Type: application/json" \
  -d '{"config_path": "data/config/mall_v6_minimal.json"}'
```

**Expected response:**
```json
{
  "world_id": "mall_abc12345",
  "status": "initialized",
  "config": {...}
}
```

### Step 3: Test Tick (Normal)
```bash
curl -X POST http://localhost:5000/tick \
  -H "Content-Type: application/json" \
  -d '{
    "world_id": "mall_abc12345",
    "dt": 0.25,
    "player_event": {"type": "wait"}
  }'
```

### Step 4: Test Tick (Player Moves)
```bash
curl -X POST http://localhost:5000/tick \
  -H "Content-Type: application/json" \
  -d '{
    "world_id": "mall_abc12345",
    "dt": 0.25,
    "player_event": {
      "type": "move",
      "to_zone": "FC-ARCADE",
      "from_zone": "MAIN_HALL"
    }
  }'
```

### Step 5: Raise Cloud to Trigger Contradiction
```bash
# Send multiple "discover" events to raise Cloud
for i in {1..10}; do
  curl -X POST http://localhost:5000/tick \
    -H "Content-Type: application/json" \
    -d '{
      "world_id": "mall_abc12345",
      "dt": 0.25,
      "player_event": {"type": "discover", "document": "log_00'"$i"'"}
    }'
  sleep 0.3
done
```

**Expected:** Cloud level rises to 75+, janitor triggers contradiction

---

## 6. Next Steps

1. ✅ **Copy these files to v6-nextgen/src/**
2. 🔴 **Create `data/config/mall_v6_minimal.json`**
3. 🔴 **Test Python server standalone**
4. 🔴 **Create UE5 test project**
5. 🔴 **Implement C++ subsystem**
6. 🔴 **Verify end-to-end integration**

---

**End of Specification**

**Related:** `V6_UE5_ACE_INTEGRATION_ANALYSIS.md` (strategy overview)
**Next:** `UE5_INTEGRATION_COOKBOOK.md` (step-by-step setup guide)
