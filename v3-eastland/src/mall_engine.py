"""
Core Mall Engine – Tile System, Collision, Movement, State Management
"""

import json
import os
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class Direction(Enum):
    """Cardinal directions with facing angles"""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


@dataclass
class Tile:
    """Represents a single tile in the mall"""
    x: int
    y: int
    z: int = 0
    type: str = "VOID"
    walkable: bool = False
    description: str = ""
    artifact_id: Optional[str] = None
    npc_id: Optional[str] = None


@dataclass
class PlayerState:
    """Tracks the player's position, facing, and inventory"""
    x: int
    y: int
    z: int = 0
    facing: Direction = Direction.NORTH
    inventory: List[str] = field(default_factory=list)
    playtime_seconds: int = 0
    visited_tiles: set = field(default_factory=set)
    interacted_npcs: Dict[str, int] = field(default_factory=dict)  # npc_id -> interaction_count


class MallEngine:
    """Core engine managing the mall state, collision, and movement"""

    def __init__(self, map_file: str = None):
        """Initialize the mall engine from a JSON map file"""
        self.tiles: Dict[Tuple[int, int, int], Tile] = {}
        self.width = 50
        self.height = 50
        self.depth = 1
        self.player = PlayerState(x=0, y=24, z=0, facing=Direction.EAST)
        self.npc_positions: Dict[str, Tuple[int, int, int]] = {}
        self.artifact_locations: Dict[str, Tuple[int, int, int]] = {}

        if map_file is None:
            map_file = os.path.join(os.path.dirname(__file__), "../data/mall_map.json")

        self.load_map(map_file)

    def load_map(self, map_file: str):
        """Load the mall layout from JSON"""
        with open(map_file, 'r') as f:
            map_data = json.load(f)

        self.width = map_data.get("width", 50)
        self.height = map_data.get("height", 50)

        # Initialize all tiles as VOID (impassable)
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    self.tiles[(x, y, z)] = Tile(x=x, y=y, z=z, type="VOID", walkable=False)

        # Load defined tiles from map data
        for tile_data in map_data.get("tiles", []):
            x, y, z = tile_data.get("x"), tile_data.get("y"), tile_data.get("z", 0)
            tile = Tile(
                x=x, y=y, z=z,
                type=tile_data.get("type", "CORRIDOR"),
                walkable=tile_data.get("type", "CORRIDOR") != "VOID",
                description=tile_data.get("description", "")
            )
            self.tiles[(x, y, z)] = tile

        # Load NPC spawn positions
        for npc_id, spawn_data in map_data.get("npc_spawns", {}).items():
            x, y, z = spawn_data.get("x"), spawn_data.get("y"), spawn_data.get("z", 0)
            self.npc_positions[npc_id] = (x, y, z)

    def get_tile(self, x: int, y: int, z: int = 0) -> Optional[Tile]:
        """Get tile at coordinates, or None if out of bounds"""
        if (x, y, z) in self.tiles:
            return self.tiles[(x, y, z)]
        return None

    def is_walkable(self, x: int, y: int, z: int = 0) -> bool:
        """Check if a tile is walkable"""
        tile = self.get_tile(x, y, z)
        if tile is None:
            return False
        return tile.walkable

    def get_direction_offset(self, direction: Direction) -> Tuple[int, int]:
        """Get x, y offset for a direction"""
        offsets = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0),
        }
        return offsets[direction]

    def move_player(self, direction: Direction) -> bool:
        """
        Move the player in a direction.
        Returns True if move succeeded, False if blocked.
        """
        dx, dy = self.get_direction_offset(direction)
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        new_z = self.player.z

        # Check bounds
        if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height:
            return False

        # Check walkability
        if not self.is_walkable(new_x, new_y, new_z):
            return False

        # Move succeeded
        self.player.x = new_x
        self.player.y = new_y
        self.player.visited_tiles.add((new_x, new_y, new_z))
        return True

    def turn_player(self, direction: Direction):
        """Rotate player to face a direction"""
        self.player.facing = direction

    def rotate_player_left(self):
        """Turn 90 degrees left (counter-clockwise)"""
        current = self.player.facing.value
        self.player.facing = Direction((current - 1) % 4)

    def rotate_player_right(self):
        """Turn 90 degrees right (clockwise)"""
        current = self.player.facing.value
        self.player.facing = Direction((current + 1) % 4)

    def get_player_tile(self) -> Tile:
        """Get the tile the player is currently on"""
        return self.get_tile(self.player.x, self.player.y, self.player.z)

    def add_artifact_to_location(self, artifact_id: str, x: int, y: int, z: int = 0):
        """Place an artifact at a tile"""
        self.artifact_locations[artifact_id] = (x, y, z)

    def get_artifact_at_location(self, x: int, y: int, z: int = 0) -> Optional[str]:
        """Get artifact ID at a location, if any"""
        for artifact_id, (ax, ay, az) in self.artifact_locations.items():
            if ax == x and ay == y and az == z:
                return artifact_id
        return None

    def pickup_artifact(self, artifact_id: str) -> bool:
        """
        Pick up an artifact.
        Returns True if successful, False if not found.
        """
        if artifact_id not in self.artifact_locations:
            return False

        x, y, z = self.artifact_locations[artifact_id]
        if x == self.player.x and y == self.player.y and z == self.player.z:
            self.player.inventory.append(artifact_id)
            del self.artifact_locations[artifact_id]
            return True
        return False

    def get_player_inventory(self) -> List[str]:
        """Get player's inventory"""
        return self.player.inventory

    def get_player_position(self) -> Tuple[int, int, int]:
        """Get player's position"""
        return (self.player.x, self.player.y, self.player.z)

    def get_player_facing(self) -> Direction:
        """Get player's facing direction"""
        return self.player.facing

    def is_at_entrance(self) -> bool:
        """Check if player is at the mall entrance"""
        tile = self.get_player_tile()
        return tile is not None and tile.type == "ENTRANCE"

    def update_playtime(self, delta_seconds: int):
        """Update playtime counter"""
        self.player.playtime_seconds += delta_seconds

    def get_playtime(self) -> int:
        """Get elapsed playtime in seconds"""
        return self.player.playtime_seconds

    def get_tiles_by_type(self, tile_type: str) -> List[Tile]:
        """Get all tiles of a specific type"""
        return [tile for tile in self.tiles.values() if tile.type == tile_type]

    def get_nearby_tiles(self, x: int, y: int, radius: int = 3) -> List[Tile]:
        """Get all walkable tiles within radius of a position"""
        nearby = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                tile = self.get_tile(nx, ny)
                if tile and tile.walkable:
                    nearby.append(tile)
        return nearby

    def get_line_of_sight(self, x1: int, y1: int, x2: int, y2: int) -> List[Tuple[int, int]]:
        """
        Simple Bresenham line of sight between two points.
        Returns list of coordinates along the line.
        """
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x2 > x1 else -1
        sy = 1 if y2 > y1 else -1
        err = dx - dy

        x, y = x1, y1
        while True:
            points.append((x, y))
            if x == x2 and y == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

        return points

    def can_see(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        """Check if there's a clear line of sight between two points"""
        los = self.get_line_of_sight(x1, y1, x2, y2)
        for x, y in los:
            if not self.is_walkable(x, y):
                return False
        return True

    def record_interaction(self, npc_id: str):
        """Record that player has interacted with an NPC"""
        if npc_id not in self.player.interacted_npcs:
            self.player.interacted_npcs[npc_id] = 0
        self.player.interacted_npcs[npc_id] += 1

    def get_interaction_count(self, npc_id: str) -> int:
        """Get number of times player has interacted with an NPC"""
        return self.player.interacted_npcs.get(npc_id, 0)

    def save_state(self) -> Dict[str, Any]:
        """Serialize game state to dict"""
        return {
            "player": {
                "x": self.player.x,
                "y": self.player.y,
                "z": self.player.z,
                "facing": self.player.facing.name,
                "inventory": self.player.inventory,
                "playtime_seconds": self.player.playtime_seconds,
            },
            "visited_tiles": list(self.player.visited_tiles),
            "interacted_npcs": self.player.interacted_npcs,
        }

    def load_state(self, state: Dict[str, Any]):
        """Deserialize game state from dict"""
        p = state.get("player", {})
        self.player.x = p.get("x", 0)
        self.player.y = p.get("y", 24)
        self.player.z = p.get("z", 0)
        self.player.facing = Direction[p.get("facing", "EAST")]
        self.player.inventory = p.get("inventory", [])
        self.player.playtime_seconds = p.get("playtime_seconds", 0)
        self.player.visited_tiles = set(state.get("visited_tiles", []))
        self.player.interacted_npcs = state.get("interacted_npcs", {})
