# Voxel Object: ARCADE_TOKEN
# Symbol: 🪙
# Source: assets/voxel_sources/arcade_token.png

define voxel_arcade_token = {
    "symbol": "🪙",
    "obj_id": "ARCADE_TOKEN",
    "qbit": {
    "power": 50,
    "charisma": 800,
    "resonance": 120,
    "note": "High attention draw, low structural leverage"
},
    "qbit_aggregate": 970,
    "placement": {"attach": "floor", "offset": [0, 0, 0]},
    "behavior": {"type": "PICKUP", "tags": ["ARCADE", "CURRENCY"], "on_pickup": ["cloud_pressure+1", "subtitle: 'Something in the arcade wakes up.'", "flag:FOUND_TOKEN=true"]},
    # Probe telemetry format
    "entity_type": 2,
}
