#!/usr/bin/env python3
"""
CLOUD STATE SYSTEM - V4 Renderist Mall OS

The Cloud is the global state machine driving all mall behavior.
"The mall remembers vibes, not details."

Architecture:
- Global Cloud: Mall-wide mood/metaphysical pressure
- Zone Microstates: Local turbulence pockets
- Pure diegetic feedback (no UI meters)
- Hard memory across sessions (vibes persist)

Driver Weights:
- Player actions: 0.6 (primary driver)
- NPC interactions: 0.3 (adds texture)
- Ambient conditions: 0.1 (slow drift)
"""

import json
import os
import time
import random
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


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
class ZoneMicrostate:
    """Local turbulence pocket for a specific zone."""
    zone_id: str
    turbulence: float = 0.0          # 0-10 scale
    resonance: float = 0.0           # Echo accumulation from discoveries
    swarm_bias: Dict = field(default_factory=lambda: {
        "color_weight": 0.0,         # How beige the crowd (-1 to 1)
        "clustering": 0.0,           # How much they cluster (0-1)
        "speed": 1.0,                # Movement speed multiplier
        "avoidance": []              # Zones customers avoid
    })
    last_player_visit: float = 0.0   # Timestamp
    discovery_count: int = 0         # AO3 logs found here
    last_contradiction_time: float = 0.0  # For zone cooldown (LOCKED: 30 sec)

    def to_dict(self) -> Dict:
        return {
            "zone_id": self.zone_id,
            "turbulence": self.turbulence,
            "resonance": self.resonance,
            "swarm_bias": self.swarm_bias,
            "last_player_visit": self.last_player_visit,
            "discovery_count": self.discovery_count
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ZoneMicrostate':
        state = cls(zone_id=data["zone_id"])
        state.turbulence = data.get("turbulence", 0.0)
        state.resonance = data.get("resonance", 0.0)
        state.swarm_bias = data.get("swarm_bias", state.swarm_bias)
        state.last_player_visit = data.get("last_player_visit", 0.0)
        state.discovery_count = data.get("discovery_count", 0)
        return state


class Cloud:
    """
    Global Cloud State - The soul of the mall.

    The Cloud drives all behavior through:
    - Global pressure level (0-100)
    - Mood classification
    - Zone microstates
    - Persistence across sessions

    Pure diegetic feedback - no UI. Read the swarm, read the vibe.
    """

    # Driver weights (locked in from alignment)
    # 50% player discovery, 25% NPC stress, 15% drift, 10% other
    WEIGHT_PLAYER = 0.50
    WEIGHT_NPC = 0.25
    WEIGHT_DRIFT = 0.15
    WEIGHT_OTHER = 0.10

    # Mood thresholds (calm/uneasy/strained/critical)
    THRESHOLD_UNEASY = 25
    THRESHOLD_STRAINED = 50
    THRESHOLD_CRITICAL = 75

    # Bleed tiers
    BLEED_TIER_1 = 75   # Visual/Audio only
    BLEED_TIER_2 = 80   # Visual + NPC contradictions
    BLEED_TIER_3 = 90   # Visual + NPC + Space effects

    # LOCKED DECISIONS (from alignment session)
    CLOUD_UPDATE_INTERVAL = 10           # frames - Cloud updates every 10 frames
    ZONE_CONTRADICTION_COOLDOWN = 30.0   # seconds between contradictions in same zone
    MAX_SWARM_CONTRIBUTION = 0.05        # 5% cap on swarm feedback
    BLEED_WINDDOWN_TIME = 7.5            # seconds for Bleed to fade when Cloud drops

    # Zone behavior modifiers
    ZONE_DRIFT_RATES = {
        "FOOD_COURT": 1.5,        # Always drifts faster
        "SERVICE_HALL": 1.3,      # Goes weird first
        "STORE_BORED": 0.7,       # Unusually stable
        "STORE_HARD_COPY": 1.2,   # Slight instability
        "ANCHOR_STORE": 1.0,      # Baseline
        "CORRIDOR": 0.9,          # Slightly stable
    }

    def __init__(self, save_path: Optional[str] = None):
        """Initialize Cloud state."""
        self.save_path = save_path or self._default_save_path()

        # Global Cloud variables
        self.cloud_level: float = 0.0           # 0-100
        self.pressure_trend: PressureTrend = PressureTrend.STABLE
        self.mall_mood: MallMood = MallMood.CALM
        self.bleed_threshold_reached: bool = False

        # Session tracking
        self.session_start: float = time.time()
        self.total_playtime: float = 0.0        # Accumulated across sessions
        self.session_count: int = 0

        # Zone microstates
        self.zones: Dict[str, ZoneMicrostate] = {}
        self._init_zones()

        # Event history (for Echo system)
        self.discovery_history: List[Dict] = []
        self.npc_contradiction_log: List[Dict] = []

        # Bleed event tracking
        self.bleed_events_triggered: int = 0
        self.last_bleed_time: float = 0.0
        self.current_bleed_tier: int = 0  # 0=none, 1=visual, 2=+NPC, 3=+space

        # Pressure change tracking (for trend calculation)
        self._pressure_history: List[Tuple[float, float]] = []  # (timestamp, level)

        # Load persisted state if exists
        self._load_state()

    def _default_save_path(self) -> str:
        """Get default save path for Cloud state."""
        return os.path.join(
            os.path.dirname(__file__), '..', 'data', 'cloud_state.json'
        )

    def _init_zones(self):
        """Initialize zone microstates."""
        default_zones = [
            "FOOD_COURT",
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

    # ========== UPDATE SYSTEM ==========

    def update(self, dt: float, player_action: Optional[Dict] = None,
               npc_events: Optional[List[Dict]] = None) -> Dict:
        """
        Main update loop - call every frame.

        Args:
            dt: Delta time in seconds
            player_action: Current player action dict
            npc_events: List of NPC interaction events

        Returns:
            Render hints dict for diegetic feedback
        """
        # Update playtime
        self.total_playtime += dt

        # Calculate pressure changes from each driver
        # 50% player discovery, 25% NPC stress, 15% drift, 10% other
        player_delta = self._calc_player_pressure(player_action) * self.WEIGHT_PLAYER
        npc_delta = self._calc_npc_pressure(npc_events) * self.WEIGHT_NPC
        drift_delta = self._calc_drift_pressure(dt) * self.WEIGHT_DRIFT
        other_delta = self._calc_other_pressure(player_action, dt) * self.WEIGHT_OTHER

        # Apply total pressure change
        total_delta = player_delta + npc_delta + drift_delta + other_delta
        self._apply_pressure_change(total_delta, dt)

        # Update zone microstates
        self._update_zones(dt, player_action)

        # Update mood classification
        self._update_mood()

        # Check for bleed threshold (tiered system)
        if self.cloud_level >= self.BLEED_TIER_1 and not self.bleed_threshold_reached:
            self.bleed_threshold_reached = True
            self.bleed_events_triggered += 1
            self.last_bleed_time = time.time()

        # Determine current bleed tier for render hints
        if self.cloud_level >= self.BLEED_TIER_3:
            self.current_bleed_tier = 3
        elif self.cloud_level >= self.BLEED_TIER_2:
            self.current_bleed_tier = 2
        elif self.cloud_level >= self.BLEED_TIER_1:
            self.current_bleed_tier = 1
        else:
            self.current_bleed_tier = 0

        # Generate render hints (diegetic feedback)
        return self._generate_render_hints()

    def _calc_player_pressure(self, action: Optional[Dict]) -> float:
        """Calculate pressure change from player action."""
        if not action:
            return 0.0

        delta = 0.0
        action_type = action.get("type", "")

        # Movement patterns
        if action_type == "move":
            zone = action.get("zone", "")
            # Entering restricted areas increases pressure
            if zone in ["SERVICE_HALL", "ANCHOR_STORE"]:
                delta += 0.5
            # Lingering in one zone too long
            if action.get("time_in_zone", 0) > 120:  # 2 minutes
                delta += 0.3

        # Interactions
        elif action_type == "interact":
            target = action.get("target", "")
            # NPC interactions - depends on NPC state
            if "npc" in target.lower():
                delta += 0.8
            # Artifact pickup
            elif "artifact" in target.lower():
                delta += 1.5
                self._record_discovery(action)
            # AO3 log discovery
            elif "log" in target.lower():
                delta += 2.0
                self._record_discovery(action)

        # Running/sprinting increases pressure
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

            # NPC-to-NPC interactions
            if event_type == "npc_interaction":
                delta += 0.3
                # Conflict increases pressure more
                if event.get("conflict", False):
                    delta += 0.5

            # NPC state changes
            elif event_type == "npc_state_change":
                # Alert states increase pressure
                if event.get("new_state") in ["alert", "suspicious", "hostile"]:
                    delta += 0.8

            # NPC contradiction (spine break)
            elif event_type == "npc_contradiction":
                delta += 3.0
                self._record_contradiction(event)

        return delta

    def _calc_drift_pressure(self, dt: float) -> float:
        """
        Calculate random drift pressure (15% of total).
        Tiny background noise so Cloud never sits perfectly still.
        Keeps the world from feeling clockwork.
        """
        # Random micro-fluctuations - the mall breathes
        noise = random.uniform(-0.02, 0.03) * dt

        # Very slow base drift upward (entropy)
        base_drift = 0.005 * dt

        return base_drift + noise

    def _calc_other_pressure(self, action: Optional[Dict], dt: float) -> float:
        """
        Calculate other pressure sources (10% of total).
        - Time in high-risk zones
        - Accumulated resonance
        - Session length fatigue
        """
        delta = 0.0

        # Accumulated resonance creates upward pressure
        total_resonance = sum(z.resonance for z in self.zones.values())
        resonance_pressure = (total_resonance / 100) * 0.02 * dt
        delta += resonance_pressure

        # Time in high-risk zones
        if action:
            zone = action.get("zone", "")
            if zone in ["SERVICE_HALL", "ANCHOR_STORE"]:
                time_in_zone = action.get("time_in_zone", 0)
                if time_in_zone > 60:  # Over 1 minute
                    delta += 0.1 * dt

        # Long session fatigue (very subtle)
        if self.total_playtime > 1800:  # 30+ minutes
            delta += 0.01 * dt

        return delta

    def _apply_pressure_change(self, delta: float, dt: float):
        """Apply pressure change and update trend."""
        old_level = self.cloud_level

        # Apply change with bounds
        self.cloud_level = max(0, min(100, self.cloud_level + delta))

        # Record for trend calculation
        now = time.time()
        self._pressure_history.append((now, self.cloud_level))

        # Keep only last 60 seconds of history
        cutoff = now - 60
        self._pressure_history = [
            (t, l) for t, l in self._pressure_history if t > cutoff
        ]

        # Calculate trend
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
        """Update zone microstates."""
        current_zone = None
        if player_action:
            current_zone = player_action.get("zone", "")

        for zone_id, zone in self.zones.items():
            # Get drift rate for this zone
            drift_rate = self.ZONE_DRIFT_RATES.get(zone_id, 1.0)

            # Turbulence drifts toward global cloud level
            target_turbulence = (self.cloud_level / 100) * 10
            zone.turbulence += (target_turbulence - zone.turbulence) * 0.01 * dt * drift_rate

            # Player presence increases local turbulence
            if zone_id == current_zone:
                zone.turbulence += 0.1 * dt
                zone.last_player_visit = time.time()

            # Update swarm bias based on turbulence
            self._update_swarm_bias(zone)

    def _update_swarm_bias(self, zone: ZoneMicrostate):
        """Update swarm behavior weights for a zone."""
        # Color weight: higher turbulence = more beige (uniform)
        zone.swarm_bias["color_weight"] = min(1.0, zone.turbulence / 8)

        # Clustering: moderate turbulence = more clustering
        if zone.turbulence < 3:
            zone.swarm_bias["clustering"] = zone.turbulence / 10
        elif zone.turbulence < 7:
            zone.swarm_bias["clustering"] = 0.3 + (zone.turbulence - 3) / 10
        else:
            zone.swarm_bias["clustering"] = 0.1  # They scatter at high turbulence

        # Speed: higher turbulence = faster, more erratic
        zone.swarm_bias["speed"] = 1.0 + (zone.turbulence / 20)

        # Avoidance: at high turbulence, customers avoid high-pressure zones
        if zone.turbulence > 6:
            zone.swarm_bias["avoidance"] = ["SERVICE_HALL", "ANCHOR_STORE"]
        elif zone.turbulence > 4:
            zone.swarm_bias["avoidance"] = ["SERVICE_HALL"]
        else:
            zone.swarm_bias["avoidance"] = []

    def _update_mood(self):
        """Update global mood classification based on cloud level."""
        if self.cloud_level >= self.THRESHOLD_CRITICAL:
            self.mall_mood = MallMood.CRITICAL
        elif self.cloud_level >= self.THRESHOLD_STRAINED:
            self.mall_mood = MallMood.STRAINED
        elif self.cloud_level >= self.THRESHOLD_UNEASY:
            self.mall_mood = MallMood.UNEASY
        else:
            self.mall_mood = MallMood.CALM

    # ========== RENDER HINTS (DIEGETIC FEEDBACK) ==========

    def _generate_render_hints(self) -> Dict:
        """
        Generate render hints for diegetic feedback.
        No UI - the swarm and environment ARE the feedback.
        """
        hints = {
            # Global state (for systems that need it)
            "cloud_level": self.cloud_level,
            "mood": self.mall_mood.value,
            "trend": self.pressure_trend.value,
            "bleed_ready": self.bleed_threshold_reached,
            "bleed_tier": self.current_bleed_tier,  # 0=none, 1=visual, 2=+NPC, 3=+space

            # Swarm behavior (the crowd tells the story)
            "swarm": self._generate_swarm_hints(),

            # Environmental (aesthetics first)
            "environment": self._generate_environment_hints(),

            # Physics (only at high cloud)
            "physics": self._generate_physics_hints(),

            # NPC behavior modifiers
            "npc_modifiers": self._generate_npc_modifiers(),

            # Zone states
            "zones": {
                zone_id: zone.to_dict()
                for zone_id, zone in self.zones.items()
            }
        }

        return hints

    def _generate_swarm_hints(self) -> Dict:
        """Generate swarm behavior hints - the crowd is the weather."""
        level = self.cloud_level

        return {
            # Color uniformity (0 = varied, 1 = all beige)
            "color_uniformity": min(1.0, level / 60),

            # Clustering behavior
            "cluster_tendency": 0.3 if level < 40 else (0.6 if level < 70 else 0.1),

            # Movement speed (1.0 = normal)
            "speed_multiplier": 1.0 + (level / 100) * 0.5,

            # Freeze probability (momentary stare at high levels)
            "freeze_chance": 0.0 if level < 70 else (level - 70) / 100,

            # Scatter trigger (customers flee)
            "scatter_threshold": level >= 85,

            # Stare behavior (customers look at player)
            "stare_intensity": max(0, (level - 50) / 50)
        }

    def _generate_environment_hints(self) -> Dict:
        """Generate environmental aesthetic hints."""
        level = self.cloud_level

        return {
            # Lighting
            "flicker_intensity": min(1.0, level / 80),
            "color_temperature": 1.0 - (level / 200),  # Cooler at high pressure
            "shadow_depth": 1.0 + (level / 100),

            # Audio
            "ambient_detune": level / 100,  # How off-pitch ambient sounds are
            "hum_intensity": min(1.0, level / 60),
            "silence_pockets": level >= 40,  # Zones of unnatural quiet

            # Visual artifacts (at higher levels)
            "vhs_drag": max(0, (level - 50) / 100),
            "jpeg_artifacts": max(0, (level - 60) / 80),
            "color_banding": max(0, (level - 70) / 60),

            # Spatial
            "perspective_drift": max(0, (level - 40) / 120)
        }

    def _generate_physics_hints(self) -> Dict:
        """
        Generate physics hints - only at high cloud.
        Aesthetics first, physics second.
        """
        level = self.cloud_level

        # No physics changes below STRESSED
        if level < self.THRESHOLD_STRAINED:
            return {
                "tile_drift": False,
                "length_fluctuation": 0.0,
                "gravity_variance": 0.0
            }

        return {
            # Tile position drift (mild)
            "tile_drift": level >= self.BLEED_TIER_2,
            "tile_drift_magnitude": max(0, (level - 60) / 200),

            # Hallway length fluctuation
            "length_fluctuation": max(0, (level - 50) / 100),

            # Subtle gravity variance (things feel heavier/lighter)
            "gravity_variance": max(0, (level - 70) / 150)
        }

    def _generate_npc_modifiers(self) -> Dict:
        """Generate NPC behavior modifiers based on cloud state."""
        level = self.cloud_level

        return {
            # Dialogue selection
            "dialogue_tension": level / 100,

            # Movement patterns
            "patrol_deviation": min(0.5, level / 200),

            # Responsiveness
            "reaction_speed": 1.0 + (level / 200),

            # Spine pressure (for contradiction system)
            "spine_pressure": level / 100,

            # Contradiction threshold (when NPCs break their "never" rules)
            "contradiction_ready": level >= self.THRESHOLD_CRITICAL
        }

    # ========== ECHO SYSTEM (CANON MEMORY) ==========

    def _record_discovery(self, action: Dict):
        """Record a discovery for the Echo system."""
        discovery = {
            "timestamp": time.time(),
            "type": action.get("type", ""),
            "target": action.get("target", ""),
            "zone": action.get("zone", ""),
            "cloud_level": self.cloud_level
        }
        self.discovery_history.append(discovery)

        # Update zone resonance
        zone_id = action.get("zone", "")
        if zone_id in self.zones:
            self.zones[zone_id].resonance += 1.0
            self.zones[zone_id].discovery_count += 1

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
        """Get the canon weight of an artifact based on discoveries."""
        discoveries = [
            d for d in self.discovery_history
            if artifact_id in d.get("target", "")
        ]
        # More discoveries = higher weight
        return min(1.0, len(discoveries) / 3)

    def get_zone_resonance(self, zone_id: str) -> float:
        """Get accumulated resonance for a zone."""
        if zone_id in self.zones:
            return self.zones[zone_id].resonance
        return 0.0

    # ========== BLEED EVENT INTERFACE ==========

    def trigger_bleed_event(self, intensity: str = "minor") -> Dict:
        """
        Trigger a Bleed Event.

        Args:
            intensity: "minor" (drift) or "major" (warp)

        Returns:
            Bleed event configuration for SORA/renderer
        """
        self.bleed_events_triggered += 1
        self.last_bleed_time = time.time()

        if intensity == "major":
            # Warp bleed - rare, max 2 minutes
            duration = random.uniform(60, 120)
            self.cloud_level = min(100, self.cloud_level + 10)
        else:
            # Drift bleed - 5-12 minutes
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
        """Get the zones with highest turbulence."""
        sorted_zones = sorted(
            self.zones.items(),
            key=lambda x: x[1].turbulence,
            reverse=True
        )
        return [zone_id for zone_id, _ in sorted_zones[:count]]

    # ========== PERSISTENCE ==========

    def save_state(self):
        """Save Cloud state to disk - mall remembers vibes."""
        state = {
            "version": "4.0",
            "timestamp": time.time(),

            # Global cloud (always saved)
            "cloud_level": self.cloud_level,
            "mall_mood": self.mall_mood.value,
            "bleed_threshold_reached": self.bleed_threshold_reached,

            # Session tracking
            "total_playtime": self.total_playtime,
            "session_count": self.session_count + 1,
            "bleed_events_triggered": self.bleed_events_triggered,

            # Echo system (canon memory)
            "discovery_history": self.discovery_history[-100:],  # Keep last 100
            "npc_contradiction_log": self.npc_contradiction_log[-50:],

            # Zone microstates (saved only if cloud is high)
            "zones": {}
        }

        # Only save zone microstates if significant pressure
        if self.cloud_level >= self.THRESHOLD_STRAINED:
            state["zones"] = {
                zone_id: zone.to_dict()
                for zone_id, zone in self.zones.items()
            }

        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

        with open(self.save_path, 'w') as f:
            json.dump(state, f, indent=2)

        print(f"[CLOUD] State saved. Level: {self.cloud_level:.1f}, Mood: {self.mall_mood.value}")

    def _load_state(self):
        """Load persisted Cloud state if it exists."""
        if not os.path.exists(self.save_path):
            print("[CLOUD] No saved state found. Starting fresh.")
            return

        try:
            with open(self.save_path, 'r') as f:
                state = json.load(f)

            # Restore global cloud
            self.cloud_level = state.get("cloud_level", 0.0)
            mood_value = state.get("mall_mood", "neutral")
            self.mall_mood = MallMood(mood_value)
            self.bleed_threshold_reached = state.get("bleed_threshold_reached", False)

            # Restore session tracking
            self.total_playtime = state.get("total_playtime", 0.0)
            self.session_count = state.get("session_count", 0)
            self.bleed_events_triggered = state.get("bleed_events_triggered", 0)

            # Restore echo system
            self.discovery_history = state.get("discovery_history", [])
            self.npc_contradiction_log = state.get("npc_contradiction_log", [])

            # Restore zone microstates if present
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
        """
        Reset Cloud state.

        Args:
            keep_memory: If True, preserve discovery history (soft reset)
        """
        self.cloud_level = 0.0
        self.pressure_trend = PressureTrend.STABLE
        self.mall_mood = MallMood.NEUTRAL
        self.bleed_threshold_reached = False

        # Reset zones
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

    # ========== DEBUG / DEV TOOLS ==========

    def get_status(self) -> str:
        """Get human-readable status string (for dev tools only)."""
        return (
            f"Cloud Level: {self.cloud_level:.1f}/100\n"
            f"Mood: {self.mall_mood.value}\n"
            f"Trend: {self.pressure_trend.value}\n"
            f"Bleed Ready: {self.bleed_threshold_reached}\n"
            f"Sessions: {self.session_count}\n"
            f"Playtime: {self.total_playtime/60:.1f} min\n"
            f"Discoveries: {len(self.discovery_history)}\n"
            f"Contradictions: {len(self.npc_contradiction_log)}"
        )

    def force_pressure(self, level: float):
        """Force Cloud pressure to specific level (dev tool)."""
        self.cloud_level = max(0, min(100, level))
        self._update_mood()
        print(f"[CLOUD] Forced to {self.cloud_level:.1f}")


# ========== MODULE INTERFACE ==========

def create_cloud(save_path: Optional[str] = None) -> Cloud:
    """Factory function to create Cloud instance."""
    return Cloud(save_path=save_path)


if __name__ == "__main__":
    # Test Cloud system
    print("=" * 60)
    print("CLOUD STATE SYSTEM - V4 Renderist Mall OS")
    print("=" * 60)

    cloud = Cloud()

    print("\nInitial state:")
    print(cloud.get_status())

    # Simulate some updates
    print("\nSimulating pressure buildup...")
    for i in range(100):
        action = {
            "type": "interact",
            "target": "artifact_test",
            "zone": "FOOD_COURT"
        }
        hints = cloud.update(0.1, player_action=action)

        if i % 20 == 0:
            print(f"  Tick {i}: Level={cloud.cloud_level:.1f}, "
                  f"Mood={cloud.mall_mood.value}")

    print("\nFinal state:")
    print(cloud.get_status())

    print("\nSwarm hints:")
    for key, value in hints["swarm"].items():
        print(f"  {key}: {value}")

    print("\nEnvironment hints:")
    for key, value in hints["environment"].items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    # Save state
    cloud.save_state()
    print("\nCloud state saved.")
