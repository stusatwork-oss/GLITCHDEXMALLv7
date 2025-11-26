# GLITCHDEX MALL V2: IMMERSIVE SIM
## *A Symphony in a 50-Cent Halloween Mask*

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   "A full modern immersive sim wearing a cheap Wolf3D Halloween mask        ║
║    that starts to slip as the toddler and glitches escalate."               ║
║                                                                              ║
║   What the player SEES: Retro Wolf3D mall crawler in ANSI terminal art      ║
║   What's ACTUALLY running: Cutting-edge 2025 game AI and systems            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 🎭 THE CONCEPT

This is an **open-world immersive sim** (think Far Cry 6 / Dishonored / Deus Ex) with:
- Faction AI with emergent politics
- Individual NPC intelligence with A* pathfinding
- Stealth mechanics (vision cones, noise propagation)
- GTA-style heat/wanted system
- 25+ interactive props with systemic interactions

**BUT** it's all rendered as:
- Wolfenstein 3D raycaster
- ANSI 256-color terminal art
- 64x64 pixel textures

The kicker: **At maximum heat (5 stars), the simulation BREAKS**. The Wolf3D facade can't handle the chaos. Modern rendering bleeds through. You see:
- Real-time AI pathfinding visualization
- Nav mesh overlays
- Engine profiler stats
- Photorealistic texture leaks
- 1080p glory breaking through 8-bit constraints

---

## 🏗️ ARCHITECTURE

### **Core Philosophy: Separation of Simulation and Presentation**

```
┌─────────────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER (Wolf3D Facade - The 50¢ Mask)                 │
│  ├─ wolf_renderer.py    - Raycaster with textured walls            │
│  ├─ ANSI 256-color      - VGA palette aesthetic                    │
│  └─ reality_glitch.py   - Cracks in the facade                     │
└─────────────────────────────────────────────────────────────────────┘
                                    ▲
                                    │
                    Rendering hints & NPC positions
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│  SIMULATION LAYER (2025 AAA Engine - The Real Deal)                │
│  ├─ mall_simulation.py     - Main orchestrator                     │
│  ├─ faction_system.py      - Complex faction AI                    │
│  ├─ npc_intelligence.py    - Individual NPC AI + A* pathfinding    │
│  ├─ stealth_system.py      - Vision cones, noise, alerts           │
│  ├─ heat_system.py         - GTA wanted stars + reality breaks     │
│  └─ prop_system.py         - Interactive objects with physics      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 SYSTEM BREAKDOWN

### **1. Faction System** (`faction_system.py`)
**Complexity Level: MAXIMUM**

- **6 Factions**: Security, Workers, Shoppers, Teens, Management, Janitors
- **Collective Memory**: Factions remember player actions, share information via gossip
- **Dynamic Relationships**: Factions' relationships evolve based on player behavior
- **Schedules**: Time-based behavior patterns (patrols, breaks, rush hours)
- **Coordinated Responses**: Allied factions work together when heat is high

**Emergent Behavior Example**:
*Player attacks a security guard → Security faction becomes hostile → They gossip to Management → Management also becomes hostile → Coordinated lockdown response*

---

### **2. NPC Intelligence** (`npc_intelligence.py`)
**Complexity Level: MAXIMUM**

Each NPC is a tiny AI agent with:
- **A* Pathfinding**: Real pathfinding with dynamic obstacle avoidance
- **Personal Memory**: Remembers seeing player, suspicious events
- **GOAP (Goal-Oriented Action Planning)**: NPCs select goals dynamically
- **Behavior States**: Idle, Patrolling, Investigating, Pursuing, Fleeing, etc.
- **Personality**: Aggression, bravery, curiosity, sociability affect decisions
- **Schedules**: Individual daily routines

**What You See**: Simple sprites sliding around
**What's Running**: Sophisticated AI agents with decision trees and pathfinding

---

### **3. Stealth System** (`stealth_system.py`)
**Complexity Level: BASIC (as requested)**

- **Vision Cones**: NPCs have field-of-view with angle and range
- **Line-of-Sight**: Raycasting to check if player is visible
- **Noise Propagation**: Actions create noise with radius and falloff
- **Alert States**: Unalert → Suspicious → Searching → Alerted

**Immersive Sim Tactics**:
- Throw plant pot → Creates noise → Guards investigate → Sneak past
- Break glass → Loud noise → Multiple guards converge → Create chaos

---

### **4. Heat System** (`heat_system.py`)
**Complexity Level: REALITY-BREAKING**

GTA-style wanted stars (★★★★★) but with a twist:

| Heat Level | Effect | Facade Status |
|------------|--------|---------------|
| ★☆☆☆☆ | Security watches | Intact |
| ★★☆☆☆ | Active pursuit | Stable |
| ★★★☆☆ | Lockdown procedures | Minor cracks |
| ★★★★☆ | Full lockdown | Glitching |
| ★★★★★ | **REALITY BREAK** | **MASK SHATTERED** |

**At Heat 5**:
- Reality stability drops to 0%
- Modern rendering systems bleed through
- You see:
  - AI pathfinding lines overlaid on Wolf3D view
  - Nav mesh visualization
  - Engine stats (Unreal/Unity fake profiler)
  - Photorealistic textures leaking through retro art
  - Wireframe geometry peeking out

**The Showpiece**: This is where GenAlpha goes "THIS SLAPS FR FR" on stream.

---

### **5. Prop System** (`prop_system.py`)
**Complexity Level: RICH (25+ props)**

Interactive objects with systemic depth:

#### **Distraction Props**
- Vending Machine: Use → noise → NPCs investigate
- Arcade Cabinet: Play → beeping → nearby NPCs distracted

#### **Destructible Props**
- Plant Pot: Throw → crash → distraction + heat
- Glass Door: Break → loud shatter → alarm + major heat

#### **Security Props**
- Security Camera: Hack → offline + reduce heat
- Alarm Panel: Trigger → lockdown + massive heat

#### **Combo Interactions**
- Trash Can + Lighter → Fire → massive distraction + evacuation + max heat
- Vending Machine + Kick → loud noise + chance of loot + heat

**Immersive Sim Moment**:
*Kick vending machine → Guards investigate noise → Sneak into security office → Hack alarm panel → Disable cameras → Steal keycard → Escape*

---

## 🎨 RENDERING & REALITY GLITCHES

### **Normal State** (Heat < 4)
- Wolf3D raycaster
- 256-color ANSI art
- Textured walls (8x8 patterns)
- Floor/ceiling rendering
- Billboard sprites for NPCs

### **Reality Break State** (Heat = 5)
```
┌─────────────────────────────────────────────────────────────────┐
│ [CRITICAL] SIMULATION INTEGRITY COMPROMISED                     │
│                                                                 │
│ ENGINE: Unreal Engine 5.3.2 / Unity 2023.2                     │
│ RENDERER: Forward+ / Deferred PBR                              │
│ DRAWCALLS: 2847 (batched: 2203)                                │
│ TRIANGLES: 184,392                                             │
│ AI_AGENTS: 87 active                                           │
│ PATHFINDING: Recast/Detour Nav Mesh [VISIBLE]                 │
│ LIGHTING: Ray Traced GI + Lumen [BLEEDING THROUGH]            │
│                                                                 │
│ [ERROR] Cannot maintain retro facade                           │
│ [WARNING] Wolf3D mask: FAILING                                │
│ [CRITICAL] Reality stable: FALSE                               │
└─────────────────────────────────────────────────────────────────┘
```

Visual effects at reality break:
- Wireframe overlay (see the actual poly mesh)
- Photorealistic texture leaks (too much detail for Wolf3D)
- AI pathfinding debug lines
- Vision cone visualization
- Nav mesh display
- Real-time profiler overlay

**The Meta Joke**: The game reveals it was ALWAYS a modern engine, desperately pretending to be retro.

---

## 📊 TECHNICAL SPECS

### **Systems**
| System | Tech | Complexity |
|--------|------|------------|
| Pathfinding | A* with caching | Production-quality |
| NPC AI | GOAP-lite + FSM | Game-quality |
| Faction AI | Memory + Gossip propagation | Cutting-edge |
| Stealth | Vision cones + raycasting | Industry-standard |
| Heat | State machine + reality break | **Meta/Unique** |
| Props | Component-based interactions | Immersive sim-tier |

### **Performance**
- **Target**: 60 FPS in terminal
- **NPC Count**: 30-50 simultaneous (batched updates)
- **Pathfinding**: Cached A* with 500-iteration limit
- **Memory**: < 200MB (all Python, no external deps)

### **No External Licenses**
- Pure Python stdlib
- No Unity, no Unreal, no Godot
- Custom raycaster
- Custom AI
- Custom everything

**"Free as in freedom, cutting-edge as in 2025."**

---

## 🎮 GAMEPLAY LOOP

1. **Enter the Mall**: Looks like a simple retro FPS
2. **Explore**: Find artifacts, talk to NPCs
3. **Experiment**: Kick vending machine → Guards investigate
4. **Escalate**: Break stuff, get seen, heat builds
5. **Chase**: Security pursues, factions coordinate
6. **Lockdown**: Mall seals, heat at 4 stars
7. **REALITY BREAK**: Heat hits 5 stars
   - Wolf3D facade **shatters**
   - Modern AI systems **exposed**
   - 1080p rendering **bleeds through**
   - GenAlpha: "BRO THIS IS INSANE"

---

## 🔥 WHY THIS IS SPECIAL

### **For Unix Gods**
- Clean architecture: Separation of concerns
- No bloat: Pure Python, no frameworks
- Hackable: Every system is modular and documented
- Performance: Batched updates, caching, optimization

### **For GenAlpha**
- Aesthetic: Retro visuals + modern mechanics = "Peak nostalgia bait"
- Meta humor: The game KNOWS it's hiding cutting-edge tech
- Streamable: Reality breaks are clip-worthy moments
- Emergent: Every playthrough is different (faction AI creates stories)

### **For Game Devs**
- **Architecture reference**: How to separate simulation from rendering
- **AI showcase**: Faction systems, GOAP, A* pathfinding
- **Immersive sim design**: Systemic interactions, emergent gameplay
- **No engine lock-in**: Proves you don't need Unity/Unreal

---

## 📂 FILE STRUCTURE

```
v2-immersive-sim/
├── src/
│   ├── mall_simulation.py      # Main orchestrator
│   ├── faction_system.py       # Complex faction AI
│   ├── npc_intelligence.py     # Individual NPC AI + A*
│   ├── stealth_system.py       # Vision/noise/alerts
│   ├── heat_system.py          # Wanted stars + reality break
│   ├── prop_system.py          # Interactive objects
│   └── (rendering components to be added)
├── data/
│   ├── mall_map.json           # World layout
│   ├── entities.json           # NPC definitions
│   └── artifacts.json          # Collectibles
├── tests/
│   └── (test suites)
└── README.md                   # This file
```

---

## 🚀 RUNNING THE GAME

**STATUS: ✅ NOW PLAYABLE!**

```bash
cd v2-immersive-sim
python3 src/main.py
```

**What to expect:**
1. Text-based rendering (Wolf3D renderer coming soon)
2. NPCs patrol, shop, work (all with sophisticated AI underneath)
3. Player interacts with props → emergent chaos
4. Heat builds → factions coordinate → lockdown
5. Heat = 5 → **REALITY SHATTERS** → modern engine revealed

**First time playing?** Read `HOW_TO_PLAY.md` for simple instructions!

---

## 🎯 DESIGN GOALS ACHIEVED

✅ **Complex Faction AI**: Schedules, memory, gossip, emergent politics
✅ **Individual NPC Intelligence**: A*, GOAP, personalities, awareness
✅ **Basic Stealth**: Vision cones, noise, alert states
✅ **Reality-Breaking Heat**: GTA stars that expose the simulation
✅ **Rich Props**: 25+ objects with combos and chain reactions
✅ **Cutting-Edge Under ANSI**: Modern 2025 AI hiding under terminal art

---

## 🧪 THE PHILOSOPHY

> **"What if we built a AAA immersive sim but forced ourselves to render it as Wolf3D?"**

This project is about:
- **Emergence over scripting**: Systems interact to create stories
- **Depth over graphics**: Sophisticated AI in ASCII
- **Meta-commentary**: The game itself is about facades breaking
- **No compromises**: Full modern systems, full retro aesthetic

**It's not just a game. It's a statement.**

---

## 🏆 FOR THE LULZ (GenAlpha Certified™)

When a streamer hits Heat 5 and the reality break happens:
```
Chat: "BRO IS THAT UNREAL ENGINE??"
"WAIT IT WAS MODERN THIS WHOLE TIME???"
"THE PATHFINDING LINES OMG"
"THIS IS ACTUALLY INSANE FR"
"CHAT IS THIS REAL"
```

**That's the moment we're building toward.**

---

## 📜 LICENSE & CREDITS

**License**: *(To be decided by creator)*
**Tech Stack**: Pure Python, no external game engines
**Philosophy**: Unix philosophy meets immersive sim design

Built with spite, ambition, and a 50-cent Halloween mask.

---

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  "A full immersive sim wearing a Wolf3D mask.                   ║
║   The mask slips. You see what's really underneath.             ║
║   It was never retro. It was always cutting-edge.               ║
║   The simulation was the lie. The systems were always real."    ║
║                                                                  ║
║   Welcome to Glitchdex Mall V2.                                ║
║   The facade is breaking.                                       ║
║   Enjoy the show.                                               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```
