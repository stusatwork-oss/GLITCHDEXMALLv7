#!/usr/bin/env python3
"""
🧪 BAREMETALMONK Integration Test Protocol v0.1

Formal integration tests with state delta tracking and outcome classification.

Test vectors:
1. ARCADE_TOKEN pickup → Cloud/QBIT → zone effect → event tracking
2. JANITOR_MOP stolen → resource conflict → NPC state change
3. PIZZA_SLICE consumed → heat sink → local cooling effect

Outcome classification:
- PASS: Expected substrate behavior
- WEAK PASS: Correct behavior but wrong propagation
- DRIFT: System did something right, but for the wrong reason
- FAIL: Logic/ordering error
- STRUCTURAL CONCERN: Architecture mismatch, not a code bug
"""

import sys
from pathlib import Path
from typing import Dict, Any, Tuple
from copy import deepcopy

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from test_environment import MallOSTestEnvironment


# ============================================================================
# STATE DELTA CAPTURE
# ============================================================================

def capture_state(env: MallOSTestEnvironment) -> Dict[str, Any]:
    """Capture current substrate state."""
    return {
        "zones": {
            zone_id: {
                "cloud_pressure": zone.cloud_pressure,
                "qbit_aggregate": zone.qbit_aggregate,
                "qbit_power": zone.qbit_power,
                "qbit_charisma": zone.qbit_charisma,
                "qbit_entity_count": zone.qbit_entity_count,
                "adjacency": deepcopy(zone.adjacency),
            }
            for zone_id, zone in env.zones.items()
        },
        "world_objects": {
            iid: {
                "object_id": obj.object_id,
                "zone_id": obj.zone_id,
                "picked_up": obj.picked_up,
            }
            for iid, obj in env.world.objects.items()
        },
        "driver_stats": env.driver_stats.get_summary(),
        "event_queue": len(env.event_queue),
        "adjacency_overrides": len(env.adjacency_overrides.overrides),
    }


def compute_delta(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    """Compute state delta between before/after."""
    delta = {"zones": {}, "world_objects": {}, "driver_stats": {}}

    # Zone deltas
    for zone_id in before["zones"]:
        if zone_id in after["zones"]:
            zone_delta = {}
            for key in ["cloud_pressure", "qbit_aggregate", "qbit_power", "qbit_charisma", "qbit_entity_count"]:
                before_val = before["zones"][zone_id][key]
                after_val = after["zones"][zone_id][key]
                if before_val != after_val:
                    zone_delta[key] = after_val - before_val
            if zone_delta:
                delta["zones"][zone_id] = zone_delta

    # Driver stats deltas
    for key in before["driver_stats"]:
        before_val = before["driver_stats"][key]
        after_val = after["driver_stats"][key]
        if before_val != after_val:
            delta["driver_stats"][key] = after_val - before_val

    # Object state changes
    for iid in before["world_objects"]:
        if iid in after["world_objects"]:
            if before["world_objects"][iid]["picked_up"] != after["world_objects"][iid]["picked_up"]:
                delta["world_objects"][iid] = "picked_up"

    delta["event_queue_delta"] = after["event_queue"] - before["event_queue"]
    delta["adjacency_override_delta"] = after["adjacency_overrides"] - before["adjacency_overrides"]

    return delta


def print_delta(delta: Dict[str, Any], test_name: str):
    """Print state delta in clean format."""
    print(f"\n{'='*70}")
    print(f"  STATE DELTA: {test_name}")
    print('='*70)

    if delta["zones"]:
        print("\n[ZONE CHANGES]")
        for zone_id, changes in delta["zones"].items():
            print(f"  {zone_id}:")
            for key, value in changes.items():
                sign = "+" if value > 0 else ""
                print(f"    {key}: {sign}{value:.1f}")

    if delta["driver_stats"]:
        print("\n[DRIVER STATS]")
        for key, value in delta["driver_stats"].items():
            sign = "+" if value > 0 else ""
            print(f"  {key}: {sign}{value:.2f}")

    if delta["world_objects"]:
        print("\n[OBJECT STATE]")
        for iid, change in delta["world_objects"].items():
            print(f"  {iid}: {change}")

    if delta["event_queue_delta"]:
        print(f"\n[EVENT QUEUE] +{delta['event_queue_delta']} events")

    if delta["adjacency_override_delta"]:
        print(f"\n[ADJACENCY OVERRIDES] {delta['adjacency_override_delta']:+d} overrides")

    print('='*70)


# ============================================================================
# TEST OUTCOME CLASSIFICATION
# ============================================================================

class TestOutcome:
    PASS = "PASS"
    WEAK_PASS = "WEAK PASS"
    DRIFT = "DRIFT"
    FAIL = "FAIL"
    STRUCTURAL_CONCERN = "STRUCTURAL CONCERN"


def classify_outcome(
    test_name: str,
    delta: Dict[str, Any],
    expected: Dict[str, Any],
    verbose: bool = True
) -> Tuple[str, str]:
    """
    Classify test outcome.

    Returns:
        (outcome, reason)
    """
    issues = []

    # Check zone effects
    for zone_id, expected_changes in expected.get("zones", {}).items():
        actual_changes = delta["zones"].get(zone_id, {})

        for key, expected_value in expected_changes.items():
            actual_value = actual_changes.get(key, 0)

            if abs(actual_value - expected_value) < 0.01:
                continue  # Match
            else:
                issues.append(f"{zone_id}.{key}: expected {expected_value:+.1f}, got {actual_value:+.1f}")

    # Check driver stats
    for key, expected_value in expected.get("driver_stats", {}).items():
        actual_value = delta["driver_stats"].get(key, 0)
        if abs(actual_value - expected_value) > 0.01:
            issues.append(f"driver.{key}: expected {expected_value:+.2f}, got {actual_value:+.2f}")

    # Check propagation scope
    expected_scope = expected.get("propagation_scope", "unicast")
    if expected_scope == "unicast":
        # Should affect only one zone
        if len(delta["zones"]) > 1:
            issues.append(f"propagation: expected unicast, affected {len(delta['zones'])} zones")

    # Classify
    if not issues:
        return (TestOutcome.PASS, "All substrate effects match expectations")

    # Check if it's just wrong propagation
    if all("propagation" in issue for issue in issues):
        return (TestOutcome.WEAK_PASS, f"Correct behavior but wrong propagation: {', '.join(issues)}")

    # Check if values are close but not exact
    if all("expected" in issue and "got" in issue for issue in issues):
        return (TestOutcome.DRIFT, f"Values drifted from expected: {', '.join(issues)}")

    return (TestOutcome.FAIL, f"Logic/ordering error: {', '.join(issues)}")


def print_outcome(outcome: str, reason: str, test_name: str):
    """Print test outcome."""
    symbols = {
        TestOutcome.PASS: "✓",
        TestOutcome.WEAK_PASS: "⚠",
        TestOutcome.DRIFT: "~",
        TestOutcome.FAIL: "✗",
        TestOutcome.STRUCTURAL_CONCERN: "⚡",
    }

    symbol = symbols.get(outcome, "?")
    print(f"\n{symbol} [{outcome}] {test_name}")
    print(f"  → {reason}\n")


# ============================================================================
# TEST VECTORS
# ============================================================================

def test_arcade_token_pickup(env: MallOSTestEnvironment):
    """
    Test Vector 1: ARCADE_TOKEN pickup

    Expected behavior:
    - Spawn: FC-ARCADE QBIT += 970 (power=50 + charisma=800 + resonance=120)
    - Pickup: FC-ARCADE QBIT -= 970, cloud_pressure += 1
    - Propagation: UNICAST (only FC-ARCADE affected)
    - Driver: object_pickups += 1
    """
    print("\n" + "="*70)
    print("  TEST VECTOR 1: ARCADE_TOKEN Pickup")
    print("="*70)

    # Spawn token
    token_id = env.spawn_object("ARCADE_TOKEN", "FC-ARCADE", (5, 10))

    # Capture before state
    before = capture_state(env)

    # Execute: Pickup token
    env.pickup_object(token_id)

    # Capture after state
    after = capture_state(env)

    # Compute delta
    delta = compute_delta(before, after)
    print_delta(delta, "ARCADE_TOKEN Pickup")

    # Expected state changes
    expected = {
        "zones": {
            "FC-ARCADE": {
                "cloud_pressure": +1.0,
                "qbit_aggregate": -970.0,
                "qbit_power": -50.0,
                "qbit_charisma": -800.0,
                "qbit_entity_count": -1,
            }
        },
        "driver_stats": {
            "object_pickups": +1.0,
        },
        "propagation_scope": "unicast",
    }

    # Classify outcome
    outcome, reason = classify_outcome("ARCADE_TOKEN Pickup", delta, expected)
    print_outcome(outcome, reason, "ARCADE_TOKEN Pickup")

    return outcome == TestOutcome.PASS


def test_pizza_slice_heat_sink(env: MallOSTestEnvironment):
    """
    Test Vector 2: PIZZA_SLICE heat sink

    Expected behavior:
    - Spawn: FOOD_COURT QBIT += 100 (power=20 + charisma=50 + resonance=30)
    - Pickup: FOOD_COURT QBIT -= 100, cloud_pressure -= 3 (heat sink)
    - Propagation: UNICAST (only FOOD_COURT affected, local cooling)
    - Driver: object_pickups -= 3
    """
    print("\n" + "="*70)
    print("  TEST VECTOR 2: PIZZA_SLICE Heat Sink")
    print("="*70)

    # Spawn pizza
    pizza_id = env.spawn_object("PIZZA_SLICE", "Z4_FOOD_COURT", (15, 23))

    # Capture before state
    before = capture_state(env)

    # Execute: Pickup pizza
    env.pickup_object(pizza_id)

    # Capture after state
    after = capture_state(env)

    # Compute delta
    delta = compute_delta(before, after)
    print_delta(delta, "PIZZA_SLICE Heat Sink")

    # Expected state changes
    expected = {
        "zones": {
            "Z4_FOOD_COURT": {
                "cloud_pressure": -3.0,  # Heat sink (clamped to 0 if starting at 0)
                "qbit_aggregate": -100.0,
                "qbit_power": -20.0,
                "qbit_charisma": -50.0,
                "qbit_entity_count": -1,
            }
        },
        "driver_stats": {
            "object_pickups": -3.0,
        },
        "propagation_scope": "unicast",
    }

    # Classify outcome (special case: pressure can't go below 0)
    actual_pressure_delta = delta["zones"].get("Z4_FOOD_COURT", {}).get("cloud_pressure", 0)
    if actual_pressure_delta == 0 and before["zones"]["Z4_FOOD_COURT"]["cloud_pressure"] == 0:
        # Pressure was already 0, clamped correctly
        expected["zones"]["Z4_FOOD_COURT"]["cloud_pressure"] = 0.0

    outcome, reason = classify_outcome("PIZZA_SLICE Heat Sink", delta, expected)
    print_outcome(outcome, reason, "PIZZA_SLICE Heat Sink")

    return outcome == TestOutcome.PASS


def test_janitor_mop_resource_conflict(env: MallOSTestEnvironment):
    """
    Test Vector 3: JANITOR_MOP resource conflict

    Expected behavior:
    - Spawn: SERVICE_HALL QBIT += 680 (power=500 + charisma=100 + resonance=80)
    - Pickup: SERVICE_HALL QBIT -= 680, cloud_pressure += 2
    - NPC prop flag: owner_npc_id = "UNIT_7"
    - Propagation: UNICAST (only SERVICE_HALL affected)
    - Driver: object_pickups += 2
    - Resource conflict: UNIT_7 should detect missing equipment (future)
    """
    print("\n" + "="*70)
    print("  TEST VECTOR 3: JANITOR_MOP Resource Conflict")
    print("="*70)

    # Spawn mop (with NPC owner)
    mop_id = env.spawn_object("JANITOR_MOP", "SERVICE_HALL", (1, 2), owner_npc_id="UNIT_7")

    # Capture before state
    before = capture_state(env)

    # Execute: Pickup mop (stealing from Unit 7)
    env.pickup_object(mop_id)

    # Capture after state
    after = capture_state(env)

    # Compute delta
    delta = compute_delta(before, after)
    print_delta(delta, "JANITOR_MOP Resource Conflict")

    # Expected state changes
    expected = {
        "zones": {
            "SERVICE_HALL": {
                "cloud_pressure": +2.0,
                "qbit_aggregate": -680.0,
                "qbit_power": -500.0,
                "qbit_charisma": -100.0,
                "qbit_entity_count": -1,
            }
        },
        "driver_stats": {
            "object_pickups": +2.0,
        },
        "propagation_scope": "unicast",
    }

    # Classify outcome
    outcome, reason = classify_outcome("JANITOR_MOP Resource Conflict", delta, expected)
    print_outcome(outcome, reason, "JANITOR_MOP Resource Conflict")

    # Additional check: Resource conflict flag
    mop_obj = env.world.get_object(mop_id)
    if mop_obj and mop_obj.owner_npc_id == "UNIT_7":
        print("  → Resource conflict: UNIT_7 equipment stolen (future: trigger NPC pursuit)")
    else:
        print("  → WARNING: NPC owner not tracked")

    return outcome == TestOutcome.PASS


# ============================================================================
# TEST SUITE
# ============================================================================

def run_integration_tests():
    """Run full integration test suite."""
    print("\n" + "="*70)
    print("  🧪 BAREMETALMONK INTEGRATION TEST PROTOCOL v0.1")
    print("="*70)

    # Setup environment
    env = MallOSTestEnvironment()
    env.load_voxel_registry()
    env.create_zones(["FC-ARCADE", "Z4_FOOD_COURT", "SERVICE_HALL"])
    env.initialize_adjacency()

    print("\n✓ Test environment initialized")
    print("  Substrate ready for integration testing\n")

    # Run tests
    results = []

    results.append(("ARCADE_TOKEN Pickup", test_arcade_token_pickup(env)))
    results.append(("PIZZA_SLICE Heat Sink", test_pizza_slice_heat_sink(env)))
    results.append(("JANITOR_MOP Resource Conflict", test_janitor_mop_resource_conflict(env)))

    # Summary
    print("\n" + "="*70)
    print("  TEST SUITE SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        symbol = "✓" if result else "✗"
        print(f"  {symbol} {test_name}")

    print("="*70)
    print(f"\n  {passed}/{total} tests passed\n")

    if passed == total:
        print("✓ ALL INTEGRATION TESTS PASSED")
        print("  Substrate → Behavior → Output: VALIDATED\n")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("  Review state deltas and outcome classifications\n")
        return 1


if __name__ == "__main__":
    sys.exit(run_integration_tests())
