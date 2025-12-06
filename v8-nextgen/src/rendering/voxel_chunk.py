#!/usr/bin/env python3
"""
VoxelChunk - Sparse 32³ Chunk Storage

Based on Biomes' voxeloo/tensors sparse chunk system.
Uses position encoding for memory-efficient sparse voxel storage.

Reference:
  - biomes-game/voxeloo/tensors/sparse.hpp:44-73
  - See: v8-nextgen/reference/biomes/voxel_math/sparse.hpp
"""

from typing import Dict, Optional, Tuple, Iterator
from dataclasses import dataclass
import sys

# Import encoding utilities
from voxel_encoding import (
    CHUNK_SIZE,
    CHUNK_VOLUME,
    encode_tensor_pos,
    decode_tensor_pos,
)


# =============================================================================
# VOXEL CHUNK (Stage 1: Basic Storage)
# =============================================================================

@dataclass
class VoxelChunk:
    """
    32³ sparse voxel chunk with encoded position storage.

    Matches Biomes' SparseChunkBuilder pattern (sparse.hpp:44-73).

    Only stores non-air voxels (air = material_id 0).
    Uses bit-packed position encoding for 66.7% memory savings.

    Attributes:
        position: Chunk coordinates (cx, cy, cz) in world space
        data: Sparse dict {encoded_pos: material_id}
              Only non-zero materials stored

    Example:
        >>> chunk = VoxelChunk(position=(0, 0, 0))
        >>> chunk.set_voxel(15, 15, 15, material_id=1)
        >>> chunk.get_voxel(15, 15, 15)
        1
        >>> chunk.get_voxel(0, 0, 0)  # Air (not stored)
        0
    """

    position: Tuple[int, int, int]  # Chunk coordinates (cx, cy, cz)
    data: Dict[int, int] = None     # {encoded_pos: material_id}

    def __post_init__(self):
        """Initialize sparse storage."""
        if self.data is None:
            self.data = {}

    # =========================================================================
    # CORE VOXEL ACCESS
    # =========================================================================

    def set_voxel(self, x: int, y: int, z: int, material: int) -> None:
        """
        Set voxel material at chunk-local coordinates.

        Args:
            x, y, z: Local coordinates within chunk (0-31)
            material: Material ID (0 = air, removes voxel)

        Example:
            >>> chunk.set_voxel(10, 20, 15, material_id=5)
            >>> chunk.get_voxel(10, 20, 15)
            5
        """
        # Validate coordinates
        assert 0 <= x < CHUNK_SIZE, f"X out of range: {x}"
        assert 0 <= y < CHUNK_SIZE, f"Y out of range: {y}"
        assert 0 <= z < CHUNK_SIZE, f"Z out of range: {z}"

        # Encode position
        encoded = encode_tensor_pos(x, y, z)

        if material == 0:
            # Air - remove from sparse dict
            self.data.pop(encoded, None)
        else:
            # Solid - store in sparse dict
            self.data[encoded] = material

    def get_voxel(self, x: int, y: int, z: int) -> int:
        """
        Get voxel material at chunk-local coordinates.

        Args:
            x, y, z: Local coordinates within chunk (0-31)

        Returns:
            Material ID (0 = air)

        Example:
            >>> chunk.set_voxel(5, 10, 15, material_id=3)
            >>> chunk.get_voxel(5, 10, 15)
            3
            >>> chunk.get_voxel(0, 0, 0)  # Not set = air
            0
        """
        # Validate coordinates
        assert 0 <= x < CHUNK_SIZE, f"X out of range: {x}"
        assert 0 <= y < CHUNK_SIZE, f"Y out of range: {y}"
        assert 0 <= z < CHUNK_SIZE, f"Z out of range: {z}"

        # Encode and lookup (default to air if not found)
        encoded = encode_tensor_pos(x, y, z)
        return self.data.get(encoded, 0)

    # =========================================================================
    # MEMORY & STATS
    # =========================================================================

    def voxel_count(self) -> int:
        """
        Get number of non-air voxels in chunk.

        Returns:
            Count of solid voxels

        Example:
            >>> chunk = VoxelChunk((0, 0, 0))
            >>> chunk.set_voxel(0, 0, 0, 1)
            >>> chunk.set_voxel(1, 1, 1, 2)
            >>> chunk.voxel_count()
            2
        """
        return len(self.data)

    def is_empty(self) -> bool:
        """
        Check if chunk is completely empty (all air).

        Returns:
            True if no voxels stored

        Example:
            >>> chunk = VoxelChunk((0, 0, 0))
            >>> chunk.is_empty()
            True
            >>> chunk.set_voxel(5, 5, 5, 1)
            >>> chunk.is_empty()
            False
        """
        return len(self.data) == 0

    def memory_usage(self) -> Dict[str, int]:
        """
        Calculate memory usage of this chunk.

        Returns:
            Dict with memory stats in bytes

        Example:
            >>> chunk = VoxelChunk((0, 0, 0))
            >>> for i in range(100):
            ...     chunk.set_voxel(i % 32, (i // 32) % 32, 0, 1)
            >>> stats = chunk.memory_usage()
            >>> stats['voxel_count']
            100
        """
        # Python dict overhead: ~8 bytes per entry (key+value)
        dict_overhead = len(self.data) * 8

        # Tuple for position (3 ints = 24 bytes)
        position_size = 24

        return {
            'voxel_count': len(self.data),
            'dict_bytes': dict_overhead,
            'position_bytes': position_size,
            'total_bytes': dict_overhead + position_size,
            'bytes_per_voxel': dict_overhead / len(self.data) if self.data else 0
        }

    def density(self) -> float:
        """
        Calculate chunk density (percentage of non-air voxels).

        Returns:
            Density from 0.0 (empty) to 1.0 (full)

        Example:
            >>> chunk = VoxelChunk((0, 0, 0))
            >>> chunk.set_voxel(0, 0, 0, 1)  # 1 of 32,768 voxels
            >>> chunk.density()
            3.0517578125e-05  # ~0.003%
        """
        return len(self.data) / CHUNK_VOLUME

    # =========================================================================
    # ITERATION
    # =========================================================================

    def iter_voxels(self) -> Iterator[Tuple[int, int, int, int]]:
        """
        Iterate over all non-air voxels in chunk.

        Yields:
            Tuples of (x, y, z, material_id)

        Example:
            >>> chunk = VoxelChunk((0, 0, 0))
            >>> chunk.set_voxel(5, 10, 15, 1)
            >>> chunk.set_voxel(10, 20, 25, 2)
            >>> list(chunk.iter_voxels())
            [(5, 10, 15, 1), (10, 20, 25, 2)]
        """
        for encoded_pos, material in self.data.items():
            x, y, z = decode_tensor_pos(encoded_pos)
            yield (x, y, z, material)

    def __iter__(self):
        """Support for 'for x, y, z, mat in chunk' syntax."""
        return self.iter_voxels()

    # =========================================================================
    # STAGE 2: CHUNK OPERATIONS
    # =========================================================================

    def fill_region(
        self,
        x_min: int, x_max: int,
        y_min: int, y_max: int,
        z_min: int, z_max: int,
        material: int
    ) -> int:
        """
        Fill a box region with a material.

        Args:
            x_min, x_max: X range (inclusive)
            y_min, y_max: Y range (inclusive)
            z_min, z_max: Z range (inclusive)
            material: Material ID to fill with

        Returns:
            Number of voxels set

        Example:
            >>> chunk = VoxelChunk((0, 0, 0))
            >>> chunk.fill_region(10, 15, 10, 15, 10, 15, material=1)
            216  # 6x6x6 = 216 voxels
        """
        count = 0
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                for z in range(z_min, z_max + 1):
                    if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE and 0 <= z < CHUNK_SIZE:
                        self.set_voxel(x, y, z, material)
                        count += 1
        return count

    def clear(self) -> None:
        """
        Clear entire chunk (set all to air).

        Example:
            >>> chunk = VoxelChunk((0, 0, 0))
            >>> chunk.fill_region(0, 10, 0, 10, 0, 10, material=1)
            1331
            >>> chunk.clear()
            >>> chunk.is_empty()
            True
        """
        self.data.clear()

    def get_bounds(self) -> Optional[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]:
        """
        Get axis-aligned bounding box of non-air voxels.

        Returns:
            ((x_min, y_min, z_min), (x_max, y_max, z_max)) or None if empty

        Example:
            >>> chunk = VoxelChunk((0, 0, 0))
            >>> chunk.set_voxel(5, 10, 15, 1)
            >>> chunk.set_voxel(20, 25, 30, 2)
            >>> chunk.get_bounds()
            ((5, 10, 15), (20, 25, 30))
        """
        if self.is_empty():
            return None

        x_vals, y_vals, z_vals = [], [], []
        for x, y, z, _ in self.iter_voxels():
            x_vals.append(x)
            y_vals.append(y)
            z_vals.append(z)

        return (
            (min(x_vals), min(y_vals), min(z_vals)),
            (max(x_vals), max(y_vals), max(z_vals))
        )

    def count_material(self, material: int) -> int:
        """
        Count voxels of a specific material.

        Args:
            material: Material ID to count

        Returns:
            Number of voxels with that material

        Example:
            >>> chunk = VoxelChunk((0, 0, 0))
            >>> chunk.set_voxel(0, 0, 0, 1)
            >>> chunk.set_voxel(1, 1, 1, 1)
            >>> chunk.set_voxel(2, 2, 2, 2)
            >>> chunk.count_material(1)
            2
        """
        return sum(1 for mat in self.data.values() if mat == material)

    def clone(self) -> 'VoxelChunk':
        """
        Create a deep copy of this chunk.

        Returns:
            New VoxelChunk with same data

        Example:
            >>> chunk = VoxelChunk((0, 0, 0))
            >>> chunk.set_voxel(5, 5, 5, 1)
            >>> copy = chunk.clone()
            >>> copy.get_voxel(5, 5, 5)
            1
            >>> copy.set_voxel(10, 10, 10, 2)
            >>> chunk.get_voxel(10, 10, 10)  # Original unchanged
            0
        """
        return VoxelChunk(
            position=self.position,
            data=self.data.copy()
        )

    def replace_material(self, old_material: int, new_material: int) -> int:
        """
        Replace all voxels of one material with another.

        Args:
            old_material: Material to replace
            new_material: New material

        Returns:
            Number of voxels replaced

        Example:
            >>> chunk = VoxelChunk((0, 0, 0))
            >>> chunk.fill_region(0, 5, 0, 5, 0, 5, material=1)
            216
            >>> chunk.replace_material(1, 2)
            216
            >>> chunk.count_material(2)
            216
        """
        count = 0
        for encoded_pos, material in list(self.data.items()):
            if material == old_material:
                if new_material == 0:
                    # Replacing with air - remove
                    del self.data[encoded_pos]
                else:
                    self.data[encoded_pos] = new_material
                count += 1
        return count

    # =========================================================================
    # REPR
    # =========================================================================

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"VoxelChunk(pos={self.position}, "
            f"voxels={len(self.data)}, "
            f"density={self.density()*100:.2f}%)"
        )


# =============================================================================
# TESTS
# =============================================================================

def test_basic_chunk():
    """Test basic chunk operations (Stage 1)."""
    print("Testing VoxelChunk (Stage 1: Basic Storage)...")

    # Create chunk
    chunk = VoxelChunk(position=(0, 0, 0))
    assert chunk.is_empty()
    print(f"  ✓ Created empty chunk: {chunk}")

    # Set some voxels
    chunk.set_voxel(0, 0, 0, material=1)
    chunk.set_voxel(15, 15, 15, material=2)
    chunk.set_voxel(31, 31, 31, material=3)
    assert chunk.voxel_count() == 3
    print(f"  ✓ Set 3 voxels: {chunk}")

    # Get voxels
    assert chunk.get_voxel(0, 0, 0) == 1
    assert chunk.get_voxel(15, 15, 15) == 2
    assert chunk.get_voxel(31, 31, 31) == 3
    assert chunk.get_voxel(10, 10, 10) == 0  # Air
    print(f"  ✓ Get voxels working")

    # Remove voxel (set to air)
    chunk.set_voxel(15, 15, 15, material=0)
    assert chunk.voxel_count() == 2
    assert chunk.get_voxel(15, 15, 15) == 0
    print(f"  ✓ Remove voxel (set to air)")

    # Memory usage
    stats = chunk.memory_usage()
    print(f"  ✓ Memory: {stats['total_bytes']} bytes for {stats['voxel_count']} voxels")

    # Iteration
    voxels = list(chunk.iter_voxels())
    assert len(voxels) == 2
    print(f"  ✓ Iteration: {voxels}")

    print(f"  ✓ Stage 1 complete: {chunk}")


def test_chunk_operations():
    """Test chunk operations (Stage 2)."""
    print("\nTesting VoxelChunk (Stage 2: Chunk Operations)...")

    # Fill region
    chunk = VoxelChunk(position=(0, 0, 0))
    count = chunk.fill_region(10, 15, 10, 15, 10, 15, material=1)
    assert count == 216  # 6x6x6
    print(f"  ✓ Fill region: {count} voxels ({chunk})")

    # Get bounds
    bounds = chunk.get_bounds()
    assert bounds == ((10, 10, 10), (15, 15, 15))
    print(f"  ✓ Get bounds: {bounds}")

    # Count material
    assert chunk.count_material(1) == 216
    assert chunk.count_material(2) == 0
    print(f"  ✓ Count material: 216 voxels of material 1")

    # Replace material
    replaced = chunk.replace_material(1, 2)
    assert replaced == 216
    assert chunk.count_material(1) == 0
    assert chunk.count_material(2) == 216
    print(f"  ✓ Replace material: {replaced} voxels (1 → 2)")

    # Clone
    copy = chunk.clone()
    copy.set_voxel(20, 20, 20, material=3)
    assert chunk.get_voxel(20, 20, 20) == 0  # Original unchanged
    assert copy.get_voxel(20, 20, 20) == 3
    print(f"  ✓ Clone: independent copy works")

    # Clear
    chunk.clear()
    assert chunk.is_empty()
    assert copy.voxel_count() == 217  # Original had 216, plus 1 new
    print(f"  ✓ Clear: chunk empty, copy unaffected")

    print(f"  ✓ Stage 2 complete!")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("VOXEL CHUNK - Stages 1 & 2")
    print("=" * 80)
    print()

    test_basic_chunk()
    test_chunk_operations()

    print()
    print("=" * 80)
    print("✓ Stages 1 & 2 complete!")
    print("Next: Stage 3 - ChunkedVoxelWorld manager")
    print("=" * 80)
