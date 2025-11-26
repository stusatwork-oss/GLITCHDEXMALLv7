# SORA SHOT COMMANDS

Command vocabulary for scene generation and transitions.

---

## Core Commands

### `<<cold-open>>`
**Function:** Establish empty, liminal atmosphere
**Visual:** Static or slow drift, no NPCs, high cloud mood
**Audio:** Ambient hum, HVAC, fluorescent buzz
**Duration:** 5-15s
**Use:** Opening shots, establishing mood

**Example:**
```
<<cold-open>>
Zone: FC-ARCADE
Camera: Static wide, slightly elevated
Lighting: Fluorescent, even, stale
Population: Empty
Cloud: 67-100 (High)
```

---

### `<<continue-shooting>>`
**Function:** Maintain current scene parameters, extend duration
**Visual:** Continue previous shot logic
**Audio:** Continuous from previous
**Duration:** +10-30s
**Use:** Extend established scenes, ambient observation

**Example:**
```
<<continue-shooting>>
Duration: +15s
Adjust: Slow dolly forward
```

---

### `<<anchor-three>>`
**Function:** Compose scene with exactly three anchor NPCs
**Visual:** Triangular blocking, character interaction visible
**Audio:** Dialogue ambient (muffled), footsteps
**Duration:** 10-30s
**Use:** Character-driven scenes, narrative moments

**Example:**
```
<<anchor-three>>
Characters: Janitor, AL GORITHM (reflection), Husband
Zone: FC-ARCADE
Blocking: Triangle formation, centered on glass block wall
Action: Janitor avoids threshold, Husband examines cabinet, AL flickers in glass
Cloud: 62-74 (baseline)
```

---

### `<<glitch-soft>>`
**Function:** Apply Bleed Tier 1-2 visual effects
**Visual:** Subtle geometry distortion, screen flicker, light bloom
**Audio:** Audio/visual desync, faint echoes
**Duration:** 3-8s (effect overlay)
**Use:** Reality glitch moments, cloud pressure spikes

**Example:**
```
<<glitch-soft>>
Type: Auditory hallucination
Effect: Arcade pings in silence
Visual: Screens display impossible games
Duration: 5s
```

---

### `<<memory-loop>>`
**Function:** Trigger nostalgia recursion visuals
**Visual:** Time-blended overlays, era superposition
**Audio:** Layered temporal audio (1985 + 2005 simultaneously)
**Duration:** 5-12s
**Use:** Echo memory sequences, character flashbacks

**Example:**
```
<<memory-loop>>
Eras: 1985 (JOLLY TIME active) + 2005 (empty arcade)
Visual: Overlay fade between populated/abandoned states
Character: Wife (Bookstore) remembering layout
```

---

### `<<echo-drift>>`
**Function:** Auditory hallucination patterns
**Visual:** Sound sources don't match visuals
**Audio:** Spatial audio desync, phantom sounds
**Duration:: 5-10s
**Use:** Cloud Prime Node effects, subsurface geometry resonance

**Example:**
```
<<echo-drift>>
Zone: FC-ARCADE
Effect: Machine pings from cabinets that are off
Visual: Empty arcade, single glowing screen
Audio: Full arcade soundscape (crowd, games, tokens)
```

---

## Scene Composition Commands

### `<<pov-walk>>`
**Function:** First-person traversal
**Camera:** Handheld stabilized, natural gait
**Movement:** Forward walk, 2-4 mph
**Duration:** 10-45s

**Example:**
```
<<pov-walk>>
Start: Food court entrance
End: FC-ARCADE threshold
Path: Descend stairs, approach glass block wall
Speed: Slow (hesitant)
```

---

### `<<vertical-reveal>>`
**Function:** Emphasize vertical geometry (elevator shaft, pit depth)
**Camera:** Tilt up/down, crane movement
**Movement:** Slow reveal of vertical scale
**Duration:** 8-20s

**Example:**
```
<<vertical-reveal>>
Subject: Four-story glass elevator shaft above FC-ARCADE
Camera: Start low (arcade floor), tilt up slowly
Reveal: Full vertical column, pressure vent structure
```

---

### `<<tri-node-pan>>`
**Function:** Show spatial relationships between three connected zones
**Camera:** Slow 180° pan or orbital movement
**Movement:** Smooth, deliberate
**Duration:** 15-30s

**Example:**
```
<<tri-node-pan>>
Nodes: Cinema entrance, FC-ARCADE, Glass elevator
Camera: Orbital from food court center
Speed: Slow (establishes spatial relationship)
```

---

## Cloud State Modifiers

Apply these to any shot to adjust mood:

- `cloud:0-33` → Low Cloud (energetic, optimistic, bright)
- `cloud:34-66` → Mid Cloud (nostalgic, wandering, ambient)
- `cloud:67-100` → High Cloud (abandoned, liminal, entropy)
- `bleed:1` → Subtle reality distortion
- `bleed:2` → Moderate geometry/audio glitches
- `bleed:3+` → Severe contradictions (use sparingly)

---

## Combination Examples

### Example 1: Opening Sequence
```
<<cold-open>>
Zone: FC-ARCADE
Camera: Static wide from upper balcony
Lighting: Fluorescent, stale
Population: Empty
Cloud: 74 (High)
Duration: 10s

<<glitch-soft>>
Effect: Auditory hallucination (arcade pings)
Duration: 5s

<<continue-shooting>>
Duration: +5s
Adjust: Slow push-in toward JOLLY TIME marquee
```

### Example 2: Character Interaction
```
<<anchor-three>>
Characters: Janitor, Husband, Wife (Bookstore)
Zone: FC-ARCADE entrance (glass block wall)
Cloud: 62 (baseline)
Blocking: Janitor maintains boundary, Husband drawn to cabinets, Wife remembers layout

<<memory-loop>>
Character: Wife
Eras: 1985 (active arcade) + V6 (HARD COPY vault)
Duration: 8s
Visual: Overlay arcade machines → bookshelves

<<continue-shooting>>
Duration: +10s
Action: Husband picks up tool (unexplained), begins examining cabinet
```

### Example 3: Vertical Geometry Emphasis
```
<<vertical-reveal>>
Subject: Glass elevator shaft + FC-ARCADE pit
Camera: Start at arcade floor (Z=-1), crane up
Reveal: Four-story vertical column, pressure vent structure
Cloud: 68 (High)
Duration: 15s

<<echo-drift>>
Effect: Elevator hum echoes in arcade pit
Visual: Elevator empty, arcade empty
Audio: Overlapping soundscapes (elevator bell + arcade tokens)
Duration: 6s
```

---

## Shot Command Syntax

```
<<command-name>>
Parameter: Value
Parameter: Value
...
```

**Rules:**
- One command per block
- Parameters are optional (defaults apply)
- Commands can stack sequentially
- Duration accumulates across `<<continue-shooting>>`
- Cloud/bleed modifiers override defaults

---

*Template version: 1.0*
*Last updated: 2025-11-21*
