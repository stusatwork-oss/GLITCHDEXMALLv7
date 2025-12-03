#!/usr/bin/env python3
"""
MASK TO VOXEL CONVERTER
Converts 2D sprite masks to 3D voxel structures.

Philosophy: Asset pipeline is data + tiny tools, not complex engines.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# Add src to path for loading palette
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from collapsed_json_engine import load_palette, hex_to_rgb


# Color legend for mask parsing
COLOR_LEGEND = {
    '.': None,  # Transparent
    'B': 'MALL_BLUE_LIGHT',
    'b': 'MALL_BLUE',
    'Y': 'FOODCOURT_YELLOW',
    'L': 'CEILING_TILE_LIGHT',
    'P': 'MILO_OPTICS_HOTPINK',
    'R': 'ALERT_RED',
    'S': 'METAL_DARK',
}


def parse_mask_file(mask_path: str) -> List[str]:
    """
    Parse mask file, removing comments and blank lines.
    Returns list of mask rows.
    """
    with open(mask_path) as f:
        lines = f.readlines()

    mask_rows = []
    for line in lines:
        # Skip comments and empty lines
        line = line.split('#')[0].strip()
        if line and not line.startswith('#'):
            mask_rows.append(line)

    return mask_rows


def brightness_to_height(char: str, max_height: int = 8) -> int:
    """
    Convert character to voxel height based on brightness.
    Darker = shorter, Brighter = taller
    """
    # Brightness scale (darkest to brightest)
    brightness_scale = {
        '.': 0,  # Transparent / no height
        'S': 1,  # Shadow/dark
        'b': 3,  # Dark blue
        'B': 4,  # Light blue
        'Y': 5,  # Yellow
        'L': 6,  # Light/lid
        'P': 7,  # Pink (bright)
        'R': 8,  # Red (brightest/tallest)
    }

    return brightness_scale.get(char, 0)


def mask_to_voxel_grid(mask_rows: List[str], extrude_depth: int = 4, heightmap_mode: bool = False, max_height: int = 8) -> Dict:
    """
    Convert 2D mask to 3D voxel grid.

    Args:
        mask_rows: List of mask row strings
        extrude_depth: How many voxels deep to extrude (Z-axis)
        heightmap_mode: If True, use brightness to determine height (Y-axis)
        max_height: Maximum voxel height in heightmap mode

    Returns:
        Dict with voxel positions and colors
    """
    height = len(mask_rows)
    width = len(mask_rows[0]) if mask_rows else 0

    voxels = []

    if heightmap_mode:
        # Height-from-brightness mode
        for row_idx, row in enumerate(mask_rows):
            for x, char in enumerate(row):
                if char in COLOR_LEGEND and COLOR_LEGEND[char] is not None:
                    color = COLOR_LEGEND[char]
                    voxel_height = brightness_to_height(char, max_height)

                    # Build column from ground up to height
                    for y in range(voxel_height):
                        for z in range(extrude_depth):
                            voxel = {
                                'position': [x, y, z],
                                'color': color
                            }
                            voxels.append(voxel)

        final_size = [width, max_height, extrude_depth]

    else:
        # Standard extrusion mode (original behavior)
        for y, row in enumerate(mask_rows):
            for x, char in enumerate(row):
                if char in COLOR_LEGEND and COLOR_LEGEND[char] is not None:
                    color = COLOR_LEGEND[char]

                    # Extrude into Z-axis (create depth)
                    for z in range(extrude_depth):
                        voxel = {
                            'position': [x, height - y - 1, z],  # Flip Y for bottom-up
                            'color': color
                        }
                        voxels.append(voxel)

        final_size = [width, height, extrude_depth]

    return {
        'size': final_size,
        'voxels': voxels,
        'total_voxels': len(voxels),
        'mode': 'heightmap' if heightmap_mode else 'extrusion'
    }


def voxel_grid_to_layers(voxel_grid: Dict) -> List[Dict]:
    """
    Convert flat voxel grid to layer-based format for rendering.
    Groups voxels by Y coordinate into horizontal slices.
    """
    width, height, depth = voxel_grid['size']
    voxels_by_layer = {}

    # Group voxels by Y coordinate
    for voxel in voxel_grid['voxels']:
        x, y, z = voxel['position']
        if y not in voxels_by_layer:
            voxels_by_layer[y] = []
        voxels_by_layer[y].append(voxel)

    # Convert to layer format
    layers = []
    for y in sorted(voxels_by_layer.keys()):
        layer_voxels = voxels_by_layer[y]

        # Find dominant color for this layer (most common)
        color_counts = {}
        for v in layer_voxels:
            color = v['color']
            color_counts[color] = color_counts.get(color, 0) + 1

        dominant_color = max(color_counts, key=color_counts.get)

        layer = {
            'y': y,
            'voxel_count': len(layer_voxels),
            'dominant_color': dominant_color,
            'voxels': layer_voxels
        }
        layers.append(layer)

    return layers


def export_voxel_json(voxel_grid: Dict, object_id: str, output_path: str):
    """
    Export voxel grid as collapsed JSON object spec.
    """
    layers = voxel_grid_to_layers(voxel_grid)

    spec = {
        'voxel_object_id': object_id,
        'size': voxel_grid['size'],
        'palette': 'COMICBOOK_MALL_V1',
        'generated_from': 'mask_to_voxel.py',
        'total_voxels': voxel_grid['total_voxels'],
        'layers': layers
    }

    with open(output_path, 'w') as f:
        json.dump(spec, f, indent=2)

    print(f"✅ Exported voxel JSON: {output_path}")
    print(f"   Size: {spec['size']}")
    print(f"   Voxels: {spec['total_voxels']}")
    print(f"   Layers: {len(layers)}")


def export_png_sprite(mask_rows: List[str], output_path: str):
    """
    Export mask as PNG sprite using actual palette colors.
    Requires PIL/Pillow.
    """
    try:
        from PIL import Image
    except ImportError:
        print("⚠️  PIL/Pillow not installed - cannot export PNG")
        print("   Install with: pip install Pillow")
        return

    # Load palette colors
    palette = load_palette()

    height = len(mask_rows)
    width = len(mask_rows[0]) if mask_rows else 0

    # Create RGBA image
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pixels = img.load()

    for y, row in enumerate(mask_rows):
        for x, char in enumerate(row):
            if char in COLOR_LEGEND and COLOR_LEGEND[char] is not None:
                palette_name = COLOR_LEGEND[char]
                hex_color = palette.get(palette_name)

                if hex_color:
                    rgb = hex_to_rgb(hex_color)
                    pixels[x, y] = (*rgb, 255)  # Add alpha channel

    # Save PNG
    img.save(output_path)
    print(f"✅ Exported PNG sprite: {output_path}")
    print(f"   Size: {width}x{height}")


def main():
    """
    Main converter entry point.
    """
    print("=" * 60)
    print("  MASK TO VOXEL CONVERTER")
    print("=" * 60)
    print()

    if len(sys.argv) < 2:
        print("Usage: python mask_to_voxel.py <mask_file> [options]")
        print()
        print("Options:")
        print("  --png <output.png>     Export PNG sprite")
        print("  --voxel <output.json>  Export voxel JSON")
        print("  --depth <n>            Extrusion depth (default: 4)")
        print("  --heightmap            Use brightness-to-height mode")
        print("  --max-height <n>       Max voxel height in heightmap mode (default: 8)")
        print()
        print("Modes:")
        print("  Extrusion (default):   Each pixel becomes a Z-extruded column")
        print("  Heightmap (--heightmap): Brightness determines Y-height")
        print()
        print("Examples:")
        print("  python mask_to_voxel.py slurpee.txt --voxel out.json --png out.png")
        print("  python mask_to_voxel.py terrain.txt --heightmap --max-height 16 --voxel terrain.json")
        return

    mask_file = sys.argv[1]
    extrude_depth = 4
    heightmap_mode = False
    max_height = 8

    # Parse options
    png_output = None
    voxel_output = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--png' and i + 1 < len(sys.argv):
            png_output = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--voxel' and i + 1 < len(sys.argv):
            voxel_output = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--depth' and i + 1 < len(sys.argv):
            extrude_depth = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--heightmap':
            heightmap_mode = True
            i += 1
        elif sys.argv[i] == '--max-height' and i + 1 < len(sys.argv):
            max_height = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    # Parse mask file
    print(f"📄 Reading mask: {mask_file}")
    mask_rows = parse_mask_file(mask_file)
    print(f"   Dimensions: {len(mask_rows[0])}x{len(mask_rows)}")
    print()

    # Convert to voxel grid
    mode_str = "heightmap" if heightmap_mode else "extrusion"
    print(f"🔨 Converting to voxel grid (mode={mode_str}, depth={extrude_depth})...")
    voxel_grid = mask_to_voxel_grid(mask_rows, extrude_depth, heightmap_mode, max_height)
    print(f"   Generated {voxel_grid['total_voxels']} voxels ({voxel_grid['mode']} mode)")
    print()

    # Export outputs
    if voxel_output:
        object_id = Path(voxel_output).stem.upper()
        export_voxel_json(voxel_grid, object_id, voxel_output)
        print()

    if png_output:
        export_png_sprite(mask_rows, png_output)
        print()

    if not png_output and not voxel_output:
        print("⚠️  No output format specified")
        print("   Use --png or --voxel to export")

    print("=" * 60)
    print("  ✅ Conversion complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
