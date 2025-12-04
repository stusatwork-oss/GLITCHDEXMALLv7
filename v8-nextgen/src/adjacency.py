#!/usr/bin/env python3
"""
QBIT-Weighted Adjacency Influence System

Calculates dynamic adjacency probabilities between zones based on:
- QBIT entity influence (zone personality gravity)
- Resonance accumulation (memory stickiness)
- Turbulence levels (instability)

High-QBIT zones become "attractors" - they pull narrative attention,
NPC movement, and bleed events toward them.

Usage:
    from adjacency import compute_adjacency_probabilities

    adjacency_matrix = compute_adjacency_probabilities(zones, qbit_map)
    for zone_id, zone in zones.items():
        zone.adjacency = adjacency_matrix[zone_id]
"""

import random
import math
from typing import Dict, Optional


def compute_adjacency_probabilities(zones: Dict, qbit_map: Optional[Dict] = None) -> Dict:
    """
    Calculate QBIT-weighted adjacency probabilities between zones.

    Zones with high QBIT scores become narrative/spatial attractors.

    Args:
        zones: Dict of zone_id → ZoneMicrostate
        qbit_map: Dict of entity_id → QBITScore (optional, can use zone.qbit_score)

    Returns:
        adjacency_matrix: Dict[zone_id][other_zone] = probability (0-1)
    """
    adjacency_matrix = {}

    for zone_id, zone in zones.items():
        # Collect QBIT signature for the zone
        # zone.qbit_score is 0-6000+ (raw), normalize to 0-10
        qbit_score = getattr(zone, 'qbit_aggregate', 0) / 600  # 0-10 scale
        qbit_score = min(10, qbit_score)  # Cap at 10

        resonance = getattr(zone, 'resonance', 0) / 100   # 0-1 normalized
        resonance = min(1.0, resonance)

        turbulence = getattr(zone, 'turbulence', 0) / 10  # 0-1 normalized
        turbulence = min(1.0, turbulence)

        # Core gravity: zones with high QBIT become attractors
        # Formula: 60% QBIT score + 30% resonance + 10% turbulence
        qbit_gravity = (qbit_score * 0.6) + (resonance * 0.3) + (turbulence * 0.1)

        # Base probability container
        adjacency_matrix[zone_id] = {}

        for other_zone_id, other_state in zones.items():
            if other_zone_id == zone_id:
                continue  # Skip self

            # Calculate other zone's QBIT signature
            other_qbit = getattr(other_state, 'qbit_aggregate', 0) / 600
            other_qbit = min(10, other_qbit) / 10  # Normalize to 0-1

            other_res = getattr(other_state, 'resonance', 0) / 100
            other_res = min(1.0, other_res)

            other_turb = getattr(other_state, 'turbulence', 0) / 10
            other_turb = min(1.0, other_turb)

            # Influence = similarity + gravity + random drift
            # Similarity: zones with similar QBIT scores "resonate"
            similarity = 1.0 - abs(other_qbit - (qbit_score / 10))
            similarity = max(0.0, similarity)

            # Gravity pull: attractor strength
            gravity_pull = qbit_gravity + (other_qbit * 0.5)

            # Random drift: prevents deterministic patterns
            drift = random.uniform(0.0, 0.15)

            # Final probability
            # 45% similarity (like attracts like)
            # 45% gravity (high-QBIT zones pull attention)
            # 10% resonance (memory creates sticky connections)
            # + drift (entropy)
            p = (
                similarity * 0.45 +
                gravity_pull * 0.45 +
                other_res * 0.1 +
                drift
            )

            adjacency_matrix[zone_id][other_zone_id] = max(0, p)

        # Normalize row (probabilities sum to 1.0)
        total = sum(adjacency_matrix[zone_id].values())
        if total > 0:
            for k in adjacency_matrix[zone_id]:
                adjacency_matrix[zone_id][k] /= total

    return adjacency_matrix


def get_adjacent_zone_weighted(zone_id: str, adjacency_matrix: Dict) -> Optional[str]:
    """
    Select an adjacent zone weighted by QBIT-influenced probabilities.

    Args:
        zone_id: Current zone
        adjacency_matrix: Computed adjacency probabilities

    Returns:
        Selected adjacent zone_id (or None if no adjacency data)
    """
    if zone_id not in adjacency_matrix:
        return None

    probabilities = adjacency_matrix[zone_id]
    if not probabilities:
        return None

    # Weighted random selection
    zones = list(probabilities.keys())
    weights = list(probabilities.values())

    return random.choices(zones, weights=weights, k=1)[0]


def calculate_zone_influence_rank(zones: Dict) -> list:
    """
    Rank zones by total QBIT influence (attractor strength).

    Args:
        zones: Dict of zone_id → ZoneMicrostate

    Returns:
        List of (zone_id, influence_score) tuples, sorted descending
    """
    rankings = []

    for zone_id, zone in zones.items():
        qbit_score = getattr(zone, 'qbit_aggregate', 0)
        resonance = getattr(zone, 'resonance', 0)
        turbulence = getattr(zone, 'turbulence', 0)

        # Influence = QBIT aggregate + resonance + turbulence
        influence = qbit_score + (resonance * 10) + (turbulence * 100)

        rankings.append((zone_id, influence))

    # Sort by influence descending
    rankings.sort(key=lambda x: x[1], reverse=True)

    return rankings


# ========== MODULE TESTING ==========

if __name__ == "__main__":
    print("=" * 60)
    print("QBIT-WEIGHTED ADJACENCY INFLUENCE TEST")
    print("=" * 60)

    # Mock ZoneMicrostate for testing
    class MockZone:
        def __init__(self, zone_id, qbit_aggregate, resonance, turbulence):
            self.zone_id = zone_id
            self.qbit_aggregate = qbit_aggregate
            self.resonance = resonance
            self.turbulence = turbulence
            self.adjacency = {}

    # Create test zones
    zones = {
        "FC-ARCADE": MockZone("FC-ARCADE", 1154, 50, 7),      # High QBIT, high turbulence
        "SERVICE_HALL": MockZone("SERVICE_HALL", 300, 20, 5),  # Medium
        "CORRIDOR": MockZone("CORRIDOR", 100, 10, 2),          # Low
        "STORE_BORED": MockZone("STORE_BORED", 500, 30, 3),    # Medium-low
    }

    print("\nZone Signatures:")
    for zone_id, zone in zones.items():
        print(f"\n  {zone_id}:")
        print(f"    QBIT Aggregate: {zone.qbit_aggregate}")
        print(f"    Resonance:      {zone.resonance}")
        print(f"    Turbulence:     {zone.turbulence}")

    # Compute adjacency
    print("\n" + "-" * 60)
    print("Computing QBIT-weighted adjacency probabilities...")
    adjacency = compute_adjacency_probabilities(zones)

    print("\nAdjacency Matrix:")
    for zone_id, probs in adjacency.items():
        print(f"\n  From {zone_id}:")
        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        for other_zone, prob in sorted_probs:
            print(f"    → {other_zone}: {prob:.3f}")

    # Test weighted selection
    print("\n" + "-" * 60)
    print("Testing weighted zone selection (10 samples):")

    for i in range(10):
        selected = get_adjacent_zone_weighted("FC-ARCADE", adjacency)
        print(f"  Sample {i+1}: FC-ARCADE → {selected}")

    # Calculate influence rankings
    print("\n" + "-" * 60)
    print("Zone Influence Rankings:")

    rankings = calculate_zone_influence_rank(zones)
    for i, (zone_id, influence) in enumerate(rankings, 1):
        print(f"  {i}. {zone_id}: {influence:.1f}")

    # Verify high-QBIT zone is top attractor
    top_zone = rankings[0][0]
    print(f"\n✓ Top attractor: {top_zone}")

    assert top_zone == "FC-ARCADE", "FC-ARCADE should be top attractor"
    print("✓ QBIT-weighted adjacency test passed")
