"""
NPC INTELLIGENCE SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Individual NPC AI with:
- A* pathfinding with dynamic obstacle avoidance
- Personal memory and decision trees
- Behavior states and transitions
- Goal-oriented action planning (GOAP-lite)
- Individual schedules and routines

Each NPC is a tiny AI agent running a mini-simulation.
The player THINKS they're simple sprites. They're not.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import heapq
import time
import random
import math
from typing import Dict, List, Tuple, Set, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import deque, defaultdict


class NPCState(Enum):
    """High-level NPC behavior states"""
    IDLE = "idle"
    PATROLLING = "patrolling"
    WORKING = "working"
    SHOPPING = "shopping"
    INVESTIGATING = "investigating"
    PURSUING = "pursuing"
    FLEEING = "fleeing"
    CONVERSING = "conversing"
    PANICKING = "panicking"


class AwarenessLevel(Enum):
    """How aware the NPC is of the player"""
    UNAWARE = 0
    PERIPHERAL = 1  # Saw something in periphery
    NOTICED = 2  # Definitely saw player
    TRACKING = 3  # Actively following player
    COMBAT = 4  # Engaging player


@dataclass
class NPCMemory:
    """Individual NPC memory of an event"""
    timestamp: float
    memory_type: str  # "saw_player", "heard_noise", "saw_violence", etc.
    location: Tuple[int, int, int]
    target_id: Optional[str] = None  # Who/what this memory is about
    intensity: float = 0.5  # How strong the memory is
    details: Dict[str, Any] = field(default_factory=dict)

    def decay(self, current_time: float, decay_rate: float = 0.01) -> float:
        """Memory fades over time"""
        age = current_time - self.timestamp
        self.intensity = max(0.0, self.intensity - (age * decay_rate))
        return self.intensity


@dataclass
class NPCGoal:
    """Goal for GOAP-lite system"""
    goal_type: str
    priority: float  # 0.0 to 1.0
    target_location: Optional[Tuple[int, int, int]] = None
    target_npc: Optional[str] = None
    conditions: Dict[str, Any] = field(default_factory=dict)
    expiry_time: Optional[float] = None


@dataclass
class PathNode:
    """Node for A* pathfinding"""
    position: Tuple[int, int, int]
    g_cost: float  # Cost from start
    h_cost: float  # Heuristic cost to goal
    parent: Optional['PathNode'] = None

    @property
    def f_cost(self) -> float:
        return self.g_cost + self.h_cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost


class Pathfinder:
    """
    A* pathfinding with dynamic obstacle avoidance.

    This is legitimate game-quality pathfinding hidden under
    Wolf3D sprites that just slide around.
    """

    def __init__(self, world_tiles: Dict[Tuple[int, int, int], Any]):
        self.world_tiles = world_tiles
        self.cache: Dict[Tuple, List[Tuple[int, int, int]]] = {}
        self.cache_max_age = 5.0
        self.cache_timestamps: Dict[Tuple, float] = {}

    def find_path(self,
                  start: Tuple[int, int, int],
                  goal: Tuple[int, int, int],
                  dynamic_obstacles: Set[Tuple[int, int, int]] = None) -> List[Tuple[int, int, int]]:
        """
        A* pathfinding.
        Returns list of positions from start to goal.
        """
        if dynamic_obstacles is None:
            dynamic_obstacles = set()

        # Check cache
        cache_key = (start, goal, frozenset(dynamic_obstacles))
        if cache_key in self.cache:
            if time.time() - self.cache_timestamps[cache_key] < self.cache_max_age:
                return self.cache[cache_key]

        # A* algorithm
        open_set = []
        closed_set = set()

        start_node = PathNode(start, 0, self._heuristic(start, goal))
        heapq.heappush(open_set, start_node)

        nodes: Dict[Tuple[int, int, int], PathNode] = {start: start_node}

        max_iterations = 500  # Prevent infinite loops
        iterations = 0

        while open_set and iterations < max_iterations:
            iterations += 1

            current = heapq.heappop(open_set)

            if current.position == goal:
                # Reconstruct path
                path = self._reconstruct_path(current)
                self.cache[cache_key] = path
                self.cache_timestamps[cache_key] = time.time()
                return path

            closed_set.add(current.position)

            # Check neighbors
            for neighbor_pos in self._get_neighbors(current.position):
                if neighbor_pos in closed_set:
                    continue

                if not self._is_walkable(neighbor_pos, dynamic_obstacles):
                    continue

                tentative_g = current.g_cost + self._distance(current.position, neighbor_pos)

                if neighbor_pos not in nodes:
                    neighbor_node = PathNode(
                        neighbor_pos,
                        tentative_g,
                        self._heuristic(neighbor_pos, goal),
                        current
                    )
                    nodes[neighbor_pos] = neighbor_node
                    heapq.heappush(open_set, neighbor_node)
                elif tentative_g < nodes[neighbor_pos].g_cost:
                    # Better path found
                    neighbor_node = nodes[neighbor_pos]
                    neighbor_node.g_cost = tentative_g
                    neighbor_node.parent = current
                    heapq.heappush(open_set, neighbor_node)

        # No path found
        return []

    def _heuristic(self, a: Tuple[int, int, int], b: Tuple[int, int, int]) -> float:
        """Manhattan distance heuristic"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

    def _distance(self, a: Tuple[int, int, int], b: Tuple[int, int, int]) -> float:
        """Actual distance between adjacent cells"""
        return 1.0

    def _get_neighbors(self, pos: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        """Get walkable neighbors (4-directional)"""
        x, y, z = pos
        neighbors = [
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
        ]
        return neighbors

    def _is_walkable(self, pos: Tuple[int, int, int], dynamic_obstacles: Set[Tuple[int, int, int]]) -> bool:
        """Check if position is walkable"""
        if pos in dynamic_obstacles:
            return False

        if pos not in self.world_tiles:
            return False

        tile = self.world_tiles[pos]
        return tile.walkable

    def _reconstruct_path(self, node: PathNode) -> List[Tuple[int, int, int]]:
        """Reconstruct path from goal to start"""
        path = []
        current = node

        while current is not None:
            path.append(current.position)
            current = current.parent

        path.reverse()
        return path


class NPCAgent:
    """
    Individual NPC with sophisticated AI.

    This is the hidden engine - each NPC has:
    - Personal memory
    - Pathfinding
    - Goal-oriented behaviors
    - Awareness states
    - Individual personality

    But rendered as a simple Wolf3D sprite.
    """

    def __init__(self, npc_id: str, config: Dict[str, Any], pathfinder: Pathfinder):
        self.id = npc_id
        self.name = config.get("name", npc_id)

        # Position
        self.position = tuple(config.get("spawn_position", (0, 0, 0)))
        self.facing = 0.0  # Angle in degrees

        # Faction
        from faction_system import FactionID
        faction_str = config.get("faction", "shoppers")
        self.faction = FactionID(faction_str)

        # State
        self.state = NPCState.IDLE
        self.awareness = AwarenessLevel.UNAWARE
        self.state_timer = 0.0

        # Pathfinding
        self.pathfinder = pathfinder
        self.current_path: List[Tuple[int, int, int]] = []
        self.path_index = 0

        # Memory
        self.memories: deque = deque(maxlen=50)
        self.short_term_memory: List[NPCMemory] = []  # Last 5 seconds
        self.important_memories: List[NPCMemory] = []  # Never forget

        # Goals
        self.goals: List[NPCGoal] = []
        self.current_goal: Optional[NPCGoal] = None

        # Personality
        self.aggression = config.get("aggression", 0.5)
        self.curiosity = config.get("curiosity", 0.5)
        self.sociability = config.get("sociability", 0.5)
        self.bravery = config.get("bravery", 0.5)

        # Schedule
        self.schedule: List[Dict[str, Any]] = config.get("schedule", [])
        self.current_schedule_index = 0

        # Patrol route
        self.patrol_route: List[Tuple[int, int, int]] = config.get("patrol_route", [])
        self.patrol_index = 0

        # Player tracking
        self.last_known_player_position: Optional[Tuple[int, int, int]] = None
        self.time_since_saw_player = float('inf')
        self.player_threat_level = 0.0  # 0.0 to 1.0

        # Dialogue
        self.dialogue_lines: Dict[str, List[str]] = config.get("dialogue", {})
        self.in_conversation = False
        self.conversation_partner: Optional[str] = None

    def update(self, dt: float, world_state: Dict[str, Any]):
        """
        Update NPC AI.

        This is where the magic happens - sophisticated decision making
        rendered as simple sprite movement.
        """
        current_time = time.time()

        # Update state timer
        self.state_timer += dt

        # Decay memories
        self._decay_memories(current_time)

        # Update awareness
        self._update_awareness(world_state)

        # Process current schedule
        self._update_schedule(world_state.get("simulation_time", 0))

        # Select and pursue goals
        self._update_goals(current_time, world_state)

        # Execute current behavior
        self._execute_behavior(dt, world_state)

        # Update facing direction
        self._update_facing()

    def _decay_memories(self, current_time: float):
        """Fade old memories"""
        for memory in list(self.short_term_memory):
            if memory.decay(current_time) <= 0:
                self.short_term_memory.remove(memory)

    def _update_awareness(self, world_state: Dict[str, Any]):
        """Update awareness of player and environment"""
        player_pos = world_state.get("player_position")
        if not player_pos:
            self.time_since_saw_player += 0.1
            return

        # Check if player is visible (simplified - stealth system will handle full logic)
        distance = self._distance_to(player_pos)

        if distance < 3:  # Very close
            self.awareness = AwarenessLevel.NOTICED
            self.last_known_player_position = player_pos
            self.time_since_saw_player = 0
            self._create_memory("saw_player_close", player_pos, intensity=0.9)

        elif distance < 8:  # Medium distance
            if self.awareness.value >= AwarenessLevel.NOTICED.value:
                self.awareness = AwarenessLevel.TRACKING
                self.last_known_player_position = player_pos
                self.time_since_saw_player = 0
            else:
                self.awareness = AwarenessLevel.PERIPHERAL

        else:
            if self.time_since_saw_player > 10:
                self.awareness = AwarenessLevel.UNAWARE

    def _update_schedule(self, simulation_time: float):
        """Update based on schedule (e.g., patrol at 10am, break at noon)"""
        if not self.schedule:
            return

        # Find current schedule entry
        # (Simplified - could be much more sophisticated)
        hour = (simulation_time / 3600) % 24
        for i, entry in enumerate(self.schedule):
            if entry.get("hour", 0) <= hour < entry.get("hour", 0) + entry.get("duration", 1):
                if self.current_schedule_index != i:
                    self.current_schedule_index = i
                    self._switch_to_scheduled_activity(entry)
                break

    def _switch_to_scheduled_activity(self, schedule_entry: Dict[str, Any]):
        """Switch NPC to scheduled activity"""
        activity = schedule_entry.get("activity", "idle")

        if activity == "patrol":
            self.state = NPCState.PATROLLING
        elif activity == "work":
            self.state = NPCState.WORKING
        elif activity == "break":
            self.state = NPCState.IDLE
        elif activity == "shop":
            self.state = NPCState.SHOPPING

    def _update_goals(self, current_time: float, world_state: Dict[str, Any]):
        """
        Goal-oriented action planning (GOAP-lite).

        NPCs select goals based on:
        - Current state
        - Memories
        - Personality
        - Faction directives
        """
        # Remove expired goals
        self.goals = [g for g in self.goals if not g.expiry_time or current_time < g.expiry_time]

        # Generate new goals based on state
        if self.state == NPCState.IDLE and random.random() < 0.1:
            # Idle NPCs occasionally wander
            if self.sociability > 0.6 and random.random() < 0.3:
                self.goals.append(NPCGoal("socialize", priority=0.4, expiry_time=current_time + 60))
            else:
                self.goals.append(NPCGoal("wander", priority=0.3, expiry_time=current_time + 30))

        elif self.state == NPCState.INVESTIGATING:
            # Investigate suspicious activity
            if self.last_known_player_position:
                self.goals.append(NPCGoal(
                    "investigate_location",
                    priority=0.7,
                    target_location=self.last_known_player_position,
                    expiry_time=current_time + 45
                ))

        # Select highest priority goal
        if self.goals:
            self.goals.sort(key=lambda g: g.priority, reverse=True)
            self.current_goal = self.goals[0]
        else:
            self.current_goal = None

    def _execute_behavior(self, dt: float, world_state: Dict[str, Any]):
        """Execute current behavior state"""

        if self.state == NPCState.PATROLLING:
            self._behavior_patrol(dt)

        elif self.state == NPCState.INVESTIGATING:
            self._behavior_investigate(dt)

        elif self.state == NPCState.PURSUING:
            self._behavior_pursue(dt, world_state)

        elif self.state == NPCState.FLEEING:
            self._behavior_flee(dt, world_state)

        elif self.state == NPCState.IDLE:
            self._behavior_idle(dt)

        elif self.state == NPCState.WORKING:
            self._behavior_work(dt)

        elif self.state == NPCState.SHOPPING:
            self._behavior_shop(dt)

    def _behavior_patrol(self, dt: float):
        """Patrol along route"""
        if not self.patrol_route:
            return

        target = self.patrol_route[self.patrol_index]

        # Move towards target
        if self._move_towards(target, dt):
            # Reached waypoint
            self.patrol_index = (self.patrol_index + 1) % len(self.patrol_route)

    def _behavior_investigate(self, dt: float):
        """Investigate suspicious location"""
        if not self.last_known_player_position:
            self.state = NPCState.IDLE
            return

        # Move towards last known position
        if self._move_towards(self.last_known_player_position, dt):
            # Reached location
            self.state = NPCState.IDLE
            self.awareness = AwarenessLevel.PERIPHERAL

    def _behavior_pursue(self, dt: float, world_state: Dict[str, Any]):
        """Chase player"""
        player_pos = world_state.get("player_position")
        if not player_pos:
            self.state = NPCState.INVESTIGATING
            return

        self._move_towards(player_pos, dt)

    def _behavior_flee(self, dt: float, world_state: Dict[str, Any]):
        """Run away from player"""
        player_pos = world_state.get("player_position")
        if not player_pos:
            self.state = NPCState.IDLE
            return

        # Move in opposite direction
        dx = self.position[0] - player_pos[0]
        dy = self.position[1] - player_pos[1]

        # Normalize and scale
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx /= length
            dy /= length

        flee_target = (
            int(self.position[0] + dx * 10),
            int(self.position[1] + dy * 10),
            self.position[2]
        )

        self._move_towards(flee_target, dt)

    def _behavior_idle(self, dt: float):
        """Stand around, occasionally look around"""
        if random.random() < 0.05:
            self.facing = random.uniform(0, 360)

    def _behavior_work(self, dt: float):
        """Work at assigned location"""
        # Stay in place, face random directions occasionally
        if random.random() < 0.02:
            self.facing = random.uniform(0, 360)

    def _behavior_shop(self, dt: float):
        """Wander and "shop" """
        # Random walk
        if random.random() < 0.1:
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            target = (self.position[0] + dx, self.position[1] + dy, self.position[2])
            self._move_towards(target, dt)

    def _move_towards(self, target: Tuple[int, int, int], dt: float) -> bool:
        """
        Move towards target using pathfinding.
        Returns True when target reached.
        """
        # Check if we need a new path
        if not self.current_path or self.current_path[-1] != target:
            self.current_path = self.pathfinder.find_path(self.position, target)
            self.path_index = 0

        if not self.current_path:
            return False

        # Follow path
        if self.path_index < len(self.current_path):
            next_pos = self.current_path[self.path_index]

            # Move towards next position (simplified)
            if self.position != next_pos:
                self.position = next_pos
                self.path_index += 1
            else:
                self.path_index += 1

        # Check if reached target
        return self.position == target

    def _update_facing(self):
        """Update facing direction based on movement"""
        if len(self.current_path) > self.path_index:
            next_pos = self.current_path[self.path_index]
            dx = next_pos[0] - self.position[0]
            dy = next_pos[1] - self.position[1]

            if dx != 0 or dy != 0:
                self.facing = math.degrees(math.atan2(dy, dx))

    def _distance_to(self, position: Tuple[int, int, int]) -> float:
        """Calculate distance to position"""
        dx = position[0] - self.position[0]
        dy = position[1] - self.position[1]
        dz = position[2] - self.position[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def _create_memory(self, memory_type: str, location: Tuple[int, int, int], intensity: float = 0.5):
        """Create a new memory"""
        memory = NPCMemory(
            timestamp=time.time(),
            memory_type=memory_type,
            location=location,
            intensity=intensity
        )

        self.memories.append(memory)
        self.short_term_memory.append(memory)

        if intensity > 0.8:
            self.important_memories.append(memory)

    def get_state_info(self) -> Dict[str, Any]:
        """Get NPC state for rendering/debugging"""
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position,
            "facing": self.facing,
            "state": self.state.value,
            "awareness": self.awareness.value,
            "faction": self.faction.value
        }


class NPCManager:
    """
    Manages all NPCs in the simulation.

    Orchestrates hundreds of tiny AI agents while keeping
    performance acceptable.
    """

    def __init__(self, world_tiles: Dict[Tuple[int, int, int], Any]):
        self.npcs: Dict[str, NPCAgent] = {}
        self.pathfinder = Pathfinder(world_tiles)

        # Performance optimization
        self.update_batches = 3  # Update NPCs in batches
        self.current_batch = 0

    def spawn_npc(self, npc_id: str, config: Dict[str, Any]) -> NPCAgent:
        """Spawn a new NPC"""
        npc = NPCAgent(npc_id, config, self.pathfinder)
        self.npcs[npc_id] = npc
        return npc

    def update(self, dt: float, world_state: Dict[str, Any]):
        """Update all NPCs (batched for performance)"""
        npc_list = list(self.npcs.values())

        # Batch update for performance
        batch_size = len(npc_list) // self.update_batches
        if batch_size == 0:
            batch_size = len(npc_list)

        start_idx = self.current_batch * batch_size
        end_idx = min(start_idx + batch_size, len(npc_list))

        for npc in npc_list[start_idx:end_idx]:
            npc.update(dt, world_state)

        # Rotate batches
        self.current_batch = (self.current_batch + 1) % self.update_batches

    def get_npcs_in_range(self, position: Tuple[int, int, int], radius: float) -> List[NPCAgent]:
        """Get NPCs within range of position"""
        nearby = []
        for npc in self.npcs.values():
            dx = npc.position[0] - position[0]
            dy = npc.position[1] - position[1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist <= radius:
                nearby.append(npc)
        return nearby

    def get_npc(self, npc_id: str) -> Optional[NPCAgent]:
        """Get NPC by ID"""
        return self.npcs.get(npc_id)

    def get_all_npc_states(self) -> List[Dict[str, Any]]:
        """Get state of all NPCs for rendering"""
        return [npc.get_state_info() for npc in self.npcs.values()]
