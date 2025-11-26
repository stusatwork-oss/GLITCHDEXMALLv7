# Sora - Video Generation Logic

Prompt templates and shot logic for video generation systems (Sora, Runway, etc.)

## Purpose

This directory contains structured prompt templates and scene composition logic for generating video content of Eastland Mall spaces and characters.

## Components

### `templates/`
Reusable prompt templates:
- `atrium_establishing.txt` - Wide shots of main atrium
- `corridor_walk.txt` - First-person corridor traversal
- `food_court_ambient.txt` - Ambient food court scenes
- `escalator_ascent.txt` - Escalator POV shots

### `anchors/`
Anchor NPC placement and scene composition:
- `npc_positions.json` - Canonical positions for 13 anchor NPCs
- `zone_population.json` - Swarm density per zone
- `shot_rules.json` - Composition and framing rules

### `shot_logic/`
Scene transition and sequencing:
- `cloud_mood_mapping.json` - How cloud state affects visual tone
- `bleed_events.json` - Reality glitch shot specifications
- `continuity_rules.json` - Maintain consistency across cuts

## Prompt Structure

```
[ESTABLISHING] Wide shot, architectural scale
Zone: {zone_name}
Era: {1981 | 1995 | 2005 | 2011}
Cloud Mood: {tension | wander | surge | bleed}
Lighting: {natural sunlight through tensile roof | fluorescent | dim}
Population: {empty | sparse | moderate | crowded}

[DETAILS]
- Escalator: {visible | not visible}, {operational | stopped}
- Fountain: {active | dry}, height: {measured from v5 CRD}
- Glass block walls: {translucent ambient glow}
- Anchor stores: {open | closed | boarded}

[CAMERA]
Movement: {static | slow dolly | tracking | POV walk}
Focal length: {wide 24mm | standard 50mm | tight 85mm}
Duration: {5s | 10s | 30s}

[REFERENCES]
Photos: {eastlandpics IDs}
CRD Zone: {v5 zone graph reference}
```

## Integration

- Consumed by: `v6-nextgen/src/video_gen/` (future)
- References: `v6-nextgen/canon/zones/`, `ai/spynt/` for NPC placement
- Measurements: `v5-eastland/docs/crd/MEASUREMENT_SHEET_V1.csv`

## Validation

Prompts must reference:
1. Specific CRD zone from v5
2. Era-appropriate details (no post-2011 content in 1981 scenes)
3. Measured dimensions (escalator height, atrium diameter, etc.)

---

*Video is evidence synthesis, not hallucination.*
