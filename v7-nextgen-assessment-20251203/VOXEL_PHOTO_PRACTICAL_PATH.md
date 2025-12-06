# V7 Voxel + Photo Practical Path

**Date:** 2025-12-03
**Goal:** Retro voxel rendering (Doom↔Minecraft style) using existing photos and renderers

---

## WHAT WE HAVE

### Renderers (3 existing)

**1. Wolf Renderer (v1-doofenstein)**
- **Type:** ANSI terminal raycaster
- **Style:** Unicode block patterns, 256-color palette
- **Textures:** Procedural (BRICK, TILE, CONCRETE, GLASS, METAL patterns)
- **Status:** ✅ COMPLETE, playable game
- **File:** `v1-doofenstein/src/wolf_renderer.py`

**2. Pygame Renderer (v3-eastland)**
- **Type:** Graphical raycaster (Wolf3D-style)
- **Style:** Procedural textures with tile patterns
- **Era Support:** ✅ ALREADY HAS ERA-BLEED SYSTEM!
  - `self.textures` - Decay era (late 80s worn)
  - `self.modern_textures` - Modern renovated versions
- **Stores:** BORED, Milo Optics, Hard Copy, CompHut, etc.
- **Status:** ✅ COMPLETE, graphical + all v2 AI systems
- **File:** `v3-eastland/src/pygame_renderer.py`

**3. Voxel Builder (v7-nextgen)**
- **Type:** Geometry generator (not a renderer)
- **Input:** Measurements from v5 CRD data
- **Output:** JSON voxel boxes/cylinders for zones
- **Status:** ✅ EXISTS, generates `v7_mall_doom.json`
- **File:** `v7-nextgen/src/voxel_builder.py`

### Photos (46 total)

**Food Court Video Frames (40 photos)**
- Location: `./processed/frames/foodcourt-2010/`
- Files: `frame_0001.png` through `frame_0040.png`
- Era: 2010 (decline era, near closure)
- Coverage: Food court area only

**Eastland Archive (3 photos)**
- v6: `v6-nextgen/assets/photos/eastland-archive/h8o3ufj4tuqe1.jpeg`
- v7: Same photo (copied)
- Raw reference: `raw/reference-video/foodcourt_2010.mp4`

**Classification System (v6 canon)**
- 3-layer system: zones/semantic/narrative
- Batch classification manifests exist
- Photo slots defined but empty (36 referenced photos missing)

### Zone Measurements (v7 canon)

**From v5 CRD Integration:**
- 9 zones fully measured
- Atrium: 175' diameter, 70' ceiling
- Food court pit: 8' descent
- Corridors: 18-25' wide
- Full spatial data ready for voxel builder

---

## ERA DEGRADATION STRATEGY

**User Requirements:**
- **1981:** NEW (pristine)
- **1995:** DIRTY (starting era - baseline)
- **2005:** BROKEN (decline)
- **2011:** MOSTLY ABANDONED LOOKING (closure)

**Good News:** v3 Pygame renderer ALREADY has era-bleed scaffolding!
- `textures` dict = default/worn look
- `modern_textures` dict = clean/renovated look
- Just needs 4-way expansion for degradation levels

---

## PRACTICAL PATH FORWARD

### Option A: Adapt v3 Pygame Renderer (FASTEST)

**What it gives you:**
- Working raycaster with texture system
- Era-bleed framework already exists
- All v2 AI systems (Cloud, NPCs, factions, stealth)
- Playable RIGHT NOW

**What you'd add:**
1. **COMICBOOK_MALL_V1 palette** → Replace procedural colors
2. **4-era texture variants** → Expand from 2 to 4 (new/dirty/broken/abandoned)
3. **Photo textures** → Use food court frames as actual textures instead of procedural
4. **Voxel geometry** → Feed v7 measurements to adjust zone sizes

**Work estimate:** 2-4 hours to adapt

**Steps:**
```python
# 1. Import COMICBOOK palette into pygame renderer
palette = load_palette("TILE_PALETTE_MAPPINGS.json")

# 2. Create 4 texture variants per tile
textures_1981 = generate_clean(palette)    # NEW
textures_1995 = generate_dirty(palette)    # DIRTY (baseline)
textures_2005 = generate_broken(palette)   # BROKEN (flickering, cracks)
textures_2011 = generate_abandoned(palette) # ABANDONED (darkness, decay)

# 3. Load food court frames as textures
food_court_tex = load_frames("./processed/frames/foodcourt-2010/*.png")

# 4. Era switching
current_era = 1995  # Starting era
render_with_textures(textures[current_era])
```

### Option B: Build New Voxel Renderer from Scratch (CUSTOM)

**What it gives you:**
- Exactly the visual style you want
- Minecraft-like block aesthetic
- Full control over rendering

**What you'd need:**
- 3D graphics library (pygame/pyglet/OpenGL)
- Camera system
- Voxel mesh rendering
- Texture mapping
- Collision detection
- ~40-80 hours of work

**Reality check:** You said "custom engines are TUFF" - this is the hard path

### Option C: Hybrid (v3 Renderer + v7 Measurements)

**Best of both worlds:**
- Use v3 Pygame renderer as BASE
- Feed it v7 zone measurements for accurate scale
- Apply COMICBOOK palette
- Add 4-era degradation
- Replace procedural textures with food court photo textures

**This is the SWEET SPOT** - existing renderer, faithful to measurements, uses real photos

---

## PHOTO STRATEGY

### What Photos Do We Actually Have?

**Food Court Only:**
- 40 frames from 2010 walkthrough video
- Covers: sunken area, seating, vendor stalls, escalator descent
- Era: 2005-2011 (decline/closure)

**What's Missing:**
- Atrium/fountain
- Escalators (upper landing)
- Corridors
- Stores (Milo, CompHut, BORED, etc.)
- Exterior
- Cinema entrance

### Practical Photo Approach

**DON'T:**
- ❌ Try to do NeRF reconstruction (you said "too time intensive")
- ❌ Generate 36 missing photos with AI (risky, time-consuming)
- ❌ Build custom photo-to-voxel pipeline

**DO:**
- ✅ Use food court frames as ACTUAL food court textures
- ✅ Use procedural textures for missing zones (like v3 does)
- ✅ Let COMICBOOK palette unify the look
- ✅ Add photos later as you get them (modular approach)

**Hybrid Texture Strategy:**
```
ZONES WITH PHOTOS:
- Food Court → Use processed frames (40 available)

ZONES WITHOUT PHOTOS (use procedural + palette):
- Atrium → Use palette "ATRIUM_FOUNTAIN" colors
- Corridors → Use palette "CORRIDOR" colors
- Stores → Use palette "STORE_*" colors
- Escalators → Use palette "ESCALATOR_WELL" colors
- Exterior → Use palette "EXTERIOR_PARKING" colors
```

---

## RECOMMENDED PATH (Today)

**Phase 1: Adapt v3 Renderer (2-4 hours)**

1. **Copy v3 pygame renderer to v7**
   ```bash
   cp v3-eastland/src/pygame_renderer.py v7-nextgen/src/
   ```

2. **Integrate COMICBOOK palette**
   - Replace RGB tuples with palette lookups
   - Map tile types to palette tags

3. **Add 4-era texture generation**
   - Expand from 2 eras to 4
   - Apply degradation filters:
     - 1981: brightness +15%, saturation +10%
     - 1995: baseline
     - 2005: brightness -15%, add cracks/flicker
     - 2011: brightness -40%, add darkness zones

4. **Wire to v7 Cloud system**
   - Era transitions at Cloud thresholds
   - Reality strain effects from toddler system

5. **Test with food court textures**
   - Load 40 frames
   - Apply to food court zone
   - Verify degradation across eras

**Phase 2: Connect Measurements (1-2 hours)**

1. Use v7 spatial measurements for zone sizing
2. Adjust corridor widths (18-25' not standard 12')
3. Scale atrium to 175' diameter

**Phase 3: Populate Missing Zones (ongoing)**

1. Use procedural textures + COMICBOOK palette
2. Add real photos as you acquire them
3. Modular texture swapping system

---

## TECHNICAL NOTES

**v3 Pygame Renderer Capabilities:**
- Raycasting (Wolf3D-style)
- Texture mapping
- Floor/ceiling rendering
- Era-bleed (2-way, needs expansion to 4-way)
- Procedural texture generation
- Integration with Cloud/heat system
- NPC rendering
- Prop system

**What Needs Adaptation:**
- Color palette (RGB tuples → COMICBOOK tags)
- Era count (2 → 4)
- Zone dimensions (use v7 measurements)
- Photo texture loading (add for food court)

**What You Get:**
- Playable game TODAY
- Retro raycaster aesthetic (Doom-like)
- Real photos in food court
- Procedural elsewhere (looks cohesive with palette)
- 4-era degradation
- All v7 horror systems (Cloud, Toddler, NPCs)

---

## DECISION POINT

**Do you want me to:**

**A)** Adapt v3 Pygame renderer to v7 with COMICBOOK palette + 4-era system?
   - Fastest path to playable voxel game
   - Uses existing renderer
   - Food court gets real photos, rest is procedural

**B)** Just create a texture loading system for food court frames?
   - Minimal change
   - Proof of concept for photo→texture pipeline
   - Can expand later

**C)** Document the adaptation plan for later?
   - No coding yet
   - Full specification for when you're ready

**My recommendation:** Option A - adapt v3 renderer. It's 90% done, just needs palette + era expansion + photo loading. You'd have a playable voxel mall game by end of day.
