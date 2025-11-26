"""
TODDLER SYSTEM - The Entity Outside The Simulation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The toddler is NOT a game entity.
The toddler is using the AAA engine as a prybar to escape the Wolf3D prison.

Wherever the toddler goes:
- Reality becomes unstable (heat amplification)
- Glitches spawn more frequently
- The mask strains harder to contain the modern engine
- NPCs sense "something" but can't see it

The toddler is invisible most of the time.
At Heat 5, the mask fails enough that you can SEE THE TODDLER for brief moments.

This is the source of all reality breaks.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import random
import math
from typing import Tuple, Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class ToddlerBehavior(Enum):
    """Toddler behavioral states"""
    WANDERING = "wandering"  # Random exploration
    FOLLOWING_PLAYER = "following_player"  # Curious about player
    ATTRACTED_TO_CHAOS = "attracted_to_chaos"  # Moves toward high heat
    BREAKING_REALITY = "breaking_reality"  # Actively destabilizing simulation
    HIDING = "hiding"  # Stationary, watching


@dataclass
class ToddlerState:
    """Current state of the toddler entity"""
    position: Tuple[float, float, float]
    behavior: ToddlerBehavior
    visibility: float = 0.0  # 0.0 (invisible) to 1.0 (fully visible)
    reality_strain: float = 0.0  # How much reality is bending around toddler

    # Movement
    velocity: Tuple[float, float] = (0.0, 0.0)
    target_position: Optional[Tuple[float, float, float]] = None

    # Timers
    behavior_timer: float = 0.0
    flicker_timer: float = 0.0


class ToddlerSystem:
    """
    Manages the toddler entity that exists outside the simulation.

    The toddler is the REASON everything breaks down.
    It's using the modern engine to pry open the Wolf3D facade.
    """

    def __init__(self, world_bounds: Tuple[int, int]):
        """
        Initialize toddler system.

        Args:
            world_bounds: (width, height) of the world
        """
        self.world_bounds = world_bounds

        # Start toddler in random location
        spawn_x = random.uniform(10, world_bounds[0] - 10)
        spawn_y = random.uniform(10, world_bounds[1] - 10)

        self.toddler = ToddlerState(
            position=(spawn_x, spawn_y, 0),
            behavior=ToddlerBehavior.WANDERING
        )

        # Toddler parameters
        self.movement_speed = 1.5  # Tiles per second (slow wandering)
        self.distortion_radius = 15.0  # Reality distortion field radius
        self.heat_amplification = 2.0  # Heat builds 2x faster near toddler
        self.glitch_multiplier = 3.0  # Glitches 3x more likely near toddler

        # Behavior change frequency
        self.behavior_change_interval = 10.0  # Change behavior every 10 seconds

    def update(self, dt: float, player_position: Tuple[float, float, float],
               current_heat: float, world_tiles: Dict) -> Dict[str, Any]:
        """
        Update toddler behavior and effects.

        Args:
            dt: Delta time
            player_position: Current player position
            current_heat: Current heat level (0-5)
            world_tiles: World tile map for pathfinding

        Returns:
            Dict with toddler effects and state
        """
        self.toddler.behavior_timer += dt
        self.toddler.flicker_timer += dt

        # Update behavior state
        if self.toddler.behavior_timer >= self.behavior_change_interval:
            self._change_behavior(current_heat, player_position)
            self.toddler.behavior_timer = 0.0

        # Update movement
        self._update_movement(dt, player_position, current_heat, world_tiles)

        # Update visibility based on heat
        self._update_visibility(current_heat, player_position)

        # Update reality strain
        self._update_reality_strain(current_heat)

        # Calculate effects on world
        effects = self._calculate_effects(player_position, current_heat)

        return effects

    def _change_behavior(self, current_heat: float, player_position: Tuple[float, float, float]):
        """Change toddler behavior based on heat and randomness"""

        if current_heat < 1.0:
            # Low heat: mostly wandering
            behaviors = [
                (ToddlerBehavior.WANDERING, 0.8),
                (ToddlerBehavior.HIDING, 0.2)
            ]
        elif current_heat < 3.0:
            # Medium heat: curiosity about player
            behaviors = [
                (ToddlerBehavior.WANDERING, 0.5),
                (ToddlerBehavior.FOLLOWING_PLAYER, 0.3),
                (ToddlerBehavior.HIDING, 0.2)
            ]
        elif current_heat < 4.5:
            # High heat: attracted to chaos
            behaviors = [
                (ToddlerBehavior.ATTRACTED_TO_CHAOS, 0.4),
                (ToddlerBehavior.FOLLOWING_PLAYER, 0.3),
                (ToddlerBehavior.WANDERING, 0.2),
                (ToddlerBehavior.BREAKING_REALITY, 0.1)
            ]
        else:
            # Critical heat: actively breaking reality
            behaviors = [
                (ToddlerBehavior.BREAKING_REALITY, 0.6),
                (ToddlerBehavior.ATTRACTED_TO_CHAOS, 0.3),
                (ToddlerBehavior.FOLLOWING_PLAYER, 0.1)
            ]

        # Weighted random selection
        rand = random.random()
        cumulative = 0.0
        for behavior, weight in behaviors:
            cumulative += weight
            if rand < cumulative:
                self.toddler.behavior = behavior
                self._set_new_target(player_position)
                break

    def _set_new_target(self, player_position: Tuple[float, float, float]):
        """Set new target position based on behavior"""

        if self.toddler.behavior == ToddlerBehavior.WANDERING:
            # Random position in world
            target_x = random.uniform(5, self.world_bounds[0] - 5)
            target_y = random.uniform(5, self.world_bounds[1] - 5)
            self.toddler.target_position = (target_x, target_y, 0)

        elif self.toddler.behavior == ToddlerBehavior.FOLLOWING_PLAYER:
            # Near player, but not too close
            offset_x = random.uniform(-10, 10)
            offset_y = random.uniform(-10, 10)
            self.toddler.target_position = (
                player_position[0] + offset_x,
                player_position[1] + offset_y,
                0
            )

        elif self.toddler.behavior == ToddlerBehavior.ATTRACTED_TO_CHAOS:
            # Move toward player (source of chaos)
            self.toddler.target_position = player_position

        elif self.toddler.behavior == ToddlerBehavior.BREAKING_REALITY:
            # Move to player vicinity
            offset_x = random.uniform(-5, 5)
            offset_y = random.uniform(-5, 5)
            self.toddler.target_position = (
                player_position[0] + offset_x,
                player_position[1] + offset_y,
                0
            )

        elif self.toddler.behavior == ToddlerBehavior.HIDING:
            # Stay still
            self.toddler.target_position = None

    def _update_movement(self, dt: float, player_position: Tuple[float, float, float],
                        current_heat: float, world_tiles: Dict):
        """Update toddler position"""

        if not self.toddler.target_position or self.toddler.behavior == ToddlerBehavior.HIDING:
            return

        # Calculate direction to target
        dx = self.toddler.target_position[0] - self.toddler.position[0]
        dy = self.toddler.target_position[1] - self.toddler.position[1]
        distance = math.sqrt(dx*dx + dy*dy)

        if distance < 1.0:
            # Reached target
            if self.toddler.behavior != ToddlerBehavior.ATTRACTED_TO_CHAOS:
                self._set_new_target(player_position)
            return

        # Move toward target
        speed = self.movement_speed
        if self.toddler.behavior == ToddlerBehavior.BREAKING_REALITY:
            speed *= 1.5  # Faster when breaking reality

        # Normalize and apply speed
        move_x = (dx / distance) * speed * dt
        move_y = (dy / distance) * speed * dt

        new_x = self.toddler.position[0] + move_x
        new_y = self.toddler.position[1] + move_y

        # Update position (toddler can walk through walls - it's outside the simulation)
        self.toddler.position = (new_x, new_y, 0)

    def _update_visibility(self, current_heat: float, player_position: Tuple[float, float, float]):
        """Update toddler visibility based on heat and proximity"""

        # Base visibility from heat
        if current_heat < 3.0:
            base_visibility = 0.0  # Completely invisible
        elif current_heat < 4.0:
            base_visibility = 0.05  # Barely visible flickers
        elif current_heat < 4.5:
            base_visibility = 0.2  # Occasional visibility
        else:
            base_visibility = 0.5  # Frequently visible at Heat 5

        # Distance to player affects visibility
        distance = self._distance_to_player(player_position)
        if distance < 5.0:
            # Very close = more visible
            proximity_bonus = 0.3
        elif distance < 10.0:
            proximity_bonus = 0.1
        else:
            proximity_bonus = 0.0

        # Flicker effect (toddler appears and disappears)
        flicker = 1.0 if (self.toddler.flicker_timer % 2.0) < 1.0 else 0.5

        self.toddler.visibility = min(1.0, (base_visibility + proximity_bonus) * flicker)

    def _update_reality_strain(self, current_heat: float):
        """Update reality strain caused by toddler"""

        # Reality strain increases with heat
        base_strain = current_heat / 5.0

        # Behavior affects strain
        behavior_multiplier = {
            ToddlerBehavior.WANDERING: 1.0,
            ToddlerBehavior.FOLLOWING_PLAYER: 1.2,
            ToddlerBehavior.ATTRACTED_TO_CHAOS: 1.5,
            ToddlerBehavior.BREAKING_REALITY: 2.0,
            ToddlerBehavior.HIDING: 0.5
        }

        multiplier = behavior_multiplier.get(self.toddler.behavior, 1.0)
        self.toddler.reality_strain = min(1.0, base_strain * multiplier)

    def _distance_to_player(self, player_position: Tuple[float, float, float]) -> float:
        """Calculate distance to player"""
        dx = self.toddler.position[0] - player_position[0]
        dy = self.toddler.position[1] - player_position[1]
        return math.sqrt(dx*dx + dy*dy)

    def _calculate_effects(self, player_position: Tuple[float, float, float],
                          current_heat: float) -> Dict[str, Any]:
        """Calculate toddler's effects on the world"""

        distance = self._distance_to_player(player_position)
        in_distortion_field = distance <= self.distortion_radius

        # Calculate intensity based on distance
        if in_distortion_field:
            intensity = 1.0 - (distance / self.distortion_radius)
        else:
            intensity = 0.0

        return {
            "toddler_position": self.toddler.position,
            "toddler_visible": self.toddler.visibility > 0.1,
            "visibility": self.toddler.visibility,
            "behavior": self.toddler.behavior.value,
            "reality_strain": self.toddler.reality_strain,

            # Effects on player
            "in_distortion_field": in_distortion_field,
            "distortion_intensity": intensity,
            "heat_multiplier": 1.0 + (self.heat_amplification * intensity),
            "glitch_multiplier": 1.0 + (self.glitch_multiplier * intensity),

            # Atmospheric data
            "distance_to_player": distance,
            "distortion_radius": self.distortion_radius
        }

    def get_toddler_dialogue_proximity_effect(self, player_position: Tuple[float, float, float]) -> bool:
        """Check if toddler is close enough for NPCs to sense something"""
        distance = self._distance_to_player(player_position)
        return distance < 8.0  # NPCs can sense toddler within 8 tiles

    def get_rendering_data(self) -> Dict[str, Any]:
        """Get rendering data for toddler (if visible)"""
        if self.toddler.visibility < 0.05:
            return {"visible": False}

        return {
            "visible": True,
            "position": self.toddler.position,
            "visibility": self.toddler.visibility,
            "reality_strain": self.toddler.reality_strain,
            "behavior": self.toddler.behavior.value,
            "symbol": "☺" if self.toddler.visibility > 0.3 else "·",  # Unicode toddler / faint dot
            "flicker": self.toddler.flicker_timer % 0.5 < 0.25  # Rapid flicker
        }
