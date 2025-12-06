import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image


def load_palette(palette_path: Path) -> Dict[Tuple[int, int, int], str]:
    if not palette_path:
        return {}
    data = json.loads(palette_path.read_text())
    result = {}
    for hex_color, material in data.items():
        hex_str = hex_color.lstrip("#")
        if len(hex_str) != 6:
            raise ValueError(f"Invalid color key '{hex_color}' (expected #RRGGBB)")
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        result[(r, g, b)] = material
    return result


def find_runs(row: List[int]) -> List[Tuple[int, int, int]]:
    runs = []
    current = None
    for x, val in enumerate(row):
        if val:
            if current is None:
                current = [x, x]
            else:
                current[1] = x
        else:
            if current is not None:
                runs.append((current[0], current[1], val))
                current = None
    if current is not None:
        runs.append((current[0], current[1], val))
    return runs


def merge_runs_into_boxes(rows: List[List[int]], height: float, voxel_size: float, zone_id: str, material: str):
    boxes = []
    active = {}
    for y, row in enumerate(rows):
        runs = []
        in_run = False
        start = 0
        for x, val in enumerate(row):
            if val and not in_run:
                start = x
                in_run = True
            if in_run and (x == len(row) - 1 or not val):
                end = x if val else x - 1
                runs.append((start, end))
                in_run = False
        next_active = {}
        for run in runs:
            key = (run[0], run[1])
            if key in active:
                x0, x1, y0, y1 = active[key]
                next_active[key] = (x0, x1, y0, y + 1)
            else:
                next_active[key] = (run[0], run[1], y, y + 1)
        for key, box in active.items():
            if key not in next_active:
                x0, x1, y0, y1 = box
                boxes.append(
                    {
                        "zone_id": zone_id,
                        "material": material,
                        "bounds": [
                            x0 * voxel_size,
                            (x1 + 1) * voxel_size,
                            y0 * voxel_size,
                            y1 * voxel_size,
                            0,
                            height,
                        ],
                        "dimensions_feet": [
                            (x1 - x0 + 1) * voxel_size,
                            (y1 - y0) * voxel_size,
                            height,
                        ],
                    }
                )
        active = next_active
    for _, box in active.items():
        x0, x1, y0, y1 = box
        boxes.append(
            {
                "zone_id": zone_id,
                "material": material,
                "bounds": [
                    x0 * voxel_size,
                    (x1 + 1) * voxel_size,
                    y0 * voxel_size,
                    y1 * voxel_size,
                    0,
                    height,
                ],
                "dimensions_feet": [
                    (x1 - x0 + 1) * voxel_size,
                    (y1 - y0) * voxel_size,
                    height,
                ],
            }
        )
    return boxes


def convert_png(
    input_path: Path,
    output_path: Path,
    palette_path: Path,
    voxel_size: float,
    height: float,
    zone_id: str,
    ignore_alpha: bool,
):
    palette = load_palette(palette_path) if palette_path else {}
    img = Image.open(input_path).convert("RGBA")
    width, height_px = img.size
    pixels = img.load()

    material_grids: Dict[str, List[List[int]]] = defaultdict(lambda: [[0] * width for _ in range(height_px)])
    palette_used: Dict[str, str] = {}

    for y in range(height_px):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if ignore_alpha and a == 0:
                continue
            key = (r, g, b)
            if key in palette:
                material = palette[key]
            else:
                material = f"color_{r:02x}{g:02x}{b:02x}"
            material_grids[material][y][x] = 1
            palette_used[f"#{r:02x}{g:02x}{b:02x}"] = material

    boxes = []
    for material, rows in material_grids.items():
        boxes.extend(merge_runs_into_boxes(rows, height, voxel_size, zone_id, material))

    result = {
        "version": "png-converted-1.0",
        "voxel_size": voxel_size,
        "source_image": str(input_path),
        "height_feet": height,
        "zone_default": zone_id,
        "palette": palette_used,
        "boxes": boxes,
    }

    output_path.write_text(json.dumps(result, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description="Convert a top-down PNG into voxel box JSON.")
    parser.add_argument("input", type=Path, help="Input PNG file (top-down)")
    parser.add_argument("--output", type=Path, required=True, help="Output JSON path")
    parser.add_argument("--palette", type=Path, help="Optional palette JSON mapping #RRGGBB -> material name")
    parser.add_argument("--voxel-size", type=float, default=1.0, help="Size of one pixel in feet (default: 1)")
    parser.add_argument("--height", type=float, default=8.0, help="Extrusion height in feet (default: 8)")
    parser.add_argument("--zone-id", type=str, default="PNG_LAYER", help="Zone id to tag boxes with")
    parser.add_argument("--keep-alpha", action="store_true", help="Keep fully transparent pixels instead of skipping")
    args = parser.parse_args()

    convert_png(
        input_path=args.input,
        output_path=args.output,
        palette_path=args.palette,
        voxel_size=args.voxel_size,
        height=args.height,
        zone_id=args.zone_id,
        ignore_alpha=not args.keep_alpha,
    )


if __name__ == "__main__":
    main()
