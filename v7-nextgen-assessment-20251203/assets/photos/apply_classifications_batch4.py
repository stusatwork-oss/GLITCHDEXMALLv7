#!/usr/bin/env python3
"""
RAPID BATCH CLASSIFIER
Updates batch manifests with classifications
"""

import json
from pathlib import Path

# BATCH 4 CLASSIFICATIONS (Images 1-20 complete, writing now)
classifications_batch4 = {
    "453124482_ee1c413ccd_c.jpg": {
        "layer_1_zone": "atrium",
        "layer_2_semantic": ["storefronts_closed", "signage_and_wayfinding"],
        "layer_3_narrative": ["mood_mid_cloud", "liminal"],
        "anomalies": None,
        "confidence": 90
    },
    "453124482_ee1c413ccd_z.jpg": {
        "layer_1_zone": "atrium",
        "layer_2_semantic": ["storefronts_closed", "signage_and_wayfinding"],
        "layer_3_narrative": ["mood_mid_cloud", "liminal"],
        "anomalies": None,
        "confidence": 90
    },
    "453124606_d301b8ee8e_c.jpg": {
        "layer_1_zone": "atrium",
        "layer_2_semantic": ["architectural_features", "lighting_conditions"],
        "layer_3_narrative": ["mood_mid_cloud", "human_scale"],
        "anomalies": "TENSILE ROOF MASTS - CRITICAL STRUCTURAL REFERENCE, escalators visible, food court area",
        "confidence": 95
    },
    "453124750_117d0e4e30_c.jpg": {
        "layer_1_zone": "atrium",
        "layer_2_semantic": ["architectural_features", "material_patterns"],
        "layer_3_narrative": ["mood_mid_cloud", "pov_shots"],
        "anomalies": "Tensile sail fabric detail - KEY STRUCTURAL ELEMENT",
        "confidence": 92
    },
    "453124908_b8d32d4e02_c.jpg": {
        "layer_1_zone": "escalators",
        "layer_2_semantic": ["architectural_features", "lighting_conditions"],
        "layer_3_narrative": ["mood_mid_cloud", "human_scale"],
        "anomalies": "Escalator with tensile masts - SCALE REFERENCE",
        "confidence": 93
    },
    "453125154_142982f725_c.jpg": {
        "layer_1_zone": "food_court",
        "layer_2_semantic": ["architectural_features", "signage_and_wayfinding"],
        "layer_3_narrative": ["mood_mid_cloud"],
        "anomalies": "Decorative clock with tensile mast",
        "confidence": 88
    },
    "453125336_f130f92fe9_c.jpg": {
        "layer_1_zone": "escalators",
        "layer_2_semantic": ["architectural_features", "flooring_patterns"],
        "layer_3_narrative": ["mood_mid_cloud", "human_scale", "pov_shots"],
        "anomalies": "SUNKEN FOOD COURT ESCALATORS - CRITICAL SCALE + SPATIAL REFERENCE",
        "confidence": 96
    },
    "453125654_cd86d63917_c.jpg": {
        "layer_1_zone": "atrium",
        "layer_2_semantic": ["architectural_features", "material_patterns"],
        "layer_3_narrative": ["mood_mid_cloud", "pov_shots"],
        "anomalies": "Tensile fabric geometric pattern - STRUCTURAL DETAIL",
        "confidence": 94
    },
    "453126172_86b3ffe5c3_c.jpg": {
        "layer_1_zone": "atrium",
        "layer_2_semantic": ["architectural_features", "lighting_conditions"],
        "layer_3_narrative": ["mood_mid_cloud", "human_scale"],
        "anomalies": "Multi-level atrium - CIVIC SCALE INDICATOR, escalators, tensile roof",
        "confidence": 95
    },
    "453126354_70152a25b9_c.jpg": {
        "layer_1_zone": "food_court",
        "layer_2_semantic": ["abandoned_elements", "flooring_patterns", "material_patterns"],
        "layer_3_narrative": ["mood_high_cloud", "liminal"],
        "anomalies": "Dead plants, circular seating - abandonment aesthetic",
        "confidence": 91
    },
    "453126662_38466f6375_c.jpg": {
        "layer_1_zone": "food_court",
        "layer_2_semantic": ["architectural_features", "lighting_conditions"],
        "layer_3_narrative": ["mood_mid_cloud", "human_scale"],
        "anomalies": "Multi-level food court, escalators visible",
        "confidence": 89
    },
    "453126662_38466f6375_z.jpg": {
        "layer_1_zone": "food_court",
        "layer_2_semantic": ["architectural_features", "lighting_conditions"],
        "layer_3_narrative": ["mood_mid_cloud", "human_scale"],
        "anomalies": "Multi-level food court, escalators visible",
        "confidence": 89
    },
    "453126954_b9a18142ef_c.jpg": {
        "layer_1_zone": "food_court",
        "layer_2_semantic": ["abandoned_elements", "material_patterns", "flooring_patterns"],
        "layer_3_narrative": ["mood_high_cloud", "liminal"],
        "anomalies": "Drained circular fountain, stepped seating - HIGH LIMINAL VALUE",
        "confidence": 94
    },
    "453127262_63fd3f4f84_c.jpg": {
        "layer_1_zone": "atrium",
        "layer_2_semantic": ["architectural_features", "material_patterns"],
        "layer_3_narrative": ["mood_mid_cloud", "pov_shots"],
        "anomalies": "TENSILE MAST INTERNAL STRUCTURE - CRITICAL ENGINEERING REFERENCE",
        "confidence": 97
    },
    "453127434_b045c11f8d_c.jpg": {
        "layer_1_zone": "food_court",
        "layer_2_semantic": ["material_patterns", "architectural_features"],
        "layer_3_narrative": ["mood_mid_cloud"],
        "anomalies": "Glass block base, terracotta steps - MATERIAL DETAIL",
        "confidence": 90
    }
}

# Load batch 4
with open('BATCH_4_CLASSIFICATION_MANIFEST.json') as f:
    batch4 = json.load(f)

# Update classifications
for entry in batch4["classifications"]:
    filename = entry["filename"]
    if filename in classifications_batch4:
        entry.update(classifications_batch4[filename])
        entry["status"] = "classified"

# Write back
with open('BATCH_4_CLASSIFICATION_MANIFEST.json', 'w') as f:
    json.dump(batch4, f, indent=2)

print(f"✓ Updated {len(classifications_batch4)} classifications in Batch 4")
print(f"Progress: {len(classifications_batch4)}/25 images classified")
