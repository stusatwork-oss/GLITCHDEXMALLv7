#!/usr/bin/env python3
"""
EASTLAND MALL V3 - PYGAME VERSION
Full graphical raycaster with AI systems.

The 30,000 HP engine finally has a body.
"""

import sys
import os
import json
import math
import time
import random

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

import pygame
from pygame_renderer import PygameRaycaster

# Import AI systems
try:
    from mall_simulation import MallSimulation
    AI_AVAILABLE = True
except ImportError as e:
    print(f"[WARN] AI systems not available: {e}")
    AI_AVAILABLE = False


# Helper for random_int used by simulation
def random_int(a, b):
    return random.randint(a, b)

# Inject into mall_simulation module if needed
import builtins
builtins.random_int = random_int


class Tile:
    """Simple tile class for simulation compatibility."""
    def __init__(self, tile_type: str, walkable: bool, description: str = ""):
        self.type = tile_type
        self.walkable = walkable
        self.description = description


class EastlandPygame:
    """Main game controller with Pygame renderer and full AI simulation."""

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

        # Player state
        self.player_x = 11.0  # West entrance
        self.player_y = 45.0
        self.player_z = 0
        self.player_angle = 0.0  # Radians, facing east

        # Movement settings
        self.move_speed = 0.08
        self.turn_speed = 0.04

        # Game state
        self.heat_level = 0.0
        self.running = False
        self.last_frame_time = time.time()

        # World data
        self.world_tiles = {}
        self.world_tiles_raw = {}  # For renderer (dict format)
        self.npcs = []
        self.artifacts = []

        # AI Simulation
        self.simulation = None
        self.render_hints = {}

        # Player action tracking
        self.player_action = None

        # NPC positions for rendering
        self.npc_positions = []

        # Renderer
        self.renderer = None

    def load_game(self):
        """Load all game data."""
        print("Loading Eastland Mall V3...")

        # Load mall map
        try:
            map_path = os.path.join(self.data_dir, 'mall_map.json')
            with open(map_path, 'r') as f:
                map_data = json.load(f)

            # Convert to world tiles (two formats)
            for tile in map_data.get('tiles', []):
                x, y, z = tile['x'], tile['y'], tile.get('z', 0)
                tile_type = tile['type']
                walkable = tile_type not in ['VOID']
                description = tile.get('description', '')

                # Raw dict format for renderer
                self.world_tiles_raw[(x, y, z)] = {
                    'type': tile_type,
                    'description': description,
                    'walkable': walkable
                }

                # Tile object format for simulation
                self.world_tiles[(x, y, z)] = Tile(tile_type, walkable, description)

            print(f"  [OK] Map loaded: {len(self.world_tiles)} tiles")

        except Exception as e:
            print(f"  [ERROR] Failed to load map: {e}")
            return False

        # Load NPCs
        try:
            entities_path = os.path.join(self.data_dir, 'entities.json')
            with open(entities_path, 'r') as f:
                entities_data = json.load(f)
            self.npcs = entities_data.get('npcs', [])
            print(f"  [OK] NPCs loaded: {len(self.npcs)}")
        except Exception as e:
            print(f"  [WARN] NPCs: {e}")

        # Load artifacts
        try:
            artifacts_path = os.path.join(self.data_dir, 'artifacts.json')
            with open(artifacts_path, 'r') as f:
                artifacts_data = json.load(f)
            self.artifacts = artifacts_data.get('artifacts', [])
            print(f"  [OK] Artifacts loaded: {len(self.artifacts)}")
        except Exception as e:
            print(f"  [WARN] Artifacts: {e}")

        # Initialize AI simulation
        if AI_AVAILABLE:
            try:
                print("\n[SIMULATION] Initializing AI systems...")
                self.simulation = MallSimulation(self.world_tiles)
                # Set initial player position in simulation
                self.simulation.player.position = (int(self.player_x), int(self.player_y), self.player_z)
                self.simulation.player.facing = math.degrees(self.player_angle)
                print("[SIMULATION] All systems online. The engine is running.")
            except Exception as e:
                print(f"[WARN] Simulation init failed: {e}")
                import traceback
                traceback.print_exc()
                self.simulation = None
        else:
            print("[INFO] Running without AI simulation")

        print("\nLoading complete!")
        return True

    def is_walkable(self, x: float, y: float) -> bool:
        """Check if position is walkable."""
        tile = self.world_tiles.get((int(x), int(y), self.player_z))
        if tile:
            return tile.walkable if hasattr(tile, 'walkable') else tile.get('walkable', False)
        return False

    def handle_input(self, inputs: dict):
        """Handle player input and track actions for simulation."""
        old_pos = (int(self.player_x), int(self.player_y), self.player_z)
        self.player_action = None

        # Rotation
        if inputs['left']:
            self.player_angle -= self.turn_speed
        if inputs['right']:
            self.player_angle += self.turn_speed

        # Forward/backward movement
        moved = False
        if inputs['forward']:
            new_x = self.player_x + math.cos(self.player_angle) * self.move_speed
            new_y = self.player_y + math.sin(self.player_angle) * self.move_speed
            if self.is_walkable(new_x, new_y):
                self.player_x, self.player_y = new_x, new_y
                moved = True

        if inputs['backward']:
            new_x = self.player_x - math.cos(self.player_angle) * self.move_speed
            new_y = self.player_y - math.sin(self.player_angle) * self.move_speed
            if self.is_walkable(new_x, new_y):
                self.player_x, self.player_y = new_x, new_y
                moved = True

        # Strafing
        if inputs['strafe_left']:
            strafe_angle = self.player_angle - math.pi / 2
            new_x = self.player_x + math.cos(strafe_angle) * self.move_speed
            new_y = self.player_y + math.sin(strafe_angle) * self.move_speed
            if self.is_walkable(new_x, new_y):
                self.player_x, self.player_y = new_x, new_y
                moved = True

        if inputs['strafe_right']:
            strafe_angle = self.player_angle + math.pi / 2
            new_x = self.player_x + math.cos(strafe_angle) * self.move_speed
            new_y = self.player_y + math.sin(strafe_angle) * self.move_speed
            if self.is_walkable(new_x, new_y):
                self.player_x, self.player_y = new_x, new_y
                moved = True

        # Track movement action
        if moved:
            new_pos = (int(self.player_x), int(self.player_y), self.player_z)
            if new_pos != old_pos:
                self.player_action = {
                    "type": "move",
                    "old_position": old_pos,
                    "new_position": new_pos
                }

        # Interaction
        if inputs['interact']:
            self.handle_interaction()
            self.player_action = {
                "type": "interact",
                "position": (int(self.player_x), int(self.player_y), self.player_z)
            }

        # Heat adjustment (for testing - press H to increase, bypasses simulation)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_h]:
            if self.simulation:
                self.simulation.heat_system.add_heat(0.5)
            else:
                self.heat_level = min(5, self.heat_level + 0.02)
        if keys[pygame.K_g]:
            if self.simulation:
                self.simulation.heat_system.reduce_heat(0.5)
            else:
                self.heat_level = max(0, self.heat_level - 0.02)

        # Z-level changes
        tile = self.world_tiles.get((int(self.player_x), int(self.player_y), self.player_z))
        if tile:
            tile_type = tile.type if hasattr(tile, 'type') else tile.get('type', '')
            if tile_type == 'RAMP_DOWN' and keys[pygame.K_SPACE]:
                self.player_z = -1
                self.player_y += 2  # Move into food court
            elif self.player_z < 0 and keys[pygame.K_SPACE]:
                # Check if near ramp
                if int(self.player_y) <= 60:
                    self.player_z = 0
                    self.player_y = 58

    def handle_interaction(self):
        """Handle E key interaction."""
        # Check what's in front of player
        check_x = int(self.player_x + math.cos(self.player_angle) * 1.5)
        check_y = int(self.player_y + math.sin(self.player_angle) * 1.5)

        tile = self.world_tiles.get((check_x, check_y, self.player_z))
        if tile:
            tile_type = tile.get('type', '')

            # Special interactions
            if 'HARD_COPY' in tile_type:
                print("HARD COPY - Arcade cabinet glows invitingly...")
                # Could launch pong here

    def game_loop(self):
        """Main game loop."""
        while self.running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - self.last_frame_time
            self.last_frame_time = current_time

            # Handle events and input
            self.running, inputs = self.renderer.handle_events()

            if inputs['quit']:
                self.running = False
                break

            # Handle movement and interaction
            self.handle_input(inputs)

            # Update AI simulation
            if self.simulation:
                # Sync player position to simulation
                self.simulation.player.position = (int(self.player_x), int(self.player_y), self.player_z)
                self.simulation.player.facing = math.degrees(self.player_angle) % 360

                # Update all AI systems
                self.render_hints = self.simulation.update(dt, self.player_action)

                # Extract heat level from simulation
                self.heat_level = self.render_hints.get('heat_level', 0)

                # Get NPC positions for rendering
                npc_states = self.render_hints.get('npcs', {})
                self.npc_positions = []
                for npc_id, npc_data in npc_states.items():
                    if isinstance(npc_data, dict) and 'position' in npc_data:
                        pos = npc_data['position']
                        self.npc_positions.append({
                            'id': npc_id,
                            'x': pos[0],
                            'y': pos[1],
                            'z': pos[2] if len(pos) > 2 else 0,
                            'name': npc_data.get('name', npc_id)
                        })

            # Render
            self.renderer.render(
                self.player_x,
                self.player_y,
                self.player_z,
                self.player_angle,
                self.world_tiles,
                self.heat_level,
                self.npcs,
                self.render_hints if self.simulation else {}
            )

    def run(self):
        """Main entry point."""
        # Load game data
        if not self.load_game():
            print("Failed to load game!")
            return

        print("\nStarting Eastland Mall...")
        print("Controls: WASD to move, Mouse/Arrows to look")
        print("H/G: Increase/Decrease heat (testing)")
        print("SPACE: Use ramps")
        print("Q/ESC: Quit\n")

        # Initialize renderer
        self.renderer = PygameRaycaster(1024, 768)

        # Start game loop
        self.running = True
        try:
            self.game_loop()
        finally:
            self.renderer.cleanup()

        print("\nYou leave Eastland Mall.")
        print("The fluorescent lights continue to flicker.")
        print("Nothing changes.")


def main():
    """Entry point."""
    try:
        game = EastlandPygame()
        game.run()
    except Exception as e:
        print(f"\n[ERROR] Game crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
