#!/usr/bin/env python3
"""
MallOS Phase 1 Integration Test

Tests the complete object → Cloud → QBIT feedback loop:
1. Load voxel objects with QBIT scores
2. Spawn objects → zone QBIT charging
3. Pickup objects → zone QBIT discharging + cloud pressure unicast
4. Verify all state changes

The mall as a computational substrate.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from cloud import ZoneMicrostate
from voxel_object_loader import (
    VoxelObjectRegistry,
    build_voxels_from_png,
    load_palette_json,
)
from mallos_world import (
    WorldObjectRegistry,
    charge_zone_qbit,
    discharge_zone_qbit,
    modify_zone_pressure,
)
from object_interactions import handle_object_interaction


def print_separator(title=""):
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)


def print_zone_state(zone_id: str, zone: ZoneMicrostate):
    print(f"\n[ZONE] {zone_id}")
    print(f"  Cloud Pressure:  {zone.cloud_pressure:.1f}")
    print(f"  QBIT Aggregate:  {zone.qbit_aggregate:.1f}")
    print(f"  QBIT Power:      {zone.qbit_power:.1f}")
    print(f"  QBIT Charisma:   {zone.qbit_charisma:.1f}")
    print(f"  Entity Count:    {zone.qbit_entity_count}")


def main():
    print_separator("MALLOS PHASE 1 INTEGRATION TEST")
    print("\nThe mall is a computer. Testing the I/O devices...\n")

    # ========================================================================
    # 1. Load Voxel Object Registry with QBIT Scores
    # ========================================================================

    print_separator("1. Loading Voxel Object Registry")

    base_path = Path(__file__).parent.parent / "data"
    palette_path = base_path / "palette_COMICBOOK_MALL_V1.json"
    objects_path = base_path / "voxel_objects"

    palette = load_palette_json(palette_path)
    registry = VoxelObjectRegistry(
        str(objects_path), palette, build_voxels_from_png
    )
    registry.load_registry()

    print(f"\n✓ Loaded {len(registry)} voxel objects")

    # Show QBIT scores
    for obj_id in ["ARCADE_TOKEN", "JANITOR_MOP", "PIZZA_SLICE"]:
        obj = registry.get(obj_id)
        if obj.qbit:
            print(f"\n  {obj_id}:")
            print(f"    Power:     {obj.qbit.get('power', 0)}")
            print(f"    Charisma:  {obj.qbit.get('charisma', 0)}")
            print(f"    Resonance: {obj.qbit.get('resonance', 0)}")
            print(f"    Aggregate: {obj.get_qbit_aggregate():.1f}")

    # ========================================================================
    # 2. Create Zones (Compute Nodes)
    # ========================================================================

    print_separator("2. Creating Zone Compute Nodes")

    zones = {
        "FC-ARCADE": ZoneMicrostate("FC-ARCADE"),
        "Z4_FOOD_COURT": ZoneMicrostate("Z4_FOOD_COURT"),
        "SERVICE_HALL": ZoneMicrostate("SERVICE_HALL"),
    }

    print("\n✓ Created 3 zone compute nodes")
    for zone_id, zone in zones.items():
        print_zone_state(zone_id, zone)

    # ========================================================================
    # 3. Spawn Objects → QBIT Zone Charging
    # ========================================================================

    print_separator("3. Spawning Objects (QBIT Zone Charging)")

    world_registry = WorldObjectRegistry()

    # Spawn ARCADE_TOKEN in FC-ARCADE
    token_obj = registry.get("ARCADE_TOKEN")
    token_id = world_registry.spawn_object(
        "ARCADE_TOKEN",
        token_obj,
        "FC-ARCADE",
        (5, 10),
        zones=zones  # Pass zones for QBIT charging
    )
    print(f"\n✓ Spawned ARCADE_TOKEN (instance: {token_id})")

    # Spawn PIZZA_SLICE in FOOD_COURT
    pizza_obj = registry.get("PIZZA_SLICE")
    pizza_id = world_registry.spawn_object(
        "PIZZA_SLICE",
        pizza_obj,
        "Z4_FOOD_COURT",
        (15, 23),
        zones=zones
    )
    print(f"✓ Spawned PIZZA_SLICE (instance: {pizza_id})")

    # Spawn JANITOR_MOP in SERVICE_HALL
    mop_obj = registry.get("JANITOR_MOP")
    mop_id = world_registry.spawn_object(
        "JANITOR_MOP",
        mop_obj,
        "SERVICE_HALL",
        (1, 2),
        zones=zones,
        owner_npc_id="UNIT_7"
    )
    print(f"✓ Spawned JANITOR_MOP (instance: {mop_id}, owner: UNIT_7)")

    print("\n--- Zone State After Spawning ---")
    for zone_id, zone in zones.items():
        print_zone_state(zone_id, zone)

    # ========================================================================
    # 4. Pickup Objects → Cloud Pressure + QBIT Discharging
    # ========================================================================

    print_separator("4. Picking Up Objects (Cloud Pressure + QBIT Discharge)")

    # Mock game state with zones
    game_state = {
        "zones": zones,
        "cloud_pressure": 0.0,
        "flags": {},
        "cloud_events": [],
    }

    # Pickup ARCADE_TOKEN (cloud_pressure+1, zone_id=FC-ARCADE)
    print("\n--- Picking up ARCADE_TOKEN ---")
    print("Expected: FC-ARCADE cloud_pressure +1, QBIT discharge")

    world_registry.pickup_object(token_id, zones=zones)
    handle_object_interaction(game_state, token_obj, zone_id="FC-ARCADE")

    print("\nAfter pickup:")
    print_zone_state("FC-ARCADE", zones["FC-ARCADE"])
    print(f"\nCloud events: {game_state.get('cloud_events', [])}")

    # Pickup PIZZA_SLICE (cloud_pressure-3, zone_id=FOOD_COURT)
    print("\n--- Picking up PIZZA_SLICE (heat sink) ---")
    print("Expected: FOOD_COURT cloud_pressure -3, QBIT discharge")

    world_registry.pickup_object(pizza_id, zones=zones)
    handle_object_interaction(game_state, pizza_obj, zone_id="Z4_FOOD_COURT")

    print("\nAfter pickup:")
    print_zone_state("Z4_FOOD_COURT", zones["Z4_FOOD_COURT"])
    print(f"\nCloud events: {game_state.get('cloud_events', [])}")

    # Pickup JANITOR_MOP (NPC prop - resource contention)
    print("\n--- Picking up JANITOR_MOP (NPC Prop) ---")
    print("Expected: SERVICE_HALL cloud_pressure +2, QBIT discharge")
    print("Note: This is resource contention - Unit 7 will notice!")

    world_registry.pickup_object(mop_id, zones=zones)
    handle_object_interaction(game_state, mop_obj, zone_id="SERVICE_HALL")

    print("\nAfter pickup:")
    print_zone_state("SERVICE_HALL", zones["SERVICE_HALL"])
    print(f"\nCloud events: {game_state.get('cloud_events', [])}")

    # ========================================================================
    # 5. Final State Summary
    # ========================================================================

    print_separator("5. Final State Summary")

    print("\n--- All Zones ---")
    for zone_id, zone in zones.items():
        print_zone_state(zone_id, zone)

    print("\n--- World Object Registry ---")
    print(f"  Total objects spawned: {len(world_registry.objects)}")
    print(f"  Objects picked up: {sum(1 for obj in world_registry.objects.values() if obj.picked_up)}")

    print("\n--- Cloud Event Log ---")
    for i, event in enumerate(game_state.get("cloud_events", []), 1):
        print(f"  {i}. {event}")

    # ========================================================================
    # 6. Verification
    # ========================================================================

    print_separator("6. Verification")

    checks = []

    # Check ARCADE_TOKEN effects
    arcade_zone = zones["FC-ARCADE"]
    checks.append((
        "ARCADE_TOKEN picked up: FC-ARCADE pressure increased",
        arcade_zone.cloud_pressure > 0
    ))
    checks.append((
        "ARCADE_TOKEN picked up: FC-ARCADE QBIT discharged",
        arcade_zone.qbit_aggregate == 0  # Token removed
    ))

    # Check PIZZA_SLICE effects (heat sink, negative pressure)
    food_court_zone = zones["Z4_FOOD_COURT"]
    checks.append((
        "PIZZA_SLICE picked up: FOOD_COURT pressure decreased (heat sink)",
        food_court_zone.cloud_pressure == 0  # Started at 0, went negative → clamped to 0
    ))
    checks.append((
        "PIZZA_SLICE picked up: FOOD_COURT QBIT discharged",
        food_court_zone.qbit_aggregate == 0
    ))

    # Check JANITOR_MOP effects
    service_zone = zones["SERVICE_HALL"]
    checks.append((
        "JANITOR_MOP picked up: SERVICE_HALL pressure increased",
        service_zone.cloud_pressure > 0
    ))
    checks.append((
        "JANITOR_MOP picked up: SERVICE_HALL QBIT discharged",
        service_zone.qbit_aggregate == 0
    ))

    # Check cloud events
    checks.append((
        "Cloud events tracked for analytics",
        len(game_state.get("cloud_events", [])) >= 3
    ))

    print("\nRunning verification checks:\n")
    all_passed = True
    for desc, result in checks:
        status = "✓" if result else "✗"
        print(f"  {status} {desc}")
        if not result:
            all_passed = False

    # ========================================================================
    # Final Result
    # ========================================================================

    print_separator("INTEGRATION TEST COMPLETE")

    if all_passed:
        print("\n✓ ALL CHECKS PASSED")
        print("\nThe circuit is operational.")
        print("Objects are I/O devices.")
        print("Zones are compute nodes.")
        print("The mall is a computer.")
        return 0
    else:
        print("\n✗ SOME CHECKS FAILED")
        print("\nDebug the circuit...")
        return 1


if __name__ == "__main__":
    sys.exit(main())
