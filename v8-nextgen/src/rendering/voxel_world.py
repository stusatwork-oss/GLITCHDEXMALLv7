#!/usr/bin/env python3
"""
VoxelWorld - Multi-Chunk World Manager

Manages multiple 32³ VoxelChunks in world space.
Based on Biomes' SparseTensorBuilder pattern (sparse.hpp:75-115).

Reference:
  - biomes-game/voxeloo/tensors/sparse.hpp:75-115
  - See: v8-nextgen/reference/biomes/voxel_math/sparse.hpp
"""

from typing import Dict, Optional, Tuple, Iterator, List
from dataclasses import dataclass
import sys

# Import chunk and encoding
sys.path.insert(0, '.')
from voxel_chunk import VoxelChunk
from voxel_encoding import (
    CHUNK_SIZE,
    world_to_chunk,
    world_to_local,
)


# =============================================================================
# CHUNKED VOXEL WORLD (Stage 3: World Manager)
# =============================================================================

class ChunkedVoxelWorld:
    """
    Multi-chunk voxel world manager.

    Provides world-space voxel access across multiple 32³ chunks.
    Matches Biomes' SparseTensorBuilder pattern (sparse.hpp:75-115).

    Chunks are lazily created on first write to their region.
    Empty chunks are automatically removed to save memory.

    Attributes:
        chunks: Dict of {(cx, cy, cz): VoxelChunk}

    Example:
        >>> world = ChunkedVoxelWorld()
        >>> world.set_voxel(100, 200, 50, material_id=1)  # Auto-creates chunk (3, 6, 1)
        >>> world.get_voxel(100, 200, 50)
        1
        >>> world.chunk_count()
        1
    """

    def __init__(self):
        """Initialize empty world."""
        self.chunks: Dict[Tuple[int, int, int], VoxelChunk] = {}

    # =========================================================================
    # CORE VOXEL ACCESS (World Space)
    # =========================================================================

    def set_voxel(self, world_x: int, world_y: int, world_z: int, material: int) -> None:
        """
        Set voxel material at world coordinates.

        Args:
            world_x, world_y, world_z: World coordinates (any integer)
            material: Material ID (0 = air, removes voxel)

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.set_voxel(100, 200, 50, material_id=1)
            >>> world.get_voxel(100, 200, 50)
            1
        """
        # Convert world → chunk + local
        chunk_pos = world_to_chunk(world_x, world_y, world_z)
        local_x, local_y, local_z = world_to_local(world_x, world_y, world_z)

        # Get or create chunk
        if chunk_pos not in self.chunks:
            if material == 0:
                return  # Don't create chunk just to set air
            self.chunks[chunk_pos] = VoxelChunk(position=chunk_pos)

        # Set voxel in chunk
        chunk = self.chunks[chunk_pos]
        chunk.set_voxel(local_x, local_y, local_z, material)

        # Remove empty chunks to save memory
        if chunk.is_empty():
            del self.chunks[chunk_pos]

    def get_voxel(self, world_x: int, world_y: int, world_z: int) -> int:
        """
        Get voxel material at world coordinates.

        Args:
            world_x, world_y, world_z: World coordinates (any integer)

        Returns:
            Material ID (0 = air)

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.set_voxel(100, 200, 50, material_id=3)
            >>> world.get_voxel(100, 200, 50)
            3
            >>> world.get_voxel(0, 0, 0)  # Unloaded chunk = air
            0
        """
        # Convert world → chunk + local
        chunk_pos = world_to_chunk(world_x, world_y, world_z)

        # Return air if chunk not loaded
        if chunk_pos not in self.chunks:
            return 0

        local_x, local_y, local_z = world_to_local(world_x, world_y, world_z)
        return self.chunks[chunk_pos].get_voxel(local_x, local_y, local_z)

    # =========================================================================
    # CHUNK MANAGEMENT
    # =========================================================================

    def get_chunk(self, cx: int, cy: int, cz: int) -> Optional[VoxelChunk]:
        """
        Get chunk at chunk coordinates.

        Args:
            cx, cy, cz: Chunk coordinates

        Returns:
            VoxelChunk or None if not loaded

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.set_voxel(100, 200, 50, 1)
            >>> chunk = world.get_chunk(3, 6, 1)  # 100//32=3, 200//32=6, 50//32=1
            >>> chunk.voxel_count()
            1
        """
        return self.chunks.get((cx, cy, cz))

    def load_chunk(self, cx: int, cy: int, cz: int) -> VoxelChunk:
        """
        Load (or get existing) chunk at coordinates.

        Args:
            cx, cy, cz: Chunk coordinates

        Returns:
            VoxelChunk (created if doesn't exist)

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> chunk = world.load_chunk(0, 0, 0)
            >>> chunk.position
            (0, 0, 0)
        """
        chunk_pos = (cx, cy, cz)
        if chunk_pos not in self.chunks:
            self.chunks[chunk_pos] = VoxelChunk(position=chunk_pos)
        return self.chunks[chunk_pos]

    def unload_chunk(self, cx: int, cy: int, cz: int) -> bool:
        """
        Unload chunk at coordinates.

        Args:
            cx, cy, cz: Chunk coordinates

        Returns:
            True if chunk was unloaded, False if not loaded

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.set_voxel(100, 200, 50, 1)
            >>> world.unload_chunk(3, 6, 1)
            True
            >>> world.get_voxel(100, 200, 50)  # Now returns air
            0
        """
        chunk_pos = (cx, cy, cz)
        if chunk_pos in self.chunks:
            del self.chunks[chunk_pos]
            return True
        return False

    def chunk_count(self) -> int:
        """
        Get number of loaded chunks.

        Returns:
            Count of loaded chunks

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.chunk_count()
            0
            >>> world.set_voxel(0, 0, 0, 1)
            >>> world.set_voxel(100, 100, 100, 1)
            >>> world.chunk_count()
            2
        """
        return len(self.chunks)

    # =========================================================================
    # WORLD OPERATIONS
    # =========================================================================

    def fill_box(
        self,
        x_min: int, x_max: int,
        y_min: int, y_max: int,
        z_min: int, z_max: int,
        material: int
    ) -> int:
        """
        Fill a box region in world space.

        Args:
            x_min, x_max: X range (inclusive, world coords)
            y_min, y_max: Y range (inclusive, world coords)
            z_min, z_max: Z range (inclusive, world coords)
            material: Material ID to fill with

        Returns:
            Number of voxels set

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.fill_box(0, 63, 0, 63, 0, 31, material=1)
            131072  # 64x64x32 = 131,072 voxels
        """
        count = 0
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                for z in range(z_min, z_max + 1):
                    self.set_voxel(x, y, z, material)
                    count += 1
        return count

    def clear_all(self) -> None:
        """
        Clear entire world (unload all chunks).

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.fill_box(0, 100, 0, 100, 0, 100, 1)
            1030301
            >>> world.clear_all()
            >>> world.chunk_count()
            0
        """
        self.chunks.clear()

    # =========================================================================
    # STATS & ITERATION
    # =========================================================================

    def voxel_count(self) -> int:
        """
        Get total number of non-air voxels across all chunks.

        Returns:
            Total voxel count

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.set_voxel(0, 0, 0, 1)
            >>> world.set_voxel(100, 100, 100, 1)
            >>> world.voxel_count()
            2
        """
        return sum(chunk.voxel_count() for chunk in self.chunks.values())

    def memory_usage(self) -> Dict[str, int]:
        """
        Calculate total memory usage across all chunks.

        Returns:
            Dict with memory stats in bytes

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.fill_box(0, 63, 0, 63, 0, 31, 1)
            131072
            >>> stats = world.memory_usage()
            >>> stats['voxel_count']
            131072
        """
        total_voxels = 0
        total_bytes = 0

        for chunk in self.chunks.values():
            chunk_stats = chunk.memory_usage()
            total_voxels += chunk_stats['voxel_count']
            total_bytes += chunk_stats['total_bytes']

        return {
            'chunk_count': len(self.chunks),
            'voxel_count': total_voxels,
            'total_bytes': total_bytes,
            'bytes_per_voxel': total_bytes / total_voxels if total_voxels > 0 else 0,
            'bytes_per_chunk': total_bytes / len(self.chunks) if self.chunks else 0,
        }

    def iter_chunks(self) -> Iterator[VoxelChunk]:
        """
        Iterate over all loaded chunks.

        Yields:
            VoxelChunk instances

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.set_voxel(0, 0, 0, 1)
            >>> world.set_voxel(100, 100, 100, 2)
            >>> for chunk in world.iter_chunks():
            ...     print(chunk.position, chunk.voxel_count())
            (0, 0, 0) 1
            (3, 3, 3) 1
        """
        return iter(self.chunks.values())

    def iter_voxels(self) -> Iterator[Tuple[int, int, int, int]]:
        """
        Iterate over all non-air voxels in world space.

        Yields:
            Tuples of (world_x, world_y, world_z, material_id)

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.set_voxel(5, 10, 15, 1)
            >>> world.set_voxel(100, 200, 50, 2)
            >>> list(world.iter_voxels())
            [(5, 10, 15, 1), (100, 200, 50, 2)]
        """
        for chunk in self.chunks.values():
            cx, cy, cz = chunk.position
            chunk_base_x = cx * CHUNK_SIZE
            chunk_base_y = cy * CHUNK_SIZE
            chunk_base_z = cz * CHUNK_SIZE

            for local_x, local_y, local_z, material in chunk.iter_voxels():
                world_x = chunk_base_x + local_x
                world_y = chunk_base_y + local_y
                world_z = chunk_base_z + local_z
                yield (world_x, world_y, world_z, material)

    # =========================================================================
    # REPR
    # =========================================================================

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"ChunkedVoxelWorld(chunks={len(self.chunks)}, "
            f"voxels={self.voxel_count()})"
        )


# =============================================================================
# TESTS
# =============================================================================

def test_world_basic():
    """Test basic world operations (Stage 3)."""
    print("Testing ChunkedVoxelWorld (Stage 3: World Manager)...")

    # Create world
    world = ChunkedVoxelWorld()
    assert world.chunk_count() == 0
    print(f"  ✓ Created empty world: {world}")

    # Set voxels in different chunks
    world.set_voxel(0, 0, 0, material=1)        # Chunk (0, 0, 0)
    world.set_voxel(100, 200, 50, material=2)   # Chunk (3, 6, 1)
    world.set_voxel(31, 31, 31, material=3)     # Chunk (0, 0, 0) - same as first
    assert world.chunk_count() == 2
    assert world.voxel_count() == 3
    print(f"  ✓ Set voxels in 2 chunks: {world}")

    # Get voxels
    assert world.get_voxel(0, 0, 0) == 1
    assert world.get_voxel(100, 200, 50) == 2
    assert world.get_voxel(31, 31, 31) == 3
    assert world.get_voxel(1000, 1000, 1000) == 0  # Unloaded chunk
    print(f"  ✓ Get voxels working")

    # Chunk access
    chunk_0 = world.get_chunk(0, 0, 0)
    assert chunk_0 is not None
    assert chunk_0.voxel_count() == 2  # Has (0,0,0) and (31,31,31)
    print(f"  ✓ Chunk access: {chunk_0}")

    # Memory usage
    stats = world.memory_usage()
    print(f"  ✓ Memory: {stats['total_bytes']} bytes for {stats['voxel_count']} voxels in {stats['chunk_count']} chunks")

    # Iteration
    voxels = list(world.iter_voxels())
    assert len(voxels) == 3
    print(f"  ✓ Iteration: {len(voxels)} voxels")

    print(f"  ✓ Stage 3 basic tests complete!")


def test_world_operations():
    """Test world-space operations."""
    print("\nTesting ChunkedVoxelWorld (Stage 3: World Operations)...")

    # Fill box across chunks
    world = ChunkedVoxelWorld()
    count = world.fill_box(0, 63, 0, 63, 0, 31, material=1)
    assert count == 64 * 64 * 32  # 131,072 voxels
    assert world.chunk_count() == 4  # 2x2x1 chunks (X:0-1, Y:0-1, Z:0)
    print(f"  ✓ Fill box: {count:,} voxels across {world.chunk_count()} chunks")

    # Unload chunk
    world.unload_chunk(0, 0, 0)
    assert world.chunk_count() == 3  # 4 - 1 = 3 chunks remaining
    assert world.get_voxel(0, 0, 0) == 0  # Now air
    print(f"  ✓ Unload chunk: {world.chunk_count()} chunks remain")

    # Clear all
    world.clear_all()
    assert world.chunk_count() == 0
    assert world.voxel_count() == 0
    print(f"  ✓ Clear all: {world}")

    print(f"  ✓ Stage 3 operations complete!")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("CHUNKED VOXEL WORLD - Stage 3")
    print("=" * 80)
    print()

    test_world_basic()
    test_world_operations()

    print()
    print("=" * 80)
    print("✓ Stage 3 complete!")
    print("Next: Integration with voxel_builder.py for mall construction")
    print("=" * 80)
