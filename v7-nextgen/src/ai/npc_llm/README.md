# LLM NPC Layer - Implementation

This directory contains the LLM-powered dialogue system for V7 NPCs.

## Current Status

**Phase 1: Janitor Only (Reactive)** ✓ Structure Created
- [x] Directory structure
- [x] `janitor_llm.py` - Complete implementation
- [ ] LLM client wrapper
- [ ] Integration with Janitor state machine
- [ ] Testing

**Phase 2: Cloud-Aware Tone** ✓ Implemented in janitor_llm.py
- [x] `cloud_tone()` function
- [x] `zone_topic_hint()` function
- [x] Tone bands in system prompts

**Phase 3: Multi-NPC Network** 🔲 Placeholder
- [x] Shared event context builder
- [ ] Wife LLM wrapper
- [ ] Al-Gorithm LLM wrapper
- [ ] Mall Event Log data structure

## Quick Start

```python
from ai.npc_llm.janitor_llm import build_janitor_prompt, parse_npc_response

# When an event triggers (e.g., Janitor crosses FC-ARCADE)
event = {
    'type': 'RULE_BROKEN',
    'time': 1049.2
}

system, user = build_janitor_prompt(
    janitor=janitor_state,
    cloud=cloud_state,
    zone=current_zone,
    metadata=mall_metadata,
    event=event
)

# Call your LLM client
response = llm_client.chat(system=system, user=user)

# Parse structured response
dialogue = parse_npc_response(response)

print(f"Janitor: {dialogue['utterance']}")
```

## Files

- `__init__.py` - Package initialization
- `janitor_llm.py` - The Janitor dialogue system (COMPLETE)
- `wife_llm.py` - The Wife dialogue system (PLACEHOLDER)
- `algoritmo_llm.py` - Al-Gorithm dialogue system (PLACEHOLDER)

## See Also

- [LLM_NPC_LAYER_v1.md](../../docs/LLM_NPC_LAYER_v1.md) - Full design specification
- [API.md](../../docs/API.md) - V7 integration API reference

## Next Steps

1. Implement LLM client wrapper (OpenAI/Anthropic/local)
2. Wire up to existing Janitor state machine events
3. Test: Janitor speaks when crossing FC-ARCADE at Cloud 71.5
4. Extend to Wife and Al-Gorithm

**The mall awaits its voices.**
