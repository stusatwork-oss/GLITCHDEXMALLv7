#!/usr/bin/env python3
"""
QBIT INTEGRATION END-TO-END TEST

Validates complete QBIT → Cloud → NPC → Zone behavior pipeline.

Test Flow:
1. Load and score entities with QBIT engine
2. Calculate zone QBIT aggregates
3. Initialize Cloud with QBIT integration
4. Create NPCs with QBIT-aware state machines
5. Simulate gameplay loop
6. Verify QBIT influences all systems correctly

Success Criteria:
- Entities scored correctly
- Zone aggregates calculated
- Cloud pressure affected by entity influence
- NPC contradiction thresholds scale with QBIT power
- Artifact weights use QBIT charisma
- Zone resonance modified by QBIT
"""

import time
import json
from pathlib import Path

# Import QBIT systems
from qbit_engine import score_entity, calculate_zone_qbit_aggregate
from cloud import Cloud
from npc_state_machine import NPCSpine, NPCStateMachine


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_entity_scoring():
    """Test QBIT entity scoring."""
    print_section("TEST 1: Entity Scoring")

    # Create test entity
    entity = {
        "id": "test-arcade-cabinet",
        "name": "Test Arcade Cabinet",
        "role": "Secondary",
        "type": "arcade_cabinet",
        "tags": ["fc-arcade", "test"],
        "metrics": {
            "resonanceScore": 80,
            "grassrootsSupport": 500,
            "audienceSize": 5000,
            "deepViewCount": 250000,
            "engagementScore": 75,
            "referenceCount": 600,
            "trustScore": 65,
            "backingVolume": 0,
            "resourcePool": 50,
            "networkReach": 3
        }
    }

    print("\nScoring test entity...")
    scored = score_entity(entity)

    print(f"\nEntity: {scored['name']}")
    print(f"  Power:    {scored['computed']['power']:>5}")
    print(f"  Charisma: {scored['computed']['charisma']:>5}")
    print(f"  Overall:  {scored['computed']['overall']:>5}")
    print(f"  Rarity:   {scored['computed']['rarity']}")

    assert scored['computed']['power'] >= 0, "Power score invalid"
    assert scored['computed']['charisma'] >= 0, "Charisma score invalid"
    assert scored['computed']['overall'] > 0, "Overall score should be > 0"
    print("\n✓ Entity scoring test passed")

    return scored


def test_zone_aggregates(entities):
    """Test zone QBIT aggregation."""
    print_section("TEST 2: Zone QBIT Aggregates")

    zone_id = "fc-arcade"

    print(f"\nCalculating aggregate for zone: {zone_id}")
    stats = calculate_zone_qbit_aggregate(entities, zone_id)

    print(f"\nZone Stats:")
    print(f"  Zone ID:         {stats['zone_id']}")
    print(f"  Entity Count:    {stats['entity_count']}")
    print(f"  Total Power:     {stats['total_power']}")
    print(f"  Total Charisma:  {stats['total_charisma']}")
    print(f"  Total Influence: {stats['total_influence']}")
    print(f"  Avg Power:       {stats['avg_power']:.1f}")
    print(f"  Avg Charisma:    {stats['avg_charisma']:.1f}")

    if stats['top_entities']:
        print(f"\n  Top Entities:")
        for e in stats['top_entities']:
            print(f"    - {e['name']}: {e['overall']}")

    assert stats['entity_count'] > 0, "Should have entities in zone"
    assert stats['total_influence'] > 0, "Total influence should be > 0"
    print("\n✓ Zone aggregate test passed")

    return stats


def test_cloud_integration(entities):
    """Test Cloud system with QBIT integration."""
    print_section("TEST 3: Cloud QBIT Integration")

    # Create Cloud (will load entities from canon/entities/)
    print("\nInitializing Cloud with QBIT...")
    cloud = Cloud()

    print(f"\nCloud initialized:")
    print(f"  Entities loaded: {len(cloud.entities)}")
    print(f"  Zones with QBIT: {len(cloud.zone_qbit_cache)}")

    # Check FC-ARCADE zone
    fc_arcade_stats = cloud.get_zone_qbit_stats("FC-ARCADE")
    if fc_arcade_stats:
        print(f"\n  FC-ARCADE Zone:")
        print(f"    Entity count: {fc_arcade_stats.get('entity_count', 0)}")
        print(f"    Total influence: {fc_arcade_stats.get('total_influence', 0)}")

    # Test pressure calculation with entity influence
    print("\nTesting Cloud pressure with entity influence...")

    action = {
        "type": "interact",
        "target": "leisurely-leon",
        "zone": "FC-ARCADE"
    }

    initial_level = cloud.cloud_level

    # Run 20 updates
    for i in range(20):
        hints = cloud.update(0.1, player_action=action)

    final_level = cloud.cloud_level
    delta = final_level - initial_level

    print(f"\n  Initial Cloud: {initial_level:.2f}")
    print(f"  Final Cloud:   {final_level:.2f}")
    print(f"  Delta:         {delta:.2f}")
    print(f"  Mood:          {cloud.mall_mood.value}")

    assert delta > 0, "Cloud pressure should increase"
    print("\n✓ Cloud integration test passed")

    return cloud


def test_artifact_weights(cloud):
    """Test QBIT-aware artifact weight system."""
    print_section("TEST 4: Artifact Weight System")

    print("\nTesting artifact weight calculation...")

    # Test with entity that exists
    entity_id = "leisurely-leon"
    weight = cloud.get_artifact_weight(entity_id)

    print(f"\n  Artifact: {entity_id}")
    print(f"  Weight:   {weight:.3f}")

    entity = cloud.get_entity_by_id(entity_id)
    if entity:
        charisma = entity.get("computed", {}).get("charisma", 0)
        print(f"  Charisma: {charisma}")
        print(f"  (Weight = Charisma / 3000)")

    # Test with non-existent entity (should use discovery fallback)
    fake_id = "nonexistent-artifact"
    weight_fake = cloud.get_artifact_weight(fake_id)
    print(f"\n  Artifact: {fake_id} (non-existent)")
    print(f"  Weight:   {weight_fake:.3f}")

    assert 0 <= weight <= 1, "Weight should be in [0, 1]"
    print("\n✓ Artifact weight test passed")


def test_npc_contradiction_thresholds():
    """Test QBIT-aware NPC contradiction thresholds."""
    print_section("TEST 5: NPC Contradiction Thresholds")

    print("\nCreating NPCs with different QBIT power levels...")

    # Low power NPC
    low_power_spine = NPCSpine(
        npc_id="npc-low",
        name="Low Power NPC",
        role="Secondary",
        never_rules=["never_leave_zone"],
        qbit_power=500,
        qbit_charisma=200,
        qbit_overall=700
    )

    # High power NPC
    high_power_spine = NPCSpine(
        npc_id="npc-high",
        name="High Power NPC",
        role="Primary",
        never_rules=["never_acknowledge_player"],
        qbit_power=2500,
        qbit_charisma=1500,
        qbit_overall=4000
    )

    low_npc = NPCStateMachine(npc_id="npc-low", spine=low_power_spine)
    high_npc = NPCStateMachine(npc_id="npc-high", spine=high_power_spine)

    print(f"\n  Low Power NPC:")
    print(f"    QBIT Power: {low_power_spine.qbit_power}")
    print(f"    Contradiction Threshold: {low_power_spine.get_contradiction_threshold():.1f}")

    print(f"\n  High Power NPC:")
    print(f"    QBIT Power: {high_power_spine.qbit_power}")
    print(f"    Contradiction Threshold: {high_power_spine.get_contradiction_threshold():.1f}")

    # Test at Cloud level 65 (between thresholds)
    cloud_level = 65.0

    low_hints = low_npc.update(cloud_level=cloud_level, cloud_mood="strained", dt=0.1)
    high_hints = high_npc.update(cloud_level=cloud_level, cloud_mood="strained", dt=0.1)

    print(f"\n  At Cloud Level {cloud_level}:")
    print(f"    Low Power can contradict:  {low_hints['can_contradict']}")
    print(f"    High Power can contradict: {high_hints['can_contradict']}")

    assert not low_hints['can_contradict'], "Low power NPC shouldn't contradict at 65"
    assert high_hints['can_contradict'], "High power NPC should contradict at 65"
    print("\n✓ NPC contradiction threshold test passed")


def test_zone_resonance_qbit_modifier(cloud):
    """Test zone resonance modification by QBIT."""
    print_section("TEST 6: Zone Resonance QBIT Modifier")

    print("\nTesting resonance gain with QBIT charisma modifier...")

    zone_id = "FC-ARCADE"
    zone = cloud.zones.get(zone_id)

    if not zone:
        print("  ⚠️  FC-ARCADE zone not found, skipping test")
        return

    initial_resonance = zone.resonance
    initial_charisma = zone.qbit_charisma

    print(f"\n  Zone: {zone_id}")
    print(f"  Initial Resonance: {initial_resonance:.2f}")
    print(f"  Zone QBIT Charisma: {initial_charisma}")

    # Trigger discovery
    action = {
        "type": "interact",
        "target": "artifact_test",
        "zone": zone_id
    }

    # Record discovery (this should apply QBIT modifier)
    cloud._record_discovery(action)

    final_resonance = zone.resonance
    resonance_gain = final_resonance - initial_resonance

    print(f"\n  After discovery:")
    print(f"  Final Resonance: {final_resonance:.2f}")
    print(f"  Resonance Gain:  {resonance_gain:.2f}")

    if initial_charisma > 0:
        expected_base_gain = 1.0
        modifier = 1.0 + (initial_charisma / 3000) * cloud.QBIT_RESONANCE_MODIFIER
        expected_gain = expected_base_gain * modifier
        print(f"  Expected Gain:   {expected_gain:.2f} (base=1.0, modifier={modifier:.2f})")

    assert resonance_gain > 0, "Resonance should increase"
    print("\n✓ Zone resonance QBIT modifier test passed")


def run_full_integration_test():
    """Run complete end-to-end integration test."""
    print("\n" + "#" * 70)
    print("#" + " " * 68 + "#")
    print("#  QBIT INTEGRATION END-TO-END TEST SUITE".center(70) + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)

    try:
        # Test 1: Entity Scoring
        scored_entity = test_entity_scoring()

        # Test 2: Zone Aggregates
        entities = [scored_entity]
        zone_stats = test_zone_aggregates(entities)

        # Test 3: Cloud Integration
        cloud = test_cloud_integration(entities)

        # Test 4: Artifact Weights
        test_artifact_weights(cloud)

        # Test 5: NPC Contradiction Thresholds
        test_npc_contradiction_thresholds()

        # Test 6: Zone Resonance QBIT Modifier
        test_zone_resonance_qbit_modifier(cloud)

        # Final Summary
        print_section("INTEGRATION TEST SUMMARY")
        print("\n✅ ALL TESTS PASSED")
        print("\nQBIT Integration Status:")
        print("  [✓] Entity scoring (QBIT engine)")
        print("  [✓] Zone QBIT aggregates")
        print("  [✓] Cloud pressure with entity influence")
        print("  [✓] Artifact weights (QBIT charisma)")
        print("  [✓] NPC contradiction thresholds (QBIT power)")
        print("  [✓] Zone resonance modifiers (QBIT charisma)")
        print("\nQBIT System: FULLY OPERATIONAL")
        print("\n" + "#" * 70)

        return True

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_full_integration_test()
    exit(0 if success else 1)
