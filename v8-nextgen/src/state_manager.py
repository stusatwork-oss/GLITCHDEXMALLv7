#!/usr/bin/env python3
"""
GAME STATE MANAGER
Loads initial world state (Service Hall / Food Court) into the Ninja Engine.
"""

import json
from typing import Dict, Any, List, Tuple

class GameStateLoader:
    def __init__(self):
        self.current_state = {}

    def load_state(self, json_path: str) -> Dict[str, Any]:
        """Loads a Game State JSON."""
        try:
            with open(json_path, 'r') as f:
                self.current_state = json.load(f)
                print(f"[STATE] Loaded Level: {self.current_state.get('level_id')}")
                return self.current_state
        except Exception as e:
            print(f"[STATE] Error loading {json_path}: {e}")
            return {}

    def get_spawns(self) -> List[Tuple[str, int, int]]:
        """Extracts initial object spawns as (ID, x, y)."""
        spawns = []
        raw_spawns = self.current_state.get("object_spawns", [])
        for s in raw_spawns:
            oid = s.get("object_id")
            pos = s.get("pos", [0, 0])
            if oid and len(pos) >= 2:
                spawns.append((oid, pos[0], pos[1]))
        return spawns

    def get_initial_flags(self) -> Dict[str, bool]:
        return self.current_state.get("flags", {})

    def get_cloud_pressure(self) -> float:
        return self.current_state.get("cloud_pressure", 0.0)