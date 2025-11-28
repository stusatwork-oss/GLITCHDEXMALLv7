"""
Objects - Interactive Mall Items and Environmental Nodes

Three categories of objects in V7:

1. **Cloud Relief Nodes** - Pressure release valves
   - Recycler Trash Can: Player-activated, cooldown-based
   - Reduces Cloud pressure, grants QBIT order bonus

2. **Consumables** - Personal comfort items
   - Slushee: Heat tolerance, Cloud relief, status effects
   - Can be purchased from vendors

3. **Environmental FX Nodes** - Reactive ambience
   - HOLOmister: Cloud-triggered mist + holograms
   - Glitches when Toddler nearby or Cloud critical

Usage:
    from objects import RecyclerTrashCan, SlusheeItem, HoloMister
    from objects import use_recycler, drink_slushee
"""

from __future__ import annotations

from .holomister import HoloMister, HoloMisterDefinition, HoloMisterEffects, HoloMisterState, HoloMisterTriggers
from .slushee import (
    SlusheeConsumptionResult,
    SlusheeDefinition,
    SlusheeEffects,
    SlusheeItem,
    SlusheeModifiers,
    SlusheeUsage,
    drink_slushee,
)

# Back-compat: Recycler lives in the root of src as an earlier prototype
try:  # pragma: no cover - optional dependency
    from objects.recycler import RecyclerTrashCan, use_recycler  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    RecyclerTrashCan = None  # type: ignore
    use_recycler = None  # type: ignore

__all__ = [
    "HoloMister",
    "HoloMisterDefinition",
    "HoloMisterEffects",
    "HoloMisterState",
    "HoloMisterTriggers",
    "SlusheeItem",
    "SlusheeDefinition",
    "SlusheeEffects",
    "SlusheeModifiers",
    "SlusheeUsage",
    "SlusheeConsumptionResult",
    "drink_slushee",
    "RecyclerTrashCan",
    "use_recycler",
]
