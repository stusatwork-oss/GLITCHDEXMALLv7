# Video2Game Installation Guide

## Overview
This guide covers installing video2game to process the 11-minute Eastland Mall walkthrough video into game-ready 3D assets.

## System Requirements

### Hardware
- **GPU**: NVIDIA GPU with CUDA support (minimum 8GB VRAM recommended)
- **RAM**: 16GB+ recommended
- **Storage**: 50GB+ free space for video processing and outputs

### Software Prerequisites
- **Python**: 3.7 (specific version required)
- **CUDA**: 11.6
- **PyTorch**: 1.12 with CUDA 11.6 support

## Installation Steps

### 1. Clone Video2Game Repository
```bash
cd v8-nextgen/video2game-integration/
git clone https://github.com/video2game/video2game.git
cd video2game
```

### 2. Create Python 3.7 Environment
```bash
# Using conda (recommended)
conda create -n video2game python=3.7
conda activate video2game

# OR using pyenv
pyenv install 3.7.16
pyenv virtualenv 3.7.16 video2game
pyenv activate video2game
```

### 3. Install PyTorch 1.12 + CUDA 11.6
```bash
pip install torch==1.12.0+cu116 torchvision==0.13.0+cu116 --extra-index-url https://download.pytorch.org/whl/cu116
```

### 4. Install Core Dependencies
```bash
# Install tiny-cuda-nn (NeRF acceleration)
pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch

# Install nvdiffrast (differentiable rendering)
pip install git+https://github.com/NVlabs/nvdiffrast/

# Install torch-scatter
pip install torch-scatter -f https://data.pyg.org/whl/torch-1.12.0+cu116.html

# Install pymesh (mesh processing)
# Note: pymesh can be tricky, may need to build from source
pip install pymesh
```

### 5. Install V-HACD (Collision Decomposition)
```bash
# Download and compile V-HACD
git clone https://github.com/kmammou/v-hacd.git
cd v-hacd
mkdir build && cd build
cmake ..
make
# Add to PATH or note location for config
```

### 6. Install COLMAP (Camera Reconstruction)
```bash
# On Ubuntu/Debian
sudo apt-get install colmap

# On macOS
brew install colmap

# Or build from source: https://colmap.github.io/install.html
```

### 7. Install Remaining Dependencies
```bash
cd v8-nextgen/video2game-integration/video2game
pip install -r requirements.txt
```

## Verification

### Test Installation
```bash
python -c "import torch; print(torch.cuda.is_available())"  # Should print True
python -c "import tinycudann; print('tiny-cuda-nn OK')"
python -c "import nvdiffrast; print('nvdiffrast OK')"
```

### GPU Check
```bash
nvidia-smi  # Verify CUDA is accessible
```

## Common Issues

### Issue: tiny-cuda-nn compilation fails
**Solution**: Ensure CUDA toolkit 11.6 is installed and nvcc is in PATH
```bash
nvcc --version  # Should show CUDA 11.6
export CUDA_HOME=/usr/local/cuda-11.6
```

### Issue: pymesh installation fails
**Solution**: Build from source
```bash
git clone https://github.com/PyMesh/PyMesh.git
cd PyMesh
git submodule update --init --recursive
pip install .
```

### Issue: Out of GPU memory during processing
**Solution**: Reduce batch size or resolution in config files

## Next Steps

After installation, proceed to:
1. `PIPELINE_GUIDE.md` - How to process the walkthrough video
2. `INTEGRATION_GUIDE.md` - How to integrate outputs with voxel_builder

## Status Tracking

Five of seven modules are currently complete in video2game:
- ✅ NeRF training
- ✅ Mesh extraction
- ✅ Baking pretraining
- ✅ Collision generation
- ✅ Evaluation code
- ⏳ Baking finetuning (in progress)
- ⏳ GPT-4 integration (planned)

The current version is sufficient for basic video-to-mesh conversion.

## Resources

- Video2Game GitHub: https://github.com/video2game/video2game
- Paper/Documentation: Check repo for latest research paper
- Issues: Report problems to video2game repo
