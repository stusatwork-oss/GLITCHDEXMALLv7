"""
FACTION INTELLIGENCE SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complex faction AI with:
- Individual and collective memory
- Dynamic schedules and routines
- Emergent faction politics
- Reputation propagation
- Coordinated responses

This is cutting-edge 2025 AI simulation hiding under ANSI art.
Think Far Cry 6 faction AI but in a shopping mall.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import time
import random
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque


class FactionID(Enum):
    """Mall factions with distinct behaviors and politics"""
    MALL_SECURITY = "security"
    MALL_WORKERS = "workers"
    SHOPPERS = "shoppers"
    TEEN_MENACES = "teens"
    MANAGEMENT = "management"
    JANITORS = "janitors"
    TODDLER = "toddler"  # Special emergent agent


class FactionRelation(Enum):
    """Relationship states between factions"""
    ALLIED = 3
    FRIENDLY = 2
    NEUTRAL = 1
    SUSPICIOUS = 0
    HOSTILE = -1
    WAR = -2


class AlertLevel(Enum):
    """Faction-wide alert states"""
    CALM = 0
    AWARE = 1
    CONCERNED = 2
    ALERT = 3
    LOCKDOWN = 4


@dataclass
class FactionMemory:
    """Collective faction memory of player actions"""
    timestamp: float
    event_type: str  # "attack", "trespass", "theft", "chaos", "help"
    location: Tuple[int, int, int]
    severity: float  # 0.0 to 1.0
    witnesses: Set[str] = field(default_factory=set)  # NPC IDs who saw it
    propagated_to: Set[FactionID] = field(default_factory=set)


@dataclass
class FactionReputation:
    """Player's standing with a faction"""
    value: float = 0.0  # -100 to +100
    peak_value: float = 0.0  # Highest reputation ever (for "fall from grace" narratives)
    lowest_value: float = 0.0  # Lowest ever
    actions_count: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    last_interaction: float = 0.0

    def adjust(self, amount: float, action_type: str):
        """Adjust reputation and track the action"""
        self.value = max(-100.0, min(100.0, self.value + amount))
        self.peak_value = max(self.peak_value, self.value)
        self.lowest_value = min(self.lowest_value, self.value)
        self.actions_count[action_type] += 1
        self.last_interaction = time.time()


@dataclass
class FactionSchedule:
    """Time-based faction behavior patterns"""
    time_of_day: float  # 0.0 to 24.0 (simulated mall hours)
    activity: str  # "patrol", "break", "meeting", "rush_hour", "closing"
    zones: List[str]  # Which zones this faction focuses on during this activity
    intensity: float  # 0.0 to 1.0 - how actively they pursue their activity
    npc_count_modifier: float  # Multiplier for how many NPCs are active


class Faction:
    """
    Sophisticated faction with emergent behaviors.

    Each faction has:
    - Collective memory of player actions
    - Dynamic relationships with other factions
    - Schedule-based behavior patterns
    - Coordinated response capabilities
    """

    def __init__(self, faction_id: FactionID, config: Dict[str, Any]):
        self.id = faction_id
        self.name = config.get("name", faction_id.value)

        # Memory systems
        self.memory_buffer = deque(maxlen=100)  # Recent events
        self.critical_memories: List[FactionMemory] = []  # Never forget these

        # Relationships
        self.relations: Dict[FactionID, FactionRelation] = {}
        self.initialize_relations(config.get("default_relations", {}))

        # State
        self.alert_level = AlertLevel.CALM
        self.alert_timer = 0.0
        self.suspicion_map: Dict[Tuple[int, int, int], float] = {}  # Location -> suspicion

        # Schedule
        self.schedules: List[FactionSchedule] = []
        self.current_schedule: Optional[FactionSchedule] = None

        # Behavior config
        self.aggression = config.get("aggression", 0.5)  # 0.0 to 1.0
        self.memory_span = config.get("memory_span", 600)  # Seconds before forgetting
        self.gossip_rate = config.get("gossip_rate", 0.3)  # How fast info spreads
        self.coordination = config.get("coordination", 0.5)  # How well they work together

        # Zones of control
        self.controlled_zones: Set[str] = set(config.get("zones", []))
        self.patrol_routes: List[List[Tuple[int, int, int]]] = []

    def initialize_relations(self, default_relations: Dict[str, str]):
        """Set up initial faction relationships"""
        for faction_name, relation_str in default_relations.items():
            try:
                faction_id = FactionID(faction_name)
                relation = FactionRelation[relation_str.upper()]
                self.relations[faction_id] = relation
            except (ValueError, KeyError):
                pass

    def record_event(self, event: FactionMemory):
        """Record a player action in faction memory"""
        self.memory_buffer.append(event)

        # Critical events are never forgotten
        if event.severity >= 0.8:
            self.critical_memories.append(event)

        # Adjust alert level based on event
        self._update_alert_level(event)

        # Mark location as suspicious
        decay_time = 300 * (1.0 - event.severity)  # Higher severity = longer suspicion
        self.suspicion_map[event.location] = time.time() + decay_time

    def _update_alert_level(self, event: FactionMemory):
        """Escalate or de-escalate alert level based on events"""
        if event.event_type in ["attack", "chaos", "extreme_trespass"]:
            if event.severity > 0.8:
                self.alert_level = AlertLevel.LOCKDOWN
                self.alert_timer = 600  # 10 minutes
            elif event.severity > 0.5:
                self.alert_level = max(self.alert_level, AlertLevel.ALERT)
                self.alert_timer = 300
            elif event.severity > 0.3:
                self.alert_level = max(self.alert_level, AlertLevel.CONCERNED)
                self.alert_timer = 180

    def update(self, dt: float, current_time: float):
        """Update faction state"""
        # Decay alert level
        if self.alert_timer > 0:
            self.alert_timer -= dt
            if self.alert_timer <= 0:
                self._deescalate_alert()

        # Decay suspicion map
        expired_locations = []
        for location, expiry_time in self.suspicion_map.items():
            if current_time > expiry_time:
                expired_locations.append(location)
        for loc in expired_locations:
            del self.suspicion_map[loc]

        # Update current schedule based on time
        self._update_schedule(current_time)

    def _deescalate_alert(self):
        """Lower alert level by one step"""
        if self.alert_level == AlertLevel.LOCKDOWN:
            self.alert_level = AlertLevel.ALERT
            self.alert_timer = 120
        elif self.alert_level == AlertLevel.ALERT:
            self.alert_level = AlertLevel.CONCERNED
            self.alert_timer = 60
        elif self.alert_level == AlertLevel.CONCERNED:
            self.alert_level = AlertLevel.AWARE
            self.alert_timer = 30
        elif self.alert_level == AlertLevel.AWARE:
            self.alert_level = AlertLevel.CALM
            self.alert_timer = 0

    def _update_schedule(self, current_time: float):
        """Update current activity based on time of day"""
        if not self.schedules:
            return

        # Simple time mapping (could be made more sophisticated)
        time_of_day = (current_time / 60) % 24  # Convert to hours

        # Find matching schedule
        for schedule in self.schedules:
            if abs(schedule.time_of_day - time_of_day) < 1.0:  # Within 1 hour
                self.current_schedule = schedule
                break

    def get_relation_with(self, other_faction: FactionID) -> FactionRelation:
        """Get relationship status with another faction"""
        return self.relations.get(other_faction, FactionRelation.NEUTRAL)

    def modify_relation(self, other_faction: FactionID, change: int):
        """Change relationship with another faction (emergent politics)"""
        current = self.get_relation_with(other_faction)
        new_value = max(-2, min(3, current.value + change))

        # Find matching enum
        for relation in FactionRelation:
            if relation.value == new_value:
                self.relations[other_faction] = relation
                break

    def is_location_suspicious(self, location: Tuple[int, int, int], current_time: float) -> float:
        """Check if a location is under suspicion (0.0 to 1.0)"""
        if location in self.suspicion_map:
            expiry = self.suspicion_map[location]
            remaining = max(0, expiry - current_time)
            return min(1.0, remaining / 300.0)  # Normalize to 0-1
        return 0.0

    def get_active_npc_count(self) -> int:
        """How many NPCs should be active based on schedule and alert level"""
        base_count = 5

        if self.current_schedule:
            base_count = int(base_count * self.current_schedule.npc_count_modifier)

        # Alert level increases presence
        if self.alert_level == AlertLevel.LOCKDOWN:
            base_count *= 3
        elif self.alert_level == AlertLevel.ALERT:
            base_count *= 2
        elif self.alert_level == AlertLevel.CONCERNED:
            base_count = int(base_count * 1.5)

        return base_count

    def should_coordinate_with(self, other_faction: FactionID) -> bool:
        """Check if this faction will coordinate with another"""
        relation = self.get_relation_with(other_faction)

        if relation in [FactionRelation.ALLIED, FactionRelation.FRIENDLY]:
            return random.random() < self.coordination

        return False


class FactionSystem:
    """
    Central system managing all factions and their interactions.

    This creates emergent faction dynamics where:
    - Factions remember player actions
    - Relationships between factions evolve
    - Information propagates through gossip
    - Coordinated responses emerge naturally
    """

    def __init__(self):
        self.factions: Dict[FactionID, Faction] = {}
        self.player_reputation: Dict[FactionID, FactionReputation] = {}
        self.simulation_time: float = 0.0  # Mall time in seconds

        # Event propagation queue
        self.event_queue: deque = deque()

        self._initialize_factions()

    def _initialize_factions(self):
        """Initialize all mall factions with their configs"""

        # MALL SECURITY - Law enforcement
        self.factions[FactionID.MALL_SECURITY] = Faction(
            FactionID.MALL_SECURITY,
            {
                "name": "Mall Security",
                "aggression": 0.6,
                "memory_span": 900,  # 15 minutes
                "gossip_rate": 0.7,
                "coordination": 0.8,
                "zones": ["entrance", "corridors", "security_office"],
                "default_relations": {
                    "workers": "FRIENDLY",
                    "shoppers": "NEUTRAL",
                    "teens": "SUSPICIOUS",
                    "management": "ALLIED",
                    "janitors": "FRIENDLY"
                }
            }
        )

        # MALL WORKERS - Service staff
        self.factions[FactionID.MALL_WORKERS] = Faction(
            FactionID.MALL_WORKERS,
            {
                "name": "Mall Workers",
                "aggression": 0.2,
                "memory_span": 600,
                "gossip_rate": 0.9,  # Workers gossip the most!
                "coordination": 0.4,
                "zones": ["stores", "food_court", "kiosks"],
                "default_relations": {
                    "security": "FRIENDLY",
                    "shoppers": "FRIENDLY",
                    "teens": "NEUTRAL",
                    "management": "NEUTRAL",
                    "janitors": "FRIENDLY"
                }
            }
        )

        # SHOPPERS - Civilians
        self.factions[FactionID.SHOPPERS] = Faction(
            FactionID.SHOPPERS,
            {
                "name": "Shoppers",
                "aggression": 0.1,
                "memory_span": 300,
                "gossip_rate": 0.5,
                "coordination": 0.2,
                "zones": ["stores", "food_court", "corridors"],
                "default_relations": {
                    "security": "NEUTRAL",
                    "workers": "FRIENDLY",
                    "teens": "SUSPICIOUS",
                    "management": "NEUTRAL",
                    "janitors": "NEUTRAL"
                }
            }
        )

        # TEEN MENACES - Chaos agents
        self.factions[FactionID.TEEN_MENACES] = Faction(
            FactionID.TEEN_MENACES,
            {
                "name": "Teen Menaces",
                "aggression": 0.4,
                "memory_span": 180,  # Short attention span
                "gossip_rate": 0.8,
                "coordination": 0.3,
                "zones": ["arcade", "food_court", "entrance"],
                "default_relations": {
                    "security": "HOSTILE",
                    "workers": "SUSPICIOUS",
                    "shoppers": "NEUTRAL",
                    "management": "HOSTILE",
                    "janitors": "NEUTRAL"
                }
            }
        )

        # MANAGEMENT - Mall authority
        self.factions[FactionID.MANAGEMENT] = Faction(
            FactionID.MANAGEMENT,
            {
                "name": "Management",
                "aggression": 0.5,
                "memory_span": 1800,  # Long memory
                "gossip_rate": 0.6,
                "coordination": 0.9,
                "zones": ["offices", "security_office"],
                "default_relations": {
                    "security": "ALLIED",
                    "workers": "NEUTRAL",
                    "shoppers": "FRIENDLY",
                    "teens": "HOSTILE",
                    "janitors": "NEUTRAL"
                }
            }
        )

        # JANITORS - Maintenance crew
        self.factions[FactionID.JANITORS] = Faction(
            FactionID.JANITORS,
            {
                "name": "Janitors",
                "aggression": 0.3,
                "memory_span": 400,
                "gossip_rate": 0.6,
                "coordination": 0.5,
                "zones": ["service_halls", "restrooms", "corridors"],
                "default_relations": {
                    "security": "FRIENDLY",
                    "workers": "FRIENDLY",
                    "shoppers": "NEUTRAL",
                    "teens": "SUSPICIOUS",
                    "management": "NEUTRAL"
                }
            }
        )

        # Initialize reputations
        for faction_id in self.factions.keys():
            self.player_reputation[faction_id] = FactionReputation()

    def record_player_action(self,
                            action_type: str,
                            location: Tuple[int, int, int],
                            severity: float,
                            witnessed_by: Set[str],
                            affected_factions: Set[FactionID]):
        """
        Record a player action and propagate through faction memory.

        This is where the emergent behavior happens - factions remember,
        gossip, and coordinate responses.
        """
        event = FactionMemory(
            timestamp=time.time(),
            event_type=action_type,
            location=location,
            severity=severity,
            witnesses=witnessed_by
        )

        # Directly affected factions remember immediately
        for faction_id in affected_factions:
            if faction_id in self.factions:
                self.factions[faction_id].record_event(event)
                event.propagated_to.add(faction_id)

                # Adjust reputation
                rep_change = self._calculate_reputation_change(action_type, severity, faction_id)
                self.player_reputation[faction_id].adjust(rep_change, action_type)

        # Queue event for gossip propagation
        self.event_queue.append((event, affected_factions))

    def _calculate_reputation_change(self, action_type: str, severity: float, faction_id: FactionID) -> float:
        """Calculate how much reputation changes based on action"""
        base_changes = {
            "attack": -30,
            "theft": -20,
            "trespass": -10,
            "chaos": -15,
            "vandalism": -12,
            "help": +15,
            "purchase": +5,
            "conversation": +2
        }

        base = base_changes.get(action_type, 0)

        # Faction-specific modifiers
        faction = self.factions[faction_id]
        modifier = 1.0 + faction.aggression

        return base * severity * modifier

    def update(self, dt: float):
        """Update all factions and propagate information"""
        self.simulation_time += dt

        # Update each faction
        for faction in self.factions.values():
            faction.update(dt, time.time())

        # Propagate gossip
        self._propagate_gossip()

        # Check for emergent faction relationship changes
        self._update_faction_relations()

    def _propagate_gossip(self):
        """
        Information spreads between factions based on gossip rates.
        This creates realistic information flow - security hears about chaos,
        workers gossip about weird customers, etc.
        """
        if not self.event_queue:
            return

        # Process a few events per update
        for _ in range(min(3, len(self.event_queue))):
            if not self.event_queue:
                break

            event, source_factions = self.event_queue.popleft()

            # Each source faction might gossip to related factions
            for source_id in source_factions:
                if source_id not in self.factions:
                    continue

                source = self.factions[source_id]

                # Check each other faction
                for target_id, target in self.factions.items():
                    if target_id in event.propagated_to:
                        continue  # Already knows

                    # Gossip probability based on relationship and gossip rate
                    relation = source.get_relation_with(target_id)
                    base_prob = source.gossip_rate

                    if relation in [FactionRelation.ALLIED, FactionRelation.FRIENDLY]:
                        prob = base_prob * 0.8
                    elif relation == FactionRelation.NEUTRAL:
                        prob = base_prob * 0.3
                    else:
                        prob = base_prob * 0.1

                    if random.random() < prob:
                        # Information spreads!
                        target.record_event(event)
                        event.propagated_to.add(target_id)

                        # Weaker reputation impact from hearsay
                        rep_change = self._calculate_reputation_change(
                            event.event_type, event.severity * 0.5, target_id
                        )
                        self.player_reputation[target_id].adjust(rep_change, f"heard_{event.event_type}")

    def _update_faction_relations(self):
        """
        Emergent faction politics - relationships change based on player actions.

        If player attacks one faction, allied factions might become hostile.
        If player helps one faction, their allies might become friendlier.
        """
        for faction_id, reputation in self.player_reputation.items():
            faction = self.factions[faction_id]

            # Extreme player actions affect allied factions
            if reputation.value < -50:  # Player is enemy of this faction
                for other_id, relation in faction.relations.items():
                    if relation == FactionRelation.ALLIED:
                        # Allied factions also become suspicious
                        other_faction = self.factions.get(other_id)
                        if other_faction:
                            other_faction.modify_relation(faction_id, -1)

            elif reputation.value > 50:  # Player is friend of this faction
                for other_id, relation in faction.relations.items():
                    if relation == FactionRelation.FRIENDLY:
                        # Friendly factions become more friendly
                        other_faction = self.factions.get(other_id)
                        if other_faction:
                            other_faction.modify_relation(faction_id, 1)

    def get_faction_alert_level(self, faction_id: FactionID) -> AlertLevel:
        """Get current alert level for a faction"""
        faction = self.factions.get(faction_id)
        return faction.alert_level if faction else AlertLevel.CALM

    def get_reputation(self, faction_id: FactionID) -> float:
        """Get player reputation with a faction (-100 to +100)"""
        return self.player_reputation.get(faction_id, FactionReputation()).value

    def is_coordinated_response_active(self) -> bool:
        """Check if multiple factions are coordinating against player"""
        hostile_count = 0

        for faction_id, reputation in self.player_reputation.items():
            if reputation.value < -30:  # Hostile threshold
                faction = self.factions[faction_id]
                if faction.alert_level.value >= AlertLevel.ALERT.value:
                    hostile_count += 1

        return hostile_count >= 2  # Multiple factions coordinating

    def get_faction_by_id(self, faction_id: FactionID) -> Optional[Faction]:
        """Get faction object"""
        return self.factions.get(faction_id)
