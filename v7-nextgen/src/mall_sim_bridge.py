#!/usr/bin/env python3
"""
mall-sim ↔ Mall_OS Integration Bridge

Bridges the v2/v3 mall_simulation.py runtime with Mall_OS Cloud/QBIT systems.

Implements:
1. QBIT adapter for mall-sim NPCs
2. Spine overlay for anchor NPCs
3. ZoneMicrostate wrapper around world_tiles
4. Heat ↔ Cloud adapter (Heat * 20 = Cloud)
5. Persistence layer (JSON snapshot)
6. Adjacency matrix builder from layout
7. Unified mall_os_step() orchestrator

Design principle: Wrap, don't rewrite. mall-sim stays intact.
"""

import json
import os
import time
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from pathlib import Path


# =============================================================================
# 1. QBIT ADAPTER FOR mall-sim NPCs
# =============================================================================

@dataclass
class QbitStats:
    """QBIT scoring attached to mall-sim NPCs."""
    power: int = 0       # Structural leverage (0-3000)
    charisma: int = 0    # Attention/resonance (0-3000)
    overall: int = 0     # Combined score (0-6000)


# Default QBIT mappings by faction/role
QBIT_DEFAULTS = {
    # Faction-based defaults
    "security": QbitStats(power=1800, charisma=600, overall=2400),
    "workers": QbitStats(power=400, charisma=800, overall=1200),
    "shoppers": QbitStats(power=100, charisma=400, overall=500),
    "teens": QbitStats(power=200, charisma=1600, overall=1800),

    # Role-based overrides (higher specificity)
    "security_chief": QbitStats(power=2400, charisma=1200, overall=3600),
    "janitor": QbitStats(power=2400, charisma=800, overall=3200),
    "arcade_guy": QbitStats(power=1200, charisma=2000, overall=3200),
    "hard_copy": QbitStats(power=800, charisma=2400, overall=3200),
}


def compute_npc_qbit(npc_data: Dict[str, Any]) -> QbitStats:
    """
    Compute QBIT stats for a mall-sim NPC based on faction/role/aggression.

    Args:
        npc_data: NPC dict with 'faction', 'name', 'aggression', etc.

    Returns:
        QbitStats with power/charisma/overall
    """
    faction = npc_data.get("faction", "shoppers")
    name = npc_data.get("name", "").lower()
    aggression = npc_data.get("aggression", 0.5)

    # Check for role-based override first
    for role_key, stats in QBIT_DEFAULTS.items():
        if role_key in name:
            return QbitStats(
                power=stats.power,
                charisma=stats.charisma,
                overall=stats.overall
            )

    # Fall back to faction defaults
    base = QBIT_DEFAULTS.get(faction, QbitStats(power=100, charisma=100, overall=200))

    # Modify by aggression (high aggression = more power, less charisma)
    power_mod = int(aggression * 500)
    charisma_mod = int((1.0 - aggression) * 300)

    return QbitStats(
        power=base.power + power_mod,
        charisma=base.charisma + charisma_mod,
        overall=base.power + power_mod + base.charisma + charisma_mod
    )


def attach_qbit_to_npc(npc: Any) -> None:
    """
    Attach QBIT stats to a mall-sim NPC object in-place.

    Args:
        npc: NPCAgent or similar object with faction/name attributes
    """
    npc_data = {
        "faction": getattr(npc, "faction", "shoppers"),
        "name": getattr(npc, "name", ""),
        "aggression": getattr(npc, "aggression", 0.5),
    }
    npc.qbit = compute_npc_qbit(npc_data)


# =============================================================================
# 2. SPINE OVERLAY FOR ANCHOR NPCs
# =============================================================================

@dataclass
class SpineOverlay:
    """Mall_OS-style spine rules overlaid on mall-sim NPC."""
    npc_id: str
    spine_id: str
    never_rules: List[str] = field(default_factory=list)
    always_rules: List[str] = field(default_factory=list)
    spatial_constraints: List[str] = field(default_factory=list)
    home_zone: str = ""
    forbidden_zones: List[str] = field(default_factory=list)

    # State tracking
    contradiction_active: bool = False
    last_contradiction_time: float = 0.0


# Registry of spines for anchor NPCs
SPINE_REGISTRY: Dict[str, SpineOverlay] = {}


def load_spine_registry(spine_dir: str) -> Dict[str, SpineOverlay]:
    """
    Load all spine JSONs from a directory into the registry.

    Args:
        spine_dir: Path to directory containing spine JSON files

    Returns:
        Dict of spine_id → SpineOverlay
    """
    spine_path = Path(spine_dir)

    if not spine_path.exists():
        print(f"[BRIDGE] Spine directory not found: {spine_dir}")
        return SPINE_REGISTRY

    for json_file in spine_path.glob("*.json"):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)

            spine_id = data.get("id", json_file.stem)
            spine = SpineOverlay(
                npc_id=spine_id,
                spine_id=spine_id,
                never_rules=data.get("never_rules", []),
                always_rules=data.get("always_rules", []),
                spatial_constraints=data.get("spatial_constraints", []),
                home_zone=data.get("home_zone", ""),
                forbidden_zones=data.get("forbidden_zones", []),
            )
            SPINE_REGISTRY[spine_id] = spine

        except Exception as e:
            print(f"[BRIDGE] Error loading spine {json_file.name}: {e}")

    print(f"[BRIDGE] Loaded {len(SPINE_REGISTRY)} spines")
    return SPINE_REGISTRY


def attach_spine_to_npc(npc: Any, spine_id: str) -> Optional[SpineOverlay]:
    """
    Attach a Mall_OS spine overlay to a mall-sim NPC.

    Args:
        npc: mall-sim NPC object
        spine_id: ID of spine to attach from registry

    Returns:
        SpineOverlay if found, None otherwise
    """
    if spine_id not in SPINE_REGISTRY:
        print(f"[BRIDGE] Spine not found: {spine_id}")
        return None

    spine = SPINE_REGISTRY[spine_id]
    npc.spine_overlay = spine
    return spine


def check_spine_contradiction(npc: Any, cloud_level: float, action: str) -> bool:
    """
    Check if NPC action violates spine rules (triggers contradiction).

    Args:
        npc: NPC with spine_overlay attached
        cloud_level: Current Cloud pressure (0-100)
        action: Action being attempted

    Returns:
        True if contradiction should trigger
    """
    spine = getattr(npc, 'spine_overlay', None)
    if not spine:
        return False

    # Get QBIT power for threshold calculation
    qbit = getattr(npc, 'qbit', QbitStats())

    # Base threshold is 75 (CRITICAL), high-power reduces it
    threshold = 75.0
    if qbit.power > 2000:
        threshold = 60.0
    elif qbit.power > 1500:
        threshold = 65.0
    elif qbit.power > 1000:
        threshold = 70.0

    # Check if Cloud is high enough for contradiction
    if cloud_level < threshold:
        return False

    # Check if action violates never_rules
    for rule in spine.never_rules:
        if action.lower() in rule.lower():
            spine.contradiction_active = True
            spine.last_contradiction_time = time.time()
            return True

    return False


# =============================================================================
# 3. ZONEMICROSTATE WRAPPER AROUND mall-sim TILES
# =============================================================================

@dataclass
class ZoneMicrostateWrapper:
    """
    Mall_OS ZoneMicrostate built from mall-sim tile data.

    Wraps a patch of world_tiles into Mall_OS-compatible zone state.
    """
    zone_id: str
    tiles: Dict[Tuple[int, int], Any] = field(default_factory=dict)

    # Mall_OS fields
    turbulence: float = 0.0          # 0-10 scale
    resonance: float = 0.0           # Echo accumulation
    cloud_pressure: float = 0.0      # Zone-local pressure (0-100)
    qbit_aggregate: float = 0.0      # Total entity influence
    qbit_power: float = 0.0
    qbit_charisma: float = 0.0
    qbit_entity_count: int = 0

    swarm_bias: Dict = field(default_factory=lambda: {
        "color_weight": 0.0,
        "clustering": 0.0,
        "speed": 1.0,
        "avoidance": []
    })

    last_player_visit: float = 0.0
    discovery_count: int = 0
    adjacency: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Serialize for persistence."""
        return {
            "zone_id": self.zone_id,
            "turbulence": self.turbulence,
            "resonance": self.resonance,
            "cloud_pressure": self.cloud_pressure,
            "qbit_aggregate": self.qbit_aggregate,
            "qbit_power": self.qbit_power,
            "qbit_charisma": self.qbit_charisma,
            "qbit_entity_count": self.qbit_entity_count,
            "swarm_bias": self.swarm_bias,
            "last_player_visit": self.last_player_visit,
            "discovery_count": self.discovery_count,
            "adjacency": self.adjacency,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ZoneMicrostateWrapper':
        """Deserialize from persistence."""
        wrapper = cls(zone_id=data["zone_id"])
        wrapper.turbulence = data.get("turbulence", 0.0)
        wrapper.resonance = data.get("resonance", 0.0)
        wrapper.cloud_pressure = data.get("cloud_pressure", 0.0)
        wrapper.qbit_aggregate = data.get("qbit_aggregate", 0.0)
        wrapper.qbit_power = data.get("qbit_power", 0.0)
        wrapper.qbit_charisma = data.get("qbit_charisma", 0.0)
        wrapper.qbit_entity_count = data.get("qbit_entity_count", 0)
        wrapper.swarm_bias = data.get("swarm_bias", wrapper.swarm_bias)
        wrapper.last_player_visit = data.get("last_player_visit", 0.0)
        wrapper.discovery_count = data.get("discovery_count", 0)
        wrapper.adjacency = data.get("adjacency", {})
        return wrapper


def build_zone_from_mall_sim(
    world_tiles: Dict[Tuple[int, int, int], Any],
    zone_id: str,
    zone_bounds: Tuple[int, int, int, int]  # (x_min, y_min, x_max, y_max)
) -> ZoneMicrostateWrapper:
    """
    Build a Mall_OS ZoneMicrostate from mall-sim world_tiles.

    Args:
        world_tiles: mall-sim tile dict {(x,y,z): TileType}
        zone_id: Zone identifier
        zone_bounds: Bounding box (x_min, y_min, x_max, y_max)

    Returns:
        ZoneMicrostateWrapper populated from tiles
    """
    x_min, y_min, x_max, y_max = zone_bounds

    # Extract tiles within bounds
    zone_tiles = {}
    for (x, y, z), tile in world_tiles.items():
        if x_min <= x <= x_max and y_min <= y <= y_max:
            zone_tiles[(x, y)] = tile

    wrapper = ZoneMicrostateWrapper(
        zone_id=zone_id,
        tiles=zone_tiles
    )

    # Calculate initial values based on tile composition
    total_tiles = len(zone_tiles)
    if total_tiles > 0:
        restricted_count = sum(
            1 for t in zone_tiles.values()
            if hasattr(t, 'type') and ('SECURITY' in str(t.type) or 'STAFF' in str(t.type))
        )
        # More restricted tiles = higher base turbulence
        wrapper.turbulence = (restricted_count / total_tiles) * 5.0

    return wrapper


# =============================================================================
# 4. HEAT ↔ CLOUD ADAPTER
# =============================================================================

def heat_to_cloud(heat_level: float) -> float:
    """
    Convert mall-sim Heat (0-5) to Mall_OS Cloud (0-100).

    Mapping: Heat * 20 = Cloud
    """
    return max(0.0, min(100.0, heat_level * 20.0))


def cloud_to_heat(cloud_level: float) -> float:
    """
    Convert Mall_OS Cloud (0-100) to mall-sim Heat (0-5).

    Mapping: Cloud / 20 = Heat
    """
    return max(0.0, min(5.0, cloud_level / 20.0))


def is_reality_breaking(heat_level: float = None, cloud_level: float = None) -> bool:
    """
    Check if reality is breaking (Heat 5 / Cloud 90+).

    Can use either heat or cloud level.
    """
    if heat_level is not None:
        return heat_level >= 4.8  # mall-sim threshold
    if cloud_level is not None:
        return cloud_level >= 90.0  # Mall_OS Bleed Tier 3
    return False


def get_bleed_tier(cloud_level: float) -> int:
    """
    Get Mall_OS bleed tier from Cloud level.

    Tier 0: 0-74 (stable)
    Tier 1: 75-79 (soft bleed)
    Tier 2: 80-89 (moderate bleed)
    Tier 3: 90-100 (severe bleed)
    """
    if cloud_level >= 90:
        return 3
    elif cloud_level >= 80:
        return 2
    elif cloud_level >= 75:
        return 1
    return 0


class HeatCloudBridge:
    """
    Bidirectional bridge between mall-sim HeatSystem and Mall_OS Cloud.

    Keeps both systems synchronized while allowing either to lead.
    """

    def __init__(self, heat_system=None, cloud=None):
        self.heat_system = heat_system
        self.cloud = cloud
        self._last_sync_time = 0.0

    def sync_heat_to_cloud(self) -> None:
        """Push heat_system state into Cloud."""
        if not self.heat_system or not self.cloud:
            return

        heat = self.heat_system.get_heat_value()
        cloud_level = heat_to_cloud(heat)

        # Set Cloud level (bypass normal update)
        self.cloud.cloud_level = cloud_level
        self.cloud._update_mood()

    def sync_cloud_to_heat(self) -> None:
        """Push Cloud state back into heat_system."""
        if not self.heat_system or not self.cloud:
            return

        cloud_level = self.cloud.cloud_level
        heat = cloud_to_heat(cloud_level)

        # Set heat level directly
        self.heat_system.current_heat = heat

    def bidirectional_sync(self, primary: str = "heat") -> None:
        """
        Sync both systems, with one as primary source.

        Args:
            primary: "heat" or "cloud" - which system is authoritative
        """
        if primary == "heat":
            self.sync_heat_to_cloud()
        else:
            self.sync_cloud_to_heat()

        self._last_sync_time = time.time()


# =============================================================================
# 5. PERSISTENCE LAYER
# =============================================================================

@dataclass
class MallSessionSnapshot:
    """Complete state snapshot for save/load."""
    timestamp: float
    version: str = "1.0-bridge"

    # mall-sim state
    heat_level: float = 0.0
    player_position: Tuple[int, int, int] = (0, 0, 0)
    npc_states: List[Dict] = field(default_factory=list)

    # Mall_OS state
    cloud_level: float = 0.0
    mall_mood: str = "calm"
    bleed_tier: int = 0
    zones: Dict[str, Dict] = field(default_factory=dict)
    discovery_history: List[Dict] = field(default_factory=list)

    # Bridge state
    qbit_cache: Dict[str, Dict] = field(default_factory=dict)


def save_mall_session(
    path: str,
    mall_sim_state: Dict[str, Any],
    cloud_state: Any,
    zones: Dict[str, ZoneMicrostateWrapper]
) -> None:
    """
    Save combined mall-sim + Mall_OS state to JSON.

    Args:
        path: Output file path
        mall_sim_state: Dict with heat_level, player_position, npcs, etc.
        cloud_state: Mall_OS Cloud instance
        zones: Dict of zone_id → ZoneMicrostateWrapper
    """
    snapshot = MallSessionSnapshot(
        timestamp=time.time(),

        # mall-sim
        heat_level=mall_sim_state.get("heat_level", 0.0),
        player_position=mall_sim_state.get("player_position", (0, 0, 0)),
        npc_states=mall_sim_state.get("npcs", []),

        # Mall_OS
        cloud_level=getattr(cloud_state, 'cloud_level', 0.0),
        mall_mood=getattr(cloud_state, 'mall_mood', 'calm'),
        bleed_tier=get_bleed_tier(getattr(cloud_state, 'cloud_level', 0.0)),
        zones={zid: z.to_dict() for zid, z in zones.items()},
        discovery_history=getattr(cloud_state, 'discovery_history', [])[-100:],
    )

    # Serialize
    data = {
        "timestamp": snapshot.timestamp,
        "version": snapshot.version,
        "mall_sim": {
            "heat_level": snapshot.heat_level,
            "player_position": list(snapshot.player_position),
            "npc_states": snapshot.npc_states,
        },
        "mall_os": {
            "cloud_level": snapshot.cloud_level,
            "mall_mood": snapshot.mall_mood,
            "bleed_tier": snapshot.bleed_tier,
            "zones": snapshot.zones,
            "discovery_history": snapshot.discovery_history,
        }
    }

    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"[BRIDGE] Session saved: {path}")


def load_mall_session(path: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Load combined mall-sim + Mall_OS state from JSON.

    Args:
        path: Input file path

    Returns:
        Tuple of (mall_sim_state, mall_os_state)
    """
    if not os.path.exists(path):
        print(f"[BRIDGE] No session file found: {path}")
        return {}, {}

    with open(path, 'r') as f:
        data = json.load(f)

    mall_sim_state = data.get("mall_sim", {})
    mall_os_state = data.get("mall_os", {})

    # Convert player_position back to tuple
    if "player_position" in mall_sim_state:
        mall_sim_state["player_position"] = tuple(mall_sim_state["player_position"])

    print(f"[BRIDGE] Session loaded: {path}")
    return mall_sim_state, mall_os_state


# =============================================================================
# 6. ADJACENCY MATRIX BUILDER
# =============================================================================

def build_adjacency_from_mall_sim(
    zones: Dict[str, ZoneMicrostateWrapper],
    explicit_connections: Optional[Dict[str, List[str]]] = None
) -> Dict[str, Dict[str, float]]:
    """
    Build QBIT-weighted adjacency matrix from zone wrappers.

    Args:
        zones: Dict of zone_id → ZoneMicrostateWrapper
        explicit_connections: Optional dict of zone_id → [connected_zone_ids]

    Returns:
        Adjacency matrix: {zone_id: {other_zone: probability}}
    """
    adjacency_matrix = {}

    for zone_id, zone in zones.items():
        adjacency_matrix[zone_id] = {}

        # Get this zone's QBIT gravity
        qbit_score = min(10, zone.qbit_aggregate / 600)
        resonance = min(1.0, zone.resonance / 100)
        turbulence = min(1.0, zone.turbulence / 10)

        qbit_gravity = (qbit_score * 0.6) + (resonance * 0.3) + (turbulence * 0.1)

        for other_zone_id, other_zone in zones.items():
            if other_zone_id == zone_id:
                continue

            # Check if explicitly connected
            if explicit_connections:
                if other_zone_id not in explicit_connections.get(zone_id, []):
                    continue

            # Calculate attraction probability
            other_qbit = min(10, other_zone.qbit_aggregate / 600) / 10
            other_res = min(1.0, other_zone.resonance / 100)

            # Similarity (like attracts like)
            similarity = 1.0 - abs(other_qbit - (qbit_score / 10))
            similarity = max(0.0, similarity)

            # Gravity pull
            gravity_pull = qbit_gravity + (other_qbit * 0.5)

            # Final probability
            p = similarity * 0.45 + gravity_pull * 0.45 + other_res * 0.1
            adjacency_matrix[zone_id][other_zone_id] = max(0, p)

        # Normalize row
        total = sum(adjacency_matrix[zone_id].values())
        if total > 0:
            for k in adjacency_matrix[zone_id]:
                adjacency_matrix[zone_id][k] /= total

    return adjacency_matrix


# =============================================================================
# 7. UNIFIED mall_os_step() ORCHESTRATOR
# =============================================================================

class MallOSBridge:
    """
    Main orchestrator bridging mall-sim and Mall_OS.

    Wraps mall-sim update inside Mall_OS update, merging render hints.
    """

    def __init__(
        self,
        mall_sim=None,
        cloud=None,
        zones: Optional[Dict[str, ZoneMicrostateWrapper]] = None
    ):
        self.mall_sim = mall_sim
        self.cloud = cloud
        self.zones = zones or {}

        self.heat_cloud_bridge = HeatCloudBridge()
        self.adjacency_matrix = {}

        self._frame_counter = 0
        self._cloud_update_interval = 10  # Update Cloud every N frames

    def initialize(
        self,
        mall_sim,
        cloud,
        spine_dir: Optional[str] = None
    ) -> None:
        """
        Initialize the bridge with simulation instances.

        Args:
            mall_sim: MallSimulation instance
            cloud: Cloud instance
            spine_dir: Path to spine JSON directory
        """
        self.mall_sim = mall_sim
        self.cloud = cloud

        # Set up heat-cloud bridge
        if hasattr(mall_sim, 'heat_system'):
            self.heat_cloud_bridge.heat_system = mall_sim.heat_system
        self.heat_cloud_bridge.cloud = cloud

        # Load spines if directory provided
        if spine_dir:
            load_spine_registry(spine_dir)

        # Attach QBIT stats to all NPCs
        if hasattr(mall_sim, 'npc_manager'):
            for npc_id, npc in mall_sim.npc_manager.npcs.items():
                attach_qbit_to_npc(npc)

        # Build zones from world_tiles if available
        if hasattr(mall_sim, 'world_tiles'):
            self._build_zones_from_tiles(mall_sim.world_tiles)

        # Copy zones to Cloud
        if self.cloud and self.zones:
            for zone_id, wrapper in self.zones.items():
                if zone_id in self.cloud.zones:
                    # Copy QBIT data
                    self.cloud.zones[zone_id].qbit_aggregate = wrapper.qbit_aggregate
                    self.cloud.zones[zone_id].qbit_power = wrapper.qbit_power
                    self.cloud.zones[zone_id].qbit_charisma = wrapper.qbit_charisma

        print("[BRIDGE] Initialized mall-sim ↔ Mall_OS bridge")

    def _build_zones_from_tiles(self, world_tiles: Dict) -> None:
        """Build zone wrappers from world_tiles."""
        # Default zone definitions (would come from config in production)
        zone_defs = {
            "FC-ARCADE": (0, 0, 15, 15),
            "SERVICE_HALL": (16, 0, 30, 10),
            "CORRIDOR": (0, 16, 50, 20),
            "STORE_BORED": (31, 0, 45, 15),
        }

        for zone_id, bounds in zone_defs.items():
            self.zones[zone_id] = build_zone_from_mall_sim(
                world_tiles, zone_id, bounds
            )

        # Build adjacency matrix
        self.adjacency_matrix = build_adjacency_from_mall_sim(self.zones)

    def mall_os_step(
        self,
        dt: float,
        player_action: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main update loop bridging mall-sim and Mall_OS.

        Args:
            dt: Delta time in seconds
            player_action: Player action dict

        Returns:
            Merged render hints from both systems
        """
        self._frame_counter += 1

        # 1. Update mall-sim
        mall_sim_hints = {}
        npc_events = []

        if self.mall_sim:
            mall_sim_hints = self.mall_sim.update(dt, player_action)

            # Extract NPC events for Cloud
            npc_events = self._extract_npc_events(mall_sim_hints)

        # 2. Sync heat → cloud (mall-sim drives, Cloud follows)
        self.heat_cloud_bridge.sync_heat_to_cloud()

        # 3. Update Mall_OS Cloud (every N frames to save cycles)
        cloud_hints = {}
        if self.cloud and self._frame_counter % self._cloud_update_interval == 0:
            cloud_hints = self.cloud.update(dt * self._cloud_update_interval, player_action, npc_events)

            # Check for contradictions
            self._check_npc_contradictions(self.cloud.cloud_level)

        # 4. Update zone states
        self._update_zone_states(dt, player_action)

        # 5. Merge render hints
        merged_hints = self._merge_render_hints(mall_sim_hints, cloud_hints)

        return merged_hints

    def _extract_npc_events(self, hints: Dict) -> List[Dict]:
        """Extract NPC events from mall-sim hints for Cloud consumption."""
        events = []

        # Extract from npc_dialogues
        dialogues = hints.get("npc_dialogues", {})
        for npc_id, dialogue in dialogues.items():
            if dialogue.get("goal_overlay"):
                events.append({
                    "type": "npc_state_change",
                    "npc_id": npc_id,
                    "new_state": "active"
                })

        # Extract from simulation_messages
        messages = hints.get("simulation_messages", [])
        for msg in messages:
            if "CONTRADICTION" in msg.upper():
                events.append({
                    "type": "npc_contradiction",
                    "message": msg
                })

        return events

    def _check_npc_contradictions(self, cloud_level: float) -> None:
        """Check all NPCs with spines for contradiction triggers."""
        if not self.mall_sim or not hasattr(self.mall_sim, 'npc_manager'):
            return

        for npc_id, npc in self.mall_sim.npc_manager.npcs.items():
            spine = getattr(npc, 'spine_overlay', None)
            if not spine:
                continue

            # Check current action against spine
            current_action = getattr(npc, 'current_goal', '')
            if check_spine_contradiction(npc, cloud_level, current_action):
                print(f"[BRIDGE] Contradiction triggered: {npc_id}")

    def _update_zone_states(self, dt: float, player_action: Optional[Dict]) -> None:
        """Update zone wrapper states based on simulation."""
        if not player_action:
            return

        current_zone = player_action.get("zone", "")
        if current_zone in self.zones:
            zone = self.zones[current_zone]
            zone.last_player_visit = time.time()
            zone.turbulence += 0.1 * dt
            zone.turbulence = min(10.0, zone.turbulence)

    def _merge_render_hints(
        self,
        mall_sim_hints: Dict,
        cloud_hints: Dict
    ) -> Dict[str, Any]:
        """
        Merge render hints from mall-sim and Mall_OS.

        mall-sim provides: npcs, props, heat_level, stealth, etc.
        Mall_OS provides: cloud_level, mood, bleed_tier, zones, etc.
        """
        merged = dict(mall_sim_hints)

        # Add Mall_OS hints
        merged["cloud_level"] = cloud_hints.get("cloud_level", 0.0)
        merged["mall_mood"] = cloud_hints.get("mood", "calm")
        merged["bleed_tier"] = get_bleed_tier(cloud_hints.get("cloud_level", 0.0))
        merged["bleed_ready"] = cloud_hints.get("bleed_ready", False)

        # Override swarm hints with Cloud-driven values
        if "swarm" in cloud_hints:
            merged["swarm"] = cloud_hints["swarm"]

        # Add zone data
        merged["zones"] = {
            zid: z.to_dict() for zid, z in self.zones.items()
        }

        # Add adjacency matrix
        merged["adjacency"] = self.adjacency_matrix

        return merged

    def save_session(self, path: str) -> None:
        """Save current session state."""
        mall_sim_state = {
            "heat_level": self.mall_sim.heat_system.get_heat_value() if self.mall_sim else 0.0,
            "player_position": self.mall_sim.get_player_position() if self.mall_sim else (0, 0, 0),
            "npcs": [],  # Would extract NPC states
        }

        save_mall_session(path, mall_sim_state, self.cloud, self.zones)

    def load_session(self, path: str) -> None:
        """Load session state."""
        mall_sim_state, mall_os_state = load_mall_session(path)

        # Restore heat
        if self.mall_sim and "heat_level" in mall_sim_state:
            self.mall_sim.heat_system.current_heat = mall_sim_state["heat_level"]

        # Restore Cloud
        if self.cloud and "cloud_level" in mall_os_state:
            self.cloud.cloud_level = mall_os_state["cloud_level"]
            self.cloud._update_mood()

        # Restore zones
        for zone_id, zone_data in mall_os_state.get("zones", {}).items():
            if zone_id in self.zones:
                self.zones[zone_id] = ZoneMicrostateWrapper.from_dict(zone_data)


# =============================================================================
# MODULE TESTING
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MALL-SIM ↔ MALL_OS BRIDGE TEST")
    print("=" * 60)

    # Test QBIT computation
    print("\n1. QBIT Adapter Test:")
    test_npcs = [
        {"faction": "security", "name": "Security Guard #1", "aggression": 0.7},
        {"faction": "teens", "name": "Teen #1", "aggression": 0.4},
        {"faction": "workers", "name": "Janitor", "aggression": 0.3},
    ]

    for npc in test_npcs:
        qbit = compute_npc_qbit(npc)
        print(f"  {npc['name']}: power={qbit.power}, charisma={qbit.charisma}, overall={qbit.overall}")

    # Test Heat↔Cloud conversion
    print("\n2. Heat ↔ Cloud Adapter Test:")
    for heat in [0, 1, 2.5, 4, 5]:
        cloud = heat_to_cloud(heat)
        back = cloud_to_heat(cloud)
        tier = get_bleed_tier(cloud)
        print(f"  Heat {heat} → Cloud {cloud} → Heat {back:.1f} (Bleed Tier {tier})")

    # Test zone wrapper
    print("\n3. ZoneMicrostate Wrapper Test:")
    mock_tiles = {(x, y, 0): "FLOOR" for x in range(10) for y in range(10)}
    zone = build_zone_from_mall_sim(mock_tiles, "TEST_ZONE", (0, 0, 10, 10))
    print(f"  Zone: {zone.zone_id}, tiles: {len(zone.tiles)}, turbulence: {zone.turbulence}")

    # Test persistence
    print("\n4. Persistence Test:")
    test_zones = {"TEST_ZONE": zone}
    save_mall_session(
        "/tmp/test_mall_session.json",
        {"heat_level": 2.5, "player_position": (10, 20, 0)},
        type('Cloud', (), {'cloud_level': 50.0, 'mall_mood': 'uneasy', 'discovery_history': []})(),
        test_zones
    )
    loaded_mall, loaded_os = load_mall_session("/tmp/test_mall_session.json")
    print(f"  Loaded heat: {loaded_mall.get('heat_level')}, cloud: {loaded_os.get('cloud_level')}")

    print("\n✓ Bridge module test complete")
