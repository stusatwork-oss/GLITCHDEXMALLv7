# NARRATIVE HOOKS – STORY INTEGRATION POINTS

This document describes how narrative is woven into the engine without explicit quest/objective systems.

## NPC Dialogue Framework

### Milo (The Lore-Keeper)

**Role**: Primary narrator. Tells the history of every artifact.

**Dialogue Triggers**:
- Player enters STORE_MILO_OPTICS → greeting
- Player shows artifact (talks to Milo with item selected) → artifact lore
- Player carries 3+ artifacts → commented on strangeness
- Toddler Stage 2+ → Milo expresses concern (can't identify the sound, but it's wrong)
- Toddler Stage 3 → Milo suggests leaving (panic is creeping in)

**Artifact Lore Examples**:
```
sunglasses:
  "These came from BORED's dressing room, 1994. Kid left them
   and never came back. They still smell like Axe body spray."

necronomicon_bookmark:
  "This marked a page in a book from the anchor store. Someone
   reported the entire book vanishing. No title recorded. Weird."

sticker_sheets:
  "1998 rave stickers. Everyone with a sheet like this moved
   away that summer. Same month. All of them."
```

**Milo's Commentary** (Stage-based):
```
Stage 0-1: "The mall's dying, you know. Retail apocalypse."
Stage 2: "Do you hear that? What is that sound?"
Stage 3: "We need to go. Now. Something's very wrong."
```

### BORED (The Apathetic Kid)

**Role**: Local color. Confirms the vibe of the mall, especially his shop.

**Dialogue Triggers**:
- Player enters STORE_BORED → acknowledgment (barely looks up)
- Player lingers → random sarcastic comment
- Toddler Stage 2+ → BORED shows unease
- Toddler Stage 3 → BORED is visibly scared, huddles behind counter

**Example Lines**:
```
"Yeah, we're open. Kinda."
"You gonna buy something or...?"
"This mall's haunted or whatever. No one comes here anymore."
"(nervous fidgeting) Did you hear that? Please tell me you heard that too."
```

### R0-MBA (Silent Observer)

**Role**: Environmental chronicler. Doesn't speak directly to player but leaves traces.

**Behavior**:
- Roams SERVICE_HALL and CORRIDOR areas on patrol
- If player encounters R0-MBA on same tile:
  - "R0-MBA's optical sensors whirr as it rolls past."
  - No dialogue, just observation
- **Event Log**: R0-MBA logs encounters ("R0-MBA observed player at FOOD_COURT, 12:34")
- Toddler Stage 3: R0-MBA's movements become erratic (gets scared/avoids player)

**In Narrative**: R0-MBA is the game's witness. Its logs are flavor text that reinforce the passage of time.

### Mall Cop

**Role**: Authority figure. Reacts to artifact carrying.

**Dialogue Triggers**:
- Player carrying Necronomicon openly → "That's... unusual for the mall."
- Repeated encounters → "You've been here a while."
- Toddler Stage 3 → Mall Cop abandons post, says "I'm going to get coffee. For like 2 hours."

**Example Lines**:
```
"Is that a book? Who reads anymore?"
"Look, I don't get paid enough for this."
"I'm leaving. You should too."
```

### Generic Shoppers

**Role**: 1988 Nintendo sparseness. Ambient NPCs that underscore isolation.

**Behavior**:
- Occasional idling in FOOD_COURT
- Minimal dialogue: "Shopping?" / "The sales suck this year."
- React to toddler stages (look uncomfortable, hurry away)

---

## Environmental Narrative Triggers

### Sound Design Cues

**Stage 1** (0–5 min):
- Distant, muffled crying (1–2x per minute)
- "A baby's wail echoes from somewhere deeper in the mall..."
- Rare and easy to dismiss

**Stage 2** (5–15 min):
- Wails become frequent (every 30–45 seconds)
- "The crying is louder now. It's coming from... somewhere."
- Players can no longer ignore it
- NPCs start reacting

**Stage 3** (15+ min):
- Constant, increasing screaming
- "THE CRYING DOESN'T STOP. IT'S EVERYWHERE."
- Chaos events trigger (escalators rattle, lights flicker)
- NPCs abandon posts

### Shadow Mechanics

**Stage 1**:
- Rare shadow flickers at edge of vision
- "Did something just move in the corner?"

**Stage 2**:
- Shadow visible in corners of main rooms
- Shadow blocks parts of corridors (player can still move through)
- Visual distortion increases with proximity

**Stage 3**:
- Shadow fills most of the screen
- Player can see it, but can't interact with it
- Rendering becomes increasingly distorted

### Event Cascades (Toddler Stage 3)

When toddler reaches Stage 3, chaos events trigger:

```
Event: Escalator Rattle
Description: "The escalators start screaming. Metal on metal. Awful."

Event: Crowd Panic
Description: "Everyone in the food court suddenly gets up and leaves."

Event: Light Flicker
Description: "Fluorescent lights strobe. On. Off. On. Off. The shadows dance."

Event: Object Displacement
Description: "Did the mall just... shift? Corridors look slightly different."
```

These events don't change tile layout, but they shift perception. The game's rendering gets jankier as stage 3 progresses.

---

## Artifact as Narrative Catalysts

Each artifact is a **story node**. Finding it and talking to Milo creates a micro-narrative:

**Discovery Phase**: "Found sunglasses in BORED's dressing room area."

**Inquiry Phase** (talk to Milo):
> "Oh, those. Yeah. Kid left them here in '94. Used to come every weekend.
> Then one day, didn't show up. Parents never reported him missing.
> Weird how that happens in malls."

**Carrying Phase** (player holds artifact):
- Visual glitch increases
- Milo starts looking at the artifact uncomfortably
- Artifact might influence where toddler presence feels strongest

**Example Artifacts & Their Stories**:

1. **Sunglasses** – Kid who vanished, left belongings
2. **Necronomicon Bookmark** – Book that disappeared, never catalogued
3. **Sticker Sheet** – 1998 rave promotion. Everyone with it moved away same month.
4. **Food Court Tray** – From 1987. Still has food residue. Never cleaned.
5. **Escalator Grease** – Oil collected from step. Smells like rust and synthetic.
6. **Gift Card (Dead Brand)** – $50 balance from a store that closed in 2003.
7. **Leather Wallet** – No ID, just receipts from 1996.
8. **Keychain** – Key to nothing. Unknown what lock it fits.
9. **Film Roll** – Developed in 1989, photos are blank or overexposed.
10. **Arcade Token** – From arcade that doesn't exist in the mall.

---

## No Objectives, Only Flavor

**Key Design Rule**: Artifacts and NPC dialogue never gate progression or create objectives.

- Player doesn't need to "collect all artifacts"
- NPCs don't give quests ("Go find the blue wallet")
- Stories are optional discoveries, not required plot

The narrative is **emergent** from:
1. Playtime (toddler intensity)
2. Artifact discovery (random, optional)
3. NPC encounters (sparse, environmental)
4. Environmental sounds and effects

Players create their own story by exploring, finding artifacts, and deciding when to leave.

---

## Story Generators & Prompts

The engine logs all discoveries in a **session transcript**:

```
[00:00] Player spawned at ENTRANCE
[00:15] Player moved to CORRIDOR_NORTH
[01:02] Player discovered: sunglasses (STORE_BORED area)
[01:15] Player talked to BORED ("Yeah, we're open. Kinda.")
[02:30] Player reached MILO_OPTICS, talked to Milo
        Milo told artifact lore: sunglasses story
[03:45] Toddler Stage 1 triggered. First cry heard.
[05:00] Player discovered: sticker_sheets (ANCHOR_STORE)
[06:30] Toddler Stage 2 triggered. Wails intensify.
[07:15] R0-MBA passed player in SERVICE_HALL
[08:00] Player talked to MILO again
        Milo expressed concern: "Do you hear that?"
[12:00] Toddler Stage 3 triggered. Chaos events begin.
[12:45] Player reached ENTRANCE, left the mall.
```

This transcript can be fed to a narrative generator or examined as its own artifact.

---

## Integration with Engine

- NPC dialogue is **stored in entities.json** with stage conditions
- Artifact lore is **stored in artifacts.json**
- All dialogue triggers are **checked in game_loop.py** during state updates
- Event logs are **written to session transcript** automatically
