#!/usr/bin/env python3
"""
VoxelWorldManager - High-Level Orchestration Layer

The "snap-together" layer between Mall_OS and the voxel engine.

Responsibilities:
  1. Route all Mall_OS → voxel requests
  2. Coordinate chunk lifetime (load/unload policies)
  3. Expose clean API for Synthactors, WATTITUDE, physics
  4. Track performance counters
  5. Sync with renderer pre-frame

Architecture:
  Mall_OS / Synthactors / WATTITUDE
         ↓
  VoxelWorldManager (this layer - ORCHESTRATES)
         ↓
  ChunkedVoxelWorld (7 responsibilities - EXECUTES)
         ↓
  VoxelChunk (sparse storage - STORES)

Principles:
  - AWARE but NOT OPINIONATED (no NPC/quest logic)
  - Policy-driven (configurable strategies)
  - Event-ready (DeltaBus hooks)
  - Observable (stats, metrics, debugging)
"""

from typing import Optional, Dict, List, Tuple, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
import time

# Import voxel system
import sys
sys.path.insert(0, '.')
from voxel_world import ChunkedVoxelWorld
from voxel_encoding import CHUNK_SIZE


# =============================================================================
# CONFIGURATION
# =============================================================================

class ChunkLoadPolicy(Enum):
    """Chunk loading strategies."""
    MANUAL = "manual"               # No auto-loading
    RADIUS = "radius"               # Load within radius of focus
    ON_DEMAND = "on_demand"         # Load only when accessed
    AGGRESSIVE = "aggressive"       # Pre-load neighboring chunks


@dataclass
class VoxelWorldConfig:
    """Configuration for VoxelWorldManager."""

    # Chunk loading
    load_policy: ChunkLoadPolicy = ChunkLoadPolicy.RADIUS
    load_radius: int = 8            # Chunks to keep loaded (for RADIUS policy)
    unload_distance: int = 12       # Unload beyond this distance

    # Performance
    max_chunks_per_frame: int = 4   # Max chunks to load/unload per frame
    enable_stats: bool = True       # Track performance stats

    # Rendering
    auto_clear_dirty: bool = True   # Auto-clear dirty chunks after get_render_chunks()

    # Debug
    verbose: bool = False           # Log operations


@dataclass
class PerformanceStats:
    """Performance tracking for voxel world."""

    # Counters
    total_frames: int = 0
    total_voxels_changed: int = 0
    total_chunks_loaded: int = 0
    total_chunks_unloaded: int = 0

    # Timing
    total_update_time_ms: float = 0.0
    total_render_sync_time_ms: float = 0.0

    # Current state
    current_chunk_count: int = 0
    current_voxel_count: int = 0
    current_dirty_count: int = 0

    def reset(self):
        """Reset all stats."""
        self.__init__()


# =============================================================================
# VOXEL WORLD MANAGER
# =============================================================================

class VoxelWorldManager:
    """
    High-level orchestration layer for voxel world.

    This is the clean API that Mall_OS, Synthactors, and WATTITUDE
    will interact with. It handles policies, routing, and coordination.

    Example:
        >>> config = VoxelWorldConfig(load_policy=ChunkLoadPolicy.RADIUS, load_radius=8)
        >>> manager = VoxelWorldManager(config)
        >>>
        >>> # Frame loop
        >>> manager.on_frame_start()
        >>> manager.update_focus(player_x, player_y, player_z)
        >>>
        >>> # Handle events
        >>> manager.apply_footprint(npc_x, npc_y, npc_z, material_id=4)
        >>>
        >>> # Sync with renderer
        >>> dirty_chunks = manager.get_render_chunks()
        >>> for chunk_coords in dirty_chunks:
        ...     renderer.remesh_chunk(chunk_coords)
        >>>
        >>> manager.on_frame_end()
    """

    def __init__(self, config: Optional[VoxelWorldConfig] = None):
        """
        Initialize manager.

        Args:
            config: Configuration (uses defaults if not provided)
        """
        self.config = config or VoxelWorldConfig()
        self.world = ChunkedVoxelWorld()
        self.stats = PerformanceStats()

        # Focus point for chunk loading (world coords)
        self.focus_x: Optional[int] = None
        self.focus_y: Optional[int] = None
        self.focus_z: Optional[int] = None

        # Event hooks (can be set by Mall_OS)
        self.on_chunk_loaded: Optional[Callable[[Tuple[int, int, int]], None]] = None
        self.on_chunk_unloaded: Optional[Callable[[Tuple[int, int, int]], None]] = None
        self.on_voxels_changed: Optional[Callable[[int], None]] = None  # Count of voxels changed

        if self.config.verbose:
            print(f"VoxelWorldManager initialized: {self.config}")

    # =========================================================================
    # FRAME LIFECYCLE
    # =========================================================================

    def on_frame_start(self):
        """
        Call at start of frame (before any voxel operations).

        Handles:
        - Chunk loading based on focus point
        - Performance counter reset
        """
        self.stats.total_frames += 1
        self._update_time_start = time.perf_counter()

        # Apply chunk loading policy
        if self.config.load_policy == ChunkLoadPolicy.RADIUS and self.focus_x is not None:
            self._apply_radius_loading()

    def on_frame_end(self):
        """
        Call at end of frame (after all voxel operations, before rendering).

        Handles:
        - Performance timing
        - Stats update
        """
        # Update timing
        elapsed = (time.perf_counter() - self._update_time_start) * 1000  # ms
        self.stats.total_update_time_ms += elapsed

        # Update current state
        self.stats.current_chunk_count = self.world.chunk_count()
        self.stats.current_voxel_count = self.world.voxel_count()
        self.stats.current_dirty_count = len(self.world.get_dirty_chunks())

    # =========================================================================
    # FOCUS & CHUNK MANAGEMENT
    # =========================================================================

    def update_focus(self, world_x: int, world_y: int, world_z: int):
        """
        Update focus point for chunk loading.

        This is typically the player position, camera center, or
        authoritative simulation center.

        Args:
            world_x, world_y, world_z: Focus point in world coords

        Example:
            >>> manager.update_focus(player.x, player.y, player.z)
        """
        self.focus_x = world_x
        self.focus_y = world_y
        self.focus_z = world_z

        # Unload far chunks
        if self.config.unload_distance > 0:
            unloaded = self.world.unload_far_chunks(
                world_x, world_y, world_z,
                max_distance=self.config.unload_distance
            )

            if unloaded > 0:
                self.stats.total_chunks_unloaded += unloaded
                if self.config.verbose:
                    print(f"  Unloaded {unloaded} far chunks (distance > {self.config.unload_distance})")

                if self.on_chunk_unloaded:
                    # Note: We don't know which specific chunks were unloaded from unload_far_chunks
                    # This is a batch notification
                    pass

    def _apply_radius_loading(self):
        """Apply RADIUS loading policy (preload chunks within radius)."""
        if self.focus_x is None:
            return

        # This is a simplified version - could be optimized to only check
        # chunks at the edge of the radius rather than full iteration
        # For now, we rely on the world's lazy loading on access
        pass  # ChunkedVoxelWorld already does lazy loading on set_voxel

    # =========================================================================
    # VOXEL OPERATIONS (High-Level API)
    # =========================================================================

    def set_voxel(self, world_x: int, world_y: int, world_z: int, material: int):
        """
        Set single voxel (direct pass-through).

        Args:
            world_x, world_y, world_z: World coordinates
            material: Material ID
        """
        self.world.set_voxel(world_x, world_y, world_z, material)
        self.stats.total_voxels_changed += 1

        if self.on_voxels_changed:
            self.on_voxels_changed(1)

    def get_voxel(self, world_x: int, world_y: int, world_z: int) -> int:
        """
        Get single voxel (direct pass-through).

        Args:
            world_x, world_y, world_z: World coordinates

        Returns:
            Material ID (0 = air)
        """
        return self.world.get_voxel(world_x, world_y, world_z)

    def apply_footprint(self, center_x: int, center_y: int, center_z: int, material: int, size: int = 1) -> int:
        """
        Apply NPC footprint (high-level operation).

        Args:
            center_x, center_y, center_z: Center position
            material: Footprint material ID
            size: Radius of footprint (1 = 2x2, 2 = 4x4, etc.)

        Returns:
            Number of voxels changed

        Example:
            >>> manager.apply_footprint(npc.x, npc.y, npc.z, material_id=4)
        """
        changed = self.world.apply_region_change(
            center_x - size, center_x + size,
            center_y, center_y,  # Only affect floor level
            center_z - size, center_z + size,
            material=material
        )

        self.stats.total_voxels_changed += changed

        if self.on_voxels_changed:
            self.on_voxels_changed(changed)

        return changed

    def apply_ripple(self, center_x: int, center_y: int, center_z: int, radius: int, material: int) -> int:
        """
        Apply Cloak of In-Conspicuity ripple effect.

        Args:
            center_x, center_y, center_z: Ripple center
            radius: Ripple radius
            material: Ripple material ID

        Returns:
            Number of voxels changed

        Example:
            >>> manager.apply_ripple(player.x, player.y, player.z, radius=3, material=5)
        """
        # Simple box ripple (could be enhanced to ring/sphere)
        changed = self.world.apply_region_change(
            center_x - radius, center_x + radius,
            center_y - 1, center_y + 1,
            center_z - radius, center_z + radius,
            material=material
        )

        self.stats.total_voxels_changed += changed

        if self.on_voxels_changed:
            self.on_voxels_changed(changed)

        return changed

    def apply_destruction(self, x: int, y: int, z: int, radius: int = 1) -> int:
        """
        Destroy voxels (set to air) in region.

        Args:
            x, y, z: Destruction center
            radius: Destruction radius

        Returns:
            Number of voxels destroyed

        Example:
            >>> manager.apply_destruction(explosion_x, explosion_y, explosion_z, radius=3)
        """
        changed = self.world.apply_region_change(
            x - radius, x + radius,
            y - radius, y + radius,
            z - radius, z + radius,
            material=0  # Air
        )

        self.stats.total_voxels_changed += changed

        if self.on_voxels_changed:
            self.on_voxels_changed(changed)

        return changed

    # =========================================================================
    # DELTABUS INTEGRATION
    # =========================================================================

    def handle_deltabus_event(self, event: Dict[str, Any]) -> int:
        """
        Route DeltaBus event to voxel world.

        Event format:
            {
                'kind': 'VOXEL_CHANGE' | 'FOOTSTEP' | 'CLOAK_RIPPLE' | 'DESTRUCTION',
                'payload': { ... }
            }

        Args:
            event: DeltaBus event dict

        Returns:
            Number of voxels changed

        Example:
            >>> event = {
            ...     'kind': 'FOOTSTEP',
            ...     'payload': {'x': 10, 'y': 0, 'z': 5, 'material': 4}
            ... }
            >>> manager.handle_deltabus_event(event)
        """
        kind = event.get('kind')
        payload = event.get('payload', {})

        if kind == 'VOXEL_CHANGE':
            # Direct voxel changes: {(x,y,z): material}
            changes = payload.get('changes', {})
            return self.world.apply_voxel_delta(changes)

        elif kind == 'FOOTSTEP':
            # Footprint event
            x = payload.get('x')
            y = payload.get('y')
            z = payload.get('z')
            material = payload.get('material', 4)
            size = payload.get('size', 1)
            return self.apply_footprint(x, y, z, material, size)

        elif kind == 'CLOAK_RIPPLE':
            # Cloak ripple event
            x = payload.get('x')
            y = payload.get('y')
            z = payload.get('z')
            radius = payload.get('radius', 2)
            material = payload.get('material', 5)
            return self.apply_ripple(x, y, z, radius, material)

        elif kind == 'DESTRUCTION':
            # Destruction event
            x = payload.get('x')
            y = payload.get('y')
            z = payload.get('z')
            radius = payload.get('radius', 1)
            return self.apply_destruction(x, y, z, radius)

        else:
            if self.config.verbose:
                print(f"  Unknown event kind: {kind}")
            return 0

    # =========================================================================
    # RENDERER INTEGRATION
    # =========================================================================

    def get_render_chunks(self) -> List[Tuple[int, int, int]]:
        """
        Get list of dirty chunks for renderer.

        Call this before rendering to get chunks that need re-meshing.
        Automatically clears dirty chunks if auto_clear_dirty is True.

        Returns:
            List of chunk coordinates that need re-meshing

        Example:
            >>> dirty = manager.get_render_chunks()
            >>> for chunk_coords in dirty:
            ...     renderer.remesh_chunk(chunk_coords)
        """
        sync_start = time.perf_counter()

        dirty_chunks = self.world.get_dirty_chunks()

        if self.config.auto_clear_dirty:
            self.world.clear_dirty_chunks()

        # Update timing
        elapsed = (time.perf_counter() - sync_start) * 1000  # ms
        self.stats.total_render_sync_time_ms += elapsed

        return dirty_chunks

    def build_mesh_for_chunk(self, chunk_coords: Tuple[int, int, int]) -> Optional[Any]:
        """
        Placeholder for mesh building.

        This would be implemented by the renderer (Voxeloo/WASM/Godot).
        The manager just provides the hook.

        Args:
            chunk_coords: Chunk coordinates to mesh

        Returns:
            Mesh data (renderer-specific)
        """
        # This is where you'd call into the actual meshing system
        # For now, just a placeholder
        chunk = self.world.get_chunk(*chunk_coords)
        if chunk is None:
            return None

        # Renderer would convert chunk voxels to triangles/instances
        return {
            'chunk_coords': chunk_coords,
            'voxel_count': chunk.voxel_count(),
            # ... mesh data would go here
        }

    # =========================================================================
    # QUERIES
    # =========================================================================

    def query_region(self, x_min: int, x_max: int, y_min: int, y_max: int, z_min: int, z_max: int) -> List[Tuple[int, int, int, int]]:
        """
        Query voxels in region (for Mall_OS spatial reasoning).

        Args:
            x_min, x_max, y_min, y_max, z_min, z_max: Region bounds

        Returns:
            List of (x, y, z, material) tuples

        Example:
            >>> voxels = manager.query_region(0, 100, 0, 10, 0, 100)
            >>> footprint_count = sum(1 for _, _, _, mat in voxels if mat == FOOTPRINT_MAT)
        """
        return list(self.world.iter_region(x_min, x_max, y_min, y_max, z_min, z_max))

    def count_material_in_region(self, x_min: int, x_max: int, y_min: int, y_max: int, z_min: int, z_max: int, material: int) -> int:
        """
        Count voxels of specific material in region.

        Useful for:
        - Crowd density (count footprints)
        - Damage assessment (count destroyed voxels)
        - Resource tracking

        Args:
            x_min, x_max, y_min, y_max, z_min, z_max: Region bounds
            material: Material ID to count

        Returns:
            Count of matching voxels

        Example:
            >>> footprints = manager.count_material_in_region(0, 100, 0, 0, 0, 100, material=4)
        """
        voxels = self.query_region(x_min, x_max, y_min, y_max, z_min, z_max)
        return sum(1 for _, _, _, mat in voxels if mat == material)

    # =========================================================================
    # STATS & DEBUG
    # =========================================================================

    def get_stats(self) -> PerformanceStats:
        """
        Get performance stats.

        Returns:
            PerformanceStats snapshot
        """
        return self.stats

    def print_stats(self):
        """Print performance stats summary."""
        print("=" * 80)
        print("VOXEL WORLD MANAGER - Performance Stats")
        print("=" * 80)
        print(f"Frames: {self.stats.total_frames}")
        print(f"Chunks: {self.stats.current_chunk_count} active "
              f"(+{self.stats.total_chunks_loaded}/-{self.stats.total_chunks_unloaded} total)")
        print(f"Voxels: {self.stats.current_voxel_count:,} active, "
              f"{self.stats.total_voxels_changed:,} changed total")
        print(f"Dirty: {self.stats.current_dirty_count} chunks")

        if self.stats.total_frames > 0:
            avg_update = self.stats.total_update_time_ms / self.stats.total_frames
            avg_render = self.stats.total_render_sync_time_ms / self.stats.total_frames
            print(f"Timing: {avg_update:.2f}ms avg update, {avg_render:.2f}ms avg render sync")

        print("=" * 80)

    def reset_stats(self):
        """Reset performance stats."""
        self.stats.reset()

    # =========================================================================
    # DIRECT WORLD ACCESS (for advanced use)
    # =========================================================================

    def get_world(self) -> ChunkedVoxelWorld:
        """
        Get direct access to underlying ChunkedVoxelWorld.

        Use this for advanced operations not covered by the manager API.

        Returns:
            ChunkedVoxelWorld instance
        """
        return self.world


# =============================================================================
# DEMO
# =============================================================================

def demo_manager():
    """Demo the manager orchestration."""
    print("=" * 80)
    print("VOXEL WORLD MANAGER - Orchestration Demo")
    print("=" * 80)
    print()

    # Configure manager
    config = VoxelWorldConfig(
        load_policy=ChunkLoadPolicy.RADIUS,
        load_radius=8,
        unload_distance=12,
        verbose=True,
    )

    manager = VoxelWorldManager(config)
    print()

    # Simulate 10 frames
    for frame in range(10):
        manager.on_frame_start()

        # Update focus (simulated player movement)
        player_x = frame * 10
        player_y = 0
        player_z = 0
        manager.update_focus(player_x, player_y, player_z)

        # Simulate some voxel operations
        if frame % 2 == 0:
            manager.apply_footprint(player_x, player_y, player_z, material=4)

        if frame == 5:
            manager.apply_ripple(player_x, player_y, player_z, radius=3, material=5)

        # Get dirty chunks for rendering
        dirty = manager.get_render_chunks()
        if dirty:
            print(f"  Frame {frame}: {len(dirty)} chunks need re-mesh")

        manager.on_frame_end()

    print()
    manager.print_stats()


if __name__ == "__main__":
    demo_manager()
