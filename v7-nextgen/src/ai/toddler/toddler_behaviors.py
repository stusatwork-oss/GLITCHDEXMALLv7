"""
Toddler Behavioral Modes

Defines the different behavioral states and their movement patterns.
"""

from enum import Enum
from typing import Tuple, Optional
import random
import math


class ToddlerBehavior(Enum):
    """
    Behavioral states for the toddler.

    WANDERING: Drifts randomly, low visibility, background dread
    CURIOUS: Follows player at distance, medium visibility
    MANIFESTING: Approaches player, high visibility, triggered by high Cloud
    FLEEING: Moves away, drops visibility, triggered by direct look
    STATIC: Stays in one location, creates haunted zone
    """
    WANDERING = "wandering"
    CURIOUS = "curious"
    MANIFESTING = "manifesting"
    FLEEING = "fleeing"
    STATIC = "static"


class BehaviorController:
    """
    Controls toddler behavior state transitions and movement patterns.
    """

    def __init__(self, config: dict):
        self.config = config
        self.behavior = ToddlerBehavior.WANDERING
        self.static_timer = 0.0
        self.wander_target = None

    def update_behavior(
        self,
        distance_to_player: float,
        current_cloud: float,
        player_looking_at_toddler: bool,
        npc_contradiction_triggered: bool
    ) -> ToddlerBehavior:
        """
        Determine next behavior based on sim state.

        Args:
            distance_to_player: Distance in feet
            current_cloud: Cloud level 0-100
            player_looking_at_toddler: True if player's view is aimed at toddler
            npc_contradiction_triggered: True if NPC just broke a rule

        Returns:
            Updated behavior state
        """
        triggers = self.config["behavior_triggers"]

        # STATIC behavior (from contradiction) takes priority
        if self.behavior == ToddlerBehavior.STATIC:
            if self.static_timer > 0:
                return self.behavior  # Stay static
            else:
                self.behavior = ToddlerBehavior.WANDERING  # Resume

        # Trigger STATIC on NPC contradiction
        if npc_contradiction_triggered and triggers.get("static_on_contradiction"):
            self.behavior = ToddlerBehavior.STATIC
            self.static_timer = triggers.get("static_duration", 30.0)
            return self.behavior

        # FLEEING triggered by direct look
        if player_looking_at_toddler and triggers.get("fleeing_direct_look"):
            self.behavior = ToddlerBehavior.FLEEING
            return self.behavior

        # MANIFESTING triggered by high Cloud
        if current_cloud >= triggers.get("manifesting_cloud", 70.0):
            self.behavior = ToddlerBehavior.MANIFESTING
            return self.behavior

        # CURIOUS triggered by proximity
        if distance_to_player < triggers.get("curious_distance", 50.0):
            if self.behavior != ToddlerBehavior.FLEEING:  # Don't interrupt fleeing
                self.behavior = ToddlerBehavior.CURIOUS
                return self.behavior

        # Default: WANDERING
        if self.behavior == ToddlerBehavior.FLEEING:
            # Return to wandering after fleeing far enough
            if distance_to_player > 100:
                self.behavior = ToddlerBehavior.WANDERING

        return self.behavior

    def tick_static_timer(self, dt: float):
        """Decrement static timer if in STATIC mode."""
        if self.behavior == ToddlerBehavior.STATIC:
            self.static_timer = max(0, self.static_timer - dt)

    def get_movement_vector(
        self,
        toddler_pos: Tuple[float, float, float],
        player_pos: Tuple[float, float, float],
        dt: float
    ) -> Tuple[float, float, float]:
        """
        Calculate movement vector based on current behavior.

        Returns:
            (dx, dy, dz) movement delta
        """
        if self.behavior == ToddlerBehavior.STATIC:
            return (0, 0, 0)

        # Get speed for current behavior
        speed_map = {
            ToddlerBehavior.WANDERING: self.config["movement"]["base_speed"],
            ToddlerBehavior.CURIOUS: self.config["movement"]["curious_speed"],
            ToddlerBehavior.MANIFESTING: self.config["movement"]["curious_speed"],
            ToddlerBehavior.FLEEING: self.config["movement"]["fleeing_speed"],
        }
        speed = speed_map.get(self.behavior, 3.0)

        # Calculate direction based on behavior
        if self.behavior == ToddlerBehavior.WANDERING:
            return self._wander_movement(toddler_pos, dt, speed)

        elif self.behavior == ToddlerBehavior.CURIOUS:
            return self._follow_at_distance(toddler_pos, player_pos, dt, speed, target_distance=30.0)

        elif self.behavior == ToddlerBehavior.MANIFESTING:
            return self._approach_movement(toddler_pos, player_pos, dt, speed)

        elif self.behavior == ToddlerBehavior.FLEEING:
            return self._flee_movement(toddler_pos, player_pos, dt, speed)

        return (0, 0, 0)

    def _wander_movement(
        self,
        pos: Tuple[float, float, float],
        dt: float,
        speed: float
    ) -> Tuple[float, float, float]:
        """Random walk movement."""
        # Pick new wander target occasionally
        if self.wander_target is None or random.random() < 0.01:
            radius = self.config["movement"]["wander_radius"]
            angle = random.uniform(0, 2 * math.pi)
            self.wander_target = (
                pos[0] + radius * math.cos(angle),
                pos[1] + radius * math.sin(angle),
                pos[2]  # Keep same Z level
            )

        # Move toward wander target
        return self._move_toward(pos, self.wander_target, dt, speed)

    def _follow_at_distance(
        self,
        pos: Tuple[float, float, float],
        target: Tuple[float, float, float],
        dt: float,
        speed: float,
        target_distance: float = 30.0
    ) -> Tuple[float, float, float]:
        """Follow at preferred distance."""
        distance = self._distance(pos, target)

        if distance > target_distance + 10:
            # Too far, approach
            return self._move_toward(pos, target, dt, speed)
        elif distance < target_distance - 10:
            # Too close, back off
            return self._move_away(pos, target, dt, speed * 0.5)
        else:
            # In sweet spot, match player movement
            return (0, 0, 0)

    def _approach_movement(
        self,
        pos: Tuple[float, float, float],
        target: Tuple[float, float, float],
        dt: float,
        speed: float
    ) -> Tuple[float, float, float]:
        """Direct approach."""
        return self._move_toward(pos, target, dt, speed)

    def _flee_movement(
        self,
        pos: Tuple[float, float, float],
        threat: Tuple[float, float, float],
        dt: float,
        speed: float
    ) -> Tuple[float, float, float]:
        """Move away from threat."""
        return self._move_away(pos, threat, dt, speed)

    def _move_toward(
        self,
        pos: Tuple[float, float, float],
        target: Tuple[float, float, float],
        dt: float,
        speed: float
    ) -> Tuple[float, float, float]:
        """Calculate movement vector toward target."""
        dx = target[0] - pos[0]
        dy = target[1] - pos[1]
        dz = target[2] - pos[2]

        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < 0.1:
            return (0, 0, 0)

        # Normalize and scale by speed * dt
        scale = (speed * dt) / dist
        return (dx * scale, dy * scale, dz * scale)

    def _move_away(
        self,
        pos: Tuple[float, float, float],
        threat: Tuple[float, float, float],
        dt: float,
        speed: float
    ) -> Tuple[float, float, float]:
        """Calculate movement vector away from threat."""
        dx = pos[0] - threat[0]
        dy = pos[1] - threat[1]
        dz = pos[2] - threat[2]

        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < 0.1:
            # If overlapping, pick random direction
            angle = random.uniform(0, 2 * math.pi)
            return (
                speed * dt * math.cos(angle),
                speed * dt * math.sin(angle),
                0
            )

        # Normalize and scale
        scale = (speed * dt) / dist
        return (dx * scale, dy * scale, dz * scale)

    @staticmethod
    def _distance(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
        """Euclidean distance."""
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        dz = b[2] - a[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)
