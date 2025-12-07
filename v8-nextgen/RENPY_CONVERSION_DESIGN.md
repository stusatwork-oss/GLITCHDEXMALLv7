# Ren'Py Conversion Architecture - v8 NextGen
## Python Script to Ren'Py Primitives Conversion

**Date:** 2025-12-07
**Version:** 1.0.0
**Status:** Design Specification

---

## Executive Summary

This document outlines the conversion of v8-nextgen Python voxel systems to Ren'Py visual novel primitives, using **escalator/elevator measurements as the single source of truth** and implementing a **wingdings-style microencoding** approach for compact voxel representation.

---

## Part 1: Measurement Anchors (Source of Truth)

### Primary Measurement Standards

From `v8-nextgen/data/measurements/`:

**1. ESCALATOR STAIRS (Z5_ESCALATOR_WELLS)**
```
12 steps × 8 inches per step = 96 inches = 8 feet
Confidence: HIGH
Source: Verified via photo evidence
```

**2. ELEVATOR DOORS (Standard Commercial)**
```
Width:  42-48 inches (3.5-4.0 feet)
Height: 80-84 inches (6.67-7.0 feet)
Confidence: INDUSTRY STANDARD
```

### Derived Spatial Scale

All v8 measurements derive from these anchors:
- Atrium diameter: 175 feet (scale factor 2.5 from v5)
- Food court pit depth: **8 feet** (escalator measurement)
- Mast height: 70 feet (scale factor 2.0)
- Corridor width: 18-25 feet

**Critical Rule:** All Ren'Py conversions MUST preserve these ratios.

---

## Part 2: Wingdings-Style Microencoding

### Encoding Philosophy

Instead of storing full PNG heightmap data, we use **Unicode block drawing characters** to represent voxel states in a compact, human-readable format.

### Character Set Definition

#### Level 1: Block Drawing (8 symbols)
```
█ = Solid voxel (100% filled)
▓ = Dense material (75% filled)
▒ = Medium material (50% filled)
░ = Light material (25% filled)
▄ = Bottom half
▀ = Top half
▌ = Left half
▐ = Right half
```

#### Level 2: Braille Patterns (256 combinations)
```
Braille Unicode Range: U+2800 - U+28FF
Each character represents a 2×4 grid of dots
Example: ⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉...⣿

Use for high-density micro-voxel encoding
```

#### Level 3: Material Symbols (Custom Palette)
```
Material ID  → Symbol
---------------------------
TILE_WHITE   → ⬜
TILE_BROWN   → 🟫
CARPET_RED   → 🟥
GLASS_BLOCK  → 💎
CONCRETE     → ⬛
METAL_RAIL   → 🔵
NEON_SIGN    → 💡
WATER        → 💧
```

### Run-Length Encoding (RLE)

For repetitive patterns:
```
Format: {symbol}{count}

Example:
  Full notation:  ████████████████
  RLE notation:   █16

  Full notation:  ░░░░▓▓░░░░
  RLE notation:   ░4▓2░4
```

### Composite Encoding Format

```
VoxelLine ::= MaterialCode + DensityPattern + RLE_Count

Example:
  "TILE_WHITE:█8" = 8 solid white tiles
  "CARPET_RED:░4▓2░4" = red carpet with density variation
  "GLASS_BLOCK:⣿12" = 12 braille-encoded glass blocks
```

---

## Part 3: Ren'Py Primitive Mapping

### 3.1 Core Ren'Py Components

#### Image Definitions
```renpy
# Traditional approach (NOT used - too large)
image voxel_janitor_mop = "assets/voxel_sources/janitor_mop.png"

# Microencoded approach (USED)
define voxel_janitor_mop = VoxelMicroSprite(
    encoding="METAL_RAIL:▓4█2▓4 / METAL_RAIL:▓4█2▓4 / WOOD_HANDLE:█1⬛1█1",
    dimensions=(3, 3, 8),
    qbit={"power": 500, "charisma": 100, "resonance": 80}
)
```

#### Screen Language
```renpy
screen voxel_object_display(obj_id):
    frame:
        align (0.5, 0.5)

        # Decode microencoding on-the-fly
        python:
            voxel_data = decode_microencoding(obj_id)
            render_layers = build_render_layers(voxel_data)

        # Layer composite rendering
        for layer in render_layers:
            add layer.sprite pos layer.offset
```

#### Python Blocks
```renpy
init python:
    class VoxelMicroSprite:
        """Ren'Py compatible voxel object using microencoding."""

        def __init__(self, encoding, dimensions, qbit):
            self.encoding = encoding  # Wingdings-style string
            self.dimensions = dimensions  # (width, height, depth_feet)
            self.qbit = qbit
            self._cache = None

        def decode(self):
            """Lazy decode microencoding to render data."""
            if self._cache is None:
                self._cache = decode_voxel_microencoding(self.encoding)
            return self._cache

        def get_qbit_aggregate(self):
            return sum(self.qbit.values())
```

### 3.2 Loader Integration

The Python `voxel_object_loader.py` must be wrapped for Ren'Py:

```renpy
init python:
    import sys
    sys.path.append("src")

    from voxel_object_loader import VoxelObjectRegistry, build_voxels_from_png
    from measurements_loader import MeasurementsLoader

    # Initialize with Ren'Py compatibility layer
    ml = MeasurementsLoader()

    # CRITICAL: Respect existing loader architecture
    voxel_registry = VoxelObjectRegistry(
        base_path="data/voxel_objects",
        palette=COMICBOOK_MALL_V1_PALETTE,
        png_to_vox_fn=build_voxels_from_png_microencoded  # Modified version
    )

    def build_voxels_from_png_microencoded(image_path, palette, **kwargs):
        """
        Wrapper that converts PNG to microencoding instead of full mesh.
        Preserves VoxelObjectRegistry contract.
        """
        # 1. Load PNG using existing decoder
        _, _, pixels = _decode_png_rgba(image_path)

        # 2. Convert to microencoding
        encoding_lines = []
        for row in pixels:
            line_encoding = compress_row_to_microencoding(row, palette)
            encoding_lines.append(line_encoding)

        # 3. Return compatible structure
        return {
            "version": "voxel-microencoding-1.0",
            "encoding": " / ".join(encoding_lines),  # "/" separates rows
            "dimensions": (len(pixels[0]), len(pixels), kwargs.get('height', 8.0)),
            "original_source": str(image_path)
        }
```

---

## Part 4: Conversion Workflow

### Step 1: Analyze Existing Python Scripts

Target files for conversion:
- `src/measurements_loader.py` → `renpy/measurements_store.rpy`
- `src/voxel_object_loader.py` → `renpy/voxel_micro_loader.rpy`
- `data/voxel_objects/*.json` → `renpy/objects/*.rpy`

### Step 2: Generate Microencoding Palette

```python
# Conversion script: python_to_renpy_converter.py

def generate_microencoding_palette():
    """
    Reads data/measurements/spatial_measurements.json
    and creates a Ren'Py define block with all measurements.
    """
    ml = MeasurementsLoader()

    output = []
    output.append("# Auto-generated from measurements_loader.py")
    output.append("# Source of truth: Escalator stairs (8 feet) + Elevator doors")
    output.append("")

    # Critical measurements
    output.append(f"define ESCALATOR_DROP_FEET = {ml.get_spatial('food_court.pit_depth_feet.value')}")
    output.append(f"define ELEVATOR_DOOR_WIDTH_FEET = 3.5  # Commercial standard")
    output.append(f"define ELEVATOR_DOOR_HEIGHT_FEET = 6.75  # Commercial standard")
    output.append("")

    # All spatial measurements
    output.append(f"define ATRIUM_DIAMETER_FEET = {ml.get_spatial('atrium.diameter_feet.value')}")
    output.append(f"define MAST_HEIGHT_FEET = {ml.get_spatial('tensile_roof.mast_height_feet.value')}")
    # ... etc

    return "\n".join(output)
```

### Step 3: Convert Voxel Objects

```python
def convert_voxel_object_to_renpy(obj_id):
    """
    Converts JANITOR_MOP.json to janitor_mop.rpy with microencoding.
    """
    # Load via existing loader (respects architecture)
    registry = VoxelObjectRegistry(...)
    registry.load_registry()
    obj = registry.get(obj_id)

    # Extract microencoding
    encoding = obj.mesh["encoding"]  # Already microencoded

    # Generate Ren'Py script
    output = []
    output.append(f"# Object: {obj_id}")
    output.append(f"# Source: {obj.source_image}")
    output.append(f"")
    output.append(f"define voxel_{obj_id.lower()} = VoxelMicroSprite(")
    output.append(f'    encoding="{encoding}",')
    output.append(f"    dimensions={obj.metadata['zone_id']},")
    output.append(f"    qbit={obj.qbit}")
    output.append(f")")

    return "\n".join(output)
```

### Step 4: Create Ren'Py Game Structure

```
v8-nextgen-renpy/
├── game/
│   ├── script.rpy                    # Main game script
│   ├── measurements_store.rpy        # Converted measurements
│   ├── voxel_micro_loader.rpy        # Microencoding decoder
│   ├── screens.rpy                   # UI screens
│   │
│   ├── objects/                      # Converted voxel objects
│   │   ├── janitor_mop.rpy
│   │   ├── pizza_slice.rpy
│   │   ├── slurpee_cup.rpy
│   │   └── ...
│   │
│   ├── zones/                        # Zone definitions
│   │   ├── z1_central_atrium.rpy
│   │   ├── z4_food_court.rpy
│   │   ├── z5_escalator_wells.rpy
│   │   └── ...
│   │
│   └── python/                       # Python modules (existing loader)
│       ├── measurements_loader.py    # Unchanged (source of truth)
│       ├── voxel_object_loader.py    # Microencoding wrapper
│       └── microencoding.py          # Encoder/decoder
│
└── images/
    └── voxel_symbols/                # Rendered symbol sprites
        ├── solid.png
        ├── braille_patterns/
        └── material_icons/
```

---

## Part 5: Example Conversion

### Before (Python v8)

**File:** `data/voxel_objects/JANITOR_MOP.json`
```json
{
  "voxel_object_id": "JANITOR_MOP",
  "source_image": "assets/voxel_sources/janitor_mop.png",
  "mode": "HEIGHTMAP_EXTRUDE",
  "voxel_scale": [1, 1, 1],
  "qbit": {
    "power": 500,
    "charisma": 100,
    "resonance": 80
  },
  "placement": {
    "attach": "floor",
    "offset": [0, 0, 0]
  },
  "behavior": {
    "type": "NPC_PROP",
    "tags": ["SERVICE_HALL", "UNIT7"],
    "on_pickup": [
      "subtitle: 'You really shouldn't be holding that.'",
      "cloud_pressure+2"
    ]
  }
}
```

**Loaded via:** `voxel_object_loader.py` → PNG decoded → mesh generated

### After (Ren'Py Microencoded)

**File:** `game/objects/janitor_mop.rpy`
```renpy
# JANITOR_MOP - Microencoded Voxel Object
# Original source: assets/voxel_sources/janitor_mop.png
# Measurement anchor: 8-foot scale (escalator drop)

define voxel_janitor_mop = VoxelMicroSprite(
    encoding="""
        METAL_RAIL:▓4█2▓4
        METAL_RAIL:▓4█2▓4
        WOOD_HANDLE:█10
        WOOD_HANDLE:█10
        WOOD_HANDLE:█10
        WOOD_HANDLE:█10
        MOP_HEAD:▒8░2
        MOP_HEAD:▒8░2
    """,
    dimensions=(10, 8, 4.5),  # width, height, feet_tall
    qbit={
        "power": 500,
        "charisma": 100,
        "resonance": 80,
        "owner_npc_id": "UNIT_7"
    },
    placement={"attach": "floor", "offset": [0, 0, 0]},
    behavior={
        "type": "NPC_PROP",
        "tags": ["SERVICE_HALL", "UNIT7"]
    }
)

# Ren'Py interaction
label interact_janitor_mop:
    show voxel_janitor_mop at center

    "You reach for the janitor's mop."
    "You really shouldn't be holding that."

    python:
        cloud_pressure += 2

    return
```

---

## Part 6: Respecting the Loader

### Critical Design Constraint

**The existing `voxel_object_loader.py` must remain the authoritative source.**

#### Approach: Wrapper, Not Replacement

```python
# In Ren'Py python block
init python:
    # Import original loader (unchanged)
    from voxel_object_loader import VoxelObjectRegistry

    # Create Ren'Py-compatible wrapper
    class RenpyVoxelRegistry(VoxelObjectRegistry):
        """
        Extends VoxelObjectRegistry with microencoding support.
        Does NOT modify parent class - only adds Ren'Py rendering.
        """

        def __init__(self, *args, **kwargs):
            # Use original initialization
            super().__init__(*args, **kwargs)
            self.microencoding_cache = {}

        def get_renpy_sprite(self, obj_id):
            """
            New method: Returns Ren'Py displayable.
            Uses original loader's data as source of truth.
            """
            # 1. Load via parent class (respects original loader)
            obj = self.get(obj_id)

            # 2. Convert to microencoding (caching)
            if obj_id not in self.microencoding_cache:
                encoding = self._mesh_to_microencoding(obj.mesh)
                self.microencoding_cache[obj_id] = encoding

            # 3. Return Ren'Py sprite
            return VoxelMicroSprite(
                encoding=self.microencoding_cache[obj_id],
                dimensions=obj.metadata,
                qbit=obj.qbit
            )
```

### Data Flow Diagram

```
measurements_loader.py (Source of Truth)
         ↓
   [Escalator: 8 feet]
   [Elevator: 3.5' × 6.75']
         ↓
voxel_object_loader.py (Original Loader - UNCHANGED)
         ↓
   [PNG → Mesh Data]
         ↓
RenpyVoxelRegistry (Wrapper)
         ↓
   [Mesh → Microencoding]
         ↓
VoxelMicroSprite (Ren'Py Displayable)
         ↓
   [Render in Visual Novel]
```

---

## Part 7: Implementation Checklist

### Phase 1: Foundation
- [ ] Create `microencoding.py` - encoder/decoder utilities
- [ ] Create `renpy_voxel_wrapper.py` - wrapper around original loader
- [ ] Generate symbol palette from measurements

### Phase 2: Conversion
- [ ] Convert `measurements_loader.py` → `measurements_store.rpy`
- [ ] Convert all voxel objects to `.rpy` with microencoding
- [ ] Convert zone definitions to Ren'Py screens

### Phase 3: Integration
- [ ] Create main `script.rpy` with game flow
- [ ] Implement `VoxelMicroSprite` displayable class
- [ ] Build rendering pipeline (microencoding → sprites)

### Phase 4: Validation
- [ ] Verify all measurements match source of truth
- [ ] Test voxel object loading via original loader
- [ ] Confirm QBIT scores preserved
- [ ] Validate zone dimensions (8-foot escalator drop)

---

## Part 8: Wingdings Encoding Reference

### Complete Symbol Mapping

```python
VOXEL_SYMBOLS = {
    # Density levels (4 bits)
    'solid': '█',
    'dense': '▓',
    'medium': '▒',
    'light': '░',

    # Geometric primitives
    'half_bottom': '▄',
    'half_top': '▀',
    'half_left': '▌',
    'half_right': '▐',

    # Material types (from palette)
    'tile_white': '⬜',
    'tile_terracotta': '🟫',
    'carpet_red': '🟥',
    'glass_block': '💎',
    'concrete': '⬛',
    'metal_blue': '🔵',
    'metal_green': '🟢',
    'neon': '💡',
    'water': '💧',

    # Braille patterns (2×4 grids) - 256 combinations
    # Range: U+2800 (⠀) to U+28FF (⣿)
    # Example: ⠀⠁⠂⠃⠄⠅⠆⠇...
    'braille_base': 0x2800,
}

def encode_voxel_cell(material, density, pattern=None):
    """
    Encode a single voxel cell.

    Examples:
        encode_voxel_cell('tile_white', 'solid') → '⬜█'
        encode_voxel_cell('glass_block', 'medium') → '💎▒'
        encode_voxel_cell('metal_blue', 'braille', 0b11110000) → '🔵⣰'
    """
    material_sym = VOXEL_SYMBOLS.get(material, '?')

    if pattern and density == 'braille':
        braille_char = chr(VOXEL_SYMBOLS['braille_base'] + pattern)
        return f"{material_sym}{braille_char}"
    else:
        density_sym = VOXEL_SYMBOLS.get(density, '█')
        return f"{material_sym}{density_sym}"
```

### Compression Ratio

```
Original PNG (janitor_mop.png):
  10×8 pixels × 4 bytes (RGBA) = 320 bytes

Microencoded:
  8 lines × ~15 chars/line = 120 characters
  UTF-8 encoding: ~240 bytes (2 bytes/char average)

Compression: ~25% reduction
Human-readable: YES
Version-controllable: YES (git diff friendly)
```

---

## Part 9: Well-Defined Path Forward

### Directory Structure (Already Exists)
```
v8-nextgen/
├── data/measurements/         ← Source of truth files (KEEP)
│   ├── spatial_measurements.json
│   ├── zone_measurements.json
│   └── feature_measurements.json
│
├── src/
│   ├── measurements_loader.py       ← Keep unchanged
│   └── voxel_object_loader.py       ← Keep unchanged
```

### New Additions for Ren'Py
```
v8-nextgen/
├── renpy_conversion/                 ← NEW
│   ├── microencoding.py             ← Encoder/decoder
│   ├── renpy_voxel_wrapper.py       ← Wrapper around original loader
│   └── python_to_renpy.py           ← Conversion script
│
└── renpy_output/                     ← NEW (generated)
    └── game/
        ├── script.rpy
        ├── measurements_store.rpy
        ├── objects/
        │   ├── janitor_mop.rpy
        │   └── ...
        └── python/
            ├── measurements_loader.py   ← Symlink to original
            └── voxel_object_loader.py   ← Symlink to original
```

### Execution Path

1. **Read measurements** (escalator + elevator as anchors)
2. **Load voxel objects** via original `voxel_object_loader.py`
3. **Convert to microencoding** using wingdings-style symbols
4. **Generate `.rpy` files** preserving all metadata
5. **Wrap original loader** for Ren'Py compatibility
6. **Validate** all measurements against source of truth

---

## Conclusion

This architecture:
- ✅ Uses escalator/elevator measurements as single source of truth
- ✅ Respects existing `voxel_object_loader.py` (wrapper pattern)
- ✅ Implements wingdings-style microencoding for compact storage
- ✅ Converts Python scripts to Ren'Py primitives (`.rpy` files)
- ✅ Preserves all metadata (QBIT, placement, behavior)
- ✅ Provides well-defined conversion path

**Next step:** Implement `microencoding.py` and conversion scripts.
