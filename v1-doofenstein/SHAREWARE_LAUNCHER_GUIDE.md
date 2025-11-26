# GLITCHDEX MALL - Cursed Shareware CD Launcher

Transform your game into an authentic 1990s cursed shareware CD experience.

## What You Get

A complete launcher system that mimics the horrifying aesthetic of 1990s shareware collections:

- **500-program catalog** (499 fake + 1 real: GLITCHDEX MALL)
- **DOS-style menu system** with colored text, ASCII art, and authentic borders
- **Fake initialization screen** with system checks
- **Fake loading screens** with progress bars
- **Fake error messages** for non-existent programs
- **Screen flicker effect** on startup
- **Fire cursor** (visual effect in text)

## Structure

```
GAMEZILLA_MEGA_COLLECTION_VOL4/
├── launcher.py              (main launcher - run this!)
├── shareware_gen.py         (catalog generator)
├── glitchdex-mall.exe       (the real game)
├── data/                    (game data files)
├── CD_README.txt            (fake CD documentation)
└── PROGRAM_CATALOG.txt      (generated list of 500 programs)
```

## Usage

### Run with Python

```bash
python src/launcher.py
```

This launches the cursed shareware menu.

### Build as Standalone Executable

```batch
# Build the launcher as .exe
pyinstaller --onefile --add-data "data:data" src/launcher.py
```

## Menu Commands

```
UP/DOWN       - Navigate program list
ENTER         - Launch selected program
P             - Previous page
N             - Next page
Q             - Quit

Or type program number (1-500) and press ENTER
```

## Program #387 - The Real One

Hidden among 499 fake programs is **Program 387: GLITCHDEX MALL** (marked with ✦ in menu).

When selected, it shows a fake loading screen, then launches the actual game.

When selecting any other program, it shows an error message:
```
PROGRAM NOT FOUND - ERROR

File: prog_XXX.exe

This program is listed in the catalog but is not installed.
Installation Disk 1 of 3 required.
```

## Customization

### Add Hidden Messages to Program Names

Edit `src/shareware_gen.py` to customize program titles:

```python
if i == 387:
    programs_list.append({
        "number": i,
        "name": "GLITCHDEX MALL",
        ...
    })
```

You can modify the program lists to include hidden messages, inside jokes, or easter eggs.

### Change CD Name

The launcher is hardcoded with "GAMEZILLA MEGA COLLECTION VOL. 4". To change it:

Edit `launcher.py` and change this line:
```python
print("  GAMEZILLA MEGA COLLECTION VOL. 4")
```

### Modify Fake Program Categories

Edit the `genres` dict in `shareware_gen.py`:

```python
genres = {
    "solitaire": [...],
    "screensaver": [...],
    "compression": [...],
    # Add your own categories!
}
```

### Change System Messages

The fake initialization and loading screens are defined in `launcher.py`. Edit:

- `init_screen()` - Initialization messages
- `show_loading()` - Loading screen
- `show_error()` - Error message

## How It Works

### Shareware Generator

`shareware_gen.py` creates a list of 500 realistic 1990s shareware program names:

- **Real program** (#387): GLITCHDEX MALL
- **Fake programs** (#1-386, #388-500): Generated from templates

The generator uses:
- Genre categories (games, utilities, demos, etc.)
- Version numbers (1.0, 2.5, LITE, PRO, etc.)
- Adjectives (ULTRA, MEGA, TURBO, etc.)

Result: Authentic-sounding programs like:
```
 40. MEGA INTRO
288. INFO
216. CALCULATOR 4.5
498. TURBO TEXTVIEW
...
387. GLITCHDEX MALL ✦
...
```

### Launcher System

`launcher.py` provides:

1. **Initialization Screen**: Fake system checks (memory, drivers, fonts, etc.)
2. **Screen Flicker**: Brief black flicker at startup
3. **Menu System**: Colored text, ASCII borders, program list
4. **Navigation**: Arrow keys, page up/down, direct program number entry
5. **Loading Screens**: Fake progress bars and initialization text
6. **Error Handling**: Error messages for fake programs

## Distribution

### As a Python Package

```bash
# Run directly with Python
python src/launcher.py
```

### As a Standalone .exe

```bash
# Build with PyInstaller
pip install pyinstaller
pyinstaller --onefile --add-data "src:src" --add-data "data:data" src/launcher.py

# Or use the batch script (if available)
build_launcher.bat
```

### As a ZIP File (Cursed CD)

Create a ZIP that looks like an old CD:

```
GAMEZILLA_MEGA_COLLECTION_VOL4.zip
├── launcher.exe
├── glitchdex-mall.exe
├── data/
├── CD_README.txt
└── PROGRAM_CATALOG.txt
```

Share this ZIP and users can extract and run it.

## The Aesthetic

The launcher recreates the specific horror of 1990s software:

- **DOS/Windows 95 hybrid**: Blue backgrounds, yellow text, ASCII art
- **Fake loading**: System checks and progress bars that don't mean anything
- **Fake errors**: Programs that don't exist but seem plausible
- **Cursed UI**: Colored text, boxes, separators
- **Screen flicker**: That "loading..." effect from old CDs
- **Authentic naming**: 500 programs that sound real but mostly don't

The experience is both nostalgic and unsettling - deliberately capturing the uncanny feeling of old software.

## Tips for Maximum Atmosphere

1. **Include the fake README**: `CD_README.txt` adds to the illusion
2. **Generate full catalog**: Run `python src/shareware_gen.py` to create `PROGRAM_CATALOG.txt`
3. **Customize error messages**: Make them more or less helpful
4. **Add sound**: (Optional) Include beeps/boops when navigating
5. **Use DOS font**: Run in a terminal with retro fonts for extra authenticity

## Technical Details

### No External Dependencies

The launcher uses only Python stdlib:
- `sys` - System interaction
- `os` - File/program launching
- `time` - Delays and timing
- `random` - Random program generation

### Colors (ANSI Codes)

```python
BLUE_BG = "\033[44m"      # Blue background
TEXT_YELLOW = "\033[33m"  # Yellow text
TEXT_GREEN = "\033[32m"   # Green text
TEXT_RED = "\033[31m"     # Red text
TEXT_CYAN = "\033[36m"    # Cyan text
```

### Program Selection

The launcher tracks which program is selected and which page is being viewed. When a program is launched:

1. Check if it's the real program (#387)
2. If real: show loading screen, then launch `glitchdex-mall.exe`
3. If fake: show error message, return to menu

## Examples

### Hidden Message in Program Names

You could embed messages in the program list. For example, edit `shareware_gen.py`:

```python
# Every 10th program is a hint
if i % 10 == 0 and i != 387:
    name = f"PROGRAM_#{i}_IS_WATCHING"
```

### Custom Genre

Add a new genre:

```python
genres = {
    ...
    "haunted": ["OUIJA", "GHOST HUNTER", "POLTERGEIST", "PHANTOM"],
}
```

### Redirect to Different Game

Change the launch behavior in `launcher.py`:

```python
if prog["number"] == 387:
    # Launch something else
    subprocess.run("your-game.exe")
```

## Architecture

```
User runs launcher.py
    ↓
Shareware generator creates 500 programs
    ↓
Launcher displays menu with DOS aesthetic
    ↓
User selects program
    ↓
If program #387 (GLITCHDEX MALL):
    - Show fake loading screen
    - Launch glitchdex-mall.exe
↓
If other program:
    - Show error message
    - Return to menu
```

---

**That's everything!** The launcher is ready to make your game feel like a cursed piece of 1990s shareware history.

Enjoy the horror! 🔥
