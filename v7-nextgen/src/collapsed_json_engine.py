#!/usr/bin/env python3
"""
COLLAPSED JSON ENGINE - V7 Food Court Vertical Slice
Minimal game engine that loads everything from JSON files.

Philosophy: The game IS the JSON. The code just executes it.
"""

import json
from pathlib import Path
from typing import Dict, List, Any


# =============================================================================
# DATA LOADING
# =============================================================================

def load_palette(path="data/palette_COMICBOOK_MALL_V1.json") -> Dict:
    """Load color palette and build lookup dictionaries."""
    with open(path) as f:
        data = json.load(f)

    # Build name → hex lookup
    palette_map = {}
    for entry in data["entries"]:
        palette_map[entry["name"]] = entry["hex"]

    return palette_map


def load_tileset(path="data/mall_tileset_v1.json") -> Dict:
    """Load tile definitions."""
    with open(path) as f:
        return json.load(f)


def load_npc_profiles(path="data/npc_profiles_v1.json") -> Dict:
    """Load NPC color schemes."""
    with open(path) as f:
        return json.load(f)


def load_game_state(path="data/game_state_foodcourt_v1.json") -> Dict:
    """Load complete game state (level + entities + config)."""
    with open(path) as f:
        return json.load(f)


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# =============================================================================
# GAME STATE MANAGEMENT
# =============================================================================

class GameState:
    """
    Minimal game state container.
    Everything observable - no hidden complexity.
    """

    def __init__(self, config_path="data/game_state_foodcourt_v1.json"):
        # Load all data
        self.palette = load_palette()
        self.tileset = load_tileset()
        self.npc_profiles = load_npc_profiles()
        self.config = load_game_state(config_path)

        # Extract key state
        self.cloud_level = self.config["cloud_pressure"]["current_level"]
        self.cloud_phase = "calm"
        self.entities = {e["id"]: e for e in self.config["entities"]}
        self.player = self.entities["PLAYER"]

        # Triggers
        self.triggers = {t["id"]: t for t in self.config["triggers"]}

        # Runtime state
        self.subtitle_text = None
        self.subtitle_timer = 0.0
        self.cycle_count = 0

    def get_color(self, palette_name: str) -> tuple:
        """Look up palette name → RGB color."""
        hex_color = self.palette.get(palette_name, "#FFFFFF")
        return hex_to_rgb(hex_color)

    def get_tile_colors(self, tile_type: str) -> Dict[str, tuple]:
        """Get all colors for a tile type."""
        tile_def = self.tileset["tiles"].get(tile_type, {})
        return {
            part: self.get_color(palette_name)
            for part, palette_name in tile_def.items()
        }


# =============================================================================
# GAME LOGIC (Threshold-based, no behavior trees)
# =============================================================================

def update_cloud(gs: GameState, dt: float):
    """Update cloud pressure (passive rise + events)."""

    # Passive rise
    passive_rate = gs.config["cloud_pressure"]["passive_rate"]
    gs.cloud_level += passive_rate * dt

    # Cap at max
    max_level = gs.config["cloud_pressure"]["max_level"]
    gs.cloud_level = min(gs.cloud_level, max_level)

    # Update phase based on thresholds
    phases = gs.config["cloud_pressure"]["phases"]
    for phase_name, phase_data in phases.items():
        low, high = phase_data["range"]
        if low <= gs.cloud_level < high:
            gs.cloud_phase = phase_name
            break


def check_triggers(gs: GameState):
    """
    Check all threshold-based triggers.
    No complex AI - just: if condition, then action.
    """

    # Janitor threshold
    janitor = gs.entities.get("JANITOR")
    if janitor and not janitor.get("rule_broken", False):
        if gs.cloud_level >= janitor["threshold"]:
            trigger = gs.triggers["JANITOR_THRESHOLD"]
            execute_trigger(gs, trigger)

    # Cloud release
    release_threshold = gs.config["cloud_pressure"]["cycle"]["release_at"]
    if gs.cloud_level >= release_threshold:
        trigger = gs.triggers["CLOUD_RELEASE"]
        execute_trigger(gs, trigger)


def execute_trigger(gs: GameState, trigger: Dict):
    """
    Execute trigger actions.
    Simple action interpreter - no scripting language needed.
    """

    for action_def in trigger.get("on_trigger", []):
        action_type = action_def["action"]

        if action_type == "subtitle":
            gs.subtitle_text = action_def["text"]
            gs.subtitle_timer = action_def.get("duration", 3.0)

        elif action_type == "set_flag":
            npc_id = action_def["npc"]
            flag = action_def["flag"]
            value = action_def["value"]
            gs.entities[npc_id][flag] = value

        elif action_type == "cloud_drop":
            target = action_def["target"]
            duration = action_def["duration"]
            # In real engine: tween cloud_level → target over duration
            gs.cloud_level = target
            gs.cycle_count += 1

        elif action_type == "reset_npc":
            npc_id = action_def["npc"]
            npc = gs.entities[npc_id]
            npc["rule_broken"] = False
            # Move back to spawn, etc.

        elif action_type == "toddler_fade":
            toddler = gs.entities["TODDLER"]
            toddler["manifestation"] = action_def["target_manifestation"]

        # Add more actions as needed (screen_flash, move_npc, etc.)


def handle_credit_card_use(gs: GameState, card_name: str):
    """
    Player uses credit card → Cloud increases.
    Toddler amplifies effect if nearby.
    """

    card = gs.config["player"]["credit_cards"][card_name]
    cost = card["cost"]

    # Check toddler proximity
    toddler = gs.entities["TODDLER"]
    toddler_multiplier = toddler["on_credit_card_use"]["cloud_multiplier"]

    # Apply cost (with amplification if toddler visible)
    if toddler["manifestation"] > 0.5:
        gs.cloud_level += cost * toddler_multiplier
        toddler["manifestation"] = min(1.0, toddler["manifestation"] + 0.1)
        gs.subtitle_text = "The toddler giggles."
        gs.subtitle_timer = 2.0
    else:
        gs.cloud_level += cost
        gs.subtitle_text = "That's probably fine."
        gs.subtitle_timer = 2.0


def update_subtitle(gs: GameState, dt: float):
    """Update subtitle timer (simple fade system)."""
    if gs.subtitle_timer > 0:
        gs.subtitle_timer -= dt
        if gs.subtitle_timer <= 0:
            gs.subtitle_text = None


# =============================================================================
# MINIMAL GAME LOOP
# =============================================================================

def game_loop(gs: GameState, dt: float, input_state: Dict):
    """
    Entire game logic in ~20 lines.
    No behavior trees. Just: update numbers, check thresholds, execute.
    """

    # 1. Handle player input
    if input_state.get("use_credit_card"):
        active_card = input_state["card_name"]
        handle_credit_card_use(gs, active_card)

    # 2. Update cloud (passive rise)
    update_cloud(gs, dt)

    # 3. Check thresholds → execute triggers
    check_triggers(gs)

    # 4. Update UI timers
    update_subtitle(gs, dt)

    # That's it. Game state updated.
    # Renderer just reads gs and displays it.


# =============================================================================
# MAIN (Example usage)
# =============================================================================

def main():
    """
    Example: Load game from JSON, run minimal update loop.
    """

    print("=" * 60)
    print("  COLLAPSED JSON ENGINE - Food Court Vertical Slice")
    print("=" * 60)

    # Load everything from JSON
    gs = GameState("data/game_state_foodcourt_v1.json")

    print(f"\n✅ Loaded palette: {len(gs.palette)} colors")
    print(f"✅ Loaded tileset: {len(gs.tileset['tiles'])} tiles")
    print(f"✅ Loaded NPCs: {len(gs.npc_profiles['npcs'])} profiles")
    print(f"✅ Loaded level: {gs.config['level_id']}")
    print(f"✅ Entities: {len(gs.entities)}")

    # Example: Get tile colors
    print("\n--- FOOD_COURT Tile Colors ---")
    fc_colors = gs.get_tile_colors("FOOD_COURT")
    for part, rgb in fc_colors.items():
        print(f"  {part:12s} → RGB{rgb}")

    # Example: Get NPC colors
    print("\n--- JANITOR_UNIT7 Colors ---")
    janitor_def = gs.npc_profiles["npcs"]["JANITOR_UNIT7"]
    for part, palette_name in janitor_def.items():
        if part != "description":
            rgb = gs.get_color(palette_name)
            print(f"  {part:12s} → {palette_name:25s} → RGB{rgb}")

    # Example: Simulate credit card use
    print("\n--- Simulating Credit Card Use ---")
    print(f"Cloud before: {gs.cloud_level}")
    handle_credit_card_use(gs, "VISA")
    print(f"Cloud after VISA: {gs.cloud_level}")
    print(f"Subtitle: '{gs.subtitle_text}'")

    # Example: Update until threshold
    print("\n--- Simulating Cloud Rise to Janitor Threshold ---")
    dt = 1.0
    steps = 0
    while gs.cloud_level < 70 and steps < 200:
        game_loop(gs, dt, {})
        steps += 1
        if steps % 10 == 0:
            print(f"  Step {steps:3d}: Cloud = {gs.cloud_level:5.1f} ({gs.cloud_phase})")

    print(f"\n✅ Janitor threshold reached at Cloud {gs.cloud_level:.1f}")
    print(f"✅ Janitor rule broken: {gs.entities['JANITOR']['rule_broken']}")
    if gs.subtitle_text:
        print(f"✅ Subtitle: '{gs.subtitle_text}'")

    print("\n" + "=" * 60)
    print("  Demo complete. Game state fully defined in JSON.")
    print("  Engine is ~150 lines. Everything else is data.")
    print("=" * 60)


if __name__ == "__main__":
    main()
