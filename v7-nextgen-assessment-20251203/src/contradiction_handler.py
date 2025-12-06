#!/usr/bin/env python3
"""
NPC Contradiction Event Handler - V6 NextGen

Handles NPC contradiction events (spine rule violations) with full
cascade effects: Cloud pressure spikes, zone instability, adjacency chaos,
and cross-entity reactions.

Contradiction events occur when:
- Cloud pressure exceeds NPC's QBIT-weighted threshold
- NPC violates a "never" rule from their behavioral spine
- Reality breaks in a localized, observable way

Effects cascade through:
1. Cloud pressure spike (+5-10 based on NPC power)
2. Zone turbulence ripple (affects all zones)
3. Adjacency matrix noise (pathfinding chaos)
4. Cross-entity reactions (Wife responds to Janitor, etc.)
5. Bleed event probability increase
"""

import time
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from npc_state_machine import NPCStateMachine
    from cloud import Cloud


def handle_npc_contradiction(
    npc: 'NPCStateMachine',
    broken_rule: str,
    cloud: 'Cloud',
    zones: Optional[Dict] = None
) -> Dict:
    """
    Handle NPC contradiction event with full cascade effects.

    Args:
        npc: NPC state machine that triggered contradiction
        broken_rule: The "never" rule that was violated
        cloud: Cloud instance (for pressure spike + logging)
        zones: Optional dict of zones for turbulence ripple

    Returns:
        Contradiction event dict with full details
    """
    # Calculate QBIT-weighted spike magnitude
    power_norm = npc.spine.qbit_power / 3000  # Normalize to 0-1
    charisma_norm = npc.spine.qbit_charisma / 3000
    overall_norm = npc.spine.qbit_overall / 6000

    # Cloud pressure spike (5-10 based on power)
    base_spike = 5.0
    power_multiplier = 1.0 + power_norm  # 1.0-2.0x
    spike_magnitude = base_spike * power_multiplier

    cloud_before = cloud.cloud_level
    cloud.cloud_level = max(0, min(100, cloud.cloud_level + spike_magnitude))
    cloud_after = cloud.cloud_level

    # Capture bleed tier before modifications
    bleed_tier_before = cloud.current_bleed_tier

    # Create event record
    event = {
        "timestamp": time.time(),
        "npc_id": npc.npc_id,
        "npc_name": npc.spine.name,
        "rule_broken": broken_rule,
        "zone": npc.current_zone,
        "cloud_before": cloud_before,
        "cloud_after": cloud_after,
        "cloud_spike": spike_magnitude,
        "npc_qbit_power": npc.spine.qbit_power,
        "npc_qbit_overall": npc.spine.qbit_overall,
        "bleed_tier_before": bleed_tier_before
    }

    # Log to Cloud contradiction history
    cloud.npc_contradiction_log.append(event)

    # Mark NPC as having contradicted
    npc.contradiction_active = True
    npc.last_contradiction_time = time.time()

    # Zone turbulence ripple (affects all zones)
    if zones:
        turbulence_ripple = overall_norm * 2.0  # 0-2.0 turbulence spike

        for zone_id, zone in zones.items():
            # Distance decay: zones farther from contradiction epicenter get less ripple
            if zone_id == npc.current_zone:
                # Epicenter: full ripple
                zone.turbulence = min(10, zone.turbulence + turbulence_ripple)
            else:
                # Adjacent zones: reduced ripple
                decay_factor = 0.5
                zone.turbulence = min(10, zone.turbulence + (turbulence_ripple * decay_factor))

    # Adjacency matrix noise injection
    # High-charisma contradictions create pathfinding chaos
    adjacency_noise = charisma_norm * 0.3  # 0-0.3 noise factor
    if hasattr(cloud, '_adjacency_noise_accumulator'):
        cloud._adjacency_noise_accumulator += adjacency_noise
    else:
        cloud._adjacency_noise_accumulator = adjacency_noise

    # Force immediate adjacency recalculation
    cloud._update_adjacency_matrix()

    # Check for Bleed tier escalation
    bleed_tier_after = cloud.current_bleed_tier
    if cloud.cloud_level >= cloud.BLEED_TIER_1 and not cloud.bleed_threshold_reached:
        cloud.bleed_threshold_reached = True
        cloud.bleed_events_triggered += 1
        cloud.last_bleed_time = time.time()

    # Update bleed tier based on new Cloud level
    if cloud.cloud_level >= cloud.BLEED_TIER_3:
        cloud.current_bleed_tier = 3
    elif cloud.cloud_level >= cloud.BLEED_TIER_2:
        cloud.current_bleed_tier = 2
    elif cloud.cloud_level >= cloud.BLEED_TIER_1:
        cloud.current_bleed_tier = 1

    event["bleed_tier_after"] = cloud.current_bleed_tier
    event["bleed_escalation"] = cloud.current_bleed_tier > bleed_tier_before

    # Print contradiction alert
    print("\n" + "=" * 70)
    print("🚨 CONTRADICTION EVENT")
    print("=" * 70)
    print(f"NPC:           {npc.spine.name} ({npc.npc_id})")
    print(f"Rule Broken:   {broken_rule}")
    print(f"Zone:          {npc.current_zone}")
    print(f"Cloud:         {cloud_before:.1f} → {cloud_after:.1f} (+{spike_magnitude:.1f})")
    print(f"QBIT Power:    {npc.spine.qbit_power}")
    print(f"Bleed Tier:    {bleed_tier_before} → {cloud.current_bleed_tier}")
    if event["bleed_escalation"]:
        print(f"⚠️  BLEED TIER ESCALATION: Tier {cloud.current_bleed_tier} ACTIVE")
    print("=" * 70 + "\n")

    return event


def handle_cross_entity_reaction(
    trigger_npc_id: str,
    affected_npc: 'NPCStateMachine',
    cloud: 'Cloud',
    reaction_type: str = "witness"
) -> Optional[Dict]:
    """
    Handle cross-entity reactions to contradiction events.

    When one NPC contradicts, nearby NPCs may react:
    - Witness: NPC observes contradiction (meta-awareness)
    - Sympathy: NPC becomes more likely to contradict (contagion)
    - Counter: NPC attempts to stabilize (rare)

    Args:
        trigger_npc_id: NPC that triggered the contradiction
        affected_npc: NPC reacting to the contradiction
        cloud: Cloud instance
        reaction_type: Type of reaction

    Returns:
        Reaction event dict if reaction occurred, None otherwise
    """
    # Check proximity (same zone or adjacent zone)
    # For now, simplified: any Primary NPC can react

    if affected_npc.spine.role != "Primary":
        return None  # Only Primary entities react

    # Calculate reaction probability based on affected NPC's QBIT scores
    charisma_norm = affected_npc.spine.qbit_charisma / 3000
    power_norm = affected_npc.spine.qbit_power / 3000

    # High-charisma NPCs are more likely to witness/react
    reaction_chance = charisma_norm * 0.5  # 0-0.5 probability

    import random
    if random.random() > reaction_chance:
        return None  # No reaction

    # Create reaction event
    reaction = {
        "timestamp": time.time(),
        "trigger_npc": trigger_npc_id,
        "affected_npc": affected_npc.npc_id,
        "reaction_type": reaction_type,
        "cloud_level": cloud.cloud_level
    }

    # Apply reaction effects
    if reaction_type == "witness":
        # Meta-aware NPCs log the impossibility
        # Check if spine has tags attribute and if it contains "meta"
        spine_tags = getattr(affected_npc.spine, 'tags', [])
        if "meta" in spine_tags:
            print(f"  → {affected_npc.spine.name} witnesses the contradiction")
            # Increase own contradiction likelihood
            affected_npc.spine.qbit_power += 50  # Temporary power boost

    elif reaction_type == "sympathy":
        # Contradiction contagion: lower own threshold
        print(f"  → {affected_npc.spine.name} feels the pull to contradict")
        # This is handled by Cloud pressure being higher

    elif reaction_type == "counter":
        # Rare stabilization attempt (not implemented yet)
        pass

    return reaction


def check_wife_reaction_to_janitor(
    wife_npc: 'NPCStateMachine',
    janitor_zone: str,
    cloud: 'Cloud'
) -> Optional[str]:
    """
    Special handler for Wife's reaction to Janitor crossing FC-ARCADE.

    The Wife is the "contradiction magnet" - Janitor's spatial anchor.
    When he violates the "never_crosses_fc_arcade" rule, she reacts.

    Possible reactions:
    - "glance": Looks toward FC-ARCADE (Cloud 70-79)
    - "stand": Stands up from browsing (Cloud 80-89)
    - "follow": Begins moving toward FC-ARCADE (Cloud 90+)
    - "speak": Ultimate contradiction - she speaks (Cloud 95+)

    Args:
        wife_npc: Wife NPC state machine
        janitor_zone: Current zone of Janitor
        cloud: Cloud instance

    Returns:
        Reaction type string if reaction occurred
    """
    if janitor_zone != "FC-ARCADE":
        return None  # Janitor hasn't crossed yet

    # Check Cloud level for reaction intensity
    cloud_level = cloud.cloud_level

    if cloud_level >= 95:
        reaction = "speak"
        print(f"  🗣️  {wife_npc.spine.name} SPEAKS (ultimate contradiction)")
    elif cloud_level >= 90:
        reaction = "follow"
        print(f"  👣 {wife_npc.spine.name} begins moving toward FC-ARCADE")
    elif cloud_level >= 80:
        reaction = "stand"
        print(f"  🧍 {wife_npc.spine.name} stands up")
    elif cloud_level >= 70:
        reaction = "glance"
        print(f"  👀 {wife_npc.spine.name} glances toward FC-ARCADE")
    else:
        return None

    return reaction


# ========== MODULE TESTING ==========

if __name__ == "__main__":
    print("=" * 70)
    print("CONTRADICTION HANDLER TEST")
    print("=" * 70)

    # Import required modules
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))

    from cloud import Cloud
    from npc_state_machine import NPCSpine, NPCStateMachine

    # Create test cloud
    cloud = Cloud()
    cloud.cloud_level = 78.3  # Critical threshold

    # Create Janitor NPC
    janitor_spine = NPCSpine(
        npc_id="the-janitor",
        name="The Janitor",
        role="Primary",
        never_rules=["never_crosses_fc_arcade", "never_speaks_about_wife"],
        qbit_power=1478,
        qbit_charisma=1308,
        qbit_overall=2786
    )

    janitor = NPCStateMachine(
        npc_id="the-janitor",
        spine=janitor_spine,
        current_zone="CORRIDOR"
    )

    print("\nInitial State:")
    print(f"  Cloud Level: {cloud.cloud_level}")
    print(f"  Janitor Zone: {janitor.current_zone}")
    print(f"  Janitor Can Contradict: {janitor_spine.get_contradiction_threshold() < cloud.cloud_level}")

    # Simulate Janitor entering FC-ARCADE (contradiction)
    print("\n⚠️  Janitor enters FC-ARCADE...")
    janitor.current_zone = "FC-ARCADE"

    # Trigger contradiction event
    event = handle_npc_contradiction(
        npc=janitor,
        broken_rule="never_crosses_fc_arcade",
        cloud=cloud,
        zones=cloud.zones
    )

    print("\nContradiction Event Details:")
    print(f"  Timestamp: {event['timestamp']:.2f}")
    print(f"  Cloud Spike: +{event['cloud_spike']:.1f}")
    print(f"  Cloud After: {event['cloud_after']:.1f}")
    print(f"  Bleed Escalation: {event['bleed_escalation']}")

    print("\nZone Turbulence After Contradiction:")
    for zone_id in ["FC-ARCADE", "CORRIDOR", "SERVICE_HALL"]:
        zone = cloud.zones.get(zone_id)
        if zone:
            print(f"  {zone_id}: {zone.turbulence:.2f}/10")

    print("\n✓ Contradiction handler test complete")
