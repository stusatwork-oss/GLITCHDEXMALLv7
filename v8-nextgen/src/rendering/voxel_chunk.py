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
# STAGE 1 TESTS
# =============================================================================

def test_basic_chunk():
    """Test basic chunk operations."""
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


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("VOXEL CHUNK - Stage 1: Basic Storage")
    print("=" * 80)
    print()

    test_basic_chunk()

    print()
    print("=" * 80)
    print("✓ Stage 1 tests passed!")
    print("Next: Stage 2 - Chunk operations (fill, clear, neighbors)")
    print("=" * 80)
