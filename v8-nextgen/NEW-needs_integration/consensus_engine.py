#!/usr/bin/env python3
"""
CONSENSUS ENGINE v2.1 - CIRCUIT SIMULATOR
Calculates Signal Integrity (SNR) and Voltage for proposed constructs.
"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class ConsensusResult:
    approved: bool
    score: float        # V_out (0.0 - 1.0)
    stability: float    # SNR (Signal-to-Noise Ratio)
    votes: Dict[str, float] 
    reason: str
    reason_code: str = "OK"

class ConsensusEngine:
    def __init__(self):
        self.LOGIC_THRESHOLD = 0.55
        self.RESISTANCE_PER_UNIT = 0.05
        self.DIELECTRIC_WALL = 0.4
        self.CROSSTALK_PENALTY = 0.25
        self.BOOTSTRAP_VOLTAGE = 0.8

    def calculate_consensus(self, 
                          proposal_pos: Tuple[int, int], 
                          ninja_focus: int, 
                          active_swarm: List[Tuple[int, int]], 
                          grid_context: dict) -> ConsensusResult:
        
        # 1. INPUT VOLTAGE (V_in)
        v_in = max(0.0, min(1.0, ninja_focus / 100.0))
        
        # 2. IMPEDANCE (Resistance + Dielectric)
        min_dist = 999.0
        if active_swarm:
            for node in active_swarm:
                d = math.sqrt((node[0]-proposal_pos[0])**2 + (node[1]-proposal_pos[1])**2)
                if d < min_dist: min_dist = d
            trace_resistance = min_dist * self.RESISTANCE_PER_UNIT
        else:
            trace_resistance = 0.0 if v_in >= self.BOOTSTRAP_VOLTAGE else 1.0

        env_impedance = 0.4 if grid_context.get("tile_type") == 1 else 0.0
        total_impedance = trace_resistance + env_impedance

        # 3. NOISE (Cross-talk)
        noise_floor = 0.0
        if active_swarm:
            nearby = 0
            for node in active_swarm:
                d = math.sqrt((node[0]-proposal_pos[0])**2 + (node[1]-proposal_pos[1])**2)
                if d < 2.5: nearby += 1
            if nearby > 1:
                noise_floor = (nearby - 1) * self.CROSSTALK_PENALTY

        # 4. SIMULATION
        signal_loss = total_impedance + noise_floor
        v_out = max(0.0, min(1.0, v_in - signal_loss))
        
        snr = 1.0
        if noise_floor > 0: snr = v_in / (noise_floor + 0.01)
        elif total_impedance > 0.8: snr = 0.2

        # 5. RESULT
        approved = v_out >= self.LOGIC_THRESHOLD
        reason = "CIRCUIT_CLOSED"
        code = "OK"

        if not approved:
            if not active_swarm and v_in < self.BOOTSTRAP_VOLTAGE:
                reason = "FAILURE: Cold Boot Voltage Low"
                code = "COLD_BOOT_LOW"
            elif noise_floor > 0.4:
                reason = "FAILURE: Signal Cross-talk"
                code = "CROSSTALK"
            elif trace_resistance > 0.5:
                reason = "FAILURE: High Impedance"
                code = "HIGH_IMPEDANCE"
            elif env_impedance > 0:
                reason = "FAILURE: Dielectric Blockage"
                code = "DIELECTRIC"
            else:
                reason = "FAILURE: Low Input Voltage"
                code = "LOW_VOLTAGE"

        return ConsensusResult(
            approved=approved,
            score=round(v_out, 3),
            stability=round(snr, 2),
            votes={
                "input_voltage": round(v_in, 2),
                "impedance": round(total_impedance, 2),
                "noise": round(noise_floor, 2)
            },
            reason=reason,
            reason_code=code
        )