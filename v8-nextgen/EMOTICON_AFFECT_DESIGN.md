# Emoticon Affect Layer - Narrative Playground Design

## The Three-Layer System

```
Layer 1: WINGDINGS/EMOJI    = Structure & Meaning (objective)
Layer 2: EMOTICON           = Affect (subjective/emotional)
Layer 3: CONTEXT            = Narrative state (Cloud, Toddler, Era, Events)
```

---

## Philosophy

**Emoji layers answer:** "What IS this voxel?"
```
🟨🕐⬇️🌓⚙️🏃
= Metal escalator step, active, moving down, semi-gloss surface,
  mechanical hum, fast movement
```

**Emoticon layer answers:** "How does it FEEL?"
```
:|  = Normal (Cloud 20)
:/  = Unsettling (Cloud 65)
D:  = Alarming (Cloud 90 + Toddler)
```

**Same structure, different affect** = Narrative progression through emotional tone

---

## Emoticon Palette

### Baseline Affects

| Emoticon | Affect | Context |
|----------|--------|---------|
| `:|` | Neutral | Normal operation, Cloud < 30 |
| `:/` | Unsettling | Something's off, Cloud 50-70 |
| `:(` | Disturbing | This is bad, Cloud 70-85 |
| `D:` | Alarming | OH NO, Cloud 85+ or Toddler |
| `:)` | Comforting | 1981 opening, low strain |
| `;_;` | Melancholic | 2011 abandoned, resigned |
| `>:|` | Ominous | Threshold approaching, pre-cutscene |
| `:o` | Shocked | Post-cutscene, revelation |
| `o_O` | Curious | Discovery, exploration |
| `-_-` | Resigned | Acceptance, decline era |

### Intensity Scaling

Each affect has 3 intensity levels:

**Unsettling:**
```
Low:    :|  (noticing)
Medium: :/  (something's off)
High:   :\  (definitely wrong)
```

**Alarming:**
```
Low:    :(  (bad)
Medium: D:  (oh no)
High:   D:< (OH NO!)
```

---

## Context Resolution

Affect is determined by **weighted context factors:**

### Cloud Pressure (Base weight: 0.5)
```python
Cloud 0-30:   Neutral     :|
Cloud 30-50:  Curious     o_O
Cloud 50-70:  Unsettling  :/
Cloud 70-85:  Disturbing  :(
Cloud 85+:    Alarming    D:
```

### Era Timeline (Weight: 0.3)
```python
1981 Opening:    Comforting    :)
1995 Peak:       Neutral       :|
2005 Decline:    Melancholic   :(
2011 Abandoned:  Resigned      -_-
```

### Toddler Proximity (Weight: 0.8 - VERY STRONG)
```python
Visibility < 0.3:  No effect
Visibility 0.4+:   Unsettling    :/
Distance < 30:     Ominous       >:|
Distance < 15 + Manifested: Alarming  D:
```

### Recent Events (Weight: 1.0 - IMMEDIATE)
```python
CUTSCENE_TRIGGERED:    Shocked      :o
RULE_BROKEN:           Ominous      >:|
DISCOVERY:             Curious      o_O
CONTRADICTION:         Disturbing   :(
```

**Dominant affect = Highest weighted score**

---

## Narrative Applications

### 1. Dynamic State Feedback

**Same escalator across conditions:**

```
Normal operation (Cloud 20):
🟨🕐⬇️🌓⚙️🏃 :|

Rising tension (Cloud 65):
🟨🕐⬇️🌓⚙️🏃 :/

Reality strain (Cloud 90):
🟨🕐⬇️🌓⚙️🏃 D:

Toddler manifesting nearby:
🟨🕐⬇️🌓⚙️🏃 D:<
```

**Player sees the emotional shift without changing the voxel structure**

### 2. Multi-Era Timeline Affect

**Glass block fountain wall across eras:**

```
1981 Opening:
🪟✨🔒💎🧊 :)
(Pristine and wonderful)

1995 Peak:
🪟✨🔒💎🧊 :|
(Normal operation)

2005 Decline:
🪟💧🔒🌓🧊 :(
(Wet, dulled, sad)

2011 Abandoned:
🪟💔🌬️🌑🧊 -_-
(Broken, resigned)
```

**Structure degrades (emoji) + Affect shifts (emoticon)**

### 3. Pattern Absorption Integration

**NPCs absorb voxel affect patterns:**

```python
# Janitor encounters escalator at different Cloud levels
if voxel.emoticon == ":/":
    janitor.absorb_pattern("unease_escalator_rhythm")
    janitor.dialogue → "Steps sound... wrong today"

elif voxel.emoticon == "D:":
    janitor.absorb_pattern("terror_descent_machine")
    janitor.dialogue → "THE STAIRS WON'T STOP COUNTING"
```

**Emoticons become narrative triggers for NPC pattern system**

### 4. Cutscene Threshold Indicators

**Pre-cutscene visual feedback:**

```
Cloud approaching 85 (cutscene threshold):
All voxels shift to >:| (ominous)

Cloud crosses 85:
Cutscene triggers
All voxels shift to :o (shocked)

Post-cutscene:
Voxels return to context-appropriate affect
```

**Emoticons = visual tension/release markers**

### 5. Toddler Proximity Visualization

**ASCII "radar" using emoticons:**

```
Toddler distant (100+ feet):
Voxels: :|  :|  :|  :|  :|

Toddler approaching (50 feet):
Voxels: :|  :/  :|  :/  :|

Toddler manifesting (15 feet):
Voxels: :/  D:  D:  D:  :/

Toddler at player (< 5 feet):
Voxels: D:< D:< D:< D:< D:<
```

**Environment "reacts" to Toddler presence through affect**

---

## Technical Implementation

### VoxelWithAffect Class

```python
@dataclass
class VoxelWithAffect:
    emoji_compact: str      # "🟨🕐⬇️🌓⚙️🏃"
    emoticon: str           # ":/"
    affect_category: AffectCategory
    affect_intensity: float  # 0.0-1.0
    context: AffectContext

    def __str__(self) -> str:
        return f"{self.emoji_compact} {self.emoticon}"
```

### Context System

```python
@dataclass
class AffectContext:
    cloud_level: float = 50.0
    era: str = "1995_PEAK"
    toddler_visibility: float = 0.0
    toddler_distance: float = 999.0
    recent_event: Optional[str] = None
    time_of_day: float = 12.0
    player_sanity: float = 1.0
    zone_disturbance: float = 0.0
```

### Resolution Algorithm

```python
def resolve_affect(context: AffectContext) -> tuple[AffectCategory, float]:
    """
    1. Collect weighted affects from all context factors
    2. Find dominant affect (highest weight)
    3. Calculate intensity (0.0-1.0)
    4. Return (category, intensity)
    """
    affects = {
        cloud_affect: 0.5 * cloud_intensity,
        era_affect: 0.3,
        toddler_affect: 0.8 * toddler_visibility,
        event_affect: 1.0  # Immediate
    }

    dominant = max(affects.items(), key=lambda x: x[1])
    return dominant[0], min(1.0, dominant[1])
```

---

## Integration with Existing Systems

### Cloud System ✓
```python
from emoticon_affect_layer import add_affect_to_voxel, AffectContext

context = AffectContext(cloud_level=cloud.level)
voxel = add_affect_to_voxel(emoji_compact, context)
```

### Toddler System ✓
```python
context = AffectContext(
    cloud_level=cloud.level,
    toddler_visibility=toddler.visibility,
    toddler_distance=distance_to_player(toddler.pos)
)
```

### Cutscene Engine ✓
```python
# Pre-cutscene
context.recent_event = "CUTSCENE_IMMINENT"
# Voxels shift to >:| (ominous)

# Post-cutscene
context.recent_event = "CUTSCENE_TRIGGERED"
# Voxels shift to :o (shocked)
```

### NPC Pattern Absorption ✓
```python
from pattern_dialogue_engine import PatternProfile

# NPCs absorb emoticon patterns
if voxel.emoticon == "D:":
    janitor.pattern_profile.add_pattern(f"alarmed_{voxel.emoji_compact}")

# Later dialogue references absorbed affects
```

### LLM DM Narration ✓
```python
# Include affect in narration prompts
narrator_prompt = f"""
The escalator {voxel.emoji_compact} hums before you.
Emotional tone: {voxel.affect_category.value} {voxel.emoticon}

Narrate the player's perception.
"""
```

---

## Ren'Py Export Format

### Voxel with Affect

```renpy
# Voxel: Z5_ESCALATOR_WELLS_VOXEL_0000
# Emoji: 🟨🕐⬇️🌓⚙️🏃
# Affect: :/ (unsettling)

define voxel_z5_escalator_wells_0000 = {
    "emoji_compact": "🟨🕐⬇️🌓⚙️🏃",
    "emoticon": ":/",
    "affect": "unsettling",
    "affect_intensity": 0.65,

    "layers": {
        "material": {"emoji": "🟨", "name": "METAL_STEEL"},
        "state": {"emoji": "🕐", "name": "ACTIVE"},
        "behavior": {"emoji": "⬇️", "name": "SINKS"},
        "surface": {"emoji": "🌓", "name": "SEMI_GLOSS"},
        "audio": {"emoji": "⚙️", "name": "MECHANICAL_HUM"},
        "physics": {"emoji": "🏃", "name": "FAST"},
    },

    "context": {
        "cloud_level": 65,
        "era": "1995_PEAK",
        "toddler_visibility": 0.0
    }
}
```

### Dynamic Affect Screen

```renpy
screen voxel_display(voxel_id):
    python:
        voxel = voxel_registry[voxel_id]
        context = build_current_context()
        affect = resolve_affect(context)

    # Structure (emoji)
    text "[voxel.emoji_compact]" size 64

    # Affect (emoticon)
    text "[affect.emoticon]" size 48 color affect_color(affect)

    # Tooltip
    if affect.intensity > 0.7:
        text "Something feels very wrong here..."
```

---

## Storytelling Modes

### A) Simulation (Observer)
**Affect = Environmental state indicator**
```
Player observes voxel emoticons shifting as Cloud rises
:| → :/ → :( → D:
Emergent narrative from systemic pressure
```

### B) Stage (Director)
**Affect = Narrative control tool**
```
Player triggers events → affects cascade
RULE_BROKEN → all nearby voxels shift to >:|
Player as conductor of emotional tone
```

### C) Memory Palace (Archaeologist)
**Affect = Temporal artifact marker**
```
Same voxel across eras shows affect decay:
1981: :)  (hopeful)
2011: -_- (resigned)

Player excavates emotional history
```

**All three modes work because emoticons are context-responsive**

---

## Example: Full Escalator Journey

**Player descends food court escalator as Cloud rises:**

```
Step 1 (Cloud 20):  🟨🕐⬇️🌓⚙️🏃 :|  "Normal descent"
Step 3 (Cloud 40):  🟨🕐⬇️🌓⚙️🏃 :/  "Something feels off"
Step 6 (Cloud 60):  🟨🕐⬇️🌓⚙️🏃 :(  "The hum is wrong"
Step 9 (Cloud 80):  🟨🕐⬇️🌓⚙️🏃 D:  "It's counting me"

[Toddler manifests at bottom]

Step 12 (Cloud 90, Toddler visible): 🟨🕐⬇️🌓⚙️🏃 D:< "OH NO"

[Cutscene triggers: Theater void opens]

All steps shift to: 🟨🕐⬇️🌓⚙️🏃 :o  "What just happened"
```

**Structure never changed. Only affect.**

**The mall's emotional state is visible through emoticons.**

---

## Math: Affect Weighting

Given:
```
Cloud: 75  → Disturbing affect (weight 0.5 × 0.75 = 0.375)
Era: 1995  → Neutral affect (weight 0.3)
Toddler: visible 0.8, distance 12 → Alarming affect (weight 0.8 × 0.8 = 0.64)
Event: None → No event affect
```

Calculation:
```
Disturbing: 0.375
Neutral: 0.30
Alarming: 0.64  ← DOMINANT

Result: ALARMING affect, intensity 0.64
Emoticon: D: (medium intensity)
```

**Toddler proximity overrides Cloud pressure**

---

## Future Extensions

### 1. Affect Gradients
```
Voxels near player = higher intensity
Voxels distant = lower intensity
Creates "ripple" effect from player position
```

### 2. Affect Persistence
```
Post-cutscene: voxels "remember" shock state
Decay over time: :o → :/ → :|
Emotional echo of events
```

### 3. Player Sanity Modifier
```
player_sanity < 0.5 → all affects shift darker
:| becomes :/
:/ becomes :(
Reality distortion through player state
```

### 4. Compound Emoticons
```
Multiple simultaneous affects:
D:/ (alarmed + unsettled)
:o( (shocked + sad)
;_; (resigned + melancholic)
```

---

## Philosophy Summary

**Wingdings/Emoji** = The skeleton (structure, objective truth)
**Emoticon** = The flesh (affect, subjective experience)
**Context** = The soul (narrative state, story progression)

**Together:**
- Structure tells you WHAT
- Affect tells you HOW TO FEEL
- Context tells you WHY

**The mall has bones (emoji), but it FEELS through emoticons.**

The same escalator can be:
- A normal conveyance `:|`
- A source of unease `:/`
- A terror machine `D:`

**Not because it changed. Because YOU changed. Because the WORLD changed.**

That's the storytelling power of the emoticon affect layer.

---

## Commit Summary

**Added:**
- `emoticon_affect_layer.py` - Full affect resolution system
- 10 affect categories with emoticon mappings
- Context-aware affect resolution (Cloud, Toddler, Era, Events)
- Intensity scaling (3 levels per affect)
- Integration hooks for all v8 narrative systems

**Philosophy:**
Emoji = WHAT (structure/meaning)
Emoticon = HOW IT FEELS (affect)

**Result:**
The mall can now express emotional state through ASCII emoticons
while preserving structural emoji encoding.

Same voxel, different feels. 🟨🕐⬇️🌓⚙️🏃 :|  →  🟨🕐⬇️🌓⚙️🏃 D:
