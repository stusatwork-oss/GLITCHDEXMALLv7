#!/usr/bin/env python3
"""
MALL VOXEL EXAMPLES - Emoji Layer Application
Demonstrates how to use emoji layers for mall-specific voxels.

Converts actual mall elements using multi-layer emoji encoding.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

from voxel_emoji_layers import (
    VoxelLayers,
    create_glass_block_voxel,
    create_escalator_step_voxel,
    create_fountain_water_voxel,
    create_neon_sign_voxel,
    create_janitor_mop_voxel,
    voxel_to_renpy_define,
    voxel_to_geojson_feature
)


# ============================================================================
# MALL-SPECIFIC VOXEL LIBRARY
# ============================================================================

def create_food_court_floor_voxel(x: float, y: float) -> VoxelLayers:
    """
    Food court tile (staggered geometry from photos).

    Elevation: -8 feet (escalator drop)
    """
    return VoxelLayers(
        position=(x, y, -8),
        material='🟫',      # Terracotta tile
        state='💩',         # Dirty (abandoned mall)
        behavior='🔒',      # Solid
        surface='🌑',       # Matte
        physics='🐌',       # Slow (sticky floor)
    )


def create_atrium_fountain_tier_voxel(tier: int, x: float, y: float) -> VoxelLayers:
    """
    Fountain tier voxel (4 tiers total from CRD).

    Each tier is ~3.5 feet tall
    """
    elevation = tier * 3.5

    return VoxelLayers(
        position=(x, y, elevation),
        material='💧',      # Water
        state='🌊',         # Flooded (when operational)
        behavior='🌬️',     # Passable
        surface='🌊',       # Ripples
        audio='🌊',        # Flowing water
        physics='⬇️',       # Sinks
    )


def create_tensile_mast_voxel(mast_num: int, x: float, y: float, z: float) -> VoxelLayers:
    """
    Yellow lattice tension mast (4 total, 70 feet tall).

    From measurements: MAST_HEIGHT_FEET = 70
    """
    return VoxelLayers(
        position=(x, y, z),
        material='🟨',      # Yellow metal steel
        state='✨',         # Pristine (iconic feature)
        behavior='🔒',      # Solid
        surface='🎨',       # Painted (yellow)
        audio='🌬️',        # Wind through lattice
        physics='🪨',       # Heavy
    )


def create_cable_voxel(cable_num: int, x: float, y: float, z: float) -> VoxelLayers:
    """
    Tensile roof cable (32 total from CRD HIGH confidence count).

    Radial configuration from mast tops
    """
    return VoxelLayers(
        position=(x, y, z),
        material='🟨',      # Metal steel (cable)
        state='⚡',         # Under tension
        behavior='🔒',      # Solid (non-passable)
        surface='🌓',       # Semi-gloss
        audio='🔔',        # Chime (wind)
        physics='🧲',       # Under tension (like magnetic attraction)
    )


def create_theater_entrance_voxel(x: float, y: float) -> VoxelLayers:
    """
    Theater entrance "blank black open mouth" from CRD.

    Elevation: -8 feet (food court level)
    Position: Center of food court bowl
    """
    return VoxelLayers(
        position=(x, y, -8),
        material='🔲',      # Void
        state='💀',         # Dead (abandoned theater)
        behavior='🚪',      # Door (entrance)
        surface='🌑',       # Matte black
        audio='👻',        # Silent/eerie
        physics='🌬️',     # Passable
    )


def create_neon_food_court_sign_voxel(x: float, y: float) -> VoxelLayers:
    """
    Circular FOOD COURT neon sign (6-8 feet diameter from v7).

    Elevation: Above food court (-8 feet + sign height)
    """
    return VoxelLayers(
        position=(x, y, -4),  # Suspended above food court
        material='🪟',      # Glass (neon tube)
        state='⚡',         # Powered (or unpowered in decline)
        behavior='💡',      # Light source
        surface='🌟',       # Sparkly
        audio='📻',        # Transformer hum
        physics='🪶',       # Light
    )


def create_blue_metal_railing_voxel(x: float, y: float, z: float) -> VoxelLayers:
    """
    Blue/green metal railing (upper ring corridors from CRD).

    Height: 42 inches (building code - HIGH confidence)
    """
    return VoxelLayers(
        position=(x, y, z),
        material='🟦',      # Metal aluminum (blue anodized)
        state='✨',         # Pristine
        behavior='🔒',      # Solid barrier
        surface='🌓',       # Semi-gloss
        physics='🪶',       # Light metal
    )


def create_coca_cola_vending_machine_voxel(x: float, y: float) -> VoxelLayers:
    """
    Coca-Cola vending machine (SCALE ANCHOR from CRD).

    Standard dimensions: ~6 feet tall × 3 feet wide
    """
    return VoxelLayers(
        position=(x, y, 0),
        material='🟥',      # Red metal
        state='🔌',         # Unplugged (abandoned)
        behavior='💡',      # Light source (when powered)
        surface='✨',       # Shiny
        audio='⚙️',        # Mechanical (compressor)
        physics='🪨',       # Heavy
    )


def create_escalator_handrail_voxel(x: float, y: float, z: float) -> VoxelLayers:
    """
    Escalator handrail (moving rubber).

    Verified dimensions from user:
    - Width: 24-34 inches average
    - Rise: 7-8 inches per step
    """
    return VoxelLayers(
        position=(x, y, z),
        material='⬛',      # Black rubber
        state='🕐',         # Active (moving)
        behavior='⬆️',      # Moves upward
        surface='🌑',       # Matte
        audio='⚙️',        # Mechanical hum
        physics='🍯',       # Sticky (grip texture)
    )


# ============================================================================
# VOXEL COLLECTIONS (By Zone)
# ============================================================================

def generate_z1_central_atrium_voxels() -> List[VoxelLayers]:
    """
    Generate voxels for Z1 Central Atrium.

    From CRD:
    - Diameter: 175 feet
    - Height: 70 feet
    - Contains: Fountain (4 tiers), 4 masts, 32 cables
    """
    voxels = []

    # Fountain tiers (4 levels)
    for tier in range(4):
        for i in range(8):  # 8 voxels per tier (simplified)
            angle = i * 45  # degrees
            radius = 20 - (tier * 3)  # Smaller at higher tiers
            x = radius * (1 if i % 4 < 2 else -1)
            y = radius * (1 if i % 2 == 0 else -1)
            voxels.append(create_atrium_fountain_tier_voxel(tier, x, y))

    # 4 Yellow lattice masts (70 feet tall)
    mast_positions = [(50, 50), (-50, 50), (-50, -50), (50, -50)]
    for i, (x, y) in enumerate(mast_positions):
        for z_level in range(0, 70, 10):  # Every 10 feet
            voxels.append(create_tensile_mast_voxel(i, x, y, z_level))

    return voxels


def generate_z4_food_court_voxels() -> List[VoxelLayers]:
    """
    Generate voxels for Z4 Food Court.

    From CRD:
    - Elevation: -8 feet (verified from escalator)
    - Diameter: 120 feet
    - Contains: Floor tiles, neon sign, theater entrance
    """
    voxels = []

    # Floor tiles (staggered geometry)
    for x in range(-60, 60, 2):
        for y in range(-60, 60, 2):
            # Create circular bowl
            distance = (x**2 + y**2) ** 0.5
            if distance < 60:
                voxels.append(create_food_court_floor_voxel(x, y))

    # FOOD COURT neon sign
    voxels.append(create_neon_food_court_sign_voxel(0, 0))

    # Theater entrance (at bowl center)
    voxels.append(create_theater_entrance_voxel(0, -60))

    return voxels


def generate_z5_escalator_wells_voxels() -> List[VoxelLayers]:
    """
    Generate voxels for Z5 Escalator Wells.

    From CRD HIGH confidence:
    - 12 steps × 8 inches = 8 feet drop
    - Width: 24-34 inches average
    - Bidirectional pair
    """
    voxels = []

    # Escalator steps (12 steps, going down)
    for step in range(12):
        z = -step * (8/12)  # 8 inches per step = 0.667 feet
        y = -80 - (step * 1.67)  # 18-22 inch tread depth (using 20")

        # Down escalator
        voxels.append(VoxelLayers((-2, y, z), material='🟨', state='🕐', behavior='⬇️', surface='🌓', audio='⚙️', physics='🏃'))

        # Up escalator (parallel)
        voxels.append(create_escalator_step_voxel((0, -100, z)))

    # Handrails
    for step in range(12):
        z = -step * (8/12) + 3.5  # 42 inches above step
        y = -80 - (step * 1.67)
        voxels.append(create_escalator_handrail_voxel(-3, y, z))
        voxels.append(create_escalator_handrail_voxel(3, y, z))

    return voxels


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_zone_voxels_to_renpy(zone_id: str, voxels: List[VoxelLayers], output_dir: Path):
    """Export zone voxels to Ren'Py .rpy file."""
    lines = []
    lines.append(f"# Zone: {zone_id}")
    lines.append(f"# Total voxels: {len(voxels)}")
    lines.append(f"# Generated from emoji layer system")
    lines.append("")

    for i, voxel in enumerate(voxels):
        voxel_id = f"{zone_id}_VOXEL_{i:04d}"
        lines.append(voxel_to_renpy_define(voxel, voxel_id))

    output_file = output_dir / f"{zone_id.lower()}_voxels.rpy"
    output_file.write_text('\n'.join(lines))
    print(f"✓ {zone_id}: {len(voxels)} voxels → {output_file}")


def export_zone_voxels_to_geojson(zone_id: str, voxels: List[VoxelLayers], output_dir: Path):
    """Export zone voxels to GeoJSON."""
    features = []

    for i, voxel in enumerate(voxels):
        voxel_id = f"{zone_id}_VOXEL_{i:04d}"
        features.append(voxel_to_geojson_feature(voxel, voxel_id))

    geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "zone_id": zone_id,
            "voxel_count": len(voxels),
            "encoding": "emoji_layers",
            "measurement_source": "CRD v7 + user-verified escalator dimensions"
        },
        "features": features
    }

    output_file = output_dir / f"{zone_id.lower()}_voxels.geojson"
    output_file.write_text(json.dumps(geojson, indent=2))
    print(f"✓ {zone_id}: GeoJSON → {output_file}")


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Generate all mall zone voxels with emoji layers."""
    print("=" * 80)
    print("MALL VOXEL GENERATION - Emoji Layer Application")
    print("=" * 80)

    output_base = Path(__file__).parent.parent / "renpy_output" / "game"
    voxels_dir = output_base / "voxels"
    geojson_dir = output_base / "geojson" / "zones"

    voxels_dir.mkdir(parents=True, exist_ok=True)
    geojson_dir.mkdir(parents=True, exist_ok=True)

    # Generate zones
    print("\n[Generating Z1 Central Atrium]")
    z1_voxels = generate_z1_central_atrium_voxels()
    export_zone_voxels_to_renpy("Z1_CENTRAL_ATRIUM", z1_voxels, voxels_dir)
    export_zone_voxels_to_geojson("Z1_CENTRAL_ATRIUM", z1_voxels, geojson_dir)

    print("\n[Generating Z4 Food Court]")
    z4_voxels = generate_z4_food_court_voxels()
    export_zone_voxels_to_renpy("Z4_FOOD_COURT", z4_voxels, voxels_dir)
    export_zone_voxels_to_geojson("Z4_FOOD_COURT", z4_voxels, geojson_dir)

    print("\n[Generating Z5 Escalator Wells]")
    z5_voxels = generate_z5_escalator_wells_voxels()
    export_zone_voxels_to_renpy("Z5_ESCALATOR_WELLS", z5_voxels, voxels_dir)
    export_zone_voxels_to_geojson("Z5_ESCALATOR_WELLS", z5_voxels, geojson_dir)

    print("\n" + "=" * 80)
    print(f"TOTAL VOXELS GENERATED: {len(z1_voxels) + len(z4_voxels) + len(z5_voxels)}")
    print("=" * 80)

    # Show example voxel
    print("\n[EXAMPLE VOXEL - Escalator Step]")
    example = z5_voxels[0]
    print(f"  Position: {example.position}")
    print(f"  Compact: {example.to_compact()}")
    print(f"  Material: {example.material} (METAL_STEEL)")
    print(f"  State: {example.state} (ACTIVE)")
    print(f"  Behavior: {example.behavior} (Moving up)")
    print(f"  Audio: {example.audio} (MECHANICAL_HUM)")
    print("")


if __name__ == "__main__":
    main()
