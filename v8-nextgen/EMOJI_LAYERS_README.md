# Emoji Layers - Voxel Semantic Encoding

## Multi-Layer Meaning System for Voxels

Instead of text labels, voxels have **emoji-encoded properties** across multiple semantic layers.

---

## Layer Types

### 1. **MATERIAL Layer** (What is it made of?)
```
🧱 BRICK          💎 GLASS          🟫 WOOD
🌳 WOOD_NATURAL   ⬛ CONCRETE       🟨 METAL_STEEL
⬜ TILE_WHITE     🟧 TERRACOTTA     🟥 CARPET_RED
💧 WATER          🪟 GLASS_BLOCK    🚪 DOOR_MATERIAL
```

### 2. **STATE Layer** (What condition is it in?)
```
🔥 HOT            ❄️ COLD           💧 WET
⚡ POWERED        ✨ PRISTINE        💩 DIRTY
🦠 CONTAMINATED   💔 BROKEN          🕐 ACTIVE
```

### 3. **BEHAVIOR Layer** (What does it do?)
```
🚪 DOOR           🪜 CLIMBABLE       🛏️ SLEEPABLE
💡 LIGHT_SOURCE   🔒 SOLID           🌬️ PASSABLE
⬆️ FLOATS         ⬇️ SINKS           🪙 COLLECTIBLE
```

### 4. **SURFACE Layer** (How does it look?)
```
✨ SHINY          🌟 SPARKLY         💫 GLITTERY
🪞 MIRROR         💎 REFLECTIVE      🌑 MATTE
🎨 PAINTED        🌈 RAINBOW         💧 DROPLETS
```

### 5. **AUDIO Layer** (What does it sound like?)
```
🔇 SILENT         🔊 LOUD            🎵 MUSICAL
⚙️ MECHANICAL_HUM 🌊 FLOWING_WATER   🔔 CHIME
🌬️ WIND           👻 EERIE
```

### 6. **PHYSICS Layer** (Physical properties)
```
🪨 HEAVY          🪶 LIGHT           💨 WEIGHTLESS
🧲 MAGNETIC       🧊 SLIPPERY        🍯 STICKY
🏃 FAST           🐌 SLOW            🌀 SPINNING
```

---

## Compact Encoding

Each voxel concatenates its layer emoji into a compact string:

**Example: Glass Block Voxel**
```
🪟✨🔒💎🧊

Material:  🪟 (GLASS_BLOCK)
State:     ✨ (PRISTINE)
Behavior:  🔒 (SOLID)
Surface:   💎 (REFLECTIVE)
Physics:   🧊 (SLIPPERY)
```

**Example: Escalator Step**
```
🟨🕐⬇️🌓⚙️🏃

Material:  🟨 (METAL_STEEL)
State:     🕐 (ACTIVE)
Behavior:  ⬇️ (Moving down)
Surface:   🌓 (SEMI_GLOSS)
Audio:     ⚙️ (MECHANICAL_HUM)
Physics:   🏃 (FAST)
```

**Example: Fountain Water**
```
💧💦🌬️🌊🌊⬇️

Material:  💧 (WATER)
State:     💦 (DRIPPING)
Behavior:  🌬️ (PASSABLE)
Surface:   🌊 (RIPPLES)
Audio:     🌊 (FLOWING_WATER)
Physics:   ⬇️ (SINKS)
```

---

## Generated Voxels

**File Structure:**
```
renpy_output/game/
├── voxels/
│   ├── z1_central_atrium_voxels.rpy      (60 voxels)
│   ├── z4_food_court_voxels.rpy          (2,811 voxels)
│   └── z5_escalator_wells_voxels.rpy     (48 voxels)
└── geojson/zones/
    ├── z1_central_atrium_voxels.geojson
    ├── z4_food_court_voxels.geojson
    └── z5_escalator_wells_voxels.geojson

TOTAL: 2,919 voxels
```

---

## Ren'Py Format

**Voxel Definition:**
```renpy
# Voxel: Z5_ESCALATOR_WELLS_VOXEL_0000
# Emoji layers: 🟨🕐⬇️🌓⚙️🏃

define voxel_z5_escalator_wells_voxel_0000 = {
    "position": [-2, -80.0, 0.0],
    "emoji_compact": "🟨🕐⬇️🌓⚙️🏃",
    "layers": {
        "material": { "emoji": "🟨", "name": "METAL_STEEL" },
        "state": { "emoji": "🕐", "name": "ACTIVE" },
        "behavior": { "emoji": "⬇️", "name": "SINKS" },
        "surface": { "emoji": "🌓", "name": "SEMI_GLOSS" },
        "audio": { "emoji": "⚙️", "name": "MECHANICAL_HUM" },
        "physics": { "emoji": "🏃", "name": "FAST" },
    }
}
```

---

## GeoJSON Format

```json
{
  "type": "Feature",
  "id": "Z5_ESCALATOR_WELLS_VOXEL_0000",
  "geometry": {
    "type": "Point",
    "coordinates": [-2, -80.0, 0.0]
  },
  "properties": {
    "voxel_id": "Z5_ESCALATOR_WELLS_VOXEL_0000",
    "emoji_compact": "🟨🕐⬇️🌓⚙️🏃",
    "material": { "emoji": "🟨", "name": "METAL_STEEL" },
    "state": { "emoji": "🕐", "name": "ACTIVE" },
    "behavior": { "emoji": "⬇️", "name": "SINKS" },
    "surface": { "emoji": "🌓", "name": "SEMI_GLOSS" },
    "audio": { "emoji": "⚙️", "name": "MECHANICAL_HUM" },
    "physics": { "emoji": "🏃", "name": "FAST" }
  }
}
```

---

## Mall-Specific Voxel Examples

### Central Atrium (Z1)
- **Fountain tiers** (4 levels): `💧🌊🌬️🌊🌊⬇️`
- **Yellow lattice masts** (70 feet): `🟨✨🔒🎨🌬️🪨`
- **Tensile cables** (32 radial): `🟨⚡🔒🌓🔔🧲`

### Food Court (Z4)
- **Floor tiles** (terracotta): `🟫💩🔒🌑🐌`
- **FOOD COURT neon sign**: `🪟⚡💡🌟📻🪶`
- **Theater entrance** (void): `🔲💀🚪🌑👻🌬️`

### Escalator Wells (Z5)
- **Escalator steps**: `🟨🕐⬇️🌓⚙️🏃`
- **Handrails**: `⬛🕐⬆️🌑⚙️🍯`

---

## Measurement Verification

All voxels use **verified measurements** from CRD + user confirmation:

**Escalator (SOURCE OF TRUTH):**
```
12 steps × 8 inches = 8 feet drop
Risers: 7-8 inches ✓
Tread depth: 18-22 inches
Width: 24-34 inches average
```

**Positions in feet:**
- Z1 Atrium: Elevation 0
- Z4 Food Court: Elevation -8 feet (escalator drop)
- Z5 Escalator: Gradient from 0 to -8 feet

---

## Benefits

### 1. Semantic Compression
- `🟨🕐⬇️🌓⚙️🏃` = Full voxel description
- No text labels needed
- Language-independent

### 2. Visual Pattern Recognition
- Quick scanning: `💎✨🔒` vs `GLASS_PRISTINE_SOLID`
- Immediate meaning from symbols
- Git-friendly diffs

### 3. Composable Layers
- Mix and match emoji for new combinations
- `🔥` + `💧` = Steam voxel
- `💡` + `💔` = Broken light

### 4. Query-Friendly
```python
# Find all wet voxels
wet_voxels = [v for v in voxels if '💧' in v.to_compact()]

# Find all light sources
lights = [v for v in voxels if v.behavior == '💡']

# Find heavy metal objects
heavy_metal = [v for v in voxels if v.material == '🟨' and v.physics == '🪨']
```

---

## Deep Space Probe Analogy

| Layer | Probe Equivalent |
|-------|------------------|
| Material | Sensor material (silicon, metal) |
| State | Component status (active, standby) |
| Behavior | Function (transmitter, sensor) |
| Surface | Coating (reflective, ablative) |
| Audio | Telemetry tone |
| Physics | Mass, trajectory |

Same encoding philosophy: **Compact, symbolic, semantic compression**

---

## Usage

### Python API
```python
from voxel_emoji_layers import VoxelLayers

# Create a voxel
voxel = VoxelLayers(
    position=(10, 20, 0),
    material='💎',
    state='💧',
    behavior='💡',
    surface='✨'
)

# Get compact encoding
print(voxel.to_compact())  # "💎💧💡✨"

# Export to Ren'Py
renpy_code = voxel_to_renpy_define(voxel, "GLASS_001")

# Export to GeoJSON
geojson = voxel_to_geojson_feature(voxel, "GLASS_001")
```

### Ren'Py Integration
```renpy
# Load voxel definitions
init python:
    from voxel_emoji_layers import VoxelLayers

# Display voxel
screen show_voxel(voxel_id):
    python:
        voxel = voxel_registry[voxel_id]
        layers = voxel["layers"]

    text "[voxel['emoji_compact']]" size 48
    text "Material: [layers['material']['name']]"
    text "State: [layers['state']['name']]"
```

---

## Future Extensions

### Dynamic Layers
- Weather effects: `🌧️` (raining), `☀️` (sunny)
- Time of day: `🌅` (dawn), `🌙` (night)
- Player proximity: `👁️` (observed), `🙈` (hidden)

### Compound Effects
- Wet + Cold = `💧❄️` (ice)
- Hot + Metal = `🔥🟨` (molten)
- Light + Water = `💡💧` (refraction)

### Animation Sequences
```python
# Flickering neon sign
states = ['⚡💡', '⚡🌑', '⚡💡', '⚡🌑']  # On/off cycle

# Dripping water
states = ['💧', '💦', '🌊']  # Drop formation → splash
```

---

## Philosophy

**Wingdings principle applied to voxel properties:**

Instead of:
```json
{
  "material": "glass",
  "state": "pristine",
  "behavior": "solid",
  "surface": "reflective"
}
```

Use:
```
🪟✨🔒💎
```

**Same information, symbolic encoding, visual immediacy.**

Emoji layers = **semantic compression through universal symbols**.
