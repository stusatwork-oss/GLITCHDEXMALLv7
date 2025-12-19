#!/usr/bin/env python3
"""
CLOUD FLOCKING SYSTEM
Simulates "Cloud Persons" (Attention Nodes) as signal-seeking particles.

Logic:
1. Particles scan the Grid for Active Constructs (Circuit Nodes).
2. They calculate the 'Field Strength' (Consensus Score) and 'coherence' (Stability) of nearby nodes.
3. Movement Vector = (Attraction to Voltage) * (Stability Coefficient).

Result:
- High SNR builds -> Form dense, stable clumps (Safe zones).
- Low SNR builds -> Particles drift erratically or dissipate (Chaos/Wattitude spike).
"""

import math
import random
from typing import List, Tuple, Dict

class CloudParticle:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.stability_lock = 0.0  # 0.0 = Free, 1.0 = Bound to circuit

class CloudFlock:
    def __init__(self, width, height, count=20):
        self.width = width
        self.height = height
        self.particles = [CloudParticle(random.randint(0, width), random.randint(0, height)) for _ in range(count)]
        self.field_strength = {} # (x,y) -> {score, stability}

    def update_field(self, active_constructs: Dict[Tuple[int,int], dict]):
        """
        Updates the attractive field based on the Ninja's circuit.
        active_constructs values should ideally contain cached consensus metrics.
        """
        self.field_strength = {}
        for pos, data in active_constructs.items():
            # In a real impl, we'd query the ConsensusEngine for these values per node
            # For now, we simulate 'hot' nodes
            self.field_strength[pos] = {
                "score": data.get("voltage", 0.8),    # Attraction
                "stability": data.get("snr", 1.2)     # Binding
            }

    def tick(self):
        """Update particle positions."""
        for p in self.particles:
            # 1. Calculate Pull Vector
            dx, dy = 0.0, 0.0
            best_stability = 0.0
            
            for node_pos, metrics in self.field_strength.items():
                dist = math.sqrt((node_pos[0] - p.x)**2 + (node_pos[1] - p.y)**2)
                
                if dist < 0.1: dist = 0.1 # Clamp
                
                if dist < 8.0: # Sensing range
                    # Attraction = Voltage / Distance
                    force = (metrics["score"] * 2.0) / (dist * 1.5)
                    
                    # Direction
                    dir_x = (node_pos[0] - p.x) / dist
                    dir_y = (node_pos[1] - p.y) / dist
                    
                    dx += dir_x * force
                    dy += dir_y * force
                    
                    # Check for binding (if very close)
                    if dist < 1.5:
                        best_stability = max(best_stability, metrics["stability"])

            # 2. Apply Movement
            # If stability is high, we "lock" (move less)
            movement_factor = 1.0
            if best_stability > 1.0:
                movement_factor = 0.1 # Bound state
                p.stability_lock = min(1.0, p.stability_lock + 0.1)
            else:
                p.stability_lock = max(0.0, p.stability_lock - 0.1)
                # Add drift noise if unstable
                dx += (random.random() - 0.5) * 0.5
                dy += (random.random() - 0.5) * 0.5

            p.x += dx * movement_factor
            p.y += dy * movement_factor
            
            # Boundary Clamp
            p.x = max(0, min(self.width, p.x))
            p.y = max(0, min(self.height, p.y))

    def get_density_at(self, x, y, radius=2.0) -> int:
        """Returns number of particles near a point."""
        count = 0
        for p in self.particles:
            if math.sqrt((p.x - x)**2 + (p.y - y)**2) < radius:
                count += 1
        return count