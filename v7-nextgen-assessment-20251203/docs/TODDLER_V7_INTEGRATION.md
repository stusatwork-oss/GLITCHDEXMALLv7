# TODDLER V7 INTEGRATION – Reality Catalyst System

**Status:** Design Document
**Source:** v2 Toddler System (invisible reality catalyst)
**Target:** V7 Integration (Cloud/QBIT/Leon-aware)
**Purpose:** Mobile QBIT blender that makes zones go weird

---

## EXECUTIVE SUMMARY

The Toddler from v2 is an **invisible reality catalyst** with its own state that outputs effects each tick:
- `heat_multiplier` → feeds Cloud pressure
- `glitch_multiplier` → feeds renderer strain
- `in_distortion_field` → affects player perception
- `reality_strain` → zone QBIT agitation

**In V2:** Self-contained horror engine with "heat 1–5" toy model
**In V7:** Wired into Cloud, QBIT, zones, and Leon's awareness

**Key Insight:** The toddler's "heat" concept becomes a **Cloud input**, not its own separate bar.

---

## 1. WHAT THE TODDLER ALREADY IS (FROM V2)

An invisible reality catalyst with its own state:
- `position` - Where in the mall it is
- `behavior` - Current behavioral mode
- `visibility` - 0.0 (invisible) to 1.0 (fully manifested)
- `reality_strain` - How much it's warping local space
- `distortion_radius` - Area of effect around it

A system that outputs an **effects dict** each tick:
```python
{
    "heat_multiplier": 1.5,           # Amplifier for Cloud pressure
    "glitch_multiplier": 2.0,         # Amplifier for visual/audio glitches
    "in_distortion_field": True,      # Player is within effect radius
    "distortion_intensity": 0.7,      # How strong the distortion is
    "distance_to_player": 12.3,       # Distance in feet
    "toddler_visible": 0.3,           # Visibility level (0-1)
    "reality_strain": 0.8,            # Reality fabric stress
    "toddler_position": (x, y, z)     # World coordinates
}
```

Hooks for:
- Visual distortion (screen warps, vignettes, reality tears)
- Audio (drone, whispers, heartbeat, static)
- Wolf3D-style render/ASCII render, camera shake, renderer strain

**V2 basically gave you a self-contained horror engine you can drop into any loop.**

---

## 2. WHERE TODDLER LIVES IN V7

### Folder Structure

```
v7-nextgen/
  src/
    sim/
      mall_simulation.py      # Integration point
      cloud_system.py
      qbit_engine.py
      zones.py
    ai/
      toddler/
        __init__.py
        toddler_system.py     # From v2, lightly adapted
        toddler_config.py     # Behavior configs
        toddler_behaviors.py  # Behavioral modes
```

### Integration Point: MallSimulation

```python
class MallSimulation:
    def __init__(self, ...):
        self.cloud = CloudSystem(...)
        self.qbit = QbitEngine(...)
        self.toddler = ToddlerSystem(initial_pos, config)
        # ...

    def update(self, dt, player_action):
        # 1) Normal sim update
        self._update_player(dt, player_action)
        self._update_npcs(dt)
        self._update_zones(dt)

        # 2) Toddler update (now Cloud-aware)
        toddler_effects = self.toddler.update(
            dt,
            player_position=self.player.position,
            current_cloud=self.cloud.level,
            world_tiles=self.world.tiles
        )

        # 3) Apply toddler → Cloud/QBIT/render effects
        self._apply_toddler_to_cloud(toddler_effects)
        self._apply_toddler_to_qbit(toddler_effects)
        self._apply_toddler_to_renderer(toddler_effects)

        # 4) Package full state (for renderer + Leon)
        return {
            "player": self.player.export_state(),
            "zones": self.zones.export_state(),
            "cloud": self.cloud.export_state(),
            "qbit": self.qbit.export_state(),
            "toddler": self.toddler.export_state(),
            "toddler_effects": toddler_effects,
            # plus anything else (Janitor, events, etc.)
        }
```

**The key twist:** Toddler's "heat" concept in v2 becomes a **Cloud input** in v7, not its own separate bar.

---

## 3. TODDLER ↔ CLOUD MAPPING

In v2, toddler returns `heat_multiplier` + `glitch_multiplier` as generic amplifiers.
In v7, those should feed your **Cloud Pressure** and **Render Tax / glitch systems**.

### 3.1 Cloud Pressure Hook

```python
def _apply_toddler_to_cloud(self, toddler_effects):
    """
    Toddler proximity amplifies Cloud pressure gain.

    Effect: just being near / seeing the toddler makes everything else spiral faster.
    Cloud mood → Leon → missions → zone failures → destruction.
    """
    # Base Cloud gain this tick from normal sim
    base_delta = self.cloud.compute_base_delta()

    # Toddler proximity amplifies it
    heat_mult = toddler_effects.get("heat_multiplier", 1.0)
    distance = toddler_effects.get("distance_to_player", 999)

    # Optional: extra spike when VERY close + visible
    close_bonus = 0.0
    if distance < 5 and toddler_effects.get("toddler_visible", 0) > 0.5:
        close_bonus = 0.5  # tweak

    cloud_delta = base_delta * heat_mult + close_bonus

    self.cloud.add_pressure(
        source="TODDLER",
        amount=cloud_delta,
        tags={
            "distance": distance,
            "reality_strain": toddler_effects.get("reality_strain", 0.0)
        }
    )
```

**Result:** Just being near / seeing the toddler makes everything else spiral faster.

### 3.2 Render / Glitch Hook

```python
def _apply_toddler_to_renderer(self, toddler_effects):
    """
    Feed toddler glitch/strain into renderer.

    Used for:
    - Screen glitch, chromatic aberration, vignettes
    - In voxel/Wolf3D: color shifts, sprite jitter, fake Z-fighting
    """
    glitch_mult = toddler_effects.get("glitch_multiplier", 1.0)
    reality_strain = toddler_effects.get("reality_strain", 0.0)

    # Feed into existing "renderer strain / glitch" system
    self.renderer_state.glitch_intensity = (glitch_mult - 1.0) / 3.0
    self.renderer_state.reality_strain = reality_strain

    # Optional: camera shake when very close
    if toddler_effects.get("distance_to_player", 999) < 10:
        self.renderer_state.camera_shake = reality_strain * 0.2
```

**The toddler stays a global instability multiplier.**

---

## 4. TODDLER ↔ QBIT / ZONES

V7 has: zones with QBIT aggregates and adjacency logic.

**Simple first rule:** When the toddler is inside a zone, that zone's QBIT aggregate is **"agitated"**.

That makes it a more likely candidate for:
- Zone events (lockdowns, failures)
- Leon commentary
- Spawning micro-glitches / NPC contradictions

```python
def _apply_toddler_to_qbit(self, toddler_effects):
    """
    Toddler = mobile "QBIT blender" that makes whatever zone it's in more likely to go weird.
    """
    toddler_pos = toddler_effects.get("toddler_position")
    if not toddler_pos:
        return

    zone = self.zones.get_zone_at(toddler_pos)
    if not zone:
        return

    # Agitate that zone in QBIT space
    self.qbit.apply_disturbance(
        zone_id=zone.id,
        intensity=toddler_effects.get("reality_strain", 0.0),
        source="TODDLER"
    )

    # Optional: increase likelihood of events in that zone
    distortion = toddler_effects.get("distortion_intensity", 0.0)
    zone.event_weight_modifiers["toddler_presence"] = 1.0 + distortion

    # Tag zone as "haunted" for Leon awareness
    zone.tags.add("TODDLER_PRESENT")
```

**Think of it as:** Toddler = mobile "QBIT blender" that makes whatever zone it's in more likely to go weird.

---

## 5. TODDLER ↔ LEON (LLM Layer)

To "bring the toddler back in" with Leon, you just make him aware of toddler state in `game_state`:

```python
game_state_for_leon = {
    "game_time": self.time,
    "player_location": current_zone.id,
    "entropy": self.cloud.level,
    "cloud_mood": self.cloud.mood,
    "zones": self.zones.export_state(),
    "active_mission": self.missions.current().export_state(),
    "nearby_npcs": self.npcs.export_near_player(),

    # NEW: Toddler context
    "toddler": {
        "visible": toddler_state.visible,
        "distance": toddler_effects["distance_to_player"],
        "reality_strain": toddler_effects["reality_strain"],
        "in_distortion_field": toddler_effects["in_distortion_field"],
        "current_zone": toddler_zone.id if toddler_zone else None
    }
}
```

### Leon's System Prompt Addition

```
If toddler.reality_strain is high near the player, you may describe feelings of:
- Wrong geometry (angles that don't add up)
- Wrong sound (frequencies that hurt)
- Reality "buzzing" or "thinning"

Rules for toddler acknowledgment:
- If toddler.visible < 0.3: DO NOT name it. Only ambient unease.
- If toddler.visible 0.3-0.7: You may notice "movement in peripheral vision" or "something small".
- If toddler.visible > 0.7: You may directly acknowledge the entity.

The toddler is not hostile. It is a catalyst. Its presence accelerates decay.
```

### Behavioral Gradient

| Cloud Level | Toddler Visible | Leon's Response |
|-------------|-----------------|-----------------|
| Low (0-40) | Invisible (0.0-0.2) | "Everything's fine. Just the AC." |
| Mid (40-70) | Semi-visible (0.3-0.5) | "Did you hear that? No, probably just... wait." |
| High (70-85) | Manifesting (0.6-0.8) | "There's something in the food court. Don't look directly at it." |
| Critical (85+) | Fully visible (0.9-1.0) | "It's following you. It's been following you the whole time." |

**The toddler becomes a shared object of dread for both player and Leon, both being driven by the same numbers.**

---

## 6. MINIMAL "BRING THE TODDLER TO V7" CHECKLIST

You don't have to do the entire v2 deluxe implementation right away. To get him "online" in V7:

### Phase 1: Basic Integration
- [ ] Port the v2 toddler system module into `src/ai/toddler/` (leave most logic intact)
- [ ] In `MallSimulation.update()`:
  - [ ] Call `toddler.update(...)` each tick
  - [ ] Fold its `heat_multiplier` into Cloud pressure
  - [ ] Fold `glitch_multiplier` / `reality_strain` into renderer strain / glitch variables
- [ ] Add toddler info to the global `sim_data/game_state`:
  - [ ] Position, visible, distance, reality_strain

### Phase 2: Visual Manifestation
- [ ] Make your Wolf3D/voxel prototype render something from `toddler.visible`:
  - Even if it's just: `if visible: draw little silhouette sprite at toddler_pos`
- [ ] Add basic distortion effects:
  - [ ] Screen vignette when `in_distortion_field`
  - [ ] Color shift when `reality_strain > 0.5`

### Phase 3: Leon Awareness
- [ ] Add toddler context to Leon's prompt
  - [ ] Step 1: "Mention weird feelings when reality_strain > 0.5"
  - [ ] Step 2: Graduated awareness based on visibility
  - [ ] Step 3: Zone-specific descriptions ("something's wrong in the food court")

### Phase 4: Advanced Effects (After Phase 1-3 working)
- [ ] Audio: drone, whispers, heartbeat based on distance
- [ ] Distortion shaders: chromatic aberration, reality tears
- [ ] Story beats: footprints, NPC reactions, zone failures
- [ ] Behavioral modes: wandering, stalking, fleeing, manifesting

---

## 7. TODDLER BEHAVIORAL MODES (FROM V2)

The toddler has different behavioral states that affect its movement and visibility:

### WANDERING
- Drifts through zones randomly
- Low visibility (0.0-0.2)
- Minimal reality strain
- Purpose: Background dread

### CURIOUS
- Follows player at distance
- Medium visibility (0.3-0.5)
- Moderate reality strain
- Triggered by: Player staying in one zone too long

### MANIFESTING
- Approaches player
- High visibility (0.6-0.9)
- High reality strain
- Triggered by: High Cloud level, player in "significant" zones

### FLEEING
- Moves away from player
- Drops visibility rapidly
- Low reality strain
- Triggered by: Player turning to look directly, sudden loud sounds

### STATIC
- Stays in one location
- Variable visibility
- Creates "haunted zone"
- Triggered by: Zone failures, NPC contradictions

---

## 8. TODDLER CONFIGURATION

```python
# toddler_config.py

TODDLER_CONFIG = {
    "movement": {
        "base_speed": 3.0,              # feet per second
        "curious_speed": 5.0,           # when following player
        "fleeing_speed": 8.0,           # when running away
        "teleport_distance": 200.0,     # instant relocation if too far
    },

    "visibility": {
        "base_rate": 0.01,              # visibility gain per second
        "cloud_amplifier": 0.02,        # extra gain per Cloud point
        "decay_rate": 0.05,             # visibility loss when not triggered
        "max_visibility": 1.0,
    },

    "distortion": {
        "base_radius": 15.0,            # feet
        "max_radius": 40.0,             # at full visibility
        "reality_strain_threshold": 0.5,  # when effects kick in
    },

    "behavior_triggers": {
        "curious_distance": 50.0,       # switch to curious if player within
        "manifesting_cloud": 70.0,      # switch to manifesting at Cloud 70+
        "fleeing_direct_look": True,    # flee if player looks directly
        "static_on_contradiction": True,  # become static when NPC contradicts
    }
}
```

---

## 9. EXAMPLE: TODDLER AT CLOUD 75 IN FOOD COURT

### Context
- **Cloud:** 75.3 (strained)
- **Zone:** Z4_FOOD_COURT (sunken bowl, 8' below ground)
- **Toddler:** Following player (CURIOUS mode)
  - Distance: 23 feet
  - Visibility: 0.6 (semi-manifested)
  - Reality strain: 0.75

### Effects Generated

```python
toddler_effects = {
    "heat_multiplier": 1.8,           # Cloud pressure x1.8
    "glitch_multiplier": 2.2,         # Visual glitches x2.2
    "in_distortion_field": True,      # Player is within 15-40ft radius
    "distortion_intensity": 0.75,
    "distance_to_player": 23.0,
    "toddler_visible": 0.6,
    "reality_strain": 0.75,
    "toddler_position": (100, 0, -8),  # In food court bowl
    "behavior": "CURIOUS"
}
```

### System Responses

**Cloud:**
```python
base_delta = 0.8  # Normal Cloud gain this tick
amplified_delta = 0.8 * 1.8 = 1.44
# Cloud jumps 75.3 → 76.74 (accelerated by toddler presence)
```

**Renderer:**
```python
glitch_intensity = (2.2 - 1.0) / 3.0 = 0.4  # 40% glitch
reality_strain = 0.75
# Screen: vignette, color shift, chromatic aberration
```

**QBIT:**
```python
zone_FC_ARCADE.event_weight_modifiers["toddler_presence"] = 1.75
zone_FC_ARCADE.tags.add("TODDLER_PRESENT")
# Food court zone now 1.75x more likely for events
```

**Leon (sees in game_state):**
```
toddler.visible = 0.6 (above 0.5 threshold)
toddler.distance = 23 feet
toddler.current_zone = "Z4_FOOD_COURT"

Leon's utterance:
"Something's moving near the neon sign. Don't turn around.
The geometry down here is wrong - this pit is 8 feet but it feels deeper.
Can you hear that hum? It's not the ventilation."
```

**Visual (Wolf3D render):**
```
if toddler.visible > 0.5:
    draw_sprite(
        position=toddler.position,
        sprite=TODDLER_SILHOUETTE,
        alpha=toddler.visible * 0.8,  # Semi-transparent
        distortion=reality_strain
    )
```

---

## 10. INTEGRATION WITH EXISTING V7 SYSTEMS

### With Cloud System
- Toddler `heat_multiplier` amplifies all Cloud pressure sources
- High Cloud → toddler becomes more visible (positive feedback loop)
- Toddler can trigger Cloud spikes when manifesting

### With QBIT Engine
- Toddler agitates zone QBIT aggregates
- Makes zones more likely to fail, spawn events, generate contradictions
- Creates "haunted zone" effect

### With NPC State Machines
- NPCs can detect toddler presence (if visible > 0.7)
- Janitor: "There's something in the service corridor. I can feel it in the pipes."
- NPCs may refuse to enter zones marked "TODDLER_PRESENT"

### With Leon (Leisurely Leon)
- Leon senses toddler through `reality_strain` and `distortion_field`
- Graduated awareness based on visibility
- Can warn player, describe sensations, suggest evasion

### With Zone System
- Toddler affects zone adjacency weights (zones "pull" toward it)
- Can trigger zone-specific events
- Creates local reality instability

---

## 11. TECHNICAL REQUIREMENTS

### Dependencies
- Existing Cloud system
- Existing QBIT engine
- Existing zone system
- Player position tracking
- Renderer state object

### Performance
- Toddler update: ~0.5ms per tick
- Distance calculations: Simple Euclidean
- Zone lookups: Hash map O(1)

### State Management
```python
toddler_state = {
    "position": (x, y, z),
    "behavior": "CURIOUS",
    "visibility": 0.6,
    "reality_strain": 0.75,
    "distortion_radius": 28.0,
    "target_zone": "Z4_FOOD_COURT",
    "last_player_seen": timestamp
}
```

---

## 12. WHAT THIS ENABLES

**Mobile reality catalyst that:**
- Amplifies Cloud pressure wherever it goes
- Makes zones go weird through QBIT agitation
- Creates graduated horror (invisible → semi-visible → manifested)
- Gives Leon something to sense and warn about
- Adds spatial dread (it's in a specific place, moving)
- Integrates with all existing V7 systems

**You get:**
- The v2 toddler's self-contained horror engine
- Wired into Cloud, QBIT, zones, and Leon
- Not a separate "heat bar" - it's part of the world
- A shared object of dread for player and Leon

---

## NEXT STEPS

1. Port `toddler_system.py` from v2 to `src/ai/toddler/`
2. Add toddler update hook in `MallSimulation.update()`
3. Wire `heat_multiplier` → Cloud pressure
4. Wire `glitch_multiplier` → renderer strain
5. Add toddler to `game_state` export
6. Test: Watch Cloud accelerate when toddler is near player

**The toddler returns. The mall remembers.**

---

*Design Document v1.0*
*V7 Integration - Toddler as Reality Catalyst*
*"It's not hostile. It's a catalyst. Its presence accelerates decay."*
