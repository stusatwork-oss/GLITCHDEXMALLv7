"""
MallOS World State - Object Registry and Spatial Coordinates

Zone = Compute node (Cloud/QBIT live here)
Tile = Memory address within zone's local state

This module provides:
- tile ↔ world coordinate conversion
- World object registry (zone_id + tile + world_pos tracking)
- Unicast zone pressure modification
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path


# ============================================================================
# CONSTANTS
# ============================================================================

TILE_SIZE_FEET = 4.0  # Each tile = 4x4 feet (standard mall corridor width ~18-25 ft = 4-6 tiles)


# ============================================================================
# COORDINATE CONVERSION
# ============================================================================

def tile_to_world(tx: int, ty: int, zone_id: str, zone_origins: Optional[Dict[str, Tuple[float, float]]] = None) -> Tuple[float, float, float]:
    """
    Convert tile coordinates to world coordinates.

    Args:
        tx, ty: Tile coordinates (integers)
        zone_id: Zone identifier
        zone_origins: Dict mapping zone_id → (world_x, world_y) origin (optional)

    Returns:
        (world_x, world_y, world_z) in feet
    """
    # Default zone origins (can be overridden)
    default_origins = {
        "Z1_CENTRAL_ATRIUM": (0, 0),
        "Z4_FOOD_COURT": (100, 0),
        "FC-ARCADE": (100, -30),
        "SERVICE_HALL": (20, -50),
        "Z3_LOWER_RING": (0, 0),
    }

    origins = zone_origins or default_origins
    origin_x, origin_y = origins.get(zone_id, (0, 0))

    world_x = origin_x + (tx * TILE_SIZE_FEET)
    world_y = origin_y + (ty * TILE_SIZE_FEET)
    world_z = 0.0  # Ground level (zones handle vertical offset)

    return (world_x, world_y, world_z)


def world_to_tile(world_x: float, world_y: float, zone_id: str, zone_origins: Optional[Dict[str, Tuple[float, float]]] = None) -> Tuple[int, int]:
    """
    Convert world coordinates to tile coordinates within a zone.

    Args:
        world_x, world_y: World coordinates in feet
        zone_id: Zone identifier
        zone_origins: Dict mapping zone_id → (world_x, world_y) origin (optional)

    Returns:
        (tx, ty) tile coordinates (integers)
    """
    default_origins = {
        "Z1_CENTRAL_ATRIUM": (0, 0),
        "Z4_FOOD_COURT": (100, 0),
        "FC-ARCADE": (100, -30),
        "SERVICE_HALL": (20, -50),
        "Z3_LOWER_RING": (0, 0),
    }

    origins = zone_origins or default_origins
    origin_x, origin_y = origins.get(zone_id, (0, 0))

    tx = int((world_x - origin_x) / TILE_SIZE_FEET)
    ty = int((world_y - origin_y) / TILE_SIZE_FEET)

    return (tx, ty)


# ============================================================================
# WORLD OBJECT REGISTRY
# ============================================================================

@dataclass
class WorldObject:
    """
    Object instance in the MallOS world.

    Combines:
    - Voxel object definition (from registry)
    - Spatial location (zone + tile + world pos)
    - Runtime state (picked up, modified, etc.)
    """
    object_id: str              # e.g., "ARCADE_TOKEN"
    zone_id: str                # e.g., "FC-ARCADE"
    tile: Tuple[int, int]       # (tx, ty) tile address
    world_pos: Tuple[float, float, float]  # (x, y, z) in feet

    voxel_object: Any = None    # Reference to VoxelObject from registry
    picked_up: bool = False
    owner_npc_id: Optional[str] = None  # For NPC props (e.g., JANITOR_MOP → "UNIT_7")

    # Runtime state
    state: Dict[str, Any] = field(default_factory=dict)


class WorldObjectRegistry:
    """
    Central registry of all active voxel objects in the world.

    Tracks:
    - All spawned objects (zone + tile + world position)
    - Object lifecycle (spawn, pickup, despawn)
    - Zone-local object queries
    """

    def __init__(self):
        self.objects: Dict[str, WorldObject] = {}  # object_id → WorldObject
        self.zone_objects: Dict[str, List[str]] = {}  # zone_id → [object_ids]
        self.next_instance_id = 0

    def spawn_object(
        self,
        object_id: str,
        voxel_object: Any,
        zone_id: str,
        tile: Tuple[int, int],
        zones: Optional[Dict[str, Any]] = None,
        zone_origins: Optional[Dict[str, Tuple[float, float]]] = None,
        owner_npc_id: Optional[str] = None
    ) -> str:
        """
        Spawn a voxel object in the world.

        Args:
            object_id: Base object ID (e.g., "ARCADE_TOKEN")
            voxel_object: VoxelObject from registry
            zone_id: Zone to spawn in
            tile: (tx, ty) tile coordinates
            zones: Optional zones dict for QBIT charging
            zone_origins: Optional zone origin map
            owner_npc_id: Optional NPC owner for props

        Returns:
            Instance ID (unique for this spawn)
        """
        # Generate unique instance ID
        instance_id = f"{object_id}_{self.next_instance_id}"
        self.next_instance_id += 1

        # Convert tile to world position
        world_pos = tile_to_world(tile[0], tile[1], zone_id, zone_origins)

        # Create world object
        world_obj = WorldObject(
            object_id=object_id,
            zone_id=zone_id,
            tile=tile,
            world_pos=world_pos,
            voxel_object=voxel_object,
            owner_npc_id=owner_npc_id
        )

        # Register object
        self.objects[instance_id] = world_obj

        # Add to zone index
        if zone_id not in self.zone_objects:
            self.zone_objects[zone_id] = []
        self.zone_objects[zone_id].append(instance_id)

        # QBIT zone charging (object adds computational load)
        if zones:
            charge_zone_qbit(zones, zone_id, voxel_object)

        return instance_id

    def get_object(self, instance_id: str) -> Optional[WorldObject]:
        """Get object by instance ID."""
        return self.objects.get(instance_id)

    def get_zone_objects(self, zone_id: str) -> List[WorldObject]:
        """Get all objects in a zone."""
        instance_ids = self.zone_objects.get(zone_id, [])
        return [self.objects[iid] for iid in instance_ids if iid in self.objects]

    def pickup_object(self, instance_id: str, zones: Optional[Dict[str, Any]] = None) -> bool:
        """
        Mark object as picked up.

        Args:
            instance_id: Object instance ID
            zones: Optional zones dict for QBIT discharging

        Returns:
            True if successful, False if already picked up or not found
        """
        obj = self.objects.get(instance_id)
        if obj and not obj.picked_up:
            obj.picked_up = True

            # QBIT zone discharging (object removed from zone computational load)
            if zones and obj.voxel_object:
                discharge_zone_qbit(zones, obj.zone_id, obj.voxel_object)

            return True
        return False

    def despawn_object(self, instance_id: str, zones: Optional[Dict[str, Any]] = None) -> bool:
        """
        Remove object from world.

        Args:
            instance_id: Object instance ID
            zones: Optional zones dict for QBIT discharging

        Returns:
            True if successful, False if not found
        """
        obj = self.objects.get(instance_id)
        if obj:
            # QBIT zone discharging (object removed from zone)
            if zones and obj.voxel_object and not obj.picked_up:
                discharge_zone_qbit(zones, obj.zone_id, obj.voxel_object)

            # Remove from zone index
            if obj.zone_id in self.zone_objects:
                self.zone_objects[obj.zone_id].remove(instance_id)

            # Remove from main registry
            del self.objects[instance_id]
            return True
        return False

    def find_objects_at_tile(self, zone_id: str, tile: Tuple[int, int]) -> List[WorldObject]:
        """Find all objects at a specific tile."""
        zone_objs = self.get_zone_objects(zone_id)
        return [obj for obj in zone_objs if obj.tile == tile and not obj.picked_up]

    def find_npc_props(self, npc_id: str) -> List[WorldObject]:
        """Find all objects owned by an NPC."""
        return [obj for obj in self.objects.values() if obj.owner_npc_id == npc_id]


# ============================================================================
# ZONE PRESSURE MODIFICATION (Unicast)
# ============================================================================

def modify_zone_pressure(zones: Dict[str, Any], zone_id: str, delta: float) -> bool:
    """
    Modify cloud pressure for a specific zone (unicast).

    Args:
        zones: Dict of zone_id → ZoneMicrostate
        zone_id: Target zone
        delta: Pressure change (+/-)

    Returns:
        True if successful, False if zone not found
    """
    zone = zones.get(zone_id)
    if zone:
        zone.cloud_pressure += delta
        # Clamp to 0-100
        zone.cloud_pressure = max(0.0, min(100.0, zone.cloud_pressure))
        return True
    return False


# ============================================================================
# ZONE QBIT CHARGING (Circuit Component Integration)
# ============================================================================

def charge_zone_qbit(zones: Dict[str, Any], zone_id: str, voxel_object: Any) -> bool:
    """
    Charge zone's QBIT aggregate with object's QBIT vector.

    Args:
        zones: Dict of zone_id → ZoneMicrostate
        zone_id: Target zone
        voxel_object: VoxelObject with QBIT scores

    Returns:
        True if successful, False if zone not found or object has no QBIT
    """
    zone = zones.get(zone_id)
    if not zone:
        return False

    # Check if object has QBIT scores
    if not hasattr(voxel_object, 'get_qbit_aggregate'):
        return False

    qbit_aggregate = voxel_object.get_qbit_aggregate()
    if qbit_aggregate > 0:
        zone.qbit_aggregate += qbit_aggregate
        # Also update component counts
        zone.qbit_entity_count += 1

        # Update individual scores if available
        if voxel_object.qbit:
            zone.qbit_power += voxel_object.qbit.get("power", 0)
            zone.qbit_charisma += voxel_object.qbit.get("charisma", 0)
        return True
    return False


def discharge_zone_qbit(zones: Dict[str, Any], zone_id: str, voxel_object: Any) -> bool:
    """
    Discharge zone's QBIT aggregate (object picked up/removed).

    Args:
        zones: Dict of zone_id → ZoneMicrostate
        zone_id: Target zone
        voxel_object: VoxelObject with QBIT scores

    Returns:
        True if successful, False if zone not found or object has no QBIT
    """
    zone = zones.get(zone_id)
    if not zone:
        return False

    # Check if object has QBIT scores
    if not hasattr(voxel_object, 'get_qbit_aggregate'):
        return False

    qbit_aggregate = voxel_object.get_qbit_aggregate()
    if qbit_aggregate > 0:
        zone.qbit_aggregate -= qbit_aggregate
        # Clamp to 0 (can't go negative)
        zone.qbit_aggregate = max(0.0, zone.qbit_aggregate)

        # Update component counts
        zone.qbit_entity_count = max(0, zone.qbit_entity_count - 1)

        # Update individual scores if available
        if voxel_object.qbit:
            zone.qbit_power -= voxel_object.qbit.get("power", 0)
            zone.qbit_power = max(0.0, zone.qbit_power)
            zone.qbit_charisma -= voxel_object.qbit.get("charisma", 0)
            zone.qbit_charisma = max(0.0, zone.qbit_charisma)
        return True
    return False


# ============================================================================
# MODULE TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MALLOS WORLD STATE TEST")
    print("=" * 60)

    # Test coordinate conversion
    print("\nTile → World Conversion:")
    for zone_id in ["Z1_CENTRAL_ATRIUM", "Z4_FOOD_COURT", "FC-ARCADE"]:
        world_pos = tile_to_world(5, 10, zone_id)
        print(f"  {zone_id} tile (5, 10) → world {world_pos}")

    print("\nWorld → Tile Conversion:")
    tile = world_to_tile(100, 0, "Z4_FOOD_COURT")
    print(f"  World (100, 0) in FOOD_COURT → tile {tile}")

    # Test world object registry
    print("\n" + "-" * 60)
    print("World Object Registry Test:")

    registry = WorldObjectRegistry()

    # Mock voxel object
    class MockVoxelObject:
        def __init__(self, obj_id):
            self.id = obj_id

    # Spawn objects
    token_id = registry.spawn_object(
        "ARCADE_TOKEN",
        MockVoxelObject("ARCADE_TOKEN"),
        "FC-ARCADE",
        (5, 10)
    )
    print(f"\nSpawned ARCADE_TOKEN: {token_id}")

    mop_id = registry.spawn_object(
        "JANITOR_MOP",
        MockVoxelObject("JANITOR_MOP"),
        "SERVICE_HALL",
        (1, 2),
        owner_npc_id="UNIT_7"
    )
    print(f"Spawned JANITOR_MOP: {mop_id}")

    # Query objects
    print(f"\nObjects in FC-ARCADE: {len(registry.get_zone_objects('FC-ARCADE'))}")
    print(f"Objects in SERVICE_HALL: {len(registry.get_zone_objects('SERVICE_HALL'))}")

    # Pickup object
    registry.pickup_object(token_id)
    token = registry.get_object(token_id)
    print(f"\nToken picked up: {token.picked_up}")

    # Find NPC props
    janitor_props = registry.find_npc_props("UNIT_7")
    print(f"Janitor props: {[p.object_id for p in janitor_props]}")

    # Test zone pressure modification
    print("\n" + "-" * 60)
    print("Zone Pressure Modification Test:")

    # Mock zones
    class MockZone:
        def __init__(self, zone_id):
            self.zone_id = zone_id
            self.cloud_pressure = 0.0

    zones = {
        "FC-ARCADE": MockZone("FC-ARCADE"),
        "SERVICE_HALL": MockZone("SERVICE_HALL"),
    }

    print(f"\nInitial FC-ARCADE pressure: {zones['FC-ARCADE'].cloud_pressure}")
    modify_zone_pressure(zones, "FC-ARCADE", +15.5)
    print(f"After +15.5: {zones['FC-ARCADE'].cloud_pressure}")
    modify_zone_pressure(zones, "FC-ARCADE", -5.0)
    print(f"After -5.0: {zones['FC-ARCADE'].cloud_pressure}")

    print("\n✓ MallOS world state test complete")
