"""
Toddler V7 Integration - Reality Catalyst System

The Toddler is an invisible reality catalyst that amplifies instability wherever it goes.

From v2: Self-contained horror engine with behavioral states, visibility, and distortion.
In V7: Wired into Cloud (pressure amplifier), QBIT (zone agitator), and Leon (shared dread).

Key properties:
- position: Where it is in the mall
- behavior: WANDERING | CURIOUS | MANIFESTING | FLEEING | STATIC
- visibility: 0.0 (invisible) → 1.0 (fully manifested)
- reality_strain: How much it warps local space
- distortion_radius: Area of effect

Effects each tick:
- heat_multiplier: Amplifies Cloud pressure
- glitch_multiplier: Amplifies visual/audio glitches
- in_distortion_field: Player within effect radius
- reality_strain: Zone QBIT agitation intensity

Integration:
    from ai.toddler import ToddlerSystem

    toddler = ToddlerSystem(initial_pos, config)

    # Each tick
    effects = toddler.update(
        dt,
        player_position=player.pos,
        current_cloud=cloud.level,
        world_tiles=world.tiles
    )

    # Apply effects
    cloud.add_pressure("TODDLER", effects["heat_multiplier"])
    renderer.glitch_intensity = effects["glitch_multiplier"]
    qbit.agitate_zone(zone, effects["reality_strain"])

See: docs/TODDLER_V7_INTEGRATION.md for full specification

"It's not hostile. It's a catalyst. Its presence accelerates decay."
"""

__version__ = "1.0.0-alpha"
__all__ = ["ToddlerSystem", "ToddlerBehavior", "TODDLER_CONFIG"]

# Imports will be uncommented as we implement:
# from .toddler_system import ToddlerSystem
# from .toddler_behaviors import ToddlerBehavior
# from .toddler_config import TODDLER_CONFIG
