#!/usr/bin/env python3
"""
JSON TO GEOJSON CONVERTER
Converts v8 measurement JSON files to GeoJSON format with spatial coordinates.

Source of truth: Escalator stairs (8 feet) + Elevator doors (3.5' x 6.75')
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from measurements_loader import MeasurementsLoader
from wingdings_registry import name_to_symbol, ZONE_SYMBOLS


# ============================================================================
# COORDINATE SYSTEM
# ============================================================================

# Origin: Center of Central Atrium
# Units: Feet
# +X: East
# +Y: North
# Z: Elevation (feet above ground floor)

ORIGIN = (0.0, 0.0, 0.0)  # Central Atrium center


# ============================================================================
# ZONE COORDINATE MAPPING
# ============================================================================

def get_zone_coordinates(zone_id: str, ml: MeasurementsLoader) -> Dict[str, Any]:
    """
    Calculate GeoJSON coordinates for a zone.
    Uses measurements_loader as source of truth.
    """
    zone = ml.get_zone(zone_id)

    # Base coordinates (simplified - assuming center points for now)
    coord_map = {
        "Z1_CENTRAL_ATRIUM": {
            "type": "Point",
            "coordinates": [0, 0, 0]  # Origin
        },
        "Z2_UPPER_RING": {
            "type": "Polygon",
            "coordinates": [[
                # Ring around atrium (approximation)
                [100, 100, 0],
                [100, -100, 0],
                [-100, -100, 0],
                [-100, 100, 0],
                [100, 100, 0]  # Close polygon
            ]]
        },
        "Z3_LOWER_RING": {
            "type": "Polygon",
            "coordinates": [[
                [150, 150, 0],
                [150, -150, 0],
                [-150, -150, 0],
                [-150, 150, 0],
                [150, 150, 0]
            ]]
        },
        "Z4_FOOD_COURT": {
            "type": "Point",
            "coordinates": [0, -120, -8]  # South of atrium, 8 feet down (escalator)
        },
        "Z5_ESCALATOR_WELLS": {
            "type": "LineString",
            "coordinates": [
                [0, -80, 0],   # Top of escalator (ground level)
                [0, -100, -8]  # Bottom of escalator (8 feet down)
            ]
        },
        "Z6_THEATER": {
            "type": "Point",
            "coordinates": [0, -140, -8]  # Behind food court, same elevation
        },
        "Z7_SUBTERRANEAN": {
            "type": "Polygon",
            "coordinates": [[
                [200, 200, -16],
                [200, -200, -16],
                [-200, -200, -16],
                [-200, 200, -16],
                [200, 200, -16]
            ]]
        },
    }

    return coord_map.get(zone_id, {"type": "Point", "coordinates": [0, 0, 0]})


# ============================================================================
# GEOJSON FEATURE BUILDER
# ============================================================================

def build_zone_feature(zone_id: str, ml: MeasurementsLoader) -> Dict[str, Any]:
    """Build a GeoJSON Feature for a zone."""
    zone = ml.get_zone(zone_id)
    symbol = name_to_symbol(zone_id)

    geometry = get_zone_coordinates(zone_id, ml)

    properties = {
        "symbol": symbol,  # Wingdings symbol ID
        "zone_id": zone_id,
        "name": zone.get("name", ""),
        "level": zone.get("level", 0),
        "elevation_feet": zone.get("elevation_feet", 0),
        "confidence": zone.get("confidence", "MEDIUM"),

        # Extract numeric measurements
        "measurements": {}
    }

    # Add all measurements
    for key, value in zone.items():
        if isinstance(value, dict) and "value" in value:
            properties["measurements"][key] = {
                "value": value["value"],
                "confidence": value.get("confidence", "MEDIUM"),
                "unit": "feet"
            }

    feature = {
        "type": "Feature",
        "id": symbol,  # Use symbol as primary ID
        "geometry": geometry,
        "properties": properties
    }

    return feature


def build_item_feature(item_id: str, position: Tuple[float, float, float], properties: Dict[str, Any]) -> Dict[str, Any]:
    """Build a GeoJSON Feature for an item (voxel object)."""
    from wingdings_registry import name_to_symbol

    symbol = name_to_symbol(item_id)

    feature = {
        "type": "Feature",
        "id": symbol,  # Use symbol as primary ID
        "geometry": {
            "type": "Point",
            "coordinates": list(position)  # [x, y, z] in feet
        },
        "properties": {
            "symbol": symbol,
            "item_id": item_id,
            **properties
        }
    }

    return feature


# ============================================================================
# MAIN CONVERSION
# ============================================================================

def convert_zones_to_geojson(ml: MeasurementsLoader) -> Dict[str, Any]:
    """Convert all zones to a GeoJSON FeatureCollection."""

    features = []

    for zone_id in ml.zones.keys():
        feature = build_zone_feature(zone_id, ml)
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "version": "v8-nextgen-geojson-1.0",
            "source": "measurements_loader.py",
            "coordinate_system": "Mall Cartesian (feet)",
            "origin": "Central Atrium center",
            "measurement_anchors": {
                "escalator_drop_feet": 8,
                "elevator_door_width_feet": 3.5,
                "elevator_door_height_feet": 6.75
            }
        },
        "features": features
    }

    return geojson


def convert_spatial_measurements_to_geojson(ml: MeasurementsLoader) -> Dict[str, Any]:
    """Convert spatial measurements to GeoJSON features."""

    features = []

    # Atrium feature
    atrium_diameter = ml.get_spatial("atrium.diameter_feet.value")
    features.append({
        "type": "Feature",
        "id": "⛲",  # Fountain symbol
        "geometry": {
            "type": "Point",
            "coordinates": [0, 0, 0]
        },
        "properties": {
            "symbol": "⛲",
            "feature_type": "ATRIUM",
            "diameter_feet": atrium_diameter,
            "ceiling_height_feet": ml.get_spatial("atrium.ceiling_height_feet.value"),
            "confidence": ml.get_spatial("atrium.diameter_feet.confidence")
        }
    })

    # Escalator wells feature (SOURCE OF TRUTH)
    features.append({
        "type": "Feature",
        "id": "⬆️",  # Escalator symbol
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [0, -80, 0],   # Top
                [0, -100, -8]  # Bottom (-8 feet from 12 steps × 8 inches)
            ]
        },
        "properties": {
            "symbol": "⬆️",
            "feature_type": "ESCALATOR_WELLS",
            "drop_feet": 8,
            "step_count": 12,
            "step_rise_inches": 8,
            "confidence": "HIGH",
            "note": "SOURCE OF TRUTH - verified measurement"
        }
    })

    # Elevator doors feature (SOURCE OF TRUTH)
    features.append({
        "type": "Feature",
        "id": "🚪",
        "geometry": {
            "type": "Point",
            "coordinates": [50, 50, 0]  # Example position
        },
        "properties": {
            "symbol": "🚪",
            "feature_type": "ELEVATOR_DOORS",
            "width_feet": 3.5,
            "height_feet": 6.75,
            "confidence": "HIGH",
            "note": "Commercial standard - SOURCE OF TRUTH"
        }
    })

    # Tensile roof masts
    mast_height = ml.get_spatial("tensile_roof.mast_height_feet.value")
    for i, pos in enumerate([(50, 50, 0), (-50, 50, 0), (-50, -50, 0), (50, -50, 0)]):
        features.append({
            "type": "Feature",
            "id": f"🟨_{i}",
            "geometry": {
                "type": "Point",
                "coordinates": list(pos)
            },
            "properties": {
                "symbol": "🟨",
                "feature_type": "TENSILE_MAST",
                "mast_number": i + 1,
                "height_feet": mast_height,
                "material": "Yellow lattice steel"
            }
        })

    geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "version": "v8-nextgen-spatial-1.0",
            "source": "spatial_measurements.json",
            "measurement_anchors": {
                "escalator_drop_feet": 8,
                "elevator_door_dimensions": "3.5' × 6.75'"
            }
        },
        "features": features
    }

    return geojson


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Convert all measurement JSON to GeoJSON."""

    ml = MeasurementsLoader()

    # Convert zones
    zones_geojson = convert_zones_to_geojson(ml)
    zones_output = Path(__file__).parent.parent / "data" / "geojson" / "zones.geojson"
    zones_output.parent.mkdir(exist_ok=True)
    zones_output.write_text(json.dumps(zones_geojson, indent=2))
    print(f"✓ Zones GeoJSON: {zones_output}")

    # Convert spatial measurements
    spatial_geojson = convert_spatial_measurements_to_geojson(ml)
    spatial_output = Path(__file__).parent.parent / "data" / "geojson" / "spatial_features.geojson"
    spatial_output.write_text(json.dumps(spatial_geojson, indent=2))
    print(f"✓ Spatial GeoJSON: {spatial_output}")

    print("\n[SAMPLE FEATURE]")
    print(json.dumps(zones_geojson["features"][0], indent=2))


if __name__ == "__main__":
    main()
