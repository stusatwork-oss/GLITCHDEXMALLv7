# Voxel Object: TRASH_CAN
# Symbol: 🗑️
# Source: assets/voxel_sources/trash_can.png

define voxel_trash_can = {
    "symbol": "🗑️",
    "obj_id": "TRASH_CAN",
    "qbit": {},
    "qbit_aggregate": 0,
    "placement": {"attach": "floor", "offset": [0, 0, 0]},
    "behavior": {"type": "STATIC", "tags": ["FOODCOURT", "SERVICE"], "on_use": ["subtitle: 'The smell is a whole separate timeline.'"]},
    # Probe telemetry format
    "entity_type": 2,
}
