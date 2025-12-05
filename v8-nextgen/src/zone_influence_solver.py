#!/usr/bin/env python3
"""
INFLUENCE SPINE ↔ ZONE CONTROLLER
Step 3 of 5-part integration

Creates feedback loop: NPC → Zone → NPC
Zones become "vessels" of emotional physics.
Crowd density becomes meaningful. NPC charisma finally does something mechanical.

Architecture:
- Zones recalculate pressure based on entities inside
- Entity QBIT scores (charisma, power) affect zone state
- "Wattitude" (entity mood/energy) amplifies influence
- Creates emergent hotspots and dead zones

Usage:
    from zone_influence_solver import ZoneInfluenceSolver

    solver = ZoneInfluenceSolver()
    solver.add_entity_to_zone("FC-ARCADE", entity_id="leon", charisma=2400, wattitude=0.8)
    solver.solve_zone_pressure("FC-ARCADE")

    pressure = solver.get_zone_pressure("FC-ARCADE")  # Amplified by Leon's presence

Reference:
- QBIT Influence Spine
- Version Matrix (zone authority)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional
import math


@dataclass
class EntityPresence:
    """
    Entity's influence contribution to a zone.

    Attributes:
        entity_id: Unique identifier
        qbit_charisma: Charisma score (0-3000)
        qbit_power: Power score (0-3000)
        wattitude: Energy/mood multiplier (-1 to 1)
        duration: How long in zone (seconds)
        intensity: How active they are (0-1)
    """
    entity_id: str
    qbit_charisma: float = 0.0
    qbit_power: float = 0.0
    wattitude: float = 0.0      # -1 (hostile) to 1 (positive)
    duration: float = 0.0        # Time in zone (seconds)
    intensity: float = 0.5       # Activity level (0=idle, 1=very active)

    def get_influence_contribution(self) -> float:
        """
        Calculate this entity's pressure contribution.

        Formula:
            base = charisma * wattitude
            amplifier = intensity * (1 + duration_bonus)
            contribution = base * amplifier

        Returns:
            Pressure contribution (can be negative)
        """
        # Base influence from charisma + mood
        base = self.qbit_charisma * self.wattitude

        # Duration bonus (longer presence = more influence)
        # Caps at 2x after 300 seconds (5 minutes)
        duration_bonus = min(1.0, self.duration / 300.0)

        # Activity amplifier
        amplifier = self.intensity * (1.0 + duration_bonus)

        return base * amplifier / 1000.0  # Normalize


@dataclass
class ZoneState:
    """
    Zone emotional physics state.

    Attributes:
        zone_id: Zone identifier
        base_pressure: Baseline Cloud pressure (0-100)
        entity_pressure: Pressure from entities (calculated)
        total_pressure: Combined pressure
        entity_count: Number of entities present
        turbulence: Local chaos/instability (0-10)
        dominant_wattitude: Average mood of zone (-1 to 1)
    """
    zone_id: str
    base_pressure: float = 0.0
    entity_pressure: float = 0.0
    total_pressure: float = 0.0
    entity_count: int = 0
    turbulence: float = 0.0
    dominant_wattitude: float = 0.0

    # Tracking
    entities: Dict[str, EntityPresence] = field(default_factory=dict)
    high_influence_entities: List[str] = field(default_factory=list)


class ZoneInfluenceSolver:
    """
    Solver that recalculates zone pressure based on entity influence.

    This creates the feedback loop:
    1. Entities enter zone with QBIT scores + wattitude
    2. Zone pressure = base + Σ(entity.charisma * entity.wattitude)
    3. Zone pressure affects entities (via QBIT→Vector bridge)
    4. Entity behavior changes, feeding back into zone

    Result: Emergent hotspots, emotional contagion, crowd dynamics
    """

    def __init__(self):
        self.zones: Dict[str, ZoneState] = {}

        # Configuration
        self.crowd_density_threshold = 10  # When crowding effects kick in
        self.charisma_weight = 1.0         # How much charisma affects pressure
        self.wattitude_amplifier = 2.0     # How much mood amplifies
        self.turbulence_decay = 0.95       # Per-tick turbulence decay

    def register_zone(self, zone_id: str, base_pressure: float = 0.0):
        """Register a zone for tracking."""
        if zone_id not in self.zones:
            self.zones[zone_id] = ZoneState(
                zone_id=zone_id,
                base_pressure=base_pressure
            )

    def add_entity_to_zone(
        self,
        zone_id: str,
        entity_id: str,
        charisma: float = 0.0,
        power: float = 0.0,
        wattitude: float = 0.0,
        intensity: float = 0.5
    ):
        """
        Add entity to zone influence calculation.

        Args:
            zone_id: Target zone
            entity_id: Entity identifier
            charisma: QBIT charisma score (0-3000)
            power: QBIT power score (0-3000)
            wattitude: Mood/energy (-1 to 1)
            intensity: Activity level (0-1)
        """
        if zone_id not in self.zones:
            self.register_zone(zone_id)

        zone = self.zones[zone_id]

        # Create or update entity presence
        if entity_id in zone.entities:
            # Update existing
            presence = zone.entities[entity_id]
            presence.qbit_charisma = charisma
            presence.qbit_power = power
            presence.wattitude = wattitude
            presence.intensity = intensity
            presence.duration += 1.0  # Increment (actual dt should be passed)
        else:
            # New entity
            zone.entities[entity_id] = EntityPresence(
                entity_id=entity_id,
                qbit_charisma=charisma,
                qbit_power=power,
                wattitude=wattitude,
                intensity=intensity,
                duration=0.0
            )

        zone.entity_count = len(zone.entities)

    def remove_entity_from_zone(self, zone_id: str, entity_id: str):
        """Remove entity from zone."""
        if zone_id in self.zones and entity_id in self.zones[zone_id].entities:
            del self.zones[zone_id].entities[entity_id]
            self.zones[zone_id].entity_count = len(self.zones[zone_id].entities)

    def solve_zone_pressure(self, zone_id: str) -> float:
        """
        Solve zone pressure equation:
            total_pressure = base_pressure + Σ(entity.charisma * entity.wattitude * intensity)

        Also calculates:
        - Turbulence (from conflicting wattitudes)
        - Dominant wattitude (average mood)
        - High-influence entities

        Returns:
            Total zone pressure (0-100+)
        """
        if zone_id not in self.zones:
            return 0.0

        zone = self.zones[zone_id]

        # Base pressure from global Cloud
        total = zone.base_pressure

        # Entity contributions
        entity_contributions = []
        wattitudes = []

        for entity in zone.entities.values():
            contribution = entity.get_influence_contribution()
            entity_contributions.append((entity.entity_id, contribution))
            wattitudes.append(entity.wattitude)

            # Add to total (can be negative)
            total += contribution * self.charisma_weight

        # Store entity pressure component
        zone.entity_pressure = sum(c for _, c in entity_contributions) * self.charisma_weight

        # Clamp total pressure (but allow negative from very negative wattitude)
        zone.total_pressure = max(0.0, min(100.0, total))

        # Calculate turbulence (variance in wattitudes = conflict)
        if wattitudes:
            mean_watt = sum(wattitudes) / len(wattitudes)
            variance = sum((w - mean_watt) ** 2 for w in wattitudes) / len(wattitudes)
            zone.turbulence = math.sqrt(variance) * 10.0  # Scale to 0-10
            zone.dominant_wattitude = mean_watt
        else:
            zone.turbulence *= self.turbulence_decay
            zone.dominant_wattitude = 0.0

        # Crowding amplification
        if zone.entity_count > self.crowd_density_threshold:
            crowd_factor = 1.0 + (zone.entity_count - self.crowd_density_threshold) * 0.05
            zone.total_pressure *= crowd_factor
            zone.turbulence *= crowd_factor

        # Identify high-influence entities
        zone.high_influence_entities = [
            eid for eid, contrib in entity_contributions
            if abs(contrib) > 1.0  # Threshold for "significant"
        ]

        return zone.total_pressure

    def solve_all_zones(self):
        """Solve pressure for all registered zones."""
        for zone_id in self.zones:
            self.solve_zone_pressure(zone_id)

    def get_zone_pressure(self, zone_id: str) -> float:
        """Get total pressure for a zone."""
        if zone_id in self.zones:
            return self.zones[zone_id].total_pressure
        return 0.0

    def get_zone_state(self, zone_id: str) -> Optional[ZoneState]:
        """Get full zone state."""
        return self.zones.get(zone_id)

    def get_entity_influence_in_zone(self, zone_id: str, entity_id: str) -> float:
        """Get specific entity's influence contribution."""
        if zone_id in self.zones and entity_id in self.zones[zone_id].entities:
            return self.zones[zone_id].entities[entity_id].get_influence_contribution()
        return 0.0

    def propagate_pressure_to_adjacent_zones(
        self,
        zone_id: str,
        adjacent_zones: List[str],
        propagation_rate: float = 0.3
    ):
        """
        Propagate pressure to adjacent zones.

        High-pressure zones bleed into neighbors.

        Args:
            zone_id: Source zone
            adjacent_zones: List of neighbor zone IDs
            propagation_rate: How much pressure spreads (0-1)
        """
        if zone_id not in self.zones:
            return

        source = self.zones[zone_id]
        excess_pressure = max(0, source.total_pressure - source.base_pressure)

        for adj_id in adjacent_zones:
            if adj_id not in self.zones:
                self.register_zone(adj_id)

            # Add a fraction of excess pressure to adjacent zone
            self.zones[adj_id].base_pressure += excess_pressure * propagation_rate


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("ZONE INFLUENCE SOLVER TEST")
    print("="*60)

    solver = ZoneInfluenceSolver()

    # Register zones
    solver.register_zone("FC-ARCADE", base_pressure=30.0)
    solver.register_zone("CORRIDOR", base_pressure=20.0)

    print("\n--- Initial State ---")
    print(f"FC-ARCADE: {solver.get_zone_pressure('FC-ARCADE'):.1f}")
    print(f"CORRIDOR: {solver.get_zone_pressure('CORRIDOR'):.1f}")

    # Add Leisurely Leon (high charisma, positive wattitude)
    print("\n--- Leon Enters FC-ARCADE ---")
    solver.add_entity_to_zone(
        "FC-ARCADE",
        entity_id="leon",
        charisma=2400,
        power=800,
        wattitude=0.8,  # Positive energy
        intensity=0.6
    )
    solver.solve_zone_pressure("FC-ARCADE")

    state = solver.get_zone_state("FC-ARCADE")
    print(f"  Total Pressure: {state.total_pressure:.1f}")
    print(f"  Entity Pressure: {state.entity_pressure:.1f}")
    print(f"  Entity Count: {state.entity_count}")
    print(f"  Dominant Wattitude: {state.dominant_wattitude:.2f}")

    # Add Shadow Janitor (medium charisma, negative wattitude)
    print("\n--- Janitor Enters FC-ARCADE (Hostile) ---")
    solver.add_entity_to_zone(
        "FC-ARCADE",
        entity_id="janitor",
        charisma=1200,
        power=1800,
        wattitude=-0.6,  # Hostile energy
        intensity=0.8
    )
    solver.solve_zone_pressure("FC-ARCADE")

    state = solver.get_zone_state("FC-ARCADE")
    print(f"  Total Pressure: {state.total_pressure:.1f}")
    print(f"  Entity Pressure: {state.entity_pressure:.1f}")
    print(f"  Turbulence: {state.turbulence:.1f} (conflict!)")
    print(f"  Dominant Wattitude: {state.dominant_wattitude:.2f}")
    print(f"  High-Influence Entities: {state.high_influence_entities}")

    # Crowding effect
    print("\n--- Add 15 Generic Shoppers (Crowding) ---")
    for i in range(15):
        solver.add_entity_to_zone(
            "FC-ARCADE",
            entity_id=f"shopper-{i}",
            charisma=300,
            power=100,
            wattitude=0.2,
            intensity=0.4
        )
    solver.solve_zone_pressure("FC-ARCADE")

    state = solver.get_zone_state("FC-ARCADE")
    print(f"  Total Pressure: {state.total_pressure:.1f} (crowding amplification)")
    print(f"  Entity Count: {state.entity_count}")

    # Pressure propagation
    print("\n--- Pressure Propagates to CORRIDOR ---")
    solver.propagate_pressure_to_adjacent_zones(
        "FC-ARCADE",
        ["CORRIDOR"],
        propagation_rate=0.3
    )
    solver.solve_zone_pressure("CORRIDOR")
    print(f"  CORRIDOR Pressure: {solver.get_zone_pressure('CORRIDOR'):.1f}")

    print("\n" + "="*60)
    print("FEEDBACK LOOP COMPLETE")
    print("NPC → Zone → NPC emotional physics")
    print("="*60)
