#!/usr/bin/env python3
"""
V5 MEASUREMENTS BRIDGE - UPDATED (Source: v7 JSONs)
Reflects 'zone_measurements.json' and 'feature_measurements.json'.
"""

class V5Specs:
    # Scale Constants
    TILE_SIZE_FEET = 3.0  # 1 Grid Tile = 3x3 feet
    
    # Z4 FOOD COURT SPECIFIC (Updated)
    # Source: zone_measurements.json -> Z4_FOOD_COURT -> diameter_feet: 100
    Z4_DIAMETER_FEET = 100.0 
    
    # Grid Calculation: 100ft / 3ft = 33.3 tiles. 
    # We add padding for the "Rim" walkway (Z3 Lower Ring adjacencies).
    # Let's make the board 40x40 to encompass the 100ft bowl comfortably.
    Z4_GRID_SIZE = 40 
    
    # The Pit is the bowl itself. Radius = 50ft = ~16.5 tiles.
    Z4_PIT_RADIUS_TILES = 16
    
    # Source: spatial_measurements.json -> vertical_levels -> z_minus_1
    Z4_PIT_DEPTH_TILES = -1  # Represents the 8ft drop
    
    # Source: feature_measurements.json -> glass_blocks
    # 22.5 feet arc length / 3ft tile = ~7.5 tiles
    Z4_GLASS_WALL_LENGTH_TILES = 8 
    
    # Source: feature_measurements.json -> escalator_steps
    # 12 steps -> ~8ft run horizontal -> ~3 tiles
    Z4_ESCALATOR_RUN_TILES = 3
    
    # Source: feature_measurements.json -> neon_sign_food_court
    # Diameter 7ft -> ~2.3 tiles
    Z4_NEON_SIGN_DIAMETER_TILES = 2

    @staticmethod
    def get_feature_tiles(feature_name):
        if feature_name == "VENDING_MACHINE":
            # 39" x 72" -> ~1x2 tiles
            return (1, 2)
        return (1, 1)