# Food Court Vertical Slice - Specification

**Date:** 2025-12-03
**Goal:** Reactor pit aesthetic, era contradictions, hudless NPC interaction
**Scope:** Food court + escalator descent as unified space

---

## DESIGN PHILOSOPHY

### Era Contradictions (Simultaneous Realities)

**Core Concept:** All eras exist at once, flickering based on Cloud state and Toddler proximity.

```
At Cloud 0-30 (calm):
└─ Stable 1995 baseline (dirty but functioning)

At Cloud 30-60 (uneasy):
├─ 1995 baseline
└─ Brief flickers of 2005 (1-2 frames)

At Cloud 60-85 (strained):
├─ 1995/2005 alternating (50/50 split)
├─ Chromatic aberration at edges
└─ Occasional 2011 flash (dark, abandoned)

At Cloud 85-100 (critical):
├─ All 4 eras overlapping
├─ VHS glitch effect
├─ 1995/2005/2011 cycling rapidly
└─ Brief 1981 glimpses (pristine, impossible)
```

**Toddler Proximity Multiplier:**
- 0-50 feet: Normal flicker rate
- 20-50 feet: 2x flicker speed
- 0-20 feet: 4x flicker + overlay blend (multiple eras visible simultaneously)

### Reactor Pit Aesthetic

**Nuclear Containment Reference:**
- Concentric circular descent into pit
- 8-foot depth (verified from measurements)
- Industrial theater lighting (harsh overhead, dramatic shadows)
- Yellow/black hazard striping
- Metal grating surfaces
- Steam/vapor rising from bottom
- Echoing vertical acoustics
- Feeling of "descending into something dangerous"

**The Jolly Time Theater Entrance:**
- "Black mouth" at bottom of escalator
- Gravitational pull toward darkness
- Theater entrance IS the focal void
- Composition: Upper level → Descent → Theater abyss

---

## TECHNICAL ARCHITECTURE

### Renderer: Adapted v3 Pygame Raycaster

**Why v3:**
- Working Wolf3D-style raycasting ✅
- Texture mapping system ✅
- Floor/ceiling rendering ✅
- Integration with game state ✅
- Sprite/NPC rendering ✅

**Modifications Needed:**
1. **Texture Loading System**
   - Load 40 food court frames as pygame Surfaces
   - Index by camera position/angle
   - Multi-layer rendering for era overlays

2. **COMICBOOK Palette Integration**
   - Replace procedural RGB tuples
   - Map palette tags to actual RGB values
   - Apply palette-based lighting/tinting

3. **Era Flicker System**
   ```python
   def render_frame(cloud_level, toddler_distance):
       base_texture = get_era_texture(1995)  # Baseline

       if cloud_level > 30:
           flicker_chance = (cloud_level - 30) / 70  # 0-1
           if random.random() < flicker_chance:
               overlay_texture = get_era_texture(2005)
               blend_alpha = flicker_chance * 0.7

       if cloud_level > 85:
           # Critical: rapid cycling
           era = cycle_eras([1995, 2005, 2011, 1981])
           apply_vhs_glitch()

       if toddler_distance < 50:
           flicker_speed *= (50 / toddler_distance)
   ```

4. **Hudless Rendering**
   - No health bars, no minimap, no text overlays
   - All information environmental

### Photo Asset Processing

**40 Food Court Frames (./processed/frames/foodcourt-2010/)**

**Frame Analysis & Era Assignment:**

```python
# Categorize frames by visual content
frames_analysis = {
    "bright_lights_on": [1, 2, 5, 8, 12, 15, 18, ...],  # 1995 era
    "flickering_lights": [3, 6, 9, 14, 20, ...],        # 2005 era
    "mostly_dark": [7, 11, 16, 22, 25, ...],            # 2011 era
    "pristine_clean": [],                                # 1981 (none available, procedural)

    "angles": {
        "upper_landing": [1-10],
        "mid_descent": [11-20],
        "pit_floor": [21-30],
        "vendor_stalls": [31-40]
    }
}
```

**Texture Mapping Strategy:**
1. Use actual frames where camera angle matches
2. Blend between frames for smooth movement
3. Procedurally enhance for missing angles
4. Apply COMICBOOK palette tint over frames

**Era Enhancement Pipeline:**
```python
def enhance_frame_for_era(frame, era, palette):
    if era == 1995:  # DIRTY (baseline)
        return frame  # Use as-is, it's 2010 footage

    elif era == 2005:  # BROKEN
        # Add flicker effect
        # Increase contrast
        # Darken by 15%
        # Add crack overlays (procedural)

    elif era == 2011:  # ABANDONED
        # Heavy darkness (40% reduction)
        # Desaturate
        # Add dust particles
        # Vignette

    elif era == 1981:  # NEW (procedural only)
        # Brighten by 15%
        # Increase saturation
        # Remove wear/grime (AI inpaint?)
        # Add procedural "new" overlays
```

### Geometry (from v7 Measurements)

**Food Court Pit:**
- Bowl diameter: 120 feet (100-150' range)
- Depth: 8 feet (verified via escalator steps)
- Shape: Circular/reactor containment
- Floor: Z = -8 feet
- Upper level: Z = 0 feet

**Escalator Descent:**
- 12 steps × 8 inches = 96 inches = 8 feet
- 30° incline (standard escalator)
- Width: ~4 feet
- Metal handrails (safety blue from palette)
- Connects upper ring to pit floor

**Theater Entrance (Jolly Time):**
- Position: Bottom of escalator, at pit floor
- Visual: "Black mouth" opening
- Size: Standard theater entrance (~12' wide)
- QBIT entity: "cinema_entrance" zone

**Spatial Layout:**
```
     UPPER LEVEL (Z=0)
          |
          v
    [ESCALATOR DESCENT]
          |
          v
     FOOD COURT PIT (Z=-8)
    ╱                    ╲
   ╱  Vendor Stalls       ╲
  │   Seating Area         │  ← 120' diameter
   ╲  Coffee Stand        ╱
    ╲                    ╱
          CENTER
            ↓
    [JOLLY TIME ENTRANCE]
       "Black Mouth"
```

---

## NPC INTEGRATION: JANITOR TEST CASE

### Janitor Contradiction Sequence

**Initial State (Cloud 0-69):**
- Position: SERVICE_HALL (50, 0, 0)
- Zone: Not visible to player
- Behavior: Patrolling, maintaining
- Visual: Soft green jumpsuit (palette: `wall_soft_green`)

**Threshold Trigger (Cloud 70):**
- Janitor begins walking toward FC-ARCADE
- Movement: Slow, deliberate, unavoidable
- Player sees him approaching from corridor
- Visual change: Jumpsuit darkens slightly

**Rule Break (Enters FC-ARCADE):**
- Janitor crosses forbidden threshold into food court pit
- Cloud system detects contradiction
- Era flicker INTENSIFIES around Janitor
- Environment within 20' radius: rapid era cycling
- His position becomes contradiction epicenter

**LLM Dialogue Trigger:**
```python
if janitor.in_forbidden_zone and cloud >= 70:
    dialogue = janitor_llm.generate(
        system_prompt=build_janitor_prompt(cloud, zone, metadata),
        user_prompt="The arcade machines... they're humming in E-flat..."
    )
    display_dialogue(janitor, dialogue, method="floating_text")
```

### Hudless NPC State Indication

**Visual Cues (No HUD needed):**

**1. Color Shifts (Shader-based)**
```python
npc_color_mods = {
    "calm": {"saturation": 1.0, "brightness": 1.0},
    "uneasy": {"saturation": 0.95, "brightness": 0.97},
    "strained": {"saturation": 0.85, "brightness": 0.90},
    "critical": {"saturation": 0.6, "brightness": 0.75}
}

# Janitor's jumpsuit shifts from soft_green → dark_green
apply_color_mod(janitor.sprite, npc_color_mods[cloud.mood])
```

**2. Tool Glow (Warning Yellow)**
- Janitor carries mop/bucket (palette: `warning_yellow_dark`)
- At Cloud > 60: Tools begin glowing
- At Cloud > 85: Pulsing yellow glow (1Hz)
- Diegetic indicator: "Something's wrong, even his tools know it"

**3. Posture/Animation**
- Calm: Upright walking, steady pace
- Uneasy: Hunched slightly, looking around
- Strained: Shuffling, hesitant movement
- Critical: Rigid, mechanical, contradiction-driven

**4. Spatial Distortion**
- At contradiction: Janitor flickers between eras too
- 1995 Janitor: Younger appearance (brighter colors)
- 2005 Janitor: More worn (darker jumpsuit)
- 2011 Janitor: Barely visible (mostly shadow)
- All three overlay when Cloud > 85

### Dialogue Delivery (Hudless)

**Method: Floating World-Space Text**

```python
def display_dialogue(npc, text, duration=5.0):
    """
    Render text in 3D world space above NPC's head.
    No HUD, no UI panels - text exists IN the world.
    """
    text_sprite = render_text(
        text=text,
        font="monospace",  # Retro aesthetic
        color=palette["ceiling_tile_light"],  # Visible against dark
        background=palette["security_blue_dark"],  # Subtle box
        max_width=40  # Characters
    )

    # Position above NPC head
    world_pos = (npc.x, npc.y, npc.z + 7.0)  # 7 feet above ground

    # Billboard sprite (always faces camera)
    render_billboard(text_sprite, world_pos, duration)

    # Fade in/out for polish
    fade_alpha(text_sprite, duration)
```

**Alternative (More Immersive): Diegetic Signs**
- Janitor holds up a sign
- Sign is a physical object in world
- Text written on sign surface
- More work, but no "floating" text

**Recommendation:** Start with floating text, can upgrade to diegetic later.

---

## CLOUD STATE INDICATION (HUDLESS)

**Environmental Feedback:**

**1. Lighting Changes**
```python
lighting_by_cloud = {
    0-30:   {"overhead": 1.0, "flicker": 0.0},  # Stable
    30-60:  {"overhead": 0.9, "flicker": 0.1},  # Occasional flicker
    60-85:  {"overhead": 0.7, "flicker": 0.3},  # Frequent flicker
    85-100: {"overhead": 0.5, "flicker": 0.6}   # Strobe effect
}
```

**2. Visual Post-Processing**
- **Chromatic Aberration:** RGB channels separate at screen edges
  - Cloud 0-30: None
  - Cloud 60: 2px offset
  - Cloud 85: 8px offset

- **Vignette:** Darkness closing in
  - Cloud 0: None
  - Cloud 60: 20% edge darkness
  - Cloud 85: 50% edge darkness

- **Screen Shake:** Camera tremor
  - Triggered by Toddler proximity
  - Intensity = reality_strain value

**3. Audio Cues**
- **Escalator Hum:** Pitch shifts with Cloud
  - Base frequency: E-flat (311 Hz)
  - Cloud 0: Steady hum
  - Cloud 60: Warbling pitch
  - Cloud 85: Dissonant harmonics

- **Ambient Sound:** Mall atmosphere
  - Calm: Muzak, distant chatter
  - Uneasy: Muzak slowing down
  - Strained: Reverse muzak, silence gaps
  - Critical: White noise, reality tearing

**4. NPC Reactions (Crowd as Indicator)**
- Mall Walker NPCs visible in distance
- Cloud 0-30: Normal shopping behavior
- Cloud 60: Looking around nervously
- Cloud 85: Running toward exits
- Diegetic indicator: "If they're scared, you should be too"

---

## PLAYER STATE (HUDLESS)

### Credit Cards as Weapons

**First-Person View:**
- Credit card visible in hand (bottom of screen)
- Different cards have different colors (from palette)
- Active card is the one you SEE

**Card System (3 cards):**
```python
cards = {
    "VISA": {
        "color": palette["mall_blue"],
        "ability": "slows_time",
        "durability_max": 100
    },
    "MASTERCARD": {
        "color": palette["alert_red"],
        "ability": "damage_burst",
        "durability_max": 100
    },
    "AMEX": {
        "color": palette["warning_yellow_dark"],
        "ability": "shield",
        "durability_max": 100
    }
}
```

**Durability Indication (No Numbers):**
- Visual: Card edges become frayed/cracked
- 100%: Pristine card, sharp corners
- 50%: Visible wear, bent corners
- 10%: Barely readable, torn edges
- 0%: Card shatters (visual effect)

**Switching Cards:**
- Press 1/2/3 keys
- Card swap animation (flip/rotate)
- New card slides into view
- Color of hand/card changes

**Health/Damage:**
- No health bar
- Screen edge turns red when hurt
- Vision blurs
- Movement slows
- Heavy breathing audio
- Regenerates over time (fade back to normal)

---

## REACTOR PIT ENHANCEMENTS

### Procedural Overlays (Applied to Photo Textures)

**1. Concentric Circles**
- Draw on floor texture
- Paint-style decals
- Faded yellow (warning stripes)
- Centered on theater entrance

**2. Hazard Striping**
- Yellow/black diagonal stripes
- On escalator walls
- Around pit perimeter
- International warning aesthetic

**3. Industrial Grating**
- Metal floor texture overlay
- Diamond plate pattern
- Rust stains at edges
- Blend mode: multiply over photos

**4. Steam/Vapor Particles**
- Rising from pit bottom
- Particle system (20-50 particles)
- Slow upward drift
- Dissipates near ceiling
- Increases with Cloud level

**5. Dramatic Lighting**
- Harsh overhead spotlights
- Cast deep shadows
- Ray-traced shadows (if possible) or baked
- Increases contrast: reactor industrial feel

### Sound Design

**Escalator Hum (The E-flat Reference):**
- Base tone: 311 Hz (E-flat)
- Constant drone
- Slight warble (mechanical imperfection)
- Shifts pitch with Cloud:
  - Cloud 0: Pure E-flat
  - Cloud 50: Detuned, dissonant
  - Cloud 85: Multiple harmonics, beating frequencies

**Spatial Acoustics:**
- Large vertical space = reverb
- Footsteps echo
- Voices bounce off walls
- Theater "black mouth" = acoustic dead zone (sound absorbed)

**Ambient Layers:**
- Layer 1: Escalator hum (constant)
- Layer 2: Fluorescent light buzz
- Layer 3: Distant fountain water (from atrium above)
- Layer 4: Muzak (faint, from mall speakers)
- Layer 5: Your own breathing (first-person)

---

## SCOPE & DELIVERABLES

### Vertical Slice Contents

**Playable Area:**
- Food court pit floor (120' diameter)
- Escalator descent (8' drop)
- Upper landing connection
- Jolly Time theater entrance (exterior only, black void)

**Entities:**
- Player (first-person camera)
- Janitor NPC (contradiction test case)
- 2-3 Mall Walker NPCs (background, atmospheric)
- Toddler (invisible until Cloud 70+, reality catalyst)

**Systems:**
- Cloud system (0-100, 4 mood states)
- Toddler amplification (heat multiplier)
- Era contradiction (4-way flicker)
- Janitor LLM dialogue
- Hudless UI (all environmental)
- Photo texture rendering (40 frames)

**Visual Features:**
- COMICBOOK_MALL_V1 palette integration
- Era-based texture variants
- VHS glitch effects
- Chromatic aberration
- Vignette
- Reactor pit aesthetic overlays
- Steam particles
- Dramatic lighting

**Audio Features:**
- Escalator E-flat hum
- Reverb/echo
- Cloud-driven ambient layers
- NPC footsteps
- Player breathing

### What's NOT Included (Out of Scope)

- ❌ Other zones (atrium, corridors, stores)
- ❌ Combat system (credit cards visible but not functional)
- ❌ Full NPC roster (just Janitor + 2 walkers)
- ❌ Missions/objectives
- ❌ Save system
- ❌ Settings/options menu
- ❌ Theater interior (black void only)

---

## DEVELOPMENT PHASES

### Phase 1: Foundation (Renderer Setup)
- [ ] Copy v3 pygame_renderer.py to v7
- [ ] Load 40 food court frames as textures
- [ ] Basic raycaster display
- [ ] Player movement in pit space
- [ ] Verify 8' geometry from measurements

### Phase 2: Palette & Era System
- [ ] Integrate COMICBOOK_MALL_V1 palette
- [ ] Create 4 era texture variants
- [ ] Implement flicker logic (Cloud-driven)
- [ ] Test era cycling at different Cloud levels
- [ ] VHS glitch shader

### Phase 3: NPC Integration
- [ ] Add Janitor entity
- [ ] Implement contradiction movement
- [ ] Color-based state indication
- [ ] Tool glow effect
- [ ] Floating text dialogue system
- [ ] LLM hook for dialogue generation

### Phase 4: Hudless UI
- [ ] Remove all HUD elements
- [ ] Environmental Cloud indicators (lighting, vignette)
- [ ] Credit card first-person view
- [ ] Damage feedback (red tint, blur)
- [ ] NPC crowd reactions

### Phase 5: Reactor Aesthetic
- [ ] Concentric circle decals
- [ ] Hazard striping overlays
- [ ] Industrial grating texture
- [ ] Steam particle system
- [ ] Dramatic lighting pass

### Phase 6: Audio & Polish
- [ ] Escalator E-flat hum
- [ ] Spatial reverb
- [ ] Footstep sounds
- [ ] Cloud-driven ambient layers
- [ ] Breathing SFX

---

## SUCCESS CRITERIA

**The vertical slice is complete when:**

✅ Player can walk around food court pit
✅ 40 photo frames render as textures
✅ Era contradictions flicker at Cloud 70+
✅ Janitor breaks rule and triggers dialogue
✅ Zero HUD elements (all environmental feedback)
✅ Reactor pit aesthetic visible (circles, steam, hazards)
✅ COMICBOOK palette unifies the look
✅ Cloud state clear from environment alone
✅ Toddler proximity affects reality strain
✅ E-flat hum creates industrial atmosphere

**Demonstration Flow:**
1. Start at upper landing, Cloud = 0 (calm, stable 1995)
2. Descend escalator into pit (camera descends 8 feet)
3. Walk around pit floor, observe photo textures
4. Cloud rises to 30 → lights begin flickering
5. Cloud hits 70 → Janitor appears, walking toward pit
6. Janitor enters FC-ARCADE (forbidden zone) → contradiction
7. Era flicker intensifies, 1995/2005/2011 cycling
8. Janitor speaks (floating text): "The arcade machines hum E-flat..."
9. Toddler manifests nearby → reality strain increases
10. Screen glitches, chromatic aberration, vignette
11. All 4 eras visible simultaneously (flicker overlay)
12. Theater "black mouth" pulses at pit center
13. **Demo complete** - core systems proven

---

## NEXT STEPS

**Ready to proceed?**

This spec documents the complete food court vertical slice. It:
- Uses existing v3 renderer (no custom engine)
- Leverages 40 real photo frames
- Implements era contradictions (simultaneous realities)
- Tests Janitor NPC behavior
- Proves hudless UI concept
- Creates reactor pit aesthetic
- Stays faithful to v7 measurements

**Estimated work:** 6-12 hours (spread across phases)

**Your call:**
- Approve spec → I create detailed implementation plan
- Revise scope → Adjust what's included
- Start Phase 1 → Begin renderer adaptation

What do you want to tackle first?
