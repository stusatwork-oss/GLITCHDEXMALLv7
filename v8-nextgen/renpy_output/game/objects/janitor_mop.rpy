# Voxel Object: JANITOR_MOP
# Symbol: 🧹
# Source: assets/voxel_sources/janitor_mop.png

define voxel_janitor_mop = {
    "symbol": "🧹",
    "obj_id": "JANITOR_MOP",
    "qbit": {
    "power": 500,
    "charisma": 100,
    "resonance": 80,
    "owner_npc_id": "UNIT_7",
    "note": "Structural tool, NPC resource dependency"
},
    "qbit_aggregate": 680,
    "placement": {"attach": "floor", "offset": [0, 0, 0]},
    "behavior": {"type": "NPC_PROP", "tags": ["SERVICE_HALL", "UNIT7"], "on_pickup": ["subtitle: 'You really shouldn't be holding that.'", "cloud_pressure+2"]},
    # Probe telemetry format
    "entity_type": 2,
}

label interact_janitor_mop:
    show voxel_janitor_mop at center

    "You really shouldn't be holding that."
    $ cloud_pressure += 2

    return
