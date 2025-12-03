#!/usr/bin/env python3
"""
VOXEL BUILDER - V7 NextGen
Foundation for voxel-style mall dungeon doom-alike construction.

Uses CRD measurements from v5 integration as construction blueprints.
Generates voxel geometry for zones based on measured dimensions.

For: 3 credit cards as weapons in giant mall dungeon doom-alike
"""

import json
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

try:
    from measurements_loader import load_measurements, MeasurementsLoader
except ImportError:
    print("Warning: measurements_loader not found. Using fallback.")
    MeasurementsLoader = None


# ============================================================================
# CONSTANTS
# ============================================================================

VOXEL_SIZE = 1.0  # 1 voxel = 1 foot (adjustable)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class VoxelBox:
    """A voxel bounding box (AABB)."""
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    z_min: float
    z_max: float
    zone_id: str
    material: str = "default"

    def get_dimensions(self) -> Tuple[float, float, float]:
        """Get width, depth, height."""
        return (
            self.x_max - self.x_min,
            self.y_max - self.y_min,
            self.z_max - self.z_min
        )

    def get_volume_voxels(self) -> int:
        """Get volume in voxels."""
        w, d, h = self.get_dimensions()
        return math.ceil(w / VOXEL_SIZE) * math.ceil(d / VOXEL_SIZE) * math.ceil(h / VOXEL_SIZE)


@dataclass
class VoxelCylinder:
    """A cylindrical voxel volume (for atrium, fountain, etc.)."""
    center_x: float
    center_y: float
    radius_feet: float
    z_min: float
    z_max: float
    zone_id: str
    material: str = "default"


@dataclass
class VoxelMesh:
    """Complete voxel mesh for the mall."""
    boxes: List[VoxelBox]
    cylinders: List[VoxelCylinder]
    metadata: Dict

    def export_json(self, filepath: str):
        """Export to JSON for external voxel engines."""
        data = {
            "version": "7.0.0-alpha",
            "voxel_size": VOXEL_SIZE,
            "boxes": [
                {
                    "zone_id": box.zone_id,
                    "bounds": [box.x_min, box.x_max, box.y_min, box.y_max, box.z_min, box.z_max],
                    "dimensions_feet": box.get_dimensions(),
                    "volume_voxels": box.get_volume_voxels(),
                    "material": box.material
                }
                for box in self.boxes
            ],
            "cylinders": [
                {
                    "zone_id": cyl.zone_id,
                    "center": [cyl.center_x, cyl.center_y],
                    "radius_feet": cyl.radius_feet,
                    "z_range": [cyl.z_min, cyl.z_max],
                    "material": cyl.material
                }
                for cyl in self.cylinders
            ],
            "metadata": self.metadata
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return filepath


# ============================================================================
# VOXEL BUILDER
# ============================================================================

class VoxelBuilder:
    """
    Builds voxel geometry from CRD measurements.

    Usage:
        builder = VoxelBuilder()
        mesh = builder.build_full_mall()
        mesh.export_json("mall_voxels.json")

    For doom-alike integration:
        - Use boxes for collision detection
        - Use z-levels for vertical gameplay
        - Use materials for visual/gameplay properties
    """

    def __init__(self):
        if MeasurementsLoader:
            self.ml = load_measurements()
        else:
            self.ml = None
            print("Warning: Running without measurements loader. Using hardcoded dimensions.")

        self.boxes = []
        self.cylinders = []
        self.metadata = {
            "source": "v7 CRD measurements + v6 QBIT systems",
            "scale": "Space station - 1M+ sq ft megastructure",
            "voxel_size_feet": VOXEL_SIZE
        }

    def build_full_mall(self) -> VoxelMesh:
        """Build complete mall voxel mesh."""
        print("Building voxel mesh for 1M+ sq ft mall...")

        # Build zones in order
        self._build_atrium()
        self._build_food_court()
        self._build_corridors()
        self._build_anchor_stores()
        self._build_mickeys_wing()
        self._build_escalators()

        mesh = VoxelMesh(
            boxes=self.boxes,
            cylinders=self.cylinders,
            metadata=self.metadata
        )

        print(f"Built {len(self.boxes)} boxes, {len(self.cylinders)} cylinders")
        total_volume = sum(b.get_volume_voxels() for b in self.boxes)
        print(f"Total volume: ~{total_volume:,} voxels")

        return mesh

    def _build_atrium(self):
        """Build Z1 - Central Atrium (175' diameter)."""
        print("  Building Z1 - Central Atrium...")

        if self.ml:
            diameter = self.ml.get_spatial("atrium.diameter_feet.value", 175)
            ceiling_height = self.ml.get_spatial("atrium.ceiling_height_feet.value", 70)
        else:
            diameter = 175
            ceiling_height = 70

        radius = diameter / 2.0

        # Atrium as cylinder
        atrium_cyl = VoxelCylinder(
            center_x=0,
            center_y=0,
            radius_feet=radius,
            z_min=0,
            z_max=ceiling_height,
            zone_id="Z1_CENTRAL_ATRIUM",
            material="atrium_space"
        )
        self.cylinders.append(atrium_cyl)

        # Fountain (within atrium)
        fountain_cyl = VoxelCylinder(
            center_x=-20,  # Offset from atrium center
            center_y=0,
            radius_feet=15,  # Estimated from 22.5' arc
            z_min=0,
            z_max=6,  # 4 tiers, 6' total depth
            zone_id="Z1_FOUNTAIN",
            material="fountain_tiers"
        )
        self.cylinders.append(fountain_cyl)

        print(f"    Atrium: {diameter}' diameter, {ceiling_height}' ceiling")

    def _build_food_court(self):
        """Build Z4 - Food Court Bowl (120' diameter, 8' below ground)."""
        print("  Building Z4 - Food Court...")

        if self.ml:
            zone_data = self.ml.get_zone("Z4_FOOD_COURT")
            diameter = zone_data.get("diameter_feet", {}).get("value", 120)
            pit_depth = zone_data.get("pit_depth_feet", {}).get("value", 8)
            vertical_clearance = zone_data.get("vertical_clearance_feet", {}).get("value", 50)
        else:
            diameter = 120
            pit_depth = 8
            vertical_clearance = 50

        radius = diameter / 2.0

        # Food court bowl (sunken)
        fc_cyl = VoxelCylinder(
            center_x=100,  # Offset from atrium (adjacent)
            center_y=0,
            radius_feet=radius,
            z_min=-pit_depth,  # Z=-1 level
            z_max=vertical_clearance - pit_depth,  # To tensile roof above
            zone_id="Z4_FOOD_COURT",
            material="food_court_bowl"
        )
        self.cylinders.append(fc_cyl)

        print(f"    Food Court: {diameter}' diameter, {pit_depth}' deep, {vertical_clearance}' clearance")

    def _build_corridors(self):
        """Build Z2/Z3 - Ring Corridors."""
        print("  Building Z2/Z3 - Corridors...")

        if self.ml:
            main_width = self.ml.get_spatial("corridors.main_spine_width_feet.value", 25)
            standard_width = self.ml.get_spatial("corridors.standard_corridor_width_feet.value", 18)
            ceiling = self.ml.get_spatial("corridors.ceiling_height_feet.value", 12)
        else:
            main_width = 25
            standard_width = 18
            ceiling = 12

        # Simplified: Create a few corridor segments
        # (Full implementation would generate ring topology)

        # Main spine corridor (Z3)
        corridor_1 = VoxelBox(
            x_min=-200,
            x_max=200,
            y_min=-main_width / 2,
            y_max=main_width / 2,
            z_min=0,
            z_max=ceiling,
            zone_id="Z3_LOWER_RING",
            material="corridor_floor"
        )
        self.boxes.append(corridor_1)

        # Perpendicular corridor
        corridor_2 = VoxelBox(
            x_min=-standard_width / 2,
            x_max=standard_width / 2,
            y_min=-200,
            y_max=200,
            z_min=0,
            z_max=ceiling,
            zone_id="Z3_LOWER_RING",
            material="corridor_floor"
        )
        self.boxes.append(corridor_2)

        print(f"    Corridors: Main {main_width}', Standard {standard_width}', Ceiling {ceiling}'")

    def _build_anchor_stores(self):
        """Build Z5 - Anchor Stores (100,000+ sq ft each)."""
        print("  Building Z5 - Anchor Stores...")

        # West Anchor
        west_anchor = VoxelBox(
            x_min=-300,
            x_max=-150,
            y_min=-200,
            y_max=200,
            z_min=0,
            z_max=18,  # Higher ceilings than corridors
            zone_id="Z5_WEST_ANCHOR",
            material="anchor_store_interior"
        )
        self.boxes.append(west_anchor)

        # East Anchor
        east_anchor = VoxelBox(
            x_min=150,
            x_max=300,
            y_min=-200,
            y_max=200,
            z_min=0,
            z_max=18,
            zone_id="Z5_EAST_ANCHOR",
            material="anchor_store_interior"
        )
        self.boxes.append(east_anchor)

        print(f"    Anchor Stores: 2 stores, ~100,000 sq ft each")

    def _build_mickeys_wing(self):
        """Build Z6 - Mickey's Family Restaurant Wing."""
        print("  Building Z6 - Mickey's Wing...")

        mickeys = VoxelBox(
            x_min=80,
            x_max=150,
            y_min=120,
            y_max=180,
            z_min=0,
            z_max=15,
            zone_id="Z6_MICKEYS_WING",
            material="restaurant_interior"
        )
        self.boxes.append(mickeys)

        print("    Mickey's Wing: Southeast exterior wing")

    def _build_escalators(self):
        """Build Z5 - Escalator Wells (vertical circulation)."""
        print("  Building Z5 - Escalator Wells...")

        if self.ml:
            step_count = self.ml.get_feature("escalator").get("step_count_food_court", {}).get("value", 12)
            pit_depth = 8  # From food court pit
        else:
            step_count = 12
            pit_depth = 8

        # Escalator well (transition zone)
        escalator_well = VoxelBox(
            x_min=50,
            x_max=75,
            y_min=-15,
            y_max=15,
            z_min=-pit_depth,  # Connects Z=0 to Z=-1
            z_max=0,
            zone_id="Z5_ESCALATOR_WELLS",
            material="escalator_shaft"
        )
        self.boxes.append(escalator_well)

        print(f"    Escalators: {step_count} steps, {pit_depth}' descent")

    # ========================================================================
    # EXPORT HELPERS
    # ========================================================================

    def export_doom_format(self, filepath: str):
        """
        Export in doom-alike friendly format.

        Simple box/cylinder list for collision detection and rendering.
        """
        data = {
            "version": "7.0.0-doom-alpha",
            "voxel_size": VOXEL_SIZE,
            "zones": []
        }

        # Group boxes by zone
        zones_dict = {}
        for box in self.boxes:
            if box.zone_id not in zones_dict:
                zones_dict[box.zone_id] = {
                    "zone_id": box.zone_id,
                    "boxes": [],
                    "cylinders": []
                }
            zones_dict[box.zone_id]["boxes"].append({
                "bounds": [box.x_min, box.x_max, box.y_min, box.y_max, box.z_min, box.z_max],
                "material": box.material
            })

        for cyl in self.cylinders:
            if cyl.zone_id not in zones_dict:
                zones_dict[cyl.zone_id] = {
                    "zone_id": cyl.zone_id,
                    "boxes": [],
                    "cylinders": []
                }
            zones_dict[cyl.zone_id]["cylinders"].append({
                "center": [cyl.center_x, cyl.center_y],
                "radius": cyl.radius_feet,
                "z_range": [cyl.z_min, cyl.z_max],
                "material": cyl.material
            })

        data["zones"] = list(zones_dict.values())

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Exported doom format: {filepath}")
        return filepath


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("VOXEL BUILDER - V7 MALL DUNGEON DOOM-ALIKE")
    print("=" * 80)
    print("Building 1,000,000+ sq ft megastructure from CRD measurements...")
    print()

    builder = VoxelBuilder()
    mesh = builder.build_full_mall()

    print()
    print("Exporting voxel mesh...")
    mesh.export_json("v7_mall_voxels.json")
    print("  → v7_mall_voxels.json (full mesh)")

    builder.export_doom_format("v7_mall_doom.json")
    print("  → v7_mall_doom.json (doom-alike format)")

    print()
    print("=" * 80)
    print("VOXEL BUILD COMPLETE")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Import v7_mall_doom.json into your voxel engine")
    print("  2. Apply materials/textures per zone")
    print("  3. Add player spawn points")
    print("  4. Equip 3 credit cards as weapons")
    print("  5. DOOM in the mall")
    print()
