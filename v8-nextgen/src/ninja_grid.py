#!/usr/bin/env python3
"""
NINJA GRID SYSTEM v1.4 - 100ft SCALE UPDATE
Reflects new Z4 dimensions (100ft diameter bowl).
"""

import math
from typing import List, Dict, Optional
from dataclasses import dataclass
import sys
from pathlib import Path

# Add src root
sys.path.append(str(Path(__file__).parents[2]))

# 1. Import V5 Specs
try:
    from ninja.measurements_v5 import V5Specs
except ImportError:
    # Fallback default
    class V5Specs:
        Z4_GRID_SIZE = 40
        Z4_PIT_RADIUS_TILES = 16
        Z4_PIT_DEPTH_TILES = -1
        Z4_GLASS_WALL_LENGTH_TILES = 8
        Z4_ESCALATOR_RUN_TILES = 3

@dataclass
class Tile:
    x: int
    y: int
    # Types: 0=FLOOR, 1=WALL, 2=DOOR, 3=VOID, 4=GLASS_BLOCK, 5=ESCALATOR, 6=NEON_SIGN_ANCHOR
    type: int  
    z_level: int = 0  # 0=Rim, -1=Pit
    light_level: float = 0.0
    construct: Optional[dict] = None

class NinjaGrid:
    def __init__(self, zone_id: str = "Z4_FOOD_COURT"):
        self.zone_id = zone_id
        
        # New Dimensions (40x40 tiles = 120x120 ft coverage)
        self.width = V5Specs.Z4_GRID_SIZE
        self.height = V5Specs.Z4_GRID_SIZE
        self.tiles: List[List[Tile]] = []
        
        self._build_food_court_v5()
        print(f"[GRID] Generated {zone_id} at 100ft Scale ({self.width}x{self.height} tiles)")

    def _build_food_court_v5(self):
        """
        Reconstructs Z4 Bowl at 100ft scale.
        """
        cx, cy = self.width // 2, self.height // 2
        pit_radius = V5Specs.Z4_PIT_RADIUS_TILES  # 16 tiles

        for y in range(self.height):
            row = []
            for x in range(self.width):
                dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                t_type = 0
                z_level = 0
                
                # The Pit (Z-1)
                # The bowl is now massive (32 tiles wide)
                if dist < pit_radius:
                    z_level = V5Specs.Z4_PIT_DEPTH_TILES
                
                # Perimeter Walls (The Rim Edge)
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    t_type = 1
                
                row.append(Tile(x, y, t_type, z_level))
            self.tiles.append(row)

        # FEATURE: Glass Block Wall (North Rim)
        # 22.5ft arc / 3ft = ~8 tiles.
        wall_len = V5Specs.Z4_GLASS_WALL_LENGTH_TILES
        start_x = cx - (wall_len // 2)
        wall_y = 2 # North side, Rim level
        for i in range(wall_len):
            if 0 <= start_x + i < self.width:
                self.tiles[wall_y][start_x + i].type = 4 

        # FEATURE: Escalators (East/West)
        # Connects Rim (Z0) to Pit (Z-1)
        # Run length 3 tiles
        run_len = V5Specs.Z4_ESCALATOR_RUN_TILES
        esc_y = cy
        
        # West Escalator (entering pit)
        start_x_west = (cx - pit_radius) - 1
        for i in range(run_len + 2): # Extended slightly for landing
             tx = start_x_west + i
             if 0 <= tx < self.width:
                 self.tiles[esc_y][tx].type = 5 # ESCALATOR
        
        # FEATURE: Neon Sign (Suspended over South Entrance)
        # In a 2D top-down, this might act as an obstacle or just a landmark
        # Placed South Rim
        sign_y = self.height - 5
        self.tiles[sign_y][cx].type = 6 # NEON SIGN ANCHOR
        # Just cosmetic for now, but technically blocks light?

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def calculate_lighting(self, sources):
        for row in self.tiles:
            for t in row: t.light_level = 0.0
            
        for (lx, ly, radius) in sources:
            min_x, max_x = max(0, int(lx - radius)), min(self.width, int(lx + radius + 1))
            min_y, max_y = max(0, int(ly - radius)), min(self.height, int(ly + radius + 1))
            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    if math.sqrt((x-lx)**2 + (y-ly)**2) <= radius:
                        if self._los(lx, ly, x, y):
                            self.tiles[y][x].light_level = 1.0

    def _los(self, x0, y0, x1, y1):
        points = []
        dx = abs(x1 - x0); dy = abs(y1 - y0)
        x, y = int(x0), int(y0)
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        
        if dx > dy:
            err = dx / 2.0
            while x != x1:
                points.append((x,y)); err -= dy
                if err < 0: y += sy; err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                points.append((x,y)); err -= dx
                if err < 0: x += sx; err += dy
                y += sy
                
        for (px, py) in points:
            if (px==x0 and py==y0) or (px==x1 and py==y1): continue
            t = self.get_tile(px, py)
            # Wall(1) and Glass(4) block light. Escalator(5) and Sign(6) do not?
            if t and (t.type == 1 or t.type == 4): return False
        return True