# Getting Started with Video2Game Integration

**Turn your 11-minute Eastland Mall walkthrough video into game-ready 3D assets.**

This is your quickstart guide. For detailed information, see the docs/ folder.

## ⚡ Quick Start (5 steps)

### Step 1: Check Your System
```bash
cd v8-nextgen/video2game-integration/scripts
python check_system.py
```

This verifies you have:
- NVIDIA GPU (8GB+ VRAM)
- CUDA 11.6
- Python 3.7
- Sufficient disk space (50GB+)

If the check passes, proceed. If not, see [Installation Guide](docs/INSTALLATION.md).

### Step 2: Setup Environment
```bash
./quick_setup.sh
```

This will:
- Clone video2game repository
- Create Python 3.7 environment (conda or pyenv)
- Provide activation instructions

Then activate the environment:
```bash
conda activate video2game
# OR
pyenv activate video2game
```

### Step 3: Install Dependencies
```bash
cd video2game-integration/video2game

# Install PyTorch 1.12 + CUDA 11.6
pip install torch==1.12.0+cu116 torchvision==0.13.0+cu116 \
    --extra-index-url https://download.pytorch.org/whl/cu116

# Install video2game requirements
pip install -r requirements.txt

# Install specialized libraries
pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
pip install git+https://github.com/NVlabs/nvdiffrast/
```

For detailed installation, see [Installation Guide](docs/INSTALLATION.md).

### Step 4: Add Your Video
```bash
cd ../  # Back to video2game-integration/
cp /path/to/your/mall_walkthrough.mp4 input/
```

### Step 5: Process!
```bash
cd scripts
python process_walkthrough.py \
    --video ../input/mall_walkthrough.mp4 \
    --output ../output/eastland_$(date +%Y%m%d)
```

**Grab a coffee.** This takes 4-8 hours for an 11-minute video.

---

## 📊 What Happens During Processing

The pipeline runs through 8 stages:

1. **Frame Extraction** (~5 min) - Extracts video frames
2. **COLMAP** (~30-60 min) - Reconstructs camera poses
3. **NeRF Training** (~2-4 hours) - Learns 3D scene representation
4. **Mesh Extraction** (~30 min) - Converts NeRF to polygons
5. **Texture Baking** (~30-60 min) - Applies appearance to mesh
6. **Collision Generation** (~15 min) - Creates physics meshes
7. **Asset Export** (~5 min) - Packages for game engines
8. **Metadata** (~1 min) - Integration data for voxel_builder

**Total time:** ~4-8 hours
**Disk usage:** ~5-15 GB

You can monitor progress in the log file:
```bash
tail -f ../output/eastland_YYYYMMDD/processing_log_*.txt
```

---

## 🎯 After Processing

Once complete, you'll have:

```
output/eastland_YYYYMMDD/
├── mesh/
│   └── mall.obj               # 3D geometry
├── textured/
│   └── mall_diffuse.png       # Photorealistic texture
├── collision/
│   └── mall_collision.obj     # Physics mesh
└── exports/
    └── mall.glb               # Game-ready format
```

### What to Do Next

**Option A: Quick Visual Check**
```bash
# View the mesh in Blender (if installed)
blender ../output/eastland_YYYYMMDD/mesh/mall.obj
```

**Option B: Extract Materials for Voxel Builder**
```bash
# Extract texture materials
cd ../output/eastland_YYYYMMDD

# Create extraction script (see INTEGRATION_GUIDE.md)
# This samples textures and creates material palette
```

**Option C: Validate Geometry**
```bash
# Compare mesh with CRD measurements
cd ../output/eastland_YYYYMMDD

# Measure features in Blender:
# 1. Food court pit depth (should be ~8 feet after scaling)
# 2. Atrium diameter (should be ~175 feet after scaling)
# 3. Corridor widths (should be ~18-25 feet after scaling)

# Calculate scale factor
scale_factor = crd_measurement_feet / mesh_measurement_units
```

**Option D: Use Enhanced Voxel Builder**
```bash
cd ../../scripts

# Edit voxel_builder_enhanced.py to point to your output
# Then run:
python voxel_builder_enhanced.py
```

---

## 📚 Full Documentation

| Document | What It Covers |
|----------|----------------|
| [INSTALLATION.md](docs/INSTALLATION.md) | Detailed setup, dependencies, troubleshooting |
| [PIPELINE_GUIDE.md](docs/PIPELINE_GUIDE.md) | Processing workflow, config options, tips |
| [INTEGRATION_GUIDE.md](docs/INTEGRATION_GUIDE.md) | Using outputs with voxel_builder |

---

## 🔧 Troubleshooting

### "CUDA out of memory"
**Fix:** Reduce batch size and resolution
```json
{
  "nerf": {"batch_size": 2048},
  "mesh": {"resolution": 256},
  "texture": {"resolution": 1024}
}
```
Save as `low_vram_config.json` and use:
```bash
python process_walkthrough.py \
    --video ../input/video.mp4 \
    --config low_vram_config.json
```

### "COLMAP failed to reconstruct"
**Causes:**
- Too much motion blur in video
- Insufficient overlap between frames
- Poor lighting/texture

**Fix:** Extract more frames
```json
{"frame_extraction": {"fps": 5}}
```

### "Package installation fails"
**Fix:** Make sure you're in Python 3.7 environment
```bash
python --version  # Should show 3.7.x

# Reinstall in correct environment
conda activate video2game
pip install ...
```

For more troubleshooting, see [PIPELINE_GUIDE.md](docs/PIPELINE_GUIDE.md#troubleshooting).

---

## 💡 Tips for Best Results

### Video Capture
- Use slow, steady camera movement (gimbal/stabilizer ideal)
- Capture each area from multiple angles
- Ensure good lighting (even, diffuse)
- Include floor and ceiling in shots
- Walk at consistent pace

### Processing
- Start with default config, adjust if needed
- Monitor GPU usage: `watch -n 1 nvidia-smi`
- Keep frames after processing (for re-runs)
- Save logs for debugging

### Integration
- Trust CRD measurements for geometry
- Use video textures for visual polish
- Cross-reference measurements before changing CRD
- Document any discrepancies

---

## 🎮 Integration with GLITCHDEXMALL

**Remember the goal:** 3 credit cards as weapons in 1M+ sq ft mall dungeon

**Video2game provides:**
- Photorealistic textures → Material palettes
- Video-derived geometry → Validation of CRD measurements
- Spatial reference → Cross-check dimensions

**Voxel builder provides:**
- CRD-validated geometry → Ground truth structure
- Game-ready collision → Doom-alike physics
- Zone-based organization → Modular design

**Combined = Enhanced voxel mall with realistic textures**

See [INTEGRATION_GUIDE.md](docs/INTEGRATION_GUIDE.md) for the full workflow.

---

## 📞 Need Help?

**Installation issues?**
→ [INSTALLATION.md](docs/INSTALLATION.md)

**Processing problems?**
→ [PIPELINE_GUIDE.md](docs/PIPELINE_GUIDE.md#troubleshooting)

**Integration questions?**
→ [INTEGRATION_GUIDE.md](docs/INTEGRATION_GUIDE.md)

**Video2game bugs?**
→ https://github.com/video2game/video2game/issues

---

## ✅ Checklist

Before you start:
- [ ] NVIDIA GPU with 8GB+ VRAM
- [ ] CUDA 11.6 installed
- [ ] Python 3.7 environment
- [ ] 50GB+ free disk space
- [ ] 11-minute walkthrough video ready

After setup:
- [ ] System check passes (`python check_system.py`)
- [ ] Environment activated
- [ ] Dependencies installed
- [ ] Video in `input/` directory
- [ ] Ready to run pipeline

---

**Ready to begin? Run `python scripts/check_system.py` to verify your setup!**

For detailed guidance, start with [docs/INSTALLATION.md](docs/INSTALLATION.md).
