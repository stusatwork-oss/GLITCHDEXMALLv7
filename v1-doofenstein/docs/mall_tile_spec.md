# MALL TILE SPECIFICATION

## Tile Types

Each tile is a discrete grid cell with a type, collision properties, and optional associated data.

### Core Tiles

| Type | Symbol | Walkable | Description |
|------|--------|----------|-------------|
| **VOID** | `█` | No | Empty/wall (not accessible) |
| **CORRIDOR** | ` ` | Yes | Normal walking space |
| **ENTRANCE** | `E` | Yes | Mall entrance/exit |
| **STORE_GENERIC** | `S` | Yes | Generic shop (no special interaction) |
| **STORE_BORED** | `B` | Yes | BORED skateshop & tee emporium |
| **STORE_MILO_OPTICS** | `M` | Yes | Milo's Discount Optics |
| **FOOD_COURT** | `F` | Yes | Communal eating area |
| **ANCHOR_STORE** | `A` | Yes | Large dying department store |
| **ESCALATOR_UP** | `↑` | Yes | Stairway up (z-layer transition) |
| **ESCALATOR_DOWN** | `↓` | Yes | Stairway down (z-layer transition) |
| **SERVICE_HALL** | `H` | Yes | Back corridors (staff-only flavor) |
| **RESTROOM** | `R` | Yes | Bathroom area |
| **KIOSK** | `K` | Yes | Island stand in corridor |

### Tile Properties

```json
{
  "type": "CORRIDOR",
  "walkable": true,
  "collision": "none",
  "ambient_description": "A long corridor with fluorescent lights hum overhead.",
  "artifacts_pool": ["sticker_sheets", "sunglasses"],
  "npc_spawnable": true,
  "special_effects": []
}
```

## Collision Model

- **Tiles** have explicit walkability flags
- **Player** cannot move into non-walkable tiles
- **NPCs** follow tile walkability rules (can't path through walls)
- **Artifacts** don't block movement (can walk over them)

## Artifact Spawning

Artifacts spawn randomly in certain tile types:
- `CORRIDOR` – common (50% chance of containing 1 artifact)
- `STORE_GENERIC` – common (40%)
- `FOOD_COURT` – rare (20%)
- `ANCHOR_STORE` – common (50%)
- `SERVICE_HALL` – rare (15%)

Each artifact tile has a **pool of possible items** that can spawn there.

## NPC Behavior by Tile

### Fixed Spawns
- **Milo** → STORE_MILO_OPTICS (default), occasional wander to FOOD_COURT
- **BORED** → STORE_BORED (stays put)
- **Mall Cop** → SERVICE_HALL (patrol routes)

### Roaming
- **R0-MBA** → Starts SERVICE_HALL, random patrol algorithm
- **Generic Shoppers** → Spawn FOOD_COURT, idle or random walk

## Toddler Presence by Tile

Certain tiles amplify or reduce toddler presence:

| Tile Type | Presence Intensity |
|-----------|-------------------|
| FOOD_COURT | High (crowds, noise) |
| ANCHOR_STORE | Medium (echoes) |
| CORRIDOR | Low (sparse) |
| SERVICE_HALL | High (vents, sounds carry) |
| ESCALATOR_* | Medium (mechanical sounds mask cries) |
| RESTROOM | Medium (isolated, echoes) |

## Visual Rendering

In first-person view, each tile type renders distinctly:

- **CORRIDOR** → Plain walls, floor, ceiling with mall textures
- **FOOD_COURT** → Open area, tables, benches visible
- **STORE_*BORED** → Shop interior, shelves, merchandise
- **STORE_MILO_OPTICS** → Counter, eyeglass displays
- **ANCHOR_STORE** → Large open space, minimal fixtures
- **SERVICE_HALL** → Bland walls, utility fixtures, vents
- **RESTROOM** → Tiled walls, stalls (don't enter, just outside)
- **ESCALATOR_UP/DOWN** → Stairs, handrails, mechanical look

## Tile Memory & Persistence

- Artifacts persist once spawned (don't respawn)
- NPCs persist in their patrol/spawn locations
- Player discoveries accumulate (can revisit tiles, artifacts don't refresh)
- No dynamic tile changes except toddler-stage events (shadow on tiles, chaos)

## Tile Coordinates

- **X**: Left/Right (0–49)
- **Y**: Forward/Backward (0–49)
- **Z**: Level (0 = ground floor, 1+ = upper levels via escalators)
- **Facing**: 0=North, 1=East, 2=South, 3=West

## Special Tile Events

Certain tiles trigger special behavior:

- **ENTRANCE**: Triggers game-end prompt ("Leave the mall?")
- **FOOD_COURT**: Increased NPC spawning, ambient crowd noise
- **SERVICE_HALL**: Toddler presence louder (vents carry sound)
- **ESCALATOR_***: Can change z-layer on interaction
- **ANCHOR_STORE**: Artifacts more likely, echoes amplify toddler

## Tile JSON Format (mall_map.json)

```json
{
  "name": "Ground Floor",
  "width": 50,
  "height": 50,
  "tiles": [
    {
      "x": 0,
      "y": 0,
      "z": 0,
      "type": "ENTRANCE",
      "walkable": true,
      "description": "The bright mall entrance. You can see the parking lot beyond."
    },
    {
      "x": 10,
      "y": 10,
      "z": 0,
      "type": "STORE_BORED",
      "walkable": true,
      "npc_id": "bored",
      "description": "BORED – Skateshop & Tee Emporium. Posters and graffiti."
    }
  ]
}
```

---

**Note**: This spec is single-floor for MVP. Z-layers and escalators designed for future expansion, but not required for initial build.
