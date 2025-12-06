# PHOTO ASSETS - 3-LAYER SEMANTIC SORT

**Purpose:** AI-native photo organization for semantic understanding, canon building, and Sora integration.

---

## 🎯 The 3-Layer Sort Method

This structure enables Claude 4.5 and GitHub GPT to understand:
- **What** these assets mean
- **How** they relate
- **How** to reference them in canon
- **How** to use them in Sora prompts
- **How** to build consistent world logic

---

## Layer 1: PHYSICAL ZONES (Surface-Level Grouping)

**Purpose:** Basic spatial classification

Use ONLY when the file clearly belongs to a physical place:

```
zones/
├── escalators/        # Escalator photos (primary scale calibration)
├── food_court/        # Sunken food court (including pit)
├── movie_mouth/       # Movie theater entrance area
├── comphut/           # Computer store area
├── maintenance/       # Service corridors, back areas
├── atrium/            # Main atrium and fountain
└── exterior/          # Parking lot, building exterior
```

**Guidelines:**
- Only use if photo clearly shows a specific zone
- If ambiguous, use Layer 2 (semantic) instead
- Cross-reference with `v6-nextgen/canon/zones/`

---

## Layer 2: FUNCTIONAL SEMANTIC ZONES (AI Magic Layer) ⭐

**Purpose:** Meaning-based classification for AI understanding

This is THE MOST IMPORTANT layer. It tells AI what photos represent conceptually.

```
semantic/
├── architectural_features/     # Columns, masts, tensile roof, structural
├── lighting_conditions/        # Natural light, fluorescent, dim, shadows
├── material_patterns/          # Glass block, tile, carpet, concrete
├── signage_and_wayfinding/     # Directional signs, store signs, maps
├── reflections_and_mirrors/    # Reflective surfaces, glass, water
├── storefronts_closed/         # Shuttered stores, vacant spaces
├── storefronts_open/           # Active retail, displays
├── abandoned_elements/         # Decay, neglect, deterioration
└── flooring_patterns/          # Floor materials, patterns, wear
```

**Why This Matters:**

AI uses these categories to:
- ✓ Write canon documents
- ✓ Define zone characteristics
- ✓ Build environmental logic
- ✓ Understand Cloud-level moods
- ✓ Detect aesthetic rules
- ✓ Recognize contradictions
- ✓ Place NPCs correctly
- ✓ Write Sora 3-anchor location guides

**Classification Rules:**
1. Photo can be in MULTIPLE semantic categories
2. This is an "index of meaning," not just an index of images
3. Cross-reference with `/ai/sora/` prompt templates
4. Links to `ai/mallOS/` environmental state

---

## Layer 3: STORY/CHARACTER ZONES (Latent AI Grouping)

**Purpose:** Narrative and mood classification for MallOS/Cloud integration

Connects to SPYNT character spines and MallOS Cloud states:

```
narrative/
├── pov_shots/              # First-person perspective photos
├── human_scale/            # Photos showing scale via people/objects
├── mood_low_cloud/         # Calm, peaceful, optimistic (pressure 0-33)
├── mood_mid_cloud/         # Neutral, browsing, wandering (pressure 34-66)
├── mood_high_cloud/        # Tense, abandoned, eerie (pressure 67-100)
├── liminal/                # Transitional spaces, thresholds, emptiness
└── glitch_candidates/      # Photos showing contradictions, anomalies
```

**Integration:**

**MallOS Cloud States:**
- `mood_low_cloud/` → Cloud pressure 0-33 (TENSION, WANDER moods)
- `mood_mid_cloud/` → Cloud pressure 34-66 (WANDER, SURGE moods)
- `mood_high_cloud/` → Cloud pressure 67-100 (SURGE, BLEED moods)

**SPYNT Character Integration:**
- Use `human_scale/` for character placement logic
- Use `pov_shots/` for first-person narrative moments
- Use `liminal/` for character transition scenes

**Sora Prompt Generation:**
- Reference `glitch_candidates/` for bleed event visuals
- Use mood folders for tone matching
- Cross-reference with `ai/sora/shot_logic/cloud_mood_mapping.json`

---

## 📁 Current Contents

### eastland-archive/
**Status:** 153 photos from Flickr/community archives
**Next:** Sort into 3-layer structure using classification script

**Contents:**
- Historical photos (1981-2011)
- Various eras and conditions
- Mixed quality and perspectives
- Includes EXIF data (some photos)

---

## 🔧 Classification Workflow

### Step 1: Run Batch Classifier
```bash
python ai/pipelines/photo_processing/batch_classify.py \
  --input v6-nextgen/assets/photos/eastland-archive/ \
  --output classification_results.csv \
  --layers all
```

### Step 2: Review Classifications
- Check CSV for:
  - Layer 1 (zone) assignments
  - Layer 2 (semantic) tags (multiple allowed)
  - Layer 3 (narrative/mood) tags

### Step 3: Symlink Photos
```bash
python ai/pipelines/photo_processing/create_symlinks.py \
  --classification classification_results.csv \
  --source eastland-archive/ \
  --target zones/ semantic/ narrative/
```

### Step 4: Validate
```bash
python ai/pipelines/validation/validate_photo_structure.py
```

---

## 🎯 Classification Guidelines

### Layer 1 (Physical Zones)
**Ask:** "Where IS this?"
- If clear: Put in appropriate zone folder
- If ambiguous: Skip Layer 1, use Layer 2 instead

### Layer 2 (Semantic) ⭐
**Ask:** "What does this SHOW?" (multiple answers OK)
- Structural elements? → `architectural_features/`
- Light quality? → `lighting_conditions/`
- Material close-up? → `material_patterns/`
- Signs visible? → `signage_and_wayfinding/`
- Reflections? → `reflections_and_mirrors/`
- Store status? → `storefronts_closed/` or `storefronts_open/`
- Decay/neglect? → `abandoned_elements/`
- Floor visible? → `flooring_patterns/`

### Layer 3 (Narrative)
**Ask:** "What MOOD or STORY does this evoke?"
- POV angle? → `pov_shots/`
- People/scale reference? → `human_scale/`
- What Cloud pressure? → `mood_low/mid/high_cloud/`
- Transitional/empty? → `liminal/`
- Contradiction/anomaly? → `glitch_candidates/`

---

## 🔗 Integration Points

### With AI Tooling
- **`ai/sora/templates/`** - Reference semantic categories in prompts
- **`ai/mallOS/zones/`** - Link zone photos to simulation zones
- **`ai/spynt/`** - Use narrative photos for character context
- **`ai/renderist/`** - Pull from mood categories for lore

### With Canon
- **`v6-nextgen/canon/zones/`** - Each zone references Layer 1 photos
- **`v6-nextgen/canon/characters/`** - Characters link to narrative photos
- **`v6-nextgen/docs/reference/`** - Technical docs reference semantic photos

### With Sora
- **Prompt templates** use semantic categories:
  ```
  [LIGHTING] lighting_conditions/natural_sunlight_12.jpg
  [MATERIALS] material_patterns/glass_block_wall_04.jpg
  [MOOD] mood_high_cloud/abandoned_corridor_08.jpg
  ```

---

## 📊 Statistics (After Classification)

Will track:
- Total photos per Layer 1 zone
- Distribution across Layer 2 semantic categories
- Mood breakdown (Layer 3)
- Multi-tagged photos (photos in 2+ categories)
- Coverage gaps (missing semantic types)

---

## 🚀 Next Steps

1. ⏳ **Classify eastland-archive/** photos
2. ⏳ Create symlinks to 3-layer structure
3. ⏳ Validate coverage (check for gaps)
4. ⏳ Document semantic patterns
5. ⏳ Integrate with ai/sora/ templates
6. ⏳ Link to canon/ definitions

---

## 📝 Notes

**Why Symlinks?**
- Photos stay in `eastland-archive/` (preservation)
- Multiple layers can reference same photo
- Easy to adjust classifications

**Multi-Category Photos:**
A single photo can be:
- Layer 1: `zones/atrium/`
- Layer 2: `semantic/architectural_features/` + `semantic/lighting_conditions/`
- Layer 3: `narrative/mood_mid_cloud/`

This is intentional and encouraged.

**Automation:**
The `ai/pipelines/` scripts will handle:
- Batch classification
- Symlink creation
- Validation
- Gap detection

---

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  3-LAYER SORT = AI-NATIVE SEMANTIC UNDERSTANDING               ║
║                                                                ║
║  Layer 1: WHERE (physical zones)                              ║
║  Layer 2: WHAT (semantic meaning) ⭐ MOST IMPORTANT           ║
║  Layer 3: MOOD (narrative/Cloud states)                       ║
║                                                                ║
║  This gives AI an index of MEANING, not just images.          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

*Structure ready for classification.*
*Run batch classifier when ready to sort 153 photos.*
