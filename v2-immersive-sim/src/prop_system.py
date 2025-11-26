"""
INTERACTIVE PROP SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

25+ interactive props with physics, combos, and emergent behavior.

Immersive sim-style environmental interaction:
- Vending machines make noise, drop items
- Arcade cabinets distract NPCs
- Security panels trigger alarms
- Props interact with each other (chain reactions)
- Everything feeds into heat and stealth systems

Think Deus Ex / Dishonored object interaction...
...but it's all ASCII sprites.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import time
import random
from typing import Dict, List, Tuple, Set, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum


class PropType(Enum):
    """Types of interactive props"""
    # Distraction props
    VENDING_MACHINE = "vending_machine"
    ARCADE_CABINET = "arcade_cabinet"
    RADIO = "radio"
    TV = "tv"
    PHONE = "phone"

    # Security props
    SECURITY_CAMERA = "security_camera"
    ALARM_PANEL = "alarm_panel"
    DOOR_LOCK = "door_lock"
    SHUTTER = "shutter"

    # Destructible props
    PLANT_POT = "plant_pot"
    TRASH_CAN = "trash_can"
    DISPLAY_STAND = "display_stand"
    GLASS_DOOR = "glass_door"
    WINDOW = "window"

    # Containers
    LOCKER = "locker"
    CASH_REGISTER = "cash_register"
    STORAGE_BOX = "storage_box"

    # Furniture
    BENCH = "bench"
    TABLE = "table"
    KIOSK = "kiosk"

    # Interactive
    ESCALATOR = "escalator"
    ELEVATOR = "elevator"
    WATER_FOUNTAIN = "water_fountain"
    ATM = "atm"
    PAYPHONE = "payphone"


class PropState(Enum):
    """State of a prop"""
    INTACT = "intact"
    ACTIVATED = "activated"
    BROKEN = "broken"
    OPEN = "open"
    CLOSED = "closed"
    LOCKED = "locked"
    ON = "on"
    OFF = "off"


@dataclass
class PropInteraction:
    """An interaction available on a prop"""
    name: str  # "kick", "use", "break", "hack"
    requirements: Dict[str, Any]  # What's needed to do this
    effects: List[str]  # What happens
    cooldown: float = 0.0  # Seconds before can be used again


@dataclass
class Prop:
    """An interactive object in the world"""
    id: str
    prop_type: PropType
    position: Tuple[int, int, int]
    state: PropState = PropState.INTACT

    # Interaction data
    interactions: List[PropInteraction] = field(default_factory=list)
    last_interaction_time: float = 0.0

    # Physics
    can_be_moved: bool = False
    can_be_destroyed: bool = False
    health: float = 100.0

    # Effects
    produces_noise: bool = False
    noise_radius: float = 0.0
    blocks_movement: bool = False
    blocks_vision: bool = False

    # State data
    contains_items: List[str] = field(default_factory=list)
    is_powered: bool = True


class PropSystem:
    """
    Manages all interactive props in the world.

    This creates immersive sim-style environmental storytelling
    and emergent gameplay... rendered as ASCII.
    """

    def __init__(self):
        self.props: Dict[str, Prop] = {}
        self.prop_templates = self._init_prop_templates()

        # Active effects
        self.active_noises: List[Tuple[Tuple[int, int, int], float, float]] = []  # (pos, radius, timestamp)
        self.triggered_alarms: Set[str] = set()

    def _init_prop_templates(self) -> Dict[PropType, Dict[str, Any]]:
        """Initialize templates for each prop type"""
        return {
            PropType.VENDING_MACHINE: {
                "interactions": [
                    PropInteraction(
                        "use",
                        requirements={},
                        effects=["dispense_item", "make_noise"],
                        cooldown=5.0
                    ),
                    PropInteraction(
                        "kick",
                        requirements={},
                        effects=["make_loud_noise", "chance_dispense", "add_heat"],
                        cooldown=2.0
                    ),
                    PropInteraction(
                        "break",
                        requirements={},
                        effects=["make_loud_noise", "dispense_all", "add_major_heat", "destroy"],
                        cooldown=0.0
                    )
                ],
                "can_be_destroyed": True,
                "health": 50.0,
                "produces_noise": True,
                "noise_radius": 8.0,
                "blocks_movement": True,
                "contains_items": ["soda", "chips", "candy"]
            },

            PropType.ARCADE_CABINET: {
                "interactions": [
                    PropInteraction(
                        "play",
                        requirements={},
                        effects=["distract_nearby_npcs", "make_beeping_noise"],
                        cooldown=10.0
                    ),
                    PropInteraction(
                        "break",
                        requirements={},
                        effects=["loud_glass_break", "add_heat", "destroy"],
                        cooldown=0.0
                    )
                ],
                "can_be_destroyed": True,
                "health": 40.0,
                "produces_noise": True,
                "noise_radius": 6.0,
                "blocks_movement": True
            },

            PropType.SECURITY_CAMERA: {
                "interactions": [
                    PropInteraction(
                        "disable",
                        requirements={"has_tool": True},
                        effects=["camera_offline", "reduce_heat"],
                        cooldown=0.0
                    ),
                    PropInteraction(
                        "break",
                        requirements={},
                        effects=["camera_offline", "trigger_alarm", "add_major_heat"],
                        cooldown=0.0
                    )
                ],
                "can_be_destroyed": True,
                "health": 20.0,
                "blocks_vision": False
            },

            PropType.ALARM_PANEL: {
                "interactions": [
                    PropInteraction(
                        "trigger",
                        requirements={},
                        effects=["sound_alarm", "lockdown", "massive_heat"],
                        cooldown=0.0
                    ),
                    PropInteraction(
                        "hack",
                        requirements={"has_keycard": True},
                        effects=["disable_alarms", "clear_some_heat"],
                        cooldown=0.0
                    )
                ],
                "can_be_destroyed": False,
                "produces_noise": True,
                "noise_radius": 40.0
            },

            PropType.GLASS_DOOR: {
                "interactions": [
                    PropInteraction(
                        "open",
                        requirements={},
                        effects=["door_opens"],
                        cooldown=1.0
                    ),
                    PropInteraction(
                        "break",
                        requirements={},
                        effects=["glass_shatter_noise", "door_destroyed", "add_heat"],
                        cooldown=0.0
                    )
                ],
                "can_be_destroyed": True,
                "health": 15.0,
                "blocks_movement": True,
                "blocks_vision": True,
                "produces_noise": True,
                "noise_radius": 12.0
            },

            PropType.PLANT_POT: {
                "interactions": [
                    PropInteraction(
                        "knock_over",
                        requirements={},
                        effects=["crash_noise", "create_obstacle"],
                        cooldown=0.0
                    ),
                    PropInteraction(
                        "throw",
                        requirements={},
                        effects=["crash_noise", "distraction", "add_minor_heat"],
                        cooldown=0.0
                    )
                ],
                "can_be_moved": True,
                "can_be_destroyed": True,
                "health": 10.0,
                "produces_noise": True,
                "noise_radius": 5.0
            },

            PropType.KIOSK: {
                "interactions": [
                    PropInteraction(
                        "hide_behind",
                        requirements={},
                        effects=["concealment"],
                        cooldown=0.0
                    ),
                    PropInteraction(
                        "topple",
                        requirements={},
                        effects=["loud_crash", "block_path", "add_heat"],
                        cooldown=0.0
                    )
                ],
                "can_be_destroyed": True,
                "health": 30.0,
                "blocks_vision": True,
                "blocks_movement": True
            },

            PropType.ESCALATOR: {
                "interactions": [
                    PropInteraction(
                        "ride",
                        requirements={},
                        effects=["move_to_other_floor"],
                        cooldown=5.0
                    ),
                    PropInteraction(
                        "emergency_stop",
                        requirements={},
                        effects=["stop_escalator", "trigger_alert"],
                        cooldown=0.0
                    )
                ],
                "can_be_destroyed": False,
                "is_powered": True
            },

            PropType.ATM: {
                "interactions": [
                    PropInteraction(
                        "use",
                        requirements={"has_card": True},
                        effects=["dispense_money"],
                        cooldown=10.0
                    ),
                    PropInteraction(
                        "vandalize",
                        requirements={},
                        effects=["trigger_alarm", "major_heat"],
                        cooldown=0.0
                    )
                ],
                "can_be_destroyed": True,
                "health": 100.0,
                "contains_items": ["cash"]
            },

            PropType.WATER_FOUNTAIN: {
                "interactions": [
                    PropInteraction(
                        "drink",
                        requirements={},
                        effects=["minor_noise"],
                        cooldown=2.0
                    ),
                    PropInteraction(
                        "break",
                        requirements={},
                        effects=["water_spray", "loud_noise", "create_hazard", "add_heat"],
                        cooldown=0.0
                    )
                ],
                "can_be_destroyed": True,
                "health": 25.0
            },

            PropType.TRASH_CAN: {
                "interactions": [
                    PropInteraction(
                        "hide_in",
                        requirements={},
                        effects=["concealment"],
                        cooldown=0.0
                    ),
                    PropInteraction(
                        "knock_over",
                        requirements={},
                        effects=["noise", "distraction"],
                        cooldown=0.0
                    ),
                    PropInteraction(
                        "light_on_fire",
                        requirements={"has_lighter": True},
                        effects=["fire", "massive_distraction", "major_heat", "evacuate_zone"],
                        cooldown=0.0
                    )
                ],
                "can_be_moved": True,
                "can_be_destroyed": True,
                "health": 15.0
            },

            # Add more prop templates...
        }

    def spawn_prop(self, prop_type: PropType, position: Tuple[int, int, int], prop_id: Optional[str] = None) -> Prop:
        """Spawn a prop from template"""
        if prop_id is None:
            prop_id = f"{prop_type.value}_{len(self.props)}"

        template = self.prop_templates.get(prop_type, {})

        prop = Prop(
            id=prop_id,
            prop_type=prop_type,
            position=position,
            state=PropState.INTACT if template.get("can_be_destroyed") else PropState.CLOSED,
            interactions=template.get("interactions", []),
            can_be_moved=template.get("can_be_moved", False),
            can_be_destroyed=template.get("can_be_destroyed", False),
            health=template.get("health", 100.0),
            produces_noise=template.get("produces_noise", False),
            noise_radius=template.get("noise_radius", 0.0),
            blocks_movement=template.get("blocks_movement", False),
            blocks_vision=template.get("blocks_vision", False),
            contains_items=list(template.get("contains_items", [])),
            is_powered=template.get("is_powered", True)
        )

        self.props[prop_id] = prop
        return prop

    def interact_with_prop(self, prop_id: str, interaction_name: str, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform an interaction with a prop.

        Returns dict of effects that occurred.
        """
        if prop_id not in self.props:
            return {"success": False, "reason": "prop_not_found"}

        prop = self.props[prop_id]

        # Find interaction
        interaction = None
        for inter in prop.interactions:
            if inter.name == interaction_name:
                interaction = inter
                break

        if not interaction:
            return {"success": False, "reason": "interaction_not_available"}

        # Check cooldown
        current_time = time.time()
        if current_time - prop.last_interaction_time < interaction.cooldown:
            return {"success": False, "reason": "on_cooldown"}

        # Check requirements
        for req_key, req_val in interaction.requirements.items():
            if not self._check_requirement(req_key, req_val, world_state):
                return {"success": False, "reason": f"missing_{req_key}"}

        # Execute effects
        results = self._execute_effects(prop, interaction.effects, world_state)

        prop.last_interaction_time = current_time

        return {"success": True, "effects": results}

    def _check_requirement(self, req_type: str, req_value: Any, world_state: Dict[str, Any]) -> bool:
        """Check if requirement is met"""
        if req_type == "has_tool":
            return world_state.get("player_has_tool", False)
        elif req_type == "has_keycard":
            return world_state.get("player_has_keycard", False)
        elif req_type == "has_card":
            return world_state.get("player_has_card", False)
        elif req_type == "has_lighter":
            return world_state.get("player_has_lighter", False)
        return True

    def _execute_effects(self, prop: Prop, effects: List[str], world_state: Dict[str, Any]) -> List[str]:
        """Execute prop interaction effects"""
        results = []

        for effect in effects:
            if effect == "make_noise":
                self.active_noises.append((prop.position, prop.noise_radius, time.time()))
                results.append("noise_created")

            elif effect == "make_loud_noise":
                self.active_noises.append((prop.position, prop.noise_radius * 1.5, time.time()))
                results.append("loud_noise_created")

            elif effect == "glass_shatter_noise":
                self.active_noises.append((prop.position, 12.0, time.time()))
                results.append("glass_shattered")

            elif effect == "dispense_item":
                if prop.contains_items:
                    item = random.choice(prop.contains_items)
                    results.append(f"received_{item}")

            elif effect == "distract_nearby_npcs":
                results.append("npcs_distracted")

            elif effect == "add_heat":
                results.append("heat_increased_minor")

            elif effect == "add_major_heat":
                results.append("heat_increased_major")

            elif effect == "add_minor_heat":
                results.append("heat_increased_tiny")

            elif effect == "trigger_alarm":
                self.triggered_alarms.add(prop.id)
                self.active_noises.append((prop.position, 40.0, time.time()))
                results.append("alarm_triggered")

            elif effect == "destroy":
                prop.state = PropState.BROKEN
                prop.blocks_movement = False
                results.append("prop_destroyed")

            elif effect == "fire":
                results.append("fire_started")

        return results

    def update(self, dt: float):
        """Update prop system"""
        current_time = time.time()

        # Clean up expired noise events
        self.active_noises = [
            (pos, radius, timestamp) for pos, radius, timestamp in self.active_noises
            if current_time - timestamp < 5.0  # Noises last 5 seconds
        ]

    def get_active_noises(self) -> List[Tuple[Tuple[int, int, int], float]]:
        """Get currently active noise sources"""
        return [(pos, radius) for pos, radius, _ in self.active_noises]

    def get_props_at_location(self, position: Tuple[int, int, int]) -> List[Prop]:
        """Get all props at a location"""
        return [prop for prop in self.props.values() if prop.position == position]

    def get_prop(self, prop_id: str) -> Optional[Prop]:
        """Get prop by ID"""
        return self.props.get(prop_id)

    def is_alarm_active(self) -> bool:
        """Check if any alarm is currently active"""
        return len(self.triggered_alarms) > 0

    def get_all_props(self) -> List[Prop]:
        """Get all props"""
        return list(self.props.values())
