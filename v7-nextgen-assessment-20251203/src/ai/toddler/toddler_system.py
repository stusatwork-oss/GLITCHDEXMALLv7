"""
Toddler System - Reality Catalyst Core

Main system that manages toddler state, behavior, and effect generation.

The toddler is an invisible reality catalyst that:
- Amplifies Cloud pressure (heat_multiplier)
- Generates visual/audio glitches (glitch_multiplier)
- Creates distortion fields (reality_strain)
- Agitates zones (QBIT disturbance)
- Provides context for Leon (shared dread)

Usage:
    toddler = ToddlerSystem(initial_pos=(0, 0, 0), config=TODDLER_CONFIG)

    effects = toddler.update(
        dt=0.016,
        player_position=(50, 10, 0),
        current_cloud=75.3,
        world_tiles=world.tiles
    )

    # effects contains: heat_multiplier, glitch_multiplier, reality_strain, etc.
"""

from typing import Dict, Tuple, Optional, Any
import math
import time

from .toddler_behaviors import ToddlerBehavior, BehaviorController
from .toddler_config import TODDLER_CONFIG


class ToddlerSystem:
    """
    Main toddler reality catalyst system.

    Manages toddler state, behavior, movement, visibility, and effect generation.
    Outputs effects dict each tick for integration with Cloud, QBIT, renderer, and Leon.
    """

    def __init__(
        self,
        initial_position: Tuple[float, float, float] = (0, 0, 0),
        config: Optional[Dict] = None
    ):
        """
        Initialize toddler system.

        Args:
            initial_position: Starting (x, y, z) position in world coordinates
            config: Configuration dict (defaults to TODDLER_CONFIG)
        """
        self.config = config or TODDLER_CONFIG

        # State
        self.position = initial_position
        self.visibility = self.config["spawn"]["initial_visibility"]
        self.reality_strain = 0.0

        # Behavior controller
        self.behavior_controller = BehaviorController(self.config)
        self.behavior = self.behavior_controller.behavior

        # Tracking
        self.last_player_position = None
        self.time_alive = 0.0
        self.last_contradiction_time = 0.0

    def update(
        self,
        dt: float,
        player_position: Tuple[float, float, float],
        current_cloud: float = 0.0,
        player_looking_at_toddler: bool = False,
        npc_contradiction_triggered: bool = False,
        world_tiles: Optional[Any] = None
    ) -> Dict:
        """
        Update toddler state and generate effects.

        Args:
            dt: Delta time in seconds
            player_position: (x, y, z) player position
            current_cloud: Current Cloud level (0-100)
            player_looking_at_toddler: True if player's view is aimed at toddler
            npc_contradiction_triggered: True if NPC just broke a rule
            world_tiles: Optional world collision data (for pathfinding)

        Returns:
            effects dict with heat_multiplier, glitch_multiplier, etc.
        """
        self.time_alive += dt
        self.last_player_position = player_position

        # Calculate distance to player
        distance_to_player = self._distance(self.position, player_position)

        # Update behavior
        self.behavior = self.behavior_controller.update_behavior(
            distance_to_player=distance_to_player,
            current_cloud=current_cloud,
            player_looking_at_toddler=player_looking_at_toddler,
            npc_contradiction_triggered=npc_contradiction_triggered
        )
        self.behavior_controller.tick_static_timer(dt)

        # Update position
        self._update_position(dt, player_position)

        # Update visibility
        self._update_visibility(dt, current_cloud, player_looking_at_toddler)

        # Update reality strain
        self._update_reality_strain(dt, distance_to_player, current_cloud)

        # Check for teleport (if too far from player)
        if distance_to_player > self.config["movement"]["teleport_distance"]:
            self._teleport_near_player(player_position)

        # Generate effects dict
        return self._generate_effects(distance_to_player)

    def _update_position(self, dt: float, player_position: Tuple[float, float, float]):
        """Update toddler position based on behavior."""
        movement = self.behavior_controller.get_movement_vector(
            self.position,
            player_position,
            dt
        )

        # Apply movement
        self.position = (
            self.position[0] + movement[0],
            self.position[1] + movement[1],
            self.position[2] + movement[2]
        )

    def _update_visibility(
        self,
        dt: float,
        current_cloud: float,
        player_looking_at_toddler: bool
    ):
        """Update visibility based on Cloud level and behavior."""
        vis_config = self.config["visibility"]

        # Base rate + cloud amplifier
        base_rate = vis_config["base_rate"]
        cloud_bonus = current_cloud * vis_config["cloud_amplifier"]
        visibility_delta = (base_rate + cloud_bonus) * dt

        # Behavior-specific modifiers
        from .toddler_config import BEHAVIOR_PARAMS
        behavior_rate = BEHAVIOR_PARAMS[self.behavior.name]["visibility_rate"]
        visibility_delta += behavior_rate * dt

        # Instant fade if direct look + below threshold
        if player_looking_at_toddler and self.visibility < vis_config["instant_fade_threshold"]:
            self.visibility = max(0, self.visibility - 0.5)  # Rapid fade
        else:
            self.visibility = max(0, min(vis_config["max_visibility"],
                                        self.visibility + visibility_delta))

    def _update_reality_strain(
        self,
        dt: float,
        distance_to_player: float,
        current_cloud: float
    ):
        """
        Update reality strain based on visibility, distance, and Cloud.

        Reality strain represents how much the toddler is warping local space.
        """
        # Base strain = visibility
        base_strain = self.visibility

        # Distance modifier (closer = more strain)
        if distance_to_player < 10:
            distance_mod = 2.0
        elif distance_to_player < 30:
            distance_mod = 1.5
        else:
            distance_mod = 1.0

        # Cloud modifier (higher Cloud = more strain)
        cloud_mod = 1.0 + (current_cloud / 100.0)

        # Calculate strain
        target_strain = base_strain * distance_mod * cloud_mod

        # Smooth approach to target strain
        self.reality_strain += (target_strain - self.reality_strain) * 0.1

        # Clamp
        self.reality_strain = max(0, min(1.0, self.reality_strain))

    def _generate_effects(self, distance_to_player: float) -> Dict:
        """
        Generate effects dict for integration with other systems.

        Returns:
            {
                "heat_multiplier": 1.0-3.0,
                "glitch_multiplier": 1.0-4.0,
                "in_distortion_field": bool,
                "distortion_intensity": 0.0-1.0,
                "distance_to_player": float,
                "toddler_visible": 0.0-1.0,
                "reality_strain": 0.0-1.0,
                "toddler_position": (x, y, z),
                "behavior": str
            }
        """
        dist_config = self.config["distortion"]
        heat_config = self.config["heat_generation"]
        glitch_config = self.config["glitch_generation"]

        # Calculate distortion radius (scales with visibility)
        base_radius = dist_config["base_radius"]
        max_radius = dist_config["max_radius"]
        current_radius = base_radius + (max_radius - base_radius) * self.visibility

        # Check if player in distortion field
        in_field = distance_to_player <= current_radius

        # Calculate distortion intensity (falloff with distance)
        if in_field:
            falloff = dist_config["intensity_falloff"]
            normalized_dist = distance_to_player / current_radius
            distortion_intensity = self.reality_strain * (1.0 - normalized_dist ** falloff)
        else:
            distortion_intensity = 0.0

        # Calculate heat multiplier (for Cloud pressure)
        # Inverse square law with distance, weighted by visibility
        if distance_to_player < 1:
            distance_factor = 10.0  # Very close
        else:
            distance_factor = 1.0 / (distance_to_player ** 0.5)  # Inverse sqrt (softer than inverse square)

        visibility_weight = heat_config["visibility_weight"]
        heat_mult = 1.0 + (heat_config["max_multiplier"] - 1.0) * (
            visibility_weight * self.visibility +
            (1.0 - visibility_weight) * distance_factor
        )
        heat_mult = min(heat_config["max_multiplier"], heat_mult)

        # Calculate glitch multiplier (for renderer)
        glitch_mult = 1.0 + (glitch_config["max_multiplier"] - 1.0) * (
            self.reality_strain * glitch_config["reality_strain_factor"]
        )
        glitch_mult = min(glitch_config["max_multiplier"], glitch_mult)

        return {
            "heat_multiplier": heat_mult,
            "glitch_multiplier": glitch_mult,
            "in_distortion_field": in_field,
            "distortion_intensity": distortion_intensity,
            "distortion_radius": current_radius,
            "distance_to_player": distance_to_player,
            "toddler_visible": self.visibility,
            "reality_strain": self.reality_strain,
            "toddler_position": self.position,
            "behavior": self.behavior.value,
            "time_alive": self.time_alive
        }

    def _teleport_near_player(self, player_position: Tuple[float, float, float]):
        """Teleport toddler near player if too far away."""
        import random
        import math

        safe_dist = self.config["spawn"]["safe_spawn_distance"]

        # Random angle
        angle = random.uniform(0, 2 * math.pi)

        # Position at safe distance
        self.position = (
            player_position[0] + safe_dist * math.cos(angle),
            player_position[1] + safe_dist * math.sin(angle),
            player_position[2]  # Same Z level
        )

        # Reset visibility on teleport
        self.visibility = 0.0

    def export_state(self) -> Dict:
        """
        Export toddler state for Leon/renderer/save system.

        Returns:
            State dict with position, behavior, visibility, etc.
        """
        return {
            "position": self.position,
            "behavior": self.behavior.value,
            "visibility": self.visibility,
            "reality_strain": self.reality_strain,
            "time_alive": self.time_alive
        }

    @staticmethod
    def _distance(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
        """Calculate Euclidean distance between two points."""
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        dz = b[2] - a[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)
