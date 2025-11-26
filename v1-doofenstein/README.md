# DOOFENSTEIN 3D MALL

> **A Wolfenstein 3D-style first-person mall crawler.**
> **Your weapon is a credit card. The toddler is never visible.**

A gloriously broken raycaster set in a liminal 1988 shopping mall. Coffee-spilled shareware clone edition.

## ⏱️ QUICK START (Nintendo Cartridge Easy)

### Windows
Double-click: **`PLAY.bat`**

### Mac / Linux
Run: **`bash PLAY.sh`**

That's it. If you have Python 3.8+, you're ready to play.

(See [START_HERE.txt](START_HERE.txt) for more details.)

---

## What This Is

A **Wolfenstein 3D-style raycaster** set in a sparse 1988 shopping mall. Textured walls, floor casting, ANSI 256-color graphics – authentic early-3D experience running in your terminal. Explore corridors, find cursed artifacts, talk to NPCs, and try to reach the exit before the *presence* in the mall becomes too much.

**The Core Mechanic**: Time is intensity. The longer you play in a single session, the more the invisible toddler in the mall—the thing whose cries echo through vents, whose shadow flickers at the edge of walls—becomes *real*.

### Graphics Technology (NEW!)
- ✨ **Textured walls** with 8x8 tiled patterns
- ✨ **Floor and ceiling rendering** with depth shading
- ✨ **ANSI 256-color VGA palette** for authentic early-3D visuals
- ✨ **Sprite-based items/NPCs** rendered as billboards in 3D space
- ✨ **Visual corruption effects** that intensify with toddler presence

**See [`DOOFENSTEIN_README.md`](DOOFENSTEIN_README.md) for full technical documentation.**

## How to Play

**Windows:** Double-click `PLAY.bat`

**Mac/Linux:** `bash PLAY.sh`

That's it. The launcher will start with the cursed shareware CD menu. Select program #387 (GLITCHDEX MALL ✦) to play the game.

### Controls
- **W / Up**: Move forward
- **S / Down**: Move backward
- **A / Left**: Turn left
- **D / Right**: Turn right
- **E**: Interact (talk to NPCs, pick up items)
- **I**: View inventory
- **H**: Show help
- **Q**: Quit (only works at the ENTRANCE)

### Gameplay
1. You start at the mall entrance with nothing
2. Explore the sparse mall, find artifacts scattered around
3. Talk to NPCs (Milo will tell you the story of every artifact)
4. The longer you stay, the more the invisible toddler's presence intensifies
5. When you can't take it anymore, navigate back to the ENTRANCE and leave

**You can't quit mid-session—you must physically escape through the entrance.**

## Design Philosophy

- **No physics engine**: Tile-to-tile movement. Collision boxes. Simple triggers.
- **No objectives**: You came to shop. That's it. Random events, social encounters, found artifacts.
- **Dungeon crawler aesthetic**: Zelda/early roguelike vibes. Sparse NPCs. Echoing spaces.
- **Jank is a feature**: Broken 3D rendering, texture warping, that eerie unfocused depth from 30KB games.
- **One vision, singular**: This is the definitive version. No future ports, no engine flexibility.

## The Mall

A 1988-style shopping mall with:
- Entrance/Exit
- BORED (skateshop & tee emporium)
- Milo's Discount Optics
- Food court (sparse crowd)
- Anchor store (dying retail)
- Service corridors
- Restrooms, kiosks, escalators

## Key Characters

- **Milo**: Overqualified, disillusioned optician. Keeps the lore of every artifact.
- **BORED**: The kid running the skateshop. Apathetic, sarcastic.
- **R0-MBA**: Silent roaming observer (vacuum). Logs events into the simulation.
- **The Mall Cop**: Simple patrol routes. May flag you if carrying cursed artifacts.
- **Generic Shoppers**: 1988 Nintendo-sparse crowds.

## The Artifacts

Find random objects scattered through the mall. Each one has a story. Take them to Milo—he'll tell you their history. But the more you carry, the weirder things get.

## The Toddler

You never see him. You never directly encounter him. But as your session lengthens:
- **Stage 1**: Occasional distant cries. Rare shadow glimpses.
- **Stage 2**: Frequent wails. Shadow visible in corners.
- **Stage 3**: Constant screaming. Chaos. Tremors. Events cascade.

The toddler is the environment. He is the timer. He is why you need to leave.

## Project Structure

```
docs/              – Design docs
data/              – JSON tile maps, entities, artifacts, stores
src/               – Core Python engine
  main.py          – Entry point
  game_loop.py     – Main game loop (DOOFENSTEIN 3D)
  wolf_renderer.py – Wolfenstein 3D raycaster
  reality_glitch.py – Reality glitch system (mask slips)
  sprite_system.py – Billboard sprite rendering
  mall_engine.py   – Tile system, collision, movement
  entities.py      – NPC and artifact definitions
  toddler_system.py – Toddler presence & visual corruption
  launcher.py      – Shareware CD menu
examples/          – Sample runs, story prompts
```

## Requirements

- Python 3.8+ (for source development)
- No external dependencies for runtime (pure stdlib)

## Windows Package

**Want to ship a Windows executable?** See [BUILD_AND_DISTRIBUTE.md](BUILD_AND_DISTRIBUTE.md) for:
- Building a standalone `.exe` (no Python required for users)
- Creating a Windows installer
- Distributing on GitHub, itch.io, or your own server

Quick steps:

**Recommended (works on any system):**
```bash
python build.py
```

Creates: `dist/glitchdex-mall/glitchdex-mall.exe`

**Or use Windows batch file:**
```bash
build_windows.bat
```

**Having issues?** See [TROUBLESHOOT_BUILD.md](TROUBLESHOOT_BUILD.md) for solutions.

**Total size**: ~40-60 MB (includes Python runtime)

## Cursed Shareware CD Launcher

**Want maximum atmosphere?** Wrap the game in a fake 1990s shareware CD experience:

```bash
python src/launcher.py
```

This launches an authentic DOS-style menu system with:
- ✓ 500-program catalog (499 fake + 1 real: GLITCHDEX MALL at #387)
- ✓ Colored ASCII art borders and fake system initialization
- ✓ Fake loading screens with progress bars
- ✓ Fake error messages for non-existent programs
- ✓ Screen flicker effect on startup
- ✓ Fire cursor visual effects

See [SHAREWARE_LAUNCHER_GUIDE.md](SHAREWARE_LAUNCHER_GUIDE.md) for details on:
- Customizing the 500 program list
- Adding hidden messages to program names
- Building as standalone .exe
- Distributing as a "cursed CD" ZIP

## Status

**COMPLETE** – All 7 layers implemented, tested, and playable.

- ✓ Core tile engine with collision and movement
- ✓ First-person raycaster renderer with DOS-era jank aesthetic
- ✓ NPC system with 6 unique characters and behavior rules
- ✓ Artifact discovery system with Milo's lore database (14 cursed items)
- ✓ Invisible toddler presence system (3 stages, audio, shadow, chaos)
- ✓ Game loop with input handling and state management
- ✓ Exit-only game ending mechanic
- ✓ Session logging and transcript generation

Ready to play. No external dependencies required.

## Testing

Run the gameplay test suite to validate all systems:

```bash
python test_gameplay.py
```

All tests should pass (movement, artifacts, NPCs, toddler system, state management, interactions, weirdness boost).

## Examples

See `examples/` for:
- **example_session.md** – Annotated walkthrough of a typical playthrough
- **story_prompts.md** – How to use the engine as a narrative generator

The session log (saved after each game) can be used to construct stories, analyze patterns, or feed into other creative systems.

---

*A game by the GLITCHDEX collective. Made with spite and synthetic transcendence.*
