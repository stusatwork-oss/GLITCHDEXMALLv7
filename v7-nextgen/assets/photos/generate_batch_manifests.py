#!/usr/bin/env python3
"""
BATCH CLASSIFICATION GENERATOR
Creates image batches for rapid Claude classification

Strategy:
- Scan all 224 images in eastland-archive
- Exclude 40 already classified in Batches 1 & 2
- Create Batches 4-11 with ~20-25 images each
- Generate batch manifests for Claude vision processing
"""

import os
import json
from pathlib import Path

# Paths
ARCHIVE_PATH = Path("eastland-archive")
BATCH_1_PATH = Path("BATCH_1_CLASSIFICATION_MANIFEST.json")
BATCH_2_PATH = Path("BATCH_2_CLASSIFICATION_MANIFEST.json")

# Load existing classifications
with open(BATCH_1_PATH) as f:
    batch1 = json.load(f)
with open(BATCH_2_PATH) as f:
    batch2 = json.load(f)

# Get already classified filenames
classified = set()
for item in batch1["classifications"]:
    classified.add(item["filename"])
for item in batch2["classifications"]:
    classified.add(item["filename"])

print(f"Already classified: {len(classified)} images")

# Get all images in archive
all_images = sorted([f.name for f in ARCHIVE_PATH.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
print(f"Total archive images: {len(all_images)}")

# Get unclassified
unclassified = [img for img in all_images if img not in classified]
print(f"Remaining to classify: {len(unclassified)}")

# Create batches of 25 images each
BATCH_SIZE = 25
batches = []
for i in range(0, len(unclassified), BATCH_SIZE):
    batch = unclassified[i:i+BATCH_SIZE]
    batches.append(batch)

print(f"\nCreating {len(batches)} batches:")
for i, batch in enumerate(batches, 4):  # Start at batch 4
    print(f"  Batch {i}: {len(batch)} images")

# Generate batch manifests
for batch_num, batch_images in enumerate(batches, 4):
    manifest = {
        "batch_number": batch_num,
        "batch_date": "2025-11-22",
        "processed_by": "AI Classification - RAPID MODE",
        "total_items": len(batch_images),
        "classifications": [],
        "status": "PENDING_CLASSIFICATION"
    }
    
    # Add placeholder entries for each image
    for filename in batch_images:
        entry = {
            "filename": filename,
            "source_path": f"v6-nextgen/assets/photos/eastland-archive/{filename}",
            "layer_1_zone": "PENDING",
            "layer_2_semantic": [],
            "layer_3_narrative": [],
            "anomalies": None,
            "confidence": 0,
            "status": "pending"
        }
        manifest["classifications"].append(entry)
    
    # Write manifest
    output_path = Path(f"BATCH_{batch_num}_CLASSIFICATION_MANIFEST.json")
    with open(output_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✓ Created {output_path}")

print(f"\n✅ Generated {len(batches)} batch manifests")
print(f"Next: Process batches 4-{3+len(batches)} with Claude vision")
