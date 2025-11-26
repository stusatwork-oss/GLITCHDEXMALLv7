"""
REALITY GLITCH SYSTEM - Micro-Glitches Before The Mask Shatters
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The mask doesn't break instantly at Heat 5.
It CRACKS at Heat 3. It STRAINS at Heat 4.

Visual glitches that hint at the truth:
- Heat 3.0: Pathfinding lines flicker (1 frame every 10 seconds)
- Heat 3.5: NPC names glitch to "AI_AGENT_047" for a frame
- Heat 4.0: Photorealistic texture bleeds
- Heat 4.5: Fake engine stats appear in corner

This builds suspicion before the Heat 5 revelation.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import random
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class GlitchType(Enum):
    """Types of reality glitches"""
    PATHFINDING_FLICKER = "pathfinding_flicker"  # Show AI pathfinding lines
    NAME_CORRUPTION = "name_corruption"  # NPC names become AI_AGENT_XX
    TEXTURE_BLEED = "texture_bleed"  # Photorealistic textures leak
    ENGINE_STAT_POPUP = "engine_stat_popup"  # Fake engine stats appear
    WIREFRAME_FLASH = "wireframe_flash"  # Wireframe geometry visible
    NAV_MESH_PEEK = "nav_mesh_peek"  # Navigation mesh briefly visible
    COORDINATE_OVERLAY = "coordinate_overlay"  # World coordinates shown
    RENDER_ERROR = "render_error"  # Fake render errors


@dataclass
class GlitchEvent:
    """A single glitch occurrence"""
    glitch_type: GlitchType
    timestamp: float
    duration: float  # How long the glitch lasts (seconds)
    intensity: float  # 0.0 to 1.0
    data: Dict[str, Any] = field(default_factory=dict)


class RealityGlitchSystem:
    """
    Manages micro-glitches that appear before full reality break.

    The philosophy:
    - Heat < 3: No glitches (mask intact)
    - Heat 3-3.5: Rare, subtle glitches (1-frame flickers)
    - Heat 3.5-4: Increasing frequency, more obvious
    - Heat 4-4.5: Frequent glitches, player is getting suspicious
    - Heat 4.5+: Near-constant glitching before Heat 5 breaks everything
    """

    def __init__(self):
        # Active glitches (currently visible)
        self.active_glitches: List[GlitchEvent] = []

        # Glitch timers
        self.time_since_last_glitch = 0.0
        self.glitch_cooldown = 10.0  # Base cooldown between glitches

        # Glitch intensity ramping
        self.cumulative_glitch_intensity = 0.0  # Builds over time

        # Frame counters for 1-frame flickers
        self.frame_count = 0

    def update(self, dt: float, heat_level: float, glitch_intensity: float):
        """
        Update glitch system.

        Args:
            dt: Delta time
            heat_level: Current heat (0.0 to 5.0)
            glitch_intensity: Reality break intensity from heat system
        """
        self.time_since_last_glitch += dt
        self.frame_count += 1

        # Remove expired glitches
        current_time = time.time()
        self.active_glitches = [
            g for g in self.active_glitches
            if current_time - g.timestamp < g.duration
        ]

        # No glitches below Heat 3
        if heat_level < 3.0:
            return

        # Calculate glitch spawn chance based on heat
        spawn_chance = self._calculate_spawn_chance(heat_level, dt)

        # Try to spawn glitch
        if random.random() < spawn_chance and self.time_since_last_glitch > self._get_cooldown(heat_level):
            glitch = self._spawn_glitch(heat_level, glitch_intensity)
            if glitch:
                self.active_glitches.append(glitch)
                self.time_since_last_glitch = 0.0
                self.cumulative_glitch_intensity += 0.1

    def _calculate_spawn_chance(self, heat_level: float, dt: float) -> float:
        """Calculate probability of spawning a glitch this frame"""
        if heat_level < 3.0:
            return 0.0
        elif heat_level < 3.5:
            # Rare glitches - about 1 every 10 seconds
            return 0.01
        elif heat_level < 4.0:
            # More common - about 1 every 3 seconds
            return 0.03
        elif heat_level < 4.5:
            # Frequent - about 1 per second
            return 0.06
        else:
            # Near-constant - multiple per second
            return 0.20

    def _get_cooldown(self, heat_level: float) -> float:
        """Get cooldown between glitches based on heat"""
        if heat_level < 3.5:
            return 10.0  # 10 seconds between glitches
        elif heat_level < 4.0:
            return 5.0  # 5 seconds
        elif heat_level < 4.5:
            return 2.0  # 2 seconds
        else:
            return 0.5  # Almost constant glitching

    def _spawn_glitch(self, heat_level: float, glitch_intensity: float) -> Optional[GlitchEvent]:
        """Spawn a glitch appropriate for current heat level"""

        # Select glitch type based on heat
        available_glitches = self._get_available_glitches(heat_level)
        if not available_glitches:
            return None

        glitch_type = random.choice(available_glitches)

        # Determine glitch duration
        duration = self._get_glitch_duration(glitch_type, heat_level)

        # Create glitch event
        return GlitchEvent(
            glitch_type=glitch_type,
            timestamp=time.time(),
            duration=duration,
            intensity=glitch_intensity,
            data=self._generate_glitch_data(glitch_type, heat_level)
        )

    def _get_available_glitches(self, heat_level: float) -> List[GlitchType]:
        """Get which glitch types can spawn at current heat"""
        available = []

        if heat_level >= 3.0:
            # Subtle glitches
            available.extend([
                GlitchType.PATHFINDING_FLICKER,
                GlitchType.NAV_MESH_PEEK,
            ])

        if heat_level >= 3.5:
            # Name corruption starts
            available.extend([
                GlitchType.NAME_CORRUPTION,
                GlitchType.COORDINATE_OVERLAY,
            ])

        if heat_level >= 4.0:
            # Visual corruption
            available.extend([
                GlitchType.TEXTURE_BLEED,
                GlitchType.WIREFRAME_FLASH,
            ])

        if heat_level >= 4.5:
            # Engine exposure
            available.extend([
                GlitchType.ENGINE_STAT_POPUP,
                GlitchType.RENDER_ERROR,
            ])

        return available

    def _get_glitch_duration(self, glitch_type: GlitchType, heat_level: float) -> float:
        """Get how long a glitch should last"""

        # At lower heat, glitches are brief (1-frame flickers)
        if heat_level < 3.5:
            return 0.016  # 1 frame at 60fps
        elif heat_level < 4.0:
            # Short glitches (2-5 frames)
            return random.uniform(0.032, 0.083)
        elif heat_level < 4.5:
            # Medium glitches (0.1-0.5 seconds)
            return random.uniform(0.1, 0.5)
        else:
            # Long glitches (0.5-2 seconds)
            return random.uniform(0.5, 2.0)

    def _generate_glitch_data(self, glitch_type: GlitchType, heat_level: float) -> Dict[str, Any]:
        """Generate type-specific glitch data"""

        if glitch_type == GlitchType.PATHFINDING_FLICKER:
            # Show pathfinding lines for random NPCs
            return {
                "npc_count": random.randint(1, 3),
                "line_color": "cyan" if heat_level < 4.0 else "red",
                "show_waypoints": heat_level >= 4.0
            }

        elif glitch_type == GlitchType.NAME_CORRUPTION:
            # Replace NPC names with AI agent IDs
            return {
                "corruption_chance": 0.3 if heat_level < 4.0 else 0.7,
                "show_agent_id": True,
                "show_state": heat_level >= 4.5
            }

        elif glitch_type == GlitchType.TEXTURE_BLEED:
            # Photorealistic textures leak through
            return {
                "bleed_intensity": min(1.0, (heat_level - 4.0) / 1.0),
                "affected_surfaces": random.randint(1, 5),
                "hd_resolution": heat_level >= 4.5
            }

        elif glitch_type == GlitchType.ENGINE_STAT_POPUP:
            # Fake engine stats in corner
            return {
                "stat_lines": random.randint(3, 8),
                "position": random.choice(["top_left", "top_right", "bottom_left"]),
                "show_fps": True,
                "show_drawcalls": heat_level >= 4.5
            }

        elif glitch_type == GlitchType.WIREFRAME_FLASH:
            # Wireframe geometry visible
            return {
                "wireframe_opacity": random.uniform(0.2, 0.6),
                "show_normals": heat_level >= 4.5
            }

        elif glitch_type == GlitchType.NAV_MESH_PEEK:
            # Navigation mesh briefly visible
            return {
                "mesh_opacity": random.uniform(0.1, 0.4),
                "show_walkable": True,
                "show_obstacles": heat_level >= 4.0
            }

        elif glitch_type == GlitchType.COORDINATE_OVERLAY:
            # World coordinates shown
            return {
                "show_player_coords": True,
                "show_npc_coords": heat_level >= 4.0,
                "show_grid": heat_level >= 4.5
            }

        elif glitch_type == GlitchType.RENDER_ERROR:
            # Fake render error messages
            return {
                "error_type": random.choice([
                    "BUFFER_OVERFLOW",
                    "TEXTURE_CACHE_MISS",
                    "TOO_MANY_AGENTS",
                    "RAYCASTER_LIMIT_EXCEEDED"
                ]),
                "show_stack_trace": heat_level >= 4.8
            }

        return {}

    def get_active_glitches(self) -> List[GlitchEvent]:
        """Get list of currently active glitches"""
        return self.active_glitches

    def get_glitch_rendering_data(self) -> Dict[str, Any]:
        """
        Get rendering instructions for current glitches.

        Returns a dict that the renderer can use to apply glitch effects.
        """
        if not self.active_glitches:
            return {}

        rendering_data = {
            "active": True,
            "glitches": []
        }

        for glitch in self.active_glitches:
            glitch_data = {
                "type": glitch.glitch_type.value,
                "intensity": glitch.intensity,
                "age": time.time() - glitch.timestamp,
                "duration": glitch.duration,
                **glitch.data
            }
            rendering_data["glitches"].append(glitch_data)

        return rendering_data

    def force_glitch(self, glitch_type: GlitchType, duration: float = 1.0):
        """Force a specific glitch to occur (for testing/scripting)"""
        glitch = GlitchEvent(
            glitch_type=glitch_type,
            timestamp=time.time(),
            duration=duration,
            intensity=1.0,
            data=self._generate_glitch_data(glitch_type, 5.0)
        )
        self.active_glitches.append(glitch)

    def get_glitch_frequency_description(self, heat_level: float) -> str:
        """Get text description of glitch frequency at current heat"""
        if heat_level < 3.0:
            return "Stable. No glitches detected."
        elif heat_level < 3.5:
            return "Minor instabilities. Rare visual artifacts."
        elif heat_level < 4.0:
            return "Reality cracks appearing. Intermittent glitches."
        elif heat_level < 4.5:
            return "Facade strain evident. Frequent glitches."
        else:
            return "CRITICAL: Mask failing. Near-constant glitching."
