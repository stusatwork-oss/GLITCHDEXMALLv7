# V7 Entity Engine Wiring Assessment

**Date:** 2025-12-03
**Status:** Partial Implementation - Many entities documented but not wired

---

## SUMMARY

**Total Entities Documented:** 31
**Entities Wired to Engine:** 5
**Wiring Completion:** ~16%

---

## ✅ WIRED AND FUNCTIONAL

### 1. **The Janitor** (`the-janitor`)
- **Files:**
  - `canon/entities/the-janitor.json` - QBIT metrics (power: 1478, charisma: 1308)
  - `src/ai/npc_llm/janitor_llm.py` - LLM dialogue system
  - `src/v7_integrated_demo.py` - MockJanitor class with rule-breaking logic
  - `src/contradiction_handler.py` - Contradiction detection
  - `src/test_janitor_contradiction_sequence.py` - Integration tests
- **Behavior:** Breaks rule at Cloud 70+, crosses into FC-ARCADE, triggers LLM dialogue
- **Engine Integration:** ✅ COMPLETE (Cloud, QBIT, LLM, contradiction system)
- **Visual Palette:** ✅ MAPPED (`JANITOR_UNIT7` - soft green jumpsuit, yellow tools)

### 2. **Wife (at Bookstore)** (`wife-at-bookstore`)
- **Files:**
  - `canon/entities/wife-at-bookstore.json` - QBIT metrics (power: 320, charisma: 1178)
  - `canon/npc_spines_v3_port.json` - Full dialogue spine (lines 918-987)
  - `src/contradiction_handler.py` - Reaction to Janitor breaking rule
  - `src/ai/npc_llm/wife_llm.py` - LLM hooks (EXISTS)
- **Behavior:** Silent browsing, contradiction magnet, reacts when Janitor enters FC-ARCADE
- **Engine Integration:** ⚠️ PARTIAL (QBIT defined, contradiction logic exists, LLM hooks stubbed but not used in demo)
- **Visual Palette:** ❌ NOT MAPPED (needs NPC color definition)

### 3. **Toddler** (reality catalyst)
- **Files:**
  - `src/ai/toddler/toddler_system.py` - Full behavioral system
  - `src/ai/toddler/toddler_behaviors.py` - 5 behavior states
  - `src/ai/toddler/toddler_config.py` - Configuration
  - `docs/TODDLER_V7_INTEGRATION.md` - Documentation
  - `src/v7_integrated_demo.py` - Live integration
- **Behavior:** Wandering, stalking, lurking, manifesting, approaching; amplifies Cloud 1.0x-3.0x
- **Engine Integration:** ✅ COMPLETE (Cloud amplification, reality strain, glitch multiplier)
- **Visual Palette:** ❌ NOT MAPPED (needs visual definition for voxel renderer)

### 4. **Leisurely Leon** (`leisurely-leon`)
- **Files:**
  - `canon/entities/leisurely-leon.json` - QBIT metrics
  - `src/cloud.py` - Referenced in adjacency weighting (line: "target": "leisurely-leon")
  - `src/qbit_engine.py` - Sample entity data
- **Behavior:** Undefined - appears in QBIT system but no behavior implementation
- **Engine Integration:** ⚠️ PARTIAL (QBIT metrics exist, referenced in adjacency, no NPC state machine)
- **Visual Palette:** ❌ NOT MAPPED

### 5. **Al-Gorithm** (`al-gorithm`)
- **Files:**
  - `canon/entities/al-gorithm.json` - Entity definition (EXISTS)
  - `src/ai/npc_llm/algoritmo_llm.py` - LLM dialogue system (EXISTS)
- **Behavior:** Undefined - LLM hooks exist but not integrated into demo
- **Engine Integration:** ⚠️ PARTIAL (Entity defined, LLM stub exists, not wired to Cloud/contradiction)
- **Visual Palette:** ❌ NOT MAPPED

---

## 📋 DOCUMENTED BUT NOT WIRED (26 entities)

### NPCs from `npc_spines_v3_port.json` (14 NPCs)

| NPC ID | Name | Home Zone | QBIT Overall | Wired? | Notes |
|--------|------|-----------|--------------|--------|-------|
| `milo` | Milo | OPTICS_SHOP | 1050 | ❌ | Full dialogue spine, no engine integration |
| `bored` | BORED | STORE_BORED | 2600 | ❌ | High QBIT, full dialogue, not in engine |
| `r0mba` | R0-MBA | SERVICE_HALL | 300 | ❌ | Robot, full dialogue spine |
| `mall_cop` | Mall Cop | SERVICE_HALL | 900 | ❌ | Full dialogue, not in engine |
| `generic_shopper_1` | Shopper | FOOD_COURT | 150 | ❌ | Background NPC |
| `generic_shopper_2` | Shopper | FOOD_COURT | 170 | ❌ | Background NPC |
| `fixer` | The Fixer | STORE_COMPHUT | 1200 | ❌ | CompHut tech, full dialogue |
| `flair` | Flair Warrior | STORE_FLAIR | 1050 | ❌ | Card shop worker |
| `barista` | Mermaid Barista | FOOD_COURT | 900 | ❌ | Coffee shop, full dialogue |
| `nurse` | Clinic Nurse | CLINIC | 1350 | ❌ | Medical clinic, full dialogue |
| `sporty` | Sporty's Manager | STORE_SPORTY | 1200 | ❌ | Sports store |
| `arcade` | Arcade Guy | STORE_HARD_COPY | 1000 | ❌ | Arcade attendant |
| `lostandfound` | Lost & Found Clerk | SERVICE_HALL | 900 | ❌ | Mall services |
| `wife-at-bookstore` | Wife | STORE_BORED | 1498 | ⚠️ | PARTIAL (contradictions defined, not in demo) |

**Visual Palette Status:**
- `MALL_WALKER` ✅ MAPPED (generic shopper colors)
- `SECURITY_GUARD` ✅ MAPPED (mall cop equivalent)
- All others ❌ NOT MAPPED

### Environmental Entities from `canon/entities/` (12 entities)

| Entity ID | Type | Wired? | Notes |
|-----------|------|--------|-------|
| `coca-cola-store` | Store | ❌ | Tile palette exists, not in zone system |
| `orange-julius-stand` | Store | ❌ | Tile palette exists, not in zone system |
| `escalator-hum` | Environmental | ❌ | Sound/atmosphere entity, not in audio |
| `food-court-neon-sign` | Environmental | ❌ | Documented in canon, not rendered |
| `sunken-food-court` | Zone | ⚠️ | In zone measurements, not as entity |
| `tensile-roof-mast` | Architectural | ⚠️ | In spatial measurements, not as entity |
| `mirror-maze-token` | Object | ❌ | Documented, not in object system |
| `kenny_bits` | NPC/Entity | ❌ | Undefined role |
| `BALES_CANONICAL` | Unknown | ❌ | JSON exists, purpose unclear |
| `BULL_MOVEMENT_AGENT` | System | ❌ | Music-weighted, not wired |
| `RUST_LOGIC_GRAPH` | System | ❌ | Graph data, not in engine |
| `world_spine_base` | System | ❌ | Base template, not instantiated |

**Visual Palette Status:**
- `STORE_COCA_COLA` ✅ MAPPED
- `STORE_ORANGE_JULIUS` ✅ MAPPED
- `FOOD_COURT_MAIN` ✅ MAPPED (includes neon)
- `ATRIUM_FOUNTAIN` ✅ MAPPED (includes masts)
- Others ❌ NOT DEFINED AS RENDERABLE

---

## 🔌 WIRING GAPS ANALYSIS

### Critical Missing Connections

**1. NPC State Machine → LLM Integration**
- `wife_llm.py` exists but not called in `v7_integrated_demo.py`
- `algoritmo_llm.py` exists but not called anywhere
- Only `janitor_llm.py` is actively wired

**2. Entity Canon → Zone System**
- Stores defined in canon but not instantiated in zones
- No store placement system in voxel builder
- Tile palettes exist but no entity→tile mapping logic

**3. QBIT Scores → NPC Behavior**
- 14 NPCs have QBIT scores defined
- Only Janitor + Wife use QBIT for contradiction thresholds
- No QBIT-weighted NPC spawning/positioning

**4. Dialogue Spines → Cloud States**
- 14 NPCs have full dialogue trees (calm/uneasy/strained/critical)
- No dialogue delivery system beyond Janitor
- No generic NPC dialogue engine

**5. Visual Palette → Render System**
- NPC colors defined (3/14 NPCs)
- No voxel renderer to consume palette
- No NPC sprite/voxel generation system

---

## 🎯 RECOMMENDATIONS

### Phase 1: Wire Existing NPCs (Immediate)
1. **Add Wife to integrated demo**
   - Use `wife_llm.py` when Janitor breaks rule
   - Test contradiction magnet behavior
   - Verify Cloud-driven reactions

2. **Add generic NPC system**
   - Use MALL_WALKER palette
   - Simple Cloud-driven dialogue from spines
   - Milo or BORED as test case (high QBIT, good dialogue)

3. **Wire Al-Gorithm**
   - Use existing `algoritmo_llm.py`
   - Trigger at Cloud 80+ (pattern recognition dialogue)

### Phase 2: Store Placement (Short-term)
1. **Integrate store entities into zones**
   - Coca-Cola → Z3_LOWER_RING
   - Orange Julius → Z4_FOOD_COURT
   - CompHut → Z2_UPPER_RING
   - Milo Optics → Z2_UPPER_RING

2. **Create store tile rendering**
   - Use existing tile palette definitions
   - Map store positions in voxel builder

### Phase 3: Full NPC Population (Medium-term)
1. **Implement 14 dialogue NPCs**
   - Create generic dialogue engine
   - Use Cloud states to select dialogue tier
   - Position NPCs in home zones

2. **Create NPC visual system**
   - Define remaining 11 NPC palettes
   - Generate voxel sprites from palette
   - Animate based on state (idle/alert/contradiction)

### Phase 4: Environmental Entities (Long-term)
1. **Sound entities** (escalator-hum, etc.)
2. **Interactive objects** (mirror-maze-token, etc.)
3. **System entities** (BULL_MOVEMENT_AGENT, etc.)

---

## ⚠️ BLOCKING ISSUES

1. **No Visual Renderer:** Palette mappings exist, but no voxel renderer to display them
2. **No Zone Placement System:** Stores/NPCs defined but no spawn coordinates
3. **No Dialogue Engine:** 14 NPCs have dialogue trees but no generic delivery system
4. **No Audio System:** Sound entities documented but no audio integration

---

## 💡 QUICK WINS

These can be wired TODAY with minimal work:

1. **Wife in Demo** (30 min)
   - Import wife_llm in v7_integrated_demo.py
   - Call when Janitor enters FC-ARCADE
   - Test contradiction cascade

2. **Milo Dialogue Test** (1 hour)
   - Create MockMilo class
   - Use Cloud states to select dialogue from spine
   - Print to console (no LLM needed, use existing lines)

3. **Store Tile Test** (1 hour)
   - Add Coca-Cola store to voxel_builder.py
   - Use STORE_COCA_COLA palette
   - Generate test voxel mesh

---

**Next Steps:**
- Pick a quick win to test entity→engine pipeline
- Document wiring pattern for future entities
- Create entity instantiation template

**Question:** Which entity should we wire next? Wife (completes Janitor contradiction loop) or Milo (tests generic NPC dialogue)?
