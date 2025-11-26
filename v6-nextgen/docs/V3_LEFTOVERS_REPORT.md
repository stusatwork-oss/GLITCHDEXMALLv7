# V3 Leftovers - Cannot Port to V6

**Analysis Date:** 2025-11-26
**Source:** v3-eastland folder analysis
**Decision:** These systems are V3-specific and **cannot** be ported to V6

---

## ✅ **Successfully Ported to V6**

### Content (Data)
- ✅ **49 Artifacts** → `canon/artifacts_catalog.json`
- ✅ **6 NPC Definitions** (Milo, BORED, R0-MBA, Mall Cop, 2 Shoppers) → `canon/npc_spines_v3_port.json`
- ✅ **11 Zone Descriptions** (stores, food court, theater, etc.) → `canon/zone_lore_v3_port.md`

### Concepts (Portable Ideas)
- ✅ **Dialogue Escalation System** - V3 scales dialogue with Heat, V6 can scale with Cloud (documented in port files)
- ✅ **Artifact Lore** - Rich environmental storytelling through discoverable items
- ✅ **NPC Personality Traits** - Complex character definitions with secret knowledge

---

## ❌ **Cannot Port - Renderer-Specific Systems**

### 1. **Pygame Renderer** (`pygame_renderer.py`, `wolf_renderer.py`)
**Why:** V6 uses UE5, not Pygame/Wolf3D.
**V3 Implementation:** 256-color sprites, raycasting, Wolf3D aesthetic
**V6 Equivalent:** UE5 handles rendering. Bridge sends data, UE5 renders 3D scenes.

**Leftover Files:**
- `src/pygame_renderer.py`
- `src/wolf_renderer.py`
- `src/sprite_system.py`
- `src/renderer_strain_system.py` (visual glitch effects for Pygame)

**Decision:** Do not port. UE5 is the renderer now.

---

### 2. **Reality Glitch Visual System** (`reality_glitch_system.py`)
**Why:** Tightly coupled to Pygame rendering.
**V3 Implementation:**
- Pathfinding line flickers
- Name corruption (AI_AGENT_047 overlay)
- Texture bleeds (photorealistic leak into Wolf3D)
- Engine stat popups
- Wireframe flashes
- Nav mesh peeks

**V6 Equivalent:** UE5 post-process materials, niagara VFX, material parameter collection.

**Concept to Port:** The **escalation pattern** is good:
- Heat < 3: No glitches
- Heat 3-3.5: Rare 1-frame flickers
- Heat 3.5-4: Increasing frequency
- Heat 4-4.5: Frequent, obvious
- Heat 4.5+: Near-constant before full break

**Action:** Document this pattern in UE5_INTEGRATION.md as VFX intensity scaling based on Cloud level.

**Leftover Files:**
- `src/reality_glitch_system.py`
- `src/reality_glitch.py`
- `src/renderer_strain_system.py`

**Decision:** Keep concept (escalation), reimplement in UE5 as post-process + VFX.

---

### 3. **Prop Physics System** (`prop_system.py`)
**Why:** Immersive sim-style interaction system designed for 2D tile-based world.
**V3 Implementation:**
- 25+ interactive props (vending machines, arcade cabinets, security panels)
- Physics simulation (throwing, breaking, chain reactions)
- Distraction mechanics (noise attracts NPCs)
- Container interactions (lockers, cash registers)

**V6 Equivalent:** UE5 physics system + blueprint interactables.

**Concept to Port:** The **interaction types** are valuable:
- Distraction props (vending machines make noise)
- Security props (cameras, alarms)
- Destructible props (plants, trash cans)
- Containers (lockers with loot)

**Action:** UE5 team should implement as blueprint actors with similar interaction patterns.

**Leftover Files:**
- `src/prop_system.py` (600+ lines of prop interaction logic)

**Decision:** Do not port Python code. Reimplement in UE5 blueprints using same design patterns.

---

### 4. **Sprite System** (`sprite_system.py`)
**Why:** 256-color sprite management for Wolf3D aesthetic.
**V3 Implementation:**
- Sprite atlas loading
- Animation frame management
- Sprite rotation (8 directions)
- Layering (background, props, NPCs, foreground)

**V6 Equivalent:** UE5 skeletal meshes, static meshes, Unreal's animation system.

**Leftover Files:**
- `src/sprite_system.py`

**Decision:** Do not port. UE5 handles all visual assets.

---

## ❌ **Cannot Port - V3-Specific Game Systems**

### 5. **Tile-Based World System** (`mall_map.json`, `world_loader.py`)
**Why:** V3 uses explicit tile grid (120x90), V6 uses continuous 3D space in UE5.
**V3 Implementation:**
- Tile-by-tile map definition
- X, Y, Z coordinates (z=-1 for sunken food court)
- Tile types (CORRIDOR, FOUNTAIN_TERRACE, ATRIUM, etc.)
- Player position snapped to tiles

**V6 Equivalent:** UE5 level geometry, navmesh, trigger volumes.

**Concept to Port:** The **zone topology** (which zones connect to which) is valuable for adjacency system.

**Action:** Extract zone adjacency graph from mall_map.json, integrate into V6 Cloud's adjacency system.

**Leftover Files:**
- `data/mall_map.json` (472 lines of tile definitions)
- `src/world_loader.py` (tile loading logic)

**Decision:** Do not port tile system. Extract zone graph, discard tile coordinates.

---

### 6. **Heat System** (`heat_system.py`, `heat5_revelation.py`)
**Why:** V3 uses "Heat" (0-5 scale), V6 uses "Cloud" (0-100 scale).
**V3 Implementation:**
- Heat 0-5 based on player actions
- Heat 3+ triggers reality glitches
- Heat 5 = full mask break (simulation reveal)

**V6 Equivalent:** Cloud system (`cloud.py`)

**Mapping:**
| V3 Heat | V6 Cloud | Mood |
|---------|----------|------|
| 0-1 | 0-24 | Calm |
| 2 | 25-49 | Uneasy |
| 3 | 50-74 | Strained |
| 4 | 75-89 | Critical |
| 5 | 90-100 | Bleed |

**Leftover Files:**
- `src/heat_system.py`
- `src/heat5_revelation.py` (special reveal at Heat 5)

**Decision:** Do not port. V6 Cloud already implements similar escalation with different scale.

---

### 7. **Toddler System** (`toddler_system.py`)
**Why:** V3-specific lore entity. The "toddler" is using AAA engine to escape Wolf3D prison.
**V3 Implementation:**
- Invisible entity that amplifies heat
- Follows player or chaos
- Causes reality distortion in radius
- Becomes visible at Heat 5

**V6 Equivalent:** Could be reimplemented as "bleed amplifier" entity, but not priority.

**Concept to Port:** The idea of a **hidden entity that amplifies Cloud pressure** in certain zones is interesting for V6 late-game.

**Action:** Consider for V6 Phase 4+ (post-MVP).

**Leftover Files:**
- `src/toddler_system.py` (200+ lines)

**Decision:** Do not port now. Revisit concept for V6 endgame content.

---

### 8. **Faction System** (`faction_system.py`, `entities.json`)
**Why:** V3 uses factions (security, workers, teens, shoppers) with inter-group relationships. V6 doesn't have this yet.
**V3 Implementation:**
- 4 factions with attitudes (friendly, neutral, hostile)
- Faction members (NPCs belong to factions)
- Patrol zones (security patrols specific areas)

**V6 Equivalent:** Could be added, but not in current spec.

**Concept to Port:** The **faction membership** concept is useful for grouping NPCs and determining behavior.

**Action:** Document as "Future Enhancement" for V6. Consider for Phase 3+.

**Leftover Files:**
- `src/faction_system.py`
- Faction definitions in `data/entities.json`

**Decision:** Do not port now. V6 NPCs don't have faction relationships yet. Add later if needed.

---

### 9. **Dialogue System** (`dialogue_system.py`)
**Why:** Tightly coupled to V3's Heat system and text-based interaction.
**V3 Implementation:**
- 500+ dialogue lines
- Heat-scaled escalation (subtle → AI exposure)
- Faction-specific lines
- Schedule/patrol/GOAP leak dialogue

**V6 Equivalent:** UE5 dialogue system (Dialogue Manager, behavior trees).

**Concept to Port:** The **escalation pattern** and **line categories** are excellent:
- Stage 0-1 (Calm): Normal, subtle weirdness
- Stage 2 (Uneasy): Skyrim-level AI talk ("Shift change at 1700")
- Stage 3 (Strained): Mask slipping ("Why am I saying this?")
- Stage 4 (Critical): Full AI exposure ("GOAP priority: PURSUE_TARGET")
- Stage 5 (Bleed): Simulation speaks ("I am AI_AGENT_047")

**Action:** Dialogue escalation pattern documented in `npc_spines_v3_port.json` with Cloud-level mappings.

**Leftover Files:**
- `src/dialogue_system.py` (800+ lines)

**Decision:** Do not port Python code. UE5 implements dialogue. Use pattern documented in port files.

---

### 10. **Stealth System** (`stealth_system.py`, `stealth_feedback.py`)
**Why:** V3 stealth mechanics (line of sight, noise detection, alert states). V6 doesn't have stealth gameplay yet.
**V3 Implementation:**
- Line-of-sight raycasting
- Noise propagation
- NPC alert levels (unaware → searching → hostile)
- Stealth feedback (suspicion meter)

**V6 Equivalent:** If V6 adds stealth, UE5 AI Perception system handles this.

**Leftover Files:**
- `src/stealth_system.py`
- `src/stealth_feedback.py`

**Decision:** Do not port. V6 doesn't have stealth gameplay. If added later, use UE5's AI Perception.

---

### 11. **NPC Intelligence System** (`npc_intelligence.py`)
**Why:** V3's NPC AI system with pathfinding, schedule, patrol, GOAP-style logic.
**V3 Implementation:**
- A* pathfinding on tile grid
- Daily schedules (workers take breaks)
- Patrol routes (security loops)
- GOAP-style goal selection

**V6 Equivalent:** UE5 Behavior Trees + navmesh. V6's `npc_state_machine.py` already handles NPC logic.

**Leftover Files:**
- `src/npc_intelligence.py` (400+ lines)

**Decision:** Do not port. V6 has `npc_state_machine.py`. UE5 handles pathfinding via navmesh.

---

## ❌ **Cannot Port - V3 Game Loop Files**

### 12. **Game Loop & Main** (`game_loop.py`, `main.py`, `main_pygame.py`, `mall_engine.py`, `mall_simulation.py`)
**Why:** These are V3's CLI/Pygame game runtime. V6 uses UE5 as the game engine.
**V3 Implementation:**
- Pygame event loop
- Player input handling
- Frame timing (60 FPS)
- Save/load system

**V6 Equivalent:** UE5 GameMode, PlayerController, Level Blueprint.

**Leftover Files:**
- `src/game_loop.py`
- `src/main.py`
- `src/main_pygame.py`
- `src/mall_engine.py`
- `src/mall_simulation.py`

**Decision:** Do not port. These are entire game runtimes for a different engine.

---

### 13. **Pong Minigame** (`pong.py`)
**Why:** V3 has a playable Pong cabinet. Fun easter egg, but not essential.
**V3 Implementation:**
- Full Pong game in Pygame
- Playable from HARD COPY arcade

**V6 Equivalent:** Could be implemented in UE5 as a minigame blueprint.

**Leftover Files:**
- `src/pong.py` (200+ lines of Pong game logic)

**Decision:** Do not port now. Fun idea for V6 Phase 4+ polish.

---

## 📊 **Summary**

### ✅ **Ported to V6** (Content)
- 49 Artifacts with lore
- 6 NPC definitions (personalities, dialogue, spines)
- 11 Zone descriptions with atmospheric detail
- Dialogue escalation patterns (Heat → Cloud mapping)

### ❌ **Cannot Port** (25 files)
| Category | Files | Reason |
|----------|-------|--------|
| Rendering | 4 files | Pygame/Wolf3D specific, UE5 handles this |
| Visual Effects | 3 files | Renderer-dependent, reimplement in UE5 |
| World System | 2 files | Tile-based, V6 uses continuous 3D |
| Game Systems | 8 files | Heat, factions, stealth, toddler (V3-specific or not in V6 scope) |
| Game Runtime | 5 files | Pygame event loops, V6 uses UE5 |
| AI | 1 file | V6 has own NPC system |
| Minigames | 1 file | Pong (nice-to-have, not priority) |
| Props | 1 file | Reimplement in UE5 blueprints |

### 💡 **Concepts to Consider for V6 Future**
- **Faction System** - Group NPCs, inter-group dynamics (Phase 3+)
- **Prop Interaction Patterns** - Distraction, containers, physics (UE5 blueprints)
- **Toddler/Bleed Amplifier** - Hidden entity that amplifies Cloud pressure (Phase 4+)
- **Pong Minigame** - Easter egg at FC-ARCADE (Polish phase)
- **VFX Escalation Pattern** - Cloud-scaled visual glitches (UE5 post-process)

---

## 🎯 **Recommendation**

**DO NOT ATTEMPT TO PORT:**
- Any .py files from v3-eastland/src/ (except as reference for concepts)
- Tile-based map system
- Pygame rendering code
- Heat system (V6 has Cloud)

**USE V3 AS REFERENCE FOR:**
- Lore and world-building (already ported to canon/)
- NPC personality depth (use as template for new V6 NPCs)
- Dialogue escalation pattern (apply to V6 Cloud levels)
- Environmental storytelling approach (artifacts, zone descriptions)

**V6 IS A DIFFERENT ENGINE:**
- V3 = Python + Pygame + Wolf3D aesthetic
- V6 = Python simulation core + UE5 renderer + HTTP bridge
- Different architecture, different strengths, different goals

---

**End of V3 Leftovers Report**
