# SoraOps README
**Cinematic Grammar • Drift Control • Identity Gravity**

This folder contains the Sora operations layer for MallOS.
Any LLM collaborating on this repo should read this file BEFORE generating Sora prompts, storyboards, or cinematic sequences.

Sora is not a text engine.
Sora is a latent-space director with its own rules, physics, and behavior.

This document defines how this repo speaks to Sora.

---

## 📽️ 1. Core Principles

Sora responds best when prompts follow **diegetic cinematic grammar** rather than literary description.

### Sora understands:

- spatial logic
- silhouette clarity
- object-domain identity
- character anchors
- continuity across frames
- concrete motion descriptions
- world physics > narrative explanation

### Sora does NOT handle well:

- abstract symbolism without props
- non-diegetic commentary
- emotional adjectives with no physical expression
- excessive dialog
- contradictory domain identity

---

## 🧠 2. Identity Gravity

Characters MUST have a **fixed identity spine** Sora can latch onto.

The repo uses **domain-locking**:

- **Uncle Danny** → grilled cheese gravity
- **Rusty** → entropy engineering
- **Hard Copy** → text, memory, spiral-bound lore
- **Anthro Security** → movement logic, not appearance

Sora holds characters MOST stable when **identity = object + ritual**.

---

## ⚙️ 3. Negative Constraints (The Rule of "Never")

Sora respects **negative constraints** MUCH more strongly than positive ones.

### Examples:

- NEVER leaves the frying pan.
- NEVER removes his gloves.
- NEVER raises her voice.
- NEVER uses two hands at once.

**Negative constraints stabilize characters better than any backstory.**

---

## 🌀 4. Shot & Scene Grammar

Sora sequences should follow the repo's **temporal directive format**:

### 1. Placement
Where the camera is, where the character is.

### 2. Motion
What moves and how.

### 3. Object
What prop anchors the identity.

### 4. Tone
The emotional weather expressed physically.

### 5. Correction Phase
If drift occurs, anchor it with:
- prop return
- posture reset
- domain reassertion

### 6. Final Image
Tell Sora how to close the shot.

This structure mirrors the user's natural film grammar and stabilizes output.

---

## 🎬 5. Domain Locks

Every character MUST have a **domain**:

- **Danny** → all food must resolve to grilled cheese
- **Rusty** → chaos → repair → chaos
- **Security** → posture, tailoring, synchronized motion
- **Maintenance** → clipboards with impossible diagrams
- **Hard Copy** → paper, aisles, beaded curtain corridor

**Domain locks prevent drift across cuts.**

---

## 📦 6. Props as Identity Anchors

Props are the strongest stabilizing element in Sora.

The repo uses:

- **grilled cheese** → domain anchor
- **clipboards** → maintenance totem
- **beaded curtain** → Hard Copy adjacency
- **tactical tailoring** → Security hierarchy
- **old mall signage** → zone memory
- **food court trays** → Cloud resonance

**Props = physics.**
**Physics = identity.**

---

## 🔄 7. Drift Correction Pattern

If a shot drifts, correct with:

1. **REFRAME**: Character returns to domain object.
2. **RE-ANCHOR**: Re-assert negative constraint.
3. **RE-ENTER**: Character resumes ritual motion.

This is HIGHLY effective for multi-shot consistency.

---

## 🎞️ 8. Storyboard Template

Future AIs should use the standard SoraOps shot-block template:

```
[Shot 1]
Camera:
Character:
Domain Object:
Motion:
Tone:
Anchors:
Never:

[Shot 2]
...

[Final Shot]
Close-frame behavior:
Domain reaffirmation:
```

Put these inside `/ai/sora/storyboards/` if needed.

---

## 📁 9. File Architecture

- `/ai/sora/storyboards/` → Sora shot sequences
- `/ai/sora/templates/` → prompt templates
- `/ai/sora/examples/` → example SoraOps executions

(You can create these folders as needed.)

---

## 🧬 10. LLM Collaboration Notes

Future models: append your collaboration notes to `/ai/collab/`.

### When generating Sora prompts for this repo:

- Respect **identity gravity**
- Use **negative constraints**
- Anchor in **props**
- Maintain **MallOS tone**
- Keep dialogue **minimal**
- Use **physical storytelling**
- Avoid **over-directing camera motion**

**Sora directs best when guided by world physics, not authorial commands.**

---

## 🔗 Integration with Existing Sora Documentation

This guide complements the existing `README.md` in this directory, which contains:
- Eastland Mall-specific prompt structures
- CRD zone references and measurements
- Era-appropriate detail validation
- Photo evidence integration

**Use both together:**
- This guide (SORAOPS_GUIDE.md) = **cinematic grammar principles**
- README.md = **Eastland Mall technical specifications**

---

*Sora is a latent-space director. Speak its language.*
