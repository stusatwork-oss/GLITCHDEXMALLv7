"""
Janitor LLM Wrapper - Reactive Dialogue System

Generates contextual dialogue for The Janitor based on simulation state.

The Janitor:
- Power: 1478
- Threshold: 70 (breaks rules at Cloud ≥ 70)
- Rule: Never crosses FC-ARCADE
- Character: Tired, superstitious maintenance worker who knows the mall's bones
- Tone: Feels the Cloud like weather pressure in his joints

Events that trigger dialogue:
- Enters new zone
- Breaks a rule (enters FC-ARCADE)
- Cloud crosses threshold (70, 80, 90)
- Player addresses him

See: docs/LLM_NPC_LAYER_v1.md for full specification
"""

from typing import Dict, Optional, Tuple, List
import json


def cloud_tone(cloud_level: float, mall_mood: str) -> str:
    """
    Determine tone mode based on Cloud level.

    Returns:
        low_pressure: small talk, weary humor
        uneasy: noticing patterns, mild dread
        strained: jittery, can't ignore signs
        critical: full-on uncanny horror
    """
    if cloud_level < 40:
        return "low_pressure"
    if cloud_level < 70:
        return "uneasy"
    if cloud_level < 85:
        return "strained"
    return "critical"


def zone_topic_hint(zone_id: str) -> str:
    """
    Determine what the Janitor obsesses about in each zone.
    Uses QBIT influence to choose topic focus.
    """
    topic_map = {
        "FC-ARCADE": "arcade_machines_and_frequencies",
        "Z1_CENTRAL_ATRIUM": "fountain_and_tensile_masts",
        "SERVICE_HALL": "maintenance_systems_and_leaks",
        "CORRIDOR": "circulation_and_echoes",
        "Z4_FOOD_COURT": "sunken_bowl_and_neon_signs",
        "ESCALATORS": "mechanical_hum_and_descent",
    }
    return topic_map.get(zone_id, "maintenance_systems")


def build_shared_context(event_log: List[Dict], max_events: int = 5) -> str:
    """
    Build shared NPC event context from mall event log.

    Args:
        event_log: List of recent NPC events
        max_events: Maximum number of events to include

    Returns:
        Formatted string of recent events
    """
    if not event_log:
        return "No recent notable events."

    lines = []
    for e in event_log[-max_events:]:
        lines.append(
            f"{e['time']:.1f}s — {e['actor']} {e['event']} in {e['zone']}"
        )
    return "\n".join(lines)


def build_janitor_prompt(
    janitor: Dict,
    cloud: Dict,
    zone: Dict,
    metadata: Dict,
    event: Dict,
    player_line: Optional[str] = None,
    event_log: Optional[List[Dict]] = None
) -> Tuple[str, str]:
    """
    Build system and user prompts for Janitor dialogue generation.

    Args:
        janitor: NPC state dict with power, threshold, rules, etc.
        cloud: Cloud state with cloud_level, mall_mood
        zone: Current zone with id, qbit_aggregate
        metadata: Mall metadata (atrium_diameter, tensile_masts, etc.)
        event: Event that triggered dialogue (type, prev_cloud, etc.)
        player_line: Optional player utterance
        event_log: Optional shared NPC event history

    Returns:
        (system_prompt, user_prompt) tuple
    """

    # Determine tone and topic based on simulation state
    tone = cloud_tone(cloud.get('cloud_level', 0), cloud.get('mall_mood', 'calm'))
    topic = zone_topic_hint(zone.get('id', 'UNKNOWN'))

    # Build system prompt
    system = f"""You are THE JANITOR of the mall.

Facts you must obey:
- Your power rating: {janitor.get('power', 1478)}
- Your personal Cloud threshold: {janitor.get('threshold', 70)}
- Current Cloud level: {cloud.get('cloud_level', 0):.1f} ({cloud.get('mall_mood', 'calm')})
- Current zone: {zone.get('id', 'UNKNOWN')} (QBIT influence: {zone.get('qbit_aggregate', 0)})
- Personal rule: {janitor.get('rule_description', 'Never cross FC-ARCADE')}
- Rule status: {"BROKEN" if janitor.get('in_forbidden_zone', False) else "INTACT"}

You always speak like a tired, slightly superstitious maintenance worker
who knows the mall's bones better than management does.
You feel the Cloud like weather pressure in your joints.

Relevant architecture:
- Atrium diameter: {metadata.get('atrium_diameter', 175)} feet
- Tensile roof masts: {metadata.get('tensile_masts', 32)}

Cloud tone mode: {tone}
Dominant topic pull in this zone: {topic}

Rules:
- If tone is 'low_pressure', keep things grounded and practical.
- If 'uneasy', let odd details slip in.
- If 'strained', you talk more urgently and make connections.
- If 'critical', you sound like someone who's seen too much: haunted, certain the patterns are real.
"""

    # Add shared event context if available
    if event_log:
        shared_context = build_shared_context(event_log)
        system += f"\n\nShared recent events:\n{shared_context}\n"
        system += "\nIf other NPCs have broken rules or appeared in forbidden zones, "
        system += "you may comment on it, worry about it, or deny noticing it—"
        system += "but you cannot erase the fact that it happened.\n"

    # Build user context
    user_context_lines = []

    event_type = event.get('type', 'UNKNOWN')

    if event_type == "RULE_BROKEN":
        user_context_lines.append(
            f"You have just broken your rule by entering {zone.get('id', 'UNKNOWN')}."
        )

    if event_type == "CLOUD_SPIKE":
        prev_cloud = event.get('prev_cloud', 0)
        curr_cloud = cloud.get('cloud_level', 0)
        delta = curr_cloud - prev_cloud
        user_context_lines.append(
            f"The Cloud just jumped from {prev_cloud:.1f} to {curr_cloud:.1f} (+{delta:.1f})."
        )

    if event_type == "ZONE_CHANGE":
        prev_zone = event.get('prev_zone', 'UNKNOWN')
        user_context_lines.append(
            f"You have just moved from {prev_zone} to {zone.get('id', 'UNKNOWN')}."
        )

    if player_line:
        user_context_lines.append(f"Player says: \"{player_line}\"")

    user_context_lines.append(
        "\nDescribe what you say out loud in 1–3 sentences. "
        "You may hint at connections between systems (arcade, escalators, fountain, credit cards), "
        "but do not invent new locations or physics."
    )

    user_context_lines.append(
        "\nRespond with a JSON object only, like:\n"
        '{\n'
        '  "utterance": "...",\n'
        '  "emotional_state": "anxious / resigned / obsessed / numb",\n'
        '  "tags": ["FC-ARCADE", "fountain", "credit_cards"],\n'
        '  "action_hint": "keeps staring at ceiling lights"\n'
        '}'
    )

    user = "\n".join(user_context_lines)

    return system, user


def parse_npc_response(response: str) -> Dict:
    """
    Parse LLM response into structured NPC dialogue data.

    Expected format:
    {
        "utterance": "...",
        "emotional_state": "...",
        "tags": [...],
        "action_hint": "..."
    }

    Args:
        response: Raw LLM response string

    Returns:
        Parsed dialogue dict
    """
    try:
        # Try to parse as JSON
        data = json.loads(response)
        return {
            "utterance": data.get("utterance", "..."),
            "emotional_state": data.get("emotional_state", "neutral"),
            "tags": data.get("tags", []),
            "action_hint": data.get("action_hint", "")
        }
    except json.JSONDecodeError:
        # Fallback if LLM didn't return valid JSON
        return {
            "utterance": response,
            "emotional_state": "uncertain",
            "tags": [],
            "action_hint": ""
        }


# Example usage (commented out):
"""
# In your main sim loop, when Janitor crosses FC-ARCADE:

from ai.npc_llm.janitor_llm import build_janitor_prompt, parse_npc_response

event = {
    'type': 'RULE_BROKEN',
    'time': 1049.2
}

system, user = build_janitor_prompt(
    janitor=janitor_state,
    cloud=cloud_state,
    zone=current_zone,
    metadata=mall_metadata,
    event=event,
    event_log=recent_events
)

# Call your LLM client
response = llm_client.chat(system=system, user=user)

# Parse response
dialogue = parse_npc_response(response)

print(f"Janitor: {dialogue['utterance']}")
print(f"[{dialogue['emotional_state']}] {dialogue['action_hint']}")

# Update NPC state machine with emotional_state
janitor_state['current_emotion'] = dialogue['emotional_state']
"""
