#!/usr/bin/env python3
"""
MallSpatialBackend - Thin Facade for Mall_OS

The ONLY interface Mall_OS sees. Hides all voxel internals.

Responsibilities:
  1. World bootstrap (build zone geometry)
  2. Sim → geometry (DeltaBus events)
  3. Geometry → sim (spatial queries)

Architecture:
  Mall_OS / Synthactors / WATTITUDE
         ↓
  MallSpatialBackend ← YOU ARE HERE (facade)
         ↓
  VoxelWorldManager (orchestration)
         ↓
  ChunkedVoxelWorld (7 responsibilities)

Principles:
  - THIN: No logic, just routing
  - OPAQUE: Mall_OS never sees VoxelChunk or encoding
  - SEMANTIC: Methods named for game concepts (footprints, ripples)
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import sys

# Import voxel system
sys.path.insert(0, '.')
from voxel_world_manager import VoxelWorldManager, VoxelWorldConfig
from chunk_mesh_builder import ChunkMeshBuilder, MeshingStrategy


# =============================================================================
# EVENT TYPES (DeltaBus Integration)
# =============================================================================

class EventType(Enum):
    """DeltaBus event types that affect voxels."""
    VOXEL_CHANGE = "voxel_change"       # Direct voxel changes
    FOOTSTEP = "footstep"               # NPC footprint
    CLOAK_RIPPLE = "cloak_ripple"       # Cloak of In-Conspicuity
    DESTRUCTION = "destruction"         # Destructible props
    SAND_SETTLE = "sand_settle"         # Physics: sand settling


# =============================================================================
# ZONE GEOMETRY (Bootstrap)
# =============================================================================

@dataclass
class ZoneGeometrySpec:
    """Specification for zone geometry."""
    zone_id: str
    bounds: Tuple[int, int, int, int, int, int]  # (x_min, x_max, y_min, y_max, z_min, z_max)
    floor_material: int = 1
    wall_material: int = 2
    ceiling_material: int = 3


# =============================================================================
# MALL SPATIAL BACKEND
# =============================================================================

class MallSpatialBackend:
    """
    Thin facade between Mall_OS and voxel engine.

    Mall_OS ONLY sees this interface. All voxel internals hidden.

    Example:
        >>> backend = MallSpatialBackend()
        >>>
        >>> # Bootstrap world
        >>> backend.build_corridor(length=128, width=10, height=6)
        >>>
        >>> # Handle sim events
        >>> backend.apply_footprint(npc.x, npc.y, npc.z)
        >>> backend.apply_cloak_ripple(player.x, player.y, player.z, radius=3)
        >>>
        >>> # Query for sim logic
        >>> density = backend.query_crowd_density(region_bounds)
        >>>
        >>> # Sync with renderer
        >>> dirty_chunks = backend.get_dirty_chunks_for_render()
    """

    def __init__(self, config: Optional[VoxelWorldConfig] = None):
        """
        Initialize spatial backend.

        Args:
            config: Optional VoxelWorldConfig (uses defaults if not provided)
        """
        self.world = VoxelWorldManager(config)
        self.mesh_builder = ChunkMeshBuilder(strategy=MeshingStrategy.NAIVE_CUBES)

        # Material IDs (can be configured)
        self.MAT_AIR = 0
        self.MAT_FLOOR = 1
        self.MAT_WALL = 2
        self.MAT_CEILING = 3
        self.MAT_FOOTPRINT = 4
        self.MAT_CLOAK_RIPPLE = 5

    # =========================================================================
    # 1. WORLD BOOTSTRAP (Zone Geometry)
    # =========================================================================

    def build_corridor(self, length: int, width: int, height: int, x_offset: int = 0, y_offset: int = 0, z_offset: int = 0) -> Dict[str, int]:
        """
        Build simple corridor geometry.

        Args:
            length: Corridor length (X axis, in voxels)
            width: Corridor width (Z axis, in voxels)
            height: Corridor height (Y axis, in voxels)
            x_offset, y_offset, z_offset: World offset

        Returns:
            Stats dict with voxel counts

        Example:
            >>> backend.build_corridor(length=128, width=10, height=6)
        """
        stats = {'floor': 0, 'walls': 0, 'ceiling': 0}

        # Floor (y=0)
        for x in range(length):
            for z in range(width):
                self.world.set_voxel(x + x_offset, y_offset, z + z_offset, self.MAT_FLOOR)
                stats['floor'] += 1

        # Walls (z=0 and z=width-1)
        for x in range(length):
            for y in range(1, height):
                self.world.set_voxel(x + x_offset, y + y_offset, z_offset, self.MAT_WALL)
                self.world.set_voxel(x + x_offset, y + y_offset, width - 1 + z_offset, self.MAT_WALL)
                stats['walls'] += 2

        # Ceiling (y=height-1)
        for x in range(length):
            for z in range(width):
                self.world.set_voxel(x + x_offset, height - 1 + y_offset, z + z_offset, self.MAT_CEILING)
                stats['ceiling'] += 1

        return stats

    def build_zone_geometry(self, zone_id: str, geometry_spec: ZoneGeometrySpec) -> int:
        """
        Build zone geometry from spec.

        Args:
            zone_id: Zone identifier
            geometry_spec: ZoneGeometrySpec

        Returns:
            Number of voxels placed

        Example:
            >>> spec = ZoneGeometrySpec(
            ...     zone_id="food_court",
            ...     bounds=(0, 100, 0, 10, 0, 100)
            ... )
            >>> backend.build_zone_geometry("food_court", spec)
        """
        x_min, x_max, y_min, y_max, z_min, z_max = geometry_spec.bounds
        count = 0

        # Floor
        for x in range(x_min, x_max + 1):
            for z in range(z_min, z_max + 1):
                self.world.set_voxel(x, y_min, z, geometry_spec.floor_material)
                count += 1

        # Walls (simplified)
        for x in range(x_min, x_max + 1):
            for y in range(y_min + 1, y_max):
                self.world.set_voxel(x, y, z_min, geometry_spec.wall_material)
                self.world.set_voxel(x, y, z_max, geometry_spec.wall_material)
                count += 2

        # Ceiling
        for x in range(x_min, x_max + 1):
            for z in range(z_min, z_max + 1):
                self.world.set_voxel(x, y_max, z, geometry_spec.ceiling_material)
                count += 1

        return count

    # =========================================================================
    # 2. SIM → GEOMETRY (DeltaBus Events)
    # =========================================================================

    def apply_voxel_event(self, delta_event: Dict[str, Any]) -> int:
        """
        Apply voxel event from DeltaBus.

        This is the main entry point for Mall_OS → voxel updates.

        Args:
            delta_event: DeltaBus event dict with 'kind' and 'payload'

        Returns:
            Number of voxels changed

        Example:
            >>> event = {
            ...     'kind': EventType.FOOTSTEP,
            ...     'payload': {'x': 10, 'y': 0, 'z': 5}
            ... }
            >>> backend.apply_voxel_event(event)
        """
        return self.world.handle_deltabus_event(delta_event)

    def apply_footprint(self, x: int, y: int, z: int, size: int = 1) -> int:
        """
        Apply NPC footprint (high-level semantic call).

        Args:
            x, y, z: Footprint center (world coords)
            size: Footprint radius (1 = 2x2, 2 = 4x4, etc.)

        Returns:
            Number of voxels changed

        Example:
            >>> backend.apply_footprint(npc.x, npc.y, npc.z)
        """
        return self.world.apply_footprint(x, y, z, material=self.MAT_FOOTPRINT, size=size)

    def apply_cloak_ripple(self, x: int, y: int, z: int, radius: int = 3) -> int:
        """
        Apply Cloak of In-Conspicuity ripple effect.

        Args:
            x, y, z: Ripple center (world coords)
            radius: Ripple radius

        Returns:
            Number of voxels changed

        Example:
            >>> backend.apply_cloak_ripple(player.x, player.y, player.z, radius=3)
        """
        return self.world.apply_ripple(x, y, z, radius=radius, material=self.MAT_CLOAK_RIPPLE)

    def apply_destruction(self, x: int, y: int, z: int, radius: int = 1) -> int:
        """
        Destroy voxels (destructible props).

        Args:
            x, y, z: Destruction center (world coords)
            radius: Destruction radius

        Returns:
            Number of voxels destroyed

        Example:
            >>> backend.apply_destruction(explosion_x, explosion_y, explosion_z, radius=3)
        """
        return self.world.apply_destruction(x, y, z, radius=radius)

    # =========================================================================
    # 3. GEOMETRY → SIM (Spatial Queries)
    # =========================================================================

    def query_region(self, x_min: int, x_max: int, y_min: int, y_max: int, z_min: int, z_max: int) -> List[Tuple[int, int, int, int]]:
        """
        Query voxels in region (for Mall_OS spatial reasoning).

        Args:
            x_min, x_max, y_min, y_max, z_min, z_max: Region bounds

        Returns:
            List of (x, y, z, material) tuples

        Example:
            >>> voxels = backend.query_region(0, 100, 0, 10, 0, 100)
        """
        return self.world.query_region(x_min, x_max, y_min, y_max, z_min, z_max)

    def query_crowd_density(self, x_min: int, x_max: int, y_min: int, y_max: int, z_min: int, z_max: int) -> int:
        """
        Query crowd density (count footprints in region).

        Use case: Rust Bram sensing crowd pressure.

        Args:
            x_min, x_max, y_min, y_max, z_min, z_max: Region bounds

        Returns:
            Footprint count (proxy for crowd density)

        Example:
            >>> density = backend.query_crowd_density(0, 100, 0, 0, 0, 100)
            >>> if density > 50:
            ...     rust_bram.switch_mode(SHOWMAN)
        """
        return self.world.count_material_in_region(
            x_min, x_max, y_min, y_max, z_min, z_max,
            material=self.MAT_FOOTPRINT
        )

    def query_cloak_disturbances(self, x_min: int, x_max: int, y_min: int, y_max: int, z_min: int, z_max: int) -> int:
        """
        Query cloak ripple disturbances in region.

        Use case: Minions or Rust detecting Cloak usage.

        Args:
            x_min, x_max, y_min, y_max, z_min, z_max: Region bounds

        Returns:
            Ripple voxel count

        Example:
            >>> disturbances = backend.query_cloak_disturbances(x-10, x+10, 0, 2, z-10, z+10)
            >>> if disturbances > 0:
            ...     minion.investigate(location)
        """
        return self.world.count_material_in_region(
            x_min, x_max, y_min, y_max, z_min, z_max,
            material=self.MAT_CLOAK_RIPPLE
        )

    # =========================================================================
    # 4. RENDERER INTEGRATION
    # =========================================================================

    def get_dirty_chunks_for_render(self) -> List[Tuple[int, int, int]]:
        """
        Get dirty chunks for renderer (frame sync).

        Call this once per frame to get chunks that need re-meshing.

        Returns:
            List of chunk coordinates

        Example:
            >>> dirty = backend.get_dirty_chunks_for_render()
            >>> for chunk_coords in dirty:
            ...     mesh = backend.build_mesh(chunk_coords)
            ...     renderer.upload(chunk_coords, mesh)
        """
        return self.world.get_render_chunks()

    def build_mesh(self, chunk_coords: Tuple[int, int, int]):
        """
        Build mesh for chunk (for renderer).

        Args:
            chunk_coords: Chunk coordinates

        Returns:
            ChunkMesh or None if chunk not loaded

        Example:
            >>> mesh = backend.build_mesh((0, 0, 0))
            >>> if mesh:
            ...     renderer.upload(mesh.vertices, mesh.indices)
        """
        chunk = self.world.get_world().get_chunk(*chunk_coords)
        if chunk is None:
            return None
        return self.mesh_builder.build(chunk)

    # =========================================================================
    # 5. FRAME LIFECYCLE (Integration with Mall_OS Tick)
    # =========================================================================

    def on_frame_start(self, player_x: int, player_y: int, player_z: int):
        """
        Call at start of Mall_OS tick.

        Args:
            player_x, player_y, player_z: Player/camera focus position

        Example:
            >>> backend.on_frame_start(player.x, player.y, player.z)
        """
        self.world.on_frame_start()
        self.world.update_focus(player_x, player_y, player_z)

    def on_frame_end(self):
        """
        Call at end of Mall_OS tick.

        Example:
            >>> backend.on_frame_end()
        """
        self.world.on_frame_end()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get performance stats.

        Returns:
            Stats dict

        Example:
            >>> stats = backend.get_stats()
            >>> print(f"Chunks: {stats.current_chunk_count}")
        """
        return self.world.get_stats()


# =============================================================================
# DEMO
# =============================================================================

def demo_integration():
    """Demo Mall_OS → Spatial Backend integration."""
    print("=" * 80)
    print("MALL SPATIAL BACKEND - Mall_OS Integration Demo")
    print("=" * 80)
    print()

    # Initialize backend
    backend = MallSpatialBackend()
    print("✓ Initialized MallSpatialBackend")
    print()

    # 1. Bootstrap: Build corridor
    print("1. WORLD BOOTSTRAP")
    print("-" * 80)
    stats = backend.build_corridor(length=128, width=10, height=6)
    print(f"Built corridor: {sum(stats.values()):,} voxels")
    print(f"  - Floor: {stats['floor']}")
    print(f"  - Walls: {stats['walls']}")
    print(f"  - Ceiling: {stats['ceiling']}")
    print()

    # 2. Sim → Geometry: NPC footprints
    print("2. SIM → GEOMETRY (NPC Footprints)")
    print("-" * 80)
    for i in range(5):
        x = 10 + i * 5
        changed = backend.apply_footprint(x, 0, 5)
        print(f"  NPC{i} footprint at ({x}, 0, 5): {changed} voxels")
    print()

    # 3. Sim → Geometry: Cloak ripple
    print("3. SIM → GEOMETRY (Cloak Ripple)")
    print("-" * 80)
    changed = backend.apply_cloak_ripple(50, 0, 5, radius=3)
    print(f"  Cloak activated at (50, 0, 5): {changed} voxels rippled")
    print()

    # 4. Geometry → Sim: Crowd density query (Rust Bram)
    print("4. GEOMETRY → SIM (Rust Bram Crowd Sensing)")
    print("-" * 80)
    density = backend.query_crowd_density(0, 100, 0, 0, 0, 10)
    print(f"  Footprints in region [0-100, 0-10]: {density}")
    if density > 3:
        print(f"  → Rust Bram: SHOWMAN mode (high crowd)")
    else:
        print(f"  → Rust Bram: CALM mode (low crowd)")
    print()

    # 5. Geometry → Sim: Cloak disturbance query (Minions)
    print("5. GEOMETRY → SIM (Minion Cloak Detection)")
    print("-" * 80)
    disturbances = backend.query_cloak_disturbances(40, 60, 0, 2, 0, 10)
    print(f"  Cloak ripples detected: {disturbances}")
    if disturbances > 0:
        print(f"  → Minion: Investigate area around (50, 0, 5)")
    print()

    # 6. Renderer sync
    print("6. RENDERER SYNC")
    print("-" * 80)
    dirty = backend.get_dirty_chunks_for_render()
    print(f"  Dirty chunks: {len(dirty)} need re-mesh")
    for chunk_coords in dirty[:3]:  # Show first 3
        print(f"    - Chunk {chunk_coords}")
    print()

    # Stats
    print("=" * 80)
    print("INTEGRATION COMPLETE")
    print("=" * 80)
    stats = backend.get_stats()
    print(f"Final state:")
    print(f"  - Chunks loaded: {stats.current_chunk_count}")
    print(f"  - Total voxels: {stats.current_voxel_count:,}")
    print(f"  - Voxels changed: {stats.total_voxels_changed:,}")
    print()
    print("✓ Mall_OS can now:")
    print("  - Build zones (corridors, food courts, etc.)")
    print("  - Apply voxel events (footprints, ripples, destruction)")
    print("  - Query spatial data (crowd density, cloak detection)")
    print("  - Sync with renderer (dirty chunks)")
    print("=" * 80)


if __name__ == "__main__":
    demo_integration()
