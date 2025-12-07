#!/usr/bin/env python3
"""
PROBE TELEMETRY FORMAT
Deep space probe base primitives applied to mall simulation.

Same shape, different application:
  - Deep space probe: Position, sensors, symbols, telemetry
  - Mall simulation: Position, voxels, symbols, state

Minimal, efficient, bandwidth-optimized.
"""

import struct
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import IntEnum


# ============================================================================
# BASE PRIMITIVES (DEEP SPACE PROBE STYLE)
# ============================================================================

class EntityType(IntEnum):
    """Entity type codes (4 bits)"""
    UNKNOWN = 0
    ZONE = 1
    ITEM = 2
    NPC = 3
    FEATURE = 4
    PLAYER = 5
    SENSOR = 6
    MARKER = 7


@dataclass
class ProbePacket:
    """
    Minimal telemetry packet (deep space probe format).

    Total size: 24 bytes (192 bits)
    - Same as Voyager 1 telemetry frame structure
    """
    # Header (8 bytes)
    entity_id: int      # 4 bytes - unique ID
    entity_type: int    # 1 byte - EntityType enum
    flags: int          # 1 byte - status flags
    sequence: int       # 2 bytes - packet sequence number

    # Position (12 bytes)
    x: float           # 4 bytes - X coordinate (feet)
    y: float           # 4 bytes - Y coordinate (feet)
    z: float           # 4 bytes - Z elevation (feet)

    # State (4 bytes)
    state: int         # 2 bytes - state code
    checksum: int      # 2 bytes - CRC16

    def pack(self) -> bytes:
        """Pack to binary format (24 bytes)."""
        return struct.pack(
            '<IBBHfffHH',  # Little-endian format
            self.entity_id,
            self.entity_type,
            self.flags,
            self.sequence,
            self.x, self.y, self.z,
            self.state,
            self.checksum
        )

    @classmethod
    def unpack(cls, data: bytes) -> 'ProbePacket':
        """Unpack from binary format."""
        unpacked = struct.unpack('<IBBHfffHH', data)
        return cls(*unpacked)


# ============================================================================
# SYMBOL ENCODING (WINGDINGS AS ENTITY IDS)
# ============================================================================

def symbol_to_entity_id(symbol: str) -> int:
    """
    Convert Unicode symbol(s) to 4-byte entity ID.

    Deep space probe style: Each entity has a numeric ID.

    For single symbol: Use Unicode codepoint
    For stacked symbols: XOR codepoints together (creates unique ID)

    Examples:
        '🧹' → 129529
        '⬆️' (multi-codepoint) → XOR of codepoints
        '🏬🍽️' (stacked) → XOR of both symbols (hierarchical)
    """
    if len(symbol) == 1:
        return ord(symbol)
    else:
        # Stacked symbols: XOR all codepoints
        entity_id = 0
        for char in symbol:
            entity_id ^= ord(char)
        return entity_id


def entity_id_to_symbol(entity_id: int, reverse_map: dict = None) -> str:
    """
    Convert entity ID back to symbol.

    For single symbols: Use chr()
    For stacked symbols: Need reverse lookup table
    """
    if reverse_map and entity_id in reverse_map:
        return reverse_map[entity_id]

    # Try single character
    try:
        return chr(entity_id)
    except (ValueError, OverflowError):
        return f"<ID:{entity_id}>"


# ============================================================================
# MEASUREMENT ENCODING
# ============================================================================

def encode_measurement(value: float, unit: str = "feet") -> int:
    """
    Encode measurement as 16-bit integer (probe-style).

    Range: 0.0 - 655.35 feet (0.01 foot precision)
    Format: value * 100 (centifeet)

    Examples:
        8.0 feet → 800
        175.5 feet → 17550
    """
    return int(value * 100)


def decode_measurement(encoded: int) -> float:
    """Decode 16-bit measurement."""
    return encoded / 100.0


# ============================================================================
# VOXEL COMPACT ENCODING (PROBE DATA COMPRESSION)
# ============================================================================

def encode_voxel_run(material_id: int, count: int) -> bytes:
    """
    Run-length encoding for voxel data (deep space probe style).

    Format: 1 byte material + 1 byte count = 2 bytes per run
    Max run length: 255 voxels

    Examples:
        Material 5, 10 voxels → b'\x05\x0A'
        Material 12, 128 voxels → b'\x0C\x80'
    """
    return struct.pack('BB', material_id, count)


def decode_voxel_run(data: bytes) -> Tuple[int, int]:
    """Decode voxel run."""
    return struct.unpack('BB', data)


# ============================================================================
# ZONE TELEMETRY (SPATIAL SENSOR DATA)
# ============================================================================

@dataclass
class ZoneTelemetry:
    """
    Zone sensor data (deep space probe scanning format).

    Minimal representation of spatial zone.
    """
    symbol: str                    # Wingdings ID
    center: Tuple[float, float, float]  # Position
    bounds: Tuple[float, float, float]  # (width, height, depth) in feet
    elevation: float               # Feet from datum
    confidence: int                # 0-255 (0 = low, 255 = high)

    def to_probe_packet(self, sequence: int = 0) -> ProbePacket:
        """Convert to probe telemetry packet."""
        entity_id = symbol_to_entity_id(self.symbol)

        return ProbePacket(
            entity_id=entity_id,
            entity_type=EntityType.ZONE,
            flags=0,
            sequence=sequence,
            x=self.center[0],
            y=self.center[1],
            z=self.center[2],
            state=self.confidence << 8,  # Pack confidence in high byte
            checksum=0  # TODO: Calculate CRC16
        )


# ============================================================================
# ITEM TELEMETRY (OBJECT TRACKING)
# ============================================================================

@dataclass
class ItemTelemetry:
    """
    Item tracking data (probe object detection format).
    """
    symbol: str                    # Wingdings ID
    position: Tuple[float, float, float]
    qbit_aggregate: int            # 0-65535 (QBIT score)
    status: int                    # Status flags

    def to_probe_packet(self, sequence: int = 0) -> ProbePacket:
        """Convert to probe telemetry packet."""
        entity_id = symbol_to_entity_id(self.symbol)

        return ProbePacket(
            entity_id=entity_id,
            entity_type=EntityType.ITEM,
            flags=0,
            sequence=sequence,
            x=self.position[0],
            y=self.position[1],
            z=self.position[2],
            state=self.qbit_aggregate,
            checksum=0
        )


# ============================================================================
# RENPY BRIDGE (TELEMETRY → VISUAL NOVEL)
# ============================================================================

def telemetry_to_renpy_position(packet: ProbePacket) -> dict:
    """
    Convert probe telemetry to Ren'Py screen position.

    Deep space probe coordinates → Screen pixels
    Mapping: Feet → Pixels (1 foot = 10 pixels at 1:1 scale)
    """
    # Convert mall coordinates to screen coordinates
    # Origin: Center of screen
    # Scale: 1 foot = 10 pixels (configurable)

    SCALE = 10  # pixels per foot
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080

    screen_x = int(SCREEN_WIDTH / 2 + packet.x * SCALE)
    screen_y = int(SCREEN_HEIGHT / 2 - packet.y * SCALE)  # Invert Y (screen coords)

    return {
        "xpos": screen_x,
        "ypos": screen_y,
        "xanchor": 0.5,
        "yanchor": 0.5
    }


def generate_renpy_displayable(packet: ProbePacket) -> str:
    """
    Generate Ren'Py displayable code from telemetry packet.

    Returns Ren'Py ATL transform code.
    """
    symbol = entity_id_to_symbol(packet.entity_id)
    pos = telemetry_to_renpy_position(packet)

    return f"""
transform entity_{packet.entity_id}:
    "{symbol}"
    xpos {pos['xpos']}
    ypos {pos['ypos']}
    xanchor {pos['xanchor']}
    yanchor {pos['yanchor']}
    # Probe telemetry: ({packet.x:.2f}, {packet.y:.2f}, {packet.z:.2f})
"""


# ============================================================================
# EXAMPLE: ESCALATOR WELLS (SOURCE OF TRUTH)
# ============================================================================

def create_escalator_telemetry() -> List[ProbePacket]:
    """
    Create probe telemetry for escalator wells.

    Source of truth: 12 steps × 8 inches = 8 feet
    """
    escalator_symbol = '⬆️'

    # Top of escalator (ground level)
    top_packet = ZoneTelemetry(
        symbol=escalator_symbol,
        center=(0, -80, 0),
        bounds=(25, 25, 8),
        elevation=0.0,
        confidence=255  # HIGH confidence
    ).to_probe_packet(sequence=0)

    # Bottom of escalator (8 feet down)
    bottom_packet = ZoneTelemetry(
        symbol=escalator_symbol,
        center=(0, -100, -8),
        bounds=(25, 25, 8),
        elevation=-8.0,
        confidence=255  # HIGH confidence
    ).to_probe_packet(sequence=1)

    return [top_packet, bottom_packet]


# ============================================================================
# CLI TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PROBE TELEMETRY FORMAT TEST")
    print("=" * 80)

    # Test symbol encoding
    print("\n[SYMBOL TO ENTITY ID]")
    janitor_symbol = '🧹'
    entity_id = symbol_to_entity_id(janitor_symbol)
    print(f"  Symbol: {janitor_symbol}")
    print(f"  Entity ID: {entity_id} (0x{entity_id:08X})")
    print(f"  Reverse: {entity_id_to_symbol(entity_id)}")

    # Test probe packet
    print("\n[PROBE PACKET]")
    packet = ProbePacket(
        entity_id=entity_id,
        entity_type=EntityType.ITEM,
        flags=0,
        sequence=42,
        x=10.5, y=-20.3, z=0.0,
        state=680,  # QBIT aggregate
        checksum=0
    )
    print(f"  Packet: {packet}")
    print(f"  Binary size: {len(packet.pack())} bytes")

    # Test measurement encoding
    print("\n[MEASUREMENT ENCODING]")
    escalator_drop = 8.0  # feet (source of truth)
    encoded = encode_measurement(escalator_drop)
    print(f"  Original: {escalator_drop} feet")
    print(f"  Encoded: {encoded} (16-bit)")
    print(f"  Decoded: {decode_measurement(encoded)} feet")

    # Test escalator telemetry
    print("\n[ESCALATOR TELEMETRY]")
    escalator_packets = create_escalator_telemetry()
    for i, pkt in enumerate(escalator_packets):
        print(f"  Packet {i}: ({pkt.x}, {pkt.y}, {pkt.z}) @ seq {pkt.sequence}")

    # Test Ren'Py conversion
    print("\n[REN'PY DISPLAYABLE]")
    renpy_code = generate_renpy_displayable(packet)
    print(renpy_code)

    print("\n" + "=" * 80)
    print("SAME SHAPE, DIFFERENT APPLICATION")
    print("  Deep space probe: Mapping Europa's surface")
    print("  Mall simulation: Mapping Eastland Mall")
    print("  Format: Identical (position, symbols, telemetry)")
    print("=" * 80)
