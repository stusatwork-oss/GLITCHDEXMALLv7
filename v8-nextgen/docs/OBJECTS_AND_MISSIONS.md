# OBJECTS & MISSIONS - V7 Interaction Layer 🗑️🥤💨

**The mall has things you can touch. And they touch back.**

This layer adds concrete player agency to the V7 horror stack:
- **Recycler Trash Cans** - Cloud relief nodes (anti-Toddler)
- **Slushee Consumables** - Personal comfort buffs
- **HOLOmister Units** - Environmental FX that react to Cloud/Toddler
- **Tutorial Missions** - Teach the systems through interactive scenarios

---

## The Three Object Categories

### 1. Cloud Relief Nodes - Recycler Trash Cans 🗑️

**The anti-Toddler.** If Toddler amplifies Cloud pressure, Recycler reduces it.

**Mechanics:**
- Player-activated interaction
- Consumes discarded item → converts to Cloud pressure relief
- Cooldown per can

**Data:** Definitions live alongside sim prototypes. Use `RecyclerTrashCan` and `use_recycler` (imported via `objects.__init__`).

### 2. Consumables - Slushees 🥤

**Personal coolant.** Increases heat tolerance, offers small local Cloud relief, and grants Toddler-vision resistance.

**Data:** `data/objects/slushee_blue_raspberry.json`
- Vendor zones: Food Court + Z2 Food Court
- Cost: 3.99 credits, effectively infinite stock for tests
- Effects: +5 heat tolerance, -5 player heat, -1 local Cloud, toddler-vision resistance boost
- Duration: 60s, cooldown 10s, non-stacking except duration refresh

**Code:** `src/objects/slushee.py`
- `SlusheeItem(item_id)` loads JSON definition
- `drink_slushee(sim_state, player_state, slushee, current_time)` applies effects
- Applies numeric deltas to dict-backed or attribute-based players, attaches status flags, returns `SlusheeConsumptionResult`

**Usage snippet:**
```python
player = {"heat": 10, "heat_tolerance": 0, "toddler_vision_resistance": 0.0}
sim_state = {"cloud": {"level": 72}}
slushee = SlusheeItem("slushee_blue_raspberry")
result = drink_slushee(sim_state, player, slushee, current_time=120.0)

# Store the result for buff tracking so you can revert later
player_active_effects.append(result)
```

**Buff expiry / reversion:**

Slushee modifiers (heat_tolerance, toddler_vision_resistance, status flags) are temporary. When your buff system detects `result.expires_at` has passed, call `expire_slushee_effect` to unwind the temporary boosts while leaving the instantaneous Cloud/heat relief intact.

```python
if current_time >= result.expires_at:
    expire_slushee_effect(player, slushee, result, current_time=current_time)
```

`sim_state` is expected to expose `cloud.level` either as a dict (`{"cloud": {"level": 72}}`) or an object with a `.level` field; otherwise a descriptive error is raised to catch contract drift early.

### 3. Environmental FX Nodes - HOLOmister 💨

**Mist + holograms.** Provides comfort in the 40-85 Cloud band, and glitches with Toddler strain or critical Cloud.

**Data:** `data/objects/holomister_unit.json`
- Zone affinity: Atrium/Food Court zones
- Activation: Cloud 40-85 with 5s activation delay, 3s deactivation delay
- Glitch triggers: Cloud >= 90 or toddler reality strain >= 0.6
- Effects: Mist rate, cloud relief, comfort/heat relief, hologram and glitch message pools

**Code:** `src/objects/holomister.py`
- `HoloMister(zone_id, position)` loads definition and tracks internal state machine
- `update(current_time, cloud_level, toddler_in_zone=False, toddler_reality_strain=0.0)` returns state + events
- Emits `HOLOMISTER_GLITCH`, `HOLOMISTER_ACTIVATED`, `HOLOMISTER_COOLING`, `HOLOMISTER_RECOVERING`, `HOLOMISTER_INACTIVE`
- `as_dict()` exposes telemetry for UI/mission scripting

---

## Tutorial & Investigation Missions

Two missions showcase the new objects.

### `keep_it_cool` (Tutorial)
- Objectives: hear Leon explain Cloud, use Recycler, buy & drink Slushee
- Fail if Cloud hits 95 or timer exceeds 7 minutes
- Rewards: XP, credits, overlays for Cloud monitoring

### `the_mist_is_wrong` (Investigation)
- Objectives: observe Atrium HOLOmister glitch, verify Cloud >= 70 during spray, scan and optionally override the unit
- Fail if Cloud hits 98 or timer exceeds 8 minutes
- Rewards: XP, credits, Slushee item, HOLOmister overlay unlock

Mission definitions live in `data/missions/*.json` and are kept simple so scripting layers can bind triggers to sim events.

---

## Integration Pointers

- Import via `from objects import SlusheeItem, HoloMister, drink_slushee, use_recycler`
- Data directories are relative to repo root (`data/objects`, `data/missions`)
- Systems that watch Cloud/Toddler events can generate cutscenes via the Sora engine (see `docs/CUTSCENE_ENGINE.md`).
- For analytics/cutscenes, use `HoloMister.flag("label")` to mark first-glitch events before handing to the cutscene engine.
