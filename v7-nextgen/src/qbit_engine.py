#!/usr/bin/env python3
"""
QBIT Influence Engine (Python Port)

Portable scoring engine for any entity that needs:
 - power       → structural / systemic leverage (0-3000)
 - charisma    → attention / resonance / engagement (0-3000)
 - overall     → combined influence score (0-6000)
 - rarity      → tier label based on overall

Python port of ai/pipelines/influence/engine.js for v6 integration.

Expected input shape:
  entity = {
    "id": "leisurely-leon",
    "name": "Leisurely Leon",
    "role": "Primary" | "Secondary",
    "type": "npc" | "zone" | "artifact" | "anomaly" | "org" | ...,
    "metrics": {
      "resonanceScore":     0-100,
      "grassrootsSupport":  count (0+),
      "audienceSize":       0+,
      "deepViewCount":      0+,
      "engagementScore":    0-100,
      "referenceCount":     0+,
      "trustScore":         0-100,
      "backingVolume":      0+ (budget, power feed),
      "resourcePool":       0+ (mass, inventory, energy),
      "networkReach":       0+ (# of zones/systems affected)
    }
  }
"""

import math
import random
from typing import Dict, List, Optional


def calculate_charisma(metrics: Optional[Dict] = None) -> int:
    """
    Calculate the Charisma score for an entity.
    Charisma ≈ how much attention / emotional pull / narrative gravity it has.

    Args:
        metrics: Dict of entity metrics

    Returns:
        Charisma score in [0, 3000]
    """
    if metrics is None:
        metrics = {}

    # Neutral baseline if metrics are unusable
    if metrics.get("error"):
        return 500

    charisma = 0.0

    resonance_score = metrics.get("resonanceScore", 30)           # 0-100
    grassroots_support = metrics.get("grassrootsSupport", 10000)  # 0-10M
    audience_size = metrics.get("audienceSize", 1000)             # >0
    deep_view_count = metrics.get("deepViewCount", 100000)        # 0-50M
    engagement_score = metrics.get("engagementScore", 20)         # 0-100
    reference_count = metrics.get("referenceCount", 50)           # 0-5000
    trust_score = metrics.get("trustScore", 50)                   # 0-100

    # 1) Resonance / approval (0-100 → 0-600, capped)
    charisma += min((resonance_score / 100) * 600, 600)

    # 2) Grassroots support (0-10M → 0-600, capped)
    charisma += min((grassroots_support / 10_000_000) * 600, 600)

    # 3) Audience size (log10 scaling to avoid huge follower inflation, capped)
    charisma += min(math.log10(max(1, audience_size)) * 70, 450)

    # 4) Deep attention / time spent (0-50M → 0-600, capped at 450)
    charisma += min((deep_view_count / 50_000_000) * 600, 450)

    # 5) Engagement (0-100 → 0-400, capped at 300)
    charisma += min((engagement_score / 100) * 400, 300)

    # 6) References + trust combined
    reference_component = (reference_count / 5000) * 300
    trust_component = (trust_score / 100) * 300
    charisma += min(reference_component + trust_component, 300)

    # Global cap
    return round(min(charisma, 3000))


def calculate_power(entity: Optional[Dict] = None, metrics: Optional[Dict] = None) -> int:
    """
    Calculate the Power score for an entity.
    Power ≈ structural leverage, systemic weight, ability to move things.

    Args:
        entity: Entity dict (must include .role)
        metrics: Dict of entity metrics

    Returns:
        Power score in [0, 3000]
    """
    if entity is None:
        entity = {}
    if metrics is None:
        metrics = {}

    if metrics.get("error"):
        return 500

    role = entity.get("role", "Secondary")

    power = 0.0

    backing_volume = metrics.get("backingVolume", 100_000)      # 0-100M
    resource_pool = metrics.get("resourcePool", 1_000_000)      # 0-250B
    network_reach = metrics.get("networkReach", 10)             # 0-100

    if role == "Primary":
        # Primary actors: bosses, prime anomalies, major zones, major NPCs
        power += min((backing_volume / 100_000_000) * 600, 600)

        # Seniority / legacy fuzz – placeholder for "been here a long time"
        power += random.random() * 1000

        # Rare leadership spark (+500 about 20% of the time)
        if random.random() > 0.8:
            power += 500
    else:
        # Secondary actors: artifacts, support entities, background anomalies
        power += min((resource_pool / 250_000_000_000) * 1500, 1500)
        power += min((network_reach / 100) * 1000, 1000)

    return round(min(power, 3000))


def determine_rarity(overall: float) -> str:
    """
    Determine rarity band from overall influence.

    Args:
        overall: Expected range [0, 6000]

    Returns:
        "Legendary" | "Epic" | "Rare" | "Common"
    """
    if overall >= 5200:
        return "Legendary"
    if overall >= 4400:
        return "Epic"
    if overall >= 3600:
        return "Rare"
    return "Common"


def score_entity(entity_spine: Dict) -> Dict:
    """
    Score a single entity spine.

    Args:
        entity_spine: Entity dict including .metrics and .role

    Returns:
        New entity dict with .computed = { power, charisma, overall, rarity }
    """
    if not isinstance(entity_spine, dict):
        raise TypeError("score_entity: entity_spine must be a dict")

    metrics = entity_spine.get("metrics", {})

    power = calculate_power(entity_spine, metrics)
    charisma = calculate_charisma(metrics)
    overall = power + charisma
    rarity = determine_rarity(overall)

    # Return new dict with computed scores
    result = entity_spine.copy()
    result["computed"] = {
        "power": power,
        "charisma": charisma,
        "overall": overall,
        "rarity": rarity
    }

    return result


def score_entities(entities: List[Dict]) -> List[Dict]:
    """
    Score an array of entity spines.

    Args:
        entities: List of entity dicts

    Returns:
        List of scored entities
    """
    if not isinstance(entities, list):
        raise TypeError("score_entities: entities must be a list")

    return [score_entity(entity) for entity in entities]


# ========== ZONE AGGREGATION ==========

def calculate_zone_qbit_aggregate(entities: List[Dict], zone_id: str) -> Dict:
    """
    Calculate QBIT aggregate for all entities in a zone.

    Args:
        entities: List of entity dicts (already scored)
        zone_id: Zone identifier (e.g., "FC-ARCADE")

    Returns:
        Dict with zone QBIT stats:
        {
            "zone_id": str,
            "total_power": int,
            "total_charisma": int,
            "total_influence": int,
            "entity_count": int,
            "avg_power": float,
            "avg_charisma": float,
            "rarity_distribution": {"Common": N, "Rare": N, ...},
            "top_entities": [{"id": str, "overall": int}, ...]
        }
    """
    zone_entities = [
        e for e in entities
        if zone_id.lower() in [tag.lower() for tag in e.get("tags", [])]
    ]

    if not zone_entities:
        return {
            "zone_id": zone_id,
            "total_power": 0,
            "total_charisma": 0,
            "total_influence": 0,
            "entity_count": 0,
            "avg_power": 0.0,
            "avg_charisma": 0.0,
            "rarity_distribution": {},
            "top_entities": []
        }

    total_power = sum(e.get("computed", {}).get("power", 0) for e in zone_entities)
    total_charisma = sum(e.get("computed", {}).get("charisma", 0) for e in zone_entities)
    total_influence = total_power + total_charisma
    entity_count = len(zone_entities)

    # Rarity distribution
    rarity_dist = {}
    for entity in zone_entities:
        rarity = entity.get("computed", {}).get("rarity", "Common")
        rarity_dist[rarity] = rarity_dist.get(rarity, 0) + 1

    # Top entities by overall score
    sorted_entities = sorted(
        zone_entities,
        key=lambda e: e.get("computed", {}).get("overall", 0),
        reverse=True
    )
    top_entities = [
        {
            "id": e.get("id", "unknown"),
            "name": e.get("name", "Unknown"),
            "overall": e.get("computed", {}).get("overall", 0)
        }
        for e in sorted_entities[:5]  # Top 5
    ]

    return {
        "zone_id": zone_id,
        "total_power": total_power,
        "total_charisma": total_charisma,
        "total_influence": total_influence,
        "entity_count": entity_count,
        "avg_power": total_power / entity_count if entity_count > 0 else 0.0,
        "avg_charisma": total_charisma / entity_count if entity_count > 0 else 0.0,
        "rarity_distribution": rarity_dist,
        "top_entities": top_entities
    }


# ========== MODULE TESTING ==========

if __name__ == "__main__":
    # Test QBIT engine
    print("=" * 60)
    print("QBIT INFLUENCE ENGINE - Python Port")
    print("=" * 60)

    # Test entity
    test_entity = {
        "id": "leisurely-leon",
        "name": "Leisurely Leon",
        "role": "Secondary",
        "type": "arcade_cabinet",
        "tags": ["fc-arcade", "entropy_sink", "liminal"],
        "metrics": {
            "resonanceScore": 72,
            "grassrootsSupport": 120,
            "audienceSize": 2500,
            "deepViewCount": 120000,
            "engagementScore": 68,
            "referenceCount": 430,
            "trustScore": 55,
            "backingVolume": 0,
            "resourcePool": 10,
            "networkReach": 2
        }
    }

    print("\nScoring test entity...")
    scored = score_entity(test_entity)

    print(f"\nEntity: {scored['name']} ({scored['id']})")
    print(f"  Role: {scored['role']}")
    print(f"  Type: {scored['type']}")
    print(f"\nComputed Scores:")
    print(f"  Power:    {scored['computed']['power']:>4}")
    print(f"  Charisma: {scored['computed']['charisma']:>4}")
    print(f"  Overall:  {scored['computed']['overall']:>4}")
    print(f"  Rarity:   {scored['computed']['rarity']}")

    # Test zone aggregate
    print("\n" + "=" * 60)
    print("Zone Aggregate Test")
    print("=" * 60)

    entities = [scored]
    zone_stats = calculate_zone_qbit_aggregate(entities, "fc-arcade")

    print(f"\nZone: {zone_stats['zone_id']}")
    print(f"  Entity Count: {zone_stats['entity_count']}")
    print(f"  Total Influence: {zone_stats['total_influence']}")
    print(f"  Avg Power: {zone_stats['avg_power']:.1f}")
    print(f"  Avg Charisma: {zone_stats['avg_charisma']:.1f}")
    print(f"\nRarity Distribution:")
    for rarity, count in zone_stats['rarity_distribution'].items():
        print(f"  {rarity}: {count}")
    print(f"\nTop Entities:")
    for entity in zone_stats['top_entities']:
        print(f"  {entity['name']} ({entity['id']}): {entity['overall']}")

    print("\n✓ QBIT Engine test complete")
