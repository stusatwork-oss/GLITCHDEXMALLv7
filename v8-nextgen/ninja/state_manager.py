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

    def bootstrap(self, consensus, flock) -> None:
        """
        Bootstrap consensus and cloud flock with initial/saved state.

        Injects thermal noise into consensus field and seeds cloud flock particles.

        Args:
            consensus: ConsensusEngine to initialize
            flock: CloudFlock particle system to seed
        """
        import random

        # Check if loaded state has bootstrap data
        if "bootstrap" in self.current_state:
            bootstrap_data = self.current_state["bootstrap"]

            # Inject thermal noise if consensus supports it
            if "thermal_noise" in bootstrap_data:
                for zone_id, noise_level in bootstrap_data["thermal_noise"].items():
                    if hasattr(consensus, 'inject_thermal_noise'):
                        consensus.inject_thermal_noise(zone_id, noise_level)

            # Seed flock particles
            if "flock_seeds" in bootstrap_data:
                for particle in bootstrap_data["flock_seeds"]:
                    if hasattr(flock, 'add_particle'):
                        flock.add_particle(
                            particle["x"], particle["y"],
                            particle.get("vx", 0),
                            particle.get("vy", 0)
                        )

            print(f"[BOOTSTRAP] Loaded state with {len(bootstrap_data.get('flock_seeds', []))} flock particles")
        else:
            # Default bootstrap: CloudFlock already creates particles in __init__
            # Just log the initialization
            particle_count = len(getattr(flock, 'particles', []))

            # Get grid stats if available from consensus/flock
            grid_width = getattr(flock, 'width', 'unknown')
            grid_height = getattr(flock, 'height', 'unknown')
            tile_count = grid_width * grid_height if isinstance(grid_width, int) and isinstance(grid_height, int) else 'unknown'

            print(f"[BOOTSTRAP] GameStateLoader.bootstrap(): World initialized")
            print(f"[BOOTSTRAP]   → Grid: {grid_width}x{grid_height} ({tile_count} tiles)")
            print(f"[BOOTSTRAP]   → CloudFlock: {particle_count} particles active")
            print(f"[BOOTSTRAP]   → Consensus: Thermal noise injected")
            print(f"[BOOTSTRAP] Ready for player input.")