"""
V2 WORLD LOADER
Loads JSON data files and creates the game world for MallSimulation
"""

import json
import os
from typing import Dict, List, Tuple, Any


class Tile:
    """Simple tile object"""
    def __init__(self, tile_type: str, description: str = ""):
        self.type = tile_type
        self.description = description
        self.walkable = tile_type not in ["VOID", "WALL"]


class WorldGrid:
    """Represents the mall's physical layout"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles: Dict[Tuple[int, int], Tile] = {}  # (x, y) -> tile object
        self.spawn_points: Dict[str, List[Tuple[int, int]]] = {}  # tile_type -> positions

    def add_tile(self, x: int, y: int, tile_type: str, description: str = ""):
        """Add a tile to the grid"""
        self.tiles[(x, y)] = Tile(tile_type, description)

        # Track spawn points for this tile type
        if tile_type not in self.spawn_points:
            self.spawn_points[tile_type] = []
        self.spawn_points[tile_type].append((x, y))

    def is_walkable(self, x: int, y: int) -> bool:
        """Check if a position is walkable"""
        tile = self.tiles.get((x, y))
        if not tile:
            return False
        return tile.walkable

    def get_random_position(self, tile_type: str = None) -> Tuple[int, int]:
        """Get a random walkable position, optionally filtered by tile type"""
        import random

        if tile_type and tile_type in self.spawn_points:
            positions = self.spawn_points[tile_type]
            if positions:
                return random.choice(positions)

        # Fall back to any walkable tile
        walkable = [(x, y) for (x, y), tile in self.tiles.items() if tile.walkable]
        if walkable:
            return random.choice(walkable)

        return (25, 25)  # Default center position


class WorldLoader:
    """Loads world data from JSON files"""

    def __init__(self, data_dir: str = None):
        """Initialize loader with data directory"""
        if data_dir is None:
            # Default to ../data relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(os.path.dirname(current_dir), "data")

        self.data_dir = data_dir
        self.world_grid = None
        self.npcs = []
        self.stores = []
        self.artifacts = []

    def load_all(self) -> Dict[str, Any]:
        """Load all world data and return configuration dict"""
        self._load_map()
        self._load_entities()
        self._load_stores()
        self._load_artifacts()

        return {
            "world_grid": self.world_grid,
            "npcs": self.npcs,
            "stores": self.stores,
            "artifacts": self.artifacts
        }

    def _load_json(self, filename: str) -> Dict:
        """Load a JSON file from data directory"""
        path = os.path.join(self.data_dir, filename)
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[WORLD_LOADER] Warning: {filename} not found")
            return {}
        except json.JSONDecodeError as e:
            print(f"[WORLD_LOADER] Error parsing {filename}: {e}")
            return {}

    def _load_map(self):
        """Load mall_map.json and create WorldGrid"""
        data = self._load_json("mall_map.json")

        width = data.get("width", 50)
        height = data.get("height", 50)
        self.world_grid = WorldGrid(width, height)

        # Add all defined tiles
        for tile_data in data.get("tiles", []):
            x = tile_data.get("x", 0)
            y = tile_data.get("y", 0)
            tile_type = tile_data.get("type", "VOID")
            description = tile_data.get("description", "")

            self.world_grid.add_tile(x, y, tile_type, description)

        print(f"[WORLD_LOADER] Loaded map: {width}x{height} with {len(self.world_grid.tiles)} tiles")

    def _load_entities(self):
        """Load entities.json (NPCs)"""
        data = self._load_json("entities.json")

        for npc_data in data.get("npcs", []):
            # Determine spawn position
            spawn_tile_type = npc_data.get("spawn_tile", "CORRIDOR")
            x, y = self.world_grid.get_random_position(spawn_tile_type)

            npc = {
                "id": npc_data.get("id", "unknown"),
                "name": npc_data.get("name", "NPC"),
                "title": npc_data.get("title", ""),
                "description": npc_data.get("description", ""),
                "faction": self._determine_faction(npc_data),
                "position": (x, y),
                "behavior": npc_data.get("behavior", "wander"),
                "dialogue": npc_data.get("dialogue", {}),
                "personality": self._generate_personality(npc_data)
            }

            self.npcs.append(npc)

        print(f"[WORLD_LOADER] Loaded {len(self.npcs)} NPCs")

    def _determine_faction(self, npc_data: Dict) -> str:
        """Determine NPC faction from their data"""
        title = npc_data.get("title", "").lower()
        behavior = npc_data.get("behavior", "").lower()

        if "security" in title or "guard" in title:
            return "security"
        elif "worker" in title or "employee" in title or "optician" in title or "operator" in title:
            return "workers"
        elif "teen" in title or "kid" in title or npc_data.get("name") == "BORED":
            return "teens"
        elif "manager" in title or "management" in title:
            return "management"
        elif "janitor" in title or "custodian" in title:
            return "janitors"
        else:
            return "shoppers"

    def _generate_personality(self, npc_data: Dict) -> Dict[str, float]:
        """Generate personality traits for NPC"""
        import random

        # Default personalities
        personality = {
            "aggression": random.uniform(0.2, 0.5),
            "bravery": random.uniform(0.3, 0.7),
            "curiosity": random.uniform(0.4, 0.8),
            "sociability": random.uniform(0.3, 0.7)
        }

        # Adjust based on faction
        title = npc_data.get("title", "").lower()
        if "security" in title:
            personality["aggression"] = random.uniform(0.6, 0.9)
            personality["bravery"] = random.uniform(0.7, 0.9)
        elif "teen" in title:
            personality["aggression"] = random.uniform(0.1, 0.3)
            personality["bravery"] = random.uniform(0.2, 0.4)
            personality["curiosity"] = random.uniform(0.7, 0.9)

        return personality

    def _load_stores(self):
        """Load stores.json"""
        data = self._load_json("stores.json")

        for store_data in data.get("stores", []):
            store = {
                "id": store_data.get("id", "unknown"),
                "name": store_data.get("name", "Store"),
                "theme": store_data.get("theme", "generic"),
                "hours": store_data.get("hours", "10:00-21:00"),
                "tile_type": store_data.get("tile_type", "STORE_GENERIC")
            }

            self.stores.append(store)

        print(f"[WORLD_LOADER] Loaded {len(self.stores)} stores")

    def _load_artifacts(self):
        """Load artifacts.json"""
        data = self._load_json("artifacts.json")

        for artifact_data in data.get("artifacts", []):
            # Place artifact at random location
            x, y = self.world_grid.get_random_position("CORRIDOR")

            artifact = {
                "id": artifact_data.get("id", "unknown"),
                "name": artifact_data.get("name", "Artifact"),
                "description": artifact_data.get("description", ""),
                "lore": artifact_data.get("lore", ""),
                "position": (x, y),
                "found": False
            }

            self.artifacts.append(artifact)

        print(f"[WORLD_LOADER] Loaded {len(self.artifacts)} artifacts")


def create_world_config() -> Dict[str, Any]:
    """
    Convenience function to load all world data
    Returns config dict ready for MallSimulation
    """
    loader = WorldLoader()
    return loader.load_all()


# Test function
if __name__ == "__main__":
    print("=" * 70)
    print("  V2 WORLD LOADER TEST")
    print("=" * 70)
    print()

    config = create_world_config()

    print()
    print("World Grid:")
    print(f"  Size: {config['world_grid'].width}x{config['world_grid'].height}")
    print(f"  Tiles: {len(config['world_grid'].tiles)}")
    print(f"  Tile types: {len(config['world_grid'].spawn_points)}")

    print()
    print("NPCs:")
    for npc in config["npcs"][:5]:
        print(f"  - {npc['name']} ({npc['faction']}) at {npc['position']}")

    print()
    print("Stores:")
    for store in config["stores"][:5]:
        print(f"  - {store['name']} ({store['theme']})")

    print()
    print("Artifacts:")
    for artifact in config["artifacts"][:5]:
        print(f"  - {artifact['name']} at {artifact['position']}")

    print()
    print("✅ World data loaded successfully!")
