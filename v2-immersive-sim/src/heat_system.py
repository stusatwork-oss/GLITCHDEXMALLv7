"""
HEAT SYSTEM - GTA-Style Wanted Level
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GTA/Far Cry wanted stars... but at max heat, the SIMULATION BREAKS.

Heat Level 0: Normal mall
Heat Level 1: Security is watching
Heat Level 2: Active pursuit
Heat Level 3: Lockdown procedures
Heat Level 4: Full lockdown
Heat Level 5: REALITY FAILURE - The modern engine bleeds through
                The AI pathfinding becomes VISIBLE
                You see the actual GTA/Far Cry systems underneath
                The Wolf3D mask SHATTERS

This is the showpiece - where cutting-edge 2025 rendering
leaks through the 50-cent Halloween mask.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import time
import random
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class HeatLevel(Enum):
    """GTA-style heat levels"""
    NONE = 0  # ☆☆☆☆☆
    LOW = 1  # ★☆☆☆☆
    MEDIUM = 2  # ★★☆☆☆
    HIGH = 3  # ★★★☆☆
    CRITICAL = 4  # ★★★★☆
    REALITY_BREAK = 5  # ★★★★★  THE MASK SLIPS


@dataclass
class HeatEvent:
    """An action that affects heat"""
    timestamp: float
    event_type: str
    heat_value: float
    location: Tuple[int, int, int]


class HeatSystem:
    """
    GTA-style wanted system that BREAKS REALITY at max level.

    At Heat 5, the simulation can't maintain the facade anymore.
    Modern rendering systems bleed through. GenAlpha sees the real engine.
    """

    def __init__(self):
        self.current_heat = 0.0  # 0.0 to 5.0 (continuous for smooth transitions)
        self.heat_decay_rate = 0.05  # Heat per second when hidden
        self.heat_increase_rate_when_visible = 0.1

        # Event history
        self.recent_events: List[HeatEvent] = []

        # State tracking
        self.time_since_last_incident = 0.0
        self.player_in_restricted_zone = False
        self.lockdown_active = False

        # Reality break state
        self.reality_stability = 100.0  # 100 = stable, 0 = complete breakdown
        self.glitch_intensity = 0.0  # 0.0 to 1.0

        # Heat thresholds for escalation
        self.thresholds = {
            HeatLevel.NONE: 0.0,
            HeatLevel.LOW: 1.0,
            HeatLevel.MEDIUM: 2.0,
            HeatLevel.HIGH: 3.0,
            HeatLevel.CRITICAL: 4.0,
            HeatLevel.REALITY_BREAK: 4.8
        }

    def add_heat(self, amount: float, event_type: str, location: Tuple[int, int, int]):
        """Add heat from player action"""
        self.current_heat = min(5.0, self.current_heat + amount)

        # Record event
        event = HeatEvent(
            timestamp=time.time(),
            event_type=event_type,
            heat_value=amount,
            location=location
        )
        self.recent_events.append(event)

        # Reset incident timer
        self.time_since_last_incident = 0.0

        # At high heat, reality becomes unstable
        if self.current_heat >= self.thresholds[HeatLevel.CRITICAL]:
            self.reality_stability -= amount * 10
            self.reality_stability = max(0.0, self.reality_stability)

    def update(self, dt: float, player_detected: bool, player_in_restricted: bool):
        """Update heat system"""
        self.time_since_last_incident += dt

        # Store restricted zone status
        self.player_in_restricted_zone = player_in_restricted

        # If player is detected, heat increases
        if player_detected:
            self.current_heat += self.heat_increase_rate_when_visible * dt
            self.current_heat = min(5.0, self.current_heat)
        else:
            # Heat decays when hidden
            if self.time_since_last_incident > 5.0:  # Cool down period
                self.current_heat -= self.heat_decay_rate * dt
                self.current_heat = max(0.0, self.current_heat)

        # Restricted zone generates passive heat
        if player_in_restricted and not self.lockdown_active:
            self.current_heat += 0.02 * dt

        # Update reality stability
        if self.current_heat >= self.thresholds[HeatLevel.REALITY_BREAK]:
            # Reality is breaking down
            self.reality_stability -= 1.0 * dt
            self.glitch_intensity = 1.0 - (self.reality_stability / 100.0)
        elif self.current_heat < self.thresholds[HeatLevel.HIGH]:
            # Reality stabilizes at lower heat
            self.reality_stability += 0.5 * dt
            self.reality_stability = min(100.0, self.reality_stability)
            self.glitch_intensity = max(0.0, 1.0 - (self.reality_stability / 100.0))

        # Update lockdown state
        if self.current_heat >= self.thresholds[HeatLevel.CRITICAL]:
            self.lockdown_active = True
        elif self.current_heat < self.thresholds[HeatLevel.MEDIUM]:
            self.lockdown_active = False

        # Purge old events
        current_time = time.time()
        self.recent_events = [
            e for e in self.recent_events
            if current_time - e.timestamp < 60.0  # Keep last minute
        ]

    def get_heat_level(self) -> HeatLevel:
        """Get current heat level enum"""
        for level in reversed(HeatLevel):
            if self.current_heat >= self.thresholds[level]:
                return level
        return HeatLevel.NONE

    def get_heat_value(self) -> float:
        """Get raw heat value (0.0 to 5.0)"""
        return self.current_heat

    def is_lockdown_active(self) -> bool:
        """Check if mall is in lockdown"""
        return self.lockdown_active

    def is_reality_breaking(self) -> bool:
        """Check if we're in reality break state"""
        return self.current_heat >= self.thresholds[HeatLevel.REALITY_BREAK]

    def get_reality_stability(self) -> float:
        """Get reality stability (0-100, lower = more broken)"""
        return self.reality_stability

    def get_glitch_intensity(self) -> float:
        """Get how intense reality glitches should be (0.0 to 1.0)"""
        return self.glitch_intensity

    def get_npc_spawn_multiplier(self) -> float:
        """How many more NPCs should spawn based on heat"""
        level = self.get_heat_level()

        multipliers = {
            HeatLevel.NONE: 1.0,
            HeatLevel.LOW: 1.2,
            HeatLevel.MEDIUM: 1.5,
            HeatLevel.HIGH: 2.0,
            HeatLevel.CRITICAL: 3.0,
            HeatLevel.REALITY_BREAK: 4.0  # Tons of NPCs during reality break
        }

        return multipliers.get(level, 1.0)

    def get_escalation_description(self) -> str:
        """Get text description of current heat state"""
        level = self.get_heat_level()

        descriptions = {
            HeatLevel.NONE: "All quiet. Mall is normal.",
            HeatLevel.LOW: "Security has noticed you. They're watching.",
            HeatLevel.MEDIUM: "Active pursuit. Security is searching for you.",
            HeatLevel.HIGH: "Mall lockdown procedures initiated.",
            HeatLevel.CRITICAL: "FULL LOCKDOWN. Exits sealed. Heavy security presence.",
            HeatLevel.REALITY_BREAK: "[SIMULATION FAILURE] THE MASK IS SLIPPING. YOU SEE THE REAL ENGINE."
        }

        return descriptions.get(level, "")

    def get_reality_break_effects(self) -> Dict[str, Any]:
        """
        Get rendering effects for reality break.

        At Heat 5, we reveal the REAL simulation:
        - Modern AI pathfinding visualization
        - Nav mesh display
        - Real-time lighting calculations
        - Actual poly counts
        - System profiler overlay
        - 1080p photorealistic leaks
        """
        if not self.is_reality_breaking():
            return {}

        intensity = self.glitch_intensity

        return {
            # Visual glitches
            "show_nav_mesh": intensity > 0.3,
            "show_pathfinding_lines": intensity > 0.4,
            "show_ai_decision_trees": intensity > 0.5,
            "show_vision_cones": intensity > 0.6,
            "show_physics_debug": intensity > 0.7,
            "show_profiler": intensity > 0.8,
            "photorealistic_leak_intensity": intensity,

            # Text overlays (fake engine debug)
            "show_modern_engine_ui": intensity > 0.5,
            "engine_stats": self._generate_engine_stats() if intensity > 0.5 else {},

            # Reality cracks
            "wireframe_blend": min(0.5, intensity),
            "modern_lighting": intensity,
            "hd_texture_bleed": intensity,
        }

    def _generate_engine_stats(self) -> Dict[str, str]:
        """Generate fake modern engine statistics that appear during reality break"""
        return {
            "ENGINE": "Unreal Engine 5.3.2 / Unity 2023.2",
            "RENDERER": "Forward+ / Deferred PBR",
            "RESOLUTION": "1920x1080 @ 60Hz",
            "DRAWCALLS": f"{random.randint(2000, 5000)} (batched: {random.randint(1500, 4000)})",
            "TRIANGLES": f"{random.randint(100000, 500000):,}",
            "VRAM": f"{random.randint(1800, 3400)} MB / 8192 MB",
            "AI_AGENTS": f"{random.randint(40, 120)} active",
            "PATHFINDING": "Recast/Detour Nav Mesh",
            "PHYSICS": "PhysX 5.0 / Bullet",
            "LIGHTING": "Ray Traced GI + Lumen",
            "SHADOWS": "PCF 5x5 + Contact Shadows",
            "POST_FX": "TAA + Bloom + SSAO + DOF",
            "TARGET_FPS": "60",
            "CURRENT_FPS": f"{random.randint(55, 62)}",
            "_separator1": "",
            "_header1": "=== SIMULATION STATUS ===",
            "FACADE_INTEGRITY": f"{int(self.reality_stability)}%",
            "WOLF3D_MASK": "FAILING" if self.glitch_intensity > 0.7 else "COMPROMISED",
            "HEAT_LEVEL": f"{self.current_heat:.1f}/5.0",
            "REALITY_STABLE": "FALSE",
            "_separator2": "",
            "_error1": "[ERROR] Cannot maintain retro facade",
            "_warning1": "[WARNING] Modern rendering exposed",
            "_critical1": "[CRITICAL] Simulation integrity compromised"
        }

    def get_hud_display(self) -> str:
        """Get HUD representation of heat (like GTA stars)"""
        level = self.get_heat_level()

        if self.is_reality_breaking():
            # Reality break shows glitched stars
            return "★★★★★ [SIMULATION FAILURE]"

        stars_filled = int(self.current_heat)
        stars_empty = 5 - stars_filled

        return ("★" * stars_filled) + ("☆" * stars_empty)

    def get_ambient_chaos_level(self) -> float:
        """How chaotic the mall should feel (0.0 to 1.0)"""
        return min(1.0, self.current_heat / 5.0)

    # Action heat values
    HEAT_VALUES = {
        "trespass_minor": 0.2,
        "trespass_major": 0.5,
        "vandalism": 0.4,
        "attack_npc": 1.0,
        "destroy_property": 0.6,
        "trigger_alarm": 0.8,
        "seen_in_restricted": 0.3,
        "escape_security": -0.5,  # Negative heat
        "hide_successfully": -0.3
    }

    def trigger_event(self, event_type: str, location: Tuple[int, int, int]):
        """Trigger a heat event by type"""
        heat_amount = self.HEAT_VALUES.get(event_type, 0.1)
        self.add_heat(heat_amount, event_type, location)
