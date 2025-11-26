# GLITCHDEX MALL - LAUNCHER GUIDE

This repository includes multiple launcher options for accessing all versions of GLITCHDEX MALL.

---

## 🚀 Quick Start

### Option 1: GUI Launcher (Recommended - New!)

The mid-90s style mouse-clickable 16-color interface:

```bash
./LAUNCH_GUI.sh
# OR
python3 launcher_gui.py
```

**Features**:
- Windows 95-inspired GUI
- Full mouse support (click to select, click buttons)
- 16-color VGA palette
- 3D-style windows with shadows
- Keyboard shortcuts still work

**Requirements**:
- Python 3 with curses module (standard on Linux/Mac)

---

### Option 2: Text Launcher (Original)

The classic ANSI text-based launcher:

```bash
./LAUNCH.sh
# OR
cd v1-doofenstein && python3 src/launcher.py
```

**Features**:
- Authentic DOS-style ANSI text interface
- Keyboard-only navigation
- Lower resource usage
- Classic shareware CD experience

---

## 📦 What's Available?

Both launchers provide access to all 6 versions:

| Program | Version | Type | Status |
|---------|---------|------|--------|
| **387** | v1-doofenstein | Original Retro Game | ✅ Complete |
| **388** | v2-immersive-sim | Advanced AI Architecture | ✅ Complete |
| **389** | v3-eastland | Pygame Graphical Engine | ✅ Complete |
| **390** | v4-renderist | Cloud-Driven World | ✅ Phase 1 Complete |
| **391** | v5-eastland | CRD Reconstruction Docs | ✅ V1 Complete |
| **392** | v6-nextgen | Next Generation | 🔄 Placeholder |

---

## 🎮 Navigation

### GUI Launcher (launcher_gui.py)

**Mouse**:
- Click on program name to select
- Click buttons to perform actions:
  - `LAUNCH` - Run selected program
  - `< PREV` - Previous page
  - `NEXT >` - Next page
  - `QUIT` - Exit launcher

**Keyboard**:
- `↑/↓` - Navigate program list
- `ENTER` - Launch selected program
- `N` - Next page
- `P` - Previous page
- `Q` - Quit

---

### Text Launcher (launcher.py)

**Keyboard only**:
- `up/down` or `w/s` - Navigate program list
- `ENTER` - Launch selected program
- `n` - Next page
- `p` - Previous page
- Type program number (e.g., `387`) - Jump to program
- `q` - Quit

---

## 🛠️ Technical Details

### GUI Launcher

**File**: `launcher_gui.py`
**Dependencies**:
- `shareware_gen_v2.py` - Updated program generator
- Python `curses` module

**Features**:
- Mid-90s Windows 95-inspired design
- Full 16-color VGA palette
- Mouse support via curses
- 3D window effects with shadows
- Status bar with context help
- Program info display

---

### Text Launcher

**File**: `v1-doofenstein/src/launcher.py`
**Dependencies**:
- `shareware_gen.py` - Program generator

**Features**:
- DOS-style ANSI colors
- Keyboard-only navigation
- Screen flicker effects
- Loading animations
- Error dialogs for fake programs

---

## 🎨 The Shareware Experience

Both launchers simulate a mid-90s shareware CD collection with **500 programs** listed, but only 6 are actually installed (programs 387-392). Attempting to launch other programs will show an authentic "Installation Disk 1 of 3 required" error message.

This is intentional - it recreates the authentic experience of shareware compilation CDs from 1995-1998!

---

## 📝 Adding New Versions

To add a new version:

1. **Update `shareware_gen_v2.py`**:
   ```python
   elif i == 393:
       programs_list.append({
           "number": i,
           "name": "NEW VERSION NAME",
           "genre": "game",
           "version": "7.0",
           "executable": "v7",
           "is_real": True,
       })
   ```

2. **Update launcher launch logic**:
   - In `launcher_gui.py`: Add `elif executable == "v7":` case
   - In `v1-doofenstein/src/launcher.py`: Add same case

3. **Create version directory**:
   ```bash
   mkdir -p v7-name/{src,data,docs}
   ```

4. **Update VERSION_GUIDE.md**

---

## 🐛 Troubleshooting

### GUI Launcher Issues

**Problem**: "curses module not found"
- **Solution**: Install Python with curses support (standard on Linux/Mac)

**Problem**: Mouse clicks not working
- **Solution**: Ensure terminal supports mouse events (most modern terminals do)

**Problem**: Colors look wrong
- **Solution**: Use a terminal that supports 256-color mode

---

### Text Launcher Issues

**Problem**: ANSI colors not showing
- **Solution**: Use a terminal with ANSI color support

**Problem**: Navigation keys not working
- **Solution**: Try alternate keys (w/s instead of up/down)

---

## 🎯 Which Launcher Should I Use?

**Use GUI Launcher if**:
- You want the modern mouse-clickable experience
- You prefer visual aesthetics
- You have a terminal with good mouse support

**Use Text Launcher if**:
- You want the authentic DOS experience
- You prefer keyboard-only navigation
- You're on a system with limited terminal capabilities
- You want lower resource usage

---

## 📚 See Also

- **VERSION_GUIDE.md** - Detailed information about each version
- **v5-eastland/README.md** - CRD reconstruction methodology
- **v6-nextgen/README.md** - Future development plans

---

*The GAMEZILLA MEGA COLLECTION experience - now in 16 colors!*
