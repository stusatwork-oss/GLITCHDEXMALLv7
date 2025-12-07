#!/usr/bin/env python3
"""
SYMBOL STACKING SYSTEM
Hierarchical symbol composition for deep space probe telemetry.

Stacking gives levels:
  🏬 = Mall (level 0)
  🏬🍽️ = Mall → Food Court (level 1)
  🏬🍽️🍕 = Mall → Food Court → Pizza (level 2)

Same principle as:
  - File paths: /mall/food_court/pizza
  - DNS: pizza.food_court.mall
  - Deep space probe subsystem IDs: SYS.SUB.COMP
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass


# ============================================================================
# SYMBOL STACK DEFINITION
# ============================================================================

@dataclass
class SymbolStack:
    """A hierarchical stack of symbols."""
    symbols: List[str]

    @property
    def level(self) -> int:
        """Depth of the stack (0 = root)."""
        return len(self.symbols) - 1

    @property
    def path(self) -> str:
        """Symbol path representation."""
        return "".join(self.symbols)

    @property
    def root(self) -> str:
        """Root symbol (level 0)."""
        return self.symbols[0] if self.symbols else ""

    @property
    def leaf(self) -> str:
        """Leaf symbol (deepest level)."""
        return self.symbols[-1] if self.symbols else ""

    def push(self, symbol: str) -> 'SymbolStack':
        """Add a level to the stack."""
        return SymbolStack(self.symbols + [symbol])

    def pop(self) -> Tuple['SymbolStack', str]:
        """Remove the deepest level."""
        if len(self.symbols) <= 1:
            raise ValueError("Cannot pop root symbol")
        return SymbolStack(self.symbols[:-1]), self.symbols[-1]

    def __str__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        return f"SymbolStack({' → '.join(self.symbols)})"


# ============================================================================
# HIERARCHICAL REGISTRY
# ============================================================================

class SymbolHierarchy:
    """Registry of hierarchical symbol relationships."""

    def __init__(self):
        self.registry = {}
        self.reverse = {}  # entity_id → SymbolStack

    def register(self, stack: SymbolStack, entity_id: int):
        """Register a symbol stack with its entity ID."""
        path = stack.path
        self.registry[path] = {
            "entity_id": entity_id,
            "stack": stack,
            "level": stack.level
        }
        self.reverse[entity_id] = stack

    def get(self, path: str) -> Optional[dict]:
        """Get registered stack by path."""
        return self.registry.get(path)

    def get_by_id(self, entity_id: int) -> Optional[SymbolStack]:
        """Get stack by entity ID."""
        return self.reverse.get(entity_id)

    def children(self, parent_path: str) -> List[str]:
        """Get all child stacks of a parent."""
        return [
            path for path in self.registry.keys()
            if path.startswith(parent_path) and path != parent_path
        ]


# ============================================================================
# STANDARD HIERARCHIES
# ============================================================================

def build_mall_hierarchy() -> SymbolHierarchy:
    """
    Build the standard mall symbol hierarchy.

    Structure:
      🏬 (Mall root)
      ├── 🍽️ (Food Court)
      │   ├── 🍕 (Pizza)
      │   ├── 🥤 (Slurpee)
      │   └── ⬆️ (Escalator to food court)
      ├── 🎬 (Theater)
      └── 🧑‍🔧 (Service areas)
          └── 🧹 (Janitor equipment)
    """
    hierarchy = SymbolHierarchy()

    # Level 0: Root
    mall_root = SymbolStack(['🏬'])
    hierarchy.register(mall_root, symbol_to_entity_id_stacked(mall_root))

    # Level 1: Major zones
    food_court = SymbolStack(['🏬', '🍽️'])
    theater = SymbolStack(['🏬', '🎬'])
    service = SymbolStack(['🏬', '🧑‍🔧'])

    hierarchy.register(food_court, symbol_to_entity_id_stacked(food_court))
    hierarchy.register(theater, symbol_to_entity_id_stacked(theater))
    hierarchy.register(service, symbol_to_entity_id_stacked(service))

    # Level 2: Items in zones
    pizza = SymbolStack(['🏬', '🍽️', '🍕'])
    slurpee = SymbolStack(['🏬', '🍽️', '🥤'])
    escalator = SymbolStack(['🏬', '🍽️', '⬆️'])
    janitor_mop = SymbolStack(['🏬', '🧑‍🔧', '🧹'])

    hierarchy.register(pizza, symbol_to_entity_id_stacked(pizza))
    hierarchy.register(slurpee, symbol_to_entity_id_stacked(slurpee))
    hierarchy.register(escalator, symbol_to_entity_id_stacked(escalator))
    hierarchy.register(janitor_mop, symbol_to_entity_id_stacked(janitor_mop))

    return hierarchy


def symbol_to_entity_id_stacked(stack: SymbolStack) -> int:
    """
    Convert a symbol stack to entity ID.

    Uses XOR of all codepoints in the path for unique ID.
    """
    entity_id = 0
    for symbol in stack.symbols:
        for char in symbol:
            entity_id ^= ord(char)
    return entity_id


# ============================================================================
# MEASUREMENT ANCHOR STACKS
# ============================================================================

def create_source_of_truth_stacks() -> List[SymbolStack]:
    """
    Create symbol stacks for measurement anchors.

    These are the "known good" measurements from deep space probe calibration.
    """
    stacks = []

    # Escalator: 12 steps × 8 inches = 8 feet
    escalator_stack = SymbolStack(['🏬', '🍽️', '⬆️', '📏'])
    escalator_stack.metadata = {
        "measurement": "drop_feet",
        "value": 8.0,
        "confidence": "HIGH",
        "source": "Escalator step count",
        "anchor": True
    }
    stacks.append(escalator_stack)

    # Elevator doors: 3.5' × 6.75'
    elevator_stack = SymbolStack(['🏬', '🚪', '📏'])
    elevator_stack.metadata = {
        "measurement": "dimensions_feet",
        "value": (3.5, 6.75),
        "confidence": "HIGH",
        "source": "Commercial standard",
        "anchor": True
    }
    stacks.append(elevator_stack)

    return stacks


# ============================================================================
# RENPY INTEGRATION
# ============================================================================

def stack_to_renpy_define(stack: SymbolStack, value: any) -> str:
    """
    Convert symbol stack to Ren'Py define statement.

    Examples:
        SymbolStack(['🏬', '🍽️', '🍕']) →
            define MALL_FOOD_COURT_PIZZA = "🏬🍽️🍕"
    """
    # Convert symbols to readable names
    symbol_map = {
        '🏬': 'MALL',
        '🍽️': 'FOOD_COURT',
        '🍕': 'PIZZA',
        '🥤': 'SLURPEE',
        '⬆️': 'ESCALATOR',
        '🧹': 'JANITOR_MOP',
        '🧑‍🔧': 'SERVICE',
        '🎬': 'THEATER',
        '🚪': 'ELEVATOR',
        '📏': 'MEASUREMENT'
    }

    name_parts = []
    for symbol in stack.symbols:
        # Handle multi-codepoint emojis
        base_symbol = symbol[0] if len(symbol) > 0 else symbol
        name = symbol_map.get(base_symbol, f"SYM_{ord(base_symbol):04X}")
        name_parts.append(name)

    define_name = "_".join(name_parts)

    if isinstance(value, str):
        return f'define {define_name} = "{value}"'
    else:
        return f'define {define_name} = {value}'


# ============================================================================
# GEOJSON WITH STACKS
# ============================================================================

def stack_to_geojson_feature(stack: SymbolStack, geometry: dict, properties: dict) -> dict:
    """
    Create GeoJSON feature with symbol stack ID.

    Deep space probe telemetry → GeoJSON → Ren'Py
    """
    entity_id = symbol_to_entity_id_stacked(stack)

    return {
        "type": "Feature",
        "id": entity_id,
        "geometry": geometry,
        "properties": {
            "symbol_stack": stack.path,
            "symbol_level": stack.level,
            "symbol_root": stack.root,
            "symbol_leaf": stack.leaf,
            "entity_id": entity_id,
            **properties
        }
    }


# ============================================================================
# CLI TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("SYMBOL STACKING SYSTEM TEST")
    print("=" * 80)

    # Build hierarchy
    hierarchy = build_mall_hierarchy()

    print("\n[MALL HIERARCHY]")
    for path, data in hierarchy.registry.items():
        stack = data["stack"]
        print(f"  Level {stack.level}: {stack} (ID: {data['entity_id']})")

    print("\n[SYMBOL STACK OPERATIONS]")
    stack = SymbolStack(['🏬', '🍽️', '🍕'])
    print(f"  Stack: {stack}")
    print(f"  Path: {stack.path}")
    print(f"  Level: {stack.level}")
    print(f"  Root: {stack.root}")
    print(f"  Leaf: {stack.leaf}")

    # Push a level
    new_stack = stack.push('🔥')  # Hot pizza
    print(f"  Push '🔥': {new_stack} (Level {new_stack.level})")

    print("\n[MEASUREMENT ANCHORS]")
    anchors = create_source_of_truth_stacks()
    for stack in anchors:
        print(f"  {stack}: {stack.metadata}")

    print("\n[REN'PY DEFINES]")
    mall_stack = SymbolStack(['🏬'])
    pizza_stack = SymbolStack(['🏬', '🍽️', '🍕'])
    print(f"  {stack_to_renpy_define(mall_stack, mall_stack.path)}")
    print(f"  {stack_to_renpy_define(pizza_stack, pizza_stack.path)}")

    print("\n[GEOJSON FEATURE]")
    feature = stack_to_geojson_feature(
        pizza_stack,
        geometry={"type": "Point", "coordinates": [10, -120, -8]},
        properties={"qbit": 500, "status": "cold"}
    )
    import json
    print(json.dumps(feature, indent=2))

    print("\n" + "=" * 80)
    print("STACKING GIVES IT LEVELS")
    print("  Single symbol: 🍕 = Pizza (generic)")
    print("  Stacked: 🏬🍽️🍕 = Mall → Food Court → Pizza (specific)")
    print("  Deep space probe: Same concept as subsystem IDs (SYS.SUB.COMP)")
    print("=" * 80)
