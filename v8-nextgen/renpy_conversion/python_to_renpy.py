#!/usr/bin/env python3
"""
PYTHON TO REN'PY CONVERTER
Main conversion orchestrator using probe telemetry format.

Converts v8-nextgen Python scripts to Ren'Py primitives using:
  - Measurements as source of truth (escalator/elevator)
  - Wingdings symbol assignment (stacked hierarchies)
  - GeoJSON spatial format
  - Probe telemetry data structures
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from measurements_loader import MeasurementsLoader
from voxel_object_loader import VoxelObjectRegistry, build_voxels_from_png

# Import conversion modules
from symbol_stacking import (
    SymbolStack, SymbolHierarchy, build_mall_hierarchy,
    stack_to_renpy_define, stack_to_geojson_feature,
    create_source_of_truth_stacks
)
from wingdings_registry import export_renpy_defines
from probe_telemetry_format import (
    ProbePacket, ItemTelemetry, ZoneTelemetry, EntityType,
    generate_renpy_displayable
)


# ============================================================================
# OUTPUT STRUCTURE
# ============================================================================

class RenpyConverter:
    """Main converter orchestrating Python → Ren'Py conversion."""

    def __init__(self, v8_root: Path):
        self.v8_root = v8_root
        self.output_root = v8_root / "renpy_output" / "game"
        self.ml = MeasurementsLoader()
        self.hierarchy = build_mall_hierarchy()

        # Create output directories
        (self.output_root / "objects").mkdir(parents=True, exist_ok=True)
        (self.output_root / "zones").mkdir(parents=True, exist_ok=True)
        (self.output_root / "python").mkdir(parents=True, exist_ok=True)
        (self.output_root / "geojson").mkdir(parents=True, exist_ok=True)

    # ========================================================================
    # MEASUREMENTS → REN'PY
    # ========================================================================

    def convert_measurements(self) -> str:
        """
        Convert measurements_loader.py data to Ren'Py defines.

        Source of truth: Escalator (8 feet) + Elevator (3.5' × 6.75')
        """
        lines = []
        lines.append("# " + "=" * 76)
        lines.append("# MEASUREMENTS - Source of Truth")
        lines.append("# Auto-generated from measurements_loader.py")
        lines.append("# " + "=" * 76)
        lines.append("")

        # Critical measurement anchors
        lines.append("# MEASUREMENT ANCHORS (Deep Space Probe Calibration)")
        lines.append("# These are HIGH confidence - verified measurements")
        lines.append("")

        escalator_drop = self.ml.get_spatial('food_court.pit_depth_feet.value')
        lines.append(f"define ESCALATOR_DROP_FEET = {escalator_drop}")
        lines.append("define ESCALATOR_STEP_COUNT = 12")
        lines.append("define ESCALATOR_STEP_RISE_INCHES = 8")
        lines.append("")

        lines.append("define ELEVATOR_DOOR_WIDTH_FEET = 3.5  # Commercial standard")
        lines.append("define ELEVATOR_DOOR_HEIGHT_FEET = 6.75  # Commercial standard")
        lines.append("")

        # All spatial measurements
        lines.append("# SPATIAL MEASUREMENTS")
        atrium_diameter = self.ml.get_spatial('atrium.diameter_feet.value')
        atrium_height = self.ml.get_spatial('atrium.ceiling_height_feet.value')
        mast_height = self.ml.get_spatial('tensile_roof.mast_height_feet.value')
        cable_count = self.ml.get_spatial('tensile_roof.cable_count.value')

        lines.append(f"define ATRIUM_DIAMETER_FEET = {atrium_diameter}")
        lines.append(f"define ATRIUM_HEIGHT_FEET = {atrium_height}")
        lines.append(f"define MAST_HEIGHT_FEET = {mast_height}")
        lines.append(f"define CABLE_COUNT = {cable_count}")
        lines.append("")

        # Scale factors
        lines.append("# SCALE FACTORS (v5 corrections)")
        factors = self.ml.get_voxel_scale_factors()
        lines.append(f"define SCALE_ATRIUM_FACTOR = {factors['atrium_diameter_factor']}")
        lines.append(f"define SCALE_MAST_FACTOR = {factors['mast_height_factor']}")
        lines.append("")

        return "\n".join(lines)

    # ========================================================================
    # VOXEL OBJECTS → REN'PY
    # ========================================================================

    def convert_voxel_object(self, obj_id: str, obj_data: Dict[str, Any], symbol: str) -> str:
        """Convert a single voxel object to Ren'Py definition."""
        lines = []
        lines.append(f"# Voxel Object: {obj_id}")
        lines.append(f"# Symbol: {symbol}")
        lines.append(f"# Source: {obj_data.get('source_image', 'N/A')}")
        lines.append("")

        # Create probe telemetry
        qbit = obj_data.get('qbit', {})
        # Calculate QBIT aggregate (filter numeric values only)
        if isinstance(qbit, dict):
            qbit_aggregate = sum(v for v in qbit.values() if isinstance(v, (int, float)))
        else:
            qbit_aggregate = 0

        lines.append(f"define voxel_{obj_id.lower()} = {{")
        lines.append(f'    "symbol": "{symbol}",')
        lines.append(f'    "obj_id": "{obj_id}",')
        lines.append(f'    "qbit": {json.dumps(qbit, indent=4)},')
        lines.append(f'    "qbit_aggregate": {qbit_aggregate},')
        lines.append(f'    "placement": {json.dumps(obj_data.get("placement", {}))},')
        lines.append(f'    "behavior": {json.dumps(obj_data.get("behavior", {}))},')
        lines.append(f"    # Probe telemetry format")
        lines.append(f'    "entity_type": {EntityType.ITEM.value},')
        lines.append(f"}}")
        lines.append("")

        # Create interaction label
        behavior = obj_data.get('behavior', {})
        if behavior.get('type') == 'NPC_PROP':
            on_pickup = behavior.get('on_pickup', [])
            lines.append(f"label interact_{obj_id.lower()}:")
            lines.append(f'    show voxel_{obj_id.lower()} at center')
            lines.append("")

            for action in on_pickup:
                if action.startswith('subtitle:'):
                    subtitle = action.split(':', 1)[1].strip().strip("'\"")
                    lines.append(f'    "{subtitle}"')
                elif '+' in action:
                    # Parse cloud_pressure+2
                    var, delta = action.split('+')
                    lines.append(f"    $ {var} += {delta}")

            lines.append("")
            lines.append("    return")
            lines.append("")

        return "\n".join(lines)

    def convert_all_voxel_objects(self):
        """Convert all voxel objects in the registry."""
        # Load voxel object definitions directly from JSON
        voxel_dir = self.v8_root / "data" / "voxel_objects"
        registry_file = voxel_dir / "voxel_objects_registry.json"

        if not registry_file.exists():
            print(f"Warning: {registry_file} not found")
            return

        registry_data = json.loads(registry_file.read_text())

        # Import symbol mappings
        from wingdings_registry import ITEM_SYMBOLS, name_to_symbol

        for obj_name, obj_info in registry_data.get("objects", {}).items():
            obj_file = voxel_dir / obj_info["file"]
            if not obj_file.exists():
                continue

            obj_data = json.loads(obj_file.read_text())
            obj_id = obj_data.get("voxel_object_id", obj_name)

            # Get symbol
            symbol = name_to_symbol(obj_id)
            if not symbol:
                print(f"Warning: No symbol found for {obj_id}")
                continue

            # Convert
            renpy_code = self.convert_voxel_object(obj_id, obj_data, symbol)

            # Write to file
            output_file = self.output_root / "objects" / f"{obj_id.lower()}.rpy"
            output_file.write_text(renpy_code)
            print(f"✓ {obj_id} → {output_file}")

    # ========================================================================
    # ZONES → GEOJSON + REN'PY
    # ========================================================================

    def convert_zones_to_geojson(self) -> Dict[str, Any]:
        """Convert all zones to GeoJSON with symbol stacks."""
        features = []

        for zone_id in self.ml.zones.keys():
            zone = self.ml.get_zone(zone_id)

            # Create symbol stack
            from wingdings_registry import name_to_symbol
            symbol = name_to_symbol(zone_id)
            if not symbol:
                continue

            stack = SymbolStack(['🏬', symbol])

            # Simplified geometry (center points for now)
            geometry = {
                "type": "Point",
                "coordinates": [0, 0, zone.get("elevation_feet", 0)]
            }

            properties = {
                "zone_id": zone_id,
                "name": zone.get("name", ""),
                "level": zone.get("level", 0),
                "elevation_feet": zone.get("elevation_feet", 0),
            }

            # Add measurements
            if "pit_depth_feet" in zone:
                properties["pit_depth_feet"] = zone["pit_depth_feet"].get("value")
            if "diameter_feet" in zone:
                properties["diameter_feet"] = zone["diameter_feet"].get("value")

            feature = stack_to_geojson_feature(stack, geometry, properties)
            features.append(feature)

        # Add measurement anchors
        anchors = create_source_of_truth_stacks()
        for stack in anchors:
            geometry = {"type": "Point", "coordinates": [0, -100, -8]}
            feature = stack_to_geojson_feature(stack, geometry, stack.metadata)
            features.append(feature)

        geojson = {
            "type": "FeatureCollection",
            "metadata": {
                "version": "v8-renpy-geojson-1.0",
                "source": "python_to_renpy.py",
                "coordinate_system": "Mall Cartesian (feet)",
                "origin": "Central Atrium center",
            },
            "features": features
        }

        return geojson

    # ========================================================================
    # MAIN ORCHESTRATION
    # ========================================================================

    def convert_all(self):
        """Run all conversions."""
        print("=" * 80)
        print("PYTHON → REN'PY CONVERSION (Deep Space Probe Format)")
        print("=" * 80)

        # 1. Measurements
        print("\n[1/4] Converting measurements...")
        measurements_rpy = self.convert_measurements()
        measurements_file = self.output_root / "measurements_store.rpy"
        measurements_file.write_text(measurements_rpy)
        print(f"✓ Measurements → {measurements_file}")

        # 2. Wingdings registry
        print("\n[2/4] Generating symbol registry...")
        symbols_rpy = export_renpy_defines()
        symbols_file = self.output_root / "symbol_registry.rpy"
        symbols_file.write_text(symbols_rpy)
        print(f"✓ Symbols → {symbols_file}")

        # 3. Voxel objects
        print("\n[3/4] Converting voxel objects...")
        self.convert_all_voxel_objects()

        # 4. Zones to GeoJSON
        print("\n[4/4] Converting zones to GeoJSON...")
        zones_geojson = self.convert_zones_to_geojson()
        geojson_file = self.output_root / "geojson" / "mall_zones.geojson"
        geojson_file.write_text(json.dumps(zones_geojson, indent=2))
        print(f"✓ Zones GeoJSON → {geojson_file}")

        # Create main script.rpy
        print("\n[FINAL] Creating main script...")
        self.create_main_script()

        print("\n" + "=" * 80)
        print("CONVERSION COMPLETE")
        print(f"Output: {self.output_root}")
        print("=" * 80)

    def create_main_script(self):
        """Create the main Ren'Py script.rpy file."""
        script = """# GLITCHDEXMALLv7 - v8 NextGen Ren'Py Conversion
# Deep Space Probe Telemetry Format Applied to Mall Simulation

# Import measurements (source of truth)
$ import_measurements = True

# Import symbol registry
$ import_symbols = True

# Initialize game state
init python:
    # Cloud pressure system
    cloud_pressure = 0

    # Probe telemetry registry
    probe_entities = {}

    # Load GeoJSON spatial data
    import json
    from pathlib import Path
    geojson_path = Path(config.gamedir) / "geojson" / "mall_zones.geojson"
    if geojson_path.exists():
        with open(geojson_path) as f:
            spatial_data = json.load(f)

# Start label
label start:
    scene black

    "GLITCHDEXMALL v8"
    "Deep Space Probe Telemetry Format"
    "Same shape, different application."

    menu:
        "Where would you like to go?"

        "Central Atrium (🎪)":
            jump zone_central_atrium

        "Food Court (🍽️)":
            jump zone_food_court

        "Escalator Wells (⬆️)":
            jump zone_escalator_wells

    return

# Zone labels
label zone_central_atrium:
    scene atrium
    "You stand in the central atrium."
    "Diameter: [ATRIUM_DIAMETER_FEET] feet"
    "Height: [ATRIUM_HEIGHT_FEET] feet"
    jump start

label zone_food_court:
    scene food_court
    "You descend to the food court."
    "Drop: [ESCALATOR_DROP_FEET] feet (12 steps × 8 inches)"
    jump start

label zone_escalator_wells:
    scene escalator
    "The escalators hum quietly."
    "Vertical travel: [ESCALATOR_DROP_FEET] feet"
    "Source of truth: Verified measurement"
    jump start
"""
        script_file = self.output_root / "script.rpy"
        script_file.write_text(script)
        print(f"✓ Main script → {script_file}")


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Run the conversion."""
    v8_root = Path(__file__).parent.parent
    converter = RenpyConverter(v8_root)
    converter.convert_all()


if __name__ == "__main__":
    main()
