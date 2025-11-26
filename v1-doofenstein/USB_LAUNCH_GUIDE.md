# USB LAUNCH GUIDE – DOOFENSTEIN 3D
## Nintendo Cartridge-Level Simplicity for Distribution

This guide shows you how to package DOOFENSTEIN 3D for **plug-and-play USB distribution**, making it as simple as inserting a Nintendo cartridge.

---

## 🎯 Goal

Create a USB drive or downloadable package where users can:
1. Plug in USB (or extract ZIP)
2. Double-click `PLAY.bat` (Windows) or run `bash PLAY.sh` (Mac/Linux)
3. Start playing immediately

**No installation. No configuration. Just play.**

---

## 📦 METHOD 1: USB Drive Distribution (Portable)

### What You Need
- USB drive (256 MB+ sufficient)
- Python 3.8+ installed on target machine (or use PyInstaller for truly standalone)

### Step 1: Prepare the USB Drive

1. **Format USB drive** (optional but recommended):
   - Format as FAT32 (maximum compatibility)
   - Label it `DOOFENSTEIN_3D`

2. **Copy entire project to USB**:
   ```
   USB:/
   ├── src/              (all .py files)
   ├── data/             (all .json files)
   ├── PLAY.bat
   ├── PLAY.sh
   ├── README.md
   ├── DOOFENSTEIN_README.md
   └── USB_LAUNCH_GUIDE.md
   ```

3. **Make launch scripts executable** (Linux/Mac):
   ```bash
   chmod +x PLAY.sh
   ```

### Step 2: Test the USB Drive

**Windows**:
1. Plug in USB
2. Open USB drive in Explorer
3. Double-click `PLAY.bat`
4. Game should launch immediately

**Mac/Linux**:
1. Plug in USB
2. Open Terminal
3. Navigate to USB drive: `cd /Volumes/DOOFENSTEIN_3D`
4. Run: `bash PLAY.sh`
5. Game should launch immediately

### Requirements for Target Machine
- **Python 3.8 or higher** must be installed
- Terminal with ANSI color support
  - Windows: Windows Terminal (recommended), ConEmu
  - Mac: Built-in Terminal.app or iTerm2
  - Linux: Any modern terminal

---

## 📦 METHOD 2: Standalone Executable (No Python Required)

For true "Nintendo cartridge" simplicity where **Python is NOT required** on the target machine.

### Windows Standalone

1. **Install PyInstaller** (on development machine):
   ```bash
   pip install pyinstaller
   ```

2. **Build standalone executable**:
   ```bash
   python build.py
   ```

   Or manually:
   ```bash
   pyinstaller --onefile --name doofenstein3d src/main.py
   ```

3. **Package for distribution**:
   ```
   dist/
   ├── doofenstein3d.exe    (standalone executable)
   ├── data/                (copy data folder here)
   ├── PLAY.bat             (modified to run .exe)
   └── README.md
   ```

4. **Create PLAY.bat for executable**:
   ```batch
   @echo off
   doofenstein3d.exe
   pause
   ```

5. **Copy to USB or create ZIP**:
   - Size: ~20-40 MB (includes Python runtime)
   - **Zero dependencies on target machine**

### Linux/Mac Standalone

1. **Use PyInstaller** (same process):
   ```bash
   pyinstaller --onefile --name doofenstein3d src/main.py
   ```

2. **Create PLAY.sh for executable**:
   ```bash
   #!/bin/bash
   ./doofenstein3d
   ```

3. **Make executable**:
   ```bash
   chmod +x doofenstein3d
   chmod +x PLAY.sh
   ```

---

## 📦 METHOD 3: Downloadable ZIP Package

For web distribution (itch.io, GitHub releases, etc.)

### Create the Package

1. **Organize files**:
   ```
   DOOFENSTEIN_3D_v1.0/
   ├── src/
   ├── data/
   ├── PLAY.bat
   ├── PLAY.sh
   ├── README.md
   ├── DOOFENSTEIN_README.md
   ├── USB_LAUNCH_GUIDE.md
   └── QUICK_START.txt
   ```

2. **Create QUICK_START.txt**:
   ```
   ╔════════════════════════════════════════════╗
   ║   DOOFENSTEIN 3D – QUICK START GUIDE       ║
   ╚════════════════════════════════════════════╝

   REQUIREMENTS:
   - Python 3.8 or higher
   - Terminal with ANSI color support

   WINDOWS:
   → Double-click PLAY.bat

   MAC/LINUX:
   → Open terminal in this folder
   → Run: bash PLAY.sh

   HELP:
   - Read DOOFENSTEIN_README.md for full docs
   - Controls: W/A/S/D + E (interact) + I (inventory)
   - Press Q at entrance to quit

   ═══════════════════════════════════════════
   Built with spite & shareware nostalgia
   ═══════════════════════════════════════════
   ```

3. **ZIP the package**:
   - **Windows**: Right-click folder → Send to → Compressed folder
   - **Mac/Linux**: `zip -r DOOFENSTEIN_3D_v1.0.zip DOOFENSTEIN_3D_v1.0/`

4. **Final package size**: ~50 KB (source) or ~20-40 MB (with executable)

---

## 🎮 Distribution Platforms

### GitHub Releases
1. Create release on GitHub
2. Upload ZIP as release asset
3. Users download and extract

**Download link example**:
```
https://github.com/yourusername/GLUTCHDEXMALL/releases/download/v1.0/DOOFENSTEIN_3D.zip
```

### itch.io
1. Create game page at itch.io
2. Upload ZIP file
3. Set to "pay what you want" or free
4. Tag as: retro, fps, horror, mall, wolfenstein

### Direct Distribution
1. Host ZIP on your web server
2. Share direct download link
3. Users extract and play

---

## 🔧 Advanced: Auto-Install Python (Windows Only)

For truly zero-friction distribution on Windows, you can bundle a Python installer.

### Create Auto-Setup Batch Script

**SETUP.bat**:
```batch
@echo off
echo DOOFENSTEIN 3D - Setup Check
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found!
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo After installing, run PLAY.bat
    pause
    exit /b 1
)

echo Python detected!
echo Starting game...
echo.
python src/main.py
pause
```

### Package Structure
```
DOOFENSTEIN_3D_COMPLETE/
├── SETUP.bat           (checks Python, launches game)
├── PLAY.bat            (simple launcher)
├── python_installer.exe (optional: bundle Python installer)
├── src/
├── data/
└── README.md
```

---

## 📋 Pre-Flight Checklist

Before distributing, verify:

### Functionality
- [ ] `PLAY.bat` works on Windows
- [ ] `PLAY.sh` works on Mac/Linux
- [ ] All textures render correctly
- [ ] HUD displays properly
- [ ] Movement and controls work
- [ ] NPCs and artifacts appear
- [ ] Toddler effects trigger correctly

### Files
- [ ] All source files in `src/`
- [ ] All data files in `data/`
- [ ] README files included
- [ ] Launch scripts executable
- [ ] No dev-only files (pycache, .git, etc.)

### Documentation
- [ ] README.md explains game
- [ ] DOOFENSTEIN_README.md covers technical details
- [ ] USB_LAUNCH_GUIDE.md for distribution
- [ ] QUICK_START.txt for first-time users

### Testing
- [ ] Test on clean Windows machine
- [ ] Test on Mac
- [ ] Test on Linux
- [ ] Test with Python 3.8, 3.9, 3.10, 3.11
- [ ] Test in different terminals

---

## 🎨 Branding for USB/Physical Distribution

### USB Drive Label Ideas
```
┌─────────────────────────────┐
│  DOOFENSTEIN 3D             │
│  Coffee-Spilled Mall FPS    │
│  Shareware Edition          │
│                             │
│  Plug and Play              │
│  Python 3.8+ Required       │
└─────────────────────────────┘
```

### Optional: Include Extras
- `session_logs/` folder for gameplay transcripts
- `screenshots/` with sample renders
- `LORE.txt` with artifact backstories
- `CREDITS.txt` with acknowledgments

---

## ⚡ Performance Optimization Tips

### For Slower Machines
Edit `src/wolf_renderer.py`:

```python
# Reduce resolution
self.width = 80  # Instead of 120
self.height = 24  # Instead of 40

# Reduce render distance
self.render_distance = 16  # Instead of 24

# Lower ray density (skip columns)
# In render_frame(), step by 2 instead of 1
for col in range(0, self.width, 2):
```

### For Faster Machines
```python
# Increase resolution
self.width = 160
self.height = 50

# Increase render distance
self.render_distance = 32
```

---

## 🚨 Known Issues & Solutions

### Issue: "Python not found" on Windows
**Solution**: Install Python from python.org, check "Add to PATH" during install

### Issue: Colors don't show in Windows CMD
**Solution**: Use Windows Terminal instead of legacy CMD

### Issue: Textures look distorted
**Solution**: Use monospace font (Consolas, Courier New)

### Issue: Game too slow
**Solution**: Reduce resolution or render distance (see optimization above)

### Issue: Can't execute on Mac ("permission denied")
**Solution**: Run `chmod +x PLAY.sh` first

---

## 📊 File Size Reference

| Package Type | Size | Includes |
|-------------|------|----------|
| Source only | ~50 KB | Python source, data files |
| + Documentation | ~100 KB | + all README files |
| Windows .exe | ~20 MB | Standalone executable + runtime |
| Complete USB | ~25 MB | Executable + docs + extras |
| Installer (NSIS) | ~22 MB | Windows installer package |

---

## 🎯 Summary

### For Maximum Compatibility (Requires Python)
```
1. Copy entire project to USB
2. User double-clicks PLAY.bat / runs PLAY.sh
3. Python 3.8+ must be installed on their machine
```

### For Maximum Simplicity (No Python Required)
```
1. Build standalone .exe with PyInstaller
2. Package with data files
3. User just double-clicks .exe
4. Larger file size (~20 MB vs ~50 KB)
```

### Recommended Approach
**Offer both options**:
- `DOOFENSTEIN_3D_Source.zip` (50 KB, requires Python)
- `DOOFENSTEIN_3D_Standalone_Win.zip` (20 MB, no dependencies)
- Users choose based on their needs

---

**Your game is now ready for USB/download distribution with Nintendo-level simplicity!**

Press START to continue...
