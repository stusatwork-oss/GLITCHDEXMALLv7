#!/usr/bin/env python3
"""
NINJA GAME LOOP v8.0 - MULTI-STATE RUNTIME
Features:
- Dynamic Level Loading (Food Court vs Service Hall)
- Full Consensus/Flocking Pipeline
- Bootstrap Injection with Thermal Noise
"""

import sys
import time
import random
from pathlib import Path

# Add src root
sys.path.append(str(Path(__file__).parent))

from cloud import Cloud
from ninja_grid import NinjaGrid
from ninja_npc import ShadowJanitorMachine
from npc_state_machine import NPCSpine
# These modules were expected to be in a 'ninja' package but are now in src root?
# No, let's check where they are.
# It seems 'ninja.pfdl' implies a folder 'ninja' with 'pfdl.py'.
# The previous `ls v8-nextgen/ninja` showed pfdl.py exists there.
# But `sys.path.append(str(Path(__file__).parents[2]))` was pointing to repo root (v8-nextgen).
# Now `game_loop.py` is in `src/`. `ninja` folder is in `v8-nextgen/ninja`.
# So we need to add `v8-nextgen` to sys.path to import `ninja.pfdl`.

# Let's fix the sys.path to point to v8-nextgen root
sys.path.append(str(Path(__file__).parents[1]))

from src.cloud import Cloud
from src.ninja_grid import NinjaGrid
from src.ninja_npc import ShadowJanitorMachine
from src.npc_state_machine import NPCSpine

# These are in v8-nextgen/ninja/
from ninja.pfdl import PFDLKernel
from ninja.voxel_bridge import VoxelBridge
from ninja.ninja_assets import seed_ninja_assets
from ninja.standard_assets import seed_standard_assets
from ninja.state_manager import GameStateLoader
from ninja.cloud_flocking import CloudFlock
from ninja.consensus_engine import ConsensusEngine

try:
    from src.voxel_object_loader import VoxelObjectLoader
    VOXEL_SYS_READY = True
except ImportError:
    VOXEL_SYS_READY = False

class NinjaGameMode:
    def __init__(self, level_file="game_state_foodcourt_v1.json"):
        print(f"[INIT] Booting NINJA_SABOTEUR v8.0 (Level: {level_file})...")
        self.repo_root = Path(__file__).parents[2]
        
        # 1. Seed Assets (Ninja + Standard User Assets)
        seed_ninja_assets(self.repo_root)
        seed_standard_assets(self.repo_root)

        # 2. Systems Init
        self.voxel_loader = None
        if VOXEL_SYS_READY:
            self.voxel_loader = VoxelObjectLoader(
                source_dir=self.repo_root / "assets" / "voxel_sources" / "ninja",
                palette_path=None
            )
            # Add standard path for user assets
            self.voxel_loader.source_dirs.append(
                self.repo_root / "assets" / "voxel_sources" / "standard"
            )

        self.state_loader = GameStateLoader()
        self.game_state_data = self.state_loader.load_state(level_file)
        
        # 3. Environment & Consensus
        # Determine Zone from State (Default to Z4 if missing)
        target_zone = self.game_state_data.get("zone", "Z4_FOOD_COURT")
        self.grid = NinjaGrid(target_zone)
        
        self.bridge = VoxelBridge(self.voxel_loader)
        self.firmware = PFDLKernel("PLAYER_NINJA")
        self.consensus = ConsensusEngine()
        self.cloud = Cloud()
        self.cloud.cloud_level = self.state_loader.get_cloud_pressure()
        
        # 4. Bootstrap the "Analog" Field
        self.flock = CloudFlock(self.grid.width, self.grid.height, count=40)
        self.state_loader.bootstrap(self.consensus, self.flock)

        # 5. Populate Physical World (Visuals)
        self._populate_initial_voxels()

        # 6. Actors
        self.player_pos = [10, 10]
        self.resources = {"focus": 85, "slots": 5}
        
        spine = NPCSpine("shadow-janitor", "Shadow Janitor", "Primary")
        self.janitor = ShadowJanitorMachine("shadow-janitor", spine, self.grid)

        # Circuit Memory
        self.circuit_nodes = {} 
        self._sync_circuit_memory()

        print("[READY] RUNTIME ACTIVE.")

    def _populate_initial_voxels(self):
        """Spawns visual objects without triggering construction costs."""
        spawns = self.state_loader.get_spawns()
        for (oid, x, y) in spawns:
            # Create a mock result to feed the bridge
            from ninja.pfdl import ConstructResult
            res = ConstructResult(success=True, voxel_id=oid)
            self.bridge.spawn_construct(x, y, res, self.game_state_data)
            
            t = self.grid.get_tile(x, y)
            if t: t.construct = {"name": oid}

    def _sync_circuit_memory(self):
        """Syncs pre-existing spawns to circuit memory for flocking."""
        # This picks up the bootstrap values + active constructs
        for (x, y) in self.bridge.active_voxels:
            self.circuit_nodes[(x, y)] = {"voltage": 0.5, "snr": 1.0}

    def tick(self, dt: float, cmd: dict = None):
        if cmd: self._handle_input(cmd)
        
        # Simulation
        self.flock.update_field(self.circuit_nodes)
        self.flock.tick()
        
        self.cloud.update(dt)
        self.janitor.update_ninja_logic(dt, self.cloud, tuple(self.player_pos))

        return self._snapshot()

    def _handle_input(self, cmd):
        act = cmd.get('action')
        
        if act == 'MOVE':
            dx, dy = cmd.get('dir')
            nx, ny = self.player_pos[0]+dx, self.player_pos[1]+dy
            if self.grid.get_tile(nx, ny): self.player_pos = [nx, ny]
            
        elif act == 'CONSTRUCT':
            trap_type = cmd.get('type')
            t = self.grid.get_tile(*self.player_pos)
            
            # Gather Context
            grid_ctx = {
                "tile_type": t.type,
                "light_level": t.light_level,
                "has_construct": t.construct is not None
            }
            swarm_pos = list(self.bridge.active_voxels.keys())
            
            # Pipeline
            res = self.firmware.process_proposal(
                trap_type, 
                self.resources, 
                grid_ctx, 
                swarm_pos, 
                tuple(self.player_pos)
            )
            
            if res.success:
                self.resources["focus"] -= res.cost_focus
                t.construct = {"name": trap_type}
                self.bridge.spawn_construct(self.player_pos[0], self.player_pos[1], res, self.game_state_data)
                
                # Update Circuit Memory
                self.circuit_nodes[tuple(self.player_pos)] = {
                    "voltage": res.circuit_metrics.get("score", 0.0),
                    "snr": res.circuit_metrics.get("stability", 1.0)
                }
            else:
                print(f"[REJECTED] {res.message}")

    def _snapshot(self):
        px, py = self.player_pos
        return {
            "focus": self.resources["focus"],
            "swarm_count": len(self.circuit_nodes),
            "cloud_density": self.flock.get_density_at(px, py),
            "cloud": self.cloud.cloud_level,
            "level_id": self.game_state_data.get("level_id", "UNKNOWN")
        }