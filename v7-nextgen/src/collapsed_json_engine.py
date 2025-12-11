#!/usr/bin/env python3
"""
COLLAPSED JSON ENGINE - V7 Food Court Vertical Slice
Minimal game engine that loads everything from JSON files.

Philosophy: The game IS the JSON. The code just executes it.
"""

import ast
import json
from pathlib import Path
from typing import Any, Dict, List


# =============================================================================
# NORMALIZATION (The Forgiveness Layer)
# =============================================================================

def normalize_key(k: Any) -> str:
    """
    Normalize any key to uppercase.
    Makes JSON authoring forgiving - write however you want.
    """
    return str(k).strip().upper()


def normalize_dict(d: Dict, recursive: bool = True) -> Dict:
    """
    Normalize all dictionary keys to uppercase.
    Optionally recurse into nested dicts.
    """
    result = {}
    for k, v in d.items():
        normalized_key = normalize_key(k)

        # Recursively normalize nested dicts
        if recursive and isinstance(v, dict):
            result[normalized_key] = normalize_dict(v, recursive=True)
        elif recursive and isinstance(v, list):
            # Handle lists of dicts
            result[normalized_key] = [
                normalize_dict(item, recursive=True) if isinstance(item, dict) else item
                for item in v
            ]
        else:
            result[normalized_key] = v

    return result


def normalize_value(v: Any) -> str:
    """
    Normalize string values (entity names, tile types, etc.) to uppercase.
    Non-strings pass through unchanged.
    """
    if isinstance(v, str):
        return v.strip().upper()
    return v


# =============================================================================
# DATA LOADING
# =============================================================================

def load_palette(path="data/palette_COMICBOOK_MALL_V1.json") -> Dict:
    """Load color palette and build lookup dictionaries."""
    with open(path) as f:
        data = json.load(f)
    data = normalize_dict(data)

    # Build name → hex lookup (palette names normalized to uppercase)
    palette_map = {}
    for entry in data["ENTRIES"]:
        palette_name = normalize_value(entry["NAME"])
        palette_map[palette_name] = entry["HEX"]

    return palette_map


def load_tileset(path="data/mall_tileset_v1.json") -> Dict:
    """Load tile definitions."""
    with open(path) as f:
        data = json.load(f)
    return normalize_dict(data)


def load_npc_profiles(path="data/npc_profiles_v1.json") -> Dict:
    """Load NPC color schemes."""
    with open(path) as f:
        data = json.load(f)
    return normalize_dict(data)


def load_game_state(path="data/game_state_foodcourt_v1.json") -> Dict:
    """Load complete game state (level + entities + config)."""
    with open(path) as f:
        data = json.load(f)
    return normalize_dict(data)


def load_world_index(path="data/mall_world_index.json") -> Dict:
    """
    Load world graph topology.
    The mall structure becomes data - zones, escalators, era layers.
    """
    with open(path) as f:
        data = json.load(f)
    return normalize_dict(data)


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

    def __init__(self, config_path="data/game_state_foodcourt_v1.json", world_index_path="data/mall_world_index.json"):
        # Load all data (normalized to uppercase keys)
        self.palette = load_palette()
        self.tileset = load_tileset()
        self.npc_profiles = load_npc_profiles()
        self.config = load_game_state(config_path)
        self.world_index = load_world_index(world_index_path)

        # Extract key state (using normalized keys)
        self.cloud_level = self.config["CLOUD_PRESSURE"]["CURRENT_LEVEL"]
        self.cloud_phase = "calm"
        self.entities = {normalize_value(e["ID"]): e for e in self.config["ENTITIES"]}
        self.player = self.entities["PLAYER"]

        # Triggers (normalize trigger IDs)
        self.triggers = {normalize_value(t["ID"]): t for t in self.config["TRIGGERS"]}
        self.triggered_ids = set()  # Track which triggers have fired

        # World state (current zone from world index)
        self.current_zone = normalize_value(self.world_index["STARTING_ZONE"])

        # Runtime state
        self.subtitle_text = None
        self.subtitle_timer = 0.0
        self.cycle_count = 0

    def get_color(self, palette_name: str) -> tuple:
        """
        Look up palette name → RGB color.
        Forgiving - accepts any case.
        """
        normalized_name = normalize_value(palette_name)
        hex_color = self.palette.get(normalized_name, "#FFFFFF")
        return hex_to_rgb(hex_color)

    def get_tile(self, tile_type: str) -> Dict:
        """
        Get tile definition by type.
        Forgiving - accepts any case.
        """
        normalized_type = normalize_value(tile_type)
        return self.tileset["TILES"].get(normalized_type, {})

    def get_tile_colors(self, tile_type: str) -> Dict[str, tuple]:
        """
        Get all colors for a tile type.
        Forgiving - accepts any case.
        """
        tile_def = self.get_tile(tile_type)
        return {
            part: self.get_color(palette_name)
            for part, palette_name in tile_def.items()
        }

    def get_npc_profile(self, profile_name: str) -> Dict:
        """
        Get NPC profile by name.
        Forgiving - accepts any case.
        """
        normalized_name = normalize_value(profile_name)
        return self.npc_profiles["NPCS"].get(normalized_name, {})

    def get_entity(self, entity_id: str) -> Dict:
        """
        Get entity by ID.
        Forgiving - accepts any case.
        """
        normalized_id = normalize_value(entity_id)
        return self.entities.get(normalized_id, {})

    def get_zone(self, zone_name: str) -> Dict:
        """
        Get zone definition from world index.
        Forgiving - accepts any case.
        """
        normalized_name = normalize_value(zone_name)
        return self.world_index["ZONES"].get(normalized_name, {})

    def get_available_transitions(self) -> List[Dict]:
        """
        Get all escalators/transitions from current zone.
        Evaluates rules to determine which are currently accessible.
        """
        available = []
        for escalator in self.world_index["ESCALATORS"]:
            if normalize_value(escalator["FROM"]) == self.current_zone:
                # Evaluate the rule to see if transition is available
                rule = escalator.get("RULE", "true")
                if evaluate_condition(rule, self):
                    available.append(escalator)
        return available

    def can_transition_to(self, target_zone: str) -> bool:
        """
        Check if we can transition to a specific zone.
        Forgiving - accepts any case.
        """
        normalized_target = normalize_value(target_zone)
        for transition in self.get_available_transitions():
            if normalize_value(transition["TO"]) == normalized_target:
                return True
        return False

    def transition_to_zone(self, target_zone: str) -> bool:
        """
        Attempt to transition to a new zone.
        Returns True if successful, False if transition not available.
        """
        normalized_target = normalize_value(target_zone)

        if self.can_transition_to(normalized_target):
            # Load new game state for target zone
            zone_def = self.get_zone(normalized_target)
            if zone_def:
                new_state_file = f"data/{zone_def['FILE']}"
                self.config = load_game_state(new_state_file)

                # Re-extract entities and triggers from new zone
                self.entities = {normalize_value(e["ID"]): e for e in self.config["ENTITIES"]}
                self.triggers = {normalize_value(t["ID"]): t for t in self.config["TRIGGERS"]}
                self.triggered_ids.clear()  # Reset triggers in new zone

                # Update current zone
                self.current_zone = normalized_target

                return True

        return False


# =============================================================================
# GAME LOGIC (Threshold-based, no behavior trees)
# =============================================================================

def update_cloud(gs: GameState, dt: float):
    """Update cloud pressure (passive rise + events)."""

    # Passive rise (using normalized keys)
    passive_rate = gs.config["CLOUD_PRESSURE"]["PASSIVE_RATE"]
    gs.cloud_level += passive_rate * dt

    # Cap at max
    max_level = gs.config["CLOUD_PRESSURE"]["MAX_LEVEL"]
    gs.cloud_level = min(gs.cloud_level, max_level)

    # Update phase based on thresholds
    phases = gs.config["CLOUD_PRESSURE"]["PHASES"]
    for phase_name, phase_data in phases.items():
        low, high = phase_data["RANGE"]
        if low <= gs.cloud_level < high:
            gs.cloud_phase = phase_name.lower()  # Keep phase name lowercase for readability
            break


def _safe_eval_simple_expression(expr: str) -> bool:
    """
    Evaluate a simple boolean/comparison expression safely, e.g.:
        "1 < 2"
        "3 == 3"
        "5 >= 2 and 1 < 4"

    No function calls, no attribute access, no names.
    Only literals, comparisons, and and/or/not.
    """
    def _eval_node(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return _eval_node(node.body)
        if isinstance(node, ast.BoolOp):
            vals = [_eval_node(v) for v in node.values]
            if isinstance(node.op, ast.And):
                return all(vals)
            if isinstance(node.op, ast.Or):
                return any(vals)
            raise ValueError("Unsupported boolean operator")
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return not _eval_node(node.operand)
        if isinstance(node, ast.Compare):
            left = _eval_node(node.left)
            for op, comp in zip(node.ops, node.comparators):
                right = _eval_node(comp)
                if isinstance(op, ast.Eq) and not (left == right):
                    return False
                elif isinstance(op, ast.NotEq) and not (left != right):
                    return False
                elif isinstance(op, ast.Lt) and not (left < right):
                    return False
                elif isinstance(op, ast.LtE) and not (left <= right):
                    return False
                elif isinstance(op, ast.Gt) and not (left > right):
                    return False
                elif isinstance(op, ast.GtE) and not (left >= right):
                    return False
                left = right
            return True
        if isinstance(node, ast.Constant):
            return node.value
        # Disallow everything else: no names, no calls, no attributes
        raise ValueError(f"Unsupported expression node: {type(node).__name__}")

    tree = ast.parse(expr, mode="eval")
    return bool(_eval_node(tree))


def evaluate_condition(condition: str, gs: GameState) -> bool:
    """
    Evaluate a trigger condition string.
    Simple parser - handles JSON-style booleans and Python eval.
    Forgiving - entity names case-insensitive.
    """

    # Replace game state variables with actual values
    context = condition
    context = context.replace("cloud", str(gs.cloud_level))

    # Handle entity property checks (e.g., "janitor.rule_broken == false")
    # Entities are stored as uppercase, but conditions use lowercase
    for entity_id, entity in gs.entities.items():
        entity_lower = entity_id.lower()
        for key, value in entity.items():
            # Keep as Python bool (True/False not true/false)
            # Match lowercase entity name in condition, uppercase key in entity dict
            key_lower = key.lower()
            context = context.replace(f"{entity_lower}.{key_lower}", str(value))

    # Replace logical operators (JSON-style to Python-style)
    context = context.replace(" AND ", " and ")
    context = context.replace(" OR ", " or ")

    # Replace JSON-style booleans with Python-style
    # Use word boundaries to avoid replacing parts of variable names
    import re
    context = re.sub(r'\bfalse\b', 'False', context)
    context = re.sub(r'\btrue\b', 'True', context)

    # Safe eval of simple comparison expressions
    try:
        return _safe_eval_simple_expression(context)
    except Exception:
        return False


def check_triggers(gs: GameState):
    """
    Check all threshold-based triggers.
    Generic - evaluates conditions from JSON, no hardcoded trigger IDs.
    """

    # Iterate through all triggers and check conditions
    for trigger_id, trigger in gs.triggers.items():
        # Skip if already triggered (one-shot triggers)
        if trigger_id in gs.triggered_ids:
            continue

        # Check if trigger has condition (using normalized key)
        if "CONDITION" in trigger:
            if evaluate_condition(trigger["CONDITION"], gs):
                execute_trigger(gs, trigger)
                gs.triggered_ids.add(trigger_id)


def execute_trigger(gs: GameState, trigger: Dict):
    """
    Execute trigger actions.
    Simple action interpreter - no scripting language needed.
    Uses normalized keys (uppercase).
    """

    for action_def in trigger.get("ON_TRIGGER", []):
        # Normalize action type for case-insensitive matching
        action_type = normalize_value(action_def["ACTION"])

        if action_type == "SUBTITLE":
            gs.subtitle_text = action_def["TEXT"]
            gs.subtitle_timer = action_def.get("DURATION", 3.0)

        elif action_type == "SET_FLAG":
            npc_id = normalize_value(action_def["NPC"])
            flag = action_def["FLAG"]
            value = action_def["VALUE"]
            gs.entities[npc_id][flag] = value

        elif action_type == "CLOUD_DROP":
            target = action_def["TARGET"]
            duration = action_def["DURATION"]
            # In real engine: tween cloud_level → target over duration
            gs.cloud_level = target
            gs.cycle_count += 1
            # Reset triggers so they can fire again in next cycle
            gs.triggered_ids.clear()

        elif action_type == "RESET_NPC":
            npc_id = normalize_value(action_def["NPC"])
            npc = gs.entities.get(npc_id)
            if npc:
                npc["RULE_BROKEN"] = False
                # Move back to spawn, etc.

        elif action_type == "TODDLER_FADE":
            toddler = gs.entities.get("TODDLER")
            if toddler:
                toddler["MANIFESTATION"] = action_def["TARGET_MANIFESTATION"]

        elif action_type == "SET_LIGHTING":
            # In real engine: apply flicker/brightness to renderer
            # For now, just track in state
            pass

        elif action_type == "STOP_PATROL":
            npc_id = normalize_value(action_def["NPC"])
            npc = gs.entities.get(npc_id)
            if npc:
                npc["BEHAVIOR"] = "stopped"

        elif action_type == "RESUME_PATROL":
            npc_id = normalize_value(action_def["NPC"])
            npc = gs.entities.get(npc_id)
            if npc:
                npc["BEHAVIOR"] = "patrol_loop"

        elif action_type == "SCREEN_FLASH":
            # In real engine: flash screen with color
            # For now, just acknowledge
            pass

        elif action_type == "MOVE_NPC":
            npc_id = normalize_value(action_def["NPC"])
            target = action_def.get("TARGET")
            npc = gs.entities.get(npc_id)
            if npc and target:
                # In real engine: set movement target
                npc["ZONE"] = target

        # Add more actions as needed


def handle_credit_card_use(gs: GameState, card_name: str):
    """
    Player uses credit card → Cloud increases.
    Toddler amplifies effect if nearby.
    Forgiving - accepts any case for card name.
    """

    # Normalize card name for lookup
    card_name_normalized = normalize_value(card_name)
    card = gs.config["PLAYER"]["CREDIT_CARDS"][card_name_normalized]
    cost = card["COST"]

    # Check toddler proximity
    toddler = gs.entities.get("TODDLER")
    if not toddler:
        gs.cloud_level += cost
        return

    toddler_multiplier = toddler["ON_CREDIT_CARD_USE"]["CLOUD_MULTIPLIER"]

    # Apply cost (with amplification if toddler visible)
    if toddler["MANIFESTATION"] > 0.5:
        gs.cloud_level += cost * toddler_multiplier
        toddler["MANIFESTATION"] = min(1.0, toddler["MANIFESTATION"] + 0.1)
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
    print(f"✅ Loaded tileset: {len(gs.tileset['TILES'])} tiles")
    print(f"✅ Loaded NPCs: {len(gs.npc_profiles['NPCS'])} profiles")
    print(f"✅ Loaded level: {gs.config['LEVEL_ID']}")
    print(f"✅ Entities: {len(gs.entities)}")

    # Example: Get tile colors (case-insensitive!)
    print("\n--- food_court Tile Colors (lowercase works!) ---")
    fc_colors = gs.get_tile_colors("food_court")
    for part, rgb in fc_colors.items():
        print(f"  {part:12s} → RGB{rgb}")

    # Example: Get NPC colors (using helper method)
    print("\n--- JANITOR_unit7 Colors (MiXeD case works!) ---")
    janitor_def = gs.get_npc_profile("janitor_UNIT7")
    for part, palette_name in janitor_def.items():
        if part != "DESCRIPTION":
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
    print(f"✅ Janitor rule broken: {gs.entities['JANITOR']['RULE_BROKEN']}")
    if gs.subtitle_text:
        print(f"✅ Subtitle: '{gs.subtitle_text}'")

    print("\n" + "=" * 60)
    print("  Demo complete. Game state fully defined in JSON.")
    print("  Engine is ~150 lines. Everything else is data.")
    print("=" * 60)


if __name__ == "__main__":
    main()
