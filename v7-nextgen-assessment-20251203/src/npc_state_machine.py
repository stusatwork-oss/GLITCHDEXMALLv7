#!/usr/bin/env python3
"""
NPC STATE MACHINE - V6 NextGen with QBIT Integration

Manages NPC behavioral states with QBIT-aware contradiction system.

Key Features:
- Spine-based behavior constraints (NPCs have "never" rules)
- Cloud-driven state transitions
- QBIT power scores determine contradiction thresholds
- High-power entities can break rules at lower Cloud pressure
- Zone-aware behavior modifiers

States:
- IDLE: Default wandering/standing
- PATROL: Route-based movement
- ALERT: Aware of anomaly but not hostile
- SUSPICIOUS: Investigating unusual behavior
- HOSTILE: Actively responding to threat
- CONTRADICTION: Breaking spine rules (bleed-driven)
"""

import time
import random
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field


class NPCState(Enum):
    """NPC behavioral states."""
    IDLE = "idle"
    PATROL = "patrol"
    ALERT = "alert"
    SUSPICIOUS = "suspicious"
    HOSTILE = "hostile"
    CONTRADICTION = "contradiction"  # Breaking spine rules


@dataclass
class NPCSpine:
    """
    NPC behavior spine - defines personality constraints.

    Spines include "never" rules that NPCs cannot violate unless
    Cloud pressure triggers a contradiction event.
    """
    npc_id: str
    name: str
    role: str = "Secondary"  # Primary | Secondary

    # Behavior constraints
    never_rules: List[str] = field(default_factory=list)
    always_rules: List[str] = field(default_factory=list)
    spatial_constraints: List[str] = field(default_factory=list)

    # QBIT integration
    qbit_power: int = 0           # Structural leverage (0-3000)
    qbit_charisma: int = 0        # Attention/resonance (0-3000)
    qbit_overall: int = 0         # Combined score (0-6000)

    # Zone affinity
    home_zone: str = ""
    allowed_zones: List[str] = field(default_factory=list)
    forbidden_zones: List[str] = field(default_factory=list)

    def can_enter_zone(self, zone_id: str) -> bool:
        """Check if NPC can enter a zone based on spine constraints."""
        if zone_id in self.forbidden_zones:
            return False
        if self.allowed_zones and zone_id not in self.allowed_zones:
            return False
        return True

    def get_contradiction_threshold(self) -> float:
        """
        Get Cloud pressure threshold for contradictions.

        High-power NPCs can break rules at lower Cloud pressure.
        Base threshold: 75 (CRITICAL)
        High-power (>2000): Can contradict at 60 (STRAINED+15)
        """
        base_threshold = 75.0

        # High-power entities get earlier contradiction access
        if self.qbit_power > 2000:
            return base_threshold - 15.0  # 60
        elif self.qbit_power > 1500:
            return base_threshold - 10.0  # 65
        elif self.qbit_power > 1000:
            return base_threshold - 5.0   # 70

        return base_threshold


@dataclass
class NPCStateMachine:
    """
    NPC state machine with QBIT-aware contradiction system.
    """
    npc_id: str
    spine: NPCSpine

    # Current state
    current_state: NPCState = NPCState.IDLE
    state_start_time: float = 0.0

    # Position
    current_zone: str = ""
    target_position: Optional[tuple] = None

    # Behavior flags
    can_contradict: bool = False
    contradiction_active: bool = False
    last_contradiction_time: float = 0.0

    # Cloud awareness
    cloud_level: float = 0.0
    cloud_mood: str = "calm"

    # State history
    state_history: List[Dict] = field(default_factory=list)

    def __post_init__(self):
        self.state_start_time = time.time()

    def update(self, dt: float, cloud_level: float, cloud_mood: str,
               player_nearby: bool = False, player_action: Optional[str] = None) -> Dict:
        """
        Update NPC state machine.

        Args:
            dt: Delta time in seconds
            cloud_level: Current Cloud pressure (0-100)
            cloud_mood: Current mall mood
            player_nearby: Is player in same zone
            player_action: Current player action type

        Returns:
            Dict of behavior hints for renderer/AI
        """
        self.cloud_level = cloud_level
        self.cloud_mood = cloud_mood

        # Check if NPC can contradict based on QBIT power
        contradiction_threshold = self.spine.get_contradiction_threshold()
        self.can_contradict = cloud_level >= contradiction_threshold

        # State transitions
        self._update_state_transitions(player_nearby, player_action)

        # Generate behavior hints
        return self._generate_behavior_hints()

    def _update_state_transitions(self, player_nearby: bool, player_action: Optional[str]):
        """Update state based on Cloud pressure and player actions."""
        old_state = self.current_state

        # CONTRADICTION state (highest priority)
        if self.can_contradict and not self.contradiction_active:
            # Check if contradiction cooldown expired (30 seconds)
            if time.time() - self.last_contradiction_time > 30.0:
                # Random chance to trigger contradiction
                if random.random() < 0.1:  # 10% chance per update when ready
                    self._trigger_contradiction()
                    return

        # Normal state machine
        if self.current_state == NPCState.IDLE:
            if player_nearby and player_action in ["run", "interact"]:
                self._transition_to(NPCState.ALERT)
            elif random.random() < 0.05:  # 5% chance to patrol
                self._transition_to(NPCState.PATROL)

        elif self.current_state == NPCState.PATROL:
            if player_nearby and player_action == "run":
                self._transition_to(NPCState.SUSPICIOUS)
            elif random.random() < 0.02:  # Return to idle
                self._transition_to(NPCState.IDLE)

        elif self.current_state == NPCState.ALERT:
            if player_action == "run":
                self._transition_to(NPCState.SUSPICIOUS)
            elif not player_nearby:
                self._transition_to(NPCState.IDLE)

        elif self.current_state == NPCState.SUSPICIOUS:
            # Cloud pressure affects escalation
            if self.cloud_level > 70 and player_action == "interact":
                self._transition_to(NPCState.HOSTILE)
            elif not player_nearby:
                self._transition_to(NPCState.ALERT)

        elif self.current_state == NPCState.HOSTILE:
            # De-escalate if Cloud drops or player leaves
            if self.cloud_level < 50 or not player_nearby:
                self._transition_to(NPCState.SUSPICIOUS)

        elif self.current_state == NPCState.CONTRADICTION:
            # Contradictions last 5-15 seconds
            time_in_contradiction = time.time() - self.state_start_time
            if time_in_contradiction > random.uniform(5.0, 15.0):
                self.contradiction_active = False
                self._transition_to(NPCState.IDLE)

    def _transition_to(self, new_state: NPCState):
        """Transition to a new state."""
        if new_state != self.current_state:
            # Record state change
            self.state_history.append({
                "timestamp": time.time(),
                "from_state": self.current_state.value,
                "to_state": new_state.value,
                "cloud_level": self.cloud_level
            })

            self.current_state = new_state
            self.state_start_time = time.time()

    def _trigger_contradiction(self):
        """Trigger a contradiction event (NPC breaks spine rules)."""
        if not self.spine.never_rules:
            return  # No rules to break

        self.contradiction_active = True
        self.last_contradiction_time = time.time()
        self._transition_to(NPCState.CONTRADICTION)

        # Pick a random "never" rule to break
        broken_rule = random.choice(self.spine.never_rules)

        print(f"[NPC CONTRADICTION] {self.spine.name} breaking rule: {broken_rule}")
        print(f"  Cloud: {self.cloud_level:.1f}, QBIT Power: {self.spine.qbit_power}")

    def _generate_behavior_hints(self) -> Dict:
        """Generate behavior hints for renderer/AI system."""
        return {
            "npc_id": self.npc_id,
            "name": self.spine.name,
            "state": self.current_state.value,
            "cloud_level": self.cloud_level,
            "can_contradict": self.can_contradict,
            "contradiction_active": self.contradiction_active,
            "qbit_power": self.spine.qbit_power,
            "qbit_charisma": self.spine.qbit_charisma,
            "current_zone": self.current_zone,

            # Behavioral modifiers
            "movement_speed": self._get_movement_speed(),
            "dialogue_tension": self.cloud_level / 100,
            "aggression": self._get_aggression_level(),
            "attention_focus": self._get_attention_focus()
        }

    def _get_movement_speed(self) -> float:
        """Get movement speed based on state and Cloud."""
        base_speed = 1.0

        if self.current_state == NPCState.IDLE:
            return base_speed * 0.5
        elif self.current_state == NPCState.PATROL:
            return base_speed * 0.8
        elif self.current_state == NPCState.ALERT:
            return base_speed * 1.2
        elif self.current_state == NPCState.SUSPICIOUS:
            return base_speed * 1.5
        elif self.current_state == NPCState.HOSTILE:
            return base_speed * 2.0
        elif self.current_state == NPCState.CONTRADICTION:
            # Erratic movement during contradiction
            return base_speed * random.uniform(0.3, 2.5)

        return base_speed

    def _get_aggression_level(self) -> float:
        """Get aggression level (0-1)."""
        if self.current_state == NPCState.HOSTILE:
            return 1.0
        elif self.current_state == NPCState.SUSPICIOUS:
            return 0.6
        elif self.current_state == NPCState.ALERT:
            return 0.3
        elif self.current_state == NPCState.CONTRADICTION:
            return random.uniform(0.0, 1.0)  # Unpredictable

        return 0.0

    def _get_attention_focus(self) -> str:
        """Get what NPC is paying attention to."""
        if self.current_state in [NPCState.ALERT, NPCState.SUSPICIOUS, NPCState.HOSTILE]:
            return "player"
        elif self.current_state == NPCState.CONTRADICTION:
            return "anomaly"

        return "environment"

    def attempt_zone_entry(self, zone_id: str, force: bool = False) -> bool:
        """
        Attempt to enter a zone.

        Args:
            zone_id: Zone to enter
            force: Force entry (contradiction override)

        Returns:
            True if entry allowed
        """
        # Contradiction state can violate spatial constraints
        if self.contradiction_active or force:
            self.current_zone = zone_id
            return True

        # Normal spine check
        if self.spine.can_enter_zone(zone_id):
            self.current_zone = zone_id
            return True

        return False


# ========== MODULE TESTING ==========

if __name__ == "__main__":
    print("=" * 60)
    print("NPC STATE MACHINE - QBIT Integration Test")
    print("=" * 60)

    # Create test spine
    spine = NPCSpine(
        npc_id="janitor-001",
        name="The Janitor",
        role="Primary",
        never_rules=[
            "never_cross_fc_arcade_threshold",
            "never_speak_about_wife",
            "never_acknowledge_player_directly"
        ],
        always_rules=[
            "always_mop_same_tiles",
            "always_face_away_from_bookstore"
        ],
        spatial_constraints=[
            "forbidden:FC-ARCADE"
        ],
        qbit_power=2400,  # High power - can contradict earlier
        qbit_charisma=800,
        qbit_overall=3200,
        home_zone="CORRIDOR",
        allowed_zones=["CORRIDOR", "SERVICE_HALL", "ENTRANCE"],
        forbidden_zones=["FC-ARCADE"]
    )

    # Create state machine
    npc = NPCStateMachine(
        npc_id="janitor-001",
        spine=spine,
        current_zone="CORRIDOR"
    )

    print(f"\nNPC: {spine.name}")
    print(f"  QBIT Power: {spine.qbit_power}")
    print(f"  QBIT Charisma: {spine.qbit_charisma}")
    print(f"  Contradiction Threshold: {spine.get_contradiction_threshold():.1f}")
    print(f"  Never Rules: {len(spine.never_rules)}")

    # Test zone entry
    print("\nTesting zone entry constraints:")
    print(f"  Can enter CORRIDOR: {npc.attempt_zone_entry('CORRIDOR')}")
    print(f"  Can enter FC-ARCADE: {npc.attempt_zone_entry('FC-ARCADE')}")
    print(f"  Can enter FC-ARCADE (force): {npc.attempt_zone_entry('FC-ARCADE', force=True)}")

    # Test state updates at different Cloud levels
    print("\nTesting state machine at different Cloud levels:")

    for cloud_level in [10, 40, 60, 75, 85]:
        hints = npc.update(
            dt=0.1,
            cloud_level=cloud_level,
            cloud_mood="calm" if cloud_level < 50 else "critical",
            player_nearby=(cloud_level > 60),
            player_action="run" if cloud_level > 70 else None
        )

        print(f"\n  Cloud {cloud_level}: State={hints['state']}, "
              f"Can Contradict={hints['can_contradict']}")

        if hints['contradiction_active']:
            print(f"    ⚠️  CONTRADICTION ACTIVE")

    # Test contradiction trigger (simulate high Cloud)
    print("\nSimulating contradiction event (Cloud 85):")
    for i in range(100):  # Run until contradiction triggers
        hints = npc.update(
            dt=0.1,
            cloud_level=85,
            cloud_mood="critical",
            player_nearby=True,
            player_action="interact"
        )

        if hints['contradiction_active']:
            print(f"  ✓ Contradiction triggered after {i} updates")
            print(f"    State: {hints['state']}")
            print(f"    Movement speed: {hints['movement_speed']:.2f}")
            break

    print("\n✓ NPC state machine test complete")
