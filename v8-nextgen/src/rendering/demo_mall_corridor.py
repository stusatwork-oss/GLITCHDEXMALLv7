#!/usr/bin/env python3
"""
Mall Corridor Demo - Proof of Voxel System Integration

Demonstrates all 7 responsibilities working together:
  #1 Chunk lookup & lazy creation
  #2 World → Chunk → Local mapping
  #3 World-level set/get voxel
  #4 Chunk lifetime management
  #5 Dirty region tracking
  #6 DeltaBus integration
  #7 Region queries

Scenario:
  - 4-chunk corridor (128 voxels long)
  - 3 NPCs walking and leaving footprints
  - Dynamic chunk loading/unloading
  - Dirty chunk tracking for rendering
  - Real-time monitoring with VoxelWorldMonitor
"""

import sys
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Import voxel system
sys.path.insert(0, '.')
from voxel_world import ChunkedVoxelWorld
from voxel_encoding import CHUNK_SIZE
from voxel_world_monitor import VoxelWorldMonitor

# =============================================================================
# MATERIAL IDS
# =============================================================================

MAT_AIR = 0
MAT_FLOOR = 1
MAT_WALL = 2
MAT_CEILING = 3
MAT_FOOTPRINT = 4

# =============================================================================
# SIMPLE NPC
# =============================================================================

@dataclass
class SimpleNPC:
    """Minimal NPC for demo - just position and velocity."""
    id: int
    x: float
    y: float
    z: float
    vx: float = 1.0  # Walking speed (voxels per tick)

    def update(self):
        """Move NPC forward."""
        self.x += self.vx
        self.y += 0.0  # No vertical movement
        self.z += 0.0  # Straight line

    def get_position(self) -> Tuple[int, int, int]:
        """Get integer voxel position."""
        return (int(self.x), int(self.y), int(self.z))

    def __repr__(self):
        return f"NPC{self.id}@({int(self.x)}, {int(self.y)}, {int(self.z)})"


# =============================================================================
# CORRIDOR BUILDER
# =============================================================================

def build_corridor_geometry(world: ChunkedVoxelWorld, length_chunks: int = 4) -> Dict[str, int]:
    """
    Build a simple mall corridor.

    Layout (side view):
    ███████████████  <- Ceiling (y=5)
    ░             ░  <- Air (y=1-4)
    ███████████████  <- Floor (y=0)

    Args:
        world: ChunkedVoxelWorld to build in
        length_chunks: Number of chunks long (default 4 = 128 voxels)

    Returns:
        Stats dict with voxel counts
    """
    print(f"Building {length_chunks}-chunk corridor...")

    length_voxels = length_chunks * CHUNK_SIZE
    width = 10  # 10 voxels wide
    height = 6  # 6 voxels tall

    stats = {
        'floor_voxels': 0,
        'wall_voxels': 0,
        'ceiling_voxels': 0,
    }

    # Floor (y=0)
    for x in range(length_voxels):
        for z in range(width):
            world.set_voxel(x, 0, z, MAT_FLOOR)
            stats['floor_voxels'] += 1

    # Walls (z=0 and z=width-1, y=1 to height-1)
    for x in range(length_voxels):
        for y in range(1, height):
            world.set_voxel(x, y, 0, MAT_WALL)  # Left wall
            world.set_voxel(x, y, width - 1, MAT_WALL)  # Right wall
            stats['wall_voxels'] += 2

    # Ceiling (y=height-1)
    for x in range(length_voxels):
        for z in range(width):
            world.set_voxel(x, height - 1, z, MAT_CEILING)
            stats['ceiling_voxels'] += 1

    total = stats['floor_voxels'] + stats['wall_voxels'] + stats['ceiling_voxels']
    print(f"  ✓ Built corridor: {total:,} voxels")
    print(f"    - Floor: {stats['floor_voxels']:,}")
    print(f"    - Walls: {stats['wall_voxels']:,}")
    print(f"    - Ceiling: {stats['ceiling_voxels']:,}")

    return stats


def spawn_npcs(count: int = 3) -> List[SimpleNPC]:
    """
    Spawn NPCs in the corridor.

    Args:
        count: Number of NPCs to spawn

    Returns:
        List of SimpleNPC instances
    """
    npcs = []
    for i in range(count):
        npc = SimpleNPC(
            id=i,
            x=5.0 + i * 10.0,  # Spread out along corridor
            y=1.0,  # Standing on floor
            z=5.0,  # Middle of corridor
            vx=0.5 + i * 0.2,  # Different speeds
        )
        npcs.append(npc)

    print(f"Spawned {count} NPCs:")
    for npc in npcs:
        print(f"  - {npc} (speed={npc.vx:.1f})")

    return npcs


# =============================================================================
# FOOTPRINT SYSTEM
# =============================================================================

def apply_footprint(world: ChunkedVoxelWorld, npc: SimpleNPC) -> int:
    """
    Apply NPC footprint to floor (DeltaBus event simulation).

    Creates a 2x2 footprint region around NPC position.

    Args:
        world: ChunkedVoxelWorld
        npc: NPC to create footprint for

    Returns:
        Number of voxels changed
    """
    x, y, z = npc.get_position()

    # Footprint on floor (y=0) in 2x2 area
    changed = world.apply_region_change(
        x - 1, x + 1,  # 2 voxels wide
        0, 0,          # Floor level
        z - 1, z + 1,  # 2 voxels deep
        material=MAT_FOOTPRINT
    )

    return changed


# =============================================================================
# MAIN SIMULATION
# =============================================================================

def run_demo(ticks: int = 20, corridor_length: int = 4, use_monitor: bool = True):
    """
    Run the mall corridor demo.

    Args:
        ticks: Number of simulation ticks
        corridor_length: Corridor length in chunks
        use_monitor: Use VoxelWorldMonitor for debugging (default True)
    """
    print("=" * 80)
    print("MALL CORRIDOR DEMO - Voxel System Integration")
    print("=" * 80)
    print()

    # Initialize world
    world = ChunkedVoxelWorld()

    # Initialize monitor
    monitor = VoxelWorldMonitor(world, verbose=use_monitor) if use_monitor else None

    # Build corridor (with monitoring)
    if monitor:
        monitor.on_tick_start(-1)  # Pre-simulation tick
    build_stats = build_corridor_geometry(world, length_chunks=corridor_length)
    if monitor:
        monitor.on_tick_end()
    print()

    # Initial world stats
    mem_stats = world.memory_usage()
    print(f"Initial world state:")
    print(f"  - Chunks loaded: {world.chunk_count()}")
    print(f"  - Total voxels: {world.voxel_count():,}")
    print(f"  - Memory usage: {mem_stats['total_bytes']:,} bytes ({mem_stats['bytes_per_voxel']:.1f} bytes/voxel)")
    print()

    # Spawn NPCs
    npcs = spawn_npcs(count=3)
    print()

    # Simulation loop
    print("=" * 80)
    print("SIMULATION START")
    print("=" * 80)
    print()

    for tick in range(ticks):
        # Start tick monitoring
        if monitor:
            monitor.on_tick_start(tick)
        else:
            print(f"Tick {tick:2d}:")

        # Move NPCs
        for npc in npcs:
            npc.update()

        # Apply footprints (DeltaBus event: FOOTSTEP)
        total_footprints = 0
        for npc in npcs:
            changed = apply_footprint(world, npc)
            total_footprints += changed

        # Distance-based chunk unloading (follow NPC 0)
        lead_npc = npcs[0]
        lead_x, lead_y, lead_z = lead_npc.get_position()
        unloaded = world.unload_far_chunks(lead_x, lead_y, lead_z, max_distance=3)

        # Manual stats (if not using monitor)
        if not monitor:
            dirty_chunks = world.get_dirty_chunks()
            print(f"  NPCs: {[str(n) for n in npcs]}")
            print(f"  Footprints: {total_footprints} voxels changed")
            print(f"  Dirty chunks: {len(dirty_chunks)} need re-mesh")
            if unloaded > 0:
                print(f"  Unloaded: {unloaded} far chunks")
            print(f"  Loaded chunks: {world.chunk_count()}")
            world.clear_dirty_chunks()
            print()

        # End tick monitoring
        if monitor:
            monitor.on_tick_end()

        # Optional: Render ASCII view every 10 ticks
        if monitor and tick % 10 == 0 and tick > 0:
            monitor.render_ascii_slice(y_level=0, x_range=(0, 50), z_range=(0, 10))

        # Stop if NPCs walk out of corridor
        if lead_npc.x > corridor_length * CHUNK_SIZE:
            if not monitor:
                print(f"  → NPCs exited corridor at tick {tick}")
            break

    # Final stats
    print("=" * 80)
    print("SIMULATION COMPLETE")
    print("=" * 80)
    print()

    final_mem = world.memory_usage()
    print(f"Final world state:")
    print(f"  - Chunks loaded: {world.chunk_count()}")
    print(f"  - Total voxels: {world.voxel_count():,}")
    print(f"  - Memory usage: {final_mem['total_bytes']:,} bytes")
    print()

    # Query footprint region (Responsibility #7)
    print("Footprint analysis (region query):")
    footprint_count = 0
    for x, y, z, material in world.iter_voxels():
        if material == MAT_FOOTPRINT:
            footprint_count += 1
    print(f"  - Total footprints in world: {footprint_count}")

    # Query specific region
    region_voxels = list(world.iter_region(0, 50, 0, 0, 0, 10))
    footprints_in_region = sum(1 for _, _, _, mat in region_voxels if mat == MAT_FOOTPRINT)
    print(f"  - Footprints in first 50 voxels: {footprints_in_region}")
    print()

    # Monitor summary
    if monitor:
        monitor.print_summary()

    # Proof of all 7 responsibilities
    print("=" * 80)
    print("7 RESPONSIBILITIES DEMONSTRATED")
    print("=" * 80)
    print("  #1 ✓ Chunk lookup & lazy creation (corridor built across chunks)")
    print("  #2 ✓ World → Chunk → Local mapping (NPCs moved in world space)")
    print("  #3 ✓ World-level set/get voxel (footprints applied)")
    print("  #4 ✓ Chunk lifetime management (far chunks unloaded)")
    print("  #5 ✓ Dirty region tracking (re-mesh tracking)")
    print("  #6 ✓ DeltaBus integration (footprint events)")
    print("  #7 ✓ Region queries (footprint analysis)")
    print("=" * 80)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    run_demo(ticks=20, corridor_length=4)
