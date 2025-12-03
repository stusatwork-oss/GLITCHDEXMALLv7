"""Case-insensitive voxel object registry wired to PNG heightmap conversion."""

import json
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from voxel_asset_seed import ensure_voxel_source_images


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def normalize_key(value: Any) -> str:
    """Normalize keys/identifiers for case-insensitive lookups."""
    return str(value).strip().upper()


def load_palette_json(palette_path: Path) -> Dict[str, str]:
    """Load a palette JSON mapping #RRGGBB keys to material identifiers."""
    data = json.loads(Path(palette_path).read_text())
    return {str(k).strip(): str(v) for k, v in data.items()}


# ---------------------------------------------------------------------------
# Simple PNG decoder (no Pillow dependency)
# ---------------------------------------------------------------------------


def _decode_png_rgba(image_path: Path) -> Tuple[int, int, List[List[Tuple[int, int, int, int]]]]:
    """Decode an RGBA PNG (8-bit) into a 2D array of tuples."""

    raw = image_path.read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a PNG file")

    idx = 8
    width = height = None
    idat_chunks: List[bytes] = []

    while idx < len(raw):
        length = int.from_bytes(raw[idx : idx + 4], "big")
        chunk_type = raw[idx + 4 : idx + 8]
        data = raw[idx + 8 : idx + 8 + length]
        idx += 12 + length

        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, *_ = struct.unpack(
                ">IIBBBBB", data
            )
            if bit_depth != 8 or color_type != 6:
                raise ValueError("Only 8-bit RGBA PNGs are supported")
        elif chunk_type == b"IDAT":
            idat_chunks.append(data)
        elif chunk_type == b"IEND":
            break

    if width is None or height is None:
        raise ValueError("PNG missing IHDR")

    decompressed = zlib.decompress(b"".join(idat_chunks))
    stride = width * 4
    rows: List[List[Tuple[int, int, int, int]]] = []

    offset = 0
    for _ in range(height):
        filter_type = decompressed[offset]
        offset += 1
        if filter_type != 0:
            raise ValueError("Only filter type 0 is supported in this loader")

        row_bytes = decompressed[offset : offset + stride]
        offset += stride
        row: List[Tuple[int, int, int, int]] = []
        for i in range(0, len(row_bytes), 4):
            row.append(tuple(row_bytes[i : i + 4]))
        rows.append(row)

    return width, height, rows


# ---------------------------------------------------------------------------
# Mesh builder
# ---------------------------------------------------------------------------


def build_voxels_from_png(
    image_path: str,
    palette: Dict[str, str],
    voxel_size: float = 1.0,
    height: float = 8.0,
    zone_id: str = "VOXEL_OBJECT",
) -> Dict[str, Any]:
    """
    Convert a PNG heightmap into a simple voxel mesh JSON.

    This avoids external dependencies by decoding PNG data directly. Pixels with
    alpha=0 are skipped; all others generate 1x1 columns at the specified height.
    """

    image_path = Path(image_path)
    _, _, pixels = _decode_png_rgba(image_path)
    boxes = []
    palette_used: Dict[str, str] = {}

    for y, row in enumerate(pixels):
        for x, (r, g, b, a) in enumerate(row):
            if a == 0:
                continue
            hex_key = f"#{r:02x}{g:02x}{b:02x}"
            material = palette.get(hex_key, f"color_{r:02x}{g:02x}{b:02x}")
            palette_used[hex_key] = material
            boxes.append(
                {
                    "zone_id": zone_id,
                    "material": material,
                    "bounds": [
                        x * voxel_size,
                        (x + 1) * voxel_size,
                        y * voxel_size,
                        (y + 1) * voxel_size,
                        0,
                        height,
                    ],
                    "dimensions_feet": [voxel_size, voxel_size, height],
                }
            )

    mesh = {
        "version": "voxel-object-loader-1.0",
        "source_image": str(image_path),
        "voxel_size": voxel_size,
        "height_feet": height,
        "zone_default": zone_id,
        "palette": palette_used,
        "boxes": boxes,
    }

    return mesh


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


@dataclass
class VoxelObject:
    obj_id: str
    mesh: Any
    behavior: Dict[str, Any]
    placement: Dict[str, Any]
    source_image: str
    metadata: Dict[str, Any]

    @property
    def id(self) -> str:
        """Alias for obj_id to match common engine expectations."""

        return self.obj_id


class VoxelObjectRegistry:
    def __init__(
        self,
        base_path: str,
        palette: Dict[str, Any],
        png_to_vox_fn: Callable[..., Any],
        root_path: Optional[str] = None,
    ):
        """
        base_path: path to data/voxel_objects
        palette: already-loaded palette dict (#RRGGBB -> material)
        png_to_vox_fn: function(image_path, palette) -> mesh
        root_path: project root for resolving shared asset paths
        """

        self.base_path = Path(base_path)
        resolved = self.base_path.resolve()
        self.root_path = Path(root_path) if root_path else resolved.parent.parent
        self.palette = palette
        self.png_to_vox_fn = png_to_vox_fn
        self.objects: Dict[str, VoxelObject] = {}
        self.registry_metadata: Dict[str, Any] = {}
        asset_dir = self.root_path / "assets" / "voxel_sources"
        self.asset_paths = ensure_voxel_source_images(asset_dir)

    def load_registry(self, registry_file: str = "voxel_objects_registry.json"):
        full_path = self.base_path / registry_file
        data = json.loads(full_path.read_text())

        self.registry_metadata = {k: v for k, v in data.items() if k != "objects"}
        objects = data.get("objects", {})
        for _, info in objects.items():
            obj_file = info["file"]
            self._load_object_file(obj_file)

    def _resolve_asset_path(self, source_path: str) -> Path:
        candidate = Path(source_path)
        if candidate.is_absolute():
            return candidate

        for base in (self.root_path, self.base_path, Path.cwd()):
            potential = base / candidate
            if potential.exists():
                return potential

        return self.root_path / candidate

    def _load_object_file(self, filename: str):
        full_path = self.base_path / filename
        raw = json.loads(full_path.read_text())

        obj_id = normalize_key(raw.get("voxel_object_id", filename))
        source_image_path = self._resolve_asset_path(raw["source_image"])
        mode = normalize_key(raw.get("mode", "HEIGHTMAP_EXTRUDE"))
        voxel_scale = raw.get("voxel_scale", [1, 1, 1])
        zone_id = raw.get("zone_id", "VOXEL_OBJECT")

        if mode == "HEIGHTMAP_EXTRUDE":
            mesh = self.png_to_vox_fn(
                str(source_image_path), self.palette, zone_id=zone_id
            )
        else:
            raise ValueError(f"Unsupported voxel object mode: {mode}")

        placement = raw.get("placement", {"attach": "floor", "offset": [0, 0, 0]})
        behavior = raw.get("behavior", {"type": "STATIC"})

        self.objects[obj_id] = VoxelObject(
            obj_id=obj_id,
            mesh=mesh,
            behavior=behavior,
            placement=placement,
            source_image=str(source_image_path),
            metadata={"mode": mode, "voxel_scale": voxel_scale, "zone_id": zone_id},
        )

    def get(self, obj_id: str) -> VoxelObject:
        key = normalize_key(obj_id)
        if key not in self.objects:
            raise KeyError(f"Voxel object '{obj_id}' not loaded")
        return self.objects[key]

    def __contains__(self, obj_id: str) -> bool:
        return normalize_key(obj_id) in self.objects

    def __len__(self) -> int:
        return len(self.objects)

