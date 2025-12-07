#!/usr/bin/env python3
"""
System requirements checker for video2game integration.
Verifies GPU, CUDA, dependencies, and disk space.
"""

import sys
import subprocess
import shutil
from pathlib import Path

def check_command(command):
    """Check if a command exists."""
    return shutil.which(command) is not None

def get_gpu_info():
    """Get GPU information using nvidia-smi."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def check_cuda():
    """Check CUDA availability."""
    try:
        result = subprocess.run(
            ["nvcc", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        # Extract version
        for line in result.stdout.split('\n'):
            if 'release' in line.lower():
                return line.strip()
        return "Found (version unknown)"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def check_python_packages():
    """Check if required Python packages are installed."""
    packages = {
        "torch": "PyTorch",
        "tinycudann": "tiny-cuda-nn",
        "nvdiffrast": "nvdiffrast",
        "numpy": "NumPy",
        "PIL": "Pillow"
    }

    results = {}
    for package, name in packages.items():
        try:
            __import__(package)
            results[name] = "✓ Installed"
        except ImportError:
            results[name] = "✗ Not installed"

    return results

def check_disk_space():
    """Check available disk space."""
    try:
        stat = shutil.disk_usage(".")
        free_gb = stat.free / (1024**3)
        total_gb = stat.total / (1024**3)
        return free_gb, total_gb
    except Exception:
        return None, None

def main():
    print("="*60)
    print("VIDEO2GAME SYSTEM REQUIREMENTS CHECK")
    print("="*60)
    print()

    all_good = True

    # Check Python version
    print("Python Version:")
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info.major == 3 and sys.version_info.minor == 7:
        print(f"  ✓ Python {py_version} (required: 3.7)")
    else:
        print(f"  ✗ Python {py_version} (required: 3.7)")
        print(f"    WARNING: Video2game requires Python 3.7")
        all_good = False
    print()

    # Check GPU
    print("GPU:")
    gpu_info = get_gpu_info()
    if gpu_info:
        print(f"  ✓ {gpu_info}")
        # Check VRAM
        vram = gpu_info.split(',')[1].strip() if ',' in gpu_info else "unknown"
        if "MiB" in vram:
            vram_mb = int(vram.split()[0])
            if vram_mb >= 8000:
                print(f"    ✓ VRAM: {vram_mb} MiB (recommended: 8192+ MiB)")
            else:
                print(f"    ⚠ VRAM: {vram_mb} MiB (recommended: 8192+ MiB)")
                print(f"      You may need to use low-VRAM config")
    else:
        print("  ✗ No NVIDIA GPU found or nvidia-smi not available")
        print("    Video2game requires an NVIDIA GPU with CUDA support")
        all_good = False
    print()

    # Check CUDA
    print("CUDA:")
    cuda_info = check_cuda()
    if cuda_info:
        print(f"  ✓ {cuda_info}")
        if "11.6" in cuda_info:
            print(f"    ✓ CUDA 11.6 found (required)")
        else:
            print(f"    ⚠ CUDA version may not be 11.6 (required: 11.6)")
            print(f"      Video2game specifically requires CUDA 11.6")
    else:
        print("  ✗ CUDA not found")
        print("    Install CUDA 11.6 toolkit")
        all_good = False
    print()

    # Check Python packages
    print("Python Packages:")
    packages = check_python_packages()
    for name, status in packages.items():
        print(f"  {status}: {name}")
        if "✗" in status:
            all_good = False
    print()

    # Check external tools
    print("External Tools:")
    tools = {
        "ffmpeg": "Video processing",
        "colmap": "Camera reconstruction",
        "blender": "Mesh viewing (optional)"
    }
    for tool, desc in tools.items():
        if check_command(tool):
            print(f"  ✓ {tool} - {desc}")
        else:
            status = "optional" if tool == "blender" else "required"
            print(f"  ✗ {tool} - {desc} ({status})")
            if status == "required":
                all_good = False
    print()

    # Check disk space
    print("Disk Space:")
    free_gb, total_gb = check_disk_space()
    if free_gb is not None:
        print(f"  Free: {free_gb:.1f} GB / {total_gb:.1f} GB")
        if free_gb >= 50:
            print(f"  ✓ Sufficient space (recommended: 50+ GB)")
        else:
            print(f"  ⚠ Low disk space (recommended: 50+ GB)")
            print(f"    You may need to free up space or use external storage")
    print()

    # Summary
    print("="*60)
    if all_good:
        print("✓ SYSTEM READY FOR VIDEO2GAME")
        print("="*60)
        print()
        print("Next steps:")
        print("  1. Place your video in input/")
        print("  2. Run: python process_walkthrough.py --video ../input/video.mp4")
        print()
        return 0
    else:
        print("✗ SYSTEM NOT READY")
        print("="*60)
        print()
        print("Please resolve the issues above before proceeding.")
        print("See docs/INSTALLATION.md for detailed setup instructions.")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
