# GLITCHDEX MALL ENGINE – DESIGN OVERVIEW

## Vision

A first-person, tile-based dungeon crawler set in a 1988-style shopping mall. The game is a **narrative sandbox** with no objectives, no traditional win/loss, and one environmental "boss": an invisible, ever-present unattended toddler whose presence intensifies as playtime increases.

## Core Mechanics

### Movement & Navigation
- **Tile-to-tile grid**: 4-directional (N/S/E/W)
- **First-person perspective**: Raycaster renderer (broken DOS-era style)
- **No pathfinding**: Player moves manually
- **Collision**: Simple tile blocking
- **Must exit via entrance**: Only way to end the game safely

### Time = Intensity
- Playtime counter tracks session duration
- As time passes, the **Toddler Presence** escalates through 3 stages
- Player feels creeping dread (auditory + visual effects)
- Creates natural pacing pressure without mechanical fail states

### Artifact Discovery
- Random objects scattered through mall
- Player picks them up (added to inventory)
- Carrying artifacts makes things *weirder*
  - Visual glitches increase
  - NPC reactions change
  - Toddler presence intensifies
- **Milo is the lore-keeper**: Only NPC who tells the story of each artifact

### NPC Interaction
- Sparse population (1988 Nintendo style)
- Random encounters with iconic characters:
  - **Milo** (at counter, sometimes wandering)
  - **BORED** (in shop)
  - **R0-MBA** (roaming, logging events)
  - **Mall Cop** (patrol routes)
  - **Generic Shoppers** (few, idling or wandering)
- Dialogue is environmental flavor, not progression gates
- NPCs react to toddler stages and artifacts player carries

### The Toddler (Invisible Environmental Boss)
- Never appears on screen
- Presence manifests through:
  - **Audio**: Distant cries → wails → screaming (volume + frequency increase)
  - **Shadow**: Rare glimpses → visible in corners → fills corridors
  - **Events**: Objects shift, crowds panic, escalators malfunction
- **Stage progression**:
  - **Stage 1** (0–5 min): Occasional distant sounds, rare shadows
  - **Stage 2** (5–15 min): Frequent wails, shadow increasingly visible
  - **Stage 3** (15+ min): Constant screaming, chaos events, tremors
- Pressure to exit increases with playtime

## Design Constraints

### Small, Finite, Legible
- **Tile types**: ~15–20 defined
- **NPC types**: 5 canonical + 1 generic
- **Artifacts**: 10–15 cursed/weird objects
- **Mall size**: Single floor, ~50×50 tiles (roughly 12 key locations)

### No Physics Engine
- Dungeon crawler rules only
- Collision boxes, simple triggers, "use" flags
- No gravity, momentum, smooth interpolation

### Xennial Mall Aesthetic
- Late 80s–early 2000s vibes
- B. Dalton bookstore, Waldenbooks, dying anchor stores
- Food court, escalators, service corridors
- No smartphones, modern retail, or contemporary logic

### Narrative-Friendly, Not Graphics-Heavy
- Text-mode + minimal raycaster rendering
- Focus on state, logs, and flavor text
- Jank is intentional (30KB DOS-era broken 3D)

## Player Experience Flow

1. **Enter mall** → First-person view established, Milo waves from his counter
2. **Explore freely** → Sparse NPCs at fixed/random locations, artifacts scattered
3. **Pick up artifacts** → "Found sunglasses near BORED's shop"
4. **Talk to Milo** → Hear the artifact's strange backstory
5. **Wander more** → Time passes, audio starts
6. **Stage 1** → Distant cries, occasional shadow
7. **Keep playing** → Things escalate
8. **Stage 2** → Wails are audible, shadow visible in edges
9. **Panic creeps in** → Player feels pressure
10. **Stage 3** → Screaming, chaos, impossible to ignore
11. **Exit or persist** → Player must navigate to entrance to leave, or keep playing and face the creep
12. **Leave** → Game ends at entrance

## Toddler Presence as Mechanic

The toddler is **not a literal boss fight**. It's:
- An **environmental stressor** that scales with playtime
- A **narrative anchor** that explains why you need to leave
- A **pressure system** that creates pacing without explicit fail states
- **Pure atmosphere**: Shadow on walls, echoes in vents, displaced objects

## Artifacts as Narrative Engines

Each artifact found has a story, told only by Milo:
- "This sunglasses came from 1994. Kid left them in BORED's dressing room. He never came back."
- "This Necronomicon bookmark... it was used to hold a place in a book that disappeared. No one remembers the book."
- "These stickers were from a rave in '98. Everyone who had them moved away that summer."

Carrying multiple artifacts makes the game *weirder*—more glitches, more visual distortion, faster toddler escalation.

## Game State

- **Player position** (x, y, z, facing)
- **Inventory** (artifact list)
- **Playtime** (elapsed seconds)
- **Toddler stage** (0–3, derived from playtime)
- **NPC positions** (patrolling, idling)
- **Event log** (for narrative flavor)

## No Fail States, No Points

- No health bar, no stamina, no inventory limit
- No combat, no puzzles, no critical paths
- Game ends by **reaching entrance** (success) or **quitting** (escape)
- Playtime is the only progression metric

## File Structure References

- **mall_map.json**: Grid layout, tile types, fixed NPC spawns
- **entities.json**: NPC definitions, behavior rules
- **artifacts.json**: Item definitions, lore, weirdness properties
- **stores.json**: Shop flavor text, special tiles
- **src/mall_engine.py**: Core tile system
- **src/wolf_renderer.py**: Wolfenstein 3D raycaster + reality glitches
- **src/reality_glitch.py**: Modern rendering that bleeds through facade
- **src/toddler_system.py**: Audio, shadow, events
- **src/game_loop.py**: Input handling, state updates
