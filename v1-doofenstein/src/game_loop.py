"""
DOOFENSTEIN 3D - Main Game Loop
Wolfenstein 3D-style mall crawler
Your weapon is a credit card. The toddler is never visible.
"""

import sys
import time
import os
from typing import List, Tuple, Optional
from mall_engine import MallEngine, Direction
from entities import NPCSystem, ArtifactSystem
from toddler_system import ToddlerSystem
from wolf_renderer import WolfRenderer, Wolf3DHUD, Color
from sprite_system import SpriteRenderer, create_sprite_list_from_game_state
from reality_glitch import RealityGlitch


class Game:
    """Main game controller"""

    def __init__(self):
        """Initialize the game"""
        self.engine = MallEngine()
        self.npc_system = NPCSystem()
        self.artifact_system = ArtifactSystem()
        self.renderer = WolfRenderer(width=120, height=40)
        self.hud = Wolf3DHUD(width=120)
        self.toddler_system = ToddlerSystem()
        self.reality_glitch = RealityGlitch()  # The facade cracks, simulation bleeds through
        self.session_log: List[str] = []
        self.running = False
        self.show_inventory = False
        self.dialogue_active = False
        self.dialogue_npc = None
        self.dialogue_text = ""
        self.last_update_time = time.time()

        self._initialize_artifacts()
        self._log_event("[GAME] Session started at ENTRANCE")

    def _initialize_artifacts(self):
        """Randomly place artifacts around the mall"""
        import random
        artifact_ids = self.artifact_system.get_all_artifact_ids()
        # Limit to 8 artifacts for this run
        artifacts_to_place = random.sample(artifact_ids, min(8, len(artifact_ids)))

        for artifact_id in artifacts_to_place:
            # Place in a random corridor/store location
            tile_types = ["CORRIDOR", "STORE_GENERIC", "ANCHOR_STORE", "FOOD_COURT"]
            tiles = []
            for tile in self.engine.tiles.values():
                if tile.type in tile_types and tile.walkable:
                    tiles.append(tile)

            if tiles:
                random.shuffle(tiles)
                tile = tiles[0]
                self.engine.add_artifact_to_location(artifact_id, tile.x, tile.y, tile.z)
                self._log_event(f"[ARTIFACT] {artifact_id} placed at ({tile.x}, {tile.y})")

    def _log_event(self, message: str):
        """Log an event to the session log"""
        self.session_log.append(message)
        self.npc_system.log_event(message)

    def handle_input(self, command: str) -> bool:
        """
        Process player input.
        Returns False if game should quit.
        """
        command = command.strip().lower()

        if command in ['w', 'up', 'forward']:
            facing = self.engine.get_player_facing()
            if self.engine.move_player(facing):
                self._log_event(f"[PLAYER] Moved forward to ({self.engine.player.x}, {self.engine.player.y})")
                return True

        elif command in ['s', 'down', 'backward']:
            facing = self.engine.get_player_facing()
            opposite = Direction((facing.value + 2) % 4)
            if self.engine.move_player(opposite):
                self._log_event(f"[PLAYER] Moved backward to ({self.engine.player.x}, {self.engine.player.y})")
                return True

        elif command in ['a', 'left', 'turn_left']:
            self.engine.rotate_player_left()
            return True

        elif command in ['d', 'right', 'turn_right']:
            self.engine.rotate_player_right()
            return True

        elif command in ['e', 'interact']:
            self._handle_interaction()
            return True

        elif command in ['i', 'inventory', 'tab']:
            self.show_inventory = not self.show_inventory
            return True

        elif command in ['q', 'quit', 'exit']:
            if self.engine.is_at_entrance():
                self._log_event("[GAME] Player left the mall.")
                return False
            else:
                self._log_event("[GAME] Cannot quit from here. Must reach ENTRANCE.")
                return True

        elif command in ['help', 'h', '?']:
            self._show_help()
            return True

        return True  # Keep running

    def _handle_interaction(self):
        """Handle player interaction at current tile"""
        current_tile = self.engine.get_player_tile()
        if not current_tile:
            return

        # Check for NPC
        npc = self.npc_system.get_npc_at_location(
            self.engine.player.x, self.engine.player.y, self.engine.player.z
        )

        if npc:
            # Start dialogue with NPC
            self._start_dialogue_with_npc(npc.id)
            return

        # Check for artifact
        artifact_id = self.engine.get_artifact_at_location(
            self.engine.player.x, self.engine.player.y, self.engine.player.z
        )

        if artifact_id:
            if self.engine.pickup_artifact(artifact_id):
                artifact = self.artifact_system.get_artifact(artifact_id)
                self._log_event(f"[ARTIFACT] Picked up: {artifact.name}")
                return

    def _start_dialogue_with_npc(self, npc_id: str):
        """Start dialogue with an NPC"""
        npc = self.npc_system.get_npc(npc_id)
        if not npc:
            return

        self.engine.record_interaction(npc_id)

        # Check if player has artifacts and is talking to Milo
        if npc_id == "milo" and self.engine.player.inventory:
            # Milo talks about artifacts
            artifact_id = self.engine.player.inventory[0]  # Talk about first artifact
            self.dialogue_text = self.artifact_system.get_lore(artifact_id)
            self.dialogue_npc = npc.name
        else:
            # General dialogue based on toddler stage
            stage = self.toddler_system.get_stage_number()
            dialogue = self.npc_system.get_dialogue(npc_id, "greeting")

            # Override with stage-specific dialogue if available
            stage_dialogue = self.npc_system.get_npc_reaction_to_stage(npc_id, stage)
            if stage_dialogue:
                dialogue = stage_dialogue

            self.dialogue_text = dialogue
            self.dialogue_npc = npc.name

        self.dialogue_active = True
        self._log_event(f"[DIALOGUE] {npc.name}: {self.dialogue_text}")

    def update(self):
        """Update game state"""
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time

        # Update playtime
        self.engine.update_playtime(int(delta_time))

        # Update toddler system
        stage, messages = self.toddler_system.update(self.engine.get_playtime())
        for msg in messages:
            self._log_event(msg)

        # Check for chaos events
        if self.toddler_system.should_trigger_chaos_event():
            chaos_msg = f"[EVENT] {self.toddler_system.get_chaos_event()}"
            self._log_event(chaos_msg)

        # Update NPC positions
        self.npc_system.update_npc_positions(self.engine, stage.value)

        # Apply artifact weirdness boost
        new_stage, weirdness = self.toddler_system.apply_artifact_weirdness_boost(
            len(self.engine.player.inventory)
        )
        if new_stage != stage:
            self._log_event(f"[ARTIFACT] Weirdness increased! New toddler stage: {new_stage.value}")

        # Update reality glitches - the facade cracks as toddler presence increases
        glitch_messages = self.reality_glitch.update(
            stage.value,
            self.toddler_system.get_shadow_intensity(),
            len(self.engine.player.inventory)
        )
        for glitch_msg in glitch_messages:
            self._log_event(glitch_msg)

    def render(self) -> str:
        """Render the current game frame in Wolfenstein 3D style"""
        # Get visual distortions from toddler system
        distortions = self.toddler_system.apply_visual_distortion()

        # Get reality glitch effects - modern rendering bleeding through the facade
        glitch_effects = self.reality_glitch.get_post_processing_effects()
        glitch_effects["photorealistic"] = self.reality_glitch.get_photorealistic_intensity()
        glitch_effects["wireframe"] = 1.0 if self.reality_glitch.should_show_wireframe() else 0.0
        glitch_effects["debug_info"] = 1.0 if self.reality_glitch.should_show_debug_info() else 0.0
        if glitch_effects["debug_info"] > 0:
            glitch_effects["debug_text"] = self.reality_glitch.generate_debug_text()

        # Render 3D view with textured walls + reality glitches
        frame_3d = self.renderer.render_frame(
            self.engine.player.x + 0.5,  # Center in tile
            self.engine.player.y + 0.5,
            self.engine.player.facing,
            self.engine.tiles,
            distortions,
            glitch_effects  # Modern effects bleeding through
        )

        # Render HUD
        player_data = {
            "position": (self.engine.player.x, self.engine.player.y),
            "playtime": self.engine.get_playtime(),
            "inventory_count": len(self.engine.player.inventory)
        }
        hud = self.hud.render(player_data, self.toddler_system.get_stage_number())

        # Build complete frame
        frame = frame_3d + "\n" + hud

        # Add audio/shadow messages
        audio_msg = self.toddler_system.get_audio_message()
        if audio_msg:
            frame += "\n" + self.hud.render_message(audio_msg, "audio")

        shadow_msg = self.toddler_system.get_shadow_description()
        if shadow_msg:
            frame += "\n" + self.hud.render_message(shadow_msg, "shadow")

        pressure_text = self.toddler_system.get_pressure_text()
        if pressure_text:
            frame += "\n" + self.hud.render_message(pressure_text, "danger")

        # Reality glitch warnings - the simulation is breaking
        if self.reality_glitch.is_reality_breaking():
            frame += f"\n{Color.fg(46)}[SYSTEM] SIMULATION INTEGRITY COMPROMISED{Color.reset()}"
            frame += f"\n{Color.fg(46)}[WARNING] Rendering facade failure detected{Color.reset()}"

        # Add dialogue box if active
        if self.dialogue_active:
            dialogue_box = self._render_dialogue_box(self.dialogue_npc, self.dialogue_text)
            frame += f"\n{dialogue_box}\n{Color.fg(240)}(Press E to close){Color.reset()}"

        # Add inventory screen if active
        if self.show_inventory:
            inventory_display = self._render_inventory()
            frame += f"\n{inventory_display}"

        return frame

    def _render_dialogue_box(self, npc_name: str, dialogue: str) -> str:
        """Render a dialogue box Wolf3D style"""
        box_width = min(len(dialogue) + len(npc_name) + 6, 118)
        box = f"{Color.fg(226)}╔{'═' * (box_width - 2)}╗\n"
        box += f"║ {Color.fg(255)}{npc_name}{Color.fg(226)}: {Color.fg(250)}{dialogue[:box_width - len(npc_name) - 6]}{Color.fg(226)}\n"
        box += f"╚{'═' * (box_width - 2)}╝{Color.reset()}"
        return box

    def _render_inventory(self) -> str:
        """Render inventory screen"""
        inv_text = f"{Color.fg(226)}{'═'*40}\n"
        inv_text += f"{Color.fg(255)} INVENTORY \n"
        inv_text += f"{Color.fg(226)}{'═'*40}\n{Color.reset()}"

        if not self.engine.player.inventory:
            inv_text += f"{Color.fg(240)}(empty){Color.reset()}\n"
        else:
            for artifact_id in self.engine.player.inventory:
                artifact = self.artifact_system.get_artifact(artifact_id)
                if artifact:
                    inv_text += f"{Color.fg(208)}• {Color.fg(255)}{artifact.name}{Color.reset()}\n"
                    inv_text += f"  {Color.fg(244)}{artifact.description}{Color.reset()}\n"

        inv_text += f"\n{Color.fg(240)}Press E near Milo to learn artifact lore{Color.reset()}"
        return inv_text

    def run(self):
        """Main game loop"""
        self.running = True
        self._clear_screen()

        # DOOFENSTEIN 3D WELCOME SCREEN
        print(f"{Color.fg(196)}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                                                                ║")
        print(f"║{Color.fg(226)}          D O O F E N S T E I N   3 D   M A L L          {Color.fg(196)}║")
        print("║                                                                ║")
        print(f"║{Color.fg(244)}              A Wolfenstein 3D-style Mall Crawler           {Color.fg(196)}║")
        print(f"║{Color.fg(240)}          (Coffee-spilled shareware clone edition)          {Color.fg(196)}║")
        print("║                                                                ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{Color.reset()}\n")

        print(f"{Color.fg(255)}You enter the mall with your mom's credit card.{Color.reset()}")
        print(f"{Color.fg(244)}The automatic doors close behind you.{Color.reset()}")
        print(f"{Color.fg(240)}You're not sure how long you can stay...{Color.reset()}\n")

        print(f"{Color.fg(226)}CONTROLS:{Color.reset()}")
        print(f"{Color.fg(255)}  W{Color.fg(244)}/Up{Color.fg(255)}   = Move forward       {Color.fg(255)}A{Color.fg(244)}/Left{Color.fg(255)}  = Turn left{Color.reset()}")
        print(f"{Color.fg(255)}  S{Color.fg(244)}/Down{Color.fg(255)} = Move backward      {Color.fg(255)}D{Color.fg(244)}/Right{Color.fg(255)} = Turn right{Color.reset()}")
        print(f"{Color.fg(255)}  E       {Color.fg(244)}= Interact           {Color.fg(255)}I       {Color.fg(244)}= Inventory{Color.reset()}")
        print(f"{Color.fg(255)}  Q       {Color.fg(244)}= Quit (ENTRANCE)    {Color.fg(255)}H       {Color.fg(244)}= Help{Color.reset()}\n")

        print(f"{Color.fg(208)}WARNING: {Color.fg(240)}Something is in the mall. You can't see it.{Color.reset()}")
        print(f"{Color.fg(240)}         The longer you stay, the more real it becomes.{Color.reset()}\n")

        print(f"{Color.fg(255)}Press ENTER to begin...{Color.reset()}")
        input()

        while self.running:
            self._clear_screen()

            # Render current frame
            frame = self.render()
            print(frame)

            # Get input
            try:
                command = input("\n> ").strip()
                if not command:
                    continue

                # Clear dialogue after input
                self.dialogue_active = False

                # Handle input
                if not self.handle_input(command):
                    break

                # Update game state
                self.update()

            except KeyboardInterrupt:
                print("\nGame interrupted.")
                break
            except EOFError:
                print("\nGame ended.")
                break

        self._show_ending()
        self._save_session_log()

    def _clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def _show_help(self):
        """Show help text"""
        help_text = """
=== HELP ===
MOVEMENT:
  W / UP        - Move forward
  S / DOWN      - Move backward
  A / LEFT      - Turn left
  D / RIGHT     - Turn right

INTERACTION:
  E / INTERACT  - Talk to NPCs, pick up artifacts
  I / INVENTORY - View your inventory

GAME:
  Q / QUIT      - Leave the mall (only at ENTRANCE)
  H / HELP      - Show this help text

GOAL:
You came to the mall with your mom's credit card.
Explore, find artifacts, talk to NPCs (especially Milo – he knows their stories).
But something is in the mall. Something you can't see.
The longer you stay, the more real it becomes.

Reach the ENTRANCE to leave safely.
        """
        print(help_text)
        input("Press ENTER to continue...")

    def _show_ending(self):
        """Show ending sequence"""
        self._clear_screen()
        if self.engine.is_at_entrance():
            print("\n" + "="*80)
            print("YOU ESCAPED")
            print("="*80)
            print("You push through the doors into the parking lot.")
            print("Your mom is waiting in the car, shopping bags in the trunk.")
            print("'Did you find everything you wanted?' she asks.")
            print("You look back at the mall entrance.")
            print("For a moment, you swear you hear crying from inside.")
            print("\nFinal playtime: {0}:{1:02d}".format(
                self.engine.get_playtime() // 60, self.engine.get_playtime() % 60
            ))
            print("Artifacts collected: {0}".format(len(self.engine.player.inventory)))
            print("="*80 + "\n")
        else:
            print("\nYou quit the game.")

    def _save_session_log(self):
        """Save session log to file"""
        log_file = os.path.join(os.path.dirname(__file__), "../session_log.txt")
        with open(log_file, 'w') as f:
            f.write("=== GLITCHDEX MALL SESSION LOG ===\n\n")
            for entry in self.session_log:
                f.write(entry + "\n")
        print(f"Session log saved to {log_file}")


def main():
    """Entry point"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
