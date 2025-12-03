#!/usr/bin/env python3
"""
STANDARD ASSET SEEDER
Writes user-provided Voxel JSONs to the filesystem for the VoxelObjectLoader.
"""

import json
from pathlib import Path
import sys

def seed_standard_assets(repo_root: Path):
    """Writes the standard interactive objects to assets/voxel_sources/standard/"""
    output_dir = repo_root / "assets" / "voxel_sources" / "standard"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. TRASH CAN (Cover / Obstacle)
    _write_asset(output_dir, "TRASH_CAN.json", {
        "voxel_object_id": "TRASH_CAN",
        "source_image": "assets/voxel_sources/trash_can.png",
        "mode": "HEIGHTMAP_EXTRUDE",
        "palette": "COMICBOOK_MALL_V1",
        "voxel_scale": [1, 1, 1],
        "placement": {"attach": "floor", "offset": [0, 0, 0]},
        "behavior": {
            "type": "STATIC",
            "tags": ["FOODCOURT", "SERVICE", "COVER"], # Added COVER tag
            "on_use": ["subtitle: 'Tactical concealment unit.'"]
        }
    })

    # 2. SLURPEE CUP (Mess Lure)
    _write_asset(output_dir, "SLURPEE_CUP.json", {
        "voxel_object_id": "SLURPEE_CUP",
        "source_image": "assets/voxel_sources/slurpee_front.png",
        "mode": "HEIGHTMAP_EXTRUDE",
        "palette": "COMICBOOK_MALL_V1",
        "voxel_scale": [1, 1, 1],
        "placement": {"attach": "floor", "offset": [0, 0, 0]},
        "behavior": {
            "type": "PICKUP",
            "tags": ["FOODCOURT", "DRINK", "MESS"], # Added MESS tag
            "on_pickup": ["cloud_pressure+5", "subtitle: 'Brain freeze.'"]
        }
    })

    # 3. PIZZA SLICE (Mess Lure)
    _write_asset(output_dir, "PIZZA_SLICE.json", {
        "voxel_object_id": "PIZZA_SLICE",
        "source_image": "assets/voxel_sources/pizza_slice.png",
        "mode": "HEIGHTMAP_EXTRUDE",
        "palette": "COMICBOOK_MALL_V1",
        "voxel_scale": [1, 1, 1],
        "placement": {"attach": "table", "offset": [0, 0, 0]},
        "behavior": {
            "type": "PICKUP",
            "tags": ["FOODCOURT", "FOOD", "MESS"],
            "on_pickup": ["cloud_pressure-3", "subtitle: 'Grease trap.'"]
        }
    })

    # 4. ARCADE TOKEN (Distraction)
    _write_asset(output_dir, "ARCADE_TOKEN.json", {
        "voxel_object_id": "ARCADE_TOKEN",
        "source_image": "assets/voxel_sources/arcade_token.png",
        "mode": "HEIGHTMAP_EXTRUDE",
        "palette": "COMICBOOK_MALL_V1",
        "voxel_scale": [1, 1, 1],
        "placement": {"attach": "floor", "offset": [0, 0, 0]},
        "behavior": {
            "type": "PICKUP",
            "tags": ["ARCADE", "CURRENCY", "NOISE"],
            "on_pickup": ["cloud_pressure+1", "flag:FOUND_TOKEN=true"]
        }
    })

    # 5. JANITOR MOP (NPC Tool)
    _write_asset(output_dir, "JANITOR_MOP.json", {
        "voxel_object_id": "JANITOR_MOP",
        "source_image": "assets/voxel_sources/janitor_mop.png",
        "mode": "HEIGHTMAP_EXTRUDE",
        "palette": "COMICBOOK_MALL_V1",
        "voxel_scale": [1, 1, 1],
        "placement": {"attach": "floor", "offset": [0, 0, 0]},
        "behavior": {
            "type": "NPC_PROP",
            "tags": ["SERVICE_HALL", "UNIT7"],
            "on_pickup": ["subtitle: 'The Janitor needs this.'", "cloud_pressure+2"]
        }
    })
    
    print(f"[ASSETS] Seeded 5 Standard Voxel Objects in {output_dir}")

def _write_asset(directory, filename, data):
    with open(directory / filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    seed_standard_assets(Path("."))