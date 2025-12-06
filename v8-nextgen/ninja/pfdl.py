#!/usr/bin/env python3
"""
PFDL KERNEL v2.2
Interprets Consensus Logic into Firmware Feedback.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from ninja.consensus_engine import ConsensusEngine

DEFAULT_FIRMWARE = {
    "firmware_id": "FW_NINJA_SABOTEUR_v2.2",
    "micro_constructs": {
        "SMOKE_PELLET": {
            "req": "SHADOW_CELL", "cost": 10, "slots": 1, 
            "voxel_ref": "NINJA_SMOKE", "signal": "stealth_action"
        },
        "IMPROVISED_COVER": {
            "req": "FLAT_SURFACE", "cost": 5, "slots": 0,
            "voxel_ref": "TRASH_CAN", "signal": "recycler_used" 
        },
        "MESS_LURE_B": {
            "req": "FLAT_SURFACE", "cost": 3, "slots": 0,
            "voxel_ref": "SLURPEE_CUP", "signal": "slushee_purchased"
        },
        "COIN_TOSS": {
            "req": "ANY_FLOOR", "cost": 2, "slots": 0,
            "voxel_ref": "ARCADE_TOKEN", "signal": "token_drop"
        }
    }
}

@dataclass
class ConstructResult:
    success: bool
    phase: str
    cost_focus: int = 0
    message: str = ""
    signal: str = "NONE"
    voxel_id: str = None
    circuit_metrics: dict = None

class PFDLKernel:
    def __init__(self, agent_id: str):
        self.fw = DEFAULT_FIRMWARE
        self.circuit_sim = ConsensusEngine()

    def process_proposal(self, construct_key, resources, grid_ctx, swarm_pos, target_pos) -> ConstructResult:
        c_def = self.fw["micro_constructs"].get(construct_key)
        
        # 1. LOGIC
        if not c_def: return ConstructResult(False, "LOGIC", message="UNKNOWN_OPCODE")
        if resources["focus"] < c_def["cost"]: return ConstructResult(False, "LOGIC", message="INSUFFICIENT_FOCUS")
        if not self._check_geo(c_def.get("req"), grid_ctx):
             return ConstructResult(False, "LOGIC", message=f"GEOMETRY_MISMATCH: {c_def['req']}")

        # 2. CIRCUIT
        sim = self.circuit_sim.calculate_consensus(target_pos, resources["focus"], swarm_pos, grid_ctx)
        
        if not sim.approved:
            msg_map = {
                "CROSSTALK": "REJECTED: Signal Noise High. Spread out.",
                "HIGH_IMPEDANCE": "REJECTED: Trace too long. Move closer.",
                "DIELECTRIC": "REJECTED: Wall blockage.",
                "COLD_BOOT_LOW": "REJECTED: Cold Boot needs >80 Focus.",
                "LOW_VOLTAGE": "REJECTED: Focus too low for current resistance."
            }
            return ConstructResult(False, "CIRCUIT", message=msg_map.get(sim.reason_code, sim.reason), circuit_metrics=sim.votes)

        # 3. MANIFEST
        return ConstructResult(True, "COMPLETE", 
                             cost_focus=c_def["cost"], 
                             cost_slots=c_def["slots"],
                             message=f"MANIFESTED: {construct_key} [V:{sim.score:.2f} SNR:{sim.stability:.1f}]",
                             signal=c_def.get("signal", "NONE"),
                             voxel_id=c_def.get("voxel_ref"),
                             circuit_metrics=sim.votes)

    def _check_geo(self, req, ctx):
        if req == "SHADOW_CELL": return ctx.get("light_level", 1.0) == 0.0
        return ctx.get("tile_type") == 0