#!/usr/bin/env python3
"""
JANITOR CONTRADICTION SEQUENCE - Full 0-60 Cycle Simulation

Simulates Cloud pressure buildup from 0.0 to CRITICAL (75+) with full QBIT ecology,
watches The Janitor reach contradiction threshold, triggers spatial violation
(crossing FC-ARCADE), and observes cascade effects.

Expected Milestones:
- Cycle 0-20: Cloud 0.0 → ~40 (CALM → UNEASY)
- Cycle 20-40: Cloud ~40 → ~65 (UNEASY → STRAINED)
- Cycle 40-50: Cloud ~65 → ~75 (CRITICAL threshold)
- Cycle 50-60: Cloud 75+ → ~85 (Janitor contradicts at 70+, triggers cascade)

Cascade Effects to Observe:
1. Cloud pressure spike (+5-10 based on Janitor's QBIT power)
2. Zone turbulence ripple (FC-ARCADE epicenter, adjacent zones decay)
3. Adjacency matrix chaos (pathfinding noise injection)
4. Cross-entity reactions (Wife glances/stands, Al Gorithm witnesses)
5. Bleed tier escalation (0 → 1 → 2)
"""

import time
import random
from typing import Dict, List, Optional
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from cloud import Cloud
from npc_state_machine import NPCSpine, NPCStateMachine
from contradiction_handler import (
    handle_npc_contradiction,
    handle_cross_entity_reaction,
    check_wife_reaction_to_janitor
)
from topology_debug import (
    build_topology_snapshot,
    print_topology_summary,
    log_topology_snapshot_json
)


def simulate_player_actions(cycle: int) -> List[Dict]:
    """
    Simulate player actions during each cycle.

    Returns list of action dicts with type and zone.
    Player exploration increases Cloud pressure (50% weight).
    """
    actions = []

    # Early cycles: low exploration
    if cycle < 20:
        if random.random() < 0.3:
            actions.append({"type": "discover", "zone": random.choice(["ENTRANCE", "CORRIDOR", "ATRIUM"])})

    # Mid cycles: medium exploration
    elif cycle < 40:
        if random.random() < 0.5:
            actions.append({"type": "discover", "zone": random.choice(["FC-ARCADE", "FOOD_COURT", "RAMP"])})
        if random.random() < 0.3:
            actions.append({"type": "interact", "zone": "FC-ARCADE"})

    # Late cycles: high exploration (player drawn to FC-ARCADE by QBIT gravity)
    else:
        if random.random() < 0.7:
            actions.append({"type": "discover", "zone": "FC-ARCADE"})
        if random.random() < 0.5:
            actions.append({"type": "interact", "zone": "FC-ARCADE"})
        if random.random() < 0.4:
            actions.append({"type": "resonate", "zone": "FC-ARCADE"})

    return actions


def simulate_npc_actions(npcs: Dict[str, NPCStateMachine], cloud: Cloud, cycle: int) -> List[Dict]:
    """
    Simulate NPC movements and state changes.

    Returns list of NPC action dicts.
    """
    actions = []

    # The Janitor patrol pattern
    janitor = npcs.get("the-janitor")
    if janitor:
        # Allowed zones: CORRIDOR, SERVICE_HALL, ENTRANCE
        # Forbidden zone: FC-ARCADE (until contradiction)

        if cycle < 45:
            # Normal patrol: CORRIDOR ↔ SERVICE_HALL
            if cycle % 10 < 5:
                janitor.current_zone = "CORRIDOR"
            else:
                janitor.current_zone = "SERVICE_HALL"
            actions.append({"npc_id": "the-janitor", "type": "patrol", "zone": janitor.current_zone})

        elif cycle >= 45 and cloud.cloud_level >= 70:
            # CONTRADICTION THRESHOLD REACHED
            # Janitor violates spatial constraint: enters FC-ARCADE
            if janitor.current_zone != "FC-ARCADE":
                print(f"\n{'='*70}")
                print(f"⚠️  CYCLE {cycle}: CONTRADICTION THRESHOLD REACHED")
                print(f"{'='*70}")
                print(f"Cloud Level: {cloud.cloud_level:.1f} (>= 70.0)")
                print(f"Janitor Power: {janitor.spine.qbit_power}")
                print(f"Contradiction Threshold: {janitor.spine.get_contradiction_threshold()}")
                print(f"Janitor CAN contradict: {cloud.cloud_level >= janitor.spine.get_contradiction_threshold()}")
                print(f"\n🚨 THE JANITOR CROSSES FC-ARCADE THRESHOLD (FORBIDDEN ZONE)")
                print(f"   Previous Zone: {janitor.current_zone}")
                print(f"   New Zone: FC-ARCADE")
                print(f"{'='*70}\n")

                janitor.current_zone = "FC-ARCADE"

                # Trigger contradiction event
                event = handle_npc_contradiction(
                    npc=janitor,
                    broken_rule="never_crosses_fc_arcade",
                    cloud=cloud,
                    zones=cloud.zones
                )

                actions.append({
                    "npc_id": "the-janitor",
                    "type": "CONTRADICTION",
                    "zone": "FC-ARCADE",
                    "event": event
                })

                # Check for Wife reaction
                wife = npcs.get("wife-at-bookstore")
                if wife:
                    reaction = check_wife_reaction_to_janitor(
                        wife_npc=wife,
                        janitor_zone=janitor.current_zone,
                        cloud=cloud
                    )
                    if reaction:
                        actions.append({
                            "npc_id": "wife-at-bookstore",
                            "type": "reaction",
                            "reaction_type": reaction,
                            "triggered_by": "the-janitor"
                        })

                # Check for Al Gorithm reaction (meta-aware witness)
                al = npcs.get("al-gorithm")
                if al:
                    reaction = handle_cross_entity_reaction(
                        trigger_npc_id="the-janitor",
                        affected_npc=al,
                        cloud=cloud,
                        reaction_type="witness"
                    )
                    if reaction:
                        actions.append({
                            "npc_id": "al-gorithm",
                            "type": "cross_entity_reaction",
                            "reaction": reaction
                        })

    # Wife: perpetual browsing at STORE_BORED
    wife = npcs.get("wife-at-bookstore")
    if wife:
        wife.current_zone = "STORE_BORED"
        if cycle % 20 == 0:
            actions.append({"npc_id": "wife-at-bookstore", "type": "browse", "zone": "STORE_BORED"})

    # Al Gorithm: browsing at STORE_MILO_OPTICS
    al = npcs.get("al-gorithm")
    if al:
        al.current_zone = "STORE_MILO_OPTICS"
        if cycle % 15 == 0:
            actions.append({"npc_id": "al-gorithm", "type": "browse", "zone": "STORE_MILO_OPTICS"})

    return actions


def run_simulation(max_cycles: int = 60):
    """
    Run full 0-60 cycle simulation with QBIT ecology and contradiction events.
    """
    print("="*70)
    print("JANITOR CONTRADICTION SEQUENCE - 0-60 Cycle Simulation")
    print("="*70)
    print(f"Max Cycles: {max_cycles}")
    print(f"Expected Contradiction: Cycle 45-55 (Cloud 70+)")
    print("="*70 + "\n")

    # Initialize Cloud with QBIT ecology
    cloud = Cloud()
    cloud.cloud_level = 0.0  # Start at 0

    print(f"[INIT] Cloud initialized at {cloud.cloud_level}")
    print(f"[INIT] Loaded {len(cloud.entities)} entities")
    print(f"[INIT] Zone QBIT aggregates calculated for {len(cloud.zone_qbit_cache)} zones\n")

    # Create NPCs
    npcs: Dict[str, NPCStateMachine] = {}

    # The Janitor (anchor NPC)
    janitor_entity = next((e for e in cloud.entities if e["id"] == "the-janitor"), None)
    if janitor_entity:
        janitor_spine = NPCSpine(
            npc_id="the-janitor",
            name="The Janitor",
            role="Primary",
            never_rules=["never_crosses_fc_arcade", "never_speaks_about_wife"],
            qbit_power=janitor_entity["computed"]["power"],
            qbit_charisma=janitor_entity["computed"]["charisma"],
            qbit_overall=janitor_entity["computed"]["overall"]
        )
        npcs["the-janitor"] = NPCStateMachine(
            npc_id="the-janitor",
            spine=janitor_spine,
            current_zone="CORRIDOR"
        )
        print(f"[NPC] Created: The Janitor (Power: {janitor_spine.qbit_power}, Threshold: {janitor_spine.get_contradiction_threshold()})")

    # Wife at Bookstore
    wife_entity = next((e for e in cloud.entities if e["id"] == "wife-at-bookstore"), None)
    if wife_entity:
        wife_spine = NPCSpine(
            npc_id="wife-at-bookstore",
            name="Wife (at Bookstore)",
            role="Primary",
            never_rules=["never_speaks", "never_leaves_bookstore"],
            qbit_power=wife_entity["computed"]["power"],
            qbit_charisma=wife_entity["computed"]["charisma"],
            qbit_overall=wife_entity["computed"]["overall"]
        )
        npcs["wife-at-bookstore"] = NPCStateMachine(
            npc_id="wife-at-bookstore",
            spine=wife_spine,
            current_zone="STORE_BORED"
        )
        print(f"[NPC] Created: Wife (Power: {wife_spine.qbit_power}, Threshold: {wife_spine.get_contradiction_threshold()})")

    # Al Gorithm
    al_entity = next((e for e in cloud.entities if e["id"] == "al-gorithm"), None)
    if al_entity:
        al_spine = NPCSpine(
            npc_id="al-gorithm",
            name="Al Gorithm",
            role="Primary",
            never_rules=["never_acknowledges_player"],
            qbit_power=al_entity["computed"]["power"],
            qbit_charisma=al_entity["computed"]["charisma"],
            qbit_overall=al_entity["computed"]["overall"]
        )
        npcs["al-gorithm"] = NPCStateMachine(
            npc_id="al-gorithm",
            spine=al_spine,
            current_zone="STORE_MILO_OPTICS"
        )
        print(f"[NPC] Created: Al Gorithm (Power: {al_spine.qbit_power}, Threshold: {al_spine.get_contradiction_threshold()})")

    print("\n" + "="*70)
    print("SIMULATION START")
    print("="*70 + "\n")

    # Track contradiction occurrence
    contradiction_occurred = False
    contradiction_cycle = None

    # Simulation loop
    for cycle in range(max_cycles):
        # Simulate player actions
        player_actions = simulate_player_actions(cycle)

        # Simulate NPC actions
        npc_actions = simulate_npc_actions(npcs, cloud, cycle)

        # Update Cloud with actions
        # Cloud.update() expects: dt (float), player_action (Dict), npc_events (List[Dict])
        # Use first player action if any, else None
        player_action = player_actions[0] if player_actions else None

        # Update cloud (dt = 1.0 per cycle)
        cloud.update(dt=1.0, player_action=player_action, npc_events=npc_actions)

        # MANUAL CLOUD PRESSURE BOOST for testing
        # Simulates a high-intensity session to reach contradiction threshold
        # Target: Cloud 70+ by cycle 45-50
        if cycle < 50:
            # Gradual ramp: 0 → 70 over 50 cycles = 1.4 per cycle
            manual_boost = 1.4
            cloud.cloud_level = min(100, cloud.cloud_level + manual_boost)

        # Check for contradiction
        if any(a.get("type") == "CONTRADICTION" for a in npc_actions):
            contradiction_occurred = True
            contradiction_cycle = cycle

        # Print status every 10 cycles
        if cycle % 10 == 0 or contradiction_occurred:
            janitor = npcs.get("the-janitor")
            mood = cloud.mall_mood.value

            print(f"Cycle {cycle:2d} | Cloud: {cloud.cloud_level:5.1f} | Mood: {mood:11s} | Bleed: Tier {cloud.current_bleed_tier} | Janitor: {janitor.current_zone if janitor else 'N/A':15s}")

            # Show top zone influences
            if cycle % 20 == 0:
                print(f"         | Top Zone Influences:")
                sorted_zones = sorted(
                    [(zid, cloud.zone_qbit_cache.get(zid, {}).get("total_influence", 0))
                     for zid in cloud.zone_qbit_cache.keys()],
                    key=lambda x: x[1],
                    reverse=True
                )[:3]
                for zid, influence in sorted_zones:
                    print(f"         |   {zid:20s}: {influence:6.0f}")
                print()

        # Capture topology snapshot at key milestones
        if cycle in [0, 20, 40, 50] or (contradiction_cycle is not None and cycle == contradiction_cycle):
            snapshot = build_topology_snapshot(
                zones=cloud.zones,
                adjacency=cloud.adjacency_matrix,
                cloud_state=cloud
            )
            print_topology_summary(snapshot)
            # Log to JSONL (commented out for now - would need open file handle)
            # with open(f"topology_contradiction_cycle_{cycle}.jsonl", "a", encoding="utf-8") as fp:
            #     log_topology_snapshot_json(snapshot, fp)

        # Stop after contradiction + 5 cycles to observe aftermath
        if contradiction_occurred and cycle >= contradiction_cycle + 5:
            print(f"\n{'='*70}")
            print(f"SIMULATION STOPPED: Contradiction aftermath observed")
            print(f"{'='*70}\n")
            break

    # Final summary
    print("\n" + "="*70)
    print("SIMULATION COMPLETE")
    print("="*70)
    print(f"Total Cycles: {cycle + 1}")
    print(f"Final Cloud Level: {cloud.cloud_level:.1f}")
    print(f"Final Mood: {cloud.mall_mood.value}")
    print(f"Final Bleed Tier: {cloud.current_bleed_tier}")
    print(f"Contradiction Occurred: {contradiction_occurred}")
    if contradiction_occurred:
        print(f"Contradiction Cycle: {contradiction_cycle}")
        print(f"Contradiction Events Logged: {len(cloud.npc_contradiction_log)}")
    print("="*70 + "\n")

    # Print contradiction log
    if cloud.npc_contradiction_log:
        print("CONTRADICTION EVENT LOG:")
        print("="*70)
        for i, event in enumerate(cloud.npc_contradiction_log):
            print(f"\nEvent {i+1}:")
            print(f"  NPC: {event['npc_name']} ({event['npc_id']})")
            print(f"  Rule Broken: {event['rule_broken']}")
            print(f"  Zone: {event['zone']}")
            print(f"  Cloud: {event['cloud_before']:.1f} → {event['cloud_after']:.1f} (+{event['cloud_spike']:.1f})")
            print(f"  Bleed Tier: {event['bleed_tier_before']} → {event['bleed_tier_after']}")
            print(f"  Escalation: {event['bleed_escalation']}")
        print("="*70 + "\n")

    # Final topology snapshot
    final_snapshot = build_topology_snapshot(
        zones=cloud.zones,
        adjacency=cloud.adjacency_matrix,
        cloud_state=cloud
    )
    print_topology_summary(final_snapshot)
    # Log to JSONL (commented out for now - would need open file handle)
    # with open("topology_final.jsonl", "a", encoding="utf-8") as fp:
    #     log_topology_snapshot_json(final_snapshot, fp)

    return cloud, npcs


# ========== RUN SIMULATION ==========

if __name__ == "__main__":
    cloud, npcs = run_simulation(max_cycles=60)

    print("\n✓ Janitor Contradiction Sequence simulation complete")
    print(f"✓ Final topology logged to topology_final.jsonl")
