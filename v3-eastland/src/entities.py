"""
Entities System – NPCs, Artifacts, Behaviors
"""

import json
import os
import random
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class NPCBehavior(Enum):
    """NPC behavior types"""
    STAY_PUT = "stay_put"
    WANDER_TO_FOOD_COURT = "wander_to_food_court"
    PATROL = "patrol"
    IDLE_WANDER = "idle_wander"


@dataclass
class NPC:
    """Represents an NPC in the mall"""
    id: str
    name: str
    title: str
    description: str
    spawn_x: int
    spawn_y: int
    spawn_z: int = 0
    current_x: int = None
    current_y: int = None
    current_z: int = None
    behavior: NPCBehavior = NPCBehavior.STAY_PUT
    patrol_route: List[str] = None
    dialogue: Dict[str, Any] = None
    merchandise_lines: List[str] = None
    logging: bool = False

    def __post_init__(self):
        """Initialize current position to spawn position"""
        if self.current_x is None:
            self.current_x = self.spawn_x
        if self.current_y is None:
            self.current_y = self.spawn_y
        if self.current_z is None:
            self.current_z = self.spawn_z
        if self.dialogue is None:
            self.dialogue = {}
        if self.merchandise_lines is None:
            self.merchandise_lines = []


@dataclass
class Artifact:
    """Represents an artifact/item in the mall"""
    id: str
    name: str
    description: str
    found_location: str
    weirdness_level: int = 1
    milo_lore: str = ""
    visual_effect: str = ""


class ArtifactSystem:
    """Manages artifacts and their properties"""

    def __init__(self, artifact_file: str = None):
        """Load artifacts from JSON"""
        self.artifacts: Dict[str, Artifact] = {}

        if artifact_file is None:
            artifact_file = os.path.join(os.path.dirname(__file__), "../data/artifacts.json")

        self.load_artifacts(artifact_file)

    def load_artifacts(self, artifact_file: str):
        """Load artifact definitions from JSON"""
        with open(artifact_file, 'r') as f:
            data = json.load(f)

        for artifact_data in data.get("artifacts", []):
            artifact = Artifact(
                id=artifact_data.get("id"),
                name=artifact_data.get("name"),
                description=artifact_data.get("description"),
                found_location=artifact_data.get("found_location"),
                weirdness_level=artifact_data.get("weirdness_level", 1),
                milo_lore=artifact_data.get("milo_lore", ""),
                visual_effect=artifact_data.get("visual_effect", "")
            )
            self.artifacts[artifact.id] = artifact

    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """Get artifact by ID"""
        return self.artifacts.get(artifact_id)

    def get_lore(self, artifact_id: str) -> str:
        """Get Milo's lore for an artifact"""
        artifact = self.get_artifact(artifact_id)
        if artifact:
            return artifact.milo_lore
        return "I don't know what that is."

    def get_weirdness_level(self, artifact_id: str) -> int:
        """Get weirdness level for an artifact"""
        artifact = self.get_artifact(artifact_id)
        if artifact:
            return artifact.weirdness_level
        return 0

    def get_all_artifact_ids(self) -> List[str]:
        """Get all artifact IDs"""
        return list(self.artifacts.keys())


class NPCSystem:
    """Manages NPCs and their behaviors"""

    def __init__(self, entity_file: str = None):
        """Load NPCs from JSON"""
        self.npcs: Dict[str, NPC] = {}
        self.event_log: List[str] = []

        if entity_file is None:
            entity_file = os.path.join(os.path.dirname(__file__), "../data/entities.json")

        self.load_entities(entity_file)

    def load_entities(self, entity_file: str):
        """Load NPC definitions from JSON"""
        with open(entity_file, 'r') as f:
            data = json.load(f)

        for npc_data in data.get("npcs", []):
            npc = NPC(
                id=npc_data.get("id"),
                name=npc_data.get("name"),
                title=npc_data.get("title"),
                description=npc_data.get("description"),
                spawn_x=npc_data.get("spawn_x", 0),
                spawn_y=npc_data.get("spawn_y", 0),
                spawn_z=npc_data.get("spawn_z", 0),
                behavior=NPCBehavior(npc_data.get("behavior", "stay_put")),
                patrol_route=npc_data.get("patrol_route"),
                dialogue=npc_data.get("dialogue", {}),
                merchandise_lines=npc_data.get("merchandise_lines", []),
                logging=npc_data.get("logging", False)
            )
            self.npcs[npc.id] = npc

    def get_npc(self, npc_id: str) -> Optional[NPC]:
        """Get NPC by ID"""
        return self.npcs.get(npc_id)

    def get_all_npcs(self) -> List[NPC]:
        """Get all NPCs"""
        return list(self.npcs.values())

    def get_npc_at_location(self, x: int, y: int, z: int = 0) -> Optional[NPC]:
        """Get NPC at a specific location"""
        for npc in self.npcs.values():
            if npc.current_x == x and npc.current_y == y and npc.current_z == z:
                return npc
        return None

    def move_npc(self, npc_id: str, new_x: int, new_y: int, new_z: int = 0) -> bool:
        """Move an NPC to a new location"""
        npc = self.get_npc(npc_id)
        if npc is None:
            return False
        npc.current_x = new_x
        npc.current_y = new_y
        npc.current_z = new_z
        return True

    def reset_npc_position(self, npc_id: str):
        """Reset NPC to spawn location"""
        npc = self.get_npc(npc_id)
        if npc:
            npc.current_x = npc.spawn_x
            npc.current_y = npc.spawn_y
            npc.current_z = npc.spawn_z

    def get_dialogue(self, npc_id: str, dialogue_key: str) -> str:
        """Get dialogue line from NPC"""
        npc = self.get_npc(npc_id)
        if npc is None:
            return "..."

        dialogue_data = npc.dialogue.get(dialogue_key)
        if dialogue_data is None:
            return "..."

        if isinstance(dialogue_data, str):
            return dialogue_data
        elif isinstance(dialogue_data, list):
            return random.choice(dialogue_data)
        else:
            return str(dialogue_data)

    def get_merchandise_line(self, npc_id: str) -> str:
        """Get a random merchandise line from NPC"""
        npc = self.get_npc(npc_id)
        if npc is None or not npc.merchandise_lines:
            return "..."
        return random.choice(npc.merchandise_lines)

    def log_event(self, event: str):
        """Log an event to the event log"""
        self.event_log.append(event)

    def get_event_log(self) -> List[str]:
        """Get all logged events"""
        return self.event_log

    def update_npc_positions(self, engine, toddler_stage: int):
        """
        Update NPC positions based on their behaviors.
        Called once per game tick.
        """
        for npc_id, npc in self.npcs.items():
            if npc.behavior == NPCBehavior.STAY_PUT:
                # Stay at spawn location
                pass
            elif npc.behavior == NPCBehavior.PATROL:
                # Simple patrol: move randomly in walkable tiles
                nearby_tiles = engine.get_nearby_tiles(npc.current_x, npc.current_y, radius=2)
                if nearby_tiles and random.random() < 0.3:
                    tile = random.choice(nearby_tiles)
                    npc.current_x = tile.x
                    npc.current_y = tile.y
                    npc.current_z = tile.z

                    # Log if this NPC logs events
                    if npc.logging:
                        self.log_event(
                            f"[{npc.name}] moved to ({tile.x}, {tile.y})"
                        )
            elif npc.behavior == NPCBehavior.IDLE_WANDER:
                # Occasionally wander
                if random.random() < 0.2:
                    nearby_tiles = engine.get_nearby_tiles(npc.current_x, npc.current_y, radius=3)
                    if nearby_tiles:
                        tile = random.choice(nearby_tiles)
                        npc.current_x = tile.x
                        npc.current_y = tile.y
                        npc.current_z = tile.z

    def get_npc_reaction_to_stage(self, npc_id: str, stage: int) -> Optional[str]:
        """Get NPC's dialogue for a specific toddler stage"""
        dialogue_key = f"stage_{stage}"
        dialogue_data = self.get_dialogue(npc_id, dialogue_key)
        if dialogue_data == "...":
            return None
        return dialogue_data

    def get_nearby_npcs(self, x: int, y: int, z: int = 0, radius: int = 5) -> List[NPC]:
        """Get all NPCs within a radius"""
        nearby = []
        for npc in self.npcs.values():
            dx = abs(npc.current_x - x)
            dy = abs(npc.current_y - y)
            dz = abs(npc.current_z - z)
            if max(dx, dy, dz) <= radius:
                nearby.append(npc)
        return nearby
