# RENDERIST MALL OS - V4

## The Cloud-Driven World

V4 represents a fundamental shift from tile-based worlds to **Cloud-driven semantic spaces**.

### Core Philosophy

- The Mall is a Cloud-driven world, not a static map
- Canon emerges from resonance and repetition, not ego
- The 12 Anchor NPCs are the only persistent identities
- All Customers are ambient noise (non-canon humans)
- Sora-style clips are BLEED EVENTS that temporarily alter the world's tone

### Version Progression

| Version | Architecture | World Model |
|---------|-------------|-------------|
| V1 | Wolf3D Raycaster | Static tile map |
| V2 | AAA Immersive Sim | Static tiles + AI systems |
| V3 | Pygame Raycaster + Full AI | Static tiles + full simulation |
| **V4** | **Renderist OS** | **Cloud-driven semantic spaces** |

### Key Systems

1. **The Cloud (Global State)** - Abstract world data driving all behavior
2. **13 Anchor NPCs** - Persistent entities with Line-12 spines
3. **Swarm System** - Ambient crowd with population curves
4. **Bleed Events** - Sora clip integrations that warp reality
5. **AO3 Logs** - Canon emergence through player discovery
6. **Adjacency System** - Semantic, not geometric, relationships

---

## Running V4

### Standard Launch
```bash
cd v4-renderist
python3 src/main.py
```

### Demo Mode (Phase 1)
The `mall_demo()` function runs the integration demo exercising Cloud + Anchors + Swarm:

```bash
cd v4-renderist
python3 -c "from src.main import mall_demo; mall_demo()"
```

Or with custom duration:
```python
from src.main import MallDemo
demo = MallDemo()
demo.run(duration=30.0)  # 30 second demo
```

### Via Shareware Launcher
**Program #390** in the shareware launcher

---

## Phase 1 Status: COMPLETE

**V4.0.1-alpha** - Integration Demo

### Implemented Systems

- **Cloud State** (`cloud.py`) - Global pressure 0-100, 4 moods, 3 bleed tiers
- **Anchor NPCs** (`anchor_npcs.py`) - 13 persistent entities with spines/contradictions
- **Swarm System** (`swarm.py`) - Population curves, confirming-only feedback
- **60fps Loop** - Cloud tick every 10 frames with interpolation
- **Contradiction Cascade** - Zone cooldown logic (30 seconds)

### LOCKED Constants

```python
CLOUD_UPDATE_INTERVAL = 10           # frames
ZONE_CONTRADICTION_COOLDOWN = 30.0   # seconds
MAX_SWARM_CONTRIBUTION = 0.05        # 5% cap
BLEED_WINDDOWN_TIME = 7.5            # seconds
```

### Interpolation Logic

NPCs and Swarm read interpolated Cloud values between ticks for smooth behavior:

```python
# Cloud ticks every 10 frames
# Between ticks, systems read interpolated values:

frames_since_tick = frame_count % CLOUD_UPDATE_INTERVAL
t = frames_since_tick / CLOUD_UPDATE_INTERVAL
interpolated_level = lerp(previous_cloud, current_cloud, t)
```

This ensures:
- Cloud updates are batched (6 times/sec at 60fps)
- NPC/Swarm behavior remains smooth
- No jarring state transitions

---

## Sample Output

### Demo Console Output
```
[TICK   300] Cloud: 4.2 (calm) | Swarm: 52 | Contradictions: 0
  Zones: CORRIDOR:15, ENTRANCE:13, FOOD_COURT:11

[TICK   360] Cloud: 6.8 (calm) | Swarm: 48 | Contradictions: 0
  NPCs: Mall Cop:stressed, Barista:avoiding
  Zones: CORRIDOR:14, FOOD_COURT:12, ENTRANCE:10
```

### AO3 Contradiction Log
```json
{
  "timestamp": 8.2,
  "npc_id": "security",
  "npc_name": "Mall Cop",
  "zone": "SERVICE_HALL",
  "action": "Abandons his post"
}
```

When Cloud reaches critical (75+) and NPCs hit their contradiction thresholds, they break their "never" rules:

- **Mall Cop** (75): Abandons post
- **BORED** (75): Warns player about something specific
- **Barista** (80): Forgets what drink they're making
- **Bookwoman** (80): Recommends a book she hasn't read
- **Toddler** (90): Speaks a single word

---

## Directory Structure

```
v4-renderist/
├── src/
│   ├── main.py              # Entry point + mall_demo()
│   ├── cloud.py             # Cloud state management
│   ├── anchor_npcs.py       # 13 persistent NPCs
│   ├── swarm.py             # Ambient crowd system
│   ├── bleed_events.py      # Sora clip integration (TBD)
│   ├── ao3_logs.py          # Log generation (TBD)
│   └── adjacency.py         # Semantic zones (TBD)
│
├── data/
│   └── cloud_state.json     # Persisted cloud state
│
├── docs/
│   ├── V4_SPC_SPECIFICATION.md   # Complete system spec
│   ├── DECISIONS_LOCKED.md       # Canonical decisions
│   └── schemas/
│       └── world_spine.json      # Entity graph schema
│
└── README.md
```

---

## Requirements

- Python 3.8+
- No external dependencies for Phase 1

---

## Phase 2 Roadmap

- [ ] Bleed Events system (`bleed_events.py`)
- [ ] AO3 Log generation (`ao3_logs.py`)
- [ ] Probabilistic adjacency (`adjacency.py`)
- [ ] SORA clip integration
- [ ] Persistence across sessions

---

## Known Issues

See `docs/KNOWN_ISSUES.md` for current limitations.

---

## Documentation

- **SPC Specification**: `docs/V4_SPC_SPECIFICATION.md`
- **Locked Decisions**: `docs/DECISIONS_LOCKED.md`
- **World Spine Schema**: `docs/schemas/world_spine.json`
