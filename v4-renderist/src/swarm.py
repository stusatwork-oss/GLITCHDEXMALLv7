#!/usr/bin/env python3
"""
SWARM SYSTEM - V4 Renderist Mall OS

The Swarm is the ambient crowd of non-canon customers.
They ARE the diegetic feedback - no UI needed.

Population curves based on Cloud mood:
- CALM: 40-60 customers
- UNEASY: 25-45 customers
- STRAINED: 10-30 customers
- CRITICAL: 0-15 customers

Swarm feedback is CONFIRMING ONLY (±5% cap).
Swarm cannot push Cloud across tier thresholds.
"Crowd is weather, not governance. Cloud stays sovereign."
"""

import json
import random
import time
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# LOCKED DECISION: Swarm feedback cap
MAX_SWARM_CONTRIBUTION = 0.05  # 5% cap on swarm feedback to Cloud


class SwarmMood(Enum):
    """Individual swarm member mood."""
    APATHETIC = "apathetic"    # Default mall zombie
    CURIOUS = "curious"        # Watching, lingering
    IRRITABLE = "irritable"    # Wanting to leave


@dataclass
class SwarmMember:
    """A single non-canon customer."""
    id: int
    mood: SwarmMood
    zone: str
    speed: float = 1.0
    direction: Tuple[float, float] = (0.0, 0.0)
    time_in_zone: float = 0.0
    color_beige: float = 0.0  # 0 = colorful, 1 = beige uniform


class SwarmSystem:
    """
    Manages the ambient crowd - the weather of the mall.

    Population scales inversely with Cloud pressure.
    Behavior patterns reflect Cloud mood diegetically.
    Feedback to Cloud is confirming-only, capped at ±5%.
    """

    # Population curves by mood
    POPULATION_CURVES = {
        "calm": (40, 60),
        "uneasy": (25, 45),
        "strained": (10, 30),
        "critical": (0, 15)
    }

    # Mood distribution shifts by Cloud level
    MOOD_SHIFTS = {
        "calm": {"apathetic": 0.6, "curious": 0.3, "irritable": 0.1},
        "uneasy": {"apathetic": 0.5, "curious": 0.2, "irritable": 0.3},
        "strained": {"apathetic": 0.3, "curious": 0.1, "irritable": 0.6},
        "critical": {"apathetic": 0.1, "curious": 0.1, "irritable": 0.8}
    }

    # Zones where swarm congregates
    CONGREGATION_ZONES = ["FOOD_COURT", "CORRIDOR", "ENTRANCE"]

    def __init__(self, zones: Optional[List[str]] = None):
        """Initialize swarm system."""
        self.members: List[SwarmMember] = []
        self.zones = zones or self._default_zones()
        self.target_population = 50
        self.current_population = 0

        # Zone density tracking
        self.density_by_zone: Dict[str, int] = {z: 0 for z in self.zones}

        # Mood distribution
        self.mood_distribution = {
            "apathetic": 0.6,
            "curious": 0.2,
            "irritable": 0.2
        }

        # Feedback accumulator (for Cloud delta)
        self._feedback_accumulator = 0.0
        self._last_cloud_direction = 0.0  # Track Cloud's direction

        # Member ID counter
        self._next_id = 0

    def _default_zones(self) -> List[str]:
        """Default zone list."""
        return [
            "FOOD_COURT", "SERVICE_HALL", "CORRIDOR", "ENTRANCE",
            "STORE_HARD_COPY", "STORE_BORED", "STORE_COMPHUT",
            "STORE_MILO_OPTICS", "STORE_FLAIR", "STORE_SPORTY",
            "CLINIC", "ANCHOR_STORE"
        ]

    def update(self, dt: float, cloud_level: float, cloud_mood: str,
               cloud_delta: float, zone_states: Dict) -> Dict:
        """
        Update swarm state based on Cloud conditions.

        Args:
            dt: Delta time in seconds
            cloud_level: Current Cloud pressure (0-100)
            cloud_mood: Current Cloud mood string
            cloud_delta: How much Cloud changed this tick (for direction)
            zone_states: Zone microstate dict

        Returns:
            Dict with swarm state and feedback for Cloud
        """
        # Track Cloud direction for confirming feedback
        self._last_cloud_direction = cloud_delta

        # Update target population based on mood
        pop_range = self.POPULATION_CURVES.get(cloud_mood, (30, 50))
        self.target_population = random.randint(pop_range[0], pop_range[1])

        # Adjust population toward target
        self._adjust_population()

        # Update mood distribution
        self.mood_distribution = self.MOOD_SHIFTS.get(
            cloud_mood,
            {"apathetic": 0.5, "curious": 0.25, "irritable": 0.25}
        )

        # Update individual members
        self._update_members(dt, cloud_level, zone_states)

        # Calculate zone densities
        self._calculate_densities()

        # Calculate feedback for Cloud (confirming only, ±5% cap)
        feedback = self._calculate_cloud_feedback(cloud_delta)

        return {
            "population": self.current_population,
            "target_population": self.target_population,
            "density_by_zone": self.density_by_zone.copy(),
            "mood_distribution": self.mood_distribution.copy(),
            "cloud_feedback": feedback,
            "behavior_hints": self._generate_behavior_hints(cloud_level)
        }

    def _adjust_population(self):
        """Spawn or despawn members to reach target."""
        current = len(self.members)

        if current < self.target_population:
            # Spawn new members
            to_spawn = min(5, self.target_population - current)  # Max 5 per tick
            for _ in range(to_spawn):
                self._spawn_member()
        elif current > self.target_population:
            # Despawn members (irritable leave first)
            to_remove = min(5, current - self.target_population)
            self._despawn_members(to_remove)

        self.current_population = len(self.members)

    def _spawn_member(self):
        """Spawn a new swarm member."""
        # Determine mood based on distribution
        mood = self._random_mood()

        # Spawn in congregation zones preferentially
        if random.random() < 0.7:
            zone = random.choice(self.CONGREGATION_ZONES)
        else:
            zone = random.choice(self.zones)

        member = SwarmMember(
            id=self._next_id,
            mood=mood,
            zone=zone,
            speed=random.uniform(0.8, 1.2),
            color_beige=random.uniform(0.0, 0.3)
        )
        self._next_id += 1
        self.members.append(member)

    def _despawn_members(self, count: int):
        """Remove members (irritable first, then apathetic)."""
        # Sort by mood priority for despawning
        priority = {
            SwarmMood.IRRITABLE: 0,
            SwarmMood.APATHETIC: 1,
            SwarmMood.CURIOUS: 2
        }
        self.members.sort(key=lambda m: priority.get(m.mood, 1))

        # Remove from front (highest priority to leave)
        self.members = self.members[count:]

    def _random_mood(self) -> SwarmMood:
        """Pick a random mood based on distribution."""
        r = random.random()
        cumulative = 0.0

        for mood_name, prob in self.mood_distribution.items():
            cumulative += prob
            if r <= cumulative:
                return SwarmMood(mood_name)

        return SwarmMood.APATHETIC

    def _update_members(self, dt: float, cloud_level: float, zone_states: Dict):
        """Update individual member states."""
        for member in self.members:
            # Update time in zone
            member.time_in_zone += dt

            # Color uniformity increases with Cloud level
            target_beige = cloud_level / 100
            member.color_beige += (target_beige - member.color_beige) * 0.1 * dt

            # Possibly move to different zone
            if random.random() < 0.01 * dt:  # ~1% chance per second
                self._move_member(member, zone_states)

            # Mood can shift based on local turbulence
            zone_data = zone_states.get(member.zone, {})
            turbulence = zone_data.get("turbulence", 0) if isinstance(zone_data, dict) else 0

            if turbulence > 6 and member.mood != SwarmMood.IRRITABLE:
                if random.random() < 0.05 * dt:
                    member.mood = SwarmMood.IRRITABLE

    def _move_member(self, member: SwarmMember, zone_states: Dict):
        """Move a member to a different zone."""
        # Check avoidance from zone swarm_bias
        avoided = []
        for zone_id, zone_data in zone_states.items():
            if isinstance(zone_data, dict):
                bias = zone_data.get("swarm_bias", {})
                avoided.extend(bias.get("avoidance", []))

        # Available zones
        available = [z for z in self.zones if z not in avoided]
        if not available:
            available = self.zones

        # Weight toward congregation zones
        if member.mood == SwarmMood.CURIOUS:
            weights = [3 if z in self.CONGREGATION_ZONES else 1 for z in available]
        elif member.mood == SwarmMood.IRRITABLE:
            # Irritable head toward exit
            weights = [5 if z == "ENTRANCE" else 1 for z in available]
        else:
            weights = [2 if z in self.CONGREGATION_ZONES else 1 for z in available]

        member.zone = random.choices(available, weights=weights)[0]
        member.time_in_zone = 0.0

    def _calculate_densities(self):
        """Calculate population density per zone."""
        self.density_by_zone = {z: 0 for z in self.zones}

        for member in self.members:
            if member.zone in self.density_by_zone:
                self.density_by_zone[member.zone] += 1

    def _calculate_cloud_feedback(self, cloud_delta: float) -> float:
        """
        Calculate swarm feedback to Cloud.

        LOCKED DECISION: Confirming only, ±5% cap.
        Swarm can reinforce Cloud direction but never reverse it
        or push it across tier thresholds.
        """
        # Count irritable ratio
        if not self.members:
            return 0.0

        irritable_count = sum(1 for m in self.members if m.mood == SwarmMood.IRRITABLE)
        irritable_ratio = irritable_count / len(self.members)

        # Base feedback from crowd mood
        # More irritable = more upward pressure
        raw_feedback = (irritable_ratio - 0.3) * 0.1  # Centered around 30% irritable

        # LOCKED: Confirming only - must match Cloud direction
        if cloud_delta > 0:
            # Cloud rising - only allow positive feedback
            raw_feedback = max(0, raw_feedback)
        elif cloud_delta < 0:
            # Cloud falling - only allow negative feedback
            raw_feedback = min(0, raw_feedback)
        else:
            # Cloud stable - minimal feedback
            raw_feedback *= 0.5

        # LOCKED: Cap at ±5%
        capped_feedback = max(-MAX_SWARM_CONTRIBUTION,
                             min(MAX_SWARM_CONTRIBUTION, raw_feedback))

        return capped_feedback

    def _generate_behavior_hints(self, cloud_level: float) -> Dict:
        """Generate behavior hints for rendering."""
        return {
            # Clustering: moderate at mid-levels, scatter at high
            "clustering": 0.3 if cloud_level < 70 else 0.1,

            # Speed: faster at higher Cloud
            "speed_multiplier": 1.0 + (cloud_level / 200),

            # Stare: customers look at player at high levels
            "stare_chance": max(0, (cloud_level - 50) / 100),

            # Freeze: momentary stops at critical
            "freeze_chance": max(0, (cloud_level - 75) / 50),

            # Color uniformity (beige-ification)
            "avg_beige": sum(m.color_beige for m in self.members) / max(1, len(self.members))
        }

    def get_zone_density(self, zone_id: str) -> int:
        """Get customer count in a specific zone."""
        return self.density_by_zone.get(zone_id, 0)

    def get_status(self) -> str:
        """Get human-readable status."""
        mood_counts = {m.value: 0 for m in SwarmMood}
        for member in self.members:
            mood_counts[member.mood.value] += 1

        return (
            f"Population: {self.current_population}/{self.target_population}\n"
            f"Moods: {mood_counts}\n"
            f"Top zones: {sorted(self.density_by_zone.items(), key=lambda x: -x[1])[:3]}"
        )

    def to_dict(self) -> Dict:
        """Serialize for spine output."""
        return {
            "population": self.current_population,
            "target_population": self.target_population,
            "density_by_zone": self.density_by_zone.copy(),
            "mood_distribution": self.mood_distribution.copy()
        }


# ========== MODULE INTERFACE ==========

def create_swarm(zones: Optional[List[str]] = None) -> SwarmSystem:
    """Factory function to create Swarm system."""
    return SwarmSystem(zones=zones)


if __name__ == "__main__":
    # Test Swarm system
    print("=" * 60)
    print("SWARM SYSTEM - V4 Renderist Mall OS")
    print("=" * 60)

    swarm = SwarmSystem()

    print("\nInitial state:")
    print(swarm.get_status())

    # Simulate updates at different Cloud levels
    print("\n--- Simulating CALM (Cloud=20) ---")
    for _ in range(10):
        result = swarm.update(0.1, 20, "calm", 0.1, {})
    print(swarm.get_status())
    print(f"Cloud feedback: {result['cloud_feedback']:.4f}")

    print("\n--- Simulating STRAINED (Cloud=60) ---")
    for _ in range(20):
        result = swarm.update(0.1, 60, "strained", 0.5, {})
    print(swarm.get_status())
    print(f"Cloud feedback: {result['cloud_feedback']:.4f}")

    print("\n--- Simulating CRITICAL (Cloud=85) ---")
    for _ in range(30):
        result = swarm.update(0.1, 85, "critical", 0.2, {})
    print(swarm.get_status())
    print(f"Cloud feedback: {result['cloud_feedback']:.4f}")

    print("\n--- Behavior hints at critical ---")
    for k, v in result['behavior_hints'].items():
        print(f"  {k}: {v:.3f}" if isinstance(v, float) else f"  {k}: {v}")
