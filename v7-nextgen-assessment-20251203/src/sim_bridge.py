#!/usr/bin/env python3
"""
sim_bridge.py

Thin bridge between the Python simulation core (Cloud, NPC spines, topology, QBIT)
and any external client (CLI, Flask server, UE5, etc.).

IMPORTANT: Cloud object structure is locked for API consistency.
See docs/API.md for canonical JSON contracts.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import time

# Import real v6 systems
from cloud import Cloud, MallMood, ZoneMicrostate, PressureTrend
from npc_state_machine import NPCState, NPCSpine, NPCStateMachine


# ========== DATA STRUCTURES ==========

@dataclass
class CloudState:
    """
    Cloud state snapshot - LOCKED contract.

    This structure is used by both /status and /tick endpoints.
    DO NOT CHANGE without updating API.md.
    """
    level: float              # 0-100
    mood: str                 # "calm", "uneasy", "strained", "critical"
    trend: str                # "stable", "rising", "falling", "spiking"
    bleed_tier: int           # 0-3
    bleed_ready: bool         # Has bleed threshold been reached
    pressure_rate: float = 0.1  # Change per second (optional)


@dataclass
class NPCSummary:
    """NPC state for a single tick - LOCKED contract."""
    id: str
    zone: str
    state: str                # "idle", "patrol", "alert", "suspicious", "hostile", "contradiction"
    behavior_hint: str        # Animation/behavior hint for renderer


@dataclass
class ZoneUpdate:
    """Zone microstate for a single tick."""
    zone_id: str
    turbulence: float         # 0-10
    resonance: float          # 0-100+
    qbit_aggregate: float     # 0-6000+
    qbit_power: float         # 0-3000+
    qbit_charisma: float      # 0-3000+
    qbit_entity_count: int    # Number of entities in zone
    swarm_bias: Dict[str, Any]
    adjacency: Dict[str, float]  # zone_id → probability


@dataclass
class GameEvent:
    """Discrete event that occurred this tick - LOCKED contract."""
    type: str                 # "contradiction", "cloud_mood_changed", etc.
    timestamp: float
    details: Dict[str, Any]


@dataclass
class FrameUpdate:
    """
    Complete simulation state for one frame - LOCKED contract.

    This is what gets sent back to UE5.
    See docs/API.md for canonical JSON shape.
    """
    timestamp: float
    cloud: CloudState
    npcs: List[NPCSummary]
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
    type: str                 # "move", "interact", "discover", "wait", "run"
    timestamp: float
    data: Dict[str, Any]      # Event-specific payload


@dataclass
class WorldState:
    """
    Persistent world state.
    This is the simulation's memory.
    """
    cloud: Cloud              # Real Cloud instance from cloud.py
    zones: Dict[str, ZoneMicrostate]  # Cloud's zone dict
    npcs: Dict[str, NPCStateMachine]  # NPC state machines


# ========== CONFIG LOADING ==========

def _load_npcs(config_path: str, zones: Dict[str, ZoneMicrostate]) -> Dict[str, NPCStateMachine]:
    """
    Load NPCs as NPCStateMachine instances from config.

    Expected file: config/npcs.json
    """
    npcs_file = Path(config_path) / "npcs.json"

    if not npcs_file.exists():
        print(f"[BRIDGE] Warning: {npcs_file} not found, no NPCs loaded")
        return {}

    with npcs_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    npcs: Dict[str, NPCStateMachine] = {}

    for n in data.get("npcs", []):
        npc_id = n["id"]
        spine_data = n.get("spine", {})

        # Create NPCSpine
        spine = NPCSpine(
            npc_id=npc_id,
            name=n.get("name", npc_id),
            role=n.get("role", "Secondary"),
            never_rules=spine_data.get("never_list", []),
            always_rules=spine_data.get("always_rules", []),
            qbit_power=spine_data.get("qbit_power", 0),
            qbit_charisma=spine_data.get("qbit_charisma", 0),
            home_zone=n.get("home_zone", ""),
            allowed_zones=n.get("allowed_zones", []),
            forbidden_zones=spine_data.get("forbidden_zones", [])
        )

        # Create NPCStateMachine
        npc_machine = NPCStateMachine(
            npc_id=npc_id,
            spine=spine,
            current_zone=n.get("home_zone", "")
        )

        npcs[npc_id] = npc_machine

    print(f"[BRIDGE] Loaded {len(npcs)} NPCs")
    return npcs


# ========== CORE API FUNCTIONS ==========

def init_world(config_path: str) -> WorldState:
    """
    Initialize simulation from config using real Cloud.

    Args:
        config_path: Path to config folder containing zones.json, npcs.json

    Returns:
        WorldState ready for ticking

    Example:
        >>> world = init_world("config")
        >>> print(len(world.zones))
        11
    """
    config_dir = Path(config_path)
    if not config_dir.exists():
        raise FileNotFoundError(f"Config path not found: {config_path}")

    print(f"[BRIDGE] Initializing world from {config_path}")

    # Create real Cloud instance (handles zones + QBIT internally)
    entities_path = config_dir.parent / "canon" / "entities"
    cloud = Cloud(
        save_path=None,  # Don't auto-load saved state for now
        entities_path=str(entities_path) if entities_path.exists() else None
    )

    # Load NPCs (Cloud's zones are already initialized)
    npcs = _load_npcs(config_path, cloud.zones)

    world = WorldState(
        cloud=cloud,
        zones=cloud.zones,  # Use Cloud's zone dict directly
        npcs=npcs
    )

    print(f"[BRIDGE] World initialized:")
    print(f"  Zones: {len(world.zones)}")
    print(f"  NPCs: {len(world.npcs)}")
    print(f"  Entities: {len(world.cloud.entities)}")
    print(f"  Cloud level: {world.cloud.cloud_level:.1f}")

    return world


def tick_world(
    world: WorldState,
    dt: float,
    player_event: Optional[Dict] = None
) -> FrameUpdate:
    """
    Advance simulation by one tick using real Cloud.update().

    Args:
        world: Current world state
        dt: Delta time in seconds (typically 0.25)
        player_event: Optional player action
            Examples:
            {"type": "move", "to_zone": "FC-ARCADE", "from_zone": "CORE"}
            {"type": "interact", "target": "bag_of_screams", "zone": "FC-ARCADE"}
            {"type": "discover", "document": "log_017", "zone": "SERVICE_HALL"}
            {"type": "wait"}

    Returns:
        FrameUpdate with current state for UE5 to render

    Example:
        >>> update = tick_world(world, 0.25, {"type": "move", "to_zone": "FC-ARCADE"})
        >>> print(update.cloud.mood)
        "uneasy"
    """
    current_time = time.time()

    # Parse player event
    event = None
    if player_event:
        event = PlayerEvent(
            type=player_event.get("type", "wait"),
            timestamp=current_time,
            data=player_event
        )

    # Build player_action dict for Cloud.update()
    player_action = None
    if event:
        player_action = {
            "type": event.type,
            "zone": event.data.get("to_zone", event.data.get("zone", "")),
            "target": event.data.get("target", ""),
            "time_in_zone": 0  # Could track this externally
        }

    # Update Cloud (this updates zones internally)
    hints = world.cloud.update(dt, player_action=player_action, npc_events=None)

    # Extract cloud state - LOCKED structure for API consistency
    cloud_state = CloudState(
        level=world.cloud.cloud_level,
        mood=world.cloud.mall_mood.value,
        trend=world.cloud.pressure_trend.value,
        bleed_tier=world.cloud.current_bleed_tier,
        bleed_ready=world.cloud.bleed_threshold_reached,
        pressure_rate=0.1  # Or calculate from Cloud history
    )

    # Update NPCs
    npc_updates = _tick_npcs(world, dt, event, cloud_state)

    # Build zone updates
    zone_updates = _build_zone_updates(world)

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


# ========== INTERNAL TICK FUNCTIONS ==========

def _tick_npcs(
    world: WorldState,
    dt: float,
    player_event: Optional[PlayerEvent],
    cloud_state: CloudState
) -> List[NPCSummary]:
    """
    Update all NPCs using real NPCStateMachine.update().
    """
    updates = []

    current_zone = player_event.data.get("to_zone", "") if player_event else ""

    for npc_id, npc_machine in world.npcs.items():
        # Call real NPCStateMachine.update()
        hints = npc_machine.update(
            dt=dt,
            cloud_level=cloud_state.level,
            cloud_mood=cloud_state.mood,
            player_nearby=(npc_machine.current_zone == current_zone),
            player_action=player_event.type if player_event else None
        )

        # Build NPCSummary from hints
        update = NPCSummary(
            id=hints["npc_id"],
            zone=hints["current_zone"],
            state=hints["state"],
            behavior_hint=hints.get("behavior_hint", "idle")  # Fallback to idle
        )

        updates.append(update)

    return updates


def _build_zone_updates(world: WorldState) -> Dict[str, ZoneUpdate]:
    """Build zone updates from Cloud's zone microstates."""
    updates = {}

    for zone_id, zone in world.zones.items():
        updates[zone_id] = ZoneUpdate(
            zone_id=zone.zone_id,
            turbulence=zone.turbulence,
            resonance=zone.resonance,
            qbit_aggregate=zone.qbit_aggregate,
            qbit_power=zone.qbit_power,
            qbit_charisma=zone.qbit_charisma,
            qbit_entity_count=zone.qbit_entity_count,
            swarm_bias=zone.swarm_bias,
            adjacency=zone.adjacency
        )

    return updates


def _collect_events(
    world: WorldState,
    cloud_state: CloudState,
    npc_updates: List[NPCSummary]
) -> List[GameEvent]:
    """
    Collect discrete events that occurred this tick.
    """
    events = []

    # Check for NPC contradictions
    for npc in npc_updates:
        if npc.state == "contradiction":
            events.append(GameEvent(
                type="contradiction_triggered",
                timestamp=time.time(),
                details={
                    "npc_id": npc.id,
                    "npc_zone": npc.zone,
                    "cloud_level": cloud_state.level
                }
            ))

    # Check for cloud mood changes
    # (Cloud tracks prev_mood internally, we could expose it)
    # For now, skip mood change detection

    return events


# ========== SERIALIZATION ==========

def serialize_frame(frame: FrameUpdate) -> str:
    """Convert FrameUpdate to JSON string."""
    return json.dumps(frame.to_dict(), indent=2)


# ========== MODULE TESTING ==========

if __name__ == "__main__":
    print("=" * 60)
    print("SIM BRIDGE TEST")
    print("=" * 60)

    # Test init
    try:
        print("\nInitializing world...")
        world = init_world("../config")  # Relative to src/

        print("\nInitial state:")
        print(f"  Cloud: {world.cloud.cloud_level:.1f}")
        print(f"  Zones: {len(world.zones)}")
        print(f"  NPCs: {len(world.npcs)}")

        # Test tick
        print("\nTesting tick...")
        frame = tick_world(world, 0.25, {
            "type": "move",
            "to_zone": "FC-ARCADE",
            "from_zone": "CORRIDOR"
        })

        print(f"\nFrame update:")
        print(f"  Cloud: {frame.cloud.level:.1f} ({frame.cloud.mood})")
        print(f"  NPCs: {len(frame.npcs)}")
        print(f"  Events: {len(frame.events)}")

        # Print NPCs
        for npc in frame.npcs[:3]:
            print(f"    {npc.id}: {npc.state} @ {npc.zone}")

        print("\n✓ Bridge test complete")

    except FileNotFoundError as e:
        print(f"\n✗ Config not found: {e}")
        print("  Create config/npcs.json first")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
