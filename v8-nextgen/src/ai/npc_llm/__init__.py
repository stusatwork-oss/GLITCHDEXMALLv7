"""
LLM NPC Layer v1 - Reactive NPC Dialogue System

This module provides LLM-powered dialogue for NPCs in the V7 mall simulation.
NPCs react to simulation events (rule breaks, Cloud spikes, zone changes) with
contextually-aware utterances that reflect:

- Cloud level and mood state
- Zone QBIT influence
- NPC power ratings and contradiction thresholds
- Shared event context (multi-NPC awareness)

The LLM is read-only to the simulation - it annotates physics, it doesn't push them.

Usage:
    from ai.npc_llm.janitor_llm import build_janitor_prompt

    system, user = build_janitor_prompt(janitor, cloud, zone, metadata, event)
    response = llm_client.chat(system=system, user=user)
    dialogue = parse_npc_response(response)

See: docs/LLM_NPC_LAYER_v1.md for full design specification.
"""

__version__ = "1.0.0-alpha"
__all__ = []

# Future imports:
# from .janitor_llm import build_janitor_prompt
# from .wife_llm import build_wife_prompt
# from .algoritmo_llm import build_algoritmo_prompt
