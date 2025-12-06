# Biomes Game - Reference Math & Architecture

Reference files from [Biomes Game](https://github.com/ill-inc/biomes-game) for implementing voxel optimizations in v8-nextgen.

**Source:** https://github.com/ill-inc/biomes-game
**Purpose:** Study algorithms and data structures for Python implementation
**License:** MIT (see Biomes repository)

---

## Directory Structure

### `voxel_math/` - Core Voxel Data Structures

**Key files:**
- `tensors.hpp` - **32³ chunk system with RLE compression**
  - `kChunkDim = 32` - Standard chunk size
  - `encode_tensor_pos()` - Bit-packed position encoding (10 bits per axis)
  - `decode_tensor_pos()` - Decoding back to 3D coordinates
  - `Chunk<T>` - RLE-compressed array storage

- `sparse.hpp` - **Sparse tensor builders**
  - `SparseArrayBuilder` - Build RLE arrays efficiently
  - `SparseChunkBuilder` - Build sparse chunks from scattered voxels
  - `SparseTensorBuilder` - Build multi-chunk sparse tensors

- `arrays.hpp` - **RLE array implementation**
  - Run-length encoding for repeated values
  - Memory-efficient storage

- `succinct.hpp` - **Succinct data structures**
  - Compact representations
  - Dictionary encoding

- `buffers.hpp` - **Buffer management**
  - Memory pooling
  - Serialization

**What to model:**
1. ✅ Chunk-based spatial partitioning (32x32x32)
2. ✅ Bit-packed position encoding (saves memory)
3. ✅ RLE compression for sparse data
4. ✅ Builder pattern for efficient construction

**Python equivalent targets:**
```python
# v8-nextgen/src/rendering/voxel_chunk.py
class VoxelChunk:
    CHUNK_SIZE = 32

    @staticmethod
    def encode_pos(x: int, y: int, z: int) -> int:
        """10 bits per axis encoding."""
        return (y & 0x3ff) << 20 | (z & 0x3ff) << 10 | (x & 0x3ff)

    # Sparse dict storage instead of RLE (simpler for Python)
    data: Dict[int, int]  # {encoded_pos: material_id}
```

---

### `rendering/` - Multi-Pass Rendering Pipeline

**Key files:**
- `composer.ts` - **Render pass orchestration**
  - `RENDER_PASSES` - Ordered list of rendering stages
  - `POSTPROCESS_PASSES` - Post-processing effects
  - `RenderPassComposer` - Manages pass execution

- `pass.ts` - **Base render pass class**
  - Input/output management
  - Buffer lifecycle
  - Pass dependencies
  - Enable/disable logic

- `graphics_settings.ts` - **Dynamic quality settings**
  - `GraphicsQuality` - Low/Medium/High/Ultra presets
  - `RenderScale` - Resolution scaling (0.5x - 1.25x)
  - `DrawDistance` - Culling distance
  - `PostprocessAA` - Anti-aliasing settings
  - Settings invalidation/hot-reload

- `scene_pass.ts` - **Example scene render pass**
  - Opaque geometry rendering
  - Depth buffering

**What to model:**
1. ✅ Pass-based rendering architecture
2. ✅ Input/output channel system
3. ✅ Dynamic quality presets
4. ✅ Settings hot-reloading

**Python equivalent targets:**
```python
# v8-nextgen/src/rendering/render_pass.py
class RenderPass:
    inputs: Dict[str, Surface]
    outputs: Dict[str, Surface]

# v8-nextgen/src/rendering/composer.py
class RenderPassComposer:
    passes: List[RenderPass]

# v8-nextgen/src/rendering/graphics_settings.py
@dataclass
class GraphicsSettings:
    render_scale: float
    quality: Literal["low", "medium", "high", "ultra"]
```

---

### `blocks/` - Block/Voxel Type System

**Key files:**
- `blocks.hpp` - **Block variant system**
  - `BlockId` - 32-bit block identifier
  - `BlockSampleCriteria` - Variant selection (dye, moisture, checkerboard)
  - `Samples` - 8 texture samples per variant
  - `Index` - Block type registry

- `shapes.hpp` - **Voxel shape primitives**
  - Box shapes
  - Cylinder shapes
  - Composition operations

- `groups.hpp` - **Block grouping/clustering**
  - Spatial queries
  - Neighbor detection

**What to model:**
1. ✅ Material ID system
2. ✅ Variant/sample selection
3. ⚠️ Skip: Complex variant system (overkill for mall)
4. ✅ Basic shape primitives

**Python equivalent targets:**
```python
# v8-nextgen/src/rendering/materials.py
class MaterialRegistry:
    materials: Dict[int, Material]

@dataclass
class Material:
    id: int
    name: str
    color: Tuple[int, int, int]
    # Simple materials, no variants for v8
```

---

## Key Algorithms to Port

### 1. Position Encoding (CRITICAL)
```cpp
// C++ - biomes (tensors.hpp:20-32)
inline auto encode_tensor_pos(TensorPos pos) {
  auto k_0 = static_cast<ArrayPos>((pos.y & 0x1f) << 10);
  auto k_1 = static_cast<ArrayPos>((pos.z & 0x1f) << 5);
  auto k_2 = static_cast<ArrayPos>((pos.x & 0x1f));
  return static_cast<ArrayPos>(k_0 | k_1 | k_2);
}
```
**→ Python implementation:**
```python
def encode_tensor_pos(x: int, y: int, z: int) -> int:
    """Encode 3D position into 15-bit integer (5 bits each)."""
    k_0 = (y & 0x1f) << 10  # Y: bits 10-14
    k_1 = (z & 0x1f) << 5   # Z: bits 5-9
    k_2 = (x & 0x1f)        # X: bits 0-4
    return k_0 | k_1 | k_2
```

### 2. Sparse Chunk Builder (CRITICAL)
```cpp
// C++ - biomes (sparse.hpp:44-73)
class SparseChunkBuilder {
  void set(TensorPos pos, T val) {
    vals_.push_back({encode_tensor_pos(pos), val});
  }

  auto build() {
    std::stable_sort(vals_.begin(), vals_.end());
    // ... RLE compression
  }
};
```
**→ Python implementation:**
```python
class VoxelChunk:
    def __init__(self):
        self.data: Dict[int, int] = {}  # Sparse dict

    def set_voxel(self, x: int, y: int, z: int, material: int):
        encoded = encode_tensor_pos(x, y, z)
        if material == 0:  # Air
            self.data.pop(encoded, None)
        else:
            self.data[encoded] = material
```

### 3. Render Pass System (IMPORTANT)
```typescript
// TypeScript - biomes (pass.ts:8-30)
export class RenderPass {
  inputs: Map<RenderPassChannel, [RenderPass, RenderPassChannel]>;
  outputs: Map<RenderPassChannel, THREE.Texture>;

  setInput(name, pass, outputChannel) {
    this.inputs.set(name, [pass, outputChannel]);
  }
}
```
**→ Python implementation:**
```python
class RenderPass:
    def __init__(self, name: str):
        self.name = name
        self.inputs: Dict[str, pygame.Surface] = {}
        self.outputs: Dict[str, pygame.Surface] = {}

    @abstractmethod
    def render(self, screen: pygame.Surface, dt: float):
        pass
```

### 4. Graphics Settings (IMPORTANT)
```typescript
// TypeScript - biomes (graphics_settings.ts:55-75)
export type GraphicsQuality = "low" | "medium" | "high" | "ultra" | "auto";
export type RenderScale = 0.5 | 0.75 | 1.0 | 1.25;
```
**→ Python implementation:**
```python
@dataclass
class GraphicsSettings:
    quality: Literal["low", "medium", "high", "ultra"] = "high"
    render_scale: float = 1.0
    chunk_draw_distance: int = 8
    max_entities: int = 100
```

---

## Implementation Priority

### Phase 1: Voxel Data Structures ⭐⭐⭐
**Files to study:** `voxel_math/tensors.hpp`, `voxel_math/sparse.hpp`

**Target implementations:**
1. `v8-nextgen/src/rendering/voxel_chunk.py` - Chunk class with sparse storage
2. `v8-nextgen/src/rendering/voxel_world.py` - Multi-chunk world manager
3. `v8-nextgen/src/rendering/voxel_encoding.py` - Position encoding utilities

**Expected improvement:** 80-90% memory reduction

---

### Phase 2: Rendering Pipeline ⭐⭐
**Files to study:** `rendering/pass.ts`, `rendering/composer.ts`

**Target implementations:**
1. `v8-nextgen/src/rendering/render_pass.py` - Base pass class
2. `v8-nextgen/src/rendering/composer.py` - Pass orchestration
3. `v8-nextgen/src/rendering/passes/` - Individual pass implementations

**Expected improvement:** Modular effects, easier to add bloom/glitch/scanlines

---

### Phase 3: Graphics Settings ⭐
**Files to study:** `rendering/graphics_settings.ts`

**Target implementations:**
1. `v8-nextgen/src/rendering/graphics_settings.py` - Settings class
2. `v8-nextgen/src/rendering/resource_manager.py` - Settings hot-reload

**Expected improvement:** Performance tuning, dynamic quality

---

## Notes on C++ → Python Translation

### What to Keep:
- ✅ **Chunking concept** (32³ blocks)
- ✅ **Bit-packed encoding** (memory efficient)
- ✅ **Sparse storage** (only store non-air voxels)
- ✅ **Pass-based rendering** (modular effects)
- ✅ **Quality presets** (low/medium/high/ultra)

### What to Simplify:
- ⚠️ **RLE compression** → Use Python dict (simpler, still sparse)
- ⚠️ **Template metaprogramming** → Use Python generics/typing
- ⚠️ **Complex variant system** → Simple material IDs (mall doesn't need variants)
- ⚠️ **WASM/Native bindings** → Pure Python (good enough for single-player)

### What to Skip:
- ❌ **Multiplayer networking** (not needed)
- ❌ **Block sampling system** (overkill for mall)
- ❌ **Bazel build system** (Python uses pip/poetry)
- ❌ **WebGL/Three.js specifics** (using Pygame/PyOpenGL)

---

## Math Validation Checklist

Before implementing each algorithm, verify:

- [ ] **Position encoding is reversible** (encode → decode → same position)
- [ ] **Chunk boundaries are correct** (no off-by-one errors)
- [ ] **Sparse storage saves memory** (benchmark vs dense array)
- [ ] **Render passes execute in order** (depth → base → translucent → post)
- [ ] **Quality settings actually improve performance** (measure FPS)

---

## References

- **Biomes GitHub:** https://github.com/ill-inc/biomes-game
- **Voxeloo (C++ engine):** https://github.com/ill-inc/biomes-game/tree/main/voxeloo
- **Our analysis doc:** (see earlier conversation for full comparison)

---

**Last Updated:** 2025-12-06
**Status:** Reference files copied, ready for Python implementation
