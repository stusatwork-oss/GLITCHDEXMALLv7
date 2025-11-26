# REALITY GLITCH SYSTEM
## When the Mask Slips: Sophisticated Rendering Bleeding Through the Facade

---

## 🎭 Concept

DOOFENSTEIN 3D pretends to be a coffee-spilled 1992 Wolfenstein 3D clone. But underneath? It's running modern rendering tech that occasionally **bleeds through** when the toddler's presence breaks the simulation.

This isn't a bug. **This is a feature.** The game "glitches" into revealing its true sophisticated nature.

---

## 🌟 What Happens

As the toddler presence intensifies, the retro facade **cracks**, revealing glimpses of:

- **Ray-traced lighting** that Wolf3D couldn't do
- **Photorealistic textures** with impossible detail
- **Modern post-processing** (bloom, depth of field, motion blur)
- **Physics simulations** appearing briefly
- **Debug overlays** from the "real" engine underneath
- **Wireframe geometry** showing the mesh
- **Ambient occlusion** creating natural shadows

---

## 🎮 Types of Reality Glitches

### Lighting Glitches
**The light is too good for 1992.**

- **RAYTRACED_SHADOWS**: Shadows gain soft edges and proper occlusion
- **GLOBAL_ILLUMINATION**: Light bounces off walls realistically
- **VOLUMETRIC_LIGHT**: God rays appear through vents

### Texture Glitches
**The walls have too much detail.**

- **PHOTOREALISTIC_TEXTURE**: Walls momentarily become photographs
- **PROCEDURAL_SURFACE**: Infinite fractal detail emerges
- **NORMAL_MAPS**: Walls gain depth and bumps they shouldn't have

### Post-Processing Glitches
**Camera effects that shouldn't exist.**

- **DEPTH_OF_FIELD**: Background blurs like a real camera lens
- **MOTION_BLUR**: Movement smears with temporal sampling
- **BLOOM_EFFECT**: Bright lights glow and bleed (HDR)
- **SCREEN_SPACE_AO**: Corners darken with contact shadows

### Physics Glitches
**Things move when they shouldn't.**

- **PARTICLE_SIM**: Dust particles float with full physics
- **CLOTH_SIMULATION**: Fabric ripples and moves

### Geometry Glitches
**Too many polygons.**

- **MESH_SUBDIVISION**: Walls become smooth curves
- **DYNAMIC_TESSELLATION**: Geometry gains millions of polygons

### Reality Breaks
**The simulation itself cracks.**

- **SIMULATION_BREACH**: You see the real engine underneath
- **INFINITE_MIRRORS**: Ray-traced recursive reflections appear

---

## 📊 Trigger Conditions

### Stage 0 (0-5 minutes)
- **Probability**: 0.1% per frame
- **Effects**: Extremely rare, subtle hints only
- **Types**: Motion blur, ambient occlusion, normal maps

### Stage 1 (5-15 minutes)
- **Probability**: 2-5% per frame (scales with shadow intensity)
- **Effects**: Regular glitches, medium intensity
- **Types**: All except reality breaks

### Stage 2 (15+ minutes)
- **Probability**: 8-20% per frame (scales with shadow intensity)
- **Effects**: Frequent, intense, including full breaks
- **Types**: Everything, including simulation breaches

### Artifact Amplification
**Each artifact you carry increases glitch probability by 15%.**

- 3 artifacts: Early glitches start appearing
- 5+ artifacts: Reality breaks even in Stage 1

---

## 🎨 Visual Effects

### Depth of Field
Blurs background naturally, creating camera-like focus.

```
Before:  █▓▒░ (all sharp)
After:   █▓░  (far walls blur)
```

### Motion Blur
Temporal sampling makes movement smear.

```
Frame blending between current and previous frame
Creates ghosting effect on rapid turns
```

### Bloom
Bright areas glow and bleed into neighbors.

```
Bright pixel: █ (255)
Neighbors gain +10 brightness
Creates HDR-style light bleeding
```

### Ambient Occlusion
Corners and edges darken realistically.

```
Check neighbors for "solid" characters
3+ solid neighbors = darken by 15 color units
Creates contact shadows
```

### Photorealistic Leak
Textures gain impossible detail.

```
░ → :  (more detailed character)
▒ → ▓  (higher resolution)
. → ∙•: (floor gains micro-detail)
```

### Wireframe Overlay
Cyan grid lines reveal polygon mesh.

```
─ │ characters at regular intervals
Color: 46 (bright cyan)
Shows "beneath" the textures
```

### Debug Overlay
Green text in corner showing real engine stats.

```
[38;5;46m (bright green)
Shows: Unity version, render pipeline, drawcalls
Reveals it's not actually running on DOS
```

---

## 🛠️ Technical Implementation

### Architecture

1. **reality_glitch.py**: Core glitch system
   - Manages active glitches
   - Calculates probabilities
   - Generates effect parameters

2. **wolf_renderer.py**: Rendering integration
   - `_apply_reality_glitches()`: Master dispatcher
   - Individual methods for each effect type
   - Screen buffer post-processing

3. **game_loop.py**: Game integration
   - Updates glitch system each frame
   - Passes effects to renderer
   - Logs glitch messages

### Data Flow

```
Toddler System → Reality Glitch System
                      ↓
              Calculate probabilities
                      ↓
              Trigger new glitches
                      ↓
              Generate effect parameters
                      ↓
              Wolf Renderer → Apply effects
                      ↓
              Final frame with glitches
```

### Effect Parameters

Each glitch generates parameters passed to renderer:

```python
{
    "depth_of_field": 0.0-1.0,
    "motion_blur": 0.0-1.0,
    "bloom": 0.0-1.0,
    "ambient_occlusion": 0.0-1.0,
    "photorealistic": 0.0-1.0,
    "wireframe": 0 or 1,
    "debug_info": 0 or 1,
    "debug_text": [...] if debug_info > 0
}
```

---

## 🎭 Design Philosophy

### "Sophisticated Imitation of Simplicity"

The game **deliberately** reveals its complexity through "glitches":

1. **Surface**: Coffee-spilled Wolf3D clone, 1992 aesthetic
2. **Underneath**: Modern renderer with ray tracing, physics, post-processing
3. **Glitches**: Moments where the mask slips

This creates **cognitive dissonance**:
- "Wait, Wolf3D couldn't do that..."
- "Did I just see bloom effects?"
- "Why is there an ambient occlusion pass?"

### Horror Through Technical Impossible

The toddler doesn't just corrupt visuals - it **breaks the simulation itself**.

When you see:
- Ray-traced shadows in a 1992 game
- Depth of field in a raycaster
- Debug text showing "Unity 2023"

You realize: **This isn't what it claims to be.**

---

## 📝 Messages

Glitches generate messages logged to session:

### Stage 0 (Subtle)
```
[GLITCH] Something wrong with the rendering... NORMAL_MAPS
```

### Stage 1 (Obvious)
```
[REALITY SLIP] Shadows become too realistic - soft edges, proper occlusion
[REALITY SLIP] Light bounces appear - walls glow with reflected light
```

### Stage 2 (Breaking)
```
[SIMULATION BREAKING] WALL TEXTURES MOMENTARILY BECOME PHOTOGRAPHS - TOO DETAILED
[SIMULATION BREAKING] THE MALL FLICKERS - YOU SEE THE REAL ENGINE UNDERNEATH
```

### Full Breaks
When `is_reality_breaking()` returns true:
```
[SYSTEM] SIMULATION INTEGRITY COMPROMISED
[WARNING] Rendering facade failure detected
```

---

## 🔧 Customization

### Adjust Glitch Frequency

Edit `src/reality_glitch.py`:

```python
# In update() method
if toddler_stage == 1:
    base_chance = 0.02  # Lower = less frequent
elif toddler_stage == 2:
    base_chance = 0.08  # Lower = less frequent
```

### Adjust Effect Intensity

Edit glitch templates in `__init__()`:

```python
"raytraced_shadows": GlitchEvent(
    "RAYTRACED_SHADOWS",
    "Shadows become too realistic",
    0.7,  # Lower = less intense
    30    # Duration in frames
),
```

### Add New Glitch Types

1. Add to `glitch_catalog` in `reality_glitch.py`
2. Add rendering method in `wolf_renderer.py`
3. Call from `_apply_reality_glitches()`

Example:
```python
# In reality_glitch.py
"lens_flare": GlitchEvent(
    "LENS_FLARE",
    "Camera lens flares appear",
    0.6, 40
),

# In wolf_renderer.py
def _apply_lens_flare(self, strength: float):
    # Your implementation here
    pass

# In _apply_reality_glitches()
if effects.get("lens_flare", 0) > 0.3:
    self._apply_lens_flare(effects["lens_flare"])
```

---

## 🎯 Summary

**The reality glitch system transforms DOOFENSTEIN 3D from a retro homage into a meta-commentary on game engines themselves.**

The game **pretends** to be simple. But when the toddler's presence cracks the facade, you see what's really there:

- Modern rendering techniques
- Sophisticated lighting
- Physics simulations
- Debug information from the real engine

**This isn't a bug. This is the game revealing its true nature.**

The sophisticated system imitating simplicity... until it can't anymore.

---

*The mask always slips eventually. The toddler makes sure of it.*
