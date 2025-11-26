# V4 RENDERIST MALL OS - LOCKED DECISIONS

**Status**: CANONICAL - These decisions are final and must be implemented exactly as specified.

---

## 1. CLOUD UPDATE FREQUENCY

**Decision**: Cloud updates every **10 frames** (6 updates/sec at 60fps). NPC/Swarm read interpolated values.

**Implementation**:
```python
CLOUD_UPDATE_INTERVAL = 10  # frames

# In update loop:
if frame_count % CLOUD_UPDATE_INTERVAL == 0:
    cloud.update(dt * CLOUD_UPDATE_INTERVAL, player_action, npc_events)

# NPC/Swarm read:
interpolated_cloud = lerp(previous_cloud, current_cloud, frame_delta)
```

**Rationale**: Cloud is rhythm (dramatic beats). NPC/Swarm are smooth feel (interpolated).

---

## 2. CONTRADICTION CASCADE IN SERVICE_HALL

**Decision**: Cascades allowed with **20-30 second zone cooldown** between anchor contradictions.

**Implementation**:
```python
ZONE_CONTRADICTION_COOLDOWN = 30  # seconds

# In contradiction trigger:
if zone.last_contradiction_time + ZONE_CONTRADICTION_COOLDOWN < current_time:
    npc.trigger_contradiction()
    zone.last_contradiction_time = current_time
```

**Result**: Layered escalation (Security → L&F → Janitor), not a dogpile.

---

## 3. SWARM → CLOUD FEEDBACK

**Decision**: Swarm feedback is **confirming only**, capped at **±5%** of total Cloud delta.

**Rules**:
- Swarm can reinforce current Cloud direction
- Swarm can NEVER push Cloud across a tier threshold on its own
- Swarm cannot reverse Cloud direction by itself

**Implementation**:
```python
MAX_SWARM_CONTRIBUTION = 0.05  # 5%

swarm_delta = clamp(raw_swarm_delta, -MAX_SWARM_CONTRIBUTION, MAX_SWARM_CONTRIBUTION)
```

**Rationale**: Crowd is weather, not governance. Cloud stays sovereign.

---

## 4. BLEED EVENT INTERRUPTION

**Decision**: **Option C** - Bleed winds down over 5-10 second decay, never instant.

**Implementation**:
```python
BLEED_WINDDOWN_TIME = 7.5  # seconds (midpoint)

# When Cloud drops below tier threshold:
if cloud_level < bleed.tier_threshold:
    bleed.state = "WINDDOWN"
    bleed.remaining_time = BLEED_WINDDOWN_TIME
```

**Rationale**: Storm fades. Drama maintained. Player agency respected.

---

## 5. PROBABILISTIC ADJACENCY

**Decision**:
- **Player navigation**: DETERMINISTIC
- **NPC/Swarm pathfinding**: PROBABILISTIC

**Rules**:
- Player can never get lost or softlocked
- NPCs can experience shifting topology
- Mall may rearrange BEHIND the player, never in front

**Implementation**:
```python
def get_player_adjacency(zone_id):
    return DETERMINISTIC_GRAPH[zone_id]

def get_npc_adjacency(zone_id, cloud_mood):
    return weighted_random(PROBABILISTIC_GRAPH[zone_id], cloud_mood)
```

**Rationale**: Player lost = frustration. NPCs lost = liminality.

---

## CONSTANTS SUMMARY

```python
# Cloud
CLOUD_UPDATE_INTERVAL = 10          # frames

# Contradictions
ZONE_CONTRADICTION_COOLDOWN = 30    # seconds

# Swarm
MAX_SWARM_CONTRIBUTION = 0.05       # 5% cap

# Bleed
BLEED_WINDDOWN_TIME = 7.5           # seconds

# These values are LOCKED and should not be changed without re-alignment.
```

---

## IMPLEMENTATION CHECKLIST

- [ ] Add CLOUD_UPDATE_INTERVAL to cloud.py
- [ ] Add interpolation support for NPC/Swarm reads
- [ ] Add zone.last_contradiction_time tracking
- [ ] Add zone cooldown check to contradiction triggers
- [ ] Cap swarm feedback in swarm.py (when built)
- [ ] Add WINDDOWN state to bleed_events.py (when built)
- [ ] Separate player/NPC adjacency graphs in adjacency.py (when built)

---

**These decisions are now canonical. All implementation must conform.**
