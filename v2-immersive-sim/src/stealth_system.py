"""
STEALTH SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Vision cones, line-of-sight, noise propagation, alert states.

Think Splinter Cell / Dishonored stealth mechanics...
...rendered in ANSI terminal art.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import math
import time
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class AlertState(Enum):
    """NPC alert states (per-NPC, separate from faction alert)"""
    UNALERT = 0
    SUSPICIOUS = 1
    SEARCHING = 2
    ALERTED = 3


@dataclass
class NoiseEvent:
    """A noise that propagates through the world"""
    position: Tuple[int, int, int]
    intensity: float  # 0.0 to 1.0
    radius: float
    source_type: str  # "footstep", "gunshot", "explosion", "vending_machine"
    timestamp: float
    decay_rate: float = 0.5  # How fast it fades

    def get_intensity_at(self, position: Tuple[int, int, int], current_time: float) -> float:
        """Get noise intensity at a position"""
        # Distance falloff
        dx = position[0] - self.position[0]
        dy = position[1] - self.position[1]
        dist = math.sqrt(dx*dx + dy*dy)

        if dist > self.radius:
            return 0.0

        # Time decay
        age = current_time - self.timestamp
        time_factor = max(0.0, 1.0 - (age * self.decay_rate))

        # Distance factor
        dist_factor = 1.0 - (dist / self.radius)

        return self.intensity * dist_factor * time_factor


class VisionCone:
    """Represents NPC field of view"""

    def __init__(self, npc_position: Tuple[int, int, int], facing_angle: float, fov: float = 90.0, range: float = 10.0):
        self.position = npc_position
        self.facing = facing_angle  # Degrees
        self.fov = fov  # Field of view angle
        self.range = range

    def can_see(self, target_position: Tuple[int, int, int], world_tiles: Dict) -> bool:
        """Check if target is in vision cone with line-of-sight"""
        # Calculate angle to target
        dx = target_position[0] - self.position[0]
        dy = target_position[1] - self.position[1]
        distance = math.sqrt(dx*dx + dy*dy)

        if distance > self.range:
            return False

        if distance < 0.1:
            return True  # Very close

        angle_to_target = math.degrees(math.atan2(dy, dx))

        # Normalize angles
        angle_diff = (angle_to_target - self.facing + 180) % 360 - 180

        if abs(angle_diff) > self.fov / 2:
            return False  # Outside FOV

        # Line of sight check
        return self._has_line_of_sight(target_position, world_tiles)

    def _has_line_of_sight(self, target: Tuple[int, int, int], world_tiles: Dict) -> bool:
        """Raycast to check if path is clear"""
        # Bresenham-style line algorithm
        x0, y0, z0 = self.position
        x1, y1, z1 = target

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        x, y = x0, y0

        while (x, y) != (x1, y1):
            # Check if this tile blocks vision
            tile_key = (x, y, z0)
            if tile_key in world_tiles:
                tile = world_tiles[tile_key]
                if not tile.walkable:  # Walls block vision
                    return False

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

        return True


class StealthSystem:
    """
    Manages stealth mechanics for the entire world.

    - Tracks noise events
    - Calculates NPC awareness
    - Manages alert states
    """

    def __init__(self):
        self.noise_events: List[NoiseEvent] = []
        self.npc_alert_states: Dict[str, AlertState] = {}  # npc_id -> alert state
        self.npc_suspicion_timers: Dict[str, float] = {}  # npc_id -> time remaining suspicious
        self.player_visibility_map: Dict[str, float] = {}  # npc_id -> how visible player is (0-1)

    def create_noise(self, position: Tuple[int, int, int], intensity: float, noise_type: str):
        """Create a noise event"""
        # Determine radius based on type
        radius_map = {
            "footstep": 3.0,
            "running": 6.0,
            "gunshot": 20.0,
            "explosion": 30.0,
            "vending_machine": 8.0,
            "glass_break": 12.0,
            "alarm": 40.0
        }

        radius = radius_map.get(noise_type, 5.0)

        noise = NoiseEvent(
            position=position,
            intensity=intensity,
            radius=radius,
            source_type=noise_type,
            timestamp=time.time(),
            decay_rate=0.5 if noise_type != "alarm" else 0.1
        )

        self.noise_events.append(noise)

    def update(self, dt: float, world_state: Dict[str, Any]):
        """Update stealth system"""
        current_time = time.time()

        # Remove expired noise events
        self.noise_events = [
            n for n in self.noise_events
            if current_time - n.timestamp < (1.0 / n.decay_rate)
        ]

        # Update suspicion timers
        for npc_id in list(self.npc_suspicion_timers.keys()):
            self.npc_suspicion_timers[npc_id] -= dt
            if self.npc_suspicion_timers[npc_id] <= 0:
                del self.npc_suspicion_timers[npc_id]
                # De-escalate alert
                if npc_id in self.npc_alert_states:
                    current_alert = self.npc_alert_states[npc_id]
                    if current_alert == AlertState.SUSPICIOUS:
                        self.npc_alert_states[npc_id] = AlertState.UNALERT
                    elif current_alert == AlertState.SEARCHING:
                        self.npc_alert_states[npc_id] = AlertState.SUSPICIOUS
                        self.npc_suspicion_timers[npc_id] = 10.0

    def check_npc_awareness(self,
                           npc_id: str,
                           npc_position: Tuple[int, int, int],
                           npc_facing: float,
                           player_position: Tuple[int, int, int],
                           world_tiles: Dict) -> float:
        """
        Check if NPC can see player.
        Returns awareness level (0.0 to 1.0)
        """
        # Create vision cone
        cone = VisionCone(npc_position, npc_facing, fov=90.0, range=10.0)

        if cone.can_see(player_position, world_tiles):
            # Player is visible
            distance = math.sqrt(
                (player_position[0] - npc_position[0])**2 +
                (player_position[1] - npc_position[1])**2
            )

            # Closer = more visible
            visibility = max(0.0, min(1.0, 1.0 - (distance / 10.0)))

            self.player_visibility_map[npc_id] = visibility

            # Escalate alert if highly visible
            if visibility > 0.7:
                self.set_npc_alert_state(npc_id, AlertState.ALERTED)
            elif visibility > 0.3:
                self.set_npc_alert_state(npc_id, AlertState.SUSPICIOUS)
                self.npc_suspicion_timers[npc_id] = 15.0

            return visibility
        else:
            self.player_visibility_map[npc_id] = 0.0
            return 0.0

    def check_noise_heard(self, npc_position: Tuple[int, int, int]) -> Optional[NoiseEvent]:
        """Check if NPC can hear any active noise"""
        current_time = time.time()

        loudest_noise = None
        max_intensity = 0.0

        for noise in self.noise_events:
            intensity = noise.get_intensity_at(npc_position, current_time)
            if intensity > max_intensity:
                max_intensity = intensity
                loudest_noise = noise

        return loudest_noise if max_intensity > 0.1 else None

    def set_npc_alert_state(self, npc_id: str, alert_state: AlertState):
        """Set NPC alert state"""
        self.npc_alert_states[npc_id] = alert_state

    def get_npc_alert_state(self, npc_id: str) -> AlertState:
        """Get NPC alert state"""
        return self.npc_alert_states.get(npc_id, AlertState.UNALERT)

    def is_player_detected(self) -> bool:
        """Check if player has been detected by anyone"""
        return any(state == AlertState.ALERTED for state in self.npc_alert_states.values())

    def get_detection_level(self) -> float:
        """Get overall detection level (0.0 to 1.0)"""
        if not self.npc_alert_states:
            return 0.0

        alert_values = {
            AlertState.UNALERT: 0.0,
            AlertState.SUSPICIOUS: 0.3,
            AlertState.SEARCHING: 0.6,
            AlertState.ALERTED: 1.0
        }

        total = sum(alert_values[state] for state in self.npc_alert_states.values())
        return min(1.0, total / max(1, len(self.npc_alert_states)))
