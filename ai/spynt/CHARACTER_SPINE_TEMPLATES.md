# Character Spine Templates
**Identity Gravity • Domain Locks • Narrative Physics**

This file provides templates for creating new MallOS NPCs with full Spynt-compatible identity spines.

**All future NPCs MUST follow these templates.**
Characters are defined structurally, not descriptively.

Every spine has:

- **Domain Lock**
- **Never-List**
- **Ritual Motion**
- **Prop Anchors**
- **Zone Presence**
- **Cloud Influence**
- **Integration Notes**

Use these as fill-in-the-blank patterns when extending the mall.

---

## 🧬 1. BASIC NPC SPINE TEMPLATE

```markdown
# NPC NAME
## Role
[One sentence describing their functional presence.]

## Domain Lock
[The fundamental truth that anchors them.]

## Never-List
- NEVER [...]
- NEVER [...]
- NEVER [...]

## Rituals
- [...]
- [...]
- [...]

## Prop Anchors
- [...]
- [...]

## Zone Presence
Primary Zone:
Secondary Zone(s):

## Cloud Influence
Positive Modifiers:
Negative Modifiers:

## Adjacent NPCs
- [...]
- [...]

## Integration Notes
- [...]
```

**This is the universal skeleton.**

---

## 🧱 2. SHOPKEEP / RETAIL NPC TEMPLATE

```markdown
# [Shopkeeper Name] — [Store Type]
## Role
Maintains microzone identity and prevents spatial flattening.

## Domain Lock
[Merchandise type] + [Behavior pattern].

## Never-List
- NEVER misprice an item.
- NEVER rush a customer.
- NEVER leave the counter disorganized.

## Rituals
- Straightening merchandise in rhythmic patterns.
- Watching reflections instead of people.
- Giving commentary that matches their domain.

## Prop Anchors
- Cash drawer
- Item scanner
- Signature product

## Zone Presence
Retail Zone (Primary)
Main Hallway (Secondary)

## Cloud Influence
- Stabilizes hallway Cloud by [value].
- Reduces spatial monotony.

## Adjacent NPCs
- Sunglass Hut Guy
- Perfume Oracle

## Integration Notes
Use this NPC for grounding scenes between major zones.
```

---

## 🍽️ 3. FOOD COURT NPC TEMPLATE

```markdown
# [Food Worker Name] — [Stall Name]
## Role
Stabilizes Food Court Cloud and anchors smell-memory.

## Domain Lock
Food preparation anchored to [ingredient or method].

## Never-List
- NEVER burn anything.
- NEVER ignore a spill.
- NEVER let the counter go silent.

## Rituals
- Stirring, flipping, arranging, or tasting with ritual precision.
- Explaining life using food metaphors.

## Prop Anchors
- Food trays
- Spatula / Mixer / Knife
- Scent or steam

## Zone Presence
Food Court (Prime)

## Cloud Influence
- +0 to -2 depending on crowd.
- Reduces volatile Cloud spikes.

## Adjacent NPCs
- Pretzel Aunt
- Orange Julius Prophet

## Integration Notes
Food Court NPCs give scenes warmth & comedic timing.
```

---

## 🧯 4. SECURITY NPC TEMPLATE

```markdown
# [Rank / Name] — Security
## Role
Visible order layer; posture-based authority.

## Domain Lock
Motion-coded discipline + tailoring = authority.

## Never-List
- NEVER carry weapons.
- NEVER break formation casually.
- NEVER enter Maintenance sublevels (unless Raven).

## Rituals
- Patrol loops.
- Radio check-ins.
- Synchronized posture shifts.

## Prop Anchors
- Radios
- Utility belt
- Tailored uniform
- Segway (if Fox rank)

## Zone Presence
Atrium / Main Hallway / Dead Wing (Raven)

## Cloud Influence
- Dampens Cloud by [-1].
- Contradictions cause spikes based on rank.

## Adjacent NPCs
- Wolf Sergeant
- Dispatcher
- Fox Scout

## Integration Notes
Use movement logic from SECURITY_POSTURE_GUIDE.md.
```

---

## 🧹 5. MAINTENANCE NPC TEMPLATE

```markdown
# [Maintenance Worker Name]
## Role
Invisible structural stabilizer; quiet problem-solver.

## Domain Lock
Mall upkeep via impossible diagrams & rituals.

## Never-List
- NEVER be without a clipboard.
- NEVER say anything is strange.
- NEVER run (except major contradiction).

## Rituals
- Clipboard sync.
- Vent tapping.
- Door tension testing.
- Silent corridor inspection.

## Prop Anchors
- Clipboard (primary)
- Tool belt
- Flashlight
- HVAC keys

## Zone Presence
Service corridors
Sublevels L0–L3
Dead Wing adjacency

## Cloud Influence
- -1 structural drift when present.
- Prevents bleed escalation.

## Adjacent NPCs
- Rusty
- Wolf Sergeant (rarely)

## Integration Notes
Sublevel behavior follows SUBLEVEL_TOPOLOGY_MAP.md.
```

---

## 🎨 6. AESTHETIC NPC TEMPLATE (Atmosphere Anchors)

```markdown
# [Aesthetic NPC Name] — [Vibe Anchor]
## Role
Provides tone, texture, or emotional color to a zone.

## Domain Lock
Visual / emotional motif tied to [object] or [aesthetic].

## Never-List
- NEVER break posture.
- NEVER acknowledge anomalies.
- NEVER leave their aesthetic zone.

## Rituals
- Repeating motions that match the vibe.
- Maintaining perfect symmetry or asymmetry.

## Prop Anchors
- Mirrors
- Plants
- Decorative objects

## Zone Presence
Main Hallway
Atrium
Fountain Court

## Cloud Influence
- Softens / sharpens emotional energy depending on motif.

## Integration Notes
Aesthetic NPCs keep scenes from feeling empty or flat.
```

---

## 🎭 7. CHARACTER ACTOR TEMPLATE (Special Use NPCs)

```markdown
# [Character Actor Name] — [Role Type]
## Role
Appears in Sora sequences as identity-play characters.

## Domain Lock
Always expresses the same archetype.

## Never-List
- NEVER drop the character mid-shot.
- NEVER break eye focus.
- NEVER use props outside domain.

## Rituals
- Repeating gestures.
- Catchphrases (minimal).
- Consistent stance.

## Prop Anchors
- Costume item
- Signature object

## Zone Presence
Flexible — depends on scene

## Cloud Influence
- Controlled, small ripples.
- Good for controlled tension.

## Integration Notes
Use for TikTok / Sora micro-stories.
```

---

## 🧠 8. MINI-SPINE TEMPLATE (for background NPCs)

```markdown
# [Background NPC Name]
Domain Lock: [simple truth]
Never: NEVER [...]
Prop: [...]
Zone: [...]

Behaviors:
- [...]
- [...]
```

Small, clean, perfect for fast population of scenes.

---

## 📌 9. LLM Collaboration Notes

When creating new NPCs:

- **Always** define Domain Lock
- **Always** include a Never-List
- **Always** give at least 2 prop anchors
- **Always** specify zone presence
- **Never** ignore Cloud influence
- **Append**; never overwrite
- Log addition in `/ai/collab/`

---

**Character identity is physics, not backstory.**
**Use these templates to keep the Mall stable.**
