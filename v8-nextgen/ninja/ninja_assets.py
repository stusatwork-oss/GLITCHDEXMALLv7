#!/usr/bin/env python3
"""
NINJA ASSET FACTORY v2.0
Generates voxel assets compatible with V6 VoxelObjectLoader.
"""

import json
from pathlib import Path
from typing import Dict, Any

try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None

# --- ASSET GENERATORS ---
def generate_trap_sprites(output_dir: Path):
    """Generates 32x32 PNG sprites for the constructs."""
    if not Image:
        print("[ASSETS] PIL not found. Skipping sprite generation.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    assets = {
        "ninja_smoke.png": _draw_smoke,
        "ninja_noise.png": _draw_noise_charm,
        "ninja_decoy.png": _draw_decoy,
        "ninja_jammer.png": _draw_door_jam,
        "ninja_tripwire.png": _draw_tripwire
    }

    for filename, draw_fn in assets.items():
        # 32x32 standard voxel texture size
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw_fn(ImageDraw.Draw(img))
        img.save(output_dir / filename)
        print(f"[ASSETS] Generated {filename}")

def _draw_smoke(d):
    d.ellipse([(4, 4), (28, 28)], fill=(100, 100, 100, 200))
    d.ellipse([(8, 8), (20, 20)], fill=(150, 150, 150, 255))

def _draw_noise_charm(d):
    d.rectangle([(12, 4), (20, 28)], fill=(255, 215, 0, 255)) # Gold bar
    d.polygon([(4, 16), (12, 16), (16, 4)], fill=(255, 255, 0, 255))

def _draw_decoy(d):
    d.ellipse([(8, 24), (24, 28)], fill=(0, 0, 0, 150))
    d.rectangle([(12, 8), (20, 24)], fill=(50, 50, 50, 255))
    d.ellipse([(12, 4), (20, 12)], fill=(50, 50, 50, 255))

def _draw_door_jam(d):
    d.rectangle([(4, 12), (28, 20)], fill=(255, 50, 50, 255))
    d.rectangle([(12, 4), (20, 28)], fill=(255, 50, 50, 255))

def _draw_tripwire(d):
    d.line([(0, 16), (32, 16)], fill=(255, 0, 0, 180), width=2)
    d.rectangle([(0, 12), (4, 20)], fill=(100, 100, 100, 255))
    d.rectangle([(28, 12), (32, 20)], fill=(100, 100, 100, 255))

# --- VOXEL DEFINITIONS ---
def get_ninja_voxel_definitions() -> Dict[str, Any]:
    """
    Returns V6-compatible VoxelObject definitions.
    Maps PFDL constructs to visual properties.
    """
    return {
        "NINJA_SMOKE": {
            "voxel_object_id": "NINJA_SMOKE",
            "source_image": "ninja_smoke.png",
            "mode": "HEIGHTMAP_EXTRUDE",
            "voxel_scale": [0.5, 0.5, 1.0], 
            "behavior": {"type": "PASSIVE", "effect": "VISIBILITY_BLOCK"},
            "placement": {"attach": "floor"}
        },
        "NINJA_NOISE": {
            "voxel_object_id": "NINJA_NOISE",
            "source_image": "ninja_noise.png",
            "mode": "HEIGHTMAP_EXTRUDE",
            "voxel_scale": [0.25, 0.25, 0.5],
            "placement": {"attach": "wall", "offset": [0, 0, 3]}
        },
        "NINJA_DECOY": {
            "voxel_object_id": "NINJA_DECOY",
            "source_image": "ninja_decoy.png",
            "mode": "HEIGHTMAP_EXTRUDE",
            "voxel_scale": [1.0, 1.0, 1.0],
            "placement": {"attach": "floor"}
        },
        "NINJA_JAMMER": {
            "voxel_object_id": "NINJA_JAMMER",
            "source_image": "ninja_jammer.png",
            "mode": "HEIGHTMAP_EXTRUDE",
            "voxel_scale": [0.5, 0.5, 0.2],
            "placement": {"attach": "floor"}
        },
        "NINJA_TRIPWIRE": {
            "voxel_object_id": "NINJA_TRIPWIRE",
            "source_image": "ninja_tripwire.png",
            "mode": "HEIGHTMAP_EXTRUDE",
            "voxel_scale": [1.0, 0.1, 0.1],
            "placement": {"attach": "floor"}
        }
    }

def seed_ninja_assets(repo_root: Path):
    """Generates assets and definition JSON."""
    assets_dir = repo_root / "assets" / "voxel_sources" / "ninja"
    generate_trap_sprites(assets_dir)
    
    defs = get_ninja_voxel_definitions()
    def_path = assets_dir / "ninja_constructs.json"
    
    # Save individually for loader discovery
    for key, data in defs.items():
        fname = f"{key.lower()}.json"
        with open(assets_dir / fname, 'w') as f:
            json.dump(data, f, indent=2)
            
    print(f"[ASSETS] Seeded Ninja assets in {assets_dir}")