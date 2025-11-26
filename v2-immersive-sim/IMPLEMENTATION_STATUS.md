# GLITCHDEX MALL V2 - IMPLEMENTATION STATUS

**Last Updated:** Session ending with Tier 3 completion

---

## 🎯 VISION

> **"A full AAA immersive sim wearing a cheap Wolf3D Halloween mask that starts to slip as the toddler and glitches escalate."**

What the player SEES: Retro Wolf3D mall crawler in ANSI 256-color terminal art
What's ACTUALLY running: Cutting-edge 2025 game AI and systems

**The Core Experience:**
- Player sees Wolf3D Wolfenstein clone
- NPCs start talking about their "shift schedules" and "patrol routes"
- Player thinks: "Why does this retro game have Skyrim-level dialogue?"
- Heat increases, glitches appear (1-frame pathfinding line flickers)
- Player thinks: "Did I just see...?"
- Heat 5: Full reality break - modern AI exposed, mask shatters
- Player: "IT WAS AAA AI THE WHOLE TIME???"

---

## ✅ COMPLETED SYSTEMS (Tiers 1-5)

### **Tier 1: NPC Dialogue System** ✅

**File:** `dialogue_system.py` (338 lines)

Heat-aware dialogue that reveals AI sophistication as chaos increases.

**Dialogue Progression:**

| Heat | Example Dialogue | Effect |
|------|-----------------|--------|
| 0-1 | "Food court's dead today." | Mundane jank |
| 2 | "My shift ends at 5pm. Then Karen takes over Electronics." | Skyrim-level dissonance |
| 2 | "Sector 7 patrol complete. Moving to waypoint Delta." | NPCs have patrol routes?? |
| 3 | "Waypoint Delta... wait, why am I saying this?" | NPCs notice their own weirdness |
| 4 | "Behavior state: PURSUING. Target: Unknown entity." | GOAP AI leaking through |
| 4 | "Alert level 3... this doesn't feel like a game anymore." | Reality awareness |
| 5 | "AGENT STATE: COMBAT. GOAL: NEUTRALIZE PLAYER ENTITY." | Full AI confession |
| 5 | "This isn't a mall. This is a simulation." | Mask gone |

**Features:**
- 60+ dialogue lines organized by heat tier
- Faction-specific dialogue (security, workers, shoppers, teens)
- Schedule-aware barks (workers mention shift changes)
- Patrol-aware barks (security discusses routes)
- GOAP goal overlays: `[GOAL: wander | PRIORITY:0.30]`
  - Heat 3: 5% chance (rare flickers)
  - Heat 4: 15% chance
  - Heat 5: Always shown

**Test Results:**
```
Heat 0.5: "Everything looks normal."
Heat 2.0: "Management's gonna add another patrol if this keeps up."
Heat 3.2: "Something feels... wrong."
Heat 4.2: "Memory buffer: 73% full. Need to process incident logs."
         [GOAL: wander | PRIORITY:0.30]
Heat 5.0: "This isn't a mall. This is a simulation."
         "I can see the nav mesh now."
```

---

### **Tier 2: Micro-Glitch System** ✅

**File:** `reality_glitch_system.py` (346 lines)

The mask doesn't break instantly at Heat 5. It **CRACKS** at Heat 3.

**Glitch Types (8 total):**
1. `pathfinding_flicker` - AI pathfinding lines visible
2. `name_corruption` - NPCs show as "AI_AGENT_047"
3. `texture_bleed` - Photorealistic textures leak through
4. `engine_stat_popup` - Fake Unreal/Unity stats appear
5. `wireframe_flash` - Wireframe geometry visible
6. `nav_mesh_peek` - Navigation mesh briefly shown
7. `coordinate_overlay` - World coordinates displayed
8. `render_error` - Fake render error messages

**Spawn Frequency by Heat:**

| Heat | Spawn Chance | Expected Frequency | Effect |
|------|-------------|-------------------|---------|
| < 3.0 | 0% | Never | Mask intact |
| 3.0-3.5 | 1% per frame | ~1 per 10 seconds | "Did I just see...?" |
| 3.5-4.0 | 3% per frame | ~1 per 3 seconds | Subtle cracks |
| 4.0-4.5 | 6% per frame | ~1 per second | Player is suspicious |
| 4.5+ | 20% per frame | Multiple per second | Mask failing |

**Glitch Durations:**
- Heat < 3.5: **0.016s** (1 frame at 60fps) - blink and you miss it
- Heat 3.5-4: 0.032-0.083s (2-5 frames)
- Heat 4-4.5: 0.1-0.5 seconds
- Heat 4.5+: 0.5-2 seconds (persistent)

**Test Results:**
```
Heat 3.2: 0% occurrence (rare, RNG)
Heat 4.2: 58% frame coverage
Heat 4.8: 100% frame coverage, up to 3 simultaneous glitches
```

**The Effect:**
Player sees 1-frame pathfinding flicker at Heat 3 → "wait, did I see that?"
Heat 4: Constant wireframe flashes and coordinate overlays → "something's very wrong"
Heat 5: Confirms what they already suspected

---

### **Tier 3: Stealth Feedback** ✅

**File:** `stealth_feedback.py` (194 lines)

Minimal ANSI visual feedback for AAA stealth mechanics. This is Metal Gear Solid in Wolf3D terminal art.

**Alert Symbols (shown above NPCs):**
- `!` = Fully alerted (sees player)
- `!!` = Just detected player
- `?` = Suspicious
- `??` = Searching/investigating
- (none) = Unaware

**Noise Ripples:**
- `~` symbol expands outward from noise sources
- Expands over 2 second duration
- Fades out as it expands
- Visual representation of sound propagation

**Common Noise Profiles:**

| Action | Radius | Intensity | Visual |
|--------|--------|-----------|--------|
| Footstep | 2.0 | 0.2 | Small `~` ripple |
| Kick | 8.0 | 0.6 | Medium ripple |
| Break glass | 15.0 | 0.9 | Large ripple |
| Alarm | 30.0 | 1.0 | Massive ripple |
| Attack | 10.0 | 0.9 | Large ripple |

**Test Results:**
```
✓ Awareness 0.2: No symbol
✓ Awareness 0.4: "?"
✓ Awareness 0.6: "!!"
✓ Awareness 0.9: "!"
✓ Footstep creates ~ ripple (max radius 2.0)
✓ Attack creates ~ ripple (max radius 10.0)
```

**Philosophy:**
- **NO modern UI overlays**
- **NO vision cone graphics**
- **NO health bars**
- Just ASCII symbols - pure terminal art stealth

---

## 🎮 INTEGRATED GAMEPLAY EXPERIENCE

**Example Scenario (from test):**

```
1. Player enters mall (Heat 0)
   [Mall Worker]: "Food court's dead today."

2. Player kicks vending machine (Heat → 1.5)
   ~ noise ripple expands
   Heat: ★☆☆☆☆

3. Security responds (Heat 2-3)
   [Security Guard]: "Management's gonna add another patrol if this keeps up."
   Heat: ★★☆☆☆

4. Guard sees player (Heat increases)
   Guard shows ! alert symbol
   Heat: ★★★☆☆

5. Reality cracks (Heat 3.5+)
   GLITCH: wireframe_flash (0.442s duration)
   GLITCH: texture_bleed (0.819s duration)
   [Security]: "Something feels... wrong."

6. Full chaos (Heat 5)
   [Security]: "AGENT STATE: COMBAT. GOAL: NEUTRALIZE PLAYER ENTITY."
   [Worker]: "This isn't a mall. This is a simulation."
   Constant glitches, GOAP overlays always visible
   Heat: ★★★★★ [SIMULATION FAILURE]
```

---

## 📦 FILE STRUCTURE

```
v2-immersive-sim/
├── src/
│   ├── dialogue_system.py          # Tier 1: Heat-aware NPC dialogue
│   ├── reality_glitch_system.py    # Tier 2: Micro-glitches (mask cracking)
│   ├── stealth_feedback.py         # Tier 3: ANSI alert symbols
│   ├── toddler_system.py           # Tier 4: Invisible reality catalyst
│   ├── renderer_strain_system.py   # Tier 5: Fake performance degradation
│   ├── mall_simulation.py          # Main orchestrator (integrates all systems)
│   ├── faction_system.py           # Faction AI with memory/gossip
│   ├── npc_intelligence.py         # Individual NPC AI + A* pathfinding
│   ├── heat_system.py              # GTA wanted stars + reality break
│   ├── stealth_system.py           # Vision cones, noise propagation
│   └── prop_system.py              # Interactive props
├── data/
│   ├── mall_map.json
│   ├── entities.json
│   ├── artifacts.json
│   └── stores.json
├── test_integrated_systems.py      # Comprehensive test (Tiers 1-3)
├── test_tier4_tier5.py             # Weird bread test (Tiers 4-5)
└── README.md
```

**Lines of Code:**
- `dialogue_system.py`: 338 lines
- `reality_glitch_system.py`: 346 lines
- `stealth_feedback.py`: 194 lines
- `toddler_system.py`: 366 lines
- `renderer_strain_system.py`: 402 lines
- `mall_simulation.py`: 536 lines (with Tier 4 & 5 integrations)
- **Total new code (Tiers 1-5): ~2,182 lines**

---

## 🧪 TESTING

**Run the comprehensive tests:**

**Tiers 1-3 (Core Systems):**
```bash
cd v2-immersive-sim
python3 test_integrated_systems.py
```

**Tiers 4-5 (Weird Bread):**
```bash
cd v2-immersive-sim
python3 test_tier4_tier5.py
```

**What the tests demonstrate:**

**Tier 1-3 Test:**
- Dialogue escalation across all heat levels
- Micro-glitch spawn rates and types
- Stealth feedback alert symbols and noise ripples
- Integrated scenario: player escalation from calm to reality break

**Tier 4-5 Test:**
- Toddler autonomous wandering (moved 26.7 tiles in 30 seconds)
- Heat/glitch amplification near toddler (2-3x multipliers)
- Toddler visibility scaling with heat (invisible → ☺)
- Renderer strain escalation (stable → critical)
- Fake FPS degradation (60 → 24 FPS)
- Error message spawning (76 concurrent errors at Heat 5)
- Frame drop simulation

**Test output shows:**
- ✅ All dialogue tiers working
- ✅ Glitch frequency scaling correctly (0% → 100%)
- ✅ Alert symbols triggering based on awareness
- ✅ Noise ripples creating and expanding
- ✅ Toddler wandering and amplifying reality breaks
- ✅ Renderer visibly struggling under AAA load
- ✅ All 5 tiers integrated in mall_simulation.py

---

### **Tier 4: Toddler System** ✅

**File:** `toddler_system.py` (366 lines)

The invisible entity outside the simulation. The SOURCE of all reality breaks.

**What It Is:**
- An autonomous entity that exists outside the simulation rules
- Wanders the mall invisible to the player (most of the time)
- Uses the AAA engine as a prybar to escape the Wolf3D prison
- Wherever the toddler goes, reality becomes unstable

**Behaviors:**

| Behavior | Heat Range | Description |
|----------|-----------|-------------|
| Wandering | 0-3 | Random exploration, mostly hidden |
| Following Player | 2-4 | Curious about the player |
| Attracted to Chaos | 3-4.5 | Moves toward high heat areas |
| Breaking Reality | 4.5-5 | Actively destabilizing simulation |
| Hiding | Any | Stationary, watching |

**Reality Distortion Field:**
- **Radius:** 15 tiles around toddler
- **Heat Amplification:** 2x heat buildup rate when player is near toddler
- **Glitch Amplification:** 3x glitch spawn rate when near toddler
- **Reality Strain:** Builds up to 1.0 based on heat and behavior

**Visibility Progression:**

| Heat | Visibility | Effect |
|------|-----------|--------|
| < 3.0 | 0.0 | Completely invisible |
| 3.0-4.0 | 0.05 | Barely visible flickers (·) |
| 4.0-4.5 | 0.2 | Occasional visibility |
| 4.5+ | 0.5 | Frequently visible (☺) |

**Test Results:**
```
✓ Toddler moved 26.7 tiles over 30 seconds (autonomous wandering)
✓ Heat multiplier: 2.90x at close range
✓ Glitch multiplier: 3.86x at close range
✓ Reality strain: 0.70 → 1.00 at Heat 5
✓ Visible at Heat 5 with ☺ symbol
```

**The Narrative:**
The toddler is NOT a game character. It's an entity using the modern game engine to pry open the Wolf3D facade. At low heat, it's completely invisible - just causing inexplicable glitches. At Heat 5, the mask fails enough that you can SEE it. The toddler is the reason everything breaks down.

---

### **Tier 5: Renderer Strain System** ✅

**File:** `renderer_strain_system.py` (402 lines)

The Wolf3D raycaster visibly failing under AAA AI load.

**The Lie:**
- Wolf3D was built for 20 sprites max
- Simple AI (patrol, shoot, die)
- 320x200 resolution

**The Truth:**
- 29+ AI agents with GOAP
- A* pathfinding for every NPC
- Faction systems with memory
- Vision cones and stealth calculations
- Heat system tracking thousands of events

**Strain Calculation:**
```python
base_strain = (npc_count - 20) / 30.0  # Strain starts at 20 NPCs
heat_strain = current_heat / 5.0
toddler_multiplier = 1.0 + (toddler_strain * 2.0)
total_strain = (npc_strain * 0.4 + heat_strain * 0.6) * toddler_multiplier
```

**Strain Levels:**

| Level | Strain Value | Effects |
|-------|-------------|---------|
| Stable | < 0.2 | 60 FPS, no errors |
| Minor | 0.2-0.5 | 55-60 FPS, rare warnings |
| Moderate | 0.5-0.8 | 45-58 FPS, frequent warnings |
| Heavy | 0.8-1.2 | 30-50 FPS, errors + warnings |
| Critical | 1.2+ | 15-35 FPS, constant critical errors |

**Error Messages (24 total):**

Warnings:
- `[WARN] Raycaster: Too many active sprites (limit: 20, current: 29)`
- `[WARN] Wolf3D renderer not designed for 29 concurrent agents`
- `[WARN] Vision cone calculations exceeding frame time budget`

Errors:
- `[ERROR] Buffer underrun detected in sprite renderer`
- `[ERROR] Wolf3D mode incompatible with modern AI load`
- `[ERROR] Failed to maintain 60 FPS target (actual: 24)`

Critical:
- `[CRITICAL] Fallback renderer unavailable`
- `[CRITICAL] Wolf3D raycaster cannot handle AAA AI systems`
- `[CRITICAL] SIMULATION INTEGRITY COMPROMISED`

**Fake FPS Degradation:**

| Strain | FPS Range | Visible Effect |
|--------|----------|---------------|
| < 0.2 | 60 | Perfect performance |
| 0.2-0.5 | 55-60 | Occasional dips |
| 0.5-0.8 | 45-58 | Frequent dips |
| 0.8-1.2 | 30-50 | Significant drops |
| 1.2+ | 15-35 | Severe degradation |

**Frame Drop Simulation:**
- At Heavy/Critical strain, fake "stutters" occur
- Duration: 0.05-0.5 seconds
- Visual representation of render thread struggling
- Player sees the game visibly choking

**Test Results:**
```
Strain Level: CRITICAL
Cumulative Strain: 2.00
Fake FPS: 24 (target: 60)
Active Errors: 76
Frame Drops: Active (intensity: 1.00)

Sample Errors:
[CRITICAL] Wolf3D raycaster cannot handle AAA AI systems
[CRITICAL] Renderer strain at maximum capacity
[CRITICAL] Fallback renderer unavailable
[ERROR] AI pathfinding: Exceeded maximum iterations
```

**The Meta Joke:**
The game is LYING about performance to maintain the retro aesthetic. It could run at 60 FPS, but it PRETENDS to struggle because the narrative is "Wolf3D renderer trying to contain AAA AI". At Heat 5, it stops lying - you see 76 error messages and 24 FPS because the mask has shattered.

---

## 🚧 NOT YET IMPLEMENTED

### **Rendering Integration** (Not Built)
- Wolf3D raycaster renderer
- ANSI 256-color output
- Terminal art display
- Visual integration of all feedback systems

---

## 🎯 DESIGN PRINCIPLES IMPLEMENTED

✅ **The Slipping Mask Philosophy**
- Mask slips slowly (Heat 3-4 cracks)
- Brain reveals itself early (sophisticated dialogue at Heat 2)
- Heat 5 confirms everything (full exposure)

✅ **No Weapons - No Combat**
- All "combat" dialogue is AI exposing the mismatch
- Guards have aggression parameters but only escort player out
- The horror: AI configured for GTA but mechanics are "mall ban"

✅ **AAA AI Under Retro Mask**
- Faction systems with memory and gossip
- A* pathfinding with GOAP
- Vision cones and stealth mechanics
- All hidden under Wolf3D raycaster

✅ **Minimal UI - Maximum Dissonance**
- No modern overlays
- Just ASCII symbols: ! ? ~
- The sophistication is in the behavior, not the graphics

---

## 📊 WHAT THE PLAYER EXPERIENCES

**First 5 Minutes:**
"Huh, retro Wolf3D mall game. Kind of charming."

**10 Minutes In:**
"Wait, why is this NPC talking about their shift ending at 5pm?"
"Why does a security guard have patrol routes?"
"Why does the FPS keep dipping? There's barely anything on screen..."

**15 Minutes (Heat 3):**
"Did I just see a pathfinding line for a frame?"
"Why did that NPC's name glitch to AI_AGENT_047?"
"I keep feeling like something's... watching me? But there's nothing there."

**20 Minutes (Heat 4):**
"NPCs are saying 'Pathfinding to waypoint 23, 45'..."
"I'm seeing wireframes... coordinates overlays..."
"The game is showing error messages: 'TOO MANY AI AGENTS FOR RAYCAST RENDERER'"
"FPS counter is dropping... 45... 35... but why??"
"This isn't a simple retro game."

**25 Minutes (Heat 4.5):**
"Wait... I just saw a toddler. For like a frame. WHAT?"
"The error messages won't stop: 'BUFFER UNDERRUN' 'FALLBACK RENDERER UNAVAILABLE'"
"The game is VISIBLY struggling. But it's just sprites!"

**Heat 5 (Reality Break):**
"OH MY GOD THERE'S A TODDLER JUST STANDING THERE"
"The FPS is 24. There are 76 ERROR MESSAGES on screen."
"NPCs: 'THIS ISN'T A MALL. THIS IS A SIMULATION.'"
"THE TODDLER WAS THE SOURCE THE WHOLE TIME"
"IT WAS AAA AI THE WHOLE TIME"
"The Wolf3D renderer was ALWAYS a lie - it was NEVER capable of this"
"A toddler used a 2025 game engine as a prybar to escape a 1993 prison"
"This was a modern immersive sim pretending to be retro AND FAILING AT IT"

---

## 🏆 SUCCESS CRITERIA MET

**Core Systems (Tiers 1-3):**
✅ NPCs discuss schedules like Skyrim NPCs
✅ Wolf3D sprites have Far Cry 6 patrol AI
✅ Mask cracks before it breaks (gradual reveal)
✅ Zero weapons (Dad's AMEX is most dangerous item)
✅ ANSI-only feedback (no modern UI)
✅ Dialogue escalates to full AI confession
✅ Micro-glitches build suspicion

**Weird Bread (Tiers 4-5):**
✅ Invisible entity (toddler) as reality catalyst
✅ Toddler amplifies heat and glitches near player
✅ Toddler becomes visible at Heat 5 (source revealed)
✅ Renderer visibly struggles under AAA load
✅ Fake performance degradation (60 → 24 FPS)
✅ Error messages expose the lie (76 concurrent errors)
✅ Meta narrative: toddler using engine as prybar to escape

**Integration:**
✅ All 5 tiers integrated and tested
✅ Systems interact emergently (toddler → renderer strain → glitches → dialogue)
✅ Complete player experience arc from "charming retro" to "existential horror"

---

## 🎭 THE META JOKE

**The entire point:**
- v1: "Here's a retro game"
- v2: "Here's a modern game PRETENDING to be retro that FAILS at pretending when chaos peaks"

The AI has always been this sophisticated. The Wolf3D renderer was always struggling to contain it. At Heat 5, the 50-cent mask shatters and you see the AAA engine underneath.

**It's not a bug. It's the entire point.**

The toddler is the final twist: An entity OUTSIDE the simulation using the modern engine to break free. The renderer strain is proof - Wolf3D was never capable of this. The player discovers the source of all reality breaks isn't a bug or corruption. It's a toddler with a prybar.

---

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ALL TIERS COMPLETE & OPERATIONAL (1-5)                     ║
║                                                              ║
║  Tier 1: The dialogue leaks (NPCs talk about shifts)        ║
║  Tier 2: The mask cracks (1-frame pathfinding flickers)     ║
║  Tier 3: Stealth in ASCII (Metal Gear in terminal art)      ║
║  Tier 4: The toddler appears (invisible catalyst revealed)  ║
║  Tier 5: The renderer fails (24 FPS, 76 errors)             ║
║                                                              ║
║  The cognitive dissonance is complete.                       ║
║  The existential dread is operational.                       ║
║                                                              ║
║  Welcome to GLITCHDEX MALL V2.                              ║
║  A 2025 AAA game wearing a 1993 Halloween mask.             ║
║  The toddler broke it with an engine prybar.                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
