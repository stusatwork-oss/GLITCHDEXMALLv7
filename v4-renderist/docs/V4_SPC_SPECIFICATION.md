# V4 RENDERIST MALL OS - SPC SPECIFICATION

**Version**: 4.0
**Status**: Canonical Reference
**Last Updated**: Session Lock

---

## 1. CORE PHILOSOPHY

> "Canon emerges from resonance and repetition, not ego."

### Design Pillars

1. **Cloud-Driven World**: No static tile maps. Semantic zones with Cloud-influenced adjacency.
2. **12 Anchor NPCs**: The only persistent identities. All Customers are ambient noise.
3. **Diegetic Feedback Only**: No UI meters. Swarm, lighting, and NPC behavior ARE the feedback.
4. **Soft Memory**: Mall remembers vibes across sessions, not details.
5. **Aesthetic Before Physics**: Visual/behavioral changes first. Spatial mutation only at high Cloud.

---

## 2. CONSTRAINTS (HARD RULES)

### What V4 Does NOT Have

| Constraint | Reason |
|------------|--------|
| No visible Cloud meter | Pure diegetic feedback |
| No tile mutation in V4 | Aesthetic-only for this version |
| No permanent corruption | Soft memory prevents death spiral |
| No magic | State machine only, no supernatural causation |
| No NPC anchor degradation | Silhouettes stay clear during Bleed |
| No player character customization | Player is observer/perturbation |
| No combat system | Not an action game |
| No explicit quest log | Discovery through resonance |

### What V4 MUST Have

| Requirement | Implementation |
|-------------|----------------|
| Cloud pressure 0-100 | `cloud.py` - implemented |
| 4 mood bands | calm/uneasy/strained/critical |
| 13 Anchor NPCs | `anchor_npcs.py` - implemented |
| Zone microstates | turbulence, resonance, swarm_bias |
| Bleed tiers 1-3 | 75/80/90 thresholds |
| Contradiction system | NPCs break "never" rules at high Cloud |
| Session persistence | Canon Layer saved, ephemeral Cloud resets |

---

## 3. SYSTEMS ARCHITECTURE

### System Dependency Graph

```
┌─────────────────────────────────────────────────────┐
│                    MAIN LOOP                        │
│                   (main.py)                         │
└─────────────────────┬───────────────────────────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │  CLOUD   │ │  ANCHOR  │ │  SWARM   │
    │  STATE   │ │   NPCs   │ │GENERATOR │
    │(cloud.py)│ │(anchor_  │ │(swarm.py)│
    │          │ │ npcs.py) │ │          │
    └────┬─────┘ └────┬─────┘ └────┬─────┘
         │            │            │
         └────────────┼────────────┘
                      ▼
              ┌──────────────┐
              │   RENDERER   │
              │  (diegetic   │
              │   output)    │
              └──────────────┘
```

### System Files

| File | Status | Purpose |
|------|--------|---------|
| `main.py` | Scaffolding | Entry point, main loop |
| `cloud.py` | **Implemented** | Global state, zone microstates |
| `anchor_npcs.py` | **Implemented** | 13 persistent NPCs |
| `swarm.py` | Not started | Customer crowd generator |
| `bleed_events.py` | Not started | Timed visual/audio effects |
| `ao3_logs.py` | Not started | Canon discovery system |
| `adjacency.py` | Not started | Semantic zone relationships |

---

## 4. CLOUD STATE SYSTEM

### Global Variables

```python
class CloudState:
    cloud_level: float        # 0.0 - 100.0
    pressure_trend: str       # "stable", "rising", "falling", "spiking"
    mall_mood: str            # "calm", "uneasy", "strained", "critical"
    bleed_threshold_reached: bool
    current_bleed_tier: int   # 0, 1, 2, or 3
```

### Mood Thresholds

| Level | Mood | Effects |
|-------|------|---------|
| 0-24 | **calm** | Normal mall weirdness, mostly cosmetic |
| 25-49 | **uneasy** | Player can feel something "off" |
| 50-74 | **strained** | NPC oddness, space tension, pre-bleed |
| 75-100 | **critical** | Bleed possible, contradictions appear |

### Bleed Tiers

| Tier | Threshold | Effects |
|------|-----------|---------|
| 1 | 75 | Visual/Audio only: flicker, detune, swarm stutter |
| 2 | 80 | + NPC contradictions, dialogue substitution |
| 3 | 90 | + Space effects: hall length fluctuation, mild drift |

### Driver Weights

```python
WEIGHT_PLAYER = 0.50    # Primary driver
WEIGHT_NPC = 0.25       # Adds texture
WEIGHT_DRIFT = 0.15     # Background noise
WEIGHT_OTHER = 0.10     # Resonance, session fatigue
```

### Zone Drift Rates

| Zone | Rate | Behavior |
|------|------|----------|
| FOOD_COURT | 1.5x | Always drifts faster |
| SERVICE_HALL | 1.3x | Goes weird first |
| STORE_HARD_COPY | 1.2x | Slight instability |
| ANCHOR_STORE | 1.0x | Baseline |
| CORRIDOR | 0.9x | Slightly stable |
| STORE_BORED | 0.7x | Unusually stable |

---

## 5. ZONE SYSTEM

### Zone Types

| Zone ID | Name | Purpose | Anchor NPCs |
|---------|------|---------|-------------|
| `FOOD_COURT` | Food Court | Social hub, high drift | Barista |
| `SERVICE_HALL` | Service Hallways | Hidden routes, high drift | Security, Lost&Found, Janitor |
| `STORE_HARD_COPY` | Hard Copy | Arcade/bookstore | Bookwoman, Arcade Guy |
| `STORE_BORED` | BORED Skateshop | Stable zone | BORED |
| `STORE_COMPHUT` | CompHut | Tech repairs | Fixer |
| `STORE_MILO_OPTICS` | Milo's Optics | Artifact lore | Milo |
| `STORE_FLAIR` | Flair Warrior | Greeting cards | Flair Warrior |
| `STORE_SPORTY` | Sporty's | Sports gear | Sporty's Manager |
| `CLINIC` | Medical Clinic | Empty clinic | Nurse |
| `ANCHOR_STORE` | Anchor Store | Forbidden back area | None |
| `ENTRANCE` | Main Entrance | Spawn point | None |
| `CORRIDOR` | Corridors | Transition spaces | None |

### Zone Microstate

```python
class ZoneMicrostate:
    zone_id: str
    turbulence: float         # 0-10, local instability
    resonance: float          # 0-100, echo accumulation
    swarm_bias: dict          # Customer generator weights
    last_player_visit: float  # Timestamp
    discovery_count: int      # AO3 logs found here
```

### Adjacency (Semantic, Not Geometric)

Zones connect based on **relationship logic**, not physical layout:
- BORED knows the service door behind CompHut
- Food Court ramp leads to "somewhere below"
- Service Hall connects to forbidden Anchor Store back

**Probabilistic**: Same input may produce different adjacency outcomes.

---

## 6. NPC SYSTEM

### The 13 Anchors

| ID | Name | Zone | Contradiction Threshold |
|----|------|------|------------------------|
| bookwoman | The Bookwoman | STORE_HARD_COPY | 80 |
| fixer | The Fixer | STORE_COMPHUT | 85 |
| bored | BORED | STORE_BORED | 75 |
| flair | Flair Warrior | STORE_FLAIR | 85 |
| barista | Mermaid Barista | FOOD_COURT | 80 |
| security | Mall Cop | SERVICE_HALL | 75 |
| nurse | Clinic Nurse | CLINIC | 85 |
| sporty | Sporty's Manager | STORE_SPORTY | 80 |
| arcade | Arcade Guy | STORE_HARD_COPY | 85 |
| lostandfound | Lost & Found Clerk | SERVICE_HALL | 80 |
| janitor | Mall Janitor | SERVICE_HALL | 85 |
| toddler | The Toddler | UNKNOWN | 90 |
| milo | Milo | STORE_MILO_OPTICS | 80 |

### NPC State Machine

```
NORMAL → STRESSED → AVOIDING → CONTRADICTED
  ↑                              │
  └──────────────────────────────┘
         (session reset)
```

### Visual Anchor Rule

**Uniform + 1 Iconic Detail**

- Renderer-agnostic (works in text, pixel, video)
- Must be identifiable in 3-5 words
- Anchors do NOT degrade during Bleed
- The WORLD degrades, not the NPCs

### Behavior Grid

NPCs read `Cloud.mood` × `zone.turbulence` to select behavior:

| Cloud \ Turb | Low (0-3) | Med (3-7) | High (7-10) |
|--------------|-----------|-----------|-------------|
| **calm** | Normal route | Minor flavor changes | Déjà vu mentions |
| **uneasy** | Shorter lines, watchful | Stress variants 20-30% | Pauses, glances |
| **strained** | Skip routines | Stress variants 50-70% | Mis-speak, backtrack |
| **critical** | Tired/flat | Avoid zones silently | **Contradiction possible** |

### Never Lists (Examples)

| NPC | Never Rules |
|-----|-------------|
| Bookwoman | Never sells a book, never mis-shelves |
| BORED | Never shows enthusiasm, never admits he knows secrets |
| Security | Never leaves post, never admits fear |
| Nurse | Never sits down, never admits clinic is empty |

### Contradiction Triggers

When `Cloud.level >= npc.contradiction_trigger` AND `npc.contradiction_used == False`:
- NPC breaks ONE "never" rule
- Flag is set (once per session)
- This is the "oh shit" character moment

---

## 7. SWARM SYSTEM (Customers)

### Purpose

Customers are ambient noise - non-canon humans that serve as the **visual barometer** of Cloud state.

### Swarm Parameters

```python
class SwarmState:
    palette_bias: float       # % drab vs bright (0-1)
    speed_factor: float       # Movement multiplier
    cluster_factor: float     # How clumpy
    avoidance: float          # Tendency to avoid player
    stare_events: float       # Chance of synchronized look
```

### Swarm by Cloud Mood

| Mood | Palette | Speed | Cluster | Special Behaviors |
|------|---------|-------|---------|-------------------|
| calm | 50% neutral | 1.0 | low-med | Random strolls, scattered stops |
| uneasy | 70% neutral/beige | 0.9 | medium | Groups near exits, hovering |
| strained | 80% neutral/dark | 1.1 | med-high | Flow away from zones, pauses |
| critical | 90% desaturated | 1.2→drops | high | **Freeze → stare → scatter** |

### Swarm Feedback Rules

- No individual customer has identity
- High turbulence = more "echo people" (same model repeats)
- Swarm tells the story the UI cannot show

---

## 8. BLEED EVENT SYSTEM

### Event Structure

```python
class BleedEvent:
    id: str
    zone_id: str | None       # Affected zone (or global)
    start_time: float
    duration: float           # Seconds
    intensity: float          # 0.0 - 1.0
    type: str                 # "visual", "audio", "npc", "spatial"
```

### Trigger Conditions

1. `Cloud.level >= 75`
2. `Cloud.bleed_cooldown <= 0`
3. Qualifying stimulus:
   - High zone resonance
   - Rare artifact interaction
   - Repeated AO3 echo
   - Prolonged presence in hot zone

### Duration by Tier

| Tier | Duration | Effects |
|------|----------|---------|
| 1 | 5-10 sec | Lights flicker, PA wrong jingle, swarm stutters |
| 2 | 10-20 sec | NPC contradictions, dialogue substitution |
| 3 | 20-40 sec | Hall length shift, signage mismatch, forced cooldown |

### Visual Degradation Rules

**NPC anchors NEVER degrade.**

World degrades with:
- Temporal jitter (frame pops, repeat frames)
- Color banding / desaturation pulses
- Geometry "breathe" (tiny FOV oscillations)
- SORA-style double exposures
- VHS drag, JPEG artifacts

---

## 9. ARTIFACT SYSTEM

### Artifact Weight

Artifacts gain "canon weight" through discovery:

```python
def get_artifact_weight(artifact_id: str) -> float:
    discoveries = count_discoveries(artifact_id)
    return min(1.0, discoveries / 3)  # Cap at 3 discoveries
```

### Echo System

When artifact is discovered:
1. Record in `discovery_history`
2. Increase zone `resonance`
3. If weight > threshold, NPCs start mentioning it
4. Repeated discoveries = higher adjacency probability for that zone

### Artifact Categories

| Category | Cloud Delta | Example |
|----------|-------------|---------|
| Common | +0.5 | Old receipt, lost key |
| Uncommon | +1.0 | Worn photo, sticker sheet |
| Rare | +1.5 | Necronomicon, cursed item |
| Unique | +2.0 | AO3 log, toddler trace |

---

## 10. AO3 LOG SYSTEM

### Purpose

AO3 logs are discovered "evidence" that feed the Canon Layer:
- Not real-time Cloud pressure
- Slowly shift baseline the mall starts from in future sessions
- "Climate, not weather"

### Log Structure

```python
class AO3Log:
    id: str
    zone_id: str              # Where found
    content: str              # The text/evidence
    canon_weight: float       # Contribution to baseline
    artifact_refs: list[str]  # Related artifacts
    npc_refs: list[str]       # Related NPCs
```

### Canon Layer Persistence

Saved between sessions:
- Total AO3 logs discovered
- Zone baseline resonance adjustments
- Artifact weights
- NPC variant unlocks

---

## 11. PLAYER INTERACTION WEIGHTS

### Positive (Raises Cloud)

| Action | Δ Cloud | Zone Effect |
|--------|---------|-------------|
| Enter low-traffic back corridor | +0.5 | +turbulence |
| Circle same zone repeatedly | +0.2/loop | +resonance |
| Interact with rare artifact | +1.5 | +resonance, +turbulence |
| Read AO3 log | +1.0 | +resonance |
| Witness NPC contradiction | +2.0 | turbulence spike |
| Stay in Bleed zone | +0.3/sec | escalates tier |

### Negative (Lowers Cloud)

| Action | Δ Cloud | Zone Effect |
|--------|---------|-------------|
| Time in bright, populated zones | -0.1/sec | -turbulence |
| Sit at benign anchor (Hard Copy) | -0.3/sec | -resonance |
| Talk to "grounding" NPCs | -1.0 | calm wave |
| Leave high-turbulence quickly | -0.5 | prevents spike |

### Ambient

| Source | Effect |
|--------|--------|
| Time-of-day sine wave | ±2.0 |
| Long session fatigue | +0.01/sec after 30min |
| Random noise | ±0.1 jitter |

---

## 12. UPDATE LOOP

### Main Loop (60fps target)

```python
def main_loop():
    while running:
        dt = get_delta_time()

        # 1. Get player input
        player_action = input_system.get_action()

        # 2. Update Cloud state
        render_hints = cloud.update(dt, player_action, npc_events)

        # 3. Update NPC states
        npc_updates = anchor_system.update(
            render_hints,
            cloud.zones
        )

        # 4. Update Swarm
        swarm_state = swarm.update(render_hints)

        # 5. Check for Bleed trigger
        if should_trigger_bleed(cloud):
            bleed_event = cloud.trigger_bleed_event()

        # 6. Render (diegetic output)
        renderer.render(
            player_position,
            render_hints,
            npc_updates,
            swarm_state
        )

        # 7. Collect NPC events for next tick
        npc_events = collect_npc_events(npc_updates)
```

### Cloud Update Tick

```python
def update_cloud(dt, player_action, npc_events):
    # Calculate weighted deltas
    delta = (
        0.50 * calc_player_delta(player_action) +
        0.25 * calc_npc_delta(npc_events) +
        0.15 * calc_drift_delta(dt) +
        0.10 * calc_other_delta(dt)
    )

    # Apply and clamp
    cloud_level = clamp(cloud_level + delta, 0, 100)

    # Update mood
    mood = mood_from_level(cloud_level)

    # Update zones
    update_zone_microstates(dt, player_action)

    # Check bleed thresholds
    update_bleed_tier()

    return generate_render_hints()
```

---

## 13. PERSISTENCE MODEL

### What Saves (Canon Layer)

```python
canon_state = {
    "cloud_level": float,           # Current level
    "total_playtime": float,        # Accumulated
    "session_count": int,
    "bleed_events_triggered": int,
    "discovery_history": list,      # Last 100
    "npc_contradiction_log": list,  # Last 50
    "zones": dict                   # Only if cloud >= 50
}
```

### What Resets (Ephemeral)

- Exact turbulence values
- Swarm positions
- NPC exact positions
- Active Bleed events

### Philosophy

> "The mall remembers vibes, not details."

---

## 14. RENDER HINTS (OUTPUT)

The Cloud generates render hints for the diegetic feedback systems:

```python
render_hints = {
    # Global
    "cloud_level": float,
    "mood": str,
    "trend": str,
    "bleed_tier": int,

    # Swarm
    "swarm": {
        "color_uniformity": float,
        "cluster_tendency": float,
        "speed_multiplier": float,
        "freeze_chance": float,
        "scatter_threshold": bool,
        "stare_intensity": float
    },

    # Environment
    "environment": {
        "flicker_intensity": float,
        "color_temperature": float,
        "ambient_detune": float,
        "vhs_drag": float,
        "jpeg_artifacts": float
    },

    # Physics (high cloud only)
    "physics": {
        "tile_drift": bool,
        "length_fluctuation": float,
        "gravity_variance": float
    },

    # NPC modifiers
    "npc_modifiers": {
        "dialogue_tension": float,
        "spine_pressure": float,
        "contradiction_ready": bool
    },

    # Zone states
    "zones": dict
}
```

---

## 15. FIRST THREE ZONES (Implementation Priority)

Per alignment:

1. **STORE_HARD_COPY** (arcade/bookstore)
2. **STORE_BORED** (skateshop)
3. **FOOD_COURT** (social hub)

These three establish:
- High/low drift contrast (Food Court vs BORED)
- Two Anchor NPCs with existing lore (BORED, Bookwoman)
- Central hub for Swarm behavior

---

## 16. IMPLEMENTATION STATUS

### Completed

- [x] Cloud State system (`cloud.py`)
- [x] Anchor NPC system (`anchor_npcs.py`)
- [x] Launcher integration (program #390)
- [x] Main entry scaffolding (`main.py`)

### Next Priority

- [ ] Wire Cloud + NPCs into main.py demo
- [ ] Swarm generator (`swarm.py`)
- [ ] Bleed event system (`bleed_events.py`)
- [ ] Zone adjacency logic (`adjacency.py`)
- [ ] AO3 log system (`ao3_logs.py`)
- [ ] Renderer integration

---

## 17. SORA INTEGRATION NOTES

Bleed Events use SORA clips as cutscenes/mood setters:
- Short clips (under 2 min for warp bleeds)
- Game logic takes over after clip sets tone
- Clips are pre-rendered, stored in `assets/sora_clips/`
- Clip selection based on Cloud mood and zone

---

## 18. TESTING CHECKLIST

### Cloud System

- [ ] Mood transitions at correct thresholds
- [ ] Driver weights sum correctly
- [ ] Bleed tiers trigger properly
- [ ] Persistence saves/loads

### NPC System

- [ ] All 13 NPCs initialize
- [ ] State machine transitions work
- [ ] Contradictions fire once per session
- [ ] Dialogue pools select correctly

### Integration

- [ ] Cloud hints reach NPCs
- [ ] Zone turbulence affects NPC stress
- [ ] Swarm responds to mood changes
- [ ] Bleed events modify all systems

---

**END OF SPC SPECIFICATION**

This document is the canonical reference for V4 Renderist Mall OS development.
All implementation must conform to these constraints and systems.
