# MallOS Symbology Dictionary
## Master Reference for All Symbol Meanings

**Last Updated:** 2025-12-07
**Version:** 1.0
**Purpose:** Canonical reference for all symbols used in GLITCHDEXMALL v8-nextgen

---

## 📖 Table of Contents

1. [Entity Symbols](#entity-symbols) - Primary identifiers for things
2. [Voxel Layer Symbols](#voxel-layer-symbols) - Multi-layer voxel encoding
3. [Symbol Stacking](#symbol-stacking) - Hierarchical composition
4. [QBIT Dimensions](#qbit-dimensions) - Behavioral axes
5. [Law Codes](#law-codes) - Legislative prefix system
6. [Zone Codes](#zone-codes) - Spatial designations

---

## 1. Entity Symbols
### Primary Identifiers (Wingdings System)

### 🧰 Items (Voxel Objects)
| Symbol | Name | Description |
|--------|------|-------------|
| 🧹 | JANITOR_MOP | Unit 7's signature tool |
| 🍕 | PIZZA_SLICE | Food court consumable |
| 🥤 | SLURPEE_CUP | Orange Julius/slushee drink |
| 🪙 | ARCADE_TOKEN | Currency for arcade machines |
| 🗑️ | TRASH_CAN | Waste receptacle |
| 🔑 | MASTER_KEY | Access control item |
| 📺 | SECURITY_MONITOR | Surveillance display |
| 🛒 | SHOPPING_CART | Retail vehicle |
| 🎮 | ARCADE_CABINET | Game machine |
| 💡 | NEON_SIGN_FRAGMENT | Broken signage piece |

### 👥 NPCs (Characters)
| Symbol | Name | Role |
|--------|------|------|
| 🧑‍🔧 | UNIT_7_JANITOR | The Janitor (primary protagonist) |
| 👔 | AL_GORITHM | Algorithm-driven entity |
| 👗 | WIFE_AT_BOOKSTORE | Narrative character |
| 🧒 | LEISURELY_LEON | Young patron |
| 🐂 | BULL_MOVEMENT_AGENT | Musical weighting entity |
| 👨‍💼 | KENNY_BITS | Business character |
| 🧓 | BALES_CANONICAL | Elder figure |
| 👻 | ESCALATOR_HUM | Ambient presence |
| 🎭 | THEATER_GHOST | Theatrical entity |

### 🗺️ Zones (Spatial Areas)
| Symbol | Zone ID | Name | Scale |
|--------|---------|------|-------|
| 🎪 | Z1 | CENTRAL_ATRIUM | 175' diameter |
| 🏛️ | Z2 | UPPER_RING | Second floor |
| 🛤️ | Z3 | LOWER_RING | First floor |
| 🍽️ | Z4 | FOOD_COURT | 120' diameter, -8' elevation |
| ⬆️ | Z5 | ESCALATOR_WELLS | Vertical circulation |
| 🏬 | Z5 | ANCHOR_STORES | 100k+ sq ft each |
| 🍔 | Z6 | MICKEYS_WING | Restaurant wing |
| 🎬 | Z6 | THEATER | Cinema complex |
| 🔻 | Z7 | SUBTERRANEAN | Underground (placeholder) |
| 🌐 | Z9 | EXTERIOR | Parking/outdoors |

### 🏗️ Features (Architectural Elements)
| Symbol | Name | Measurement |
|--------|------|-------------|
| ⛲ | FOUNTAIN_TERRACED | 4 tiers, 6' total depth |
| 🟨 | TENSILE_MAST | 70' tall yellow lattice |
| 🕸️ | CABLE_ARRAY | 32 radial cables |
| 🧱 | GLASS_BLOCK_WALL | Translucent barrier |
| 🚡 | ESCALATOR_PAIR | 12 steps, 8' drop |
| 🚪 | ELEVATOR_DOORS | 3.5' × 6.75' |
| 💎 | GLASS_ELEVATOR_TOWER | Transparent shaft |
| 🔵 | METAL_RAILING_BLUE | Blue powder-coat |
| 🟢 | METAL_RAILING_GREEN | Green powder-coat |
| 🟫 | TERRACOTTA_SCALLOP | Decorative element |

---

## 2. Voxel Layer Symbols
### Multi-Layer Semantic Encoding

Voxels are encoded as concatenated emoji strings: `🪟✨🔒💎🧊`

Each layer describes a different property:

### Layer 1: MATERIAL (What is it made of?)
| Symbol | Name | Physical Properties |
|--------|------|-------------------|
| 🧱 | BRICK | Masonry, porous |
| 💎 | GLASS | Transparent, brittle |
| 🟫 | WOOD | Organic, combustible |
| 🌳 | WOOD_NATURAL | Unfinished wood |
| ⬛ | CONCRETE | Dense, durable |
| 🟨 | METAL_STEEL | Conductive, strong |
| ⬜ | TILE_WHITE | Ceramic, smooth |
| 🟧 | TERRACOTTA | Clay, textured |
| 🟥 | CARPET_RED | Soft, absorbent |
| 💧 | WATER | Liquid, flowing |
| 🪟 | GLASS_BLOCK | Translucent blocks |
| 🚪 | DOOR_MATERIAL | Variable (depends on door type) |

### Layer 2: STATE (What condition is it in?)
| Symbol | Name | Meaning |
|--------|------|---------|
| 🔥 | HOT | Above ambient temperature |
| ❄️ | COLD | Below ambient temperature |
| 💧 | WET | Moisture present |
| ⚡ | POWERED | Electrically active |
| ✨ | PRISTINE | New/clean condition |
| 💩 | DIRTY | Soiled/degraded |
| 🦠 | CONTAMINATED | Biohazard/unsafe |
| 💔 | BROKEN | Non-functional |
| 🕐 | ACTIVE | Currently operating |

### Layer 3: BEHAVIOR (What does it do?)
| Symbol | Name | Function |
|--------|------|----------|
| 🚪 | DOOR | Opens/closes |
| 🪜 | CLIMBABLE | Can be scaled |
| 🛏️ | SLEEPABLE | Rest point |
| 💡 | LIGHT_SOURCE | Emits illumination |
| 🔒 | SOLID | Blocks movement |
| 🌬️ | PASSABLE | Can walk through |
| ⬆️ | FLOATS | Rises in fluid |
| ⬇️ | SINKS | Descends in fluid |
| 🪙 | COLLECTIBLE | Can be picked up |

### Layer 4: SURFACE (How does it look?)
| Symbol | Name | Visual Quality |
|--------|------|---------------|
| ✨ | SHINY | High gloss |
| 🌟 | SPARKLY | Glittering |
| 💫 | GLITTERY | Reflective particles |
| 🪞 | MIRROR | Perfect reflection |
| 💎 | REFLECTIVE | Partial reflection |
| 🌑 | MATTE | Non-reflective |
| 🌓 | SEMI_GLOSS | Moderate sheen |
| 🎨 | PAINTED | Coated surface |
| 🌈 | RAINBOW | Multi-color |
| 💧 | DROPLETS | Wet appearance |

### Layer 5: AUDIO (What does it sound like?)
| Symbol | Name | Sound Character |
|--------|------|----------------|
| 🔇 | SILENT | No noise |
| 🔊 | LOUD | High volume |
| 🎵 | MUSICAL | Tonal |
| ⚙️ | MECHANICAL_HUM | Machine noise |
| 🌊 | FLOWING_WATER | Liquid sound |
| 🔔 | CHIME | Bell-like |
| 🌬️ | WIND | Air movement |
| 👻 | EERIE | Unsettling |
| 📻 | BUZZING | Electronic hum |

### Layer 6: PHYSICS (Physical properties)
| Symbol | Name | Behavior |
|--------|------|----------|
| 🪨 | HEAVY | High mass |
| 🪶 | LIGHT | Low mass |
| 💨 | WEIGHTLESS | Negligible mass |
| 🧲 | MAGNETIC | Ferromagnetic |
| 🧊 | SLIPPERY | Low friction |
| 🍯 | STICKY | High adhesion |
| 🏃 | FAST | High velocity |
| 🐌 | SLOW | Low velocity |
| 🌀 | SPINNING | Rotational motion |

### Example Voxel Encodings

**Glass Block:**
```
🪟✨🔒💎🧊
Material: GLASS_BLOCK
State: PRISTINE
Behavior: SOLID
Surface: REFLECTIVE
Physics: SLIPPERY
```

**Escalator Step:**
```
🟨🕐⬇️🌓⚙️🏃
Material: METAL_STEEL
State: ACTIVE
Behavior: SINKS (moving down)
Surface: SEMI_GLOSS
Audio: MECHANICAL_HUM
Physics: FAST
```

**Fountain Water:**
```
💧💦🌬️🌊🌊⬇️
Material: WATER
State: WET/DRIPPING
Behavior: PASSABLE
Surface: RIPPLES
Audio: FLOWING_WATER
Physics: SINKS
```

---

## 3. Symbol Stacking
### Hierarchical Composition System

Stacking creates context: `🏬🍽️🍕` = Mall → Food Court → Pizza

| Level | Pattern | Example | Meaning |
|-------|---------|---------|---------|
| 0 | Single | 🏬 | Mall (root) |
| 1 | Two | 🏬🍽️ | Mall → Food Court |
| 2 | Three | 🏬🍽️🍕 | Mall → Food Court → Pizza |
| 3+ | N-deep | 🏬🍽️🍕🔥 | Mall → Food Court → Pizza → Hot |

**Analogies:**
- File paths: `/mall/food_court/pizza`
- DNS: `pizza.food_court.mall`
- Probe subsystems: `MALL.FOODCOURT.PIZZA`

**Common Stacks:**
```
🏬🍽️🍕     = Pizza in Food Court
🏬🍽️🥤     = Slurpee in Food Court
🏬🍽️⬆️     = Escalator to Food Court
🏬🧑‍🔧🧹    = Janitor's mop in Service Area
🏬🎬🎭     = Theater Ghost in Cinema
```

---

## 4. QBIT Dimensions
### Behavioral Axes

| Dimension | Symbol | Range | Meaning |
|-----------|--------|-------|---------|
| **Heat** | 🌡️ | 0.0-1.0 | Activity/chaos level |
| **Debt** | 💰 | 0.0-1.0 | Economic pressure |
| **Coherence** | 🧩 | 0.0-1.0 | Order/consistency |
| **Gravity** | ⚓ | 0.0-1.0 | Institutional pull |
| **Resonance** | 🔔 | 0.0-1.0 | Alignment strength |

**QBIT Vector Example:**
```json
{
  "heat": 0.7,        // High activity
  "debt": 0.4,        // Moderate pressure
  "coherence": 0.6,   // Some order
  "gravity": 0.5,     // Neutral institutional
  "resonance": 0.8    // Strong alignment
}
```

---

## 5. Law Codes
### Legislative Prefix System

| Prefix | Category | Example |
|--------|----------|---------|
| **LC_** | Law Code | LC_0231 (Food Court Curfew) |
| **RC_** | Regulation Code | RC_0045 (Smoking Ban) |
| **EC_** | Emergency Code | EC_0001 (Fire Evacuation) |
| **TC_** | Temporary Code | TC_0099 (Holiday Hours) |

**Law ID Format:** `PREFIX_NNNN`
- PREFIX: Category (LC, RC, EC, TC)
- NNNN: Sequential number (0001-9999)

**Example Laws:**
```
LC_0231 - Food Court Curfew
LC_0145 - Central Atrium Free Speech Zone
LC_0089 - Mickey's Wing Smoking Ban
```

---

## 6. Zone Codes
### Spatial Designation System

| Code | Name | Emoji | Area (sq ft) | Elevation |
|------|------|-------|-------------|-----------|
| **Z1** | Central Atrium | 🎪 | ~24,000 | 0' |
| **Z2** | Upper Ring | 🏛️ | ~300,000 | +12' |
| **Z3** | Lower Ring | 🛤️ | ~300,000 | 0' |
| **Z4** | Food Court | 🍽️ | ~11,000 | -8' |
| **Z5** | Escalator Wells | ⬆️ | ~2,000 | 0' to -8' |
| **Z5** | Anchor Stores | 🏬 | ~200,000 | Variable |
| **Z6** | Mickey's Wing | 🍔 | ~15,000 | 0' |
| **Z6** | Theater | 🎬 | ~25,000 | 0' |
| **Z7** | Subterranean | 🔻 | Unknown | <-8' |
| **Z9** | Exterior | 🌐 | ~500,000 | 0' |

---

## 7. Measurement Symbols
### CRD Reference Anchors

| Symbol | Reference | Measurement | Confidence |
|--------|-----------|-------------|------------|
| 📏 | MEASUREMENT | Generic marker | - |
| ⬆️📏 | ESCALATOR | 8' drop (12 steps × 8") | HIGH |
| 🚪📏 | ELEVATOR | 3.5' × 6.75' | HIGH |
| ⛲📏 | FOUNTAIN | 4 tiers, 6' depth | MEDIUM |
| 🎪📏 | ATRIUM | 175' diameter | MEDIUM |
| 🟨📏 | MAST | 70' tall | MEDIUM |

---

## 8. Cloud Moods
### Environmental State Symbols

| Symbol | Mood | Heat | Coherence | Description |
|--------|------|------|-----------|-------------|
| ⚡ | TENSION | High | Low | Chaotic energy |
| 🌊 | WANDER | Low | Low | Aimless drift |
| 🔥 | SURGE | High | High | Intense focus |
| 💧 | BLEED | Low | High | Cold precision |

---

## 9. Era Symbols
### Timeline Designations

| Symbol | Year | Era | Condition |
|--------|------|-----|-----------|
| 🌅 | 1981 | OPENING | Pristine, optimistic |
| ☀️ | 1995 | PEAK | Bustling, thriving |
| 🌤️ | 2005 | DECLINE | Vacant, flickering |
| 🌑 | 2011 | CLOSURE | Abandoned, eerie |

---

## 10. Credit Card Weapons
### The Three Cards

| Symbol | Name | Type | Ability |
|--------|------|------|---------|
| 💳 | VISA_BLUE | Physical | Melee swipe |
| 💎 | AMEX_PLATINUM | Energy | Projectile blast |
| 🔥 | DISCOVER_ORANGE | AOE | Area explosion |

---

## Symbol Composition Rules

### Rule 1: Hierarchy Matters
- `🏬🍕` ≠ `🍕🏬`
- Left-to-right = root-to-leaf
- Most general → most specific

### Rule 2: Layers Are Positional
- Position 1 = Material
- Position 2 = State
- Position 3 = Behavior
- Position 4 = Surface
- Position 5 = Audio
- Position 6 = Physics

### Rule 3: Context Inference
- Single symbol: generic meaning
- Stacked symbols: contextual meaning
- `🍕` = pizza (generic)
- `🏬🍽️🍕` = pizza in mall food court (specific)

### Rule 4: Emoji as IDs
- Symbols are primary keys
- Human names are secondary
- `🧹` → `JANITOR_MOP` (lookup)
- Never the reverse

---

## Quick Reference Tables

### Most Common Symbols
| Symbol | Use | Frequency |
|--------|-----|-----------|
| 🏬 | Mall root | Very High |
| 🍽️ | Food Court | High |
| 🧹 | Janitor/cleaning | High |
| 💧 | Water/wet | High |
| 🟨 | Metal/yellow | High |
| ✨ | Pristine/clean | High |
| 🔒 | Solid/locked | High |

### Measurement Anchors (High Confidence)
1. **Escalator drop:** 8 feet (12 steps × 8")
2. **Elevator doors:** 3.5' × 6.75'
3. **Fountain tiers:** 4 levels
4. **Tensile cables:** 32 radial

### Zone Adjacency Emoji
```
🎪 (Z1 Atrium) ← connects to → 🍽️ (Z4 Food Court) via ⬆️ (Z5 Escalator)
🏛️ (Z2 Upper) ← stacks above → 🛤️ (Z3 Lower)
🍔 (Z6 Mickey's) ← exterior wing → 🎬 (Z6 Theater)
```

---

## Usage Examples

### AI Constructor Query
```python
# What symbols apply to this zone?
zone_laws = constitution.filter_by_zone("ZONE:FOOD_COURT")
zone_symbol = name_to_symbol("Z4_FOOD_COURT")  # 🍽️

# What are the voxel properties here?
voxel = VoxelLayers(
    position=(10, -120, -8),
    material='🟫',  # Terracotta
    state='💩',     # Dirty
    behavior='🔒',  # Solid
    surface='🌑'    # Matte
)
compact = voxel.to_compact()  # "🟫💩🔒🌑"
```

### Governor Interpretation
```markdown
LAW: LC_0231 (🏬🍽️⏰)
Symbol Stack: Mall → Food Court → Curfew
Interpretation Radius: 0.60
QBIT weights: 🌡️-0.4, 🧩+0.3
```

### Voxel Builder
```python
# Build escalator voxels
for step in range(12):
    voxel = create_voxel(
        material='🟨',      # Metal
        state='🕐',        # Active
        behavior='⬇️',     # Moving down
        audio='⚙️',        # Mechanical hum
        physics='🏃'       # Fast
    )
```

---

## Symbol Evolution Log

### Version 1.0 (2025-12-07)
- Initial consolidation of three systems
- 60+ entity symbols defined
- 50+ voxel layer symbols defined
- QBIT dimensions formalized
- Law code prefixes established

### Future Additions
- Weather symbols (🌧️, ☀️, 🌨️)
- Time-of-day symbols (🌅, 🌙)
- Player state symbols (👁️, 🙈)
- Dynamic effect combinations

---

## Philosophy

**Wingdings Principle:**
Symbols are primary identifiers, not decorations.

**Semantic Compression:**
`🪟✨🔒💎🧊` > `{"material":"glass_block", "state":"pristine", ...}`

**Visual Immediacy:**
Recognition over reading. Scan don't parse.

**Deep Space Probe Analogy:**
Compact telemetry. Symbol stacks = subsystem IDs.

---

**This is the living dictionary. All symbol meanings, one place.**
