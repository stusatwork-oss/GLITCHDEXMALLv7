#!/usr/bin/env python3
"""
Batch Entity Scoring Script

Scores all entities in canon/entities/ directory and generates ranking report.
"""

import json
from pathlib import Path
from qbit_engine import score_entity

def batch_score_entities(entities_dir: str = "../canon/entities"):
    """Score all entity JSONs and generate report."""
    entities_path = Path(__file__).parent / entities_dir

    if not entities_path.exists():
        print(f"Error: {entities_path} does not exist")
        return

    json_files = list(entities_path.glob("*.json"))

    if not json_files:
        print(f"No JSON files found in {entities_path}")
        return

    print("=" * 70)
    print("QBIT ENTITY BATCH SCORING")
    print("=" * 70)
    print(f"\nScoring {len(json_files)} entities from {entities_path}")

    scored_entities = []

    for json_file in sorted(json_files):
        try:
            with open(json_file, 'r') as f:
                entity = json.load(f)

            # Score entity
            scored = score_entity(entity)
            scored_entities.append(scored)

            # Write back scored entity
            with open(json_file, 'w') as f:
                json.dump(scored, f, indent=2)

            print(f"✓ {entity['id']:<25} | "
                  f"Power: {scored['computed']['power']:>4} | "
                  f"Charisma: {scored['computed']['charisma']:>4} | "
                  f"Overall: {scored['computed']['overall']:>4} | "
                  f"{scored['computed']['rarity']}")

        except Exception as e:
            print(f"✗ {json_file.name}: {e}")

    # Generate ranking report
    print("\n" + "=" * 70)
    print("ENTITY RANKINGS (by Overall Score)")
    print("=" * 70)

    # Sort by overall score
    ranked = sorted(scored_entities,
                   key=lambda e: e['computed']['overall'],
                   reverse=True)

    print(f"\n{'Rank':<6} {'ID':<25} {'Type':<12} {'Overall':<8} {'Rarity':<12}")
    print("-" * 70)

    for i, entity in enumerate(ranked, 1):
        print(f"{i:<6} {entity['id']:<25} {entity['type']:<12} "
              f"{entity['computed']['overall']:<8} {entity['computed']['rarity']:<12}")

    # Category breakdowns
    print("\n" + "=" * 70)
    print("CATEGORY BREAKDOWNS")
    print("=" * 70)

    # By role
    print("\nBy Role:")
    primary = [e for e in scored_entities if e['role'] == 'Primary']
    secondary = [e for e in scored_entities if e['role'] == 'Secondary']

    if primary:
        avg_primary = sum(e['computed']['overall'] for e in primary) / len(primary)
        print(f"  Primary ({len(primary)}):   Avg Overall = {avg_primary:.1f}")

    if secondary:
        avg_secondary = sum(e['computed']['overall'] for e in secondary) / len(secondary)
        print(f"  Secondary ({len(secondary)}): Avg Overall = {avg_secondary:.1f}")

    # By type
    print("\nBy Type:")
    types = {}
    for entity in scored_entities:
        entity_type = entity['type']
        if entity_type not in types:
            types[entity_type] = []
        types[entity_type].append(entity['computed']['overall'])

    for entity_type, scores in sorted(types.items()):
        avg_score = sum(scores) / len(scores)
        print(f"  {entity_type:<15} ({len(scores)}): Avg Overall = {avg_score:.1f}")

    # Anchor NPC candidates
    print("\n" + "=" * 70)
    print("ANCHOR NPC CANDIDATES (Overall > 3000)")
    print("=" * 70)

    anchor_candidates = [e for e in ranked if e['computed']['overall'] > 3000]

    if anchor_candidates:
        print(f"\nFound {len(anchor_candidates)} candidates:\n")
        for entity in anchor_candidates:
            print(f"  {entity['name']}")
            print(f"    ID:       {entity['id']}")
            print(f"    Type:     {entity['type']}")
            print(f"    Role:     {entity['role']}")
            print(f"    Power:    {entity['computed']['power']}")
            print(f"    Charisma: {entity['computed']['charisma']}")
            print(f"    Overall:  {entity['computed']['overall']}")
            print(f"    Rarity:   {entity['computed']['rarity']}")
            print(f"    Tags:     {', '.join(entity['tags'][:3])}")
            print()
    else:
        print("\nNo entities scored above 3000 threshold.")
        print("Top 3 candidates:")
        for entity in ranked[:3]:
            print(f"  - {entity['name']} ({entity['computed']['overall']})")

    # Zone influence summary
    print("=" * 70)
    print("ZONE INFLUENCE SUMMARY")
    print("=" * 70)

    zones = {}
    for entity in scored_entities:
        for tag in entity['tags']:
            # Common zone tags
            zone_tags = ['fc-arcade', 'corridor', 'service_hall', 'store_bored',
                        'store_milo_optics', 'ramp', 'atrium', 'food_court']
            if tag.lower() in zone_tags:
                zone_name = tag.upper()
                if zone_name not in zones:
                    zones[zone_name] = []
                zones[zone_name].append({
                    'id': entity['id'],
                    'overall': entity['computed']['overall']
                })

    print("\nEntities per zone:\n")
    for zone, entities in sorted(zones.items(), key=lambda x: -sum(e['overall'] for e in x[1])):
        total_influence = sum(e['overall'] for e in entities)
        print(f"  {zone}:")
        print(f"    Entities: {len(entities)}")
        print(f"    Total Influence: {total_influence}")
        print(f"    Top Entity: {max(entities, key=lambda e: e['overall'])['id']}")
        print()

    print("=" * 70)
    print(f"✓ Batch scoring complete. {len(scored_entities)} entities processed.")
    print("=" * 70)


if __name__ == "__main__":
    batch_score_entities()
