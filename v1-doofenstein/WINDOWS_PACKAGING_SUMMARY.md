# Windows Packaging Summary

Complete toolkit for building and distributing Glitchdex Mall as a Windows executable.

## What You Get

Three ways to deliver the game to Windows users:

### 1. **Standalone ZIP Distribution** (Easiest)

```
glitchdex-mall-v1.0.zip
├── glitchdex-mall.exe
├── _internal/ (Python runtime + dependencies)
├── data/ (game data)
├── docs/
├── examples/
└── README.md
```

**End-user experience:**
- Download ZIP
- Extract folder
- Double-click `glitchdex-mall.exe`
- Play immediately

**Pros:** Simple, no installation, portable
**Cons:** Slightly larger download (contains full Python runtime)

---

### 2. **Windows Installer** (Professional)

```
glitchdex-mall-installer.exe
```

Installs to `C:\Program Files\GlitchdexMall\`

**End-user experience:**
- Run installer
- Choose installation location
- Game appears in Start Menu
- Desktop shortcut created
- Standard uninstall via Control Panel

**Pros:** Professional appearance, standard Windows integration
**Cons:** Requires download + installation step

---

### 3. **Multi-File Distribution** (Advanced)

For very large audiences or multiple platforms:
- Publish both ZIP and MSI installer
- Host on GitHub Releases, itch.io, or own server
- Users choose preferred installation method

---

## Build Files Included

| File | Purpose |
|------|---------|
| `build_windows.bat` | One-click executable builder |
| `glitchdex_mall.spec` | PyInstaller configuration |
| `create_distribution.bat` | ZIP packager |
| `installer.nsi` | NSIS installer script |
| `requirements-build.txt` | Build dependencies |
| `BUILD_AND_DISTRIBUTE.md` | Complete build guide |

---

## Quick Build Process

### Step 1: Build Executable (on Windows)

```batch
double-click build_windows.bat
```

Creates `dist\glitchdex-mall\glitchdex-mall.exe`

### Step 2: Create Distribution ZIP

```batch
double-click create_distribution.bat
```

Creates `glitchdex-mall-v1.0.zip` ready to share

### Step 3: (Optional) Create Installer

Install NSIS, then:
```batch
right-click installer.nsi → Compile NSIS Script
```

Creates `dist\glitchdex-mall-installer.exe`

---

## File Sizes

| Component | Size |
|-----------|------|
| Python runtime | ~30-40 MB |
| Game code + data | ~2-5 MB |
| Total executable | ~40-60 MB |
| ZIP with runtime | ~35-50 MB (compressed) |

---

## Distribution Channels

### GitHub Releases
1. Push code to GitHub
2. Create Release
3. Upload `glitchdex-mall-v1.0.zip`
4. Users download from release page

### itch.io
1. Create free/commercial project
2. Upload ZIP
3. Set as Windows platform
4. Players download and play

### Direct Download
Host ZIP on own server or file hosting (Dropbox, Google Drive, etc.)

---

## Update Process

To release updates:

1. Update game code
2. Re-run `build_windows.bat`
3. Re-run `create_distribution.bat`
4. Publish new ZIP as v1.1, v1.2, etc.

---

## Technical Details

### PyInstaller Configuration

The `.spec` file:
- Bundles all Python code into single executable
- Includes data files (`data/`, `docs/`, `examples/`)
- Uses console mode (shows output window)
- Optimized for Windows

### NSIS Installer

Features:
- Standard Windows installer UI
- Program Files installation
- Start Menu shortcuts
- Desktop shortcut
- Proper uninstaller
- Registry entries for uninstall

---

## Troubleshooting

### Build fails: "Python not found"
→ Install Python from python.org and add to PATH

### Build fails: "ModuleNotFoundError"
→ Verify `src/main.py` exists, re-run `build_windows.bat`

### EXE crashes on startup
→ Ensure `data/` folder with JSON files exists in repo root

### Can't create installer
→ Install NSIS from https://nsis.sourceforge.io

---

## Requirements for Building

- Windows 10+
- Python 3.8+ (with PATH configured)
- ~100 MB disk space (for builds)
- (Optional) NSIS for installer creation

---

## No External Dependencies

The final game has **zero external dependencies**:
- Pure Python stdlib
- No pip packages required
- Self-contained executable
- Works on any Windows 10+ system

---

## Next Steps

1. Read [BUILD_AND_DISTRIBUTE.md](BUILD_AND_DISTRIBUTE.md) for detailed instructions
2. Run `build_windows.bat` to build executable
3. Test `dist\glitchdex-mall\glitchdex-mall.exe`
4. Run `create_distribution.bat` to package for distribution
5. Share `glitchdex-mall-v1.0.zip` with the world!

---

## Version Management

Suggested naming convention:
- `glitchdex-mall-v1.0.zip` – Initial release
- `glitchdex-mall-v1.1.zip` – Bugfix update
- `glitchdex-mall-v2.0.zip` – Major feature update

Always include version in filename for easy user identification.

---

## License & Credits

This game is ready to distribute freely or commercially.
Make sure to include attribution as desired in game files or distribution.

Enjoy shipping! 🎮
