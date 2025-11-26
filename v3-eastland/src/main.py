#!/usr/bin/env python3
"""
GLITCHDEX MALL V3 - EASTLAND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A dying mall from the late 80s. Stranger Things meets dead mall.
Full AI simulation hidden under retro Wolf3D aesthetics.

The fluorescent lights flicker. The slushee machine hums.
Something is wrong here.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
import os
import time
import json
import math
from typing import Dict, Tuple, Optional

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from mall_simulation import MallSimulation, PlayerState
from world_loader import WorldLoader
from pong import play_pong


class EastlandGame:
    """Main game controller for Eastland Mall V3."""

    # ANSI Colors
    RESET = "\033[0m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    DIM = "\033[2m"
    BRIGHT = "\033[1m"

    def __init__(self):
        self.running = False
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

        # Game state
        self.player_x = 10  # West entrance
        self.player_y = 45
        self.player_z = 0
        self.player_facing = 0  # Degrees, 0 = East

        # World data
        self.world_config = None
        self.world_tiles = {}
        self.simulation = None

        # Timing
        self.last_frame_time = time.time()
        self.target_fps = 10

    def clear_screen(self):
        """Clear terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')

    def load_game(self):
        """Load all game data and initialize systems."""
        print(f"{self.CYAN}Loading Eastland Mall...{self.RESET}")
        print()

        # Load mall map
        try:
            map_path = os.path.join(self.data_dir, 'mall_map.json')
            with open(map_path, 'r') as f:
                map_data = json.load(f)
            print(f"{self.GREEN}  [OK] Mall map loaded ({map_data['width']}x{map_data['height']}){self.RESET}")

            # Convert to world tiles
            for tile in map_data.get('tiles', []):
                x, y, z = tile['x'], tile['y'], tile.get('z', 0)
                self.world_tiles[(x, y, z)] = {
                    'type': tile['type'],
                    'description': tile.get('description', ''),
                    'walkable': tile['type'] not in ['VOID']
                }

        except Exception as e:
            print(f"{self.RED}  [ERROR] Failed to load map: {e}{self.RESET}")
            return False

        # Load stores
        try:
            stores_path = os.path.join(self.data_dir, 'stores.json')
            with open(stores_path, 'r') as f:
                stores_data = json.load(f)
            print(f"{self.GREEN}  [OK] Stores loaded ({len(stores_data['stores'])} stores){self.RESET}")
        except Exception as e:
            print(f"{self.YELLOW}  [WARN] Stores data: {e}{self.RESET}")

        # Load entities
        try:
            entities_path = os.path.join(self.data_dir, 'entities.json')
            with open(entities_path, 'r') as f:
                entities_data = json.load(f)
            print(f"{self.GREEN}  [OK] Entities loaded ({len(entities_data['npcs'])} NPCs){self.RESET}")
        except Exception as e:
            print(f"{self.YELLOW}  [WARN] Entities data: {e}{self.RESET}")

        # Load artifacts
        try:
            artifacts_path = os.path.join(self.data_dir, 'artifacts.json')
            with open(artifacts_path, 'r') as f:
                artifacts_data = json.load(f)
            print(f"{self.GREEN}  [OK] Artifacts loaded ({len(artifacts_data['artifacts'])} items){self.RESET}")
        except Exception as e:
            print(f"{self.YELLOW}  [WARN] Artifacts data: {e}{self.RESET}")

        print()
        return True

    def show_title(self):
        """Display the title screen."""
        self.clear_screen()

        title = f"""
{self.CYAN}    ██████████████████████████████████████████████████████████
    █                                                        █
    █   ███████  █████  ███████ ████████ ██       █████ ███  █
    █   ██      ██   ██ ██         ██    ██      ██   ██ ██  █
    █   █████   ███████ ███████    ██    ██      ███████ ██  █
    █   ██      ██   ██      ██    ██    ██      ██   ██ ██  █
    █   ███████ ██   ██ ███████    ██    ███████ ██   ██ ██  █
    █                                                        █
    █            M    A    L    L                             █
    █                                                        █
    █                   - V 3 -                               █
    █                                                        █
    ██████████████████████████████████████████████████████████{self.RESET}
        """

        print(title)
        print()
        print(f"{self.DIM}  A dying mall. Late 80s. Something is wrong here.{self.RESET}")
        print()
        print(f"{self.YELLOW}  [ENTER] Enter the mall{self.RESET}")
        print(f"{self.YELLOW}  [Q] Walk away{self.RESET}")
        print()

        choice = input("  > ").strip().lower()
        return choice != 'q'

    def show_intro(self):
        """Display intro text."""
        self.clear_screen()

        intro_lines = [
            "",
            "  You stand at the west entrance of Eastland Mall.",
            "",
            "  The parking lot behind you is nearly empty.",
            "  Through the glass doors, green-tinted light flickers.",
            "  Dead plants line the corridors.",
            "",
            "  This place used to matter to someone.",
            "  Now it just... exists.",
            "",
            "  The food court is sunken below ground level.",
            "  A 6-plex theater sits in its center, screens dark.",
            "",
            "  The door is unlocked. It always is.",
            "",
        ]

        for line in intro_lines:
            print(f"{self.DIM}{line}{self.RESET}")
            time.sleep(0.3)

        print()
        input(f"{self.YELLOW}  [Press ENTER to continue]{self.RESET}")

    def get_current_tile(self):
        """Get the tile at player's current position."""
        return self.world_tiles.get((self.player_x, self.player_y, self.player_z))

    def is_walkable(self, x, y, z=0):
        """Check if a tile is walkable."""
        tile = self.world_tiles.get((x, y, z))
        return tile and tile.get('walkable', False)

    def describe_location(self):
        """Describe the current location."""
        tile = self.get_current_tile()

        print()
        if tile:
            tile_type = tile.get('type', 'UNKNOWN')
            description = tile.get('description', '')

            # Color code by tile type
            if 'STORE' in tile_type:
                color = self.GREEN
            elif tile_type in ['FOOD_COURT', 'THEATER_LOBBY', 'THEATER_SCREEN_1']:
                color = self.YELLOW
            elif tile_type in ['SERVICE_HALL', 'RESTROOM']:
                color = self.DIM
            elif tile_type == 'ANCHOR_STORE':
                color = self.MAGENTA
            else:
                color = self.CYAN

            print(f"{color}  [{tile_type}]{self.RESET}")
            if description:
                print(f"  {description}")

            # Special prompts
            if 'HARD_COPY' in tile_type and self.player_y == 50:
                print(f"\n{self.MAGENTA}  A Pong cabinet glows here. Type 'play' to use it.{self.RESET}")
        else:
            print(f"{self.DIM}  Void. You shouldn't be here.{self.RESET}")

        print()

    def show_help(self):
        """Show help information."""
        print()
        print(f"{self.CYAN}  COMMANDS:{self.RESET}")
        print(f"  {self.GREEN}n/s/e/w{self.RESET}   - Move north/south/east/west")
        print(f"  {self.GREEN}look{self.RESET}      - Describe current location")
        print(f"  {self.GREEN}map{self.RESET}       - Show minimap")
        print(f"  {self.GREEN}play{self.RESET}      - Use arcade cabinet (at HARD COPY)")
        print(f"  {self.GREEN}inv{self.RESET}       - Check inventory")
        print(f"  {self.GREEN}help{self.RESET}      - Show this help")
        print(f"  {self.GREEN}quit{self.RESET}      - Exit game")
        print()

    def show_minimap(self):
        """Show a simple ASCII minimap."""
        print()
        print(f"{self.CYAN}  MINIMAP (30x20 view):{self.RESET}")
        print()

        # Draw a 30x20 view centered on player
        view_width = 30
        view_height = 15
        half_w = view_width // 2
        half_h = view_height // 2

        for dy in range(-half_h, half_h + 1):
            row = "  "
            for dx in range(-half_w, half_w + 1):
                x = self.player_x + dx
                y = self.player_y + dy

                if dx == 0 and dy == 0:
                    row += f"{self.YELLOW}@{self.RESET}"
                elif (x, y, self.player_z) in self.world_tiles:
                    tile = self.world_tiles[(x, y, self.player_z)]
                    tile_type = tile['type']

                    if tile_type == 'CORRIDOR':
                        row += f"{self.DIM}.{self.RESET}"
                    elif tile_type == 'ENTRANCE':
                        row += f"{self.CYAN}E{self.RESET}"
                    elif 'STORE' in tile_type:
                        row += f"{self.GREEN}S{self.RESET}"
                    elif tile_type == 'ANCHOR_STORE':
                        row += f"{self.MAGENTA}A{self.RESET}"
                    elif tile_type == 'FOOD_COURT':
                        row += f"{self.YELLOW}F{self.RESET}"
                    elif 'THEATER' in tile_type:
                        row += f"{self.RED}T{self.RESET}"
                    elif tile_type == 'SERVICE_HALL':
                        row += f"{self.DIM}#{self.RESET}"
                    elif tile_type == 'KIOSK':
                        row += f"{self.CYAN}K{self.RESET}"
                    elif tile_type == 'RAMP_DOWN':
                        row += f"{self.YELLOW}v{self.RESET}"
                    else:
                        row += " "
                else:
                    row += " "
            print(row)

        print()
        print(f"{self.DIM}  Legend: @ You | . Corridor | S Store | A Anchor | F Food Court{self.RESET}")
        print(f"{self.DIM}          T Theater | K Kiosk | E Entrance | v Ramp Down{self.RESET}")
        print()

    def handle_command(self, cmd):
        """Handle player commands."""
        cmd = cmd.lower().strip()

        if cmd in ['q', 'quit', 'exit']:
            return False

        elif cmd in ['n', 'north']:
            if self.is_walkable(self.player_x, self.player_y - 1, self.player_z):
                self.player_y -= 1
                self.describe_location()
            else:
                print(f"\n{self.DIM}  You can't go that way.{self.RESET}")

        elif cmd in ['s', 'south']:
            if self.is_walkable(self.player_x, self.player_y + 1, self.player_z):
                self.player_y += 1
                self.describe_location()
            else:
                print(f"\n{self.DIM}  You can't go that way.{self.RESET}")

        elif cmd in ['e', 'east']:
            if self.is_walkable(self.player_x + 1, self.player_y, self.player_z):
                self.player_x += 1
                self.describe_location()
            else:
                print(f"\n{self.DIM}  You can't go that way.{self.RESET}")

        elif cmd in ['w', 'west']:
            if self.is_walkable(self.player_x - 1, self.player_y, self.player_z):
                self.player_x -= 1
                self.describe_location()
            else:
                print(f"\n{self.DIM}  You can't go that way.{self.RESET}")

        elif cmd in ['d', 'down']:
            # Check for ramp down
            tile = self.get_current_tile()
            if tile and tile.get('type') == 'RAMP_DOWN':
                self.player_z = -1
                self.player_y += 2  # Move to food court
                print(f"\n{self.DIM}  You descend the ramp into the sunken food court...{self.RESET}")
                time.sleep(0.5)
                self.describe_location()
            else:
                print(f"\n{self.DIM}  There's no way down here.{self.RESET}")

        elif cmd in ['u', 'up']:
            if self.player_z < 0:
                # Find ramp back up
                self.player_z = 0
                self.player_y = 58  # Near ramp
                print(f"\n{self.DIM}  You ascend the ramp back to the main level...{self.RESET}")
                time.sleep(0.5)
                self.describe_location()
            else:
                print(f"\n{self.DIM}  There's no way up here.{self.RESET}")

        elif cmd in ['look', 'l']:
            self.describe_location()

        elif cmd in ['play', 'pong', 'arcade']:
            tile = self.get_current_tile()
            if tile and 'HARD_COPY' in tile.get('type', ''):
                play_pong()
                self.clear_screen()
                self.describe_location()
            else:
                print(f"\n{self.DIM}  There's nothing to play here.{self.RESET}")

        elif cmd in ['help', 'h', '?']:
            self.show_help()

        elif cmd in ['map', 'm']:
            self.show_minimap()

        elif cmd in ['inv', 'inventory', 'i']:
            print(f"\n{self.DIM}  Your pockets are empty. For now.{self.RESET}")

        elif cmd == '':
            pass

        else:
            print(f"\n{self.DIM}  Unknown command. Type 'help' for options.{self.RESET}")

        return True

    def game_loop(self):
        """Main game loop."""
        self.describe_location()

        while self.running:
            # Show prompt with position
            z_indicator = f"B{abs(self.player_z)}" if self.player_z < 0 else f"L{self.player_z}"
            print(f"{self.YELLOW}  [{self.player_x},{self.player_y},{z_indicator}]{self.RESET}", end=" ")

            try:
                cmd = input("> ").strip()
            except EOFError:
                break
            except KeyboardInterrupt:
                print()
                break

            # Handle command
            self.running = self.handle_command(cmd)

    def run(self):
        """Main entry point."""
        # Show title screen
        if not self.show_title():
            print(f"\n{self.DIM}  You walk away from the mall.{self.RESET}")
            print(f"{self.DIM}  Probably for the best.{self.RESET}\n")
            return

        # Load game data
        if not self.load_game():
            print(f"\n{self.RED}  Failed to load game data.{self.RESET}")
            return

        time.sleep(1)

        # Show intro
        self.show_intro()

        # Start game loop
        self.running = True
        self.clear_screen()
        self.game_loop()

        # Exit message
        self.clear_screen()
        print()
        print(f"{self.DIM}  You leave Eastland Mall.{self.RESET}")
        print(f"{self.DIM}  The fluorescent lights continue to flicker.{self.RESET}")
        print(f"{self.DIM}  The slushee machine continues to hum.{self.RESET}")
        print(f"{self.DIM}  Nothing changes.{self.RESET}")
        print()


def main():
    """Entry point."""
    try:
        game = EastlandGame()
        game.run()
    except Exception as e:
        print(f"\n[ERROR] Game crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
