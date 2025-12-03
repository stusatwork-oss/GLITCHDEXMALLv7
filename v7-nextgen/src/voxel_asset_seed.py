"""Seed tiny voxel source PNGs from inline base64 to avoid binary assets in git."""

import base64
from pathlib import Path
from typing import Dict


# Base64-encoded 32x32 (or smaller) PNGs for voxel source sprites.
VOXEL_SOURCES_BASE64: Dict[str, str] = {
    "arcade_token.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAYklEQVR4nGNgGAWjYBSMAgJAQEDgP6WYYgegi13ekvMfFyZGP9kOwGcxLodQzQGkWI7siOHhAHIsh+FRB4w6YNQBw6McGBQOINUR2PRT7ABiHEKMfpIdMKDtgVEwCkYBrQEAQpKEUTWB4HAAAAAASUVORK5CYII=",
    "janitor_mop.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAUUlEQVR4nGNgGAWjgAIgICDwHxkPiAP0U2aC8agDRh1AcwfALELGow4YdcDIygWjDhh1wKgDRh2AbCkxmKYOmH1+Nl486gCaO2BA08AooDYAADhEIYG4CYOSAAAAAElFTkSuQmCC",
    "pizza_slice.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAoElEQVR4nO3WwQmAMAwF0I7QDdzDWZxAcE4HcA7PHis9BMKntWKT1EM+BItQ8owVDMHjaSTGmHqrG7Cv8+cSAfgEhk+A1texpKdq7e8GcMQ5ba8Q4oCc3JyqhRAH8OaI4Gs1ACJ4c7ynBiBEvmJzRKgBeGoTMAHgJPBAqgL4UxPCDFB67yWE6QQoQ84AxvQrqGU4QGK/A/4BGPpH5PFo5wZ4fdMtXr+KhgAAAABJRU5ErkJggg==",
    "slurpee_front.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAUElEQVR4nGNgGAWjgEwgICDwHx3T3QFv5XPheGQ6YECjYEAANl/jwsPbAVkX/+PEow4YdcCoA4Z/ORAXF0cQjzpg1AHD2wEDmg1HwSgYlgAA4SeSDfTHmzoAAAAASUVORK5CYII=",
    "trash_can.png": "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAASElEQVR4nO3WwQkAMAgEQUuwQju92pIWNEQE2YX7D+YTMyJK5O7ndd8AksrbBRh/guoVAAAAAABACyAi0gOwEzD+HxgDEHV2AUPaxzHdbXL1AAAAAElFTkSuQmCC",
}


def ensure_voxel_source_images(base_dir: Path) -> Dict[str, Path]:
    """Ensure voxel source PNGs exist on disk, writing from base64 if missing.

    Returns a mapping of filename -> absolute path for convenience.
    """

    base_dir.mkdir(parents=True, exist_ok=True)
    written: Dict[str, Path] = {}

    for filename, b64_data in VOXEL_SOURCES_BASE64.items():
        target = base_dir / filename
        decoded = base64.b64decode(b64_data)
        if not target.exists() or target.read_bytes() != decoded:
            target.write_bytes(decoded)
        written[filename] = target

    return written
