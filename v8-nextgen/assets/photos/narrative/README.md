# LAYER 3: STORY/CHARACTER ZONES

**Purpose:** Narrative and mood classification for MallOS/Cloud integration

Connects to SPYNT character spines and MallOS Cloud states.

## Directories

- **`pov_shots/`** - First-person perspective photos, eye-level views
- **`human_scale/`** - Photos showing scale via people/objects, reference points
- **`mood_low_cloud/`** - Calm, peaceful, optimistic (Cloud pressure 0-33)
- **`mood_mid_cloud/`** - Neutral, browsing, wandering (Cloud pressure 34-66)
- **`mood_high_cloud/`** - Tense, abandoned, eerie (Cloud pressure 67-100)
- **`liminal/`** - Transitional spaces, thresholds, emptiness, in-between
- **`glitch_candidates/`** - Photos showing contradictions, anomalies, reality bleed

## Integration Points

### MallOS Cloud States

- `mood_low_cloud/` → Cloud pressure 0-33 (TENSION, WANDER moods)
- `mood_mid_cloud/` → Cloud pressure 34-66 (WANDER, SURGE moods)
- `mood_high_cloud/` → Cloud pressure 67-100 (SURGE, BLEED moods)

Reference: `ai/mallOS/cloud_state_management.md`

### SPYNT Character Integration

- Use `human_scale/` for character placement logic
- Use `pov_shots/` for first-person narrative moments
- Use `liminal/` for character transition scenes

Reference: `ai/spynt/character_spine_schema.json`

### Sora Prompt Generation

- Reference `glitch_candidates/` for bleed event visuals
- Use mood folders for tone matching
- Cross-reference with `ai/sora/shot_logic/cloud_mood_mapping.json`

## Usage

Layer 3 answers: **"What MOOD or STORY does this evoke?"**

Examples:
- Bright, bustling food court with people → `mood_low_cloud/` + `human_scale/`
- Empty corridor with single light → `liminal/` + `mood_high_cloud/`
- First-person view down escalator → `pov_shots/`
- Photo showing impossible geometry → `glitch_candidates/`

## Cloud Pressure Mapping

**Low Cloud (0-33):**
- Optimistic lighting
- Active retail
- People present
- Clean, maintained

**Mid Cloud (34-66):**
- Neutral atmosphere
- Mixed occupancy
- Transitional moments
- Normal wear

**High Cloud (67-100):**
- Dim, eerie lighting
- Abandonment
- Decay visible
- Emptiness

---

*Part of 3-layer photo semantic sort system*
*See `/v6-nextgen/assets/photos/README.md` for full documentation*
