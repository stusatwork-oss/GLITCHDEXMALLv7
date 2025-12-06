#!/usr/bin/env python3
"""
VOXEL BRIDGE
Connects PFDL logic to V6 Engine spawning.
"""
from typing import Dict, Any, Optional

class VoxelBridge:
    def __init__(self, loader=None):
        self.loader = loader
        self.active_voxels: Dict[tuple, dict] = {} 

    def spawn_construct(self, x: int, y: int, pfdl_result, game_state: Any):
        if not pfdl_result.success or not pfdl_result.voxel_id: return
        
        self.active_voxels[(x, y)] = {"id": pfdl_result.voxel_id}
        
        # Register in V6 Game State
        if isinstance(game_state, dict):
            if "object_spawns" not in game_state: game_state["object_spawns"] = []
            game_state["object_spawns"].append({
                "object_id": pfdl_result.voxel_id,
                "pos": (x, y, 0),
                "behavior": "ACTIVE"
            })

    def check_tags_at(self, x, y):
        # Placeholder for complex tag lookup
        return []