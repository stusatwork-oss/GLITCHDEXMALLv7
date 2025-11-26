#!/usr/bin/env python3
"""
GLITCHDEX MALL V2 - MAIN GAME LOOP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A full modern immersive sim wearing a cheap Wolf3D Halloween mask.

The mask slips. You see what's underneath.
It was never retro. It was always cutting-edge.
The simulation was the lie. The systems were always real.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
import os
import time
import math
from typing import Dict, Tuple, Optional

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from mall_simulation import MallSimulation, PlayerState
from world_loader import create_world_config


class GameState:
    """Overall game state"""

    def __init__(self):
        self.running = True
        self.show_menu = False
        self.show_inventory = False
        self.dialogue_active = False
        self.dialogue_text = ""
        self.dialogue_npc = None


class InputHandler:
    """Handles keyboard input"""

    @staticmethod
    def get_input() -> str:
        """Get keyboard input (blocking)"""
        try:
            import sys
            import tty
            import termios

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

            return ch
        except:
            # Fallback for Windows/non-Unix
            return input("Command: ").strip()

    @staticmethod
    def get_non_blocking_input() -> Optional[str]:
        """Get input without blocking (Unix only)"""
        try:
            import select
            if select.select([sys.stdin], [], [], 0.0)[0]:
                return InputHandler.get_input()
            return None
        except:
            return None


class SimpleRenderer:
    """
    Minimal text-based renderer for v2.

    This is a PLACEHOLDER until we adapt wolf_renderer.py.
    Shows basic game state in text form.
    """

    def __init__(self):
        self.width = 80
        self.height = 24

    def render(self, simulation: MallSimulation, render_hints: Dict) -> None:
        """Render the current game state"""
        self.clear_screen()

        # Title
        print("=" * 80)
        print("  GLITCHDEX MALL V2 - IMMERSIVE SIM")
        print("=" * 80)
        print()

        # Player info
        px, py, pz = simulation.player.position
        print(f"Position: ({px}, {py}, {pz}) | Facing: {simulation.player.facing:.1f}°")
        print()

        # Heat level
        current_heat = simulation.heat_system.get_heat_value()
        stars = "★" * int(current_heat) + "☆" * (5 - int(current_heat))
        heat_label = {
            0: "Normal",
            1: "Suspicious",
            2: "Alert",
            3: "Warning",
            4: "Lockdown",
            5: "REALITY BREAK"
        }
        heat_name = heat_label.get(int(current_heat), "Unknown")
        print(f"Heat: {stars} ({heat_name})")
        print()

        # Reality stability
        stability = render_hints.get("reality_stability", 100)
        print(f"Reality Stability: {stability}%")
        print()

        # NPCs nearby (within 5 tiles)
        nearby_npcs = []
        for npc in simulation.npc_manager.npcs.values():
            nx, ny, nz = npc.position
            dist = math.sqrt((px - nx)**2 + (py - ny)**2)
            if dist < 10:
                nearby_npcs.append((npc, dist))

        if nearby_npcs:
            print("Nearby NPCs:")
            for npc, dist in sorted(nearby_npcs, key=lambda x: x[1])[:5]:
                nx, ny, nz = npc.position
                awareness = simulation.stealth_system.get_npc_awareness(npc.id)
                alert_symbol = ""
                if awareness > 0.8:
                    alert_symbol = "!"
                elif awareness > 0.5:
                    alert_symbol = "!!"
                elif awareness > 0.3:
                    alert_symbol = "?"

                print(f"  - {npc.name} {alert_symbol} at ({nx}, {ny}) - {dist:.1f} tiles away")
        print()

        # Active glitches
        active_glitches = render_hints.get("active_glitches", [])
        if active_glitches:
            print("GLITCHES:")
            for glitch in active_glitches[:3]:
                print(f"  [{glitch['type'].upper()}] {glitch['description']}")
            print()

        # Renderer strain
        strain_info = render_hints.get("renderer_strain", {})
        if strain_info:
            fake_fps = strain_info.get("fake_fps", 60)
            strain_level = strain_info.get("level", "stable")
            print(f"FPS: {fake_fps} | Renderer: {strain_level.upper()}")

            # Show error messages if strain is high
            errors = strain_info.get("active_errors", [])
            if errors:
                print()
                print("ERROR MESSAGES:")
                for error in errors[:5]:
                    print(f"  {error}")
            print()

        # Toddler visibility
        toddler_info = render_hints.get("toddler", {})
        if toddler_info.get("visible", False):
            tx = toddler_info.get("x", 0)
            ty = toddler_info.get("y", 0)
            symbol = toddler_info.get("symbol", "☺")
            print(f"TODDLER {symbol} at ({tx}, {ty})")
            print()

        # Controls
        print("-" * 80)
        print("Controls: W/S (forward/back) | A/D (turn) | E (interact) | I (inventory) | Q (quit)")
        print("-" * 80)

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')


class Game:
    """Main game controller"""

    def __init__(self):
        print("Initializing GLITCHDEX MALL V2...")
        print()

        # Load world data
        print("[GAME] Loading world data...")
        world_config = create_world_config()

        # Convert world grid to tiles dict for simulation
        world_tiles = {}
        for (x, y), tile_data in world_config['world_grid'].tiles.items():
            world_tiles[(x, y, 0)] = tile_data

        # Initialize simulation with world
        print()
        self.simulation = MallSimulation(world_tiles, world_config)
        print()

        # Set player spawn position
        spawn_x, spawn_y = world_config['world_grid'].get_random_position("ENTRANCE")
        if (spawn_x, spawn_y, 0) not in world_tiles:
            spawn_x, spawn_y = 25, 25  # Fallback to center
        self.simulation.player.position = (spawn_x, spawn_y, 0)

        # Game state
        self.state = GameState()

        # Renderer (simple text for now)
        self.renderer = SimpleRenderer()

        # Timing
        self.last_frame_time = time.time()
        self.target_fps = 10  # Low FPS for text rendering

        print("[GAME] Initialization complete!")
        print()
        input("Press ENTER to start...")

    def handle_input(self, key: str) -> bool:
        """
        Handle player input.
        Returns False if game should quit.
        """
        key = key.lower()

        # Build player action dict
        player_action = None

        if key == 'q':
            return False

        elif key in ['w', 'W']:
            # Move forward based on facing
            facing_rad = math.radians(self.simulation.player.facing)
            dx = math.cos(facing_rad)
            dy = math.sin(facing_rad)

            old_pos = self.simulation.player.position
            new_x = int(old_pos[0] + dx)
            new_y = int(old_pos[1] + dy)

            # Check if walkable
            if (new_x, new_y, 0) in self.simulation.world_tiles:
                if self.simulation.world_tiles[(new_x, new_y, 0)].walkable:
                    self.simulation.player.position = (new_x, new_y, 0)

                    player_action = {
                        "type": "move",
                        "old_position": old_pos,
                        "new_position": (new_x, new_y, 0)
                    }

        elif key in ['s', 'S']:
            # Move backward
            facing_rad = math.radians(self.simulation.player.facing)
            dx = -math.cos(facing_rad)
            dy = -math.sin(facing_rad)

            old_pos = self.simulation.player.position
            new_x = int(old_pos[0] + dx)
            new_y = int(old_pos[1] + dy)

            if (new_x, new_y, 0) in self.simulation.world_tiles:
                if self.simulation.world_tiles[(new_x, new_y, 0)].walkable:
                    self.simulation.player.position = (new_x, new_y, 0)

                    player_action = {
                        "type": "move",
                        "old_position": old_pos,
                        "new_position": (new_x, new_y, 0)
                    }

        elif key in ['a', 'A']:
            # Turn left
            self.simulation.player.facing = (self.simulation.player.facing - 45) % 360

        elif key in ['d', 'D']:
            # Turn right
            self.simulation.player.facing = (self.simulation.player.facing + 45) % 360

        elif key in ['e', 'E']:
            # Interact
            player_action = {
                "type": "interact",
                "position": self.simulation.player.position
            }

        elif key in ['i', 'I']:
            # Toggle inventory
            self.state.show_inventory = not self.state.show_inventory

        return True, player_action

    def run(self):
        """Main game loop"""
        self.state.running = True

        print()
        print("Game started! Use WASD to move, E to interact, Q to quit.")
        time.sleep(1)

        try:
            while self.state.running:
                # Calculate delta time
                current_time = time.time()
                dt = current_time - self.last_frame_time
                self.last_frame_time = current_time

                # Get input (non-blocking)
                key = InputHandler.get_non_blocking_input()
                player_action = None

                if key:
                    result = self.handle_input(key)
                    if isinstance(result, tuple):
                        should_continue, player_action = result
                        if not should_continue:
                            break
                    elif not result:
                        break

                # Update simulation
                render_hints = self.simulation.update(dt, player_action)

                # Render
                self.renderer.render(self.simulation, render_hints)

                # Frame rate limiting
                time.sleep(1.0 / self.target_fps)

        except KeyboardInterrupt:
            print("\n\nGame interrupted!")

        print()
        print("Thanks for playing GLITCHDEX MALL V2!")
        print("The toddler is waiting for you...")


def main():
    """Entry point"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"\n[ERROR] Game crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
