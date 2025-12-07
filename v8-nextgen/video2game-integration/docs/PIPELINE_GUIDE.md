# Video2Game Pipeline Guide for Eastland Mall

## Overview
This guide walks through processing your 11-minute Eastland Mall walkthrough video into game-ready 3D assets using the video2game pipeline.

## Prerequisites
- Complete installation from `INSTALLATION.md`
- Walkthrough video file (11 minutes, any common format)
- NVIDIA GPU with 8GB+ VRAM
- 50GB+ free disk space

## Quick Start

### 1. Place Your Video
```bash
# Copy your walkthrough video to the input directory
cp /path/to/your/walkthrough.mp4 v8-nextgen/video2game-integration/input/
```

### 2. Run the Pipeline
```bash
cd v8-nextgen/video2game-integration/scripts

# Activate video2game environment
conda activate video2game  # or: pyenv activate video2game

# Process the video
python process_walkthrough.py \
    --video ../input/walkthrough.mp4 \
    --output ../output/eastland_mall_$(date +%Y%m%d)
```

### 3. Monitor Progress
The pipeline will run through 8 stages (estimated time: 4-8 hours for 11-minute video):

1. **Frame Extraction** (~5 minutes)
   - Extracts 2 frames per second = ~1320 frames
   - Output: `intermediate/frames/`

2. **COLMAP Reconstruction** (~30-60 minutes)
   - Camera pose estimation
   - Feature matching and sparse reconstruction
   - Output: `intermediate/colmap/`

3. **NeRF Training** (~2-4 hours)
   - Neural radiance field learning
   - 30,000 training steps
   - Output: `nerf/`

4. **Mesh Extraction** (~30 minutes)
   - Convert NeRF to polygon mesh
   - Marching cubes + decimation
   - Output: `mesh/`

5. **Texture Baking** (~30-60 minutes)
   - Bake NeRF appearance onto mesh
   - 2048x2048 texture maps
   - Output: `textured/`

6. **Collision Generation** (~15 minutes)
   - V-HACD convex decomposition
   - Game engine physics ready
   - Output: `collision/`

7. **Asset Export** (~5 minutes)
   - GLB and OBJ formats
   - Packaged with textures
   - Output: `exports/`

8. **Metadata Generation** (~1 minute)
   - Integration instructions
   - Scale calibration data
   - Output: `processing_metadata.json`

## Configuration

### Custom Config File
Create a JSON config to override defaults:

```json
{
  "nerf": {
    "max_steps": 50000,
    "batch_size": 8192,
    "semantic_labels": true
  },
  "mesh": {
    "resolution": 1024,
    "decimate_target": 200000
  },
  "texture": {
    "resolution": 4096
  }
}
```

Use with:
```bash
python process_walkthrough.py \
    --video ../input/walkthrough.mp4 \
    --output ../output/high_quality \
    --config custom_config.json
```

### Performance Tuning

**For Lower VRAM (6-8GB):**
```json
{
  "nerf": {
    "batch_size": 2048
  },
  "mesh": {
    "resolution": 256
  },
  "texture": {
    "resolution": 1024
  }
}
```

**For Higher Quality (16GB+ VRAM):**
```json
{
  "nerf": {
    "max_steps": 100000,
    "batch_size": 16384
  },
  "mesh": {
    "resolution": 1024
  },
  "texture": {
    "resolution": 4096
  }
}
```

## Pipeline Outputs

### Directory Structure
```
output/eastland_mall_YYYYMMDD/
├── nerf/                          # NeRF model checkpoint
│   ├── model.pth
│   └── config.json
├── mesh/                          # Extracted geometry
│   ├── mall.obj
│   └── mall.ply
├── textured/                      # Textured mesh
│   ├── mall_textured.obj
│   ├── mall_diffuse.png
│   └── mall_normal.png (optional)
├── collision/                     # Physics meshes
│   ├── mall_collision.obj
│   └── hulls_*.obj
├── exports/                       # Game-ready assets
│   ├── mall.glb                   # Recommended for engines
│   └── mall_bundle.obj            # With MTL + textures
├── intermediate/                  # Processing artifacts
│   ├── frames/
│   └── colmap/
├── processing_metadata.json       # Integration data
└── processing_log_*.txt          # Full pipeline log
```

### Using the Outputs

**For Voxel Builder Integration:**
- Use `processing_metadata.json` for scale reference
- Compare mesh geometry with CRD measurements
- Use textures for voxel material generation

**For Direct Game Engine Import:**
- Import `exports/mall.glb` into Unity/Unreal/Godot
- Collision meshes in `collision/` for physics
- Scale and align to match measurement data

**For Texture Reference:**
- `textured/mall_diffuse.png` - realistic appearance
- Use to inform voxel texturing or material creation
- Cross-reference with photo evidence

## Troubleshooting

### Issue: COLMAP fails to reconstruct
**Symptoms:** "No reconstruction found" or "Insufficient correspondences"

**Solutions:**
1. Video may have too much motion blur
2. Lighting changes too drastically
3. Not enough unique features

**Fixes:**
```bash
# Extract more frames (increase fps)
# Edit config: "frame_extraction": {"fps": 5}

# Use sequential matching instead of exhaustive
colmap sequential_matcher --database_path database.db
```

### Issue: NeRF training is slow
**Symptoms:** Training stuck at low steps, no progress

**Solutions:**
```bash
# Reduce batch size
# Edit config: "nerf": {"batch_size": 2048}

# Monitor GPU usage
nvidia-smi -l 1

# Check if tiny-cuda-nn is being used
# Should see "Using tiny-cuda-nn" in logs
```

### Issue: Out of memory errors
**Symptoms:** "CUDA out of memory"

**Solutions:**
1. Reduce mesh resolution
2. Decrease batch size
3. Lower texture resolution
4. Process in segments (split video)

### Issue: Mesh has holes or artifacts
**Symptoms:** Missing geometry, weird triangles

**Solutions:**
1. Increase NeRF training steps
2. Adjust mesh extraction threshold
3. Clean mesh manually in Blender

## Scale Calibration

The video2game output will be in arbitrary units. You need to calibrate to Eastland Mall's real dimensions:

### 1. Identify Reference Features
Look for these in the mesh:
- Food court pit (should be 8 feet deep)
- Atrium diameter (should be 175 feet)
- Store frontages (typically 20-40 feet)

### 2. Measure in Mesh
```python
# Using pymesh or open in Blender
import pymesh

mesh = pymesh.load_mesh("mesh/mall.obj")
# Measure distance between known points
# Calculate scale factor
```

### 3. Apply Scaling
```python
scale_factor = real_dimension_feet / mesh_dimension_units

# Apply to mesh before export
mesh.vertices *= scale_factor
```

### 4. Cross-Reference with CRD Data
```bash
# Compare with canonical measurements
cat ../../data/measurements/spatial_measurements.json

# Document any discrepancies
# Video-derived geometry is reference, not ground truth
```

## Next Steps

After successful processing:

1. **Review outputs** - Check mesh quality in Blender/MeshLab
2. **Calibrate scale** - Match to CRD measurements
3. **Integration** - See `INTEGRATION_GUIDE.md` for voxel_builder workflow
4. **Iteration** - Re-process sections if needed with adjusted config

## Advanced: Segmented Processing

For better results, consider processing the video in segments:

```bash
# Split video by zone
ffmpeg -i walkthrough.mp4 -ss 00:00:00 -t 00:02:00 segment_atrium.mp4
ffmpeg -i walkthrough.mp4 -ss 00:02:00 -t 00:03:00 segment_food_court.mp4
# ... etc

# Process each segment separately
for segment in segment_*.mp4; do
    python process_walkthrough.py --video $segment --output output/${segment%.mp4}
done

# Merge meshes in post-processing
```

This gives:
- Higher quality per zone
- Better semantic separation
- Easier debugging
- Manageable memory usage

## Resources

- Video2Game docs: https://github.com/video2game/video2game
- COLMAP docs: https://colmap.github.io/
- NeRF resources: https://www.matthewtancik.com/nerf
- V-HACD: https://github.com/kmammou/v-hacd

## Tips for Best Results

1. **Video Quality**
   - Steady camera movement (use gimbal/stabilization)
   - Consistent lighting (avoid dramatic shadows)
   - Good overlap between frames
   - Clear textures (avoid blur)

2. **Camera Movement**
   - Slow, steady panning
   - Circular paths around features
   - Multiple heights/angles
   - Pause on important details

3. **Lighting**
   - Even ambient lighting ideal
   - Avoid direct sun/spotlights
   - Overcast days = best outdoor capture
   - For interior: fluorescent/LED preferable

4. **Coverage**
   - Capture all angles of each zone
   - Don't rush - overlap is good
   - Include floor and ceiling
   - Document scale references in frame

---

**Processing Time Estimate for 11-Minute Video:**
- Fast (low quality): 2-3 hours
- Normal (default): 4-6 hours
- High quality: 8-12 hours

**Disk Space Used:**
- Frames: ~2-5 GB
- COLMAP: ~1-2 GB
- NeRF: ~500 MB
- Meshes: ~500 MB - 2 GB
- Textures: ~100 MB - 1 GB
- **Total: ~5-12 GB**
