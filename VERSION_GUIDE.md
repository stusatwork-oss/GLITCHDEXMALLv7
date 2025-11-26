# GLITCHDEX MALL - VERSION GUIDE

This repository contains **six versions** of the game, each building on the previous:

---

## 📁 **v1-doofenstein/** - Original Retro Mall Crawler

**What it is**: The original DOOFENSTEIN 3D game - a complete, playable Wolfenstein 3D-style mall crawler.

**Features**:
- Working Wolf3D raycaster renderer
- Toddler presence system
- Reality glitch system (basic)
- NPC interactions
- Artifact collection
- Full playable game

**Status**: ✅ **COMPLETE & PLAYABLE**

**Run it**:
```bash
cd v1-doofenstein
python src/main.py
```

**Best for**:
- Playing the original game
- Understanding the base systems
- Simpler codebase to study

---

## 📁 **v2-immersive-sim/** - Hidden Open-World Sandbox

**What it is**: A complete architectural overhaul - a cutting-edge immersive sim hiding under the Wolf3D facade.

**Features**:
- **Faction System**: Complex AI with emergent politics, memory, gossip propagation
- **NPC Intelligence**: A* pathfinding, GOAP, individual memories, schedules
- **Stealth System**: Vision cones, noise propagation, alert states
- **Heat System**: GTA wanted stars that **BREAK REALITY at level 5**
- **Prop System**: 25+ interactive objects with systemic interactions
- **Meta Design**: At max heat, the modern engine is EXPOSED

**Status**: ✅ **PLAYABLE** (text renderer, Wolf3D upgrade coming soon)

**Philosophy**:
> "A full AAA immersive sim wearing a 50-cent Wolf3D Halloween mask that slips when the chaos gets too high."

**Best for**:
- Game developers studying modern AI architecture
- Seeing how to separate simulation from rendering
- Understanding immersive sim design
- Appreciating absurd technical ambition

---

## 📁 **v3-eastland/** - Pygame Graphical Engine

**What it is**: The culmination of V1's raycaster and V2's AI systems - a full graphical Pygame renderer with all simulation systems online.

**Features**:
- **Pygame Raycaster**: Full graphical 3D rendering
- **All V2 AI Systems**: Factions, A* pathfinding, GOAP, stealth, heat
- **Pong Mini-game**: Arcade cabinet interaction
- **Dual Entry Points**: Text (main.py) or Graphical (main_pygame.py)

**Status**: ✅ **COMPLETE & PLAYABLE**

**Run it**:
```bash
cd v3-eastland
python src/main_pygame.py
```

**Best for**:
- Playing the fully realized graphical version
- Seeing all systems working together
- Complete gameplay experience

---

## 📁 **v4-renderist/** - Cloud-Driven World (NEW)

**What it is**: A fundamental architectural shift from tile-based maps to Cloud-driven semantic spaces.

**Features**:
- **Cloud State System**: Global pressure 0-100, 4 moods, 3 bleed tiers
- **13 Anchor NPCs**: Persistent entities with spines and contradiction triggers
- **Swarm System**: Population curves with confirming-only Cloud feedback
- **60fps Loop**: Cloud tick every 10 frames with interpolation
- **Contradiction Cascade**: Zone cooldown logic (30 seconds)

**Status**: ✅ **PHASE 1 COMPLETE** (V4.0.1-alpha)

**Philosophy**:
> "Canon emerges from resonance and repetition, not ego."

**Run it**:
```bash
cd v4-renderist
python src/main.py
```

**Demo mode**:
```bash
python -c "from src.main import mall_demo; mall_demo()"
```

**Best for**:
- Cloud-driven world design
- Studying NPC contradiction systems
- Sora/video integration experiments

---

## 📁 **v5-eastland/** - CRD Reconstruction (Documentation)

**What it is**: A systematic, evidence-based reconstruction of Eastland Mall using the Classification Reference Document (CRD) workflow.

**Features**:
- **Photo Classification**: 143 photos classified into PRIMARY/FEATURE/ZONE categories
- **Feature Extraction**: 11 measurable atomic units (glass blocks, vending machines, etc.)
- **Zone Graph**: 9 structural zones mapped with relationships
- **Measurement Sheet**: 15 measurements extracted with confidence levels
- **Map Corrections**: 12 corrections synthesized from photographic evidence
- **Full Traceability**: Every measurement linked to source photos

**Status**: ✅ **V1 COMPLETE** (awaiting V2+ fidelity passes)

**Philosophy**:
> "Architectural archaeology - measuring a 1,000,000+ sq ft megastructure from photographs"

**Best for**:
- Understanding evidence-based reconstruction methodology
- Seeing how to systematically document large structures
- Studying the CRD workflow for future projects
- Appreciating the scale of Eastland Mall (it's massive!)

---

## 📁 **v6-nextgen/** - Next Generation (Placeholder)

**What it is**: A placeholder for the next evolution of GLITCHDEX MALL.

**Features**:
- TBD - Future development

**Status**: 🔄 **PLACEHOLDER** (no implementation yet)

**Run it**:
```bash
cd v6-nextgen
python src/main.py
```

**Philosophy**:
> "The future awaits - what comes after cloud-driven worlds and CRD reconstruction?"

**Best for**:
- Future development and experimentation
- Integration of new technologies and methodologies
- Next-generation gameplay and simulation

---

## 🎯 WHICH VERSION SHOULD I USE?

| **If you want...** | **Use** |
|-------------------|---------|
| Quick retro experience | **v1-doofenstein** |
| To see sophisticated AI | **v2-immersive-sim** |
| Full graphical + AI | **v3-eastland** |
| Cloud-driven architecture | **v4-renderist** |
| Evidence-based reconstruction | **v5-eastland** |
| Future development | **v6-nextgen** |
| Simple codebase | **v1-doofenstein** |
| Complete gameplay | **v3-eastland** |
| Sora/AO3 integration | **v4-renderist** |
| Architectural archaeology | **v5-eastland** |
| Meta-commentary | **v2-immersive-sim** |

---

## 🔬 TECHNICAL COMPARISON

| Feature | v1 | v2 | v3 | v4 | v5 | v6 |
|---------|----|----|----|----|----|----|
| **Renderer** | Wolf3D ANSI | Text | Pygame | TBD | Documentation | TBD |
| **NPC AI** | Simple | A* + GOAP | A* + GOAP | Cloud-driven | N/A | TBD |
| **World Model** | Tile map | Tile map | Tile map | Semantic zones | CRD zones | TBD |
| **Factions** | None | Complex | Complex | Resonance-based | N/A | TBD |
| **Stealth** | None | Full | Full | Cloud mood | N/A | TBD |
| **Heat/Wanted** | None | GTA-style | GTA-style | Bleed Events | N/A | TBD |
| **Props** | Static | Interactive | Interactive | Cloud-weighted | Measured | TBD |
| **Complexity** | Game jam | AAA | AAA+ | Experimental | Archival | TBD |
| **Philosophy** | Retro game | Hidden sim | Complete sim | Cloud canon | Archaeology | Future |

---

## 🎭 THE V2 VISION: REALITY BREAKS

At **Heat Level 5** in v2, the game reveals its true nature:

```
┌──────────────────────────────────────────────────────────────┐
│ [CRITICAL] SIMULATION INTEGRITY COMPROMISED                  │
│                                                              │
│ ENGINE: Unreal Engine 5.3 / Unity 2023.2                    │
│ AI_AGENTS: 87 active                                        │
│ PATHFINDING: Recast/Detour Nav Mesh [EXPOSED]              │
│                                                              │
│ [ERROR] Cannot maintain Wolf3D facade                        │
│ [WARNING] Modern rendering bleeding through                 │
└──────────────────────────────────────────────────────────────┘
```

You see:
- AI pathfinding lines overlaid on retro graphics
- Nav mesh visualization
- Real engine stats
- Photorealistic textures leaking through
- The **50-cent mask shattering**

---

## 📜 REPOSITORY STRUCTURE

```
GLUTCHDEXMALL/
├── launcher_gui.py          # NEW: Mid-90s 16-color GUI launcher (mouse support)
├── shareware_gen_v2.py      # Updated program generator (includes v5, v6)
├── LAUNCH_GUI.sh            # Launch GUI launcher
├── LAUNCH.sh                # Launch text-based launcher
│
├── v1-doofenstein/          # Original complete game + SHAREWARE LAUNCHER
│   ├── src/
│   │   ├── launcher.py      # Shareware CD menu (launches all versions)
│   │   ├── shareware_gen.py # Updated to include v5, v6
│   │   ├── game_loop.py     # Main game
│   │   └── wolf_renderer.py # ANSI raycaster
│   └── data/
│
├── v2-immersive-sim/        # Advanced AI architecture
│   ├── src/
│   │   ├── mall_simulation.py      # Orchestrator
│   │   ├── faction_system.py       # Faction AI
│   │   ├── npc_intelligence.py     # NPC AI + A*
│   │   └── heat_system.py          # Heat + reality break
│   └── data/
│
├── v3-eastland/             # Pygame graphical version
│   ├── src/
│   │   ├── main_pygame.py   # Pygame entry point
│   │   ├── pygame_renderer.py      # Graphical raycaster
│   │   └── (all V2 systems)
│   └── data/
│
├── v4-renderist/            # Cloud-driven world (Phase 1 Complete)
│   ├── src/
│   │   ├── main.py          # Entry point + mall_demo()
│   │   ├── cloud.py         # Global state system
│   │   ├── anchor_npcs.py   # 13 persistent NPCs
│   │   ├── swarm.py         # Ambient crowd system
│   │   └── bleed_events.py  # Sora integration (Phase 2)
│   └── docs/
│
├── v5-eastland/             # CRD Reconstruction (Documentation)
│   ├── README.md
│   ├── README_ARCHITECTURAL_CONTEXT.md
│   ├── docs/
│   │   ├── crd/             # CRD workflow documents
│   │   └── BATCH_PROCESSING_PLAN.md
│   └── data/
│       └── MALL_MAP_V5_PROPOSAL.json
│
├── v6-nextgen/              # Next Generation (Placeholder)
│   ├── README.md
│   ├── src/
│   │   └── main.py          # Placeholder entry point
│   ├── data/
│   └── docs/
│
└── VERSION_GUIDE.md         # This file
```

**Shareware Launcher Programs**: 387=V1, 388=V2, 389=V3, 390=V4, 391=V5, 392=V6

---

## 🚀 GETTING STARTED

### **Play v1 (Original Game)**
```bash
cd v1-doofenstein
bash PLAY.sh
# OR
python src/main.py
```

### **Play v2 (Immersive Sim)**
```bash
cd v2-immersive-sim
python3 src/main.py
```

**New to V2?** Read `HOW_TO_PLAY.md` for simple instructions!

---

## 💡 DEVELOPER NOTES

**v1** is a complete vertical slice - play it, modify it, learn from it.

**v2** is a horizontal architecture - study the systems, see how they interact, understand the separation of simulation and rendering.

Both versions demonstrate different approaches:
- **v1**: Integrated, monolithic, "get it working"
- **v2**: Modular, systemic, "build it right"

Neither is "better" - they serve different purposes.

---

## 🎓 LEARNING PATH

1. **Start with v1**: Play the game, understand the basic systems
2. **Read v2 README**: Understand the architectural vision
3. **Study v2 systems**: See how modern game AI is built
4. **Compare**: Notice how v2 separates concerns
5. **Appreciate**: Realize the absurdity of building AAA systems for terminal art

---

## 🏆 THE META JOKE

v1: "Here's a retro game."
v2: "Here's a modern game PRETENDING to be retro that FAILS at pretending when chaos peaks."

The entire design of v2 is meta-commentary on:
- Game engine facades
- Simulation vs presentation
- How much complexity can hide under simple visuals
- What happens when the mask slips

**It's not a bug. It's the entire point.**

---

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  v1: A complete retro game.                                   ║
║  v2: A modern immersive sim hiding under retro graphics.      ║
║  v3: The full graphical realization of V2's systems.          ║
║  v4: A Cloud-driven world where canon emerges from resonance. ║
║  v5: Evidence-based reconstruction - architectural archaeology║
║  v6: The next generation - future development awaits          ║
║                                                                ║
║  All are intentional.                                         ║
║  All are real.                                                ║
║  Choose your experience.                                      ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```
