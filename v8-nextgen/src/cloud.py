#!/usr/bin/env python3
"""
CLOUD STATE SYSTEM - V6 NextGen with QBIT Integration

The Cloud is the global state machine driving all mall behavior.
"The mall remembers vibes, not details."

NEW IN V6: QBIT Entity Influence Integration
- Entity power/charisma scores affect Cloud pressure
- Zone QBIT aggregates modify turbulence
- Artifact weights use QBIT charisma
- NPC contradiction thresholds scale with QBIT power

Architecture:
- Global Cloud: Mall-wide mood/metaphysical pressure
- Zone Microstates: Local turbulence pockets with QBIT modifiers
- QBIT Entity Influence: Emergent personality gravity layer
- Pure diegetic feedback (no UI meters)
- Hard memory across sessions (vibes persist)

Driver Weights:
- Player actions: 0.50 (primary driver)
- NPC interactions: 0.25 (adds texture)
- Entity influence (QBIT): 0.15 (NEW - emergent gravity)
- Ambient drift: 0.10 (slow background noise)
"""

import json
import os
import time
import random
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path

# Import QBIT engine
from qbit_engine import (
    score_entity,
    score_entities,
    calculate_zone_qbit_aggregate
)

# Import QBIT-weighted adjacency system
from adjacency import compute_adjacency_probabilities


class MallMood(Enum):
    """Global mall mood states - the weather of the mall."""
    CALM = "calm"              # Normal mall weirdness, mostly cosmetic (0-24)
    UNEASY = "uneasy"          # Player can feel something "off" (25-49)
    STRAINED = "strained"      # NPC oddness, space tension, pre-bleed (50-74)
    CRITICAL = "critical"      # Bleed possible/likely, contradictions appear (75-100)


class PressureTrend(Enum):
    """Direction of Cloud pressure change."""
    STABLE = "stable"
    RISING = "rising"
    FALLING = "falling"
    SPIKING = "spiking"        # Rapid increase (event-driven)


@dataclass
class RoutingOverride:
    """Temporary adjacency override that decays back to baseline."""

    source_zone: str
    target_zone: str
    probability: float
    ttl: float
    reason: str = ""


@dataclass
class ZoneMicrostate:
    """Local turbulence pocket for a specific zone with QBIT modifiers."""
    zone_id: str
    turbulence: float = 0.0          # 0-10 scale
    resonance: float = 0.0           # Echo accumulation from discoveries

    # MALLOS INTEGRATION - Zone as compute node
    cloud_pressure: float = 0.0      # Zone-local pressure (0-100)
    tiles: Dict[Tuple[int, int], Dict] = field(default_factory=dict)  # Tile-based local memory

    # QBIT INTEGRATION - NEW
    qbit_aggregate: float = 0.0      # Total entity influence in this zone
    qbit_baseline: float = 0.0       # Resting QBIT influence for recovery
    qbit_power: float = 0.0          # Structural leverage weight
    qbit_charisma: float = 0.0       # Attention/resonance weight
    qbit_entity_count: int = 0       # Number of entities in zone

    swarm_bias: Dict = field(default_factory=lambda: {
        "color_weight": 0.0,         # How beige the crowd (-1 to 1)
        "clustering": 0.0,           # How much they cluster (0-1)
        "speed": 1.0,                # Movement speed multiplier
        "avoidance": []              # Zones customers avoid
    })
    last_player_visit: float = 0.0   # Timestamp
    discovery_count: int = 0         # AO3 logs found here
    last_contradiction_time: float = 0.0  # For zone cooldown (LOCKED: 30 sec)

    # QBIT-weighted adjacency probabilities
    adjacency: Dict[str, float] = field(default_factory=dict)  # zone_id → probability
    routing_overrides: List[RoutingOverride] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "zone_id": self.zone_id,
            "turbulence": self.turbulence,
            "resonance": self.resonance,
            "cloud_pressure": self.cloud_pressure,
            "tiles": {f"{k[0]},{k[1]}": v for k, v in self.tiles.items()},  # Serialize tuple keys
            "qbit_aggregate": self.qbit_aggregate,
            "qbit_baseline": self.qbit_baseline,
            "qbit_power": self.qbit_power,
            "qbit_charisma": self.qbit_charisma,
            "qbit_entity_count": self.qbit_entity_count,
            "swarm_bias": self.swarm_bias,
            "last_player_visit": self.last_player_visit,
            "discovery_count": self.discovery_count,
            "adjacency": self.adjacency,
            "routing_overrides": [
                {
                    "source_zone": o.source_zone,
                    "target_zone": o.target_zone,
                    "probability": o.probability,
                    "ttl": o.ttl,
                    "reason": o.reason,
                }
                for o in self.routing_overrides
            ],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ZoneMicrostate':
        state = cls(zone_id=data["zone_id"])
        state.turbulence = data.get("turbulence", 0.0)
        state.resonance = data.get("resonance", 0.0)
        state.cloud_pressure = data.get("cloud_pressure", 0.0)
        # Deserialize tile keys from "x,y" strings back to (x,y) tuples
        tiles_data = data.get("tiles", {})
        if isinstance(tiles_data, dict):
            state.tiles = {tuple(map(int, k.split(','))): v for k, v in tiles_data.items()}
        state.qbit_aggregate = data.get("qbit_aggregate", 0.0)
        state.qbit_baseline = data.get("qbit_baseline", state.qbit_aggregate)
        state.qbit_power = data.get("qbit_power", 0.0)
        state.qbit_charisma = data.get("qbit_charisma", 0.0)
        state.qbit_entity_count = data.get("qbit_entity_count", 0)
        state.swarm_bias = data.get("swarm_bias", state.swarm_bias)
        state.last_player_visit = data.get("last_player_visit", 0.0)
        state.discovery_count = data.get("discovery_count", 0)
        state.adjacency = data.get("adjacency", {})
        overrides_data = data.get("routing_overrides", [])
        state.routing_overrides = [
            RoutingOverride(
                source_zone=o.get("source_zone", state.zone_id),
                target_zone=o.get("target_zone", ""),
                probability=o.get("probability", 0.0),
                ttl=o.get("ttl", 0.0),
                reason=o.get("reason", ""),
            )
            for o in overrides_data
        ]
        return state


class Cloud:
    """
    Global Cloud State - The soul of the mall.

    NOW WITH QBIT: Entity influence creates emergent "personality gravity"
    that affects Cloud pressure, zone turbulence, and NPC behavior.
    """

    # Driver weights (NEW: entity influence added)
    WEIGHT_PLAYER = 0.50
    WEIGHT_NPC = 0.25
    WEIGHT_ENTITY = 0.15      # NEW - QBIT entity influence
    WEIGHT_DRIFT = 0.10

    # Mood thresholds (calm/uneasy/strained/critical)
    THRESHOLD_UNEASY = 25
    THRESHOLD_STRAINED = 50
    THRESHOLD_CRITICAL = 75

    # Bleed tiers
    BLEED_TIER_1 = 75   # Visual/Audio only
    BLEED_TIER_2 = 80   # Visual + NPC contradictions
    BLEED_TIER_3 = 90   # Visual + NPC + Space effects

    # LOCKED DECISIONS
    CLOUD_UPDATE_INTERVAL = 10           # frames
    ZONE_CONTRADICTION_COOLDOWN = 30.0   # seconds
    MAX_SWARM_CONTRIBUTION = 0.05
    BLEED_WINDDOWN_TIME = 7.5

    # QBIT INTEGRATION CONSTANTS - NEW
    QBIT_PRESSURE_SCALE = 0.0002         # Scale QBIT influence to pressure delta
    QBIT_TURBULENCE_SCALE = 0.001        # Scale QBIT aggregate to turbulence
    QBIT_RESONANCE_MODIFIER = 0.5        # QBIT charisma modifies resonance gain
    QBIT_CONTRADICTION_THRESHOLD = 2000  # QBIT power threshold for NPC breaks

    # Zone behavior modifiers
    ZONE_DRIFT_RATES = {
        "FC-ARCADE": 1.5,         # Always drifts faster (Cloud Prime Node #1)
        "SERVICE_HALL": 1.3,
        "STORE_BORED": 0.7,
        "STORE_HARD_COPY": 1.2,
        "ANCHOR_STORE": 1.0,
        "CORRIDOR": 0.9,
    }

    def __init__(self, save_path: Optional[str] = None, entities_path: Optional[str] = None):
        """Initialize Cloud state with QBIT integration."""
        self.save_path = save_path or self._default_save_path()
        self.entities_path = entities_path or self._default_entities_path()

        # Global Cloud variables
        self.cloud_level: float = 0.0
        self.pressure_trend: PressureTrend = PressureTrend.STABLE
        self.mall_mood: MallMood = MallMood.CALM
        self.bleed_threshold_reached: bool = False

        # Session tracking
        self.session_start: float = time.time()
        self.total_playtime: float = 0.0
        self.session_count: int = 0

        # Zone microstates
        self.zones: Dict[str, ZoneMicrostate] = {}
        self._init_zones()

        # QBIT INTEGRATION - NEW
        self.entities: List[Dict] = []           # All loaded entities (scored)
        self.zone_qbit_cache: Dict[str, Dict] = {}  # Zone QBIT aggregates
        self._load_and_score_entities()
        self._calculate_zone_qbit_aggregates()

        # Event history (for Echo system)
        self.discovery_history: List[Dict] = []
        self.npc_contradiction_log: List[Dict] = []

        # Bleed event tracking
        self.bleed_events_triggered: int = 0
        self.last_bleed_time: float = 0.0
        self.current_bleed_tier: int = 0

        # Pressure change tracking
        self._pressure_history: List[Tuple[float, float]] = []

        # Routing overrides (temporary adjacency tweaks)
        self.routing_overrides: List[RoutingOverride] = []
        self._adjacency_overrides_dirty: bool = False

        # QBIT-weighted adjacency matrix
        self.adjacency_matrix: Dict[str, Dict[str, float]] = {}
        self._update_adjacency_matrix()

        # Load persisted state if exists
        self._load_state()

    def _default_save_path(self) -> str:
        """Get default save path for Cloud state."""
        return os.path.join(
            os.path.dirname(__file__), '..', 'data', 'cloud_state.json'
        )

    def _default_entities_path(self) -> str:
        """Get default path for entity JSONs."""
        return os.path.join(
            os.path.dirname(__file__), '..', 'canon', 'entities'
        )

    def _init_zones(self):
        """Initialize zone microstates."""
        default_zones = [
            "FC-ARCADE",
            "SERVICE_HALL",
            "STORE_BORED",
            "STORE_HARD_COPY",
            "STORE_MILO_OPTICS",
            "ANCHOR_STORE",
            "CORRIDOR",
            "ENTRANCE",
            "KIOSK",
            "THEATER",
            "RAMP"
        ]
        for zone_id in default_zones:
            self.zones[zone_id] = ZoneMicrostate(zone_id=zone_id)

    # ========== QBIT INTEGRATION - NEW ==========

    def _load_and_score_entities(self):
        """Load all entity JSONs and score them with QBIT engine."""
        entities_dir = Path(self.entities_path)

        if not entities_dir.exists():
            print(f"[CLOUD/QBIT] Entities directory not found: {entities_dir}")
            return

        json_files = list(entities_dir.glob("*.json"))
        if not json_files:
            print(f"[CLOUD/QBIT] No entity JSON files found in {entities_dir}")
            return

        loaded_entities = []
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    entity = json.load(f)
                    # Score entity if not already scored
                    if "computed" not in entity or not entity["computed"]:
                        entity = score_entity(entity)
                    loaded_entities.append(entity)
            except Exception as e:
                print(f"[CLOUD/QBIT] Error loading {json_file.name}: {e}")

        self.entities = loaded_entities
        print(f"[CLOUD/QBIT] Loaded and scored {len(self.entities)} entities")

    def _calculate_zone_qbit_aggregates(self):
        """Calculate QBIT aggregates for all zones."""
        if not self.entities:
            print("[CLOUD/QBIT] No entities loaded, skipping aggregates")
            return

        for zone_id in self.zones.keys():
            zone_stats = calculate_zone_qbit_aggregate(self.entities, zone_id)
            self.zone_qbit_cache[zone_id] = zone_stats

            # Update zone microstate with QBIT data
            zone = self.zones[zone_id]
            zone.qbit_aggregate = zone_stats["total_influence"]
            zone.qbit_baseline = zone_stats["total_influence"]
            zone.qbit_power = zone_stats["total_power"]
            zone.qbit_charisma = zone_stats["total_charisma"]
            zone.qbit_entity_count = zone_stats["entity_count"]

        print(f"[CLOUD/QBIT] Calculated aggregates for {len(self.zone_qbit_cache)} zones")

    def get_entity_by_id(self, entity_id: str) -> Optional[Dict]:
        """Get scored entity by ID."""
        for entity in self.entities:
            if entity.get("id") == entity_id:
                return entity
        return None

    def get_zone_qbit_stats(self, zone_id: str) -> Dict:
        """Get QBIT statistics for a zone."""
        return self.zone_qbit_cache.get(zone_id, {})

    def _update_adjacency_matrix(self):
        """
        Update QBIT-weighted adjacency matrix.

        Calculates dynamic adjacency probabilities between zones based on
        QBIT influence, resonance, and turbulence. High-QBIT zones become
        narrative attractors.
        """
        base_matrix = compute_adjacency_probabilities(self.zones)

        # Apply temporary routing overrides (with TTL)
        self.adjacency_matrix = self._apply_routing_overrides(base_matrix)

        # Write adjacency back to each zone for easy access
        for zone_id, zone in self.zones.items():
            if zone_id in self.adjacency_matrix:
                zone.adjacency = self.adjacency_matrix[zone_id]

    def get_adjacent_zone_weighted(self, zone_id: str) -> Optional[str]:
        """
        Get weighted-random adjacent zone based on QBIT influence.

        High-QBIT zones have higher probability of being selected.

        Args:
            zone_id: Current zone

        Returns:
            Selected adjacent zone_id (or None if no adjacency data)
        """
        if zone_id not in self.adjacency_matrix:
            return None

        import random
        probabilities = self.adjacency_matrix[zone_id]
        if not probabilities:
            return None

        zones = list(probabilities.keys())
        weights = list(probabilities.values())

        return random.choices(zones, weights=weights, k=1)[0]

    # ========== UPDATE SYSTEM ==========

    def update(self, dt: float, player_action: Optional[Dict] = None,
               npc_events: Optional[List[Dict]] = None) -> Dict:
        """
        Main update loop - call every frame.
        NOW WITH QBIT: Entity influence affects pressure calculation.
        """
        self.total_playtime += dt

        # Calculate pressure changes from each driver
        player_delta = self._calc_player_pressure(player_action) * self.WEIGHT_PLAYER
        npc_delta = self._calc_npc_pressure(npc_events) * self.WEIGHT_NPC
        entity_delta = self._calc_entity_pressure(player_action) * self.WEIGHT_ENTITY  # NEW
        drift_delta = self._calc_drift_pressure(dt) * self.WEIGHT_DRIFT

        # Apply total pressure change
        total_delta = player_delta + npc_delta + entity_delta + drift_delta
        self._apply_pressure_change(total_delta, dt)

        # Update zone microstates (with QBIT)
        self._update_zones(dt, player_action)

        # Decay routing overrides so adjacency drifts back to baseline
        self._update_routing_overrides(dt)

        # Update QBIT-weighted adjacency matrix (every 10 updates)
        if hasattr(self, '_adjacency_update_counter'):
            self._adjacency_update_counter += 1
        else:
            self._adjacency_update_counter = 0

        if self._adjacency_overrides_dirty:
            self._update_adjacency_matrix()
            self._adjacency_overrides_dirty = False
            self._adjacency_update_counter = 0
        elif self._adjacency_update_counter % 10 == 0:
            self._update_adjacency_matrix()

        # Update mood classification
        self._update_mood()

        # Check for bleed threshold
        if self.cloud_level >= self.BLEED_TIER_1 and not self.bleed_threshold_reached:
            self.bleed_threshold_reached = True
            self.bleed_events_triggered += 1
            self.last_bleed_time = time.time()

        # Determine current bleed tier
        if self.cloud_level >= self.BLEED_TIER_3:
            self.current_bleed_tier = 3
        elif self.cloud_level >= self.BLEED_TIER_2:
            self.current_bleed_tier = 2
        elif self.cloud_level >= self.BLEED_TIER_1:
            self.current_bleed_tier = 1
        else:
            self.current_bleed_tier = 0

        # Generate render hints
        return self._generate_render_hints()

    def _calc_player_pressure(self, action: Optional[Dict]) -> float:
        """Calculate pressure change from player action."""
        if not action:
            return 0.0

        delta = 0.0
        action_type = action.get("type", "")

        if action_type == "move":
            zone = action.get("zone", "")
            if zone in ["SERVICE_HALL", "ANCHOR_STORE"]:
                delta += 0.5
            if action.get("time_in_zone", 0) > 120:
                delta += 0.3

        elif action_type == "interact":
            target = action.get("target", "")
            if "npc" in target.lower():
                delta += 0.8
            elif "artifact" in target.lower():
                delta += 1.5
                self._record_discovery(action)
            elif "log" in target.lower():
                delta += 2.0
                self._record_discovery(action)

        elif action_type == "run":
            delta += 0.2

        return delta

    def _calc_npc_pressure(self, events: Optional[List[Dict]]) -> float:
        """Calculate pressure change from NPC events."""
        if not events:
            return 0.0

        delta = 0.0

        for event in events:
            event_type = event.get("type", "")

            if event_type == "npc_interaction":
                delta += 0.3
                if event.get("conflict", False):
                    delta += 0.5

            elif event_type == "npc_state_change":
                if event.get("new_state") in ["alert", "suspicious", "hostile"]:
                    delta += 0.8

            elif event_type == "npc_contradiction":
                delta += 3.0
                self._record_contradiction(event)

        return delta

    def _calc_entity_pressure(self, action: Optional[Dict]) -> float:
        """
        Calculate pressure change from QBIT entity influence (NEW).

        Entities with high QBIT scores create "personality gravity" that
        affects local Cloud pressure based on player proximity and interaction.
        """
        if not action or not self.entities:
            return 0.0

        delta = 0.0
        current_zone = action.get("zone", "")

        if current_zone in self.zones:
            zone = self.zones[current_zone]

            # Zone QBIT aggregate creates base pressure
            # Scale: 0-6000 QBIT → 0-1.2 pressure delta per update
            delta += zone.qbit_aggregate * self.QBIT_PRESSURE_SCALE

            # Interaction with high-charisma entities increases pressure
            target = action.get("target", "")
            if target:
                entity = self.get_entity_by_id(target)
                if entity:
                    charisma = entity.get("computed", {}).get("charisma", 0)
                    # High-charisma entities draw attention, create tension
                    delta += (charisma / 3000) * 0.5

        return delta

    def _calc_drift_pressure(self, dt: float) -> float:
        """Calculate random drift pressure."""
        noise = random.uniform(-0.02, 0.03) * dt
        base_drift = 0.005 * dt
        return base_drift + noise

    def _apply_pressure_change(self, delta: float, dt: float):
        """Apply pressure change and update trend."""
        old_level = self.cloud_level
        self.cloud_level = max(0, min(100, self.cloud_level + delta))

        now = time.time()
        self._pressure_history.append((now, self.cloud_level))

        cutoff = now - 60
        self._pressure_history = [
            (t, l) for t, l in self._pressure_history if t > cutoff
        ]

        if len(self._pressure_history) >= 2:
            recent_change = self.cloud_level - self._pressure_history[0][1]
            if recent_change > 5:
                self.pressure_trend = PressureTrend.SPIKING
            elif recent_change > 1:
                self.pressure_trend = PressureTrend.RISING
            elif recent_change < -1:
                self.pressure_trend = PressureTrend.FALLING
            else:
                self.pressure_trend = PressureTrend.STABLE

    def _update_zones(self, dt: float, player_action: Optional[Dict]):
        """Update zone microstates with QBIT integration."""
        current_zone = None
        if player_action:
            current_zone = player_action.get("zone", "")

        for zone_id, zone in self.zones.items():
            self._relax_cloud(zone, dt)
            self._heal_qbit(zone, dt)

            drift_rate = self.ZONE_DRIFT_RATES.get(zone_id, 1.0)

            # Turbulence drifts toward global cloud level
            target_turbulence = (self.cloud_level / 100) * 10

            # QBIT INTEGRATION: Zone aggregate modifies turbulence
            qbit_turbulence_mod = zone.qbit_aggregate * self.QBIT_TURBULENCE_SCALE
            target_turbulence += qbit_turbulence_mod

            zone.turbulence += (target_turbulence - zone.turbulence) * 0.01 * dt * drift_rate

            # Player presence increases local turbulence
            if zone_id == current_zone:
                zone.turbulence += 0.1 * dt
                zone.last_player_visit = time.time()

            # Update swarm bias
            self._update_swarm_bias(zone)

    def _update_swarm_bias(self, zone: ZoneMicrostate):
        """Update swarm behavior weights for a zone."""
        zone.swarm_bias["color_weight"] = min(1.0, zone.turbulence / 8)

        if zone.turbulence < 3:
            zone.swarm_bias["clustering"] = zone.turbulence / 10
        elif zone.turbulence < 7:
            zone.swarm_bias["clustering"] = 0.3 + (zone.turbulence - 3) / 10
        else:
            zone.swarm_bias["clustering"] = 0.1

        zone.swarm_bias["speed"] = 1.0 + (zone.turbulence / 20)

        if zone.turbulence > 6:
            zone.swarm_bias["avoidance"] = ["SERVICE_HALL", "ANCHOR_STORE"]
        elif zone.turbulence > 4:
            zone.swarm_bias["avoidance"] = ["SERVICE_HALL"]
        else:
            zone.swarm_bias["avoidance"] = []

    def _update_mood(self):
        """Update global mood classification."""
        if self.cloud_level >= self.THRESHOLD_CRITICAL:
            self.mall_mood = MallMood.CRITICAL
        elif self.cloud_level >= self.THRESHOLD_STRAINED:
            self.mall_mood = MallMood.STRAINED
        elif self.cloud_level >= self.THRESHOLD_UNEASY:
            self.mall_mood = MallMood.UNEASY
        else:
            self.mall_mood = MallMood.CALM

    # ========== PASSIVE RECOVERY ==========

    def _relax_cloud(self, zone: ZoneMicrostate, dt: float, half_life_ticks: float = 300.0):
        """Exponential decay of local cloud pressure toward baseline calm."""
        decay_factor = 0.5 ** (dt / half_life_ticks)
        zone.cloud_pressure *= decay_factor

    def _heal_qbit(self, zone: ZoneMicrostate, dt: float, rate: float = 0.01):
        """Lerp QBIT aggregate back toward its baseline to recover coherence."""
        baseline = zone.qbit_baseline
        zone.qbit_aggregate += (baseline - zone.qbit_aggregate) * rate * dt

    def _apply_routing_overrides(self, adjacency_matrix: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        """Blend active routing overrides into the adjacency matrix."""
        effective = {
            zone_id: probs.copy()
            for zone_id, probs in adjacency_matrix.items()
        }

        touched_sources = set()
        for override in self.routing_overrides:
            if override.source_zone in effective:
                effective.setdefault(override.source_zone, {})[override.target_zone] = override.probability
                touched_sources.add(override.source_zone)

        # Renormalize any rows we modified so probabilities remain valid
        for source in touched_sources:
            row = effective.get(source, {})
            total = sum(row.values())
            if total > 0:
                for target in row:
                    row[target] /= total

        return effective

    def _update_routing_overrides(self, dt: float):
        """Decay routing overrides toward baseline by reducing TTL and removing expired ones."""
        if not self.routing_overrides:
            return

        before_count = len(self.routing_overrides)
        self.routing_overrides = [
            override for override in self.routing_overrides
            if (setattr(override, 'ttl', override.ttl - dt), override.ttl > 0)[1]
        ]

        if len(self.routing_overrides) != before_count:
            self._adjacency_overrides_dirty = True

    def add_routing_override(self, source_zone: str, target_zone: str, probability: float,
                             duration_ticks: float, reason: str = ""):
        """Register a temporary routing override with a TTL."""
        override = RoutingOverride(
            source_zone=source_zone,
            target_zone=target_zone,
            probability=probability,
            ttl=duration_ticks,
            reason=reason,
        )
        self.routing_overrides.append(override)
        self._adjacency_overrides_dirty = True

    # ========== RENDER HINTS ==========

    def _generate_render_hints(self) -> Dict:
        """Generate render hints for diegetic feedback."""
        hints = {
            "cloud_level": self.cloud_level,
            "mood": self.mall_mood.value,
            "trend": self.pressure_trend.value,
            "bleed_ready": self.bleed_threshold_reached,
            "bleed_tier": self.current_bleed_tier,
            "swarm": self._generate_swarm_hints(),
            "environment": self._generate_environment_hints(),
            "physics": self._generate_physics_hints(),
            "npc_modifiers": self._generate_npc_modifiers(),
            "zones": {
                zone_id: zone.to_dict()
                for zone_id, zone in self.zones.items()
            }
        }
        return hints

    def _generate_swarm_hints(self) -> Dict:
        """Generate swarm behavior hints."""
        level = self.cloud_level
        return {
            "color_uniformity": min(1.0, level / 60),
            "cluster_tendency": 0.3 if level < 40 else (0.6 if level < 70 else 0.1),
            "speed_multiplier": 1.0 + (level / 100) * 0.5,
            "freeze_chance": 0.0 if level < 70 else (level - 70) / 100,
            "scatter_threshold": level >= 85,
            "stare_intensity": max(0, (level - 50) / 50)
        }

    def _generate_environment_hints(self) -> Dict:
        """Generate environmental aesthetic hints."""
        level = self.cloud_level
        return {
            "flicker_intensity": min(1.0, level / 80),
            "color_temperature": 1.0 - (level / 200),
            "shadow_depth": 1.0 + (level / 100),
            "ambient_detune": level / 100,
            "hum_intensity": min(1.0, level / 60),
            "silence_pockets": level >= 40,
            "vhs_drag": max(0, (level - 50) / 100),
            "jpeg_artifacts": max(0, (level - 60) / 80),
            "color_banding": max(0, (level - 70) / 60),
            "perspective_drift": max(0, (level - 40) / 120)
        }

    def _generate_physics_hints(self) -> Dict:
        """Generate physics hints."""
        level = self.cloud_level
        if level < self.THRESHOLD_STRAINED:
            return {
                "tile_drift": False,
                "length_fluctuation": 0.0,
                "gravity_variance": 0.0
            }
        return {
            "tile_drift": level >= self.BLEED_TIER_2,
            "tile_drift_magnitude": max(0, (level - 60) / 200),
            "length_fluctuation": max(0, (level - 50) / 100),
            "gravity_variance": max(0, (level - 70) / 150)
        }

    def _generate_npc_modifiers(self) -> Dict:
        """
        Generate NPC behavior modifiers with QBIT integration.
        NOW: Contradiction thresholds scale with entity QBIT power.
        """
        level = self.cloud_level
        return {
            "dialogue_tension": level / 100,
            "patrol_deviation": min(0.5, level / 200),
            "reaction_speed": 1.0 + (level / 200),
            "spine_pressure": level / 100,
            "contradiction_ready": level >= self.THRESHOLD_CRITICAL,
            # QBIT INTEGRATION - NEW
            "qbit_power_threshold": self.QBIT_CONTRADICTION_THRESHOLD
        }

    # ========== ECHO SYSTEM ==========

    def _record_discovery(self, action: Dict):
        """Record a discovery with QBIT-modified resonance."""
        discovery = {
            "timestamp": time.time(),
            "type": action.get("type", ""),
            "target": action.get("target", ""),
            "zone": action.get("zone", ""),
            "cloud_level": self.cloud_level
        }
        self.discovery_history.append(discovery)

        zone_id = action.get("zone", "")
        if zone_id in self.zones:
            zone = self.zones[zone_id]

            # QBIT INTEGRATION: Resonance gain modified by zone charisma
            resonance_gain = 1.0
            if zone.qbit_charisma > 0:
                resonance_gain *= (1.0 + (zone.qbit_charisma / 3000) * self.QBIT_RESONANCE_MODIFIER)

            zone.resonance += resonance_gain
            zone.discovery_count += 1

    def _record_contradiction(self, event: Dict):
        """Record an NPC contradiction event."""
        contradiction = {
            "timestamp": time.time(),
            "npc_id": event.get("npc_id", ""),
            "broken_rule": event.get("broken_rule", ""),
            "cloud_level": self.cloud_level
        }
        self.npc_contradiction_log.append(contradiction)

    def get_artifact_weight(self, artifact_id: str) -> float:
        """
        Get canon weight of an artifact with QBIT integration.
        NOW: Uses QBIT charisma score instead of simple discovery count.
        """
        # Get entity if it exists
        entity = self.get_entity_by_id(artifact_id)
        if entity:
            charisma = entity.get("computed", {}).get("charisma", 0)
            # Scale charisma (0-3000) to weight (0-1.0)
            return min(1.0, charisma / 3000)

        # Fallback to discovery-based weight
        discoveries = [
            d for d in self.discovery_history
            if artifact_id in d.get("target", "")
        ]
        return min(1.0, len(discoveries) / 3)

    def get_zone_resonance(self, zone_id: str) -> float:
        """Get accumulated resonance for a zone."""
        if zone_id in self.zones:
            return self.zones[zone_id].resonance
        return 0.0

    def can_npc_contradict(self, npc_id: str) -> bool:
        """
        Check if NPC can perform contradiction (QBIT-aware).
        NPCs with high QBIT power can break rules at lower Cloud pressure.
        """
        if self.cloud_level < self.THRESHOLD_CRITICAL:
            # Below critical, check if NPC has exceptional power
            entity = self.get_entity_by_id(npc_id)
            if entity:
                power = entity.get("computed", {}).get("power", 0)
                # High-power entities (>2000) can contradict earlier
                if power > self.QBIT_CONTRADICTION_THRESHOLD:
                    return self.cloud_level >= (self.THRESHOLD_CRITICAL - 15)
            return False
        return True

    # ========== BLEED EVENT INTERFACE ==========

    def trigger_bleed_event(self, intensity: str = "minor") -> Dict:
        """Trigger a Bleed Event."""
        self.bleed_events_triggered += 1
        self.last_bleed_time = time.time()

        if intensity == "major":
            duration = random.uniform(60, 120)
            self.cloud_level = min(100, self.cloud_level + 10)
        else:
            duration = random.uniform(300, 720)
            self.cloud_level = min(100, self.cloud_level + 3)

        return {
            "type": "bleed_event",
            "intensity": intensity,
            "duration": duration,
            "cloud_level": self.cloud_level,
            "mood": self.mall_mood.value,
            "zones_affected": self._get_highest_turbulence_zones(3),
            "timestamp": time.time()
        }

    def _get_highest_turbulence_zones(self, count: int) -> List[str]:
        """Get zones with highest turbulence."""
        sorted_zones = sorted(
            self.zones.items(),
            key=lambda x: x[1].turbulence,
            reverse=True
        )
        return [zone_id for zone_id, _ in sorted_zones[:count]]

    # ========== PERSISTENCE ==========

    def save_state(self):
        """Save Cloud state to disk."""
        state = {
            "version": "6.0-qbit",
            "timestamp": time.time(),
            "cloud_level": self.cloud_level,
            "mall_mood": self.mall_mood.value,
            "bleed_threshold_reached": self.bleed_threshold_reached,
            "total_playtime": self.total_playtime,
            "session_count": self.session_count + 1,
            "bleed_events_triggered": self.bleed_events_triggered,
            "discovery_history": self.discovery_history[-100:],
            "npc_contradiction_log": self.npc_contradiction_log[-50:],
            "zones": {}
        }

        if self.cloud_level >= self.THRESHOLD_STRAINED:
            state["zones"] = {
                zone_id: zone.to_dict()
                for zone_id, zone in self.zones.items()
            }

        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        with open(self.save_path, 'w') as f:
            json.dump(state, f, indent=2)

        print(f"[CLOUD] State saved. Level: {self.cloud_level:.1f}, "
              f"Mood: {self.mall_mood.value}, Entities: {len(self.entities)}")

    def _load_state(self):
        """Load persisted Cloud state."""
        if not os.path.exists(self.save_path):
            print("[CLOUD] No saved state found. Starting fresh.")
            return

        try:
            with open(self.save_path, 'r') as f:
                state = json.load(f)

            self.cloud_level = state.get("cloud_level", 0.0)
            mood_value = state.get("mall_mood", "calm")
            self.mall_mood = MallMood(mood_value)
            self.bleed_threshold_reached = state.get("bleed_threshold_reached", False)
            self.total_playtime = state.get("total_playtime", 0.0)
            self.session_count = state.get("session_count", 0)
            self.bleed_events_triggered = state.get("bleed_events_triggered", 0)
            self.discovery_history = state.get("discovery_history", [])
            self.npc_contradiction_log = state.get("npc_contradiction_log", [])

            zones_data = state.get("zones", {})
            for zone_id, zone_data in zones_data.items():
                if zone_id in self.zones:
                    self.zones[zone_id] = ZoneMicrostate.from_dict(zone_data)

            print(f"[CLOUD] State loaded. Level: {self.cloud_level:.1f}, "
                  f"Mood: {self.mall_mood.value}, Sessions: {self.session_count}")

        except Exception as e:
            print(f"[CLOUD] Failed to load state: {e}")
            print("[CLOUD] Starting fresh.")

    def reset(self, keep_memory: bool = False):
        """Reset Cloud state."""
        self.cloud_level = 0.0
        self.pressure_trend = PressureTrend.STABLE
        self.mall_mood = MallMood.CALM
        self.bleed_threshold_reached = False

        for zone in self.zones.values():
            zone.turbulence = 0.0
            zone.swarm_bias = {
                "color_weight": 0.0,
                "clustering": 0.0,
                "speed": 1.0,
                "avoidance": []
            }

        if not keep_memory:
            self.discovery_history = []
            self.npc_contradiction_log = []
            for zone in self.zones.values():
                zone.resonance = 0.0
                zone.discovery_count = 0

        print(f"[CLOUD] Reset. Memory preserved: {keep_memory}")

    # ========== DEBUG TOOLS ==========

    def get_status(self) -> str:
        """Get human-readable status string."""
        entity_summary = f"Entities: {len(self.entities)}" if self.entities else "No entities loaded"

        return (
            f"Cloud Level: {self.cloud_level:.1f}/100\n"
            f"Mood: {self.mall_mood.value}\n"
            f"Trend: {self.pressure_trend.value}\n"
            f"Bleed Ready: {self.bleed_threshold_reached}\n"
            f"Sessions: {self.session_count}\n"
            f"Playtime: {self.total_playtime/60:.1f} min\n"
            f"Discoveries: {len(self.discovery_history)}\n"
            f"Contradictions: {len(self.npc_contradiction_log)}\n"
            f"{entity_summary}"
        )

    def force_pressure(self, level: float):
        """Force Cloud pressure to specific level (dev tool)."""
        self.cloud_level = max(0, min(100, level))
        self._update_mood()
        print(f"[CLOUD] Forced to {self.cloud_level:.1f}")


# ========== MODULE INTERFACE ==========

def create_cloud(save_path: Optional[str] = None, entities_path: Optional[str] = None) -> Cloud:
    """Factory function to create Cloud instance."""
    return Cloud(save_path=save_path, entities_path=entities_path)


if __name__ == "__main__":
    print("=" * 60)
    print("CLOUD STATE SYSTEM - V6 NextGen with QBIT Integration")
    print("=" * 60)

    cloud = Cloud()

    print("\nInitial state:")
    print(cloud.get_status())

    # Show QBIT zone stats
    if cloud.zone_qbit_cache:
        print("\nQBIT Zone Aggregates:")
        for zone_id, stats in cloud.zone_qbit_cache.items():
            if stats.get("entity_count", 0) > 0:
                print(f"  {zone_id}: {stats['entity_count']} entities, "
                      f"influence={stats['total_influence']}")

    # Test update
    print("\nTesting pressure buildup...")
    for i in range(50):
        action = {
            "type": "interact",
            "target": "leisurely-leon",
            "zone": "FC-ARCADE"
        }
        hints = cloud.update(0.1, player_action=action)

        if i % 10 == 0:
            print(f"  Tick {i}: Level={cloud.cloud_level:.1f}, "
                  f"Mood={cloud.mall_mood.value}")

    print("\nFinal state:")
    print(cloud.get_status())

    print("\n✓ QBIT-integrated Cloud system test complete")
