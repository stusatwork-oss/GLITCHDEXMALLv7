# Building & Distributing Glitchdex Mall Engine for Windows

This guide explains how to package the game as a Windows executable and create an installer.

## Prerequisites

- Windows 10 or later
- Python 3.8+ (from https://www.python.org - make sure to check "Add Python to PATH")
- (Optional) NSIS for creating the installer (from https://nsis.sourceforge.io)

## Quick Start: Building the Standalone Executable

### Step 1: Prepare Your System

1. Install Python 3.8+ from https://www.python.org
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Verify Python is installed: Open Command Prompt and type `python --version`

2. Clone or download the GLITCHDEX MALL repository

3. Open Command Prompt and navigate to the repo directory:
   ```
   cd path\to\GLUTCHDEXMALL
   ```

### Step 2: Run the Build Script

Simply double-click `build_windows.bat` (or run it from Command Prompt).

The script will:
1. Check Python installation
2. Install PyInstaller
3. Clean old builds
4. Build the executable
5. Create `dist/glitchdex-mall.exe`

**That's it!** You now have a standalone executable.

### Step 3: Test the Executable

Navigate to the `dist` folder and double-click `glitchdex-mall.exe` to test it.

---

## Distribution Options

### Option A: Direct Executable Distribution

**Easiest for end-users:**

1. Build the executable (see above)
2. Go to `dist` folder
3. Create a ZIP file: `glitchdex-mall.zip` containing:
   ```
   glitchdex-mall/
   ├── glitchdex-mall.exe
   ├── _internal/ (all dependencies)
   └── ... (other files)
   ```
4. Share the ZIP file

End-users can simply:
- Download and extract the ZIP
- Double-click `glitchdex-mall.exe`
- Play!

### Option B: Windows Installer (MSI/EXE)

**More professional, easier installation:**

#### Using NSIS:

1. Install NSIS from https://nsis.sourceforge.io
2. Build the executable first (see Step 2 above)
3. Right-click `installer.nsi` → "Compile NSIS Script"
   - OR: Open NSIS Compiler and select `installer.nsi`
4. Installer will be created at `dist/glitchdex-mall-installer.exe`

**End-users can:**
- Run the installer
- Choose installation location
- Game appears in Start Menu and Desktop
- Easy uninstall via Control Panel

---

## Build Details

### PyInstaller Configuration (`glitchdex_mall.spec`)

The spec file configures PyInstaller to:
- Bundle all Python code into a single executable
- Include data files (JSON configs, documentation)
- Run in console mode (shows output window)
- Optimize for Windows

### Build Output

```
dist/
├── glitchdex-mall.exe          (the executable)
├── glitchdex-mall/
│   ├── _internal/              (all dependencies and modules)
│   ├── data/                   (game data - JSON files)
│   ├── docs/                   (documentation)
│   └── examples/               (example playthroughs)
```

**Total size**: ~40-60 MB (includes Python runtime)

---

## Troubleshooting

### Issue: "Python is not installed or not in PATH"

**Solution:**
1. Reinstall Python from https://www.python.org
2. **IMPORTANT**: During installation, check the box "Add Python to PATH"
3. Close and reopen Command Prompt
4. Verify: `python --version`

### Issue: "pip install failed"

**Solution:**
1. Make sure Python is properly installed
2. Try: `python -m pip install --upgrade pip`
3. Then re-run the build script

### Issue: Build fails with "ModuleNotFoundError"

**Solution:**
1. Ensure you're in the repo directory: `cd path\to\GLUTCHDEXMALL`
2. Verify `src/main.py` exists
3. Re-run `build_windows.bat`

### Issue: Executable crashes on startup

**Solution:**
1. Check that `data/` folder is present in the repo
2. Make sure all JSON files are intact
3. Try building again from scratch

---

## Customization

### Change Executable Name

Edit `glitchdex_mall.spec` line:
```python
name='glitchdex-mall',  # Change this to your desired name
```

### Change Console/Windowed Mode

Edit `glitchdex_mall.spec`:
```python
console=True,   # True = console window, False = hidden window
```

### Add an Icon

1. Create a 256×256 PNG icon
2. Convert to ICO using an online tool
3. Edit `glitchdex_mall.spec`:
```python
exe = EXE(
    ...,
    icon='path\\to\\icon.ico',
    ...
)
```

---

## Publishing Your Build

### GitHub Releases

1. Build the executable
2. Create a ZIP: `glitchdex-mall-v1.0.zip` with `dist/glitchdex-mall/` contents
3. Go to GitHub → Releases → Draft new release
4. Upload the ZIP file
5. Users can download and play immediately

### itch.io

1. Create account at itch.io
2. Create a new project
3. Upload ZIP with executable
4. Set it as "Windows" platform
5. Set up free/paid pricing
6. Publish!

### Direct Download

Host the ZIP on your own server or file hosting service.

---

## Version Updates

To release an update:

1. Update code in `src/`
2. Update version in `glitchdex_mall.spec` if desired
3. Re-run `build_windows.bat`
4. Create new ZIP from `dist/glitchdex-mall/`
5. Publish as new release

---

## Advanced: Creating a Proper MSI Installer

For production-grade installations, you can use WiX (Windows Installer XML):

1. Install WiX Toolset from https://wixtoolset.org
2. Create a `.wxs` file with your package details
3. Compile to `.msi`

This is more advanced but creates a professional installer that integrates with Windows better.

---

## Notes

- The executable contains a complete Python runtime (40-60 MB)
- Users do NOT need Python installed to run the game
- Session logs are saved in the installation directory
- Game data is bundled, no external files needed

---

## Questions?

Refer to:
- PyInstaller docs: https://pyinstaller.org
- NSIS docs: https://nsis.sourceforge.io/Docs
- Python docs: https://docs.python.org

Good luck shipping your game! 🎮
