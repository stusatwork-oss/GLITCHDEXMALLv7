# Voxel Object: PIZZA_SLICE
# Symbol: 🍕
# Source: assets/voxel_sources/pizza_slice.png

define voxel_pizza_slice = {
    "symbol": "🍕",
    "obj_id": "PIZZA_SLICE",
    "qbit": {
    "power": 20,
    "charisma": 50,
    "resonance": 30,
    "note": "Consumable heat sink, low impact"
},
    "qbit_aggregate": 100,
    "placement": {"attach": "table", "offset": [0, 0, 0]},
    "behavior": {"type": "PICKUP", "tags": ["FOODCOURT", "FOOD"], "on_pickup": ["cloud_pressure-3", "subtitle: 'Grease calms the storm, for now.'"]},
    # Probe telemetry format
    "entity_type": 2,
}
