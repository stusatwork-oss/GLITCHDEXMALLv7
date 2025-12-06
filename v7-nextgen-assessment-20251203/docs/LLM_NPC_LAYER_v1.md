# LLM NPC LAYER v1 – Janitor / Cloud / Contradiction Integration

**Status:** Design Document
**Target:** V7 Integration + 3 Steps
**Goal:** Emergent NPC horror in a procedurally-stressed mall dungeon

---

## EXECUTIVE SUMMARY

The V7 simulation already has everything needed for LLM-assisted NPCs:
- QBIT power ratings (Janitor: 1478)
- Contradiction thresholds (breaks rules at Cloud 70+)
- Zone QBIT aggregates (FC-ARCADE: 6112 influence)
- Mood states (calm → uneasy → strained → critical)
- NPC state machines with behavioral rules
- Cloud pressure driving the system

**The LLM doesn't decide the physics. It just gives them a voice.**

We're bolting a "mouth" onto the existing brain.

---

## 1. WHAT YOU ALREADY HAVE (AS A BOX)

From V7 simulation spine, already exposed:

```python
janitor.power = 1478
janitor.threshold = 70  # starts breaking rules when Cloud ≥ 70

cloud.cloud_level  # 0-100, drives mood
cloud.mall_mood   # {calm, uneasy, strained, critical}

zone.qbit_aggregate  # e.g. FC-ARCADE = 6112 influence

# NPC state machines + rules
janitor.rule = "never_crosses_fc_arcade"

# Cloud pressure driven by contradictions & movement
```

**The logic is done. The LLM just annotates it.**

---

## 2. DESIGN GOAL FOR THE LLM LAYER

The LLM should:

1. **React to events** the sim has already decided (rule breaks, Cloud spikes, zone changes)
2. **Speak in-character** (Janitor, Wife, Al-Gorithm, etc.)
3. **Reflect sim state** (Cloud level, mood, QBIT, contradictions) in tone and content
4. **Emit structured output:**
   - `utterance` (what they say)
   - `emotional_state`
   - `tags` (e.g. mentions of zones, systems, people)
   - `action_hint` (optional: "wants to leave", "stares at ceiling", etc.)

**The LLM is read-only to the sim. It doesn't push physics. It annotates them.**

---

## 3. STEP 1 – Reactive NPC Wrapper (Janitor Only, Event-Driven)

### File Structure

```
v7-nextgen/
  src/
    ai/
      npc_llm/
        __init__.py
        janitor_llm.py
        wife_llm.py          # later
        algoritmo_llm.py     # later
```

### Trigger Events

Things your sim already knows how to detect:

- Janitor enters a new zone
- Janitor breaks a rule (e.g. enters FC-ARCADE)
- Cloud crosses a threshold (70, 80, 90)
- Player addresses Janitor ("talk" / proximity interact)

### Prompt Builder

```python
def build_janitor_prompt(janitor, cloud, zone, metadata, event, player_line=None):
    system = f"""
You are THE JANITOR of the mall.

Facts you must obey:
- Your power rating: {janitor.power}
- Your personal Cloud threshold: {janitor.threshold}
- Current Cloud level: {cloud.cloud_level} ({cloud.mall_mood})
- Current zone: {zone.id} (QBIT influence: {zone.qbit_aggregate})
- Personal rule: {janitor.rule_description}
- Rule status: {"BROKEN" if janitor.in_forbidden_zone else "INTACT"}

You always speak like a tired, slightly superstitious maintenance worker
who knows the mall's bones better than management does.
You feel the Cloud like weather pressure in your joints.

Relevant architecture:
- Atrium diameter: {metadata.atrium_diameter} feet
- Tensile roof masts: {metadata.tensile_masts}
"""

    user_context_lines = []

    if event.type == "RULE_BROKEN":
        user_context_lines.append(
            f"You have just broken your rule by entering {zone.id}."
        )
    if event.type == "CLOUD_SPIKE":
        user_context_lines.append(
            f"The Cloud just jumped from {event.prev_cloud} to {cloud.cloud_level}."
        )
    if player_line:
        user_context_lines.append(f"Player says: \"{player_line}\"")

    user_context_lines.append(
        "Describe what you say out loud in 1–3 sentences. "
        "You may hint at connections between systems (arcade, escalators, fountain, credit cards), "
        "but do not invent new locations or physics."
    )

    user = "\n".join(user_context_lines)

    return system, user
```

### Expected Model Response Format

```json
{
  "utterance": "I... I don't usually come here. The lights are too bright. But the water fountain in the atrium is leaking through to the service corridor. The tensile roof masts are dripping. I have to check.",
  "emotional_state": "anxious",
  "tags": ["FC-ARCADE", "fountain", "atrium", "service_corridor"],
  "action_hint": "keeps staring at ceiling lights"
}
```

### Usage in Sim

```python
# When Janitor crosses FC-ARCADE at Cloud 71.5
system, user = build_janitor_prompt(janitor, cloud, zone, metadata, event)
resp = llm_client.chat(system=system, user=user)
janitor_dialogue = json.loads(resp)

# Use in game:
# - render utterance
# - tag his emotional_state in your NPC state machine
# - maybe tweak idle animation based on action_hint
```

**That's Level 1: Every "rule break" or "zone crossing" gets a little horror micro-monologue.**

---

## 4. STEP 2 – Cloud-Aware Dialogue (Tone Bands + QBIT Pull)

### Tone Modes Keyed Off Cloud + Mood

```python
def cloud_tone(cloud_level, mall_mood):
    if cloud_level < 40:
        return "low_pressure"     # small talk, weary humor
    if cloud_level < 70:
        return "uneasy"           # noticing patterns, mild dread
    if cloud_level < 85:
        return "strained"         # jittery, can't ignore signs
    return "critical"             # full-on uncanny horror

def zone_topic_hint(zone):
    # Use QBIT to choose what he obsesses about
    if zone.id == "FC-ARCADE":
        return "arcade_machines_and_frequencies"
    if zone.id == "ATRIUM":
        return "fountain_and_tensile_masts"
    # or use zone.qbit_aggregate sub-keys when you have them
    return "maintenance_systems"
```

### Enhanced System Prompt

```python
tone = cloud_tone(cloud.cloud_level, cloud.mall_mood)
topic = zone_topic_hint(zone)

system = f"""
You are The Janitor...

Cloud tone mode: {tone}
Dominant topic pull in this zone: {topic}

Rules:
- If tone is 'low_pressure', keep things grounded and practical.
- If 'uneasy', let odd details slip in.
- If 'strained', you talk more urgently and make connections.
- If 'critical', you sound like someone who's seen too much: haunted, certain the patterns are real.
"""
```

### Result

```
Cloud 85 + FC-ARCADE + rule broken
⇒ "The arcade machines... they're humming in E-flat. Same as the escalators.
   Same as the fountain pump. It's all connected. I tried to ignore it from
   the service hall, but the sound - it's pulling at the walls. You feel it
   too, don't you? The geometry's wrong. The atrium is 175 feet but it feels
   like... more. The credit cards know. That's why they work as keys."
```

**The LLM isn't inventing that something is wrong—the Cloud number already says it is. The LLM just chooses a poetic angle.**

---

## 5. STEP 3 – Emergent NPC Network (Janitor + Wife + Al-Gorithm)

### Mall Event Log

Simple shared context your sim maintains:

```python
{
  "recent_npc_events": [
    {
      "time": 1021.5,
      "actor": "JANITOR",
      "event": "RULE_BROKEN",
      "zone": "FC-ARCADE"
    },
    {
      "time": 1023.1,
      "actor": "WIFE",
      "event": "SEEN_IN_FORBIDDEN_ZONE",
      "zone": "FC-ARCADE"
    }
  ]
}
```

### Shared Context Builder

```python
def build_shared_context(event_log, max_events=5):
    lines = []
    for e in event_log[-max_events:]:
        lines.append(
            f"{e['time']:.1f}s — {e['actor']} {e['event']} in {e['zone']}"
        )
    return "\n".join(lines) if lines else "No recent notable events."

shared_context = build_shared_context(event_log)

system = f"""
You are {npc.name}.

Shared recent events:
{shared_context}

If other NPCs have broken rules or appeared in forbidden zones,
you may comment on it, worry about it, or deny noticing it—
but you cannot erase the fact that it happened.
"""
```

### Emergent Behaviors

Now they can do things like:

**Wife referencing Janitor's rule break:**
> "He went into the arcade. He never does that..."

**Al-Gorithm noting correlations:**
> "Every time the Janitor breaks, Cloud jumps. Correlation is... concerning."

**Contradictions become fuel:**
- Flag in the prompt when any NPC's stated rule conflicts with logged actions
- Ask the LLM to reflect that as internal dissonance, paranoia, or rationalization

---

## EXAMPLE: FULL EXCHANGE AT CLOUD 85

### Context
- **Time:** 1049.2s
- **Cloud:** 85.3 (critical)
- **Zone:** FC-ARCADE (QBIT: 6112)
- **Janitor:** Rule broken (never_crosses_fc_arcade)
- **Recent events:** Wife seen in service hall, Cloud spike +12.8

### Generated Prompt

```
SYSTEM:
You are THE JANITOR of the mall.

Facts you must obey:
- Your power rating: 1478
- Your personal Cloud threshold: 70
- Current Cloud level: 85.3 (critical)
- Current zone: FC-ARCADE (QBIT influence: 6112)
- Personal rule: Never cross FC-ARCADE
- Rule status: BROKEN

You always speak like a tired, slightly superstitious maintenance worker
who knows the mall's bones better than management does.
You feel the Cloud like weather pressure in your joints.

Relevant architecture:
- Atrium diameter: 175 feet
- Tensile roof masts: 32

Cloud tone mode: critical
Dominant topic pull in this zone: arcade_machines_and_frequencies

Recent events:
1047.1s — WIFE SEEN in SERVICE_HALL
1048.9s — CLOUD_SPIKE +12.8

USER:
You have just broken your rule by entering FC-ARCADE.
Describe what you say out loud in 1–3 sentences.
```

### LLM Response

```json
{
  "utterance": "The arcade machines... they're humming in E-flat. Same as the escalators. Same as the fountain pump. It's all connected. I tried to ignore it from the service hall, but the sound - it's pulling at the walls. You feel it too, don't you? The geometry's wrong. The atrium is 175 feet but it feels like... more.",
  "emotional_state": "obsessed",
  "tags": ["arcade_machines", "escalators", "fountain", "atrium", "geometry", "E-flat"],
  "action_hint": "touching the arcade cabinet, listening intently"
}
```

---

## IMPLEMENTATION CHECKLIST

### Phase 1: Janitor Only (Reactive)
- [ ] Create `src/ai/npc_llm/` directory
- [ ] Implement `janitor_llm.py` with `build_janitor_prompt()`
- [ ] Add LLM client wrapper (OpenAI/Anthropic/local)
- [ ] Hook into existing Janitor state machine events
- [ ] Test: Janitor speaks when crossing FC-ARCADE

### Phase 2: Cloud-Aware Tone
- [ ] Implement `cloud_tone()` function
- [ ] Implement `zone_topic_hint()` function
- [ ] Add tone bands to system prompts
- [ ] Test: Different utterances at Cloud 30 vs 85

### Phase 3: Multi-NPC Network
- [ ] Create `Mall Event Log` data structure
- [ ] Implement `build_shared_context()`
- [ ] Add Wife and Al-Gorithm LLM wrappers
- [ ] Test: NPCs reference each other's actions

### Phase 4: Integration
- [ ] Add to main game loop
- [ ] UI for displaying NPC utterances
- [ ] Audio hooks for text-to-speech (optional)
- [ ] Save/load dialogue history

---

## TECHNICAL REQUIREMENTS

### LLM Client
- OpenAI API (gpt-4o-mini for speed)
- Anthropic API (Claude 3.5 Haiku)
- Or local LLM (Llama 3.1 8B)

### Response Time
- Target: < 500ms for utterance generation
- Use streaming for longer responses
- Cache tone/context prompts

### Cost Estimation
- ~200 tokens per utterance (system + user + response)
- At 10 NPC utterances per minute: ~2000 tokens/min
- Cost: ~$0.01/hour with gpt-4o-mini

---

## WHAT THIS ENABLES

**Emergent NPC horror in a procedurally-stressed mall dungeon:**

- NPCs that feel the Cloud like weather
- Dialogue that reflects QBIT influence
- Contradictions that spawn unique trees
- Multi-NPC awareness and paranoia
- Architectural knowledge grounded in real CRD data
- Tone that escalates with simulation pressure

**You're not "3 steps away" in the vague sense.**

You're literally:
1. Build the prompt function (inputs you already have)
2. Decide on JSON output contract
3. Call the model on existing events

**Do that for just the Janitor, and boom: it's real.**

---

## NEXT STEPS

1. Review this document
2. Create `src/ai/npc_llm/janitor_llm.py`
3. Wire up one event: Janitor enters FC-ARCADE
4. See what he says at Cloud 71.5

**The mall awaits its voices.**

---

*Design Document v1.0*
*V7 Integration + LLM Layer*
*"Everything but visuals: READY. Now give them words."*
