#!/usr/bin/env python3
"""
ChunkMeshBuilder - Render Bridge

Thin adapter between voxel chunks and any renderer (Voxeloo/WASM/Godot/WebGPU).

Responsibilities:
  - Convert sparse voxel chunks → renderable geometry
  - Support multiple meshing strategies (naive cubes, greedy meshing)
  - Stay renderer-agnostic (outputs generic mesh data)
  - No opinions about materials, textures, lighting

Architecture:
  VoxelWorldManager
         ↓
  get_dirty_chunks() → ChunkMeshBuilder.build(chunk) → Renderer.upload()
         ↓
  ChunkedVoxelWorld

This is the "plug any renderer under me" layer.
"""

from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import sys

# Import voxel system
sys.path.insert(0, '.')
from voxel_chunk import VoxelChunk
from voxel_encoding import CHUNK_SIZE


# =============================================================================
# MESH DATA STRUCTURES
# =============================================================================

@dataclass
class Vertex:
    """Single vertex in 3D space."""
    x: float
    y: float
    z: float

    def to_tuple(self) -> Tuple[float, float, float]:
        """Convert to tuple for renderer."""
        return (self.x, self.y, self.z)


@dataclass
class Quad:
    """Single quad face (4 vertices)."""
    v0: Vertex
    v1: Vertex
    v2: Vertex
    v3: Vertex
    material: int
    normal: Tuple[int, int, int]  # Face normal (0,1,0) = up, etc.

    def to_triangles(self) -> Tuple[List[Vertex], List[int]]:
        """
        Convert quad to 2 triangles.

        Returns:
            (vertices, indices) for triangle rendering
        """
        vertices = [self.v0, self.v1, self.v2, self.v3]
        indices = [0, 1, 2, 0, 2, 3]  # Two triangles
        return (vertices, indices)


@dataclass
class ChunkMesh:
    """
    Renderable mesh data for a chunk.

    This is renderer-agnostic - can be consumed by any renderer.
    """
    chunk_coords: Tuple[int, int, int]
    vertices: List[Tuple[float, float, float]]
    indices: List[int]
    materials: List[int]  # Per-face material IDs
    normals: List[Tuple[int, int, int]]  # Per-face normals

    def vertex_count(self) -> int:
        """Get vertex count."""
        return len(self.vertices)

    def triangle_count(self) -> int:
        """Get triangle count."""
        return len(self.indices) // 3

    def is_empty(self) -> bool:
        """Check if mesh has no geometry."""
        return len(self.vertices) == 0


# =============================================================================
# MESHING STRATEGY
# =============================================================================

class MeshingStrategy(Enum):
    """Meshing algorithm choices."""
    NAIVE_CUBES = "naive"           # One cube per voxel (simple, inefficient)
    GREEDY = "greedy"               # Greedy meshing (efficient, more complex)
    MARCHING_CUBES = "marching"     # Smooth surfaces (future)


# =============================================================================
# CHUNK MESH BUILDER
# =============================================================================

class ChunkMeshBuilder:
    """
    Convert voxel chunks to renderable mesh data.

    This is the bridge between Mall_OS voxels and any renderer.

    Example:
        >>> builder = ChunkMeshBuilder(strategy=MeshingStrategy.NAIVE_CUBES)
        >>> mesh = builder.build(chunk)
        >>> renderer.upload(mesh.chunk_coords, mesh.vertices, mesh.indices)
    """

    def __init__(self, strategy: MeshingStrategy = MeshingStrategy.NAIVE_CUBES):
        """
        Initialize mesh builder.

        Args:
            strategy: Meshing algorithm to use
        """
        self.strategy = strategy

    def build(self, chunk: VoxelChunk) -> ChunkMesh:
        """
        Build mesh for chunk.

        Args:
            chunk: VoxelChunk to mesh

        Returns:
            ChunkMesh ready for renderer
        """
        if self.strategy == MeshingStrategy.NAIVE_CUBES:
            return self._build_naive_cubes(chunk)
        elif self.strategy == MeshingStrategy.GREEDY:
            return self._build_greedy(chunk)
        else:
            raise ValueError(f"Unsupported meshing strategy: {self.strategy}")

    # =========================================================================
    # NAIVE CUBES MESHING (Simple, One Cube Per Voxel)
    # =========================================================================

    def _build_naive_cubes(self, chunk: VoxelChunk) -> ChunkMesh:
        """
        Build mesh using naive cube-per-voxel approach.

        Only renders exposed faces (faces adjacent to air).

        Args:
            chunk: VoxelChunk to mesh

        Returns:
            ChunkMesh with cube geometry
        """
        vertices = []
        indices = []
        materials = []
        normals = []

        # Face definitions (normal, vertex offsets)
        # Each face is defined by its normal and 4 vertex positions
        FACES = [
            # (nx, ny, nz), [(x0,y0,z0), (x1,y1,z1), (x2,y2,z2), (x3,y3,z3)]
            ((0, 1, 0), [(0,1,0), (1,1,0), (1,1,1), (0,1,1)]),  # Top (+Y)
            ((0,-1, 0), [(0,0,0), (0,0,1), (1,0,1), (1,0,0)]),  # Bottom (-Y)
            ((1, 0, 0), [(1,0,0), (1,0,1), (1,1,1), (1,1,0)]),  # Right (+X)
            ((-1,0, 0), [(0,0,0), (0,1,0), (0,1,1), (0,0,1)]),  # Left (-X)
            ((0, 0, 1), [(0,0,1), (0,1,1), (1,1,1), (1,0,1)]),  # Front (+Z)
            ((0, 0,-1), [(0,0,0), (1,0,0), (1,1,0), (0,1,0)]),  # Back (-Z)
        ]

        vertex_offset = 0

        # Iterate all voxels in chunk
        for local_x, local_y, local_z, material in chunk.iter_voxels():
            if material == 0:  # Skip air
                continue

            # Check each face for exposure to air
            for (nx, ny, nz), face_verts in FACES:
                # Check neighbor in this direction
                neighbor_x = local_x + nx
                neighbor_y = local_y + ny
                neighbor_z = local_z + nz

                # Is neighbor air or out of bounds?
                is_exposed = False

                if (neighbor_x < 0 or neighbor_x >= CHUNK_SIZE or
                    neighbor_y < 0 or neighbor_y >= CHUNK_SIZE or
                    neighbor_z < 0 or neighbor_z >= CHUNK_SIZE):
                    is_exposed = True  # Chunk boundary
                else:
                    neighbor_material = chunk.get_voxel(neighbor_x, neighbor_y, neighbor_z)
                    is_exposed = (neighbor_material == 0)

                if is_exposed:
                    # Add this face
                    for (dx, dy, dz) in face_verts:
                        vx = local_x + dx
                        vy = local_y + dy
                        vz = local_z + dz
                        vertices.append((float(vx), float(vy), float(vz)))

                    # Add indices for 2 triangles (quad)
                    indices.extend([
                        vertex_offset + 0, vertex_offset + 1, vertex_offset + 2,
                        vertex_offset + 0, vertex_offset + 2, vertex_offset + 3,
                    ])

                    # Material and normal for both triangles
                    materials.extend([material, material])
                    normals.extend([(nx, ny, nz), (nx, ny, nz)])

                    vertex_offset += 4

        return ChunkMesh(
            chunk_coords=chunk.position,
            vertices=vertices,
            indices=indices,
            materials=materials,
            normals=normals,
        )

    # =========================================================================
    # GREEDY MESHING (Future Optimization)
    # =========================================================================

    def _build_greedy(self, chunk: VoxelChunk) -> ChunkMesh:
        """
        Build mesh using greedy meshing algorithm.

        Merges adjacent faces of same material into larger quads.
        More efficient but more complex.

        Args:
            chunk: VoxelChunk to mesh

        Returns:
            ChunkMesh with optimized geometry

        Note:
            Not yet implemented - falls back to naive cubes.
        """
        # TODO: Implement greedy meshing
        # For now, fall back to naive
        return self._build_naive_cubes(chunk)


# =============================================================================
# BATCH MESH BUILDER
# =============================================================================

class BatchMeshBuilder:
    """
    Build meshes for multiple chunks efficiently.

    Useful for initial world loading or large updates.
    """

    def __init__(self, strategy: MeshingStrategy = MeshingStrategy.NAIVE_CUBES):
        """
        Initialize batch builder.

        Args:
            strategy: Meshing strategy to use
        """
        self.builder = ChunkMeshBuilder(strategy)

    def build_batch(self, chunks: List[VoxelChunk]) -> List[ChunkMesh]:
        """
        Build meshes for multiple chunks.

        Args:
            chunks: List of VoxelChunks to mesh

        Returns:
            List of ChunkMesh instances
        """
        meshes = []
        for chunk in chunks:
            mesh = self.builder.build(chunk)
            if not mesh.is_empty():
                meshes.append(mesh)
        return meshes


# =============================================================================
# DEMO
# =============================================================================

def demo_mesh_builder():
    """Demo the mesh builder."""
    from voxel_chunk import VoxelChunk

    print("=" * 80)
    print("CHUNK MESH BUILDER - Render Bridge Demo")
    print("=" * 80)
    print()

    # Create test chunk with some voxels
    chunk = VoxelChunk(position=(0, 0, 0))

    # Build a 3x3x3 cube
    print("Building 3x3x3 cube...")
    for x in range(3):
        for y in range(3):
            for z in range(3):
                chunk.set_voxel(x, y, z, material=1)

    print(f"  Chunk has {chunk.voxel_count()} voxels")
    print()

    # Mesh it
    builder = ChunkMeshBuilder(strategy=MeshingStrategy.NAIVE_CUBES)
    mesh = builder.build(chunk)

    print(f"Mesh stats:")
    print(f"  Vertices: {mesh.vertex_count()}")
    print(f"  Triangles: {mesh.triangle_count()}")
    print(f"  Materials: {len(set(mesh.materials))} unique")
    print()

    # Show first few vertices
    print("First 12 vertices (2 quads):")
    for i, v in enumerate(mesh.vertices[:12]):
        print(f"  v{i}: {v}")
    print()

    # Hollow it out (remove center)
    print("Hollowing out center voxel...")
    chunk.set_voxel(1, 1, 1, material=0)

    # Re-mesh
    mesh2 = builder.build(chunk)
    print(f"New mesh stats:")
    print(f"  Vertices: {mesh2.vertex_count()} (was {mesh.vertex_count()})")
    print(f"  Triangles: {mesh2.triangle_count()} (was {mesh.triangle_count()})")
    print()

    print("=" * 80)
    print("✓ Mesh builder ready for renderer integration!")
    print("  - Naive cubes: ✓ Working")
    print("  - Greedy meshing: TODO (future optimization)")
    print("  - Renderer-agnostic output")
    print("=" * 80)


if __name__ == "__main__":
    demo_mesh_builder()
