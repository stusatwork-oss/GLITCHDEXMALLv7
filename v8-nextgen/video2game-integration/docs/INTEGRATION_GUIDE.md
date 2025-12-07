# Video2Game Integration with Voxel Builder

## Overview
This guide explains how to integrate video2game outputs (mesh, textures, geometry) with the existing `voxel_builder.py` system for Eastland Mall reconstruction.

## Integration Philosophy

**Video2Game provides:**
- Real geometry from video walkthrough
- Photorealistic textures
- Spatial relationships
- Visual reference

**Voxel Builder provides:**
- CRD-validated measurements (ground truth)
- Game-ready voxel geometry
- Zone-based structure
- Doom-alike collision

**Integration strategy:**
1. Use CRD measurements as primary source (ground truth)
2. Use video2game mesh for texture extraction and visual validation
3. Cross-reference geometry to validate/refine measurements
4. Extract material definitions from video textures

## Workflow

### Step 1: Process Your Video
```bash
cd v8-nextgen/video2game-integration/scripts
python process_walkthrough.py \
    --video ../input/walkthrough.mp4 \
    --output ../output/eastland_$(date +%Y%m%d)
```

Wait for completion (~4-8 hours).

### Step 2: Validate Scale
The video2game mesh will be in arbitrary units. You need to calibrate:

```bash
cd ../output/eastland_YYYYMMDD

# Create scale calibration script
cat > calibrate_scale.py << 'EOF'
#!/usr/bin/env python3
"""Scale calibration for video2game mesh vs CRD measurements."""

import json
import numpy as np

# Load video2game mesh (simplified - adjust for actual mesh format)
# mesh = load_mesh("mesh/mall.obj")

# Load CRD measurements
with open("../../../data/measurements/spatial_measurements.json") as f:
    measurements = json.load(f)

# Known reference points from video:
# 1. Food court pit depth (easiest to measure in mesh)
# 2. Atrium diameter (if visible in captures)
# 3. Corridor widths (if walkthrough is along corridors)

print("CRD Reference Values:")
print(f"  Atrium diameter: 175 feet")
print(f"  Food court pit: 8 feet")
print(f"  Main corridor: 25 feet width")
print()
print("Measure these in your mesh (Blender/MeshLab)")
print("Then calculate: scale_factor = crd_value / mesh_value")
EOF

python calibrate_scale.py
```

### Step 3: Extract Material Textures
The video2game textures are photorealistic captures. Use them for voxel materials:

```bash
cd ../output/eastland_YYYYMMDD

# Create texture extraction script
cat > extract_materials.py << 'EOF'
#!/usr/bin/env python3
"""Extract material definitions from video2game textures."""

import json
from pathlib import Path
from PIL import Image

def extract_zone_materials():
    """
    Extract material definitions for each zone.

    Strategy:
    1. Segment textured mesh by zone (manual or semantic)
    2. Sample dominant colors/textures per zone
    3. Create material palettes for voxel builder
    """

    texture_path = Path("textured/mall_diffuse.png")

    if not texture_path.exists():
        print("Texture not found. Run video2game pipeline first.")
        return

    # Load texture
    texture = Image.open(texture_path)

    # Define material zones (example - adjust based on your mesh UVs)
    zone_materials = {
        "Z1_CENTRAL_ATRIUM": {
            "floor": "sample_texture_region(texture, uv_bounds_atrium_floor)",
            "walls": "sample_texture_region(texture, uv_bounds_atrium_walls)",
            "ceiling": "tensile_sail_white"  # Known from photos
        },
        "Z4_FOOD_COURT": {
            "floor": "tile_pattern_from_video",
            "walls": "extract_storefront_textures",
            "ceiling": "tensile_sail_shadows"
        },
        # ... more zones
    }

    # Export material palette
    palette = {
        "version": "1.0",
        "source": "video2game texture extraction",
        "materials": zone_materials
    }

    with open("../material_palette.json", 'w') as f:
        json.dump(palette, f, indent=2)

    print("Material palette exported to material_palette.json")

if __name__ == "__main__":
    extract_zone_materials()
EOF

python extract_materials.py
```

### Step 4: Cross-Reference Geometry
Compare video2game mesh with CRD measurements to validate/refine:

```bash
cat > compare_geometry.py << 'EOF'
#!/usr/bin/env python3
"""Compare video2game geometry with CRD measurements."""

import json
import sys

def compare_geometries():
    """
    Compare extracted mesh geometry with CRD measurements.

    Report discrepancies for investigation.
    """

    # Load CRD measurements
    crd_path = "../../../data/measurements/spatial_measurements.json"
    with open(crd_path) as f:
        crd = json.load(f)

    # Load video2game metadata
    with open("processing_metadata.json") as f:
        video_meta = json.load(f)

    print("="*60)
    print("GEOMETRY COMPARISON: Video2Game vs CRD")
    print("="*60)
    print()

    # Example comparisons (adjust for your data structure)
    comparisons = [
        {
            "feature": "Atrium Diameter",
            "crd_value": 175,
            "crd_confidence": "MEDIUM",
            "video_value": "measure_in_mesh",  # Placeholder
            "notes": "Measure circle diameter in mesh top-down view"
        },
        {
            "feature": "Food Court Pit Depth",
            "crd_value": 8,
            "crd_confidence": "HIGH",
            "video_value": "measure_in_mesh",
            "notes": "Z-height difference between levels"
        },
        {
            "feature": "Corridor Width (main)",
            "crd_value": 25,
            "crd_confidence": "MEDIUM",
            "video_value": "measure_in_mesh",
            "notes": "Wall-to-wall in corridor segment"
        }
    ]

    for comp in comparisons:
        print(f"Feature: {comp['feature']}")
        print(f"  CRD: {comp['crd_value']} ft (confidence: {comp['crd_confidence']})")
        print(f"  Video: {comp['video_value']}")
        print(f"  Notes: {comp['notes']}")
        print()

    print("="*60)
    print("RECOMMENDATIONS:")
    print("="*60)
    print("1. Measure features in Blender/MeshLab")
    print("2. Calculate scale factor: crd_value / mesh_value")
    print("3. If scale matches: CRD validated ✓")
    print("4. If discrepancy > 10%: Investigate (photo evidence, video angle bias)")
    print("5. Update CRD measurements if video evidence is stronger")
    print()

if __name__ == "__main__":
    compare_geometries()
EOF

python compare_geometry.py
```

### Step 5: Enhance Voxel Builder
Create an enhanced version that uses video2game data:

```bash
cd ../../..  # Back to v8-nextgen/
cp src/voxel_builder.py video2game-integration/scripts/voxel_builder_enhanced.py
```

Edit `voxel_builder_enhanced.py`:

```python
# Add at top of file:
from pathlib import Path

class EnhancedVoxelBuilder(VoxelBuilder):
    """
    Voxel builder enhanced with video2game data.

    Uses CRD measurements for geometry (primary).
    Uses video2game textures for materials (enhancement).
    """

    def __init__(self, video2game_output_dir: str = None):
        super().__init__()

        self.video2game_dir = None
        self.material_palette = None

        if video2game_output_dir:
            self.load_video2game_data(video2game_output_dir)

    def load_video2game_data(self, output_dir: str):
        """Load video2game outputs for material enhancement."""
        v2g_path = Path(output_dir)

        # Load metadata
        meta_path = v2g_path / "processing_metadata.json"
        if meta_path.exists():
            with open(meta_path) as f:
                self.video2game_metadata = json.load(f)
            print(f"Loaded video2game metadata from {output_dir}")

        # Load material palette if available
        palette_path = v2g_path / "material_palette.json"
        if palette_path.exists():
            with open(palette_path) as f:
                self.material_palette = json.load(f)
            print("Loaded material palette from video2game")

        self.video2game_dir = v2g_path

    def get_material_for_zone(self, zone_id: str, surface: str = "floor") -> str:
        """
        Get material for a zone, using video2game palette if available.

        Falls back to default materials if video data not loaded.
        """
        if self.material_palette:
            zone_materials = self.material_palette.get("materials", {}).get(zone_id, {})
            if surface in zone_materials:
                return f"v2g_{zone_materials[surface]}"

        # Fallback to default
        return f"default_{surface}"

    def _build_atrium(self):
        """Build atrium with video2game materials."""
        # Call parent implementation for geometry
        super()._build_atrium()

        # Enhance with video2game materials if available
        if self.video2game_dir:
            for cyl in self.cylinders:
                if cyl.zone_id == "Z1_CENTRAL_ATRIUM":
                    cyl.material = self.get_material_for_zone("Z1_CENTRAL_ATRIUM", "floor")

    # Override other _build_* methods similarly...
```

### Step 6: Run Enhanced Build
```bash
cd video2game-integration/scripts

python << 'EOF'
from voxel_builder_enhanced import EnhancedVoxelBuilder

# Build with video2game enhancement
builder = EnhancedVoxelBuilder(
    video2game_output_dir="../output/eastland_20250101"  # Adjust date
)

mesh = builder.build_full_mall()
mesh.export_json("enhanced_mall_voxels.json")

print("Enhanced voxel mesh with video2game materials: enhanced_mall_voxels.json")
EOF
```

## Integration Use Cases

### Use Case 1: Texture Reference Only
**When:** CRD measurements are confident, just need visual polish

**Workflow:**
1. Run video2game for textures only
2. Extract material palette
3. Apply to voxel builder materials
4. Keep CRD geometry unchanged

**Command:**
```bash
python process_walkthrough.py --video input/walkthrough.mp4 --output output/textures_only
python extract_materials.py
# Use material_palette.json in voxel builder
```

### Use Case 2: Geometry Validation
**When:** CRD measurements are uncertain, need validation

**Workflow:**
1. Run full video2game pipeline
2. Compare mesh dimensions with CRD
3. Resolve discrepancies (photo evidence review)
4. Update CRD measurements if needed
5. Rebuild voxels with corrected measurements

**Command:**
```bash
python process_walkthrough.py --video input/walkthrough.mp4 --output output/validation
python compare_geometry.py  # Manual measurement in Blender
# Update ../../data/measurements/spatial_measurements.json if needed
cd ../../src && python voxel_builder.py
```

### Use Case 3: Hybrid Mesh
**When:** Want to use video2game geometry directly in some zones

**Workflow:**
1. Run full video2game pipeline
2. Export specific zones from video mesh (e.g., storefront details)
3. Use voxel builder for major structure
4. Combine: voxel boxes + video mesh details
5. Export unified format

**Tools needed:**
- Blender for mesh editing
- Custom export script to combine formats

### Use Case 4: Quick Prototyping
**When:** Want fast iteration without full pipeline

**Workflow:**
1. Use existing CRD voxels for structure
2. Apply procedural textures (no video2game)
3. Iterate gameplay
4. Add video2game textures later for polish

**Command:**
```bash
cd ../../src
python voxel_builder.py  # Fast, CRD only
# Iterate on gameplay with simple materials
# Later: add video2game textures
```

## Data Flow Diagram

```
Input Video (11 min walkthrough)
         ↓
   video2game pipeline
         ↓
    ┌────┴────┐
    ↓         ↓
  Mesh    Textures
    ↓         ↓
    ↓    Material Palette ──→ Enhanced Voxel Builder
    ↓                              ↓
    ↓                         Voxel Geometry
    ↓                         (from CRD)
    ↓                              ↓
    └──→ Geometry Validation       ↓
         (compare with CRD)        ↓
              ↓                    ↓
         Update CRD ──────────────→┘
              ↓
    Final Voxel Mesh with
    Video-derived Materials
```

## File Organization

```
v8-nextgen/
├── video2game-integration/
│   ├── input/
│   │   └── walkthrough.mp4          # Your 11-min video
│   ├── output/
│   │   └── eastland_YYYYMMDD/       # Processing outputs
│   │       ├── mesh/                # 3D geometry
│   │       ├── textured/            # Baked textures
│   │       ├── collision/           # Physics meshes
│   │       └── processing_metadata.json
│   ├── scripts/
│   │   ├── process_walkthrough.py   # Main pipeline
│   │   ├── extract_materials.py     # Texture → materials
│   │   ├── compare_geometry.py      # Validation
│   │   └── voxel_builder_enhanced.py
│   └── docs/
│       ├── INSTALLATION.md
│       ├── PIPELINE_GUIDE.md
│       └── INTEGRATION_GUIDE.md     # This file
│
├── src/
│   └── voxel_builder.py             # Original CRD-based builder
│
└── data/
    └── measurements/
        └── spatial_measurements.json  # CRD ground truth
```

## Best Practices

### 1. Trust CRD Measurements First
Video2game geometry can have distortions from:
- Camera lens distortion
- Perspective bias
- Incomplete coverage
- NeRF hallucinations

**Always validate against:**
- Photo evidence
- Known architectural standards (escalator steps, door heights)
- Multiple measurement sources

### 2. Use Video Textures for Visual Reference
Video textures are excellent for:
- Material colors/patterns
- Lighting reference
- Atmospheric details
- Storefront signage

But **don't** rely on them for:
- Precise geometry
- Scale calibration
- Hidden/occluded areas

### 3. Document Discrepancies
When video2game and CRD disagree:
1. Document both values
2. Note confidence levels
3. Review photo evidence
4. Make informed decision
5. Mark assumption in metadata

### 4. Iterative Refinement
- Start with CRD voxels (fast)
- Add video textures (enhancement)
- Validate geometry (optional)
- Refine as needed

Don't try to do everything in one pass.

## Troubleshooting

### Video Mesh Doesn't Match CRD
**Symptoms:** Measured dimensions off by 20%+

**Causes:**
- Camera lens distortion (wide-angle)
- NeRF scale ambiguity
- Incomplete video coverage

**Fix:**
1. Recalibrate scale (use multiple reference points)
2. Check COLMAP reconstruction quality
3. Use CRD as primary, video as reference only

### Textures Look Wrong
**Symptoms:** Blurry, artifacts, color shifts

**Causes:**
- Low video quality
- Lighting variations in video
- NeRF baking artifacts

**Fix:**
1. Use higher resolution config
2. Increase NeRF training steps
3. Manual texture cleanup in Photoshop/GIMP

### Integration Script Fails
**Symptoms:** Import errors, missing data

**Causes:**
- Video2game pipeline incomplete
- File paths wrong
- Missing dependencies

**Fix:**
```bash
# Verify video2game outputs exist
ls -R output/eastland_YYYYMMDD/

# Check metadata
cat output/eastland_YYYYMMDD/processing_metadata.json

# Verify paths in integration script
```

## Advanced: Direct Mesh Use

If you want to use video2game mesh directly instead of voxels:

```bash
# Export mesh with collision
cp output/eastland_YYYYMMDD/exports/mall.glb ../exports/

# Import into game engine (Unity/Unreal/Godot)
# Apply scale factor from calibration
# Add player controller
# Add gameplay logic (credit card weapons, etc.)
```

This bypasses voxel builder entirely, giving you:
- Photorealistic geometry
- Baked lighting
- Efficient rendering

But you lose:
- Voxel-based destruction
- Easy modification
- CRD measurement validation

**Recommendation:** Use voxel builder for gameplay, video mesh for reference.

## Summary

| Aspect | CRD/Voxel Builder | Video2Game | Integration |
|--------|-------------------|------------|-------------|
| **Geometry** | Ground truth | Validation | CRD primary, video validates |
| **Textures** | Procedural | Photorealistic | Use video textures |
| **Scale** | Measured (feet) | Arbitrary units | Calibrate video to CRD |
| **Use Case** | Gameplay structure | Visual polish | Best of both |

**Key Principle:** CRD measurements are authoritative. Video2game enhances visuals and validates.

## Next Steps

1. Process your 11-minute video (see PIPELINE_GUIDE.md)
2. Extract textures and materials
3. Calibrate scale
4. Enhance voxel builder with video materials
5. Export final voxel mesh
6. **DOOM in the mall with 3 credit cards**

---

For questions or issues, check:
- Video2Game: https://github.com/video2game/video2game
- GLITCHDEXMALL docs: `../../docs/`
- CRD methodology: `../../data/measurements/`
