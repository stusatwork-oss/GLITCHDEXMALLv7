#!/usr/bin/env python3
"""
GAME STATE MANAGER
Loads initial world state (Service Hall / Food Court) into the Ninja Engine.
"""

import json
import random
from typing import Dict, Any, List, Tuple, TYPE_CHECKING

# Forward declarations for type hinting
if TYPE_CHECKING:
    from ninja.consensus_engine import ConsensusEngine
    from ninja.cloud_flocking import CloudFlock

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

    def get_grid_context(self) -> Dict[str, Any]:
        """Returns the full grid definition (walls, floors, nav availability)."""
        return self.current_state.get("grid", {})

    def get_cloud_anchors(self) -> List[Tuple[int, int]]:
        """
        Return all constructs and signal sources that should attract cloud.
        Expected JSON format: "cloud_anchors": [ { "x": 14, "y": 9 }, ... ]
        """
        anchors = []
        for item in self.current_state.get("cloud_anchors", []):
            if isinstance(item, dict) and "x" in item and "y" in item:
                anchors.append((item["x"], item["y"]))
        return anchors

    def bootstrap(self, consensus_engine: Any, cloud_flock: Any):
        """
        Injects game state into subsystems automatically with Thermal Noise.
        Seeds cloud field using object spawns and anchors.
        
        Args:
            consensus_engine: Passed for potential pre-heating.
            cloud_flock: The flocking simulation to seed with signal attractors.
        """
        if not self.current_state:
            print("[BOOTSTRAP] Warning: No state loaded. Call load_state() first.")
            return

        anchors = {}
        
        # THERMAL NOISE CONFIG
        # Simulates imperfect hardware / analog signal variance
        VOLTAGE_FUZZ = 0.05  # +/- 5% signal strength variance
        SNR_FUZZ = 0.1       # +/- 10% signal integrity variance

        # 1. Convert Spawns to Signal Sources (Standard Voltage)
        for (_, x, y) in self.get_spawns():
            # Inject fuzz so no two trash cans feel exactly the same to the cloud
            v_noise = random.uniform(-VOLTAGE_FUZZ, VOLTAGE_FUZZ)
            s_noise = random.uniform(-SNR_FUZZ, SNR_FUZZ)
            
            anchors[(x, y)] = {
                "voltage": 0.5 + v_noise, 
                "snr": 1.0 + s_noise
            }

        # 2. Convert Designer Anchors (High Voltage)
        for (x, y) in self.get_cloud_anchors():
            v_noise = random.uniform(-VOLTAGE_FUZZ, VOLTAGE_FUZZ)
            s_noise = random.uniform(-SNR_FUZZ, SNR_FUZZ)
            
            anchors[(x, y)] = {
                "voltage": 0.7 + v_noise, 
                "snr": 1.2 + s_noise
            }

        # 3. Ignite the Field
        cloud_flock.update_field(anchors)
        
        print(f"[BOOTSTRAP] Cloud field seeded with {len(anchors)} nodes.")
        print(f"[BOOTSTRAP] Thermal Noise injected (Fuzz: +/-{VOLTAGE_FUZZ}).")