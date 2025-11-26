# Spynt - Character Spine System

JSON-based character identity and behavioral schemas for GLUTCHDEXMALL.

## Purpose

**Spynt** (Spine + Intent) defines NPC identities through structured JSON documents called "spines." Each spine captures:

- Core identity (name, role, era, faction)
- Memory patterns and key experiences
- Contradiction triggers and fault lines
- Behavioral weights and decision patterns
- Relationships and social graph position

## Schema Structure

```json
{
  "character_id": "string",
  "name": "string",
  "role": "string",
  "era": "1981_opening | 1995_peak | 2005_decline | 2011_closure",
  "faction": "string",
  "spine": {
    "core_memory": ["key experiences"],
    "contradictions": ["internal conflicts"],
    "triggers": ["reality glitch conditions"],
    "relationships": {
      "character_id": "relationship_type"
    }
  },
  "behavior": {
    "goap_goals": ["goal weights"],
    "stealth_awareness": 0-100,
    "heat_tolerance": 0-5
  },
  "metadata": {
    "version": "v4 | v5 | v6",
    "photo_refs": ["source photos"],
    "author": "string",
    "last_updated": "ISO date"
  }
}
```

## Examples

See `examples/` for:
- `anchor_npc_template.json` - Template for anchor NPCs (v4 architecture)
- `swarm_npc_template.json` - Template for ambient crowd (v4 architecture)
- `eastland_employee_1981.json` - Sample from opening era
- `mall_walker_1995.json` - Sample from peak era

## Integration

Spynt schemas are consumed by:
- `v6-nextgen/src/simulation/npc_system.py`
- `ai/mallOS/cloud.py` for contradiction tracking
- `ai/sora/anchor_placement.py` for video generation

## Validation

Run `pipelines/validate_spynt.py` to check schema compliance.

---

*Spines are the memory—everything else is rendering.*
