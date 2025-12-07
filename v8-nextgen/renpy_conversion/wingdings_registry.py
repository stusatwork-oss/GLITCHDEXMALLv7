#!/usr/bin/env python3
"""
WINGDINGS REGISTRY - Symbol Assignment System
Assigns Unicode symbols as primary identifiers for items, NPCs, and zones.

This module provides the core symbol mapping that serves as the "wingdings"
approach to value assignment - each entity gets a symbol as its ID.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


# ============================================================================
# SYMBOL REGISTRY - Primary Identifiers
# ============================================================================

@dataclass
class SymbolEntity:
    """An entity identified by its symbol."""
    symbol: str          # Unicode symbol (primary key)
    name: str           # Human-readable name
    category: str       # ITEM, NPC, ZONE, FEATURE
    properties: Dict[str, Any]


# ============================================================================
# WINGDINGS ASSIGNMENTS
# ============================================================================

# Items (Voxel Objects)
ITEM_SYMBOLS = {
    '🧹': 'JANITOR_MOP',
    '🍕': 'PIZZA_SLICE',
    '🥤': 'SLURPEE_CUP',
    '🪙': 'ARCADE_TOKEN',
    '🗑️': 'TRASH_CAN',
    '🔑': 'MASTER_KEY',
    '📺': 'SECURITY_MONITOR',
    '🛒': 'SHOPPING_CART',
    '🎮': 'ARCADE_CABINET',
    '💡': 'NEON_SIGN_FRAGMENT',
}

# NPCs (Characters)
NPC_SYMBOLS = {
    '🧑‍🔧': 'UNIT_7_JANITOR',
    '👔': 'AL_GORITHM',
    '👗': 'WIFE_AT_BOOKSTORE',
    '🧒': 'LEISURELY_LEON',
    '🐂': 'BULL_MOVEMENT_AGENT',
    '👨‍💼': 'KENNY_BITS',
    '🧓': 'BALES_CANONICAL',
    '👻': 'ESCALATOR_HUM',
    '🎭': 'THEATER_GHOST',
}

# Zones (Spatial Areas)
ZONE_SYMBOLS = {
    '🎪': 'Z1_CENTRAL_ATRIUM',
    '🏛️': 'Z2_UPPER_RING',
    '🛤️': 'Z3_LOWER_RING',
    '🍽️': 'Z4_FOOD_COURT',
    '⬆️': 'Z5_ESCALATOR_WELLS',
    '🏬': 'Z5_ANCHOR_STORES',
    '🍔': 'Z6_MICKEYS_WING',
    '🎬': 'Z6_THEATER',
    '🔻': 'Z7_SUBTERRANEAN',
    '🌐': 'Z9_EXTERIOR',
}

# Features (Architectural Elements)
FEATURE_SYMBOLS = {
    '⛲': 'FOUNTAIN_TERRACED',
    '🟨': 'TENSILE_MAST',
    '🕸️': 'CABLE_ARRAY',
    '🧱': 'GLASS_BLOCK_WALL',
    '🚡': 'ESCALATOR_PAIR',
    '🚪': 'ELEVATOR_DOORS',
    '💎': 'GLASS_ELEVATOR_TOWER',
    '🔵': 'METAL_RAILING_BLUE',
    '🟢': 'METAL_RAILING_GREEN',
    '🟫': 'TERRACOTTA_SCALLOP',
}


# ============================================================================
# REVERSE LOOKUPS
# ============================================================================

def symbol_to_name(symbol: str) -> Optional[str]:
    """Convert symbol to human-readable name."""
    all_mappings = {**ITEM_SYMBOLS, **NPC_SYMBOLS, **ZONE_SYMBOLS, **FEATURE_SYMBOLS}
    return all_mappings.get(symbol)


def name_to_symbol(name: str) -> Optional[str]:
    """Convert name to symbol (reverse lookup)."""
    all_mappings = {**ITEM_SYMBOLS, **NPC_SYMBOLS, **ZONE_SYMBOLS, **FEATURE_SYMBOLS}
    reverse = {v: k for k, v in all_mappings.items()}
    return reverse.get(name)


def get_category(symbol: str) -> Optional[str]:
    """Determine category from symbol."""
    if symbol in ITEM_SYMBOLS:
        return "ITEM"
    elif symbol in NPC_SYMBOLS:
        return "NPC"
    elif symbol in ZONE_SYMBOLS:
        return "ZONE"
    elif symbol in FEATURE_SYMBOLS:
        return "FEATURE"
    return None


# ============================================================================
# SYMBOL ENTITY BUILDER
# ============================================================================

class WingdingsRegistry:
    """Registry for symbol-based entity management."""

    def __init__(self):
        self.entities: Dict[str, SymbolEntity] = {}

    def register(self, symbol: str, name: str, category: str, properties: Dict[str, Any]):
        """Register a new symbol entity."""
        self.entities[symbol] = SymbolEntity(
            symbol=symbol,
            name=name,
            category=category,
            properties=properties
        )

    def get(self, symbol: str) -> Optional[SymbolEntity]:
        """Get entity by symbol."""
        return self.entities.get(symbol)

    def get_by_name(self, name: str) -> Optional[SymbolEntity]:
        """Get entity by human-readable name."""
        for entity in self.entities.values():
            if entity.name == name:
                return entity
        return None

    def list_by_category(self, category: str) -> list:
        """List all entities in a category."""
        return [e for e in self.entities.values() if e.category == category]


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_symbol_map() -> Dict[str, str]:
    """Export complete symbol → name mapping."""
    return {
        **ITEM_SYMBOLS,
        **NPC_SYMBOLS,
        **ZONE_SYMBOLS,
        **FEATURE_SYMBOLS
    }


def export_renpy_defines() -> str:
    """Export Ren'Py define statements for all symbols."""
    lines = []
    lines.append("# Wingdings Symbol Registry - Auto-generated")
    lines.append("# Symbols are the primary identifiers")
    lines.append("")

    lines.append("# Items")
    for symbol, name in ITEM_SYMBOLS.items():
        lines.append(f'define ITEM_{name} = "{symbol}"')

    lines.append("")
    lines.append("# NPCs")
    for symbol, name in NPC_SYMBOLS.items():
        lines.append(f'define NPC_{name} = "{symbol}"')

    lines.append("")
    lines.append("# Zones")
    for symbol, name in ZONE_SYMBOLS.items():
        lines.append(f'define ZONE_{name} = "{symbol}"')

    lines.append("")
    lines.append("# Features")
    for symbol, name in FEATURE_SYMBOLS.items():
        lines.append(f'define FEATURE_{name} = "{symbol}"')

    return "\n".join(lines)


# ============================================================================
# CLI TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("WINGDINGS REGISTRY TEST")
    print("=" * 80)

    print("\n[ITEM SYMBOLS]")
    for symbol, name in list(ITEM_SYMBOLS.items())[:5]:
        print(f"  {symbol} → {name}")

    print("\n[NPC SYMBOLS]")
    for symbol, name in list(NPC_SYMBOLS.items())[:5]:
        print(f"  {symbol} → {name}")

    print("\n[ZONE SYMBOLS]")
    for symbol, name in list(ZONE_SYMBOLS.items())[:5]:
        print(f"  {symbol} → {name}")

    print("\n[REVERSE LOOKUP]")
    print(f"  '🧹' → {symbol_to_name('🧹')}")
    print(f"  'UNIT_7_JANITOR' → {name_to_symbol('UNIT_7_JANITOR')}")

    print("\n[REN'PY EXPORT]")
    print(export_renpy_defines()[:200] + "...")

    print("\n" + "=" * 80)
