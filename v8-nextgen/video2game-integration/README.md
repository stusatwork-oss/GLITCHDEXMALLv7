# Video2Game Integration for Eastland Mall

Transform your 11-minute walkthrough video of Eastland Mall into game-ready 3D assets using neural radiance fields (NeRF) and mesh extraction.

## 🎯 Quick Start

### 1. Install Video2Game
```bash
# See docs/INSTALLATION.md for detailed setup
cd video2game-integration
git clone https://github.com/video2game/video2game.git
conda create -n video2game python=3.7
conda activate video2game
# ... follow installation guide
```

### 2. Add Your Walkthrough Video
```bash
# Copy your video to input directory
cp /path/to/your/mall_walkthrough.mp4 input/
```

### 3. Process the Video
```bash
cd scripts
python process_walkthrough.py \
    --video ../input/mall_walkthrough.mp4 \
    --output ../output/eastland_$(date +%Y%m%d)
```

**Processing Time:** ~4-8 hours (11-minute video)

### 4. Integrate with Voxel Builder
```bash
# Extract materials and validate geometry
python extract_materials.py
python compare_geometry.py

# Use enhanced voxel builder
python voxel_builder_enhanced.py
```

## 📁 Directory Structure

```
video2game-integration/
├── README.md                   # This file
├── input/                      # Place videos here
│   └── .gitkeep
├── output/                     # Processing results
│   └── .gitkeep
├── scripts/
│   ├── process_walkthrough.py  # Main pipeline script
│   ├── extract_materials.py    # Texture extraction (created by you)
│   ├── compare_geometry.py     # Validation (created by you)
│   └── voxel_builder_enhanced.py  # Enhanced builder (created by you)
└── docs/
    ├── INSTALLATION.md         # Setup guide
    ├── PIPELINE_GUIDE.md       # Processing workflow
    └── INTEGRATION_GUIDE.md    # Integration with voxel builder
```

## 📚 Documentation

**Read in this order:**

1. **[INSTALLATION.md](docs/INSTALLATION.md)**
   - System requirements
   - Installing video2game and dependencies
   - GPU setup (CUDA 11.6 + PyTorch 1.12)
   - Troubleshooting common issues

2. **[PIPELINE_GUIDE.md](docs/PIPELINE_GUIDE.md)**
   - Processing your walkthrough video
   - Configuration options
   - Performance tuning
   - Output formats

3. **[INTEGRATION_GUIDE.md](docs/INTEGRATION_GUIDE.md)**
   - Using video2game with voxel_builder
   - Material extraction workflow
   - Geometry validation
   - Scale calibration

## 🎮 What You Get

### Outputs from Video2Game Pipeline

After processing your video, you'll have:

```
output/eastland_YYYYMMDD/
├── mesh/                      # 3D geometry
│   ├── mall.obj               # Polygon mesh
│   └── mall.ply               # Point cloud
├── textured/                  # Photorealistic textures
│   ├── mall_textured.obj
│   └── mall_diffuse.png       # 2048x2048 texture map
├── collision/                 # Physics meshes
│   └── mall_collision.obj     # Convex hulls for physics
├── exports/                   # Game-ready
│   └── mall.glb               # Import into Unity/Unreal/Godot
└── processing_metadata.json   # Scale + integration data
```

### Integration with Voxel Builder

The video2game outputs enhance your voxel-based game:

- **Textures** → Material palettes for voxel zones
- **Geometry** → Validation of CRD measurements
- **Scale** → Cross-reference with photo-derived dimensions
- **Materials** → Photorealistic appearance data

**Key Principle:** CRD measurements = geometry source, video2game = texture/validation

## 🚀 Usage Examples

### Example 1: Texture Enhancement Only
```bash
# Process for textures (fastest)
python scripts/process_walkthrough.py \
    --video input/walkthrough.mp4 \
    --output output/textures_only

# Extract material palette
cd output/textures_only
python ../../scripts/extract_materials.py

# Apply to voxel builder
# (use material_palette.json in voxel_builder_enhanced.py)
```

### Example 2: Full Validation + Enhancement
```bash
# Full pipeline (4-8 hours)
python scripts/process_walkthrough.py \
    --video input/walkthrough.mp4 \
    --output output/full_$(date +%Y%m%d)

# Compare with CRD measurements
cd output/full_YYYYMMDD
python ../../scripts/compare_geometry.py

# Open mesh in Blender to measure
blender mesh/mall.obj

# Calculate scale factor: crd_dimension / mesh_dimension
# Update CRD if needed: ../../data/measurements/spatial_measurements.json

# Build enhanced voxels
cd ../../scripts
python voxel_builder_enhanced.py
```

### Example 3: Direct Mesh Import (No Voxels)
```bash
# Use video2game mesh directly in game engine
cp output/eastland_YYYYMMDD/exports/mall.glb ../exports/

# Import mall.glb into Unity/Unreal/Godot
# Scale by calibration factor
# Add player + gameplay
```

## ⚙️ Configuration

### Default Settings (Balanced)
```json
{
  "frame_extraction": {"fps": 2},
  "nerf": {"max_steps": 30000, "batch_size": 4096},
  "mesh": {"resolution": 512},
  "texture": {"resolution": 2048}
}
```

### High Quality (16GB+ VRAM)
```json
{
  "frame_extraction": {"fps": 5},
  "nerf": {"max_steps": 100000, "batch_size": 16384},
  "mesh": {"resolution": 1024},
  "texture": {"resolution": 4096}
}
```

### Low VRAM (6-8GB)
```json
{
  "frame_extraction": {"fps": 1},
  "nerf": {"max_steps": 15000, "batch_size": 2048},
  "mesh": {"resolution": 256},
  "texture": {"resolution": 1024}
}
```

Save as `custom_config.json` and use:
```bash
python scripts/process_walkthrough.py \
    --video input/video.mp4 \
    --config custom_config.json
```

## 🎬 Video Capture Tips

For best results, capture your walkthrough with:

**Camera Movement:**
- Slow, steady panning (no quick jerks)
- Circular paths around features
- Multiple heights/angles
- Good overlap between frames

**Lighting:**
- Even, diffuse lighting (avoid harsh shadows)
- Consistent brightness (no dramatic changes)
- Overcast day ideal for windows

**Coverage:**
- Capture all zones from multiple angles
- Include floor and ceiling
- Document scale references in frame
- Pause on important details

**Technical:**
- 1080p minimum (4K better)
- 30fps or higher
- Stabilization on (gimbal/tripod ideal)
- Avoid motion blur

## 🔧 Troubleshooting

### Pipeline Fails
```bash
# Check GPU
nvidia-smi

# Verify CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Check video2game install
python -c "import tinycudann; print('OK')"
```

### Out of Memory
- Reduce batch_size in config
- Lower mesh resolution
- Decrease texture resolution

### Poor Mesh Quality
- Increase NeRF training steps
- Improve video quality/coverage
- Adjust mesh extraction threshold

See [PIPELINE_GUIDE.md](docs/PIPELINE_GUIDE.md#troubleshooting) for more.

## 📊 Processing Requirements

**Hardware:**
- NVIDIA GPU: 8GB+ VRAM (16GB recommended)
- CPU: 4+ cores
- RAM: 16GB+
- Storage: 50GB+ free

**Time Estimates (11-minute video):**
- Frame extraction: ~5 minutes
- COLMAP reconstruction: ~30-60 minutes
- NeRF training: ~2-4 hours
- Mesh extraction: ~30 minutes
- Texture baking: ~30-60 minutes
- Collision generation: ~15 minutes
- **Total: ~4-8 hours**

**Disk Space:**
- Frames: ~2-5 GB
- Processing artifacts: ~3-7 GB
- Final outputs: ~1-3 GB
- **Total: ~5-15 GB**

## 🧪 Status

**Video2Game Implementation Status:**
- ✅ NeRF training
- ✅ Mesh extraction
- ✅ Texture baking (pretraining)
- ✅ Collision generation
- ✅ Evaluation
- ⏳ Texture baking finetuning
- ⏳ GPT-4 integration

Current functionality is sufficient for basic video-to-mesh conversion.

## 🔗 Resources

**Video2Game:**
- GitHub: https://github.com/video2game/video2game
- Research paper: Check repo for latest publication

**Related Tools:**
- COLMAP: https://colmap.github.io/
- NeRF: https://www.matthewtancik.com/nerf
- V-HACD: https://github.com/kmammou/v-hacd

**GLITCHDEXMALL Docs:**
- Project README: `../../README.md`
- CRD Measurements: `../data/measurements/`
- Voxel Builder: `../src/voxel_builder.py`

## 🎯 Integration Philosophy

```
┌─────────────────┐
│  Walkthrough    │
│  Video (11 min) │
└────────┬────────┘
         ↓
    video2game
         ↓
    ┌────┴─────┐
    ↓          ↓
  Mesh     Textures
    ↓          ↓
    ↓      Material
    ↓      Palette
    ↓          ↓
    ↓     ┌────┴─────────┐
    ↓     ↓              ↓
Validate  ↓         Voxel Builder
    ↓     ↓         (CRD Geometry)
    ↓     ↓              ↓
    └──→ CRD ←───────────┘
         ↓
    Enhanced Voxel Mesh
    (Geometry + Textures)
         ↓
    Doom-Alike Export
```

**Key Points:**
1. CRD measurements = ground truth for geometry
2. Video2game textures = visual enhancement
3. Video mesh = validation reference
4. Integration = best of both worlds

## 🎮 End Goal

**3 credit cards as weapons in a 1,000,000+ sq ft mall dungeon.**

Video2game helps you:
- Extract photorealistic textures from your walkthrough
- Validate CRD measurements with video-derived geometry
- Create immersive materials for voxel zones
- Reference real spatial relationships

Combined with CRD voxel builder:
- Accurate, measured geometry (ground truth)
- Photorealistic appearance (from video)
- Game-ready collision (voxel-based)
- Doom-alike playability

## 📝 Quick Reference

| Task | Command |
|------|---------|
| Install | See `docs/INSTALLATION.md` |
| Process video | `python scripts/process_walkthrough.py --video input/video.mp4` |
| Extract materials | `python scripts/extract_materials.py` |
| Validate geometry | `python scripts/compare_geometry.py` |
| Build enhanced voxels | `python scripts/voxel_builder_enhanced.py` |
| Check GPU | `nvidia-smi` |
| View mesh | `blender output/*/mesh/mall.obj` |

## 🤝 Contributing

When adding video2game data to the project:

1. **Document scale calibration** in `processing_metadata.json`
2. **Cross-reference with CRD** measurements
3. **Note discrepancies** in integration notes
4. **Mark assumptions** explicitly
5. **Commit both** video outputs and CRD updates

## 📞 Support

- Video2Game issues: https://github.com/video2game/video2game/issues
- GLITCHDEXMALL issues: Project maintainers
- CUDA/PyTorch: Official documentation

---

**Status:** Ready for integration
**Last Updated:** 2025-12-07
**Version:** 1.0.0

**Ready to process your 11-minute walkthrough? Start with [INSTALLATION.md](docs/INSTALLATION.md)!**
