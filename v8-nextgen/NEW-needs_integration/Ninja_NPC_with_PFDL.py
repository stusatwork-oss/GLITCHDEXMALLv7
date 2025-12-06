#!/usr/bin/env python3
"""
NINJA NPC ADAPTER v2.0 - PFDL ENABLED
The Janitor is now a World Builder running FW_NINJA_SABOTEUR_v1.1.
"""

import sys
import random
from pathlib import Path

# Add src root to path
sys.path.append(str(Path(__file__).parents[2]))

from npc_state_machine import NPCStateMachine, NPCState, NPCSpine
from contradiction_handler import handle_npc_contradiction
from cloud import Cloud
from ninja.pfdl import PFDLKernel

class ShadowJanitorMachine(NPCStateMachine):
    """
    The Shadow Janitor: A 'Maintenance' Architect.
    
    He runs the Ninja Firmware to 'Construct' maintenance fixes (Trap Disarms, Door Repairs).
    If he encounters a Player Construct (Sabotage), it causes a PDSL MERGE CONFLICT.
    """

    def __init__(self, npc_id: str, spine: NPCSpine, grid_ref):
        super().__init__(npc_id, spine, current_zone=grid_ref.zone_id)
        
        self.grid = grid_ref
        self.wattitude_band = "COOL"
        
        # FIRMWARE STACK (The "World Builder" Logic)
        self.firmware = PFDLKernel("SHADOW_JANITOR")
        
        self.pos_x = 0
        self.pos_y = 0
        self._stun_timer = 0.0

        # AI Resources (Simulated)
        self.resources = {"focus": 100, "slots": 5}

    def update_ninja_logic(self, dt: float, cloud: Cloud, player_pos: tuple):
        """
        The Janitor's Execution Cycle.
        SCAN -> SHADOW -> CONSTRUCT -> EXECUTE
        """
        if self._stun_timer > 0:
            self._stun_timer -= dt
            return

        self._sync_wattitude(cloud.cloud_level)

        # 1. SCAN: Check for Anomalies (Player Constructs)
        self._scan_phase(cloud)

        # 2. EXECUTE: Patrol or Maintain
        self._maintain_patrol(dt)

    def _sync_wattitude(self, pressure: float):
        if pressure < 40: self.wattitude_band = "COOL"
        elif pressure < 70: self.wattitude_band = "WARM"
        elif pressure < 85: self.wattitude_band = "HOT"
        else: self.wattitude_band = "CRITICAL"

    def _scan_phase(self, cloud: Cloud):
        """
        The Janitor checks his current coordinate for 'Merge Conflicts'.
        (i.e., Stepping on a Player Trap)
        """
        tile = self.grid.get_tile(self.pos_x, self.pos_y)
        
        # If tile has a construct NOT built by Janitor (implied), it's a conflict.
        if tile and tile.construct:
            trap_name = tile.construct['name']
            
            # PDSL FAILURE MODE: NINJA_MERGE_FAIL
            # "Simultaneous movement plan (Janitor) + construction plan (Trap) cannot both be applied"
            print(f"[FIRMWARE] MERGE_CONFLICT DETECTED at {self.pos_x},{self.pos_y} ({trap_name})")
            
            # 1. Trigger V6 Contradiction (The "Vanish" Protocol)
            event = handle_npc_contradiction(
                npc=self,
                broken_rule="never_fail_maintenance", # The trap proves maintenance failed
                cloud=cloud,
                zones={}
            )
            
            # 2. Apply Firmware Failure State
            self._stun_timer = 5.0
            self.current_state = NPCState.CONTRADICTION
            
            # 3. Resolve Conflict (Clear Trap)
            print(f"[FIRMWARE] Resolving Conflict... Construct {trap_name} DELETED.")
            tile.construct = None

    def attempt_maintenance_build(self):
        """
        The Janitor can also BUILD. 
        e.g., Placed a 'DOOR_JAM' to lock a route (Maintenance Mode).
        """
        # Get context for PFDL
        tile = self.grid.get_tile(self.pos_x, self.pos_y)
        grid_state = {
            "tile_type": tile.type,
            "light_level": tile.light_level,
            "has_construct": tile.construct is not None
        }

        # Attempt to build a Lock (Door Jam)
        result = self.firmware.attempt_construct("DOOR_JAM", self.resources, grid_state)
        
        if result.success:
            tile.construct = {"name": "MAINTENANCE_LOCK"}
            print(f"[JANITOR] BUILDING: Maintenance Lock applied at {self.pos_x},{self.pos_y}")

    def _maintain_patrol(self, dt: float):
        # Placeholder movement
        pass