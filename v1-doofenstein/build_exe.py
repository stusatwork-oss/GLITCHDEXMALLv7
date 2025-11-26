"""
GLITCHDEX MALL - Windows Build Script
Robust builder with detailed error messages and progress reporting
"""

import os
import sys
import subprocess
import shutil


def run_command(cmd, description):
    """Run a command and show output"""
    print(f"\n[*] {description}...")
    print(f"    Command: {cmd}\n")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        if result.returncode != 0:
            print(f"\n[!] ERROR: Command failed with code {result.returncode}")
            return False
        print(f"[✓] {description} - SUCCESS\n")
        return True
    except Exception as e:
        print(f"[!] ERROR: {e}")
        return False


def main():
    print("\n" + "="*70)
    print("GLITCHDEX MALL - Windows Build Script")
    print("="*70)

    # Step 1: Check Python
    print("\n[1/5] Checking Python installation...")
    try:
        version = subprocess.check_output([sys.executable, "--version"], text=True)
        print(f"    Found: {version.strip()}")
        print("[✓] Python check - SUCCESS\n")
    except Exception as e:
        print(f"[!] ERROR: Python not found - {e}")
        return False

    # Step 2: Install PyInstaller
    if not run_command(
        f"{sys.executable} -m pip install pyinstaller",
        "Installing PyInstaller"
    ):
        return False

    # Step 3: Clean old builds
    print("[3/5] Cleaning old builds...")
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            print(f"    Removing {folder}/...")
            shutil.rmtree(folder, ignore_errors=True)
    print("[✓] Clean - SUCCESS\n")

    # Step 4: Verify data files exist
    print("[4/5] Verifying required files...")
    required_dirs = ["data", "src"]
    required_files = [
        "glitchdex_mall.spec",
        "src/main.py",
        "data/mall_map.json",
        "data/entities.json",
        "data/artifacts.json",
        "data/stores.json",
    ]

    all_good = True
    for path in required_dirs + required_files:
        if os.path.exists(path):
            print(f"    ✓ {path}")
        else:
            print(f"    ✗ MISSING: {path}")
            all_good = False

    if not all_good:
        print("[!] ERROR: Missing required files!")
        return False

    print("[✓] Files check - SUCCESS\n")

    # Step 5: Build executable
    if not run_command(
        f"{sys.executable} -m PyInstaller glitchdex_mall.spec",
        "Building executable with PyInstaller"
    ):
        return False

    # Step 6: Verify build succeeded
    print("[5/5] Verifying build output...")
    exe_path = "dist/glitchdex-mall/glitchdex-mall.exe"
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"    ✓ Found: {exe_path}")
        print(f"    ✓ Size: {size_mb:.1f} MB")
        print("[✓] Build verification - SUCCESS\n")
    else:
        print(f"[!] ERROR: Executable not found at {exe_path}")
        print(f"    Listing dist/ contents:")
        if os.path.exists("dist"):
            for root, dirs, files in os.walk("dist"):
                level = root.replace("dist", "").count(os.sep)
                indent = " " * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                sub_indent = " " * 2 * (level + 1)
                for file in files[:10]:  # Limit to first 10 files
                    print(f"{sub_indent}{file}")
        return False

    # Success!
    print("="*70)
    print("BUILD SUCCESSFUL!")
    print("="*70)
    print(f"\nYour executable is ready at:")
    print(f"  {exe_path}")
    print(f"\nNext steps:")
    print(f"  1. Navigate to: dist\\glitchdex-mall\\")
    print(f"  2. Double-click: glitchdex-mall.exe")
    print(f"  3. Enjoy the game!")
    print("\n" + "="*70 + "\n")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
