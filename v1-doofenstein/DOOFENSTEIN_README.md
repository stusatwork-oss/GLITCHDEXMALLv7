# DOOFENSTEIN 3D MALL

> **A Wolfenstein 3D-style mall crawler where your only weapon is a credit card.**
>
> **Coffee-spilled shareware clone edition – The toddler is never visible.**

---

## 🎮 What This Is

**DOOFENSTEIN 3D** is a first-person raycaster in the spirit of Wolfenstein 3D (1992), but set in a liminal 1988 shopping mall. This is what happens when you spill coffee on the Wolf3D source code and replace all the nazis with skateshops.

### The Experience
- **Textured walls** using Unicode block characters and ANSI 256-color
- **Floor and ceiling rendering** with distance-based shading
- **Sprite-based items and NPCs** rendered in 3D space
- **VGA palette aesthetic** – authentic early-3D visual style
- **Toddler presence system** – increasing visual corruption as you stay longer
- **Pure Python stdlib** – no external dependencies needed

---

## 🚀 QUICK START (Nintendo Cartridge Simple)

### Windows
```
Double-click: PLAY.bat
```

### Mac / Linux
```
bash PLAY.sh
```

That's it. If you have Python 3.8+, you're playing DOOFENSTEIN 3D.

---

## 🎨 Graphics Technology

### Raycaster Engine
- **Textured walls**: 8x8 tiled patterns mapped to 3D surfaces
- **Distance fog**: Brightness falloff simulates atmospheric depth
- **Floor casting**: Depth-shaded floor tiles with procedural patterns
- **Ceiling rendering**: Dark gradient ceiling for authentic Wolf3D feel
- **Sprite billboarding**: Items and NPCs rendered as 3D sprites

### Visual Effects
- **ANSI 256-color palette**: Full VGA-style colors in your terminal
- **Unicode block shaders**: `█▓▒░` for smooth texture gradients
- **Screen distortions**: Chromatic aberration, vignette, scanlines
- **Toddler corruption**: Visual glitches increase with presence intensity

### Texture Types
- **CORRIDOR**: Gray concrete with panel lines
- **BRICK**: Red brick pattern (skateshop)
- **GLASS**: Semi-transparent glass blocks (Milo's Optics)
- **TILE**: White/blue tiles (food court, restrooms)
- **METAL**: Horizontal ribbed metal (service halls)
- **CONCRETE**: Rough concrete (anchor store)
- **DOOR**: Wooden door texture (entrance/exit)

---

## 🕹️ Controls

| Key | Action |
|-----|--------|
| **W** / Up | Move forward |
| **S** / Down | Move backward |
| **A** / Left | Turn left 90° |
| **D** / Right | Turn right 90° |
| **E** | Interact (pick up items, talk to NPCs) |
| **I** | Toggle inventory |
| **H** | Show help |
| **Q** | Quit (only works at ENTRANCE) |

---

## 📦 What's Inside

### Core Systems

**`src/wolf_renderer.py`** – Wolfenstein 3D-style raycaster
- WolfRenderer class: Main rendering engine
- Texture system: 8x8 tiled wall patterns
- Color class: ANSI 256-color palette management
- Wolf3DHUD: Authentic shareware-style HUD

**`src/sprite_system.py`** – Billboard sprite rendering
- SpriteRenderer: 3D sprite projection and depth sorting
- Sprite definitions for all items and NPCs
- Z-buffer depth testing for proper occlusion

**`src/game_loop.py`** – Main game loop (upgraded for Wolf3D)
- Integrated Wolf3D rendering pipeline
- Enhanced visual corruption effects
- DOOFENSTEIN branding and UI

**`src/mall_engine.py`** – Tile engine and collision (unchanged)
- 50x50 tile grid system
- Bresenham line-of-sight
- Player state and movement

**`src/toddler_system.py`** – Invisible toddler presence (enhanced)
- 3 intensity stages based on playtime
- Enhanced visual distortion effects
- Screen corruption, glitch effects, vignetting

---

## 🎭 The Mall

Explore a sparse 1988 shopping mall:
- **ENTRANCE** – Where you start and can escape
- **BORED** – Skateshop & tee emporium
- **Milo's Discount Optics** – Milo knows every artifact's story
- **Food Court** – Sparse crowds, teriyaki smell, echoes
- **Anchor Store** – Dying retail, massive echoing space
- **Service Halls** – Vents hum, metal walls, toddler presence amplified
- **Kiosks & Restrooms** – Scattered throughout

---

## 👻 The Toddler Presence

**YOU NEVER SEE IT. IT'S ALWAYS THERE.**

### Stage 0 (0–5 minutes)
- No presence
- Clean visuals
- Calm

### Stage 1 (5–15 minutes)
- Distant cries through vents
- Occasional shadow flickers
- Light screen vignetting
- You should leave soon

### Stage 2 (15+ minutes)
- Constant screaming
- Heavy visual corruption
- Screen tears and glitches
- Extreme vignette
- **GET OUT NOW**

### Artifact Amplification
- Each artifact you carry increases toddler intensity by 20%
- 3+ artifacts can force early stage escalation
- 4+ artifacts in Stage 1 = instant Stage 2

---

## 🛠️ Technical Details

### Requirements
- **Python 3.8+** (no external libraries needed)
- **Terminal with ANSI 256-color support**
  - Windows: Windows Terminal, ConEmu
  - Mac: Terminal.app, iTerm2
  - Linux: Any modern terminal emulator

### Performance
- **Resolution**: 120x40 characters (default)
- **Render distance**: 24 tiles
- **FOV**: 66 degrees (Wolf3D authentic)
- **Frame time**: Instant (no enforced FPS limit)
- **Ray density**: 120 rays per frame
- **File size**: ~3.5KB source files (Wolf3D renderer alone)

### Architecture
- **Pure raycasting**: No 3D engine, just grid-based raycasting
- **Tile-based collision**: Wolf3D-style grid movement
- **Screen buffer rendering**: Build frame in memory, render once
- **Z-buffer for sprites**: Proper depth sorting
- **Bresenham ray traversal**: Fast grid intersection

---

## 🎯 Building & Distribution

### Play from Source
```bash
python src/main.py
```

### Build Standalone Executable (Windows)
```bash
python build.py
```

Creates: `dist/glitchdex-mall/glitchdex-mall.exe`

### Build with Launcher (Shareware CD Style)
The game can be launched through the cursed shareware CD menu (program #387):
```bash
python src/launcher.py
```

See `SHAREWARE_LAUNCHER_GUIDE.md` for full details.

---

## 📁 Project Structure

```
GLUTCHDEXMALL/
├── src/
│   ├── main.py                  # Entry point
│   ├── game_loop.py             # DOOFENSTEIN 3D game loop
│   ├── wolf_renderer.py         # Wolf3D raycaster engine
│   ├── reality_glitch.py        # Reality glitch system
│   ├── sprite_system.py         # Sprite billboard rendering
│   ├── mall_engine.py           # Tile engine & collision
│   ├── entities.py              # NPCs and artifacts
│   ├── toddler_system.py        # Toddler presence (enhanced)
│   ├── launcher.py              # Shareware CD menu
│   └── dos_menu.py              # DOS-style menu system
│
├── data/
│   ├── mall_map.json            # 50x50 tile map
│   ├── entities.json            # NPC definitions
│   └── artifacts.json           # 14 cursed artifacts
│
├── PLAY.sh                      # Nintendo-simple launcher (Unix)
├── PLAY.bat                     # Nintendo-simple launcher (Windows)
├── test_wolf_renderer.py        # Renderer test
├── test_gameplay.py             # Gameplay systems test
└── DOOFENSTEIN_README.md        # This file
```

---

## 🎨 Customization

### Adjust Resolution
Edit `src/game_loop.py`:
```python
self.renderer = WolfRenderer(width=120, height=40)  # Change these
self.hud = Wolf3DHUD(width=120)  # Match width
```

Recommended sizes:
- **Small**: 80x24 (classic terminal)
- **Medium**: 120x40 (default, best balance)
- **Large**: 160x50 (immersive, requires large terminal)

### Modify FOV
Edit `src/wolf_renderer.py`:
```python
self.fov = 66  # Wolf3D default
# Try: 60 (narrow), 75 (wide), 90 (fish-eye)
```

### Change Render Distance
Edit `src/wolf_renderer.py`:
```python
self.render_distance = 24  # Default
# Try: 16 (faster, more fog), 32 (farther sight)
```

### Create New Textures
Edit `src/wolf_renderer.py` -> `class Texture`:
```python
MY_TEXTURE = [
    "44444444",  # Each line is 8 chars
    "43333334",  # Values 0-4: empty, dark, med, light, bright
    "43333334",
    "43333334",
    "44444444",
    "43333334",
    "43333334",
    "43333334",
]
```

Then add to `_init_textures()`:
```python
"MY_TILE_TYPE": TextureMap(
    Texture.MY_TEXTURE,
    (dark_color, med_color, light_color, bright_color)  # ANSI codes
),
```

---

## 🐛 Troubleshooting

### Colors Don't Show
- **Problem**: Terminal doesn't support ANSI 256-color
- **Solution**: Use Windows Terminal, iTerm2, or modern terminal emulator
- **Test**: Run `python test_wolf_renderer.py` – should show colored output

### Performance Issues
- **Problem**: Slow rendering on large terminals
- **Solution**: Reduce resolution or render distance (see Customization above)
- **Note**: Python is not C – this won't run at 60 FPS like Wolf3D

### Textures Look Weird
- **Problem**: Font rendering varies by terminal
- **Solution**: Use a monospace font (Consolas, Monaco, Source Code Pro)
- **Best**: A font with good Unicode block character support

### Game Won't Start
- **Problem**: Missing dependencies or Python version
- **Solution**: Requires Python 3.8+, no external libraries
- **Check**: `python --version` should be 3.8 or higher

---

##  Design Philosophy

### Authentic Shareware Jank
This is not a polished AAA game. This is what you found on a Wired Magazine CD in 1995, misfiled between "Doom Shareware" and "3000 TrueType Fonts."

- **Coffee-stained code**: Bugs are features
- **VGA palette**: 256 colors were impressive in 1992
- **Terminal rendering**: We're pushing ASCII to its limits
- **No physics engine**: Tile-to-tile, baby
- **Raycasting only**: No polygons, no shaders, pure grid math

### The Toddler Hook
The invisible toddler is what makes this game unique. It's not an enemy you fight. It's environmental dread that increases with time.

- Never visible
- Only implied through sound, shadow, corruption
- Presence amplified by artifacts you carry
- No jump scares – just mounting wrongness

---

## 📝 Changelog: ASCII → DOOFENSTEIN 3D

### What Changed
- ✅ **New Wolf3D renderer** (`wolf_renderer.py`)
  - Textured walls with 8x8 tiling
  - Floor and ceiling rendering
  - ANSI 256-color system
  - Distance-based fog and shading

- ✅ **Sprite system** (`sprite_system.py`)
  - Billboard sprites for items/NPCs
  - Z-buffer depth testing
  - 3D positioning in world space

- ✅ **Enhanced toddler effects**
  - Screen corruption increases with stage
  - Chromatic aberration
  - Vignette darkening
  - Random glitches and screen tears

- ✅ **Wolf3D HUD**
  - Authentic shareware-style interface
  - Color-coded status indicators
  - Position, time, inventory count

### What Stayed the Same
- Mall layout (50x50 grid)
- Artifact system (14 cursed items)
- NPC system (6 characters)
- Toddler stage progression (time-based)
- Movement and collision (tile-based)
- Game loop and controls

---

## 🏆 Credits

**DOOFENSTEIN 3D MALL** is a coffee-spilled homage to:
- **Wolfenstein 3D** (1992) – id Software
- **Early '90s shareware culture** – PC Magazine, Wired CDs
- **Liminal space aesthetics** – Dead malls, xennial nostalgia
- **Terminal graphics** – ANSI art, BBS door games

Built with spite, synthetic transcendence, and too much coffee.

---

## 📜 License

Do whatever you want with this. It's shareware. If you make a million dollars, buy me a skateboard.

---

**Now enter the mall. Your mom's credit card is ready. The toddler is waiting.**
