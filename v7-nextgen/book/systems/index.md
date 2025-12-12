# Systems

```{admonition} Governance
:class: warning
This book records observations. It does not define behavior.
```

The operational layer. How things tick.

---

## Cloud

The metaphysics engine. Pressure, mood bands, bleed tiers.

| Source | Location |
|--------|----------|
| Implementation | [`v8-nextgen/src/cloud.py`](../../v8-nextgen/src/cloud.py) |
| Bridge adapter | [`v7-nextgen/src/mall_sim_bridge.py`](../src/mall_sim_bridge.py) → `HeatCloudBridge` |
| Integration doc | [`v7-nextgen/docs/MALL_SIM_BRIDGE_INTEGRATION.md`](../docs/MALL_SIM_BRIDGE_INTEGRATION.md) |

---

## QBIT

Entity influence scoring. Power, charisma, resonance.

| Source | Location |
|--------|----------|
| Engine | [`v8-nextgen/src/qbit_engine.py`](../../v8-nextgen/src/qbit_engine.py) |
| Entity definitions | [`v8-nextgen/canon/entities/`](../../v8-nextgen/canon/entities/) (17 JSON) |
| Zone solver | [`v8-nextgen/src/zone_influence_solver.py`](../../v8-nextgen/src/zone_influence_solver.py) |
| Bridge adapter | [`v7-nextgen/src/mall_sim_bridge.py`](../src/mall_sim_bridge.py) → `compute_npc_qbit()` |

---

## NPC Spines

Behavioral constraints. Never-rules, always-rules, mood overrides.

| Source | Location |
|--------|----------|
| Registry | [`v7-nextgen/src/mall_sim_bridge.py`](../src/mall_sim_bridge.py) → `SPINE_REGISTRY` |
| Toddler system | [`v8-nextgen/src/ai/toddler/toddler_system.py`](../../v8-nextgen/src/ai/toddler/toddler_system.py) |
| Janitor LLM | [`v8-nextgen/src/ai/npc_llm/janitor_llm.py`](../../v8-nextgen/src/ai/npc_llm/janitor_llm.py) |
| Pattern dialogue | [`v8-nextgen/src/pattern_dialogue_engine.py`](../../v8-nextgen/src/pattern_dialogue_engine.py) |

---

## Mall-Sim Bridge

Integration layer between mall-sim and Mall_OS.

| Source | Location |
|--------|----------|
| Bridge module | [`v7-nextgen/src/mall_sim_bridge.py`](../src/mall_sim_bridge.py) (919 lines) |
| README | [`v7-nextgen/src/mall_sim_bridge_README.md`](../src/mall_sim_bridge_README.md) |
| Integration doc | [`v7-nextgen/docs/MALL_SIM_BRIDGE_INTEGRATION.md`](../docs/MALL_SIM_BRIDGE_INTEGRATION.md) |

---

## Ninja Loop

Game loop. Grid, player, constructs, state.

| Source | Location |
|--------|----------|
| Main loop | [`v8-nextgen/ninja/ninja_loop.py`](../../v8-nextgen/ninja/ninja_loop.py) |
| PFDL kernel | [`v8-nextgen/ninja/pfdl.py`](../../v8-nextgen/ninja/pfdl.py) |
| State manager | [`v8-nextgen/ninja/state_manager.py`](../../v8-nextgen/ninja/state_manager.py) |
| Runtime entry | [`v8-nextgen/NEW-needs_integration/Visual_Runtime_Entry.py`](../../v8-nextgen/NEW-needs_integration/Visual_Runtime_Entry.py) |

---

## Timeline

Four eras. INPUT → UPDATE → COLLIDE → RENDER.

| Source | Location |
|--------|----------|
| Timeline system | [`v8-nextgen/src/timeline_system.py`](../../v8-nextgen/src/timeline_system.py) |
| Meta-architecture | [`v8-nextgen/META_ARCHITECTURE.md`](../../v8-nextgen/META_ARCHITECTURE.md) |
| Contradiction handler | [`v8-nextgen/src/contradiction_handler.py`](../../v8-nextgen/src/contradiction_handler.py) |

---

*Systems listed by reference. Implementation details live in source.*
