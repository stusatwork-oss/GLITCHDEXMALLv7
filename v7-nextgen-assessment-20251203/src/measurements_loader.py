#!/usr/bin/env python3
"""
MEASUREMENTS LOADER - V7 NextGen
Loads and validates CRD measurements from v5 integration.

This module provides access to the single source of truth for all
spatial measurements, preserving v5's CRD traceability while making
data accessible to v6's QBIT-based systems.

For voxel construction: Use this to get precise dimensions
For LLM narration: Access photo refs and narrative context
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


# ============================================================================
# PATHS
# ============================================================================

V7_ROOT = Path(__file__).parent.parent
MEASUREMENTS_DIR = V7_ROOT / "data" / "measurements"

SPATIAL_FILE = MEASUREMENTS_DIR / "spatial_measurements.json"
ZONES_FILE = MEASUREMENTS_DIR / "zone_measurements.json"
FEATURES_FILE = MEASUREMENTS_DIR / "feature_measurements.json"
CRD_FILE = MEASUREMENTS_DIR / "crd_traceability.json"


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Measurement:
    """A single measurement with confidence and traceability."""
    value: Any
    confidence: str  # HIGH, MEDIUM, LOW
    source: str
    photo_refs: List[str] = None
    note: str = ""

    def __post_init__(self):
        if self.photo_refs is None:
            self.photo_refs = []


# ============================================================================
# LOADER CLASS
# ============================================================================

class MeasurementsLoader:
    """
    Loads and provides access to CRD measurements.

    Usage:
        ml = MeasurementsLoader()
        atrium_diameter = ml.get_spatial("atrium.diameter_feet.value")  # 175
        confidence = ml.get_spatial("atrium.diameter_feet.confidence")  # "MEDIUM"

        # For voxel construction:
        zone_data = ml.get_zone("Z4_FOOD_COURT")
        pit_depth = zone_data["pit_depth_feet"]["value"]  # 8

        # For LLM narration with context:
        feature = ml.get_feature_with_context("fountain")
        # Returns full object with photo_refs, confidence, narrative notes
    """

    def __init__(self):
        self.spatial = None
        self.zones = None
        self.features = None
        self.crd = None
        self._load_all()

    def _load_all(self):
        """Load all measurement files."""
        with open(SPATIAL_FILE, 'r') as f:
            self.spatial = json.load(f)
        with open(ZONES_FILE, 'r') as f:
            self.zones = json.load(f)
        with open(FEATURES_FILE, 'r') as f:
            self.features = json.load(f)
        with open(CRD_FILE, 'r') as f:
            self.crd = json.load(f)

    def get_spatial(self, path: str, default=None):
        """
        Get spatial measurement by dot-notation path.

        Examples:
            get_spatial("atrium.diameter_feet.value") -> 175
            get_spatial("food_court.pit_depth_feet.value") -> 8
            get_spatial("global.total_footprint_sqft.value") -> 1000000
        """
        return self._get_nested(self.spatial, path, default)

    def get_zone(self, zone_id: str) -> Dict[str, Any]:
        """
        Get complete zone data by ID.

        Examples:
            get_zone("Z1_CENTRAL_ATRIUM")
            get_zone("Z4_FOOD_COURT")
        """
        return self.zones.get(zone_id, {})

    def get_feature(self, feature_id: str) -> Dict[str, Any]:
        """
        Get feature data by ID.

        Examples:
            get_feature("escalator")
            get_feature("fountain")
            get_feature("glass_blocks")
        """
        return self.features.get(feature_id, {})

    def get_feature_with_context(self, feature_id: str) -> Dict[str, Any]:
        """
        Get feature with full CRD context for LLM narration.

        Returns feature data + photo refs + confidence + narrative context.
        """
        feature = self.get_feature(feature_id)
        if not feature:
            return {}

        # Enrich with CRD traceability if available
        feature_enriched = feature.copy()
        feature_enriched["crd_context"] = self._get_crd_context_for_feature(feature_id)

        return feature_enriched

    def _get_crd_context_for_feature(self, feature_id: str) -> Dict[str, Any]:
        """Get CRD context for a feature (confidence levels, photo refs, etc.)."""
        # Search through high/medium/low confidence measurements
        for confidence_level in ["high_confidence_measurements", "medium_confidence_measurements", "low_confidence_measurements"]:
            measurements = self.crd.get(confidence_level, [])
            for m in measurements:
                if feature_id in m.get("id", ""):
                    return {
                        "confidence": m.get("confidence"),
                        "photo_refs": m.get("photo_refs", []),
                        "method": m.get("method", ""),
                        "source": m.get("source", "")
                    }
        return {}

    def _get_nested(self, data: Dict, path: str, default=None):
        """Navigate nested dict using dot notation."""
        keys = path.split('.')
        current = data
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            else:
                return default
            if current is None:
                return default
        return current

    # ========================================================================
    # VOXEL CONSTRUCTION HELPERS
    # ========================================================================

    def get_voxel_scale_factors(self) -> Dict[str, float]:
        """
        Get scale factors for voxel construction.

        Returns corrections from v5 scale changes.
        Useful for adjusting v6 voxel models to v7 "space station scale".
        """
        return {
            "atrium_diameter_factor": self.get_spatial("atrium.diameter_feet.correction_factor", 2.5),
            "mast_height_factor": self.get_spatial("tensile_roof.mast_height_feet.correction_factor", 2.0),
            "cable_span_factor": self.get_spatial("tensile_roof.cable_span_feet.correction_factor", 2.0),
            "note": "v5 SCALE CORRECTION - multiply old dimensions by these factors"
        }

    def get_zone_dimensions_for_voxel(self, zone_id: str) -> Dict[str, Any]:
        """
        Get zone dimensions formatted for voxel construction.

        Returns simplified dict with just the numeric values needed for building.
        """
        zone = self.get_zone(zone_id)
        if not zone:
            return {}

        result = {
            "zone_id": zone_id,
            "name": zone.get("name", ""),
            "level": zone.get("level", 0),
            "elevation_feet": zone.get("elevation_feet", 0)
        }

        # Extract numeric dimensions
        for key, value in zone.items():
            if isinstance(value, dict) and "value" in value:
                result[key] = value["value"]
            elif isinstance(value, (int, float)):
                result[key] = value

        return result

    # ========================================================================
    # LLM NARRATION HELPERS
    # ========================================================================

    def get_architectural_context(self) -> Dict[str, Any]:
        """
        Get full architectural context for LLM DM narration.

        Returns KKT design intent, cultural context, scale philosophy.
        Perfect for flavor text and narrative generation.
        """
        return self.crd.get("architectural_significance", {})

    def get_timeline_contradictions(self) -> Dict[str, Any]:
        """
        Get timeline contradictions for multi-era narration.

        User answer 8-B: Use Cloud/mood states to toggle between eras.
        This provides the data for that system.
        """
        return self.crd.get("timeline_contradictions", {})

    def get_photo_refs_for_zone(self, zone_id: str) -> List[str]:
        """Get all photo references for a zone (for LLM context)."""
        zone = self.get_zone(zone_id)
        return zone.get("photo_refs", [])

    # ========================================================================
    # VALIDATION
    # ========================================================================

    def validate_measurements(self) -> Dict[str, Any]:
        """
        Validate all measurements for consistency.

        Returns report of any issues or warnings.
        """
        warnings = []
        errors = []

        # Check that critical measurements exist
        critical = [
            ("atrium.diameter_feet.value", "Atrium diameter"),
            ("food_court.pit_depth_feet.value", "Food court pit depth"),
            ("tensile_roof.mast_height_feet.value", "Mast height"),
            ("tensile_roof.cable_count", "Cable count")
        ]

        for path, name in critical:
            value = self.get_spatial(path)
            if value is None:
                errors.append(f"MISSING CRITICAL MEASUREMENT: {name} ({path})")

        # Check that all zones exist
        expected_zones = [
            "Z1_CENTRAL_ATRIUM", "Z2_UPPER_RING", "Z3_LOWER_RING",
            "Z4_FOOD_COURT", "Z5_ESCALATOR_WELLS", "Z5_ANCHOR_STORES",
            "Z6_MICKEYS_WING", "Z6_THEATER", "Z7_SUBTERRANEAN", "Z9_EXTERIOR"
        ]

        for zone_id in expected_zones:
            if zone_id not in self.zones:
                warnings.append(f"Missing zone definition: {zone_id}")

        # Check confidence levels
        low_confidence = []
        for key, zone in self.zones.items():
            if isinstance(zone, dict) and zone.get("confidence") == "LOW":
                low_confidence.append(key)

        return {
            "status": "ERROR" if errors else ("WARNING" if warnings else "OK"),
            "errors": errors,
            "warnings": warnings,
            "low_confidence_zones": low_confidence,
            "total_zones": len(self.zones),
            "total_features": len(self.features)
        }


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def load_measurements() -> MeasurementsLoader:
    """Convenience function to load measurements."""
    return MeasurementsLoader()


def get_scale_corrected_value(old_value: float, measurement_type: str) -> float:
    """
    Apply v5 scale corrections to old v6 values.

    Args:
        old_value: Original v6 dimension
        measurement_type: "atrium_diameter", "mast_height", or "cable_span"

    Returns:
        Scale-corrected value for v7

    Examples:
        get_scale_corrected_value(70, "atrium_diameter") -> 175
        get_scale_corrected_value(35, "mast_height") -> 70
    """
    ml = load_measurements()
    factors = ml.get_voxel_scale_factors()

    factor_map = {
        "atrium_diameter": factors.get("atrium_diameter_factor", 2.5),
        "mast_height": factors.get("mast_height_factor", 2.0),
        "cable_span": factors.get("cable_span_factor", 2.0)
    }

    factor = factor_map.get(measurement_type, 1.0)
    return old_value * factor


# ============================================================================
# CLI TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("MEASUREMENTS LOADER - V7 INTEGRATION TEST")
    print("=" * 80)

    ml = MeasurementsLoader()

    print("\n[SPATIAL MEASUREMENTS]")
    print(f"Total footprint: {ml.get_spatial('global.total_footprint_sqft.value'):,} sq ft")
    print(f"Atrium diameter: {ml.get_spatial('atrium.diameter_feet.value')} feet (range: {ml.get_spatial('atrium.diameter_feet.range_min')}-{ml.get_spatial('atrium.diameter_feet.range_max')})")
    print(f"Mast height: {ml.get_spatial('tensile_roof.mast_height_feet.value')} feet (range: {ml.get_spatial('tensile_roof.mast_height_feet.range_min')}-{ml.get_spatial('tensile_roof.mast_height_feet.range_max')})")
    print(f"Food court pit: {ml.get_spatial('food_court.pit_depth_feet.value')} feet")
    print(f"Cable count: {ml.get_spatial('tensile_roof.cable_count.value')}")

    print("\n[ZONE DIMENSIONS]")
    fc = ml.get_zone("Z4_FOOD_COURT")
    print(f"Z4 Food Court: {fc.get('name')}")
    print(f"  - Elevation: {fc.get('elevation_feet')} feet")
    print(f"  - Diameter: {fc.get('diameter_feet', {}).get('value')} feet")
    print(f"  - Photo count: {fc.get('photo_count')}")

    print("\n[FEATURE WITH CONTEXT]")
    fountain = ml.get_feature_with_context("fountain")
    print(f"Fountain tiers: {fountain.get('tier_count', {}).get('value')}")
    print(f"  - Confidence: {fountain.get('tier_count', {}).get('confidence')}")
    print(f"  - Photos: {fountain.get('photo_refs', [])[:2]}")

    print("\n[SCALE FACTORS]")
    factors = ml.get_voxel_scale_factors()
    print(f"Atrium correction: {factors['atrium_diameter_factor']}x")
    print(f"Mast correction: {factors['mast_height_factor']}x")

    print("\n[ARCHITECTURAL CONTEXT]")
    context = ml.get_architectural_context()
    print(f"Architect: {context.get('architect')}")
    print(f"Design intent: {context.get('design_intent')}")

    print("\n[VALIDATION]")
    validation = ml.validate_measurements()
    print(f"Status: {validation['status']}")
    print(f"Errors: {len(validation['errors'])}")
    print(f"Warnings: {len(validation['warnings'])}")
    print(f"Low confidence zones: {len(validation['low_confidence_zones'])}")
    print(f"Total zones loaded: {validation['total_zones']}")

    print("\n" + "=" * 80)
    print("LOADER TEST COMPLETE")
    print("=" * 80)
