# CRYSTALIZED KNOWLEDGE VECTOR ENGINE
## GLITCHDEX MALL: Complete Development Legacy (v1 → v8)

**Document Purpose:** Comprehensive development history showing the evolution of GLITCHDEX MALL from initial concept to current canonical implementation.

**Date Created:** 2025-12-05
**Repository:** GLITCHDEXMALLv7
**Project Status:** v7 Canonical (Stable) | v8 Lab (Active Experiments)

---

## EXECUTIVE SUMMARY

GLITCHDEX MALL represents an unprecedented evolution in game development, progressing from a simple Wolf3D-style raycaster to a sophisticated AI-driven, evidence-based architectural reconstruction of Eastland Mall (Tulsa, OK, 1981-2011). This document chronicles eight major versions, each building upon and transforming the previous iteration.

**Key Evolution Path:**
- **v1**: Wolf3D raycaster mall crawler (complete game)
- **v2**: AAA immersive sim with modern AI hiding under retro graphics
- **v3**: Pygame graphical implementation of v2's systems
- **v4**: Cloud-driven semantic world architecture
- **v5**: Evidence-based CRD (Classification Reference Document) reconstruction
- **v6**: AI-native development placeholder
- **v7**: Integration of v5 evidence + v6 systems (CANONICAL)
- **v8**: Active lab branch for experimental features (WORKING)

---

## TABLE OF CONTENTS

1. [Version Chronology](#version-chronology)
2. [v1-doofenstein: The Original](#v1-doofenstein-the-original)
3. [v2-immersive-sim: The Hidden AAA Engine](#v2-immersive-sim-the-hidden-aaa-engine)
4. [v3-eastland: Graphical Realization](#v3-eastland-graphical-realization)
5. [v4-renderist: Cloud-Driven World](#v4-renderist-cloud-driven-world)
6. [v5-eastland: CRD Reconstruction](#v5-eastland-crd-reconstruction)
7. [v6-nextgen: AI-Native Development](#v6-nextgen-ai-native-development)
8. [v7-nextgen: Integration Build (CANONICAL)](#v7-nextgen-integration-build-canonical)
9. [v8-nextgen: Lab Branch (ACTIVE)](#v8-nextgen-lab-branch-active)
10. [Architectural Philosophy Evolution](#architectural-philosophy-evolution)
11. [Technical Achievements Timeline](#technical-achievements-timeline)
12. [Repository Restructures](#repository-restructures)
13. [Development Principles](#development-principles)

---

## VERSION CHRONOLOGY

### Timeline Overview

| Version | Name | Era | Status | Key Innovation |
|---------|------|-----|--------|----------------|
| **v1** | DOOFENSTEIN 3D | Early Development | ✅ Complete & Playable | Wolf3D raycaster, toddler presence system |
| **v2** | Immersive Sim | Advanced Architecture | ✅ Playable (Text) | AAA AI systems, reality-breaking heat |
| **v3** | Eastland Pygame | Graphical Realization | ✅ Complete & Playable | Full graphical rendering + all v2 systems |
| **v4** | Renderist Mall OS | Cloud Architecture | ✅ Phase 1 Complete | Cloud-driven semantic spaces |
| **v5** | CRD Reconstruction | Evidence Phase | ✅ V1 Complete | Photo-based architectural archaeology |
| **v6** | AI-Native | Restructure | 🔄 Placeholder | Clean slate for AI-assisted development |
| **v7** | Integration Build | Canonical | ⭐ CANONICAL | v5 evidence + v6 systems = Doom-alike |
| **v8** | Lab Branch | Active Development | 🧪 WORKING | Experimental features, LLM integration |

---

## v1-doofenstein: The Original

**Version:** 1.0
**Status:** ✅ Complete & Playable
**Launch:** `cd v1-doofenstein && python src/main.py`
**Shareware Program:** #387

### Vision
A gloriously broken Wolfenstein 3D-style raycaster set in a liminal 1988 shopping mall. The weapon is a credit card. The toddler is never visible—only felt.

### Core Features

#### Graphics Technology
- **Textured walls** with 8x8 tiled patterns
- **Floor and ceiling rendering** with depth shading
- **ANSI 256-color VGA palette** for authentic early-3D visuals
- **Sprite-based items/NPCs** rendered as billboards in 3D space
- **Visual corruption effects** that intensify with toddler presence

#### Gameplay Systems
- **Tile-based movement** - Simple collision detection
- **Artifact discovery** - 14 cursed items scattered through mall
- **NPC interactions** - 6 unique characters with distinct behaviors
- **Toddler presence system** - 3 escalating stages of environmental horror
- **Session-based gameplay** - Must physically escape through entrance to quit

#### The Toddler Mechanic
The core innovation: an invisible entity whose presence intensifies over time.

**Stage 1 (Early):** Distant cries, rare shadow glimpses
**Stage 2 (Mid):** Frequent wails, shadows in corners
**Stage 3 (Late):** Constant screaming, chaos, tremors, reality glitches

### Mall Layout (v1)
- Entrance/Exit
- BORED (skateshop & tee emporium)
- Milo's Discount Optics
- Food court (sparse crowd)
- Anchor store (dying retail)
- Service corridors, restrooms, kiosks, escalators

### Key Characters
- **Milo** - Overqualified optician, keeper of artifact lore
- **BORED** - Apathetic skateshop kid
- **R0-MBA** - Silent vacuum observer
- **The Mall Cop** - Simple patrol routes
- **Generic Shoppers** - 1988 Nintendo-sparse crowds

### Design Philosophy
> "No physics engine. No objectives. Dungeon crawler aesthetic. Jank is a feature. One vision, singular."

### Technical Stack
- Pure Python 3.8+ stdlib (no external dependencies)
- Wolf3D raycaster implementation
- ANSI terminal rendering
- Tile-based collision system

### Achievements
- ✅ Complete vertical slice
- ✅ Playable end-to-end
- ✅ Windows executable build support
- ✅ Cursed shareware CD launcher
- ✅ Session logging and transcript generation

---

## v2-immersive-sim: The Hidden AAA Engine

**Version:** 2.0
**Status:** ✅ Playable (Text renderer)
**Launch:** `cd v2-immersive-sim && python src/main.py`
**Shareware Program:** #388

### The Meta Concept

> "A full modern immersive sim wearing a cheap Wolf3D Halloween mask that starts to slip as the toddler and glitches escalate."

What the player sees: Retro Wolf3D mall crawler in ANSI terminal art
What's actually running: Cutting-edge 2025 game AI and systems

At Heat Level 5, the simulation BREAKS. The Wolf3D facade can't handle the chaos. Modern rendering bleeds through.

### Architecture Revolution

**Separation of Simulation and Presentation**

```
PRESENTATION LAYER (Wolf3D Facade - The 50¢ Mask)
├─ wolf_renderer.py    - Raycaster with textured walls
├─ ANSI 256-color      - VGA palette aesthetic
└─ reality_glitch.py   - Cracks in the facade
                            ↑
                            │
                Rendering hints & NPC positions
                            │
SIMULATION LAYER (2025 AAA Engine - The Real Deal)
├─ mall_simulation.py     - Main orchestrator
├─ faction_system.py      - Complex faction AI
├─ npc_intelligence.py    - Individual NPC AI + A*
├─ stealth_system.py      - Vision cones, noise, alerts
├─ heat_system.py         - GTA wanted stars + reality breaks
└─ prop_system.py         - Interactive objects with physics
```

### System Breakdown

#### 1. Faction System (MAXIMUM Complexity)
- **6 Factions:** Security, Workers, Shoppers, Teens, Management, Janitors
- **Collective Memory:** Factions remember and share information via gossip
- **Dynamic Relationships:** Evolve based on player behavior
- **Schedules:** Time-based behavior patterns
- **Coordinated Responses:** Allied factions work together at high heat

**Emergent Example:**
*Player attacks security → Security hostile → Gossip to Management → Management hostile → Coordinated lockdown*

#### 2. NPC Intelligence (MAXIMUM Complexity)
Each NPC is a sophisticated AI agent with:
- **A* Pathfinding** - Real pathfinding with dynamic obstacle avoidance
- **Personal Memory** - Remembers seeing player, suspicious events
- **GOAP (Goal-Oriented Action Planning)** - NPCs select goals dynamically
- **Behavior States** - Idle, Patrolling, Investigating, Pursuing, Fleeing
- **Personality** - Aggression, bravery, curiosity, sociability
- **Individual Schedules** - Daily routines

#### 3. Stealth System (BASIC)
- **Vision Cones** - NPCs have field-of-view with angle and range
- **Line-of-Sight** - Raycasting to check visibility
- **Noise Propagation** - Actions create noise with radius and falloff
- **Alert States** - Unalert → Suspicious → Searching → Alerted

#### 4. Heat System (REALITY-BREAKING)
GTA-style wanted stars with escalating reality collapse:

| Heat | Effect | Facade Status |
|------|--------|---------------|
| ★☆☆☆☆ | Security watches | Intact |
| ★★☆☆☆ | Active pursuit | Stable |
| ★★★☆☆ | Lockdown procedures | Minor cracks |
| ★★★★☆ | Full lockdown | Glitching |
| ★★★★★ | **REALITY BREAK** | **MASK SHATTERED** |

**At Heat 5:**
```
┌─────────────────────────────────────────────────────────┐
│ [CRITICAL] SIMULATION INTEGRITY COMPROMISED             │
│                                                         │
│ ENGINE: Unreal Engine 5.3.2 / Unity 2023.2             │
│ AI_AGENTS: 87 active                                   │
│ PATHFINDING: Recast/Detour Nav Mesh [VISIBLE]         │
│                                                         │
│ [ERROR] Cannot maintain retro facade                   │
│ [WARNING] Wolf3D mask: FAILING                        │
└─────────────────────────────────────────────────────────┘
```

Visual effects:
- Wireframe overlay (actual poly mesh)
- Photorealistic texture leaks
- AI pathfinding debug lines
- Vision cone visualization
- Nav mesh display
- Real-time profiler overlay

#### 5. Prop System (25+ Interactive Objects)
**Distraction Props:**
- Vending Machine - Creates noise, NPCs investigate
- Arcade Cabinet - Beeping distracts nearby NPCs

**Destructible Props:**
- Plant Pot - Throw for crash/distraction
- Glass Door - Break for loud shatter + alarm

**Security Props:**
- Security Camera - Hack to reduce heat
- Alarm Panel - Trigger for lockdown + massive heat

**Combo Interactions:**
- Trash Can + Lighter → Fire → Evacuation + max heat
- Vending Machine + Kick → Loud noise + loot + heat

### The Philosophy

> "What if we built a AAA immersive sim but forced ourselves to render it as Wolf3D?"

This project is about:
- **Emergence over scripting** - Systems interact to create stories
- **Depth over graphics** - Sophisticated AI in ASCII
- **Meta-commentary** - The game itself is about facades breaking
- **No compromises** - Full modern systems, full retro aesthetic

### Technical Achievements
- Production-quality A* pathfinding with caching
- GOAP-lite + FSM for NPC behavior
- Memory + Gossip propagation for factions
- Industry-standard stealth mechanics
- Meta reality-breaking heat system
- Component-based prop interactions

---

## v3-eastland: Graphical Realization

**Version:** 3.0
**Status:** ✅ Complete & Playable
**Launch:** `cd v3-eastland && python src/main_pygame.py`
**Shareware Program:** #389

### Vision
The culmination of v1's raycaster and v2's AI systems—a full graphical Pygame renderer with all simulation systems online.

### Key Features
- **Pygame Raycaster** - Full graphical 3D rendering
- **All V2 AI Systems** - Factions, A* pathfinding, GOAP, stealth, heat
- **Pong Mini-game** - Arcade cabinet interaction
- **Dual Entry Points** - Text (main.py) or Graphical (main_pygame.py)

### What Changed from v2
v2 had text rendering only. v3 brings visual fidelity:
- Textured wall rendering in Pygame
- Sprite rendering for NPCs and items
- Floor/ceiling texture mapping
- Visual feedback for all v2 systems

### Status
✅ All systems working together
✅ Complete gameplay experience
✅ Best version for playing the fully realized game

---

## v4-renderist: Cloud-Driven World

**Version:** 4.0.1-alpha
**Status:** ✅ Phase 1 Complete
**Launch:** `cd v4-renderist && python src/main.py`
**Shareware Program:** #390

### The Paradigm Shift

V4 represents a fundamental architectural shift from **tile-based maps** to **Cloud-driven semantic spaces**.

> "Canon emerges from resonance and repetition, not ego."

### Core Philosophy
- The Mall is a Cloud-driven world, not a static map
- 13 Anchor NPCs are the only persistent identities
- All Customers are ambient noise (non-canon)
- Sora-style clips are BLEED EVENTS that alter world tone

### Key Systems

#### 1. The Cloud (Global State)
Abstract world data driving all behavior:
- **Pressure:** 0-100 scale
- **Moods:** Calm → Uneasy → Strained → Critical
- **Bleed Tiers:** 3 levels of reality distortion

#### 2. 13 Anchor NPCs
Persistent entities with Line-12 spines (character identity cores):
- Each has contradiction threshold
- Break "never" rules when Cloud reaches threshold
- Example: Mall Cop abandons post at Cloud 75

**Key Contradictions:**
- **Mall Cop** (75): Abandons post
- **BORED** (75): Warns player about something specific
- **Barista** (80): Forgets what drink they're making
- **Bookwoman** (80): Recommends a book she hasn't read
- **Toddler** (90): Speaks a single word

#### 3. Swarm System
Ambient crowd with population curves:
- Non-persistent entities
- Confirming-only Cloud feedback (max 5% influence)
- Population fluctuates with Cloud mood

#### 4. 60fps Loop with Interpolation
- Cloud updates every 10 frames (batched)
- NPCs/Swarm read interpolated values for smooth behavior
- No jarring state transitions

#### 5. Zone Cooldown Logic
- Contradiction cascade prevention
- 30-second cooldown per zone
- Prevents spam triggers

### Locked Constants
```python
CLOUD_UPDATE_INTERVAL = 10           # frames
ZONE_CONTRADICTION_COOLDOWN = 30.0   # seconds
MAX_SWARM_CONTRIBUTION = 0.05        # 5% cap
BLEED_WINDDOWN_TIME = 7.5            # seconds
```

### Phase 1 Achievements
✅ Cloud state management
✅ 13 Anchor NPCs with spines
✅ Swarm population system
✅ 60fps loop with interpolation
✅ Contradiction cascade logic

### Phase 2 Roadmap (Future)
- Bleed Events system
- AO3 Log generation (canon emergence through player discovery)
- Probabilistic adjacency
- SORA clip integration
- Persistence across sessions

---

## v5-eastland: CRD Reconstruction

**Version:** 5.0-alpha
**Status:** ✅ V1 Complete - Awaiting Fidelity Passes
**Launch:** Documentation project (no executable)
**Shareware Program:** #391

### The Archaeological Approach

V5 represents a **methodical, evidence-based reconstruction** of Eastland Mall using the Classification Reference Document (CRD) workflow.

### Critical Context

⚠️ **SCALE WARNING:** This is a **1,000,000+ sq ft megastructure**, not a conventional mall.

**Key Facts:**
- KKT Architects pioneered tensile sail technology in early 1980s
- Scale: "Space station with a parking lot"
- Mast height: 60-80+ feet (not 35 feet)
- Atrium diameter: 150-200+ feet
- This is architectural archaeology, not game map creation

### CRD Workflow (7 Steps)

#### V1 Baseline: COMPLETE ✅

| Step | Document | Status | Progress |
|------|----------|--------|----------|
| 1 | Photo Classification | ✅ COMPLETE | 143/143 photos |
| 2 | Feature Extraction | ✅ COMPLETE | 11 features |
| 3 | Zone Graph | ✅ COMPLETE | 9 zones |
| 4 | Stereo Pairs | ⏸️ IDENTIFIED | 4 pairs |
| 5 | Measurement Sheet | ✅ COMPLETE | 15 measurements |
| 6 | Map Corrections | ✅ COMPLETE | 12 corrections |
| 7 | Map Proposal | ✅ COMPLETE | Zone-based map |

### Measurable Atomic Units

V5 uses these features as "rulers" for accurate scaling:

| Feature | Dimensions | Use Case |
|---------|------------|----------|
| Glass Block | 6×6" or 8×8" | Atrium wall radius |
| Coca-Cola Vending Machine | 39" × 72" | Global scale calibration |
| Exit Sign | 8.75" × 10.5" | Corridor scaling |
| Escalator Step | 8" rise | Z-level height differential |
| Ceiling Tile | 2' × 4' | Interior scale |
| Column Diameter | ~18-24" | Grid spacing |

### Photo Evidence Base

**Total Photos:** 153 (initially in `/eastlandpics/`)

**Key Reference Photos:**
- **Fountain:** 453127566, 453126954, 453127262, 453127434
- **Tensile Roof:** 453124750, 64360891, 453125654
- **Escalators:** 3085976410, 3085979988
- **Food Court:** 453143417, 64360891
- **Coca-Cola Store:** 3085977904, 3085977656

### V1 Deliverables
- 143 photos classified with PRIMARY/FEATURE/ZONE assignments
- 15 measurements extracted with confidence levels
- 12 corrections synthesized from measurements
- Complete zone-based map proposal with measured geometry
- Full photo traceability and contradiction tracking

### Contradiction Tracking Innovation

Unlike v3 (which resolved conflicts immediately), v5 **documents contradictions as historical layers**:
- Corridor width mismatches between eras
- Food court angles changed over renovations
- Tent fabric replacement vs. original
- Anchor store footprint drift

**Contradictions are NOT errors—they are timeline variance.**

### V2+ Fidelity Passes: PENDING

**Goal:** Raise confidence levels on LOW/MEDIUM measurements.

**Priority Targets:**
- Mast height: 35' (LOW) → 60-80+' (MEDIUM-HIGH)
- Atrium diameter: 60-80' (LOW) → 150-200+' (MEDIUM-HIGH)
- Pit depth: 8' (HIGH) → Verify or revise to 15-20+'

---

## v6-nextgen: AI-Native Development

**Version:** 6.0-placeholder
**Status:** 🔄 Placeholder
**Launch:** Placeholder only
**Shareware Program:** #392

### The Clean Slate

V6 was created as a **white box** for AI-assisted development, representing a complete architectural reset.

### Repository Restructure

The v6 introduction triggered a major repository reorganization:

**Old Structure:**
```
GLITCHDEXMALLv7/
├── v1-doofenstein/
├── v2-immersive-sim/
├── v3-eastland/
├── v4-renderist/
└── v5-eastland/
```

**New Structure (After AI-Native Restructure):**
```
GLITCHDEXMALLv7/
├── v6-nextgen/           ⭐ CANONICAL (at the time)
│   ├── canon/            # Entity definitions
│   ├── docs/             # Documentation
│   ├── src/              # White box skeleton
│   ├── data/             # Game data
│   └── assets/           # Photos, maps, media
│
├── ai/                   🤖 AI-Native Tooling
│   ├── spynt/            # Character spine schemas
│   ├── sora/             # Video generation templates
│   ├── mallOS/           # Simulation state management
│   ├── renderist/        # Lore and metaphysics
│   └── pipelines/        # Automation scripts
│
├── archive/              📚 Historical Context (v1-v5)
│   ├── v1-doofenstein/
│   ├── v2-immersive-sim/
│   ├── v3-eastland/
│   ├── v4-renderist/
│   └── v5-eastland/
│
└── docs/                 📖 Project Documentation
    ├── AI_INTENT.md
    ├── AI_MEMORY.md
    └── VERSION_MATRIX.md
```

### AI-Native Tooling (/ai/)

#### spynt/ - Character Spine System
- JSON-based NPC identity schemas
- Spine = core memory + contradictions + behavior
- Integration with simulation

#### sora/ - Video Generation Logic
- Prompt templates for Sora/Runway
- Scene composition rules
- Anchor NPC placement
- Shot transition logic

#### mallOS/ - Simulation Orchestration
- Cloud state management (from v4)
- Zone graph and activation logic
- Bleed rules and contradiction cascade
- 60fps tick system

#### renderist/ - Metaphysics & Lore
- Codex fragments
- Canon emergence principles
- Architectural philosophy
- Timeline documentation

#### pipelines/ - Automation & CI/CD
- Photo classification scripts
- Schema validation
- GitHub Actions workflows

### AI-Native Principles

1. **Reconstruction > Hallucination** - Base on photo evidence
2. **Metrology First** - Never hallucinate dimensions
3. **CRD Workflow** - Classify, reference, document
4. **Version Awareness** - v1-v5 are historical (frozen)
5. **Structured Schemas** - Use /ai/ tools for all entities

### Status
V6 served as a placeholder and organizational framework. The actual implementation came in v7.

---

## v7-nextgen: Integration Build (CANONICAL)

**Version:** 7.0.0-alpha
**Status:** ⭐ CANONICAL (Stable)
**Launch:** Integration demo available
**Philosophy:** v5 Evidence + v6 Systems = v7 Mall Dungeon Doom-Alike

### The Integration

V7 represents the **merger of two parallel development paths:**

**From V5 (CRD Reconstruction):**
- ✅ Scale corrections (space station scale: 1M+ sq ft, 175' atrium, 70' masts)
- ✅ Measured geometry (15 verified measurements)
- ✅ Architectural context (KKT design intent)
- ✅ Zone graph (9 structural zones)
- ✅ New entities (Coca-Cola store, FOOD COURT neon sign)
- ✅ Timeline contradictions (multi-era variance preserved)

**From V6 (Simulation Systems):**
- ✅ QBIT Engine (entity scoring: power, charisma, resonance)
- ✅ Cloud System (global mood states with zone microstates)
- ✅ NPC State Machines (behavioral AI with contradictions)
- ✅ Bridge Server (UE5 integration layer: HTTP/JSON)
- ✅ Entity Canon (structured JSON definitions)
- ✅ Adjacency System (QBIT-weighted zone transitions)

**NEW in V7:**
- ✅ Measurements Loader (single source of truth for dimensions)
- ✅ Voxel Builder (Doom-alike construction from CRD blueprints)
- ✅ Timeline System (multi-era support: 1981/1995/2005/2011)
- ✅ LLM DM Guide (Discord hooks narration system)
- ✅ Z7 Placeholder (subterranean zone, exterior access only)

### Voxel Doom-Alike Vision

**The Concept:** 3 credit cards as weapons in a 1,000,000+ sq ft mall dungeon.

**Gameplay:**
- Fast-paced voxel combat in cathedral-scale spaces
- 175-foot atrium gives massive room for maneuver
- Vertical gameplay (60-80 foot ceilings, 8-foot pit descents)
- Credit cards as keys/weapons in consumer nightmare

**Voxel Construction Workflow:**
```bash
# Build voxel mesh from CRD measurements
python src/voxel_builder.py
# Generates: v7_mall_doom.json
```

### Multi-Era Timeline

**Four Eras (All Canon):**
- **1981** - Opening (pristine, optimistic)
- **1995** - Peak (bustling, thriving) ⭐ Starting Era
- **2005** - Decline (vacant, flickering)
- **2011** - Closure (abandoned, temporal horror)

**Era Triggers:** Cloud pressure, player discoveries, NPC interactions

**Critical Design Principle:** Contradictions between eras are CANON, not errors.

### Scale Corrections from V5

**CRITICAL: Space Station Scale**
- Atrium: 175' diameter (2.5x correction from v6)
- Masts: 70' tall (2.0x correction from v6)
- Design philosophy: "Space station with a parking lot"

**HIGH Confidence Measurements:**
- Food court pit: 8 feet
- Fountain tiers: 4 levels
- Tensile cables: 32 radial

All measurements linked to photo evidence in `data/measurements/crd_traceability.json`

### Status

**Version:** 7.0.0-alpha
**Status:** Integration Complete - Ready for Voxel Construction

**Everything but visuals: READY.**
**3 credit cards: LOADED.**
**Mall dungeon: AWAITS.**

---

## v8-nextgen: Lab Branch (ACTIVE)

**Version:** 8.0-lab
**Status:** 🧪 Active Experiments
**Branch Type:** Working/Lab (not canonical)
**Philosophy:** Experimental features and active development

### Relationship to v7

The main README clarifies:
- **v7-nextgen:** CANONICAL - Primary development path (stable)
- **v8-nextgen:** LAB - Active experiments/working branch

V8 is where experimental features are tested before potential integration into v7.

### V7 Integrated Demo - The Horror Stack

The most significant v8 achievement is the **V7 Integrated Demo**, which wires together:

**The Horror Stack:**
- **Toddler** → Cloud amplification
- **Cloud** → Mood/pressure system
- **Janitor** → LLM dialogue (triggers at Cloud 70+)
- **Leon** → game_state awareness (ready for narration)
- **Renderer** → Glitch/strain tracking

### The Integration Flow

```
PLAYER (stationary)
  ↓
TODDLER (wandering, manifesting at Cloud 70+)
  ↓ heat_multiplier (1.0-3.0x)
  ↓
CLOUD (0 → 70.8 in 66 seconds)
  ↓ mood: calm → uneasy → strained
  ↓
JANITOR (breaks rule at Cloud 70)
  ↓ triggers LLM dialogue
  ↓
LLM (Anthropic Claude 3.5 Haiku)
  ↓ JSON response
  ↓
DIALOGUE ("The arcade machines hum E-flat...")
  ↓
game_state (toddler + cloud + janitor + renderer)
  ↓
LEON (ready to narrate)
  ↓
RENDERER (glitch 1.0, strain 1.0)
```

### Key Systems Wired

#### 1. Toddler → Cloud Amplification
Every tick, toddler effects amplify Cloud pressure:
```python
base_delta = 0.5  # Passive gain
amplified_delta = base_delta * toddler_effects["heat_multiplier"]  # 1.0-3.0x
cloud.level += amplified_delta
```

Toddler generates:
- **heat_multiplier** (1.0-3.0x) - Cloud pressure amplification
- **glitch_multiplier** (1.0-4.0x) - Visual distortion
- **reality_strain** (0-1) - Environmental stress

#### 2. Janitor → LLM Dialogue
Trigger: `cloud.level >= 70` AND `janitor.in_forbidden_zone == True`

The system:
1. Builds Cloud-aware prompt with zone context
2. Calls LLM (mock or real Anthropic API)
3. Parses JSON response
4. Displays dialogue with emotional state and tags

Example output:
```
"The arcade machines... they're humming in E-flat. Same as
 the escalators. Same as the fountain pump. It's all
 connected."

[Emotional state: obsessed]
[touching arcade cabinet, listening intently]
Tags: arcade_machines, escalators, fountain, E-flat
```

#### 3. Leon → game_state Output
Complete game state exported every tick for narration:
```python
game_state = {
    "game_time": 66.0,
    "tick_count": 65,
    "player": {"position": (0, 0, 0), "zone": "Z1_CENTRAL_ATRIUM"},
    "cloud": {"level": 70.8, "mood": "strained", "pressure_trend": "rising"},
    "toddler": {
        "visible": 1.0,
        "distance": 107.0,
        "reality_strain": 1.0,
        "behavior": "wandering"
    },
    "janitor": {
        "zone": "FC-ARCADE",
        "in_forbidden_zone": True,
        "power": 1478,
        "threshold": 70.0
    },
    "renderer": {
        "glitch_intensity": 1.0,
        "reality_strain": 1.0
    }
}
```

#### 4. Renderer → Glitch/Strain Tracking
Visual feedback system ready for:
- Chromatic aberration
- Screen vignette
- Sprite jitter
- Color shifts
- Camera shake

### Mock vs Real LLM

**Mock LLM (Default):**
- No API key needed
- Returns canned responses based on context
- Good for testing integration
- Fast

**Real LLM (--with-llm flag):**
- Requires `ANTHROPIC_API_KEY`
- Uses Claude 3.5 Haiku
- Returns actual context-aware dialogue
- ~$0.001 per utterance

### Status

**The infrastructure is no longer theoretical. It's code. It's running. It's screaming.**

The v8 demo proves all systems can work together in a unified simulation loop.

---

## ARCHITECTURAL PHILOSOPHY EVOLUTION

### Phase 1: Monolithic (v1)
**Philosophy:** "Get it working"
- Integrated, monolithic design
- Direct coupling between systems
- Simple and effective for vertical slice

### Phase 2: Separation of Concerns (v2)
**Philosophy:** "Build it right"
- Simulation layer separated from presentation
- Modular systems with clear interfaces
- Demonstrates modern game architecture

### Phase 3: Semantic Spaces (v4)
**Philosophy:** "Canon emerges from resonance"
- Cloud-driven world, not tile-based
- Semantic adjacency over geometric positioning
- Reality as emergent property of NPC contradictions

### Phase 4: Evidence-Based (v5)
**Philosophy:** "Reconstruction > Hallucination"
- Photo-driven architectural archaeology
- Metrology constraints (escalator standards, civic scale)
- Contradiction tracking as timeline variance
- Every measurement traceable to source

### Phase 5: Integration (v7)
**Philosophy:** "Evidence + Systems = Experience"
- v5's measured reality + v6's simulation systems
- Multi-era timeline with canonical contradictions
- Voxel doom-alike construction from CRD blueprints
- LLM-driven narration aware of full game state

### Phase 6: Experimentation (v8)
**Philosophy:** "The infrastructure screams"
- Horror stack fully operational
- LLM integration with context awareness
- Toddler amplification proving system interconnection
- Lab for features before canonical integration

---

## TECHNICAL ACHIEVEMENTS TIMELINE

### v1 Achievements
- ✅ Wolf3D raycaster in Python
- ✅ ANSI 256-color rendering
- ✅ Toddler presence system (3 stages)
- ✅ Artifact discovery and lore
- ✅ Session-based gameplay loop
- ✅ Windows executable packaging

### v2 Achievements
- ✅ Production-quality A* pathfinding
- ✅ GOAP-lite NPC behavior system
- ✅ Faction AI with memory and gossip
- ✅ Vision cone stealth mechanics
- ✅ Reality-breaking heat system
- ✅ 25+ interactive props with systemic interactions
- ✅ Separation of simulation and presentation

### v3 Achievements
- ✅ Pygame graphical rendering
- ✅ Integration of all v2 systems with visuals
- ✅ Pong mini-game
- ✅ Dual entry points (text/graphical)

### v4 Achievements
- ✅ Cloud state management (0-100 pressure, 4 moods)
- ✅ 13 Anchor NPCs with contradiction thresholds
- ✅ Swarm population system
- ✅ 60fps loop with interpolation
- ✅ Zone cooldown logic
- ✅ LOCKED constants for consistency

### v5 Achievements
- ✅ CRD workflow (7 steps)
- ✅ 143 photos classified
- ✅ 11 measurable atomic units identified
- ✅ 9 structural zones mapped
- ✅ 15 measurements with confidence levels
- ✅ 12 map corrections synthesized
- ✅ Full photo traceability
- ✅ Contradiction tracking as timeline variance

### v6 Achievements
- ✅ Repository restructure (archive + ai/ + docs/)
- ✅ AI-native tooling (spynt, sora, mallOS, renderist, pipelines)
- ✅ White box skeleton for canonical development
- ✅ Comprehensive AI guidelines
- ✅ Asset consolidation (153 photos to v6/assets/)

### v7 Achievements
- ✅ Integration of v5 evidence + v6 systems
- ✅ Scale corrections (space station scale)
- ✅ Measurements loader (single source of truth)
- ✅ Voxel builder (CRD → Doom-alike)
- ✅ Timeline system (4 eras: 1981/1995/2005/2011)
- ✅ QBIT adjacency with zone transitions
- ✅ LLM DM Guide framework
- ✅ Z7 subterranean placeholder

### v8 Achievements
- ✅ V7 Integrated Demo (horror stack operational)
- ✅ Toddler → Cloud amplification
- ✅ Janitor LLM dialogue with context awareness
- ✅ game_state export for Leon narration
- ✅ Renderer glitch/strain tracking
- ✅ Mock and real LLM support
- ✅ Proof of full system integration

---

## REPOSITORY RESTRUCTURES

### Restructure 1: V6 Introduction (2025-11-21)

**Trigger:** Need for AI-native development framework

**Changes:**
- Created v6-nextgen/ directory skeleton
- Added GUI launcher (launcher_gui.py)
- Updated shareware programs to include v5, v6
- Created comprehensive launcher documentation

**Branch:** `claude/add-v6-restructure-01SbzdZqEvF5DyHP7hqdxjcC`

**Files Changed:** 214 files
**Additions:** 1,471 lines

### Restructure 2: AI-Native Restructure (2025-11-21)

**Trigger:** Move to AI-native development as part of GitHub AI-Native Development Cohort

**Major Changes:**

1. **Archive Creation** - v1-v5 moved to /archive/ (frozen, DO NOT MODIFY)
2. **AI Tooling** - Created /ai/ with 5 subsystems
3. **V6 White Box** - Expanded directory skeleton with comprehensive README
4. **Assets Consolidated** - 153 photos to v6-nextgen/assets/
5. **Documentation Updated** - Root README rewritten, AI guidelines added
6. **Launchers Updated** - Paths updated to point to archive/

**New Structure:**
```
GLITCHDEXMALLv7/
├── v6-nextgen/        ⭐ CANONICAL
├── ai/                🤖 AI-Native Tooling
├── archive/           📚 Historical Context (v1-v5)
├── docs/              📖 Project Documentation
└── .github/           AI agent guidelines
```

**Branch:** `claude/add-v6-restructure-01SbzdZqEvF5DyHP7hqdxjcC`

**Commits:**
- ab4e4e1: GUI launcher + v6 placeholder
- 3af2615: AI-native restructure (214 files)

### Restructure 3: V7 Integration (2025-11-28)

**Trigger:** Merge v5 evidence with v6 systems

**Changes:**
- v7-nextgen/ becomes CANONICAL
- v6-nextgen/ remains as reference
- Integration of CRD measurements with simulation systems
- Voxel builder implementation
- Timeline system for multi-era support

### Current Structure (2025-12-05)

```
GLITCHDEXMALLv7/
├── v7-nextgen/              ⭐ CANONICAL - Stable
├── v8-nextgen/              🧪 LAB - Active development
├── v1-doofenstein/          (archived reference)
├── v2-immersive-sim/        (archived reference)
├── v3-eastland/             (archived reference)
├── v4-renderist/            (archived reference)
├── v5-eastland/             (archived reference)
├── v6-nextgen/              (archived reference)
├── ai/                      🤖 AI-Native Tooling
├── docs/                    📖 Project Documentation
│   ├── AI_INTENT.md
│   ├── AI_MEMORY.md
│   └── CRYSTALIZED_KNOWLEDGE_VECTOR_ENGINE.MD  ← THIS DOCUMENT
└── README.md                Current project status
```

---

## DEVELOPMENT PRINCIPLES

### Core Tenets (Established v1-v2)

1. **No External Dependencies** (where possible)
   - Pure Python stdlib for core systems
   - No Unity, no Unreal, no Godot
   - Custom raycaster, custom AI, custom everything

2. **Jank is a Feature**
   - Broken 3D rendering enhances liminal quality
   - Texture warping creates unease
   - Eerie unfocused depth from 30KB games

3. **Systems Over Scripting**
   - Emergent behavior from interacting systems
   - Factions create stories through AI, not cutscenes
   - Props enable player creativity, not guided sequences

### Evidence-Based Design (Introduced v5)

4. **Reconstruction > Hallucination**
   - Base all work on photo evidence
   - Use CRD workflow for classification
   - Mark proxies and assumptions explicitly

5. **Metrology First**
   - Never hallucinate dimensions
   - Use measurable atomic units (glass blocks, escalators, vending machines)
   - Maintain civic scale (1M+ sq ft, 60-80ft masts, 150-200ft atrium)

6. **Contradiction Tracking**
   - Contradictions are timeline variance, not errors
   - Document all eras: 1981/1995/2005/2011
   - Multi-era canon is intentional

### AI-Native Development (Established v6-v8)

7. **Structured Schemas**
   - Use /ai/spynt/ for character spines
   - Use /ai/mallOS/ for simulation logic
   - Use /ai/sora/ for video generation
   - Use /ai/renderist/ for lore and metaphysics

8. **Version Awareness**
   - v1-v6 are historical (reference only)
   - v7 is canonical (stable)
   - v8 is lab (active experiments)
   - Archive for context, not code reuse

9. **Canon Emergence**
   - Canon emerges from resonance and repetition, not ego
   - Cloud-driven reality, not static maps
   - NPC contradictions reveal truth
   - Player discovery generates AO3 logs

### Integration Philosophy (v7-v8)

10. **Everything Connects**
    - Toddler amplifies Cloud
    - Cloud triggers NPC contradictions
    - NPCs speak via LLM with full context
    - Renderer reflects reality strain
    - Leon narrates with game_state awareness

11. **The Infrastructure Screams**
    - Systems must prove integration
    - Mock testing validates architecture
    - Real LLM testing validates content
    - Horror stack operational = success

---

## FUTURE DIRECTIONS

### Near-Term (v8 Lab Work)

- **Multi-NPC LLM Hooks** - Wife, Al-Gorithm dialogue systems
- **Player Input** - WASD movement in integrated demo
- **Zone Geometry** - Real zone detection vs. hardcoded
- **Leon Narration Loop** - Call LLM with game_state every N ticks
- **Render Output** - Visual effects using glitch_intensity and reality_strain

### Mid-Term (v7 Canonical Development)

- **Voxel Rendering** - Import v7_mall_doom.json into voxel engine
- **3 Credit Cards** - Implement weapon/key system
- **Multi-Era Switching** - Runtime transition between 1981/1995/2005/2011
- **QBIT Zone Disturbance** - Enable commented-out zone pressure system
- **UE5 Bridge** - Full integration with Unreal Engine 5

### Long-Term (Beyond v8)

- **v5 V2+ Fidelity Passes** - Raise measurement confidence with additional photos
- **Bleed Events (v4 Phase 2)** - SORA clip integration
- **AO3 Logs** - Canon emergence through player discovery
- **Probabilistic Adjacency** - Dynamic zone connections
- **Persistence** - Save Cloud state, NPC memories across sessions

---

## CONCLUSION

GLITCHDEX MALL represents an unprecedented journey in game development—from a simple Wolf3D homage to a sophisticated, evidence-based, AI-driven architectural reconstruction and simulation.

### The Evolution in Summary

**v1:** "Let's make a retro mall crawler"
**v2:** "Let's hide a modern immersive sim inside it"
**v3:** "Let's make it look like what it actually is"
**v4:** "Let's make the world semantic, not geometric"
**v5:** "Let's measure the real mall from photos"
**v6:** "Let's restructure for AI-native development"
**v7:** "Let's merge the evidence with the systems"
**v8:** "Let's prove it all works together"

### Key Innovations Across Versions

1. **Toddler Presence System** (v1) - Invisible entity creating escalating environmental horror
2. **Reality-Breaking Heat** (v2) - GTA stars that expose the simulation
3. **Separation of Simulation and Presentation** (v2) - Modern architecture pattern
4. **Cloud-Driven Semantic Spaces** (v4) - World as abstract state, not tiles
5. **CRD Workflow** (v5) - Photo-based architectural archaeology
6. **Contradiction as Canon** (v5) - Timeline variance as intentional design
7. **AI-Native Tooling** (v6) - Structured schemas for all entities
8. **Evidence + Systems Integration** (v7) - Measured reality + simulation
9. **Horror Stack Integration** (v8) - Toddler → Cloud → NPC → LLM → Renderer

### The Philosophy

> "V1: A complete retro game.
> V2: A modern immersive sim hiding under retro graphics.
> V3: The full graphical realization of V2's systems.
> V4: A Cloud-driven world where canon emerges from resonance.
> V5: Evidence-based reconstruction—architectural archaeology.
> V6: The AI-native restructure—clean slate.
> V7: Evidence + Systems = The integration.
> V8: The infrastructure screams.
>
> All are intentional.
> All are real.
> All contribute to the whole."

### Current Status (2025-12-05)

**Canonical Version:** v7-nextgen (Integration Complete)
**Active Development:** v8-nextgen (Horror Stack Operational)
**Repository:** GLITCHDEXMALLv7
**Branch:** `claude/collect-dev-legacy-docs-015vaJ5SXkjqaWoC2tbfeUTN`

**Everything but visuals: READY.**
**3 credit cards: LOADED.**
**Mall dungeon: AWAITS.**
**The infrastructure: SCREAMING.**

---

## DOCUMENT METADATA

**Document Title:** CRYSTALIZED KNOWLEDGE VECTOR ENGINE
**Subtitle:** GLITCHDEX MALL Complete Development Legacy (v1 → v8)
**Created:** 2025-12-05
**Author:** Claude (Sonnet 4.5)
**Purpose:** Comprehensive development history preservation
**Audience:** Future developers, AI agents, project stakeholders
**Status:** Complete snapshot of development as of 2025-12-05
**Location:** `/docs/CRYSTALIZED_KNOWLEDGE_VECTOR_ENGINE.MD`

### Source Documents

This document synthesizes information from:
- VERSION_GUIDE.md
- README.md
- RECONSTRUCTION_NOTES.md
- RESTRUCTURE_SUMMARY.md
- AI_NATIVE_RESTRUCTURE.md
- v1-doofenstein/README.md
- v2-immersive-sim/README.md
- v3-eastland/ (inferred from VERSION_GUIDE)
- v4-renderist/README.md
- v5-eastland/README.md
- v6-nextgen/README.md
- v7-nextgen/README.md
- v8-nextgen/README.md
- v8-nextgen/V7_INTEGRATED_DEMO_README.md

### Maintenance

This document should be updated when:
- Major version milestones are reached
- Significant architectural changes occur
- New development principles are established
- Repository restructures happen
- Canonical version changes

---

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  GLITCHDEX MALL: Eight Versions, One Vision                   ║
║                                                                ║
║  From Wolf3D raycaster to evidence-based architectural        ║
║  archaeology with AI-driven simulation and LLM integration.   ║
║                                                                ║
║  "Canon emerges from resonance and repetition, not ego."      ║
║  "Reconstruction > Hallucination"                             ║
║  "Space station with a parking lot, not a building."          ║
║  "The infrastructure is screaming."                           ║
║                                                                ║
║  v1-v8: All are intentional. All are real.                    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**END OF DOCUMENT**
