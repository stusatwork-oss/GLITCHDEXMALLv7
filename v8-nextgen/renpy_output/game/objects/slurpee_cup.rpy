# Voxel Object: SLURPEE_CUP
# Symbol: 🥤
# Source: assets/voxel_sources/slurpee_front.png

define voxel_slurpee_cup = {
    "symbol": "🥤",
    "obj_id": "SLURPEE_CUP",
    "qbit": {},
    "qbit_aggregate": 0,
    "placement": {"attach": "floor", "offset": [0, 0, 0]},
    "behavior": {"type": "PICKUP", "tags": ["FOODCOURT", "DRINK"], "on_pickup": ["cloud_pressure+5", "subtitle: 'Brain freeze hits like divine revelation.'"]},
    # Probe telemetry format
    "entity_type": 2,
}
