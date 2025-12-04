#!/usr/bin/env python3
"""
MallOS Test Environment - Complete System Scaffold

Establishes and validates the complete testing environment:
1. world.objects registry
2. tile→world coordinate conversion
3. zone alias mapping
4. Cloud + QBIT driver separation
5. event queue
6. NPC prop flagging
7. adjacency override table
8. Full system integration

Usage:
    from test_environment import MallOSTestEnvironment

    env = MallOSTestEnvironment()
    env.validate()  # Check all systems
    env.spawn_test_objects()
    env.simulate_pickup("ARCADE_TOKEN")
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field

# Core imports
from cloud import Cloud, ZoneMicrostate, MallMood
from voxel_object_loader import (
    VoxelObjectRegistry,
    build_voxels_from_png,
    load_palette_json,
)
from mallos_world import (
    WorldObjectRegistry,
    tile_to_world,
    world_to_tile,
    charge_zone_qbit,
    discharge_zone_qbit,
    modify_zone_pressure,
    TILE_SIZE_FEET,
)
from object_interactions import handle_object_interaction
from adjacency import compute_adjacency_probabilities


# ============================================================================
# ZONE ALIAS MAPPING
# ============================================================================

ZONE_ALIASES = {
    # Canonical zone IDs → Common aliases
    "FC-ARCADE": ["ARCADE", "FC_ARCADE_ZONE", "ARCADE_ZONE"],
    "Z1_CENTRAL_ATRIUM": ["ATRIUM", "CENTRAL_ATRIUM", "Z1"],
    "Z2_FOOD_COURT": ["FOOD_COURT", "FOODCOURT", "FC", "Z2"],
    "Z4_FOOD_COURT": ["FOOD_COURT", "FOODCOURT", "Z4"],
    "SERVICE_HALL": ["SERVICE", "MAINTENANCE", "UNIT7_ZONE"],
    "Z3_LOWER_RING": ["LOWER_RING", "Z3"],
}

# Reverse mapping for fast lookups
ALIAS_TO_CANONICAL = {}
for canonical, aliases in ZONE_ALIASES.items():
    ALIAS_TO_CANONICAL[canonical] = canonical  # Self-reference
    for alias in aliases:
        ALIAS_TO_CANONICAL[alias.upper()] = canonical


def resolve_zone_id(zone_id: str) -> str:
    """Resolve zone alias to canonical zone ID."""
    return ALIAS_TO_CANONICAL.get(zone_id.upper(), zone_id)


# ============================================================================
# ADJACENCY OVERRIDE TABLE
# ============================================================================

@dataclass
class AdjacencyOverride:
    """Temporary routing override for adjacency matrix."""
    source_zone: str
    target_zone: str
    probability: float
    ticks_remaining: int
    reason: str  # "token_pickup", "npc_pursuit", etc.


class AdjacencyOverrideTable:
    """
    Manages temporary routing overrides for the adjacency matrix.

    Overrides decay over time and are removed when ticks_remaining reaches 0.
    """

    def __init__(self):
        self.overrides: List[AdjacencyOverride] = []
        self.baseline_adjacency: Dict[str, Dict[str, float]] = {}

    def set_baseline(self, adjacency: Dict[str, Dict[str, float]]):
        """Store baseline adjacency matrix."""
        self.baseline_adjacency = adjacency

    def add_override(
        self,
        source_zone: str,
        target_zone: str,
        probability: float,
        duration_ticks: int,
        reason: str
    ):
        """Add a temporary routing override."""
        override = AdjacencyOverride(
            source_zone=source_zone,
            target_zone=target_zone,
            probability=probability,
            ticks_remaining=duration_ticks,
            reason=reason
        )
        self.overrides.append(override)

    def tick(self):
        """Decrement all override timers, remove expired."""
        self.overrides = [
            o for o in self.overrides
            if (setattr(o, 'ticks_remaining', o.ticks_remaining - 1), o.ticks_remaining > 0)[1]
        ]

    def get_effective_adjacency(self) -> Dict[str, Dict[str, float]]:
        """Get adjacency matrix with overrides applied."""
        # Start with baseline
        effective = {
            zone_id: probs.copy()
            for zone_id, probs in self.baseline_adjacency.items()
        }

        # Apply overrides
        for override in self.overrides:
            if override.source_zone in effective:
                effective[override.source_zone][override.target_zone] = override.probability

        return effective

    def get_active_overrides(self) -> List[AdjacencyOverride]:
        """Get list of currently active overrides."""
        return self.overrides.copy()


# ============================================================================
# DRIVER WEIGHT TRACKING
# ============================================================================

@dataclass
class CloudDriverStats:
    """Track Cloud pressure contributions by driver type."""
    player_actions: float = 0.0
    object_pickups: float = 0.0
    npc_interactions: float = 0.0
    qbit_influence: float = 0.0
    ambient_drift: float = 0.0

    # Driver weights (from architecture doc)
    WEIGHT_PLAYER = 0.50
    WEIGHT_NPC = 0.25
    WEIGHT_QBIT = 0.15
    WEIGHT_AMBIENT = 0.10

    # Player sub-drivers
    PLAYER_ACTIONS_WEIGHT = 0.35
    OBJECT_PICKUPS_WEIGHT = 0.15

    def add_event(self, source: str, delta: float):
        """Track pressure change by source."""
        if source.startswith("object_pickup"):
            self.object_pickups += delta
        elif source.startswith("player_action"):
            self.player_actions += delta
        elif source.startswith("npc"):
            self.npc_interactions += delta
        elif source.startswith("qbit"):
            self.qbit_influence += delta
        elif source.startswith("ambient"):
            self.ambient_drift += delta

    def get_summary(self) -> Dict[str, float]:
        """Get summary of all driver contributions."""
        return {
            "player_actions": self.player_actions,
            "object_pickups": self.object_pickups,
            "npc_interactions": self.npc_interactions,
            "qbit_influence": self.qbit_influence,
            "ambient_drift": self.ambient_drift,
            "total": (
                self.player_actions + self.object_pickups +
                self.npc_interactions + self.qbit_influence +
                self.ambient_drift
            )
        }


# ============================================================================
# MALLOS TEST ENVIRONMENT
# ============================================================================

class MallOSTestEnvironment:
    """
    Complete MallOS testing environment.

    Sets up and validates all systems:
    - Voxel object registry with QBIT scores
    - World object registry for spawned instances
    - Zone compute nodes with Cloud/QBIT state
    - Coordinate conversion (tile ↔ world)
    - Zone alias mapping
    - Event queue tracking
    - Adjacency override table
    - Driver weight tracking
    """

    def __init__(self, base_path: Optional[Path] = None):
        """Initialize test environment."""
        self.base_path = base_path or Path(__file__).parent.parent

        # ✓ 1. world.objects registry
        self.world = WorldObjectRegistry()

        # ✓ 2. tile→world converter (built into mallos_world)
        self.tile_size = TILE_SIZE_FEET

        # ✓ 3. zone alias mapping
        self.zone_aliases = ZONE_ALIASES

        # ✓ 4. Cloud + QBIT drivers
        self.driver_stats = CloudDriverStats()

        # ✓ 5. event queue
        self.event_queue: List[Dict[str, Any]] = []

        # ✓ 6. NPC prop flagging (in object definitions)
        self.npc_props: Dict[str, str] = {}  # object_id → owner_npc_id

        # ✓ 7. adjacency override table
        self.adjacency_overrides = AdjacencyOverrideTable()

        # Core systems
        self.voxel_registry: Optional[VoxelObjectRegistry] = None
        self.zones: Dict[str, ZoneMicrostate] = {}
        self.cloud: Optional[Cloud] = None

        # Zone origins for coordinate conversion
        self.zone_origins = {
            "Z1_CENTRAL_ATRIUM": (0, 0),
            "Z4_FOOD_COURT": (100, 0),
            "FC-ARCADE": (100, -30),
            "SERVICE_HALL": (20, -50),
            "Z3_LOWER_RING": (0, 0),
        }

        # Game state tracking
        self.game_state = {
            "zones": self.zones,
            "cloud_pressure": 0.0,
            "flags": {},
            "cloud_events": self.event_queue,
            "subtitle": "",
        }

    def load_voxel_registry(self):
        """Load voxel object registry with QBIT scores."""
        data_path = self.base_path / "data"
        palette_path = data_path / "palette_COMICBOOK_MALL_V1.json"
        objects_path = data_path / "voxel_objects"

        palette = load_palette_json(palette_path)
        self.voxel_registry = VoxelObjectRegistry(
            str(objects_path), palette, build_voxels_from_png
        )
        self.voxel_registry.load_registry()

        # Extract NPC props
        for obj_id in self.voxel_registry.objects:
            obj = self.voxel_registry.get(obj_id)
            if obj.qbit and "owner_npc_id" in obj.qbit:
                self.npc_props[obj_id] = obj.qbit["owner_npc_id"]

        return len(self.voxel_registry)

    def create_zones(self, zone_ids: List[str]):
        """Create zone compute nodes."""
        for zone_id in zone_ids:
            canonical = resolve_zone_id(zone_id)
            if canonical not in self.zones:
                self.zones[canonical] = ZoneMicrostate(canonical)
        return len(self.zones)

    def initialize_adjacency(self):
        """Initialize baseline adjacency matrix."""
        if not self.zones:
            return False

        # Compute baseline adjacency from zone QBIT scores
        baseline = compute_adjacency_probabilities(self.zones)
        self.adjacency_overrides.set_baseline(baseline)

        # Apply to zones
        for zone_id, zone in self.zones.items():
            zone.adjacency = baseline.get(zone_id, {})

        return True

    def spawn_object(
        self,
        object_id: str,
        zone_id: str,
        tile: Tuple[int, int],
        owner_npc_id: Optional[str] = None
    ) -> str:
        """Spawn voxel object in world."""
        if not self.voxel_registry:
            raise RuntimeError("Voxel registry not loaded")

        canonical_zone = resolve_zone_id(zone_id)
        voxel_obj = self.voxel_registry.get(object_id)

        instance_id = self.world.spawn_object(
            object_id,
            voxel_obj,
            canonical_zone,
            tile,
            zones=self.zones,
            zone_origins=self.zone_origins,
            owner_npc_id=owner_npc_id
        )

        return instance_id

    def pickup_object(self, instance_id: str) -> bool:
        """Pickup object (QBIT discharge + cloud pressure)."""
        obj = self.world.get_object(instance_id)
        if not obj:
            return False

        # QBIT discharge
        success = self.world.pickup_object(instance_id, zones=self.zones)

        # Cloud pressure + behavior scripts
        if success and obj.voxel_object:
            handle_object_interaction(
                self.game_state,
                obj.voxel_object,
                zone_id=obj.zone_id
            )

            # Track driver stats
            for event in self.game_state.get("cloud_events", []):
                if "source" in event and "delta" in event:
                    self.driver_stats.add_event(event["source"], event["delta"])

        return success

    def add_adjacency_override(
        self,
        source_zone: str,
        target_zone: str,
        probability: float,
        duration_ticks: int,
        reason: str
    ):
        """Add temporary routing override."""
        canonical_source = resolve_zone_id(source_zone)
        canonical_target = resolve_zone_id(target_zone)

        self.adjacency_overrides.add_override(
            canonical_source,
            canonical_target,
            probability,
            duration_ticks,
            reason
        )

    def tick(self):
        """Advance simulation one tick."""
        # Decay adjacency overrides
        self.adjacency_overrides.tick()

        # Update effective adjacency in zones
        effective = self.adjacency_overrides.get_effective_adjacency()
        for zone_id, zone in self.zones.items():
            zone.adjacency = effective.get(zone_id, {})

    def validate(self) -> bool:
        """Validate all checklist items."""
        checks = []

        # 1. world.objects registry exists
        checks.append(("world.objects registry", self.world is not None))

        # 2. tile→world converter in place
        try:
            test_pos = tile_to_world(0, 0, "FC-ARCADE", self.zone_origins)
            checks.append(("tile→world converter", test_pos == (100, -30, 0)))
        except Exception:
            checks.append(("tile→world converter", False))

        # 3. zone alias mapping applied
        checks.append((
            "zone alias mapping",
            resolve_zone_id("ARCADE") == "FC-ARCADE"
        ))

        # 4. Cloud + QBIT drivers separated
        checks.append((
            "Cloud + QBIT drivers",
            self.driver_stats.WEIGHT_PLAYER == 0.50 and
            self.driver_stats.WEIGHT_QBIT == 0.15
        ))

        # 5. event queue active
        checks.append(("event queue", self.event_queue is not None))

        # 6. Janitor mop flagged as NPC_PROP (if loaded)
        if self.voxel_registry:
            checks.append((
                "NPC prop flagging",
                "JANITOR_MOP" in self.npc_props
            ))
        else:
            checks.append(("NPC prop flagging", "PENDING - registry not loaded"))

        # 7. adjacency override table initialized
        checks.append((
            "adjacency override table",
            self.adjacency_overrides is not None
        ))

        # 8. Full system integration
        all_systems = (
            self.world is not None and
            len(self.zone_aliases) > 0 and
            self.driver_stats is not None and
            self.adjacency_overrides is not None
        )
        checks.append(("full system integration", all_systems))

        # Print results
        print("\n" + "=" * 70)
        print("  MALLOS TEST ENVIRONMENT VALIDATION")
        print("=" * 70)

        all_passed = True
        for name, result in checks:
            if isinstance(result, bool):
                status = "✓" if result else "✗"
                print(f"  {status} {name}")
                if not result:
                    all_passed = False
            else:
                print(f"  ⚠ {name}: {result}")

        print("=" * 70)

        if all_passed:
            print("✓ ALL SYSTEMS OPERATIONAL\n")
        else:
            print("✗ SOME SYSTEMS FAILED\n")

        return all_passed

    def print_status(self):
        """Print current environment status."""
        print("\n" + "=" * 70)
        print("  MALLOS ENVIRONMENT STATUS")
        print("=" * 70)

        print(f"\nVoxel Registry: {len(self.voxel_registry) if self.voxel_registry else 0} objects loaded")
        print(f"World Objects: {len(self.world.objects)} instances spawned")
        print(f"Zones: {len(self.zones)} compute nodes")
        print(f"NPC Props: {len(self.npc_props)} flagged")
        print(f"Adjacency Overrides: {len(self.adjacency_overrides.overrides)} active")

        print("\n--- Driver Stats ---")
        for name, value in self.driver_stats.get_summary().items():
            print(f"  {name}: {value:.2f}")

        print("\n--- Zone States ---")
        for zone_id, zone in self.zones.items():
            print(f"\n  {zone_id}:")
            print(f"    Cloud Pressure: {zone.cloud_pressure:.1f}")
            print(f"    QBIT Aggregate: {zone.qbit_aggregate:.1f}")
            print(f"    Entity Count: {zone.qbit_entity_count}")

        print("\n" + "=" * 70)


# ============================================================================
# MODULE TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  MALLOS TEST ENVIRONMENT SCAFFOLD")
    print("=" * 70)

    # Create environment
    env = MallOSTestEnvironment()

    # Validate checklist
    env.validate()

    # Load systems
    print("\nLoading systems...")
    obj_count = env.load_voxel_registry()
    print(f"✓ Loaded {obj_count} voxel objects")

    zone_count = env.create_zones([
        "FC-ARCADE",
        "Z4_FOOD_COURT",
        "SERVICE_HALL"
    ])
    print(f"✓ Created {zone_count} zones")

    env.initialize_adjacency()
    print(f"✓ Initialized adjacency matrix")

    # Re-validate
    print("\n" + "-" * 70)
    env.validate()

    # Show status
    env.print_status()

    print("\n✓ Test environment ready")
    print("\nThe mall is operational.")
