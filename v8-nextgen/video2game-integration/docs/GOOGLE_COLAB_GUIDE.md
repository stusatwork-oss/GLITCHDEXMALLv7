# Running Video2Game on Google Colab

**Process your 11-minute Eastland Mall walkthrough without local GPU hardware.**

This guide shows you how to run the video2game pipeline on Google Colab, using cloud GPUs to process your video.

## 💰 Cost Overview

| Colab Tier | GPU Available | Processing Time (11 min video) | Monthly Cost | Best For |
|------------|---------------|-------------------------------|--------------|----------|
| **Free** | T4 (16GB) | ~6-10 hours* | $0 | Testing, short videos |
| **Colab Pro** | T4/V100 | ~4-6 hours | $10/month | Single run |
| **Colab Pro+** | A100 (40GB) | ~2-4 hours | $50/month | Multiple runs, high quality |

*Session timeouts may require restarting - see "Handling Timeouts" below

**Recommendation:** Start with **Colab Pro** ($10) for a single high-quality run.

## 🚀 Quick Start

### Step 1: Upload Your Repository to Google Drive

```bash
# On your local machine, create a zip of the integration
cd v8-nextgen/video2game-integration
zip -r video2game-integration.zip . -x "output/*" -x "video2game/.git/*"

# Upload video2game-integration.zip to Google Drive
# Also upload your walkthrough.mp4 video
```

Or use Google Drive desktop sync to copy:
- `v8-nextgen/video2game-integration/` folder
- Your `walkthrough.mp4` video

### Step 2: Create Colab Notebook

1. Go to https://colab.research.google.com
2. **File → New notebook**
3. **Runtime → Change runtime type → GPU → A100** (if Pro+) or **T4/V100** (if Pro)
4. Save as: `Eastland_Mall_Video2Game_Processing.ipynb`

### Step 3: Copy the Notebook Template

Use the notebook template at the end of this guide, or follow the cells below.

## 📓 Colab Notebook Structure

### Cell 1: Mount Google Drive
```python
from google.colab import drive
drive.mount('/content/drive')

# Navigate to your working directory
import os
os.chdir('/content/drive/MyDrive/video2game-integration')

!pwd
!ls -la
```

### Cell 2: System Information
```python
# Check GPU allocation
!nvidia-smi

# Check CUDA version
!nvcc --version

# Check disk space
!df -h
```

### Cell 3: Install System Dependencies
```python
%%bash
# Update package list
apt-get update -qq

# Install COLMAP (from Ubuntu repos)
apt-get install -y colmap

# Install ffmpeg (usually already installed)
apt-get install -y ffmpeg

# Install build tools for V-HACD and other deps
apt-get install -y cmake build-essential

# Verify installations
echo "COLMAP version:"
colmap -h | head -1
echo "FFmpeg version:"
ffmpeg -version | head -1
```

### Cell 4: Setup Python Environment
```python
%%bash
# Clone video2game if not already present
if [ ! -d "video2game" ]; then
    git clone https://github.com/video2game/video2game.git
fi

# Note: Colab comes with Python 3.10, but we'll adapt for compatibility
# Check Python version
python --version
```

### Cell 5: Install PyTorch + CUDA
```python
# Colab usually has PyTorch pre-installed, but we may need specific version
# Check what's installed
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")

# If you need PyTorch 1.12 + CUDA 11.6 specifically (video2game requirement):
# Note: This might conflict with Colab's pre-installed version
# Test with existing version first, reinstall only if errors occur

# Uncomment if you need to force PyTorch 1.12:
# !pip install torch==1.12.0+cu116 torchvision==0.13.0+cu116 \
#     --extra-index-url https://download.pytorch.org/whl/cu116
```

### Cell 6: Install Video2Game Dependencies
```python
%%bash
# Install tiny-cuda-nn (NeRF acceleration)
pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch

# Install nvdiffrast (differentiable rendering)
pip install git+https://github.com/NVlabs/nvdiffrast/

# Install other dependencies
pip install pymeshlab
pip install trimesh
pip install opencv-python
pip install imageio
pip install scikit-image
pip install configargparse

# Verify critical installs
python -c "import tinycudann; print('✓ tiny-cuda-nn installed')"
python -c "import nvdiffrast; print('✓ nvdiffrast installed')"
```

### Cell 7: Prepare Video
```python
# Copy video from Drive to local Colab storage (faster processing)
import shutil
from pathlib import Path

# Adjust path to where you uploaded your video
video_source = Path('/content/drive/MyDrive/eastland_walkthrough.mp4')
video_dest = Path('input/walkthrough.mp4')

video_dest.parent.mkdir(exist_ok=True)
shutil.copy(video_source, video_dest)

print(f"✓ Video copied to {video_dest}")
print(f"  Size: {video_dest.stat().st_size / (1024**3):.2f} GB")

# Verify with ffprobe
!ffprobe -v quiet -print_format json -show_format -show_streams input/walkthrough.mp4
```

### Cell 8: Configure Processing
```python
# Create config for Colab (optimized for available GPU)
import json

# Check GPU memory
gpu_mem_gb = !nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits
gpu_mem_gb = int(gpu_mem_gb[0]) / 1024

print(f"GPU Memory: {gpu_mem_gb:.1f} GB")

# Adjust config based on GPU
if gpu_mem_gb >= 40:  # A100
    config = {
        "frame_extraction": {"fps": 3},
        "nerf": {"max_steps": 50000, "batch_size": 16384},
        "mesh": {"resolution": 1024},
        "texture": {"resolution": 4096}
    }
    print("Config: HIGH QUALITY (A100)")
elif gpu_mem_gb >= 16:  # V100/T4
    config = {
        "frame_extraction": {"fps": 2},
        "nerf": {"max_steps": 30000, "batch_size": 8192},
        "mesh": {"resolution": 512},
        "texture": {"resolution": 2048}
    }
    print("Config: BALANCED (V100/T4)")
else:  # Lower memory
    config = {
        "frame_extraction": {"fps": 2},
        "nerf": {"max_steps": 20000, "batch_size": 4096},
        "mesh": {"resolution": 256},
        "texture": {"resolution": 1024}
    }
    print("Config: LOW MEMORY")

# Save config
with open('colab_config.json', 'w') as f:
    json.dump(config, f, indent=2)

!cat colab_config.json
```

### Cell 9: Run Processing Pipeline
```python
# This is the main processing cell - will take 2-8 hours
# Monitor progress in output

!python scripts/process_walkthrough.py \
    --video input/walkthrough.mp4 \
    --output output/eastland_colab \
    --config colab_config.json
```

### Cell 10: Monitor Progress (Run in Parallel)
```python
# Run this in a separate cell while Cell 9 is running
import time
from pathlib import Path

log_files = list(Path('output/eastland_colab').glob('processing_log_*.txt'))

if log_files:
    log_file = log_files[0]
    print(f"Monitoring: {log_file}")
    print("="*60)

    # Tail the log file
    !tail -f {log_file}
else:
    print("No log file found yet. Wait for processing to start...")
```

### Cell 11: Backup Progress to Drive (Important!)
```python
# Run this periodically to backup progress in case of timeout
# Especially important for long-running processes

!rsync -av --progress output/eastland_colab/ \
    /content/drive/MyDrive/video2game-integration/output/eastland_colab/

print("✓ Progress backed up to Google Drive")
```

### Cell 12: Check Outputs
```python
# After processing completes, verify outputs
!ls -lh output/eastland_colab/exports/
!ls -lh output/eastland_colab/textured/
!ls -lh output/eastland_colab/mesh/

# Check file sizes
!du -sh output/eastland_colab/*
```

### Cell 13: Download Results
```python
# Option A: Download via Colab interface
from google.colab import files

# Download the final GLB file
files.download('output/eastland_colab/exports/mall.glb')

# Download texture
files.download('output/eastland_colab/textured/mall_diffuse.png')

# Download metadata
files.download('output/eastland_colab/processing_metadata.json')
```

```python
# Option B: Already saved to Google Drive (from Cell 11)
# Just access from your Drive folder:
# MyDrive/video2game-integration/output/eastland_colab/
```

## ⏱️ Handling Session Timeouts

Colab sessions timeout after:
- **Free tier:** 12 hours (90 minutes idle)
- **Pro:** 24 hours (90 minutes idle)
- **Pro+:** 24 hours (90 minutes idle)

### Strategy 1: Keep-Alive Script
Add this to a cell and run it:

```python
# Keep session alive by printing periodically
import time
from datetime import datetime

def keep_alive():
    while True:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Still running...")
        time.sleep(300)  # Print every 5 minutes

# Run in background (won't block other cells)
import threading
thread = threading.Thread(target=keep_alive, daemon=True)
thread.start()
```

### Strategy 2: Checkpoint and Resume
Modify the pipeline to save checkpoints:

```python
# Add to your config
{
    "checkpoint_frequency": 5000,  # Save every 5000 NeRF steps
    "resume_from_checkpoint": True
}
```

If session dies:
1. Restart runtime
2. Re-run setup cells (1-7)
3. Pipeline will resume from last checkpoint

### Strategy 3: Segmented Processing
Process in stages instead of all at once:

```python
# Stage 1: Frame extraction + COLMAP (30-60 min)
!python scripts/stage1_extract_and_colmap.py

# Backup to Drive
!rsync -av output/ /content/drive/MyDrive/video2game-integration/output/

# Stage 2: NeRF training (2-4 hours)
!python scripts/stage2_train_nerf.py

# Backup again
!rsync -av output/ /content/drive/MyDrive/video2game-integration/output/

# Stage 3: Mesh + textures (1 hour)
!python scripts/stage3_mesh_and_texture.py

# Final backup
!rsync -av output/ /content/drive/MyDrive/video2game-integration/output/
```

## 🔧 Troubleshooting

### "CUDA out of memory"
```python
# Reduce config values
config = {
    "nerf": {"batch_size": 2048},  # Lower batch size
    "mesh": {"resolution": 256},   # Lower resolution
    "texture": {"resolution": 1024}
}
```

### "Session disconnected"
1. Check Google Drive backup (Cell 11)
2. Restart runtime
3. Re-run setup cells
4. Resume from checkpoint

### "Disk space full"
```python
# Colab has ~100GB space, but video processing uses a lot
# Clean intermediate files:
!rm -rf output/eastland_colab/intermediate/frames/  # After COLMAP
!rm -rf output/eastland_colab/intermediate/colmap/  # After NeRF

# Or mount additional Drive space
```

### "Package conflicts"
```python
# Colab's pre-installed packages can conflict
# Create isolated pip install:
!pip install --upgrade --force-reinstall <package>

# Or use specific versions
!pip install torch==1.12.0+cu116 --force-reinstall
```

## 💾 Storage Management

**Colab Disk Space:** ~100-200 GB

**Your Processing Needs:**
- Input video: ~1-5 GB
- Extracted frames: ~2-5 GB
- COLMAP data: ~1-2 GB
- NeRF checkpoints: ~0.5 GB
- Final outputs: ~1-3 GB
- **Total: ~6-16 GB**

**Should fit comfortably**, but backup to Drive frequently.

## 🎯 Optimization Tips

### For Fastest Processing (Pro+)
```python
config = {
    "frame_extraction": {"fps": 2},  # Don't go too high
    "nerf": {
        "max_steps": 30000,  # Balance quality/speed
        "batch_size": 16384   # Max for A100
    },
    "mesh": {"resolution": 512},
    "texture": {"resolution": 2048}
}
```

### For Best Quality (Even if slower)
```python
config = {
    "frame_extraction": {"fps": 3},
    "nerf": {
        "max_steps": 100000,  # Much longer training
        "batch_size": 16384
    },
    "mesh": {"resolution": 1024},
    "texture": {"resolution": 4096}
}
```

### For Testing (Fast iteration)
```python
config = {
    "frame_extraction": {"fps": 1},
    "nerf": {"max_steps": 5000},  # Very quick test
    "mesh": {"resolution": 128},
    "texture": {"resolution": 512}
}
# ~30 minutes total
```

## 📋 Complete Workflow Checklist

**Before Starting:**
- [ ] Subscribe to Colab Pro/Pro+ ($10-50/month)
- [ ] Upload video to Google Drive
- [ ] Upload v8-nextgen/video2game-integration to Drive
- [ ] Have 3-8 hours available (for monitoring)

**During Processing:**
- [ ] Run all setup cells (1-7)
- [ ] Start main processing (Cell 9)
- [ ] Monitor progress (Cell 10)
- [ ] Backup to Drive every hour (Cell 11)
- [ ] Keep session alive (run keep-alive script)

**After Completion:**
- [ ] Verify outputs (Cell 12)
- [ ] Download results (Cell 13)
- [ ] Cancel Colab Pro if one-time use
- [ ] Back up to Drive (redundant safety)

## 🆚 Colab vs Local Processing

| Aspect | Local (High-End GPU) | Google Colab Pro+ |
|--------|---------------------|-------------------|
| **Hardware** | RTX 4090 ($1600) | A100 (rent $50/mo) |
| **Setup** | Complex (CUDA, drivers) | Simple (pre-configured) |
| **Processing** | 2-4 hours | 2-4 hours (similar) |
| **Cost** | High upfront | Low monthly |
| **Re-runs** | Free after purchase | $50/month |
| **Portability** | Tied to machine | Access anywhere |

**Verdict:** For **one-time processing**, Colab Pro is perfect. For **repeated use**, local GPU or cheaper clouds (Vast.ai) better.

## 🔗 Alternative Cloud Options

If Colab doesn't work:

**RunPod** (~$0.50-1.50/hour)
```bash
# SSH into RunPod instance
ssh root@runpod-instance

# Clone repo
git clone <your-repo>
cd video2game-integration

# Run processing
python scripts/process_walkthrough.py --video input/video.mp4
```

**Lambda Labs** (~$1.10/hour for A100)
```bash
# More expensive but very reliable
# Similar SSH workflow
```

**Vast.ai** (~$0.20-0.80/hour)
```bash
# Cheapest option
# Community hardware (reliability varies)
```

## 📞 Getting Help

**Colab Issues:**
- Check Colab FAQ: https://research.google.com/colaboratory/faq.html
- Runtime issues: Try **Runtime → Factory reset runtime**

**Video2Game Issues:**
- See main docs: `INSTALLATION.md`, `PIPELINE_GUIDE.md`
- Check logs in `output/eastland_colab/processing_log_*.txt`

**Session Timeouts:**
- Use backup strategy (Cell 11)
- Run overnight (less idle timeout risk)
- Use keep-alive script

## 🎬 Ready to Process?

1. **Sign up for Colab Pro** ($10) - https://colab.research.google.com/signup
2. **Upload your video** to Google Drive
3. **Create new notebook** and copy the template below
4. **Run the cells** in order
5. **Wait 4-6 hours** (backup frequently!)
6. **Download your 3D mall** and integrate with voxel_builder

---

## 📓 Complete Notebook Template

Save this as: `Eastland_Mall_Video2Game.ipynb`

```python
# ============================================================================
# EASTLAND MALL VIDEO2GAME PROCESSING
# Google Colab Edition
# ============================================================================

# CELL 1: Mount Drive
from google.colab import drive
drive.mount('/content/drive')

import os
os.chdir('/content/drive/MyDrive/video2game-integration')
!pwd

# CELL 2: Check GPU
!nvidia-smi
!nvcc --version

# CELL 3: Install System Dependencies
%%bash
apt-get update -qq
apt-get install -y colmap ffmpeg cmake build-essential
colmap -h | head -1

# CELL 4: Setup Python
%%bash
if [ ! -d "video2game" ]; then
    git clone https://github.com/video2game/video2game.git
fi

# CELL 5: Check PyTorch
import torch
print(f"PyTorch: {torch.__version__}")
print(f"CUDA: {torch.cuda.is_available()}")

# CELL 6: Install Video2Game Dependencies
%%bash
pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
pip install git+https://github.com/NVlabs/nvdiffrast/
pip install pymeshlab trimesh opencv-python imageio scikit-image configargparse
python -c "import tinycudann; print('✓ tiny-cuda-nn OK')"

# CELL 7: Prepare Video
import shutil
from pathlib import Path

video_source = Path('/content/drive/MyDrive/eastland_walkthrough.mp4')
video_dest = Path('input/walkthrough.mp4')
video_dest.parent.mkdir(exist_ok=True)
shutil.copy(video_source, video_dest)
print(f"✓ Video ready: {video_dest}")

# CELL 8: Configure
import json

config = {
    "frame_extraction": {"fps": 2},
    "nerf": {"max_steps": 30000, "batch_size": 8192},
    "mesh": {"resolution": 512},
    "texture": {"resolution": 2048}
}

with open('colab_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print("Config saved")

# CELL 9: Keep-Alive (run this in background)
import time
from datetime import datetime
import threading

def keep_alive():
    while True:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Running...")
        time.sleep(300)

thread = threading.Thread(target=keep_alive, daemon=True)
thread.start()

# CELL 10: Process (MAIN - takes 4-6 hours)
!python scripts/process_walkthrough.py \
    --video input/walkthrough.mp4 \
    --output output/eastland_colab \
    --config colab_config.json

# CELL 11: Backup to Drive (run periodically during processing)
!rsync -av --progress output/eastland_colab/ \
    /content/drive/MyDrive/video2game-integration/output/eastland_colab/
print("✓ Backed up to Drive")

# CELL 12: Verify Results
!ls -lh output/eastland_colab/exports/
!du -sh output/eastland_colab/*

# CELL 13: Download
from google.colab import files
files.download('output/eastland_colab/exports/mall.glb')
files.download('output/eastland_colab/processing_metadata.json')

print("✓ Processing complete! Check your Downloads folder.")
```

Copy this entire template into a new Colab notebook and run cells in order.

---

**Total Cost for Single Run:**
- Colab Pro: **$10** (1 month)
- Processing time: **4-6 hours**
- Result: **Photorealistic 3D mall mesh**

**Way cheaper than buying a GPU!** 🎉
