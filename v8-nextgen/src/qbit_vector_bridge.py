#!/usr/bin/env python3
"""
QBIT → VECTOR EMOTIONAL BRIDGE
Step 1 of 5-part integration

Bridges QBIT scoring system (power, charisma) to Vector emotional states (fear, morale, duty).

Architecture:
- QBIT represents systemic influence (structural)
- Vector represents emotional state (experiential)
- Bridge translates world state → emotional response

Usage:
    from qbit_vector_bridge import inject_qbit_to_vector, VectorState

    vector = VectorState()
    qbit_state = {"cloud_pressure": 65.0, "entropy": 0.8, "influence_score": 1500}

    inject_qbit_to_vector(vector, qbit_state)
    # vector.fear = 26.0 (from cloud_pressure * 0.4)
    # vector.morale = -24.0 (from entropy * -0.3)
    # vector.duty = 300.0 (from influence_score * 0.2)

Reference:
- QBIT_ECOLOGY_REPORT.md
- QBIT_ENTITY_INFLUENCE_SPINE.md
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class VectorState:
    """
    Emotional state vector for an entity.

    Attributes:
        fear: Anxiety, threat response, flight instinct (0-100)
        morale: Confidence, optimism, willingness to engage (-100 to 100)
        duty: Sense of obligation, role adherence, purpose (0-100)
        coherence: Internal stability, resistance to breakdown (0-100)
    """
    fear: float = 0.0       # 0-100 (Cloud pressure drives this up)
    morale: float = 50.0    # -100 to 100 (Entropy drives this down)
    duty: float = 50.0      # 0-100 (Influence score drives this up)
    coherence: float = 100.0  # 0-100 (Degrades under contradiction strain)

    def clamp(self):
        """Clamp all values to valid ranges."""
        self.fear = max(0.0, min(100.0, self.fear))
        self.morale = max(-100.0, min(100.0, self.morale))
        self.duty = max(0.0, min(100.0, self.duty))
        self.coherence = max(0.0, min(100.0, self.coherence))

    def get_emotional_profile(self) -> str:
        """Return human-readable emotional state."""
        if self.fear > 70 and self.morale < -30:
            return "terrified_demoralized"
        elif self.fear > 70:
            return "fearful"
        elif self.morale < -50:
            return "demoralized"
        elif self.duty > 80:
            return "dutiful"
        elif self.coherence < 30:
            return "breaking_down"
        elif self.morale > 70 and self.duty > 70:
            return "confident_purposeful"
        else:
            return "neutral"


@dataclass
class QBITState:
    """
    QBIT world state snapshot for emotional injection.

    Attributes:
        cloud_pressure: Mall-wide Cloud level (0-100)
        entropy: Zone chaos/instability (0-1)
        influence_score: Entity's QBIT overall score (0-6000)
        zone_turbulence: Local zone pressure modifier (0-10)
        contradiction_active: Whether NPC is breaking spine rules
    """
    cloud_pressure: float = 0.0      # 0-100
    entropy: float = 0.0             # 0-1 (0=calm, 1=chaotic)
    influence_score: float = 0.0     # 0-6000 QBIT overall
    zone_turbulence: float = 0.0     # 0-10
    contradiction_active: bool = False


def inject_qbit_to_vector(vector: VectorState, qbit: QBITState) -> None:
    """
    Inject QBIT world state into Vector emotional state.

    This is the core emotional runtime bridge. It translates:
    - Cloud pressure → fear (entities feel threatened)
    - Entropy → morale (chaos degrades confidence)
    - Influence score → duty (power creates obligation)
    - Zone turbulence → fear amplifier
    - Contradiction → coherence damage

    Args:
        vector: Entity's emotional state (modified in-place)
        qbit: Current world state snapshot

    Effects:
        Modifies vector.fear, vector.morale, vector.duty, vector.coherence
    """
    # FEAR: Cloud pressure creates anxiety
    # Base: cloud_pressure * 0.4 (0-100 → 0-40)
    # Amplified by zone turbulence
    fear_delta = qbit.cloud_pressure * 0.4
    fear_delta += qbit.zone_turbulence * 2.0  # Zone adds 0-20
    vector.fear += fear_delta

    # MORALE: Entropy degrades confidence
    # Base: entropy * -30 (0-1 → 0 to -30)
    # Critical Cloud (75+) applies additional morale penalty
    morale_delta = qbit.entropy * -30.0
    if qbit.cloud_pressure >= 75:
        morale_delta -= 15.0  # Critical Cloud penalty
    vector.morale += morale_delta

    # DUTY: Influence score creates sense of obligation
    # Base: influence_score * 0.02 (0-6000 → 0-120, capped at 50)
    # High-influence entities feel MORE responsible as Cloud rises
    duty_delta = min(qbit.influence_score * 0.02, 50.0)

    # Influence amplification at high Cloud
    if qbit.influence_score > 3000 and qbit.cloud_pressure > 60:
        duty_delta *= 1.5  # High-power NPCs feel duty MORE under pressure

    vector.duty += duty_delta

    # COHERENCE: Contradictions degrade internal stability
    if qbit.contradiction_active:
        vector.coherence -= 25.0  # Major coherence hit per contradiction

    # Cloud-driven coherence erosion (slow degradation at high Cloud)
    if qbit.cloud_pressure > 75:
        vector.coherence -= (qbit.cloud_pressure - 75) * 0.5  # 0-12.5 at Cloud 100

    # Clamp all values
    vector.clamp()


def calculate_breakdown_risk(vector: VectorState) -> float:
    """
    Calculate NPC's risk of emotional breakdown.

    Breakdown risk is high when:
    - Fear is high + morale is low
    - Coherence is degraded
    - Duty conflicts with survival instinct (high duty + high fear)

    Returns:
        Breakdown risk (0-1, where 1.0 = imminent breakdown)
    """
    # Base risk from coherence degradation
    risk = (100 - vector.coherence) / 100.0  # 0-1

    # Fear amplifier (high fear increases risk)
    if vector.fear > 70:
        risk += (vector.fear - 70) / 100.0  # +0 to +0.3

    # Morale amplifier (low morale increases risk)
    if vector.morale < -30:
        risk += abs(vector.morale + 30) / 100.0  # +0 to +0.7

    # Duty conflict (high duty + high fear = torn between obligation and survival)
    if vector.duty > 70 and vector.fear > 70:
        risk += 0.3  # Severe internal conflict

    return min(1.0, risk)


def get_emotional_action_modifier(vector: VectorState) -> Dict[str, float]:
    """
    Get action probability modifiers based on emotional state.

    Returns:
        Dict of action types → probability multipliers
        - flee_probability: Chance to run away
        - attack_probability: Chance to attack
        - freeze_probability: Chance to freeze/do nothing
        - comply_probability: Chance to follow duty/orders
    """
    return {
        "flee_probability": max(0.0, (vector.fear - 50) / 50),  # 0-1
        "attack_probability": max(0.0, (vector.morale + 50) / 150),  # 0-0.66
        "freeze_probability": calculate_breakdown_risk(vector),
        "comply_probability": max(0.0, vector.duty / 100),  # 0-1
        "coherent_action": vector.coherence / 100  # 0-1 (can they act rationally?)
    }


# ============================================================================
# INTEGRATION HELPERS
# ============================================================================

def create_vector_from_npc_spine(spine) -> VectorState:
    """
    Initialize Vector state from NPCSpine.

    Args:
        spine: NPCSpine object with qbit_power, qbit_charisma

    Returns:
        Initialized VectorState with baseline emotional values
    """
    vector = VectorState()

    # High-power NPCs start with higher duty
    if hasattr(spine, 'qbit_power'):
        vector.duty = min(100.0, 30.0 + (spine.qbit_power / 3000) * 50)

    # High-charisma NPCs start with higher morale
    if hasattr(spine, 'qbit_charisma'):
        vector.morale = min(100.0, (spine.qbit_charisma / 3000) * 80 - 40)

    return vector


def create_qbit_state_from_world(cloud, zone_id: str = "", npc_id: str = "") -> QBITState:
    """
    Create QBITState snapshot from world objects.

    Args:
        cloud: Cloud object with .level, .mood, zones
        zone_id: Current zone ID
        npc_id: NPC ID (for contradiction check)

    Returns:
        QBITState snapshot
    """
    qbit = QBITState()

    # Cloud pressure
    if hasattr(cloud, 'level'):
        qbit.cloud_pressure = cloud.level

    # Entropy from Cloud trend
    if hasattr(cloud, 'trend'):
        if cloud.trend.value == "spiking":
            qbit.entropy = 1.0
        elif cloud.trend.value == "rising":
            qbit.entropy = 0.6
        elif cloud.trend.value == "stable":
            qbit.entropy = 0.2
        else:  # falling
            qbit.entropy = 0.1

    # Zone turbulence
    if zone_id and hasattr(cloud, 'zones') and zone_id in cloud.zones:
        zone = cloud.zones[zone_id]
        qbit.zone_turbulence = zone.turbulence

    return qbit


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("QBIT → VECTOR EMOTIONAL BRIDGE TEST")
    print("="*60)

    # Create baseline Vector
    vector = VectorState()
    print(f"\nBaseline Vector:")
    print(f"  Fear: {vector.fear:.1f}")
    print(f"  Morale: {vector.morale:.1f}")
    print(f"  Duty: {vector.duty:.1f}")
    print(f"  Coherence: {vector.coherence:.1f}")
    print(f"  Profile: {vector.get_emotional_profile()}")

    # Simulate Cloud pressure rising
    print(f"\n--- Cloud Rises to 65 (STRAINED) ---")
    qbit = QBITState(
        cloud_pressure=65.0,
        entropy=0.6,
        influence_score=1500,
        zone_turbulence=3.0
    )
    inject_qbit_to_vector(vector, qbit)
    print(f"  Fear: {vector.fear:.1f} (+{qbit.cloud_pressure * 0.4 + qbit.zone_turbulence * 2:.1f})")
    print(f"  Morale: {vector.morale:.1f} ({qbit.entropy * -30:.1f})")
    print(f"  Duty: {vector.duty:.1f} (+{min(qbit.influence_score * 0.02, 50):.1f})")
    print(f"  Coherence: {vector.coherence:.1f}")
    print(f"  Profile: {vector.get_emotional_profile()}")

    # Simulate contradiction
    print(f"\n--- NPC Breaks Spine Rule (CONTRADICTION) ---")
    qbit.contradiction_active = True
    qbit.cloud_pressure = 85.0
    inject_qbit_to_vector(vector, qbit)
    print(f"  Fear: {vector.fear:.1f}")
    print(f"  Morale: {vector.morale:.1f}")
    print(f"  Duty: {vector.duty:.1f}")
    print(f"  Coherence: {vector.coherence:.1f} (contradiction penalty)")
    print(f"  Profile: {vector.get_emotional_profile()}")

    # Breakdown risk
    risk = calculate_breakdown_risk(vector)
    print(f"\n  Breakdown Risk: {risk:.2%}")

    # Action modifiers
    actions = get_emotional_action_modifier(vector)
    print(f"\n  Action Probabilities:")
    for action, prob in actions.items():
        print(f"    {action}: {prob:.2%}")

    print("\n" + "="*60)
    print("BRIDGE ACTIVE: Entities now feel the world")
    print("="*60)
