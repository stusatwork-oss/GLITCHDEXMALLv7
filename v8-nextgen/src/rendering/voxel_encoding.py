#!/usr/bin/env python3
"""
Voxel Position Encoding Utilities

Based on Biomes' voxeloo/tensors/tensors.hpp encoding system.
Encodes 3D positions into compact integers for memory-efficient sparse storage.

Reference:
  - biomes-game/voxeloo/tensors/tensors.hpp:20-46
  - See: v8-nextgen/reference/biomes/voxel_math/tensors.hpp
"""

from typing import Tuple


# =============================================================================
# CHUNK CONSTANTS
# =============================================================================

CHUNK_SIZE = 32  # 32x32x32 voxels per chunk (matches Biomes)
CHUNK_VOLUME = CHUNK_SIZE ** 3  # 32,768 voxels


# =============================================================================
# POSITION ENCODING (15-bit for chunk-local coordinates)
# =============================================================================

def encode_tensor_pos(x: int, y: int, z: int) -> int:
    """
    Encode 3D position into a single integer (15-bit total).

    Bit layout (5 bits per axis for 0-31 range):
      - Bits 10-14: Y coordinate (5 bits)
      - Bits 5-9:   Z coordinate (5 bits)
      - Bits 0-4:   X coordinate (5 bits)

    This matches Biomes' encoding from tensors.hpp:20-25:
      auto k_0 = static_cast<ArrayPos>((pos.y & 0x1f) << 10);
      auto k_1 = static_cast<ArrayPos>((pos.z & 0x1f) << 5);
      auto k_2 = static_cast<ArrayPos>((pos.x & 0x1f));
      return static_cast<ArrayPos>(k_0 | k_1 | k_2);

    Args:
        x: X coordinate (0-31 for chunk-local)
        y: Y coordinate (0-31 for chunk-local)
        z: Z coordinate (0-31 for chunk-local)

    Returns:
        15-bit encoded position (0-32767)

    Example:
        >>> encode_tensor_pos(0, 0, 0)
        0
        >>> encode_tensor_pos(31, 31, 31)
        32767
        >>> encode_tensor_pos(15, 15, 15)
        15855
    """
    # Validate input range
    assert 0 <= x < CHUNK_SIZE, f"X out of range: {x} (must be 0-31)"
    assert 0 <= y < CHUNK_SIZE, f"Y out of range: {y} (must be 0-31)"
    assert 0 <= z < CHUNK_SIZE, f"Z out of range: {z} (must be 0-31)"

    # Encode (5 bits each, YZX order)
    k_0 = (y & 0x1f) << 10  # Y: bits 10-14
    k_1 = (z & 0x1f) << 5   # Z: bits 5-9
    k_2 = (x & 0x1f)        # X: bits 0-4

    return k_0 | k_1 | k_2


def decode_tensor_pos(encoded: int) -> Tuple[int, int, int]:
    """
    Decode integer back to 3D position.

    Reverses the encoding from encode_tensor_pos().

    This matches Biomes' decoding from tensors.hpp:27-32:
      auto y = static_cast<unsigned int>((pos >> 10) & 0x1f);
      auto z = static_cast<unsigned int>((pos >> 5) & 0x1f);
      auto x = static_cast<unsigned int>(pos & 0x1f);
      return vec3(x, y, z);

    Args:
        encoded: 15-bit encoded position

    Returns:
        Tuple of (x, y, z) coordinates (0-31 each)

    Example:
        >>> decode_tensor_pos(0)
        (0, 0, 0)
        >>> decode_tensor_pos(32767)
        (31, 31, 31)
        >>> decode_tensor_pos(15855)
        (15, 15, 15)
    """
    # Validate input range
    assert 0 <= encoded < CHUNK_VOLUME, f"Encoded value out of range: {encoded}"

    # Decode (extract 5 bits each)
    y = (encoded >> 10) & 0x1f  # Bits 10-14
    z = (encoded >> 5) & 0x1f   # Bits 5-9
    x = encoded & 0x1f          # Bits 0-4

    return (x, y, z)


# =============================================================================
# WORLD POSITION ENCODING (30-bit for global coordinates)
# =============================================================================

def encode_tensor_pos_32(x: int, y: int, z: int) -> int:
    """
    Encode 3D position into a single integer (30-bit total).

    For larger worlds, supports 0-1023 range per axis (10 bits each).

    Bit layout:
      - Bits 20-29: Y coordinate (10 bits)
      - Bits 10-19: Z coordinate (10 bits)
      - Bits 0-9:   X coordinate (10 bits)

    This matches Biomes' encode_tensor_pos32 from tensors.hpp:34-39.

    Args:
        x: X coordinate (0-1023)
        y: Y coordinate (0-1023)
        z: Z coordinate (0-1023)

    Returns:
        30-bit encoded position

    Example:
        >>> encode_tensor_pos_32(0, 0, 0)
        0
        >>> encode_tensor_pos_32(1023, 1023, 1023)
        1073741823
    """
    # Validate input range (10 bits = 0-1023)
    assert 0 <= x < 1024, f"X out of range: {x} (must be 0-1023)"
    assert 0 <= y < 1024, f"Y out of range: {y} (must be 0-1023)"
    assert 0 <= z < 1024, f"Z out of range: {z} (must be 0-1023)"

    # Encode (10 bits each, YZX order)
    k_0 = (y & 0x3ff) << 20  # Y: bits 20-29
    k_1 = (z & 0x3ff) << 10  # Z: bits 10-19
    k_2 = (x & 0x3ff)        # X: bits 0-9

    return k_0 | k_1 | k_2


def decode_tensor_pos_32(encoded: int) -> Tuple[int, int, int]:
    """
    Decode 30-bit integer back to 3D position.

    Reverses encode_tensor_pos_32().

    This matches Biomes' decode_tensor_pos32 from tensors.hpp:41-46.

    Args:
        encoded: 30-bit encoded position

    Returns:
        Tuple of (x, y, z) coordinates (0-1023 each)

    Example:
        >>> decode_tensor_pos_32(0)
        (0, 0, 0)
        >>> decode_tensor_pos_32(1073741823)
        (1023, 1023, 1023)
    """
    # Validate input range (30 bits max)
    assert 0 <= encoded < (1 << 30), f"Encoded value out of range: {encoded}"

    # Decode (extract 10 bits each)
    y = (encoded >> 20) & 0x3ff  # Bits 20-29
    z = (encoded >> 10) & 0x3ff  # Bits 10-19
    x = encoded & 0x3ff          # Bits 0-9

    return (x, y, z)


# =============================================================================
# CHUNK COORDINATE CONVERSIONS
# =============================================================================

def world_to_chunk(x: float, y: float, z: float) -> Tuple[int, int, int]:
    """
    Convert world coordinates to chunk coordinates.

    Args:
        x, y, z: World position in feet/voxels

    Returns:
        Tuple of chunk coordinates (cx, cy, cz)

    Example:
        >>> world_to_chunk(0, 0, 0)
        (0, 0, 0)
        >>> world_to_chunk(32, 64, 96)
        (1, 2, 3)
        >>> world_to_chunk(-32, -32, -32)
        (-1, -1, -1)
    """
    return (
        int(x // CHUNK_SIZE),
        int(y // CHUNK_SIZE),
        int(z // CHUNK_SIZE)
    )


def world_to_local(x: float, y: float, z: float) -> Tuple[int, int, int]:
    """
    Convert world coordinates to chunk-local coordinates (0-31).

    Args:
        x, y, z: World position in feet/voxels

    Returns:
        Tuple of local coordinates within chunk (lx, ly, lz)

    Example:
        >>> world_to_local(0, 0, 0)
        (0, 0, 0)
        >>> world_to_local(33, 65, 97)
        (1, 1, 1)
        >>> world_to_local(31, 31, 31)
        (31, 31, 31)
    """
    return (
        int(x) % CHUNK_SIZE,
        int(y) % CHUNK_SIZE,
        int(z) % CHUNK_SIZE
    )


def chunk_and_local(x: float, y: float, z: float) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    """
    Convert world coordinates to both chunk and local coordinates.

    Args:
        x, y, z: World position in feet/voxels

    Returns:
        Tuple of ((cx, cy, cz), (lx, ly, lz))

    Example:
        >>> chunk_and_local(33, 65, 97)
        ((1, 2, 3), (1, 1, 1))
    """
    chunk_coords = world_to_chunk(x, y, z)
    local_coords = world_to_local(x, y, z)
    return (chunk_coords, local_coords)


# =============================================================================
# MEMORY ANALYSIS UTILITIES
# =============================================================================

def encoding_memory_usage(num_voxels: int) -> dict:
    """
    Calculate memory usage for different storage strategies.

    Args:
        num_voxels: Number of non-air voxels to store

    Returns:
        Dict with memory usage in bytes for different approaches

    Example:
        >>> encoding_memory_usage(1000)
        {
            'tuple_dict': 24000,      # Dict[(int,int,int), int] = 24 bytes/entry
            'encoded_dict': 8000,     # Dict[int, int] = 8 bytes/entry
            'savings_bytes': 16000,
            'savings_percent': 66.67
        }
    """
    # Python dict overhead estimates:
    # - Tuple key: ~16 bytes (3 ints) + dict overhead ~8 bytes = 24 bytes
    # - Int key: ~4 bytes + dict overhead ~4 bytes = 8 bytes

    tuple_bytes = num_voxels * 24  # Dict[(x,y,z), material]
    encoded_bytes = num_voxels * 8  # Dict[encoded_pos, material]

    savings = tuple_bytes - encoded_bytes
    savings_percent = (savings / tuple_bytes * 100) if tuple_bytes > 0 else 0

    return {
        'tuple_dict': tuple_bytes,
        'encoded_dict': encoded_bytes,
        'savings_bytes': savings,
        'savings_percent': round(savings_percent, 2)
    }


# =============================================================================
# DELTA ENCODING (For Massive Crowds & Dynamic Environments)
# =============================================================================

def compute_state_delta(old_state: dict, new_state: dict) -> dict:
    """
    Compute delta between two voxel/entity states.

    Only returns changed, added, or removed entries.
    Perfect for:
    - Network sync (send only changes)
    - Save files (store only diffs)
    - Massive NPC crowds (most stationary)
    - Sand settling (most voxels stable after initial change)

    Args:
        old_state: Dict[id, encoded_pos] - Previous frame state
        new_state: Dict[id, encoded_pos] - Current frame state

    Returns:
        Delta dict with:
        - Added entities: {id: new_encoded_pos}
        - Changed entities: {id: new_encoded_pos - old_encoded_pos}
        - Removed entities: {id: None}

    Example:
        >>> old = {1: 100, 2: 200, 3: 300}
        >>> new = {1: 100, 2: 250, 4: 400}  # 1 unchanged, 2 moved, 3 removed, 4 added
        >>> compute_state_delta(old, new)
        {2: 50, 3: None, 4: 400}  # Only 3 entries instead of 4!
    """
    delta = {}

    # Check for changes and additions
    for entity_id, new_pos in new_state.items():
        if entity_id not in old_state:
            # NEW entity
            delta[entity_id] = new_pos
        elif old_state[entity_id] != new_pos:
            # MOVED entity (store as delta for compression)
            delta[entity_id] = new_pos - old_state[entity_id]

    # Check for removals
    for entity_id in old_state:
        if entity_id not in new_state:
            # REMOVED entity
            delta[entity_id] = None

    return delta


def apply_state_delta(old_state: dict, delta: dict) -> dict:
    """
    Apply delta to reconstruct new state.

    Reverses compute_state_delta().

    Args:
        old_state: Previous state
        delta: Changes from compute_state_delta()

    Returns:
        New reconstructed state

    Example:
        >>> old = {1: 100, 2: 200, 3: 300}
        >>> delta = {2: 50, 3: None, 4: 400}
        >>> apply_state_delta(old, delta)
        {1: 100, 2: 250, 4: 400}
    """
    new_state = old_state.copy()

    for entity_id, change in delta.items():
        if change is None:
            # REMOVED
            new_state.pop(entity_id, None)
        elif entity_id not in old_state:
            # ADDED (delta is absolute position)
            new_state[entity_id] = change
        else:
            # MOVED (delta is relative change)
            new_state[entity_id] = old_state[entity_id] + change

    return new_state


def compute_voxel_delta_xor(old_voxels: dict, new_voxels: dict) -> dict:
    """
    Compute XOR-based delta for voxel material changes.

    XOR is perfect for bit-level changes in material IDs.
    If materials are similar, XOR result is small.

    Args:
        old_voxels: Dict[encoded_pos, material_id]
        new_voxels: Dict[encoded_pos, material_id]

    Returns:
        Delta dict with XOR changes

    Example:
        >>> old = {100: 0b0001, 200: 0b0010}  # Material IDs
        >>> new = {100: 0b0011, 200: 0b0010}  # Slight change to first
        >>> compute_voxel_delta_xor(old, new)
        {100: 0b0010}  # XOR = 0b0001 ^ 0b0011 = 0b0010
    """
    delta = {}

    # Check all positions in new state
    all_positions = set(old_voxels.keys()) | set(new_voxels.keys())

    for pos in all_positions:
        old_material = old_voxels.get(pos, 0)  # 0 = air
        new_material = new_voxels.get(pos, 0)

        if old_material != new_material:
            # Store XOR (detects bit-level changes)
            delta[pos] = old_material ^ new_material

    return delta


def delta_compression_ratio(old_state: dict, delta: dict) -> float:
    """
    Calculate compression ratio from delta encoding.

    Args:
        old_state: Full previous state
        delta: Delta changes

    Returns:
        Compression ratio (higher = better)
        E.g., 10.0 = delta is 10x smaller than full state

    Example:
        >>> old = {i: i*100 for i in range(1000)}  # 1000 entities
        >>> delta = {5: 50, 10: 100}  # Only 2 changed
        >>> delta_compression_ratio(old, delta)
        500.0  # 1000/2 = 500x compression!
    """
    if not delta:
        return float('inf')  # Perfect compression (nothing changed)

    return len(old_state) / len(delta)


# =============================================================================
# MALL_OS INTEGRATION EXAMPLES
# =============================================================================

def example_massive_crowd_delta():
    """
    Example: 1000 NPCs in food court, only 50 moving per frame.

    Demonstrates delta encoding for Synthactor crowds.
    """
    # Frame N: 1000 NPCs
    old_positions = {
        npc_id: encode_tensor_pos(
            10 + (npc_id % 15),      # X: 10-24
            5,                        # Y: 5 (same level)
            10 + ((npc_id // 15) % 15)  # Z: 10-24 (wrap to stay in bounds)
        )
        for npc_id in range(1000)
    }

    # Frame N+1: Only 50 NPCs moved (Cloud < 50, most stationary)
    new_positions = old_positions.copy()
    for moving_npc in range(0, 50):
        x, y, z = decode_tensor_pos(old_positions[moving_npc])
        new_positions[moving_npc] = encode_tensor_pos(x + 1, y, z)  # Step forward

    # Compute delta
    delta = compute_state_delta(old_positions, new_positions)

    # Analysis
    full_size = len(old_positions) * 4  # 4 bytes per encoded position
    delta_size = len(delta) * 4
    compression = delta_compression_ratio(old_positions, delta)

    print(f"Massive Crowd Delta Example:")
    print(f"  NPCs total: {len(old_positions)}")
    print(f"  NPCs moved: {len(delta)}")
    print(f"  Full state: {full_size} bytes")
    print(f"  Delta state: {delta_size} bytes")
    print(f"  Compression: {compression:.1f}x")
    print(f"  Bandwidth saved: {(1 - delta_size/full_size)*100:.1f}%")

    return delta


def example_sand_settling_delta():
    """
    Example: Sand voxels settling after player footstep.

    Demonstrates delta encoding for dynamic environment effects.
    """
    print("\nSand Settling Delta Example:")

    # Initial: 100 sand voxels displaced by footstep
    frame_0 = {i: encode_tensor_pos((10 + i) % 30, 20, 15) for i in range(100)}

    # Frame 1: All 100 voxels fall
    frame_1 = {i: encode_tensor_pos((10 + i) % 30, 19, 15) for i in range(100)}
    delta_1 = compute_state_delta(frame_0, frame_1)
    print(f"  Frame 1: {len(delta_1)} voxels changed (all falling)")

    # Frame 2: Only 20 still falling (rest settled)
    frame_2 = frame_1.copy()
    for i in range(20):
        x, y, z = decode_tensor_pos(frame_1[i])
        frame_2[i] = encode_tensor_pos(x, y - 1, z)
    delta_2 = compute_state_delta(frame_1, frame_2)
    print(f"  Frame 2: {len(delta_2)} voxels changed")

    # Frame 3: Only 5 still falling
    frame_3 = frame_2.copy()
    for i in range(5):
        x, y, z = decode_tensor_pos(frame_2[i])
        frame_3[i] = encode_tensor_pos(x, y - 1, z)
    delta_3 = compute_state_delta(frame_2, frame_3)
    print(f"  Frame 3: {len(delta_3)} voxels changed")

    # Frame 4: All settled
    delta_4 = compute_state_delta(frame_3, frame_3)
    print(f"  Frame 4: {len(delta_4)} voxels changed (stable)")

    total_updates = len(delta_1) + len(delta_2) + len(delta_3) + len(delta_4)
    print(f"  Total updates: {total_updates} (vs 400 if sending full state each frame)")


# =============================================================================
# VALIDATION & TESTING
# =============================================================================

def validate_encoding_roundtrip():
    """
    Validate that encode → decode produces the original position.

    Tests all corners and center of a 32³ chunk.

    Raises:
        AssertionError: If any roundtrip fails
    """
    test_positions = [
        (0, 0, 0),      # Origin
        (31, 31, 31),   # Opposite corner
        (15, 15, 15),   # Center
        (0, 0, 31),     # Edge cases
        (0, 31, 0),
        (31, 0, 0),
        (1, 2, 3),      # Random
        (10, 20, 30),
    ]

    for x, y, z in test_positions:
        encoded = encode_tensor_pos(x, y, z)
        decoded = decode_tensor_pos(encoded)

        assert decoded == (x, y, z), \
            f"Roundtrip failed: ({x},{y},{z}) -> {encoded} -> {decoded}"

    print(f"✓ Validated {len(test_positions)} position encodings")


def validate_encoding_32_roundtrip():
    """
    Validate 32-bit encoding roundtrip.

    Raises:
        AssertionError: If any roundtrip fails
    """
    test_positions = [
        (0, 0, 0),
        (1023, 1023, 1023),
        (511, 511, 511),
        (100, 200, 300),
    ]

    for x, y, z in test_positions:
        encoded = encode_tensor_pos_32(x, y, z)
        decoded = decode_tensor_pos_32(encoded)

        assert decoded == (x, y, z), \
            f"Roundtrip failed: ({x},{y},{z}) -> {encoded} -> {decoded}"

    print(f"✓ Validated {len(test_positions)} 32-bit position encodings")


# =============================================================================
# MAIN / DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("VOXEL POSITION ENCODING - v8-nextgen")
    print("=" * 80)
    print(f"Chunk size: {CHUNK_SIZE}x{CHUNK_SIZE}x{CHUNK_SIZE} = {CHUNK_VOLUME:,} voxels")
    print()

    # Test encoding/decoding
    print("Testing position encoding...")
    validate_encoding_roundtrip()
    validate_encoding_32_roundtrip()
    print()

    # Show examples
    print("Example encodings:")
    examples = [
        (0, 0, 0),
        (15, 15, 15),
        (31, 31, 31),
    ]
    for x, y, z in examples:
        encoded = encode_tensor_pos(x, y, z)
        decoded = decode_tensor_pos(encoded)
        print(f"  ({x:2d}, {y:2d}, {z:2d}) -> {encoded:5d} -> {decoded}")
    print()

    # Memory analysis
    print("Memory savings analysis:")
    for num_voxels in [100, 1_000, 10_000, 100_000]:
        usage = encoding_memory_usage(num_voxels)
        print(f"  {num_voxels:,} voxels:")
        print(f"    Tuple dict:   {usage['tuple_dict']:,} bytes")
        print(f"    Encoded dict: {usage['encoded_dict']:,} bytes")
        print(f"    Savings:      {usage['savings_bytes']:,} bytes ({usage['savings_percent']:.1f}%)")
    print()

    # World coordinate examples
    print("World → Chunk conversions:")
    world_positions = [
        (0, 0, 0),
        (33, 65, 97),
        (100, 200, 300),
    ]
    for wx, wy, wz in world_positions:
        chunk_coords, local_coords = chunk_and_local(wx, wy, wz)
        print(f"  World ({wx}, {wy}, {wz}) -> Chunk {chunk_coords} + Local {local_coords}")

    print()
    print("=" * 80)
    print("DELTA ENCODING DEMOS (Massive Crowds & Dynamic Environments)")
    print("=" * 80)
    example_massive_crowd_delta()
    example_sand_settling_delta()

    print()
    print("=" * 80)
    print("✓ All tests passed!")
    print("✓ Delta encoding ready for Mall_OS integration!")
    print("=" * 80)
