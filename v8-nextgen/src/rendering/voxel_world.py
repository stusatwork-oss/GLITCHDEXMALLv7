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
        dirty_chunks: Set of chunk coords that need re-meshing

    Example:
        >>> world = ChunkedVoxelWorld()
        >>> world.set_voxel(100, 200, 50, material_id=1)  # Auto-creates chunk (3, 6, 1)
        >>> world.get_voxel(100, 200, 50)
        1
        >>> world.chunk_count()
        1
        >>> world.get_dirty_chunks()  # Returns [(3, 6, 1)]
        [(3, 6, 1)]
    """

    def __init__(self):
        """Initialize empty world."""
        self.chunks: Dict[Tuple[int, int, int], VoxelChunk] = {}
        self.dirty_chunks: set = set()  # Chunks needing re-mesh

    # =========================================================================
    # CORE VOXEL ACCESS (World Space)
    # =========================================================================

    def set_voxel(self, world_x: int, world_y: int, world_z: int, material: int) -> None:
        """
        Set voxel material at world coordinates.

        Automatically marks chunk as dirty for re-meshing.

        Args:
            world_x, world_y, world_z: World coordinates (any integer)
            material: Material ID (0 = air, removes voxel)

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.set_voxel(100, 200, 50, material_id=1)
            >>> world.get_voxel(100, 200, 50)
            1
            >>> world.is_chunk_dirty(3, 6, 1)
            True
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

        # Mark chunk dirty (needs re-mesh)
        self.dirty_chunks.add(chunk_pos)

        # Remove empty chunks to save memory
        if chunk.is_empty():
            del self.chunks[chunk_pos]
            self.dirty_chunks.discard(chunk_pos)  # No longer dirty if deleted

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
            self.dirty_chunks.discard(chunk_pos)  # Clean up dirty tracking
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
    # DIRTY REGION TRACKING (Responsibility #5)
    # =========================================================================

    def get_dirty_chunks(self) -> List[Tuple[int, int, int]]:
        """
        Get list of chunks that need re-meshing.

        Returns:
            List of dirty chunk coordinates

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.set_voxel(100, 200, 50, 1)
            >>> world.get_dirty_chunks()
            [(3, 6, 1)]
        """
        return list(self.dirty_chunks)

    def clear_dirty_chunks(self) -> int:
        """
        Clear dirty chunk tracking (call after re-meshing).

        Returns:
            Number of chunks that were dirty

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.set_voxel(0, 0, 0, 1)
            >>> world.set_voxel(100, 100, 100, 2)
            >>> dirty_count = world.clear_dirty_chunks()
            >>> dirty_count
            2
            >>> world.get_dirty_chunks()
            []
        """
        count = len(self.dirty_chunks)
        self.dirty_chunks.clear()
        return count

    def is_chunk_dirty(self, cx: int, cy: int, cz: int) -> bool:
        """
        Check if chunk needs re-meshing.

        Args:
            cx, cy, cz: Chunk coordinates

        Returns:
            True if chunk is dirty

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.set_voxel(0, 0, 0, 1)
            >>> world.is_chunk_dirty(0, 0, 0)
            True
        """
        return (cx, cy, cz) in self.dirty_chunks

    def mark_chunk_dirty(self, cx: int, cy: int, cz: int) -> None:
        """
        Manually mark chunk as dirty (for external modifications).

        Args:
            cx, cy, cz: Chunk coordinates

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.load_chunk(0, 0, 0)
            >>> world.mark_chunk_dirty(0, 0, 0)
            >>> world.is_chunk_dirty(0, 0, 0)
            True
        """
        if (cx, cy, cz) in self.chunks:
            self.dirty_chunks.add((cx, cy, cz))

    # =========================================================================
    # CHUNK LIFETIME MANAGEMENT (Responsibility #4)
    # =========================================================================

    def unload_far_chunks(self, center_x: int, center_y: int, center_z: int, max_distance: int) -> int:
        """
        Unload chunks beyond max distance from center (in chunk units).

        Args:
            center_x, center_y, center_z: Center world coordinates
            max_distance: Max chunk distance to keep loaded

        Returns:
            Number of chunks unloaded

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> # Load chunks at various distances
            >>> world.set_voxel(0, 0, 0, 1)      # Chunk (0,0,0)
            >>> world.set_voxel(1000, 1000, 1000, 1)  # Chunk (31,31,31) - far away
            >>> # Unload chunks >5 chunks from origin
            >>> unloaded = world.unload_far_chunks(0, 0, 0, max_distance=5)
            >>> unloaded
            1
        """
        center_chunk = world_to_chunk(center_x, center_y, center_z)
        cx_center, cy_center, cz_center = center_chunk

        to_unload = []
        for chunk_pos in list(self.chunks.keys()):
            cx, cy, cz = chunk_pos
            # Chebyshev distance (max of absolute differences)
            distance = max(abs(cx - cx_center), abs(cy - cy_center), abs(cz - cz_center))
            if distance > max_distance:
                to_unload.append(chunk_pos)

        for chunk_pos in to_unload:
            del self.chunks[chunk_pos]
            self.dirty_chunks.discard(chunk_pos)

        return len(to_unload)

    # =========================================================================
    # DELTABUS INTEGRATION (Responsibility #6)
    # =========================================================================

    def apply_voxel_delta(self, delta_dict: Dict[Tuple[int, int, int], int]) -> int:
        """
        Apply voxel changes from DeltaBus event.

        Args:
            delta_dict: {(world_x, world_y, world_z): material_id}

        Returns:
            Number of voxels changed

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> delta = {(0, 0, 0): 1, (10, 20, 30): 2, (100, 200, 50): 3}
            >>> world.apply_voxel_delta(delta)
            3
            >>> world.voxel_count()
            3
        """
        count = 0
        for (x, y, z), material in delta_dict.items():
            self.set_voxel(x, y, z, material)
            count += 1
        return count

    def apply_region_change(
        self,
        x_min: int, x_max: int,
        y_min: int, y_max: int,
        z_min: int, z_max: int,
        material: int
    ) -> int:
        """
        Apply material change to region (for event-driven updates).

        Use cases:
        - Sand settling (physics event)
        - NPC footprint (behavior event)
        - Cloak ripple effect (WATTITUDE event)
        - Destructible props (collision event)

        Args:
            x_min, x_max, y_min, y_max, z_min, z_max: Region bounds (world coords)
            material: Material ID to apply

        Returns:
            Number of voxels changed

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> # Footprint event: 3x3 area
            >>> world.apply_region_change(10, 12, 5, 7, 0, 0, material=5)
            9
        """
        return self.fill_box(x_min, x_max, y_min, y_max, z_min, z_max, material)

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

    def iter_region(
        self,
        x_min: int, x_max: int,
        y_min: int, y_max: int,
        z_min: int, z_max: int
    ) -> Iterator[Tuple[int, int, int, int]]:
        """
        Iterate over voxels in a specific region (Responsibility #7).

        Use cases:
        - Crowd density analysis (Rust Bram)
        - Cloak ripple detection
        - Minion pathfinding
        - NPC footprint tracking
        - Spatial queries for Mall_OS

        Args:
            x_min, x_max: X range (inclusive, world coords)
            y_min, y_max: Y range (inclusive, world coords)
            z_min, z_max: Z range (inclusive, world coords)

        Yields:
            Tuples of (world_x, world_y, world_z, material_id)

        Example:
            >>> world = ChunkedVoxelWorld()
            >>> world.set_voxel(5, 10, 15, 1)
            >>> world.set_voxel(100, 200, 50, 2)
            >>> # Query region around origin
            >>> list(world.iter_region(0, 10, 0, 15, 0, 20))
            [(5, 10, 15, 1)]
        """
        for world_x, world_y, world_z, material in self.iter_voxels():
            if (x_min <= world_x <= x_max and
                y_min <= world_y <= y_max and
                z_min <= world_z <= z_max):
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


def test_dirty_tracking():
    """Test dirty chunk tracking (Responsibility #5)."""
    print("\nTesting Dirty Chunk Tracking...")

    world = ChunkedVoxelWorld()

    # Set voxel marks chunk dirty
    world.set_voxel(0, 0, 0, 1)
    assert world.is_chunk_dirty(0, 0, 0)
    assert len(world.get_dirty_chunks()) == 1
    print(f"  ✓ set_voxel marks chunk dirty")

    # Multiple changes to same chunk
    world.set_voxel(10, 10, 10, 2)
    assert len(world.get_dirty_chunks()) == 1  # Still only 1 chunk
    print(f"  ✓ Multiple changes to same chunk tracked")

    # Clear dirty chunks
    dirty_count = world.clear_dirty_chunks()
    assert dirty_count == 1
    assert len(world.get_dirty_chunks()) == 0
    assert not world.is_chunk_dirty(0, 0, 0)
    print(f"  ✓ clear_dirty_chunks works")

    # Manual marking
    world.mark_chunk_dirty(0, 0, 0)
    assert world.is_chunk_dirty(0, 0, 0)
    print(f"  ✓ mark_chunk_dirty works")

    print(f"  ✓ Dirty tracking complete!")


def test_distance_unloading():
    """Test distance-based chunk unloading (Responsibility #4)."""
    print("\nTesting Distance-Based Chunk Unloading...")

    world = ChunkedVoxelWorld()

    # Load chunks at various distances
    world.set_voxel(0, 0, 0, 1)          # Chunk (0, 0, 0) - distance 0
    world.set_voxel(64, 64, 64, 2)       # Chunk (2, 2, 2) - distance 2
    world.set_voxel(320, 320, 320, 3)    # Chunk (10, 10, 10) - distance 10
    assert world.chunk_count() == 3
    print(f"  ✓ Loaded 3 chunks at distances 0, 2, 10")

    # Unload chunks beyond distance 5
    unloaded = world.unload_far_chunks(0, 0, 0, max_distance=5)
    assert unloaded == 1  # Only (10,10,10) unloaded
    assert world.chunk_count() == 2
    assert world.get_voxel(320, 320, 320) == 0  # Far chunk now air
    assert world.get_voxel(0, 0, 0) == 1  # Near chunk still loaded
    print(f"  ✓ unload_far_chunks: {unloaded} chunk unloaded")

    print(f"  ✓ Distance unloading complete!")


def test_deltabus_integration():
    """Test DeltaBus integration (Responsibility #6)."""
    print("\nTesting DeltaBus Integration...")

    world = ChunkedVoxelWorld()

    # Apply voxel delta
    delta = {
        (0, 0, 0): 1,
        (10, 20, 30): 2,
        (100, 200, 50): 3,
    }
    changed = world.apply_voxel_delta(delta)
    assert changed == 3
    assert world.voxel_count() == 3
    print(f"  ✓ apply_voxel_delta: {changed} voxels changed")

    # Apply region change (footprint event)
    changed = world.apply_region_change(5, 7, 5, 7, 0, 0, material=5)
    assert changed == 9  # 3x3 area
    print(f"  ✓ apply_region_change: {changed} voxels (footprint)")

    print(f"  ✓ DeltaBus integration complete!")


def test_region_queries():
    """Test region iteration (Responsibility #7)."""
    print("\nTesting Region Queries...")

    world = ChunkedVoxelWorld()

    # Set voxels in different regions
    world.set_voxel(5, 10, 15, 1)      # Inside region
    world.set_voxel(100, 200, 50, 2)   # Outside region
    world.set_voxel(8, 12, 18, 3)      # Inside region

    # Query region
    region_voxels = list(world.iter_region(0, 10, 0, 15, 0, 20))
    assert len(region_voxels) == 2  # Only (5,10,15) and (8,12,18)
    print(f"  ✓ iter_region: {len(region_voxels)} voxels in region")

    # Full iteration still sees all
    all_voxels = list(world.iter_voxels())
    assert len(all_voxels) == 3
    print(f"  ✓ iter_voxels: {len(all_voxels)} total voxels")

    print(f"  ✓ Region queries complete!")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("CHUNKED VOXEL WORLD - 7 Responsibilities")
    print("=" * 80)
    print()

    test_world_basic()
    test_world_operations()
    test_dirty_tracking()
    test_distance_unloading()
    test_deltabus_integration()
    test_region_queries()

    print()
    print("=" * 80)
    print("✓ All 7 Responsibilities Implemented!")
    print("  #1 ✓ Chunk lookup & lazy creation")
    print("  #2 ✓ World → Chunk → Local mapping")
    print("  #3 ✓ World-level set/get voxel")
    print("  #4 ✓ Chunk lifetime management")
    print("  #5 ✓ Dirty region tracking")
    print("  #6 ✓ DeltaBus integration")
    print("  #7 ✓ Region queries")
    print()
    print("Next: Integration with voxel_builder.py for mall construction")
    print("=" * 80)
