"""
GLITCHDEX MALL - Single-File Executable Builder
Simplest possible build - no external dependencies, just PyInstaller
"""

import subprocess
import sys
import os


print("\n" + "="*80)
print("GLITCHDEX MALL - Executable Builder")
print("="*80)

# Step 1: Install PyInstaller
print("\n[1] Installing PyInstaller (one-time setup)...")
print("    This may take a minute...")

result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "pyinstaller", "-q"],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"ERROR: {result.stderr}")
    sys.exit(1)

print("    ✓ PyInstaller installed")

# Step 2: Clean old builds
print("\n[2] Cleaning old builds...")
for folder in ["build", "dist"]:
    if os.path.exists(folder):
        import shutil
        shutil.rmtree(folder, ignore_errors=True)
        print(f"    ✓ Removed {folder}/")

# Step 3: Build
print("\n[3] Building executable...")
print("    This may take 30-60 seconds...\n")

result = subprocess.run(
    [sys.executable, "-m", "PyInstaller", "glitchdex_mall.spec"],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("BUILD FAILED!")
    print("\nError output:")
    print(result.stderr)
    print("\nStandard output:")
    print(result.stdout)
    sys.exit(1)

# Step 4: Verify
print("\n[4] Verifying build...")

exe_path = "dist/glitchdex-mall/glitchdex-mall.exe"
if os.path.exists(exe_path):
    size_mb = os.path.getsize(exe_path) / (1024*1024)
    print(f"    ✓ Found executable: {exe_path}")
    print(f"    ✓ Size: {size_mb:.1f} MB")
else:
    print(f"    ✗ Executable not found!")
    print(f"\n    Listing dist/ contents:")
    if os.path.exists("dist"):
        for item in os.listdir("dist"):
            print(f"      - {item}")
    sys.exit(1)

# Success!
print("\n" + "="*80)
print("SUCCESS!")
print("="*80)
print(f"\nYour game is ready!")
print(f"\nLocation: dist\\glitchdex-mall\\glitchdex-mall.exe")
print(f"\nNext: Go to that folder and double-click the .exe to play!")
print("\n" + "="*80 + "\n")
