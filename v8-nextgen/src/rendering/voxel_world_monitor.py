#!/usr/bin/env python3
"""
VoxelWorldMonitor - Debug Harness for ChunkedVoxelWorld

Provides real-time monitoring and debugging for voxel world operations:
- Chunk creation/unloading stats
- Dirty chunk tracking
- Memory usage over time
- Delta compression ratio
- ASCII top-down visualization

Usage:
    monitor = VoxelWorldMonitor(world)

    for tick in range(100):
        monitor.on_tick_start(tick)

        # ... game logic ...
        world.set_voxel(x, y, z, material)

        monitor.on_tick_end()

        # Optional: render ASCII view every 10 ticks
        if tick % 10 == 0:
            monitor.render_ascii_slice(y_level=0)
"""

from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field

# Import voxel system
import sys
sys.path.insert(0, '.')
from voxel_world import ChunkedVoxelWorld


# =============================================================================
# MONITOR STATE
# =============================================================================

@dataclass
class TickStats:
    """Stats for a single tick."""
    tick: int
    chunks_active: int
    chunks_created: int = 0
    chunks_unloaded: int = 0
    dirty_chunks_count: int = 0
    total_voxels: int = 0
    memory_bytes: int = 0
    voxels_changed: int = 0

    # Compression stats (if tracked)
    full_bytes: Optional[int] = None
    delta_bytes: Optional[int] = None
    compression_ratio: Optional[float] = None


# =============================================================================
# VOXEL WORLD MONITOR
# =============================================================================

class VoxelWorldMonitor:
    """
    Debug harness for ChunkedVoxelWorld.

    Tracks and reports:
    - Chunk lifecycle (creation/unloading)
    - Dirty chunk tracking (for render optimization)
    - Memory usage over time
    - Voxel delta compression ratios
    - ASCII visualization

    Example:
        >>> world = ChunkedVoxelWorld()
        >>> monitor = VoxelWorldMonitor(world)
        >>> monitor.on_tick_start(0)
        >>> world.set_voxel(10, 5, 10, 1)
        >>> monitor.on_tick_end()
        Tick 0: chunks=1, dirty=1, voxels=1, mem=8 bytes
    """

    def __init__(self, world: ChunkedVoxelWorld, delta_bus=None, verbose: bool = True):
        """
        Initialize monitor.

        Args:
            world: ChunkedVoxelWorld instance to monitor
            delta_bus: Optional DeltaBus for event tracking
            verbose: Print stats each tick (default True)
        """
        self.world = world
        self.delta_bus = delta_bus
        self.verbose = verbose

        # Current tick
        self.tick = 0

        # Track state between ticks
        self.prev_chunk_count = 0
        self.prev_voxel_count = 0
        self.prev_dirty_chunks: set = set()

        # History (for regression testing / analysis)
        self.history: List[TickStats] = []

        # Material symbols for ASCII rendering
        self.material_symbols = {
            0: '.',   # Air
            1: '#',   # Floor
            2: '█',   # Wall
            3: '▀',   # Ceiling
            4: '~',   # Footprint
            5: '*',   # Recently changed
        }

    # =========================================================================
    # TICK LIFECYCLE
    # =========================================================================

    def on_tick_start(self, tick: int):
        """
        Call at start of tick.

        Args:
            tick: Current tick number
        """
        self.tick = tick

        # Capture pre-tick state
        self.prev_chunk_count = self.world.chunk_count()
        self.prev_voxel_count = self.world.voxel_count()
        self.prev_dirty_chunks = set(self.world.get_dirty_chunks())

    def on_tick_end(self):
        """
        Call at end of tick (after all voxel changes).

        Logs stats and clears dirty chunks.
        """
        # Gather stats
        stats = self._gather_stats()

        # Add to history
        self.history.append(stats)

        # Log stats
        if self.verbose:
            self._log_stats(stats)

        # Clear dirty chunks (simulate re-meshing)
        self.world.clear_dirty_chunks()

    # =========================================================================
    # STATS GATHERING
    # =========================================================================

    def _gather_stats(self) -> TickStats:
        """
        Gather current tick stats.

        Returns:
            TickStats for current tick
        """
        current_chunks = self.world.chunk_count()
        current_voxels = self.world.voxel_count()
        dirty_chunks = self.world.get_dirty_chunks()

        # Calculate deltas
        chunks_created = max(0, current_chunks - self.prev_chunk_count)
        chunks_unloaded = max(0, self.prev_chunk_count - current_chunks)
        voxels_changed = abs(current_voxels - self.prev_voxel_count)

        # Memory stats
        mem_stats = self.world.memory_usage()

        # Compression ratio (estimated)
        # Sparse model: ~8 bytes/voxel (dict overhead)
        # Dense model: 32³ voxels × 1 byte = 32,768 bytes per chunk
        full_bytes = current_chunks * 32768  # Dense storage
        delta_bytes = mem_stats['total_bytes']  # Sparse storage
        compression_ratio = full_bytes / delta_bytes if delta_bytes > 0 else 1.0

        return TickStats(
            tick=self.tick,
            chunks_active=current_chunks,
            chunks_created=chunks_created,
            chunks_unloaded=chunks_unloaded,
            dirty_chunks_count=len(dirty_chunks),
            total_voxels=current_voxels,
            memory_bytes=mem_stats['total_bytes'],
            voxels_changed=voxels_changed,
            full_bytes=full_bytes,
            delta_bytes=delta_bytes,
            compression_ratio=compression_ratio,
        )

    def _log_stats(self, stats: TickStats):
        """
        Log stats to console.

        Args:
            stats: TickStats to log
        """
        # Basic stats
        print(f"Tick {stats.tick:3d}: "
              f"chunks={stats.chunks_active} "
              f"(+{stats.chunks_created}/-{stats.chunks_unloaded}), "
              f"dirty={stats.dirty_chunks_count}, "
              f"voxels={stats.total_voxels:,}, "
              f"mem={stats.memory_bytes:,}b")

        # Compression ratio (if significant savings)
        if stats.compression_ratio and stats.compression_ratio > 1.5:
            saved_pct = (1.0 - 1.0/stats.compression_ratio) * 100
            print(f"         compression: {stats.compression_ratio:.1f}x, "
                  f"{saved_pct:.0f}% saved "
                  f"({stats.delta_bytes:,}b vs {stats.full_bytes:,}b dense)")

    # =========================================================================
    # ASCII VISUALIZATION
    # =========================================================================

    def render_ascii_slice(self, y_level: int = 0, x_range: Tuple[int, int] = None, z_range: Tuple[int, int] = None):
        """
        Render ASCII top-down view of a horizontal slice.

        Args:
            y_level: Y coordinate to slice at (default 0 = floor)
            x_range: Optional (x_min, x_max) range to render
            z_range: Optional (z_min, z_max) range to render

        Example:
            >>> monitor.render_ascii_slice(y_level=0)

            Y=0 Slice (50x20):
            ████████████████████████████████████████████████
            █..............................................█
            █..............................................█
            █..............................................█
            ████████████████████████████████████████████████
        """
        # Auto-detect bounds if not specified
        if x_range is None or z_range is None:
            bounds = self._get_world_bounds()
            if bounds is None:
                print("  (Empty world - nothing to render)")
                return
            x_min, x_max, _, _, z_min, z_max = bounds
            if x_range is None:
                x_range = (x_min, min(x_max, x_min + 80))  # Max 80 wide
            if z_range is None:
                z_range = (z_min, min(z_max, z_min + 40))  # Max 40 tall

        x_min, x_max = x_range
        z_min, z_max = z_range

        print()
        print(f"Y={y_level} Slice ({x_max - x_min + 1}x{z_max - z_min + 1}):")
        print()

        # Get all voxels in slice
        voxels_in_slice = {}
        for x, y, z, material in self.world.iter_region(x_min, x_max, y_level, y_level, z_min, z_max):
            voxels_in_slice[(x, z)] = material

        # Render grid
        for z in range(z_min, z_max + 1):
            line = ""
            for x in range(x_min, x_max + 1):
                material = voxels_in_slice.get((x, z), 0)  # Default to air
                symbol = self.material_symbols.get(material, '?')
                line += symbol
            print(line)
        print()

    def _get_world_bounds(self) -> Optional[Tuple[int, int, int, int, int, int]]:
        """
        Get AABB bounds of entire world.

        Returns:
            (x_min, x_max, y_min, y_max, z_min, z_max) or None if empty
        """
        voxels = list(self.world.iter_voxels())
        if not voxels:
            return None

        x_coords = [x for x, y, z, m in voxels]
        y_coords = [y for x, y, z, m in voxels]
        z_coords = [z for x, y, z, m in voxels]

        return (
            min(x_coords), max(x_coords),
            min(y_coords), max(y_coords),
            min(z_coords), max(z_coords),
        )

    # =========================================================================
    # HISTORY & ANALYSIS
    # =========================================================================

    def get_history(self) -> List[TickStats]:
        """
        Get full tick history.

        Returns:
            List of TickStats for all ticks
        """
        return self.history

    def print_summary(self):
        """Print summary of entire monitoring session."""
        if not self.history:
            print("No history available")
            return

        print()
        print("=" * 80)
        print("MONITOR SUMMARY")
        print("=" * 80)

        total_ticks = len(self.history)
        max_chunks = max(s.chunks_active for s in self.history)
        max_voxels = max(s.total_voxels for s in self.history)
        max_dirty = max(s.dirty_chunks_count for s in self.history)
        total_created = sum(s.chunks_created for s in self.history)
        total_unloaded = sum(s.chunks_unloaded for s in self.history)

        avg_compression = sum(s.compression_ratio for s in self.history if s.compression_ratio) / total_ticks

        print(f"Total ticks: {total_ticks}")
        print(f"Chunks: max={max_chunks}, created={total_created}, unloaded={total_unloaded}")
        print(f"Voxels: max={max_voxels:,}")
        print(f"Dirty chunks: max={max_dirty}")
        print(f"Avg compression: {avg_compression:.1f}x")
        print("=" * 80)
        print()


# =============================================================================
# DEMO
# =============================================================================

def demo_monitor():
    """Demo the monitor with a simple scenario."""
    from voxel_world import ChunkedVoxelWorld

    print("=" * 80)
    print("VOXEL WORLD MONITOR - Demo")
    print("=" * 80)
    print()

    world = ChunkedVoxelWorld()
    monitor = VoxelWorldMonitor(world, verbose=True)

    # Build a small structure
    print("Building 3x3x3 cube...")
    monitor.on_tick_start(0)
    for x in range(3):
        for y in range(3):
            for z in range(3):
                world.set_voxel(x, y, z, 1)
    monitor.on_tick_end()

    # Modify it
    print("\nHollowing out center...")
    monitor.on_tick_start(1)
    world.set_voxel(1, 1, 1, 0)  # Remove center
    monitor.on_tick_end()

    # Add more voxels far away (new chunk)
    print("\nBuilding far structure...")
    monitor.on_tick_start(2)
    for x in range(100, 103):
        for z in range(100, 103):
            world.set_voxel(x, 0, z, 2)
    monitor.on_tick_end()

    # Render ASCII view
    monitor.render_ascii_slice(y_level=0)

    # Summary
    monitor.print_summary()


if __name__ == "__main__":
    demo_monitor()
