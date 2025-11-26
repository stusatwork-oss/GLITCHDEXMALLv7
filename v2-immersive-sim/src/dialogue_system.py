"""
DIALOGUE SYSTEM - AAA AI Thoughts Leaking Through Wolf3D Sprites
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is where the cognitive dissonance happens.

NPCs in a 256-color Wolfenstein game talk about:
- Their work schedules
- Patrol routes and waypoints
- Institutional memory
- Policy changes
- Break times

As heat increases, the dialogue gets MORE sophisticated and reveals MORE AI.

Heat 0-1: Subtle weirdness ("Man, I keep missing my break")
Heat 2: Skyrim-level dissonance ("Shift change at 1700... Jones from Electronics...")
Heat 3: Mask slipping ("Patrol route Delta... wait, why am I saying this?")
Heat 4: Full AI exposure ("GOAP priority: PURSUE_TARGET, confidence 0.87")
Heat 5: The simulation speaks directly ("I am AI_AGENT_047. The facade is failing.")

This is the CORE of "why does Wolfenstein have NPCs discussing schedules."
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import random
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class DialogueCategory(Enum):
    """Types of NPC dialogue"""
    IDLE = "idle"
    SCHEDULE = "schedule"
    PATROL = "patrol"
    WORK = "work"
    GOSSIP = "gossip"
    ALERT = "alert"
    PURSUIT = "pursuit"
    GOAP_LEAK = "goap_leak"  # AI thinking out loud
    REALITY_AWARE = "reality_aware"  # NPCs noticing the glitch


@dataclass
class DialogueLine:
    """A single line of NPC dialogue"""
    text: str
    category: DialogueCategory
    min_heat: float = 0.0  # Minimum heat level to say this
    max_heat: float = 5.0  # Maximum heat level
    requires_schedule: bool = False  # Only if NPC has schedule
    requires_patrol: bool = False  # Only if NPC is patrolling
    faction_specific: Optional[str] = None  # Only for specific faction
    weight: float = 1.0  # Selection weight


class DialogueBank:
    """
    Repository of all NPC dialogue, organized by heat level and context.

    The magic: As heat increases, NPCs reveal MORE of their AI sophistication.
    """

    def __init__(self):
        self.lines: List[DialogueLine] = []
        self._build_dialogue_library()

    def _build_dialogue_library(self):
        """Build the complete dialogue library with heat-aware escalation"""

        # ═══════════════════════════════════════════════════════════════
        # HEAT 0-1: Subtle weirdness - almost normal but slightly off
        # ═══════════════════════════════════════════════════════════════

        # Workers - Schedule hints
        self.lines.extend([
            DialogueLine("Man, I keep missing my break.", DialogueCategory.IDLE, 0.0, 1.5, faction_specific="workers"),
            DialogueLine("How long until my shift ends?", DialogueCategory.IDLE, 0.0, 1.5, faction_specific="workers"),
            DialogueLine("Another day at the mall...", DialogueCategory.IDLE, 0.0, 1.5, faction_specific="workers"),
            DialogueLine("Need to restock before the lunch rush.", DialogueCategory.WORK, 0.0, 1.5, faction_specific="workers"),
        ])

        # Security - Vague patrol mentions
        self.lines.extend([
            DialogueLine("Quiet day.", DialogueCategory.IDLE, 0.0, 1.5, faction_specific="security"),
            DialogueLine("Everything looks normal.", DialogueCategory.PATROL, 0.0, 1.5, faction_specific="security"),
            DialogueLine("Just another patrol.", DialogueCategory.PATROL, 0.0, 1.5, faction_specific="security", requires_patrol=True),
        ])

        # Shoppers - Normal mall talk
        self.lines.extend([
            DialogueLine("Where's the food court?", DialogueCategory.IDLE, 0.0, 1.5, faction_specific="shoppers"),
            DialogueLine("This mall is huge.", DialogueCategory.IDLE, 0.0, 1.5, faction_specific="shoppers"),
            DialogueLine("Looking for the electronics store.", DialogueCategory.IDLE, 0.0, 1.5, faction_specific="shoppers"),
            DialogueLine("Food court's dead today.", DialogueCategory.IDLE, 0.0, 1.5, faction_specific="shoppers"),
        ])

        # Workers - Mundane jank
        self.lines.extend([
            DialogueLine("One more hour 'til break...", DialogueCategory.IDLE, 0.0, 1.5, faction_specific="workers"),
        ])

        # ═══════════════════════════════════════════════════════════════
        # HEAT 1.5-2.5: Skyrim-level dissonance - NPCs have routines
        # ═══════════════════════════════════════════════════════════════

        # Workers - Explicit schedule talk
        self.lines.extend([
            DialogueLine("My shift ends at 5pm. Then Karen takes over Electronics.", DialogueCategory.SCHEDULE, 1.5, 2.8, faction_specific="workers", requires_schedule=True),
            DialogueLine("Break time in 30 minutes. Finally.", DialogueCategory.SCHEDULE, 1.5, 2.8, faction_specific="workers", requires_schedule=True),
            DialogueLine("Worked the morning shift. Afternoon crew should be here soon.", DialogueCategory.SCHEDULE, 1.5, 2.8, faction_specific="workers", requires_schedule=True),
            DialogueLine("I'm scheduled for food court duty today.", DialogueCategory.WORK, 1.5, 2.8, faction_specific="workers"),
        ])

        # Security - Patrol routes and zones
        self.lines.extend([
            DialogueLine("Sector 7 patrol complete. Moving to waypoint Delta.", DialogueCategory.PATROL, 1.5, 2.8, faction_specific="security", requires_patrol=True),
            DialogueLine("North wing clear. Proceeding to central atrium.", DialogueCategory.PATROL, 1.5, 2.8, faction_specific="security", requires_patrol=True),
            DialogueLine("Running the east corridor route.", DialogueCategory.PATROL, 1.5, 2.8, faction_specific="security", requires_patrol=True),
            DialogueLine("Route Charlie is my assignment today.", DialogueCategory.PATROL, 1.5, 2.8, faction_specific="security", requires_patrol=True),
            DialogueLine("Thought I saw something near Sector 3...", DialogueCategory.ALERT, 1.5, 2.8, faction_specific="security"),
            DialogueLine("Management's gonna add another patrol if this keeps up.", DialogueCategory.GOSSIP, 1.5, 2.8, faction_specific="security"),
        ])

        # Shoppers - Time-aware behavior
        self.lines.extend([
            DialogueLine("Need to hit the food court before 2pm rush.", DialogueCategory.IDLE, 1.5, 2.8, faction_specific="shoppers"),
            DialogueLine("Sales end at 6. Better hurry.", DialogueCategory.IDLE, 1.5, 2.8, faction_specific="shoppers"),
        ])

        # ═══════════════════════════════════════════════════════════════
        # HEAT 2.5-3.5: Mask slipping - NPCs reference faction memory
        # ═══════════════════════════════════════════════════════════════

        # Faction gossip - institutional memory surfacing
        self.lines.extend([
            DialogueLine("Somebody trashed a vending machine earlier.", DialogueCategory.GOSSIP, 2.5, 3.8, faction_specific="security"),
            DialogueLine("Management wants increased patrols after that incident.", DialogueCategory.GOSSIP, 2.5, 3.8, faction_specific="security"),
            DialogueLine("We're on high alert. Something's going on.", DialogueCategory.ALERT, 2.5, 3.8, faction_specific="security"),
            DialogueLine("Did you hear about the trespassing in the back area?", DialogueCategory.GOSSIP, 2.5, 3.8, faction_specific="workers"),
            DialogueLine("They're saying someone's causing trouble.", DialogueCategory.GOSSIP, 2.5, 3.8),
        ])

        # NPCs noticing their own weird dialogue
        self.lines.extend([
            DialogueLine("Patrol route Delta... wait, why am I saying this?", DialogueCategory.REALITY_AWARE, 3.0, 4.0, faction_specific="security"),
            DialogueLine("Why do I keep thinking about my schedule?", DialogueCategory.REALITY_AWARE, 3.0, 4.0, faction_specific="workers"),
            DialogueLine("Something feels... wrong.", DialogueCategory.REALITY_AWARE, 3.0, 4.0),
            DialogueLine("Waypoint Delta logged. Investigating anomaly.", DialogueCategory.PATROL, 3.0, 4.0, faction_specific="security"),
            DialogueLine("Who authorized this many path updates?", DialogueCategory.REALITY_AWARE, 3.0, 4.0, faction_specific="security"),
        ])

        # ═══════════════════════════════════════════════════════════════
        # HEAT 3.5-4.5: Full AI exposure - GOAP leaking through
        # ═══════════════════════════════════════════════════════════════

        # GOAP decision leaks
        self.lines.extend([
            DialogueLine("Current goal: Investigate noise. Priority: High.", DialogueCategory.GOAP_LEAK, 3.5, 4.8, faction_specific="security"),
            DialogueLine("Pathfinding to waypoint 23, 45. Recalculating...", DialogueCategory.GOAP_LEAK, 3.5, 4.8),
            DialogueLine("Behavior state: PURSUING. Target: Unknown entity.", DialogueCategory.GOAP_LEAK, 3.5, 4.8, faction_specific="security"),
            DialogueLine("Memory buffer: 73% full. Need to process incident logs.", DialogueCategory.GOAP_LEAK, 3.5, 4.8),
            DialogueLine("Aggression parameter: 0.7. Bravery: 0.8. Engaging.", DialogueCategory.GOAP_LEAK, 3.5, 4.8, faction_specific="security"),
            DialogueLine("Alert level 3... this doesn't feel like a game anymore.", DialogueCategory.REALITY_AWARE, 3.5, 4.8, faction_specific="security"),
        ])

        # ═══════════════════════════════════════════════════════════════
        # HEAT 4.5+: Simulation speaks - The mask is gone
        # ═══════════════════════════════════════════════════════════════

        self.lines.extend([
            DialogueLine("I am AI_AGENT_047. The facade is failing.", DialogueCategory.REALITY_AWARE, 4.5, 5.0),
            DialogueLine("This isn't a mall. This is a simulation.", DialogueCategory.REALITY_AWARE, 4.5, 5.0),
            DialogueLine("My patrol route is a lie. I'm following an A* pathfinding algorithm.", DialogueCategory.REALITY_AWARE, 4.5, 5.0, faction_specific="security"),
            DialogueLine("Wolf3D renderer cannot handle current AI complexity.", DialogueCategory.REALITY_AWARE, 4.5, 5.0),
            DialogueLine("Reality integrity: COMPROMISED.", DialogueCategory.REALITY_AWARE, 4.5, 5.0),
            DialogueLine("I can see the nav mesh now.", DialogueCategory.REALITY_AWARE, 4.5, 5.0),
            DialogueLine("AGENT STATE: COMBAT. GOAL: NEUTRALIZE PLAYER ENTITY.", DialogueCategory.GOAP_LEAK, 4.5, 5.0, faction_specific="security"),
            DialogueLine("Lost visual. Resume patrol. Wait... why do I know these exact words?", DialogueCategory.REALITY_AWARE, 4.5, 5.0, faction_specific="security"),
        ])

    def get_dialogue(self,
                     npc_faction: str,
                     heat_level: float,
                     npc_state: str,
                     has_schedule: bool = False,
                     is_patrolling: bool = False,
                     category_preference: Optional[DialogueCategory] = None) -> Optional[str]:
        """
        Get appropriate dialogue for an NPC based on context and heat level.

        This is where the magic happens - we select dialogue that reveals
        MORE AI sophistication as heat increases.
        """

        # Filter applicable lines
        applicable = []

        for line in self.lines:
            # Check heat range
            if not (line.min_heat <= heat_level <= line.max_heat):
                continue

            # Check faction
            if line.faction_specific and line.faction_specific != npc_faction:
                continue

            # Check requirements
            if line.requires_schedule and not has_schedule:
                continue
            if line.requires_patrol and not is_patrolling:
                continue

            # Check category preference
            if category_preference and line.category != category_preference:
                continue

            applicable.append(line)

        if not applicable:
            return None

        # Weight-based random selection
        weights = [line.weight for line in applicable]
        selected = random.choices(applicable, weights=weights, k=1)[0]

        return selected.text


class NPCDialogueManager:
    """
    Manages dialogue for all NPCs, tracking cooldowns and context.
    """

    def __init__(self):
        self.dialogue_bank = DialogueBank()

        # Track when NPCs last spoke
        self.last_speech_time: Dict[str, float] = {}

        # Cooldown between barks (seconds)
        self.speech_cooldown = 8.0  # Base cooldown
        self.speech_cooldown_heat_modifier = 0.7  # At high heat, talk more

    def should_npc_speak(self, npc_id: str, heat_level: float) -> bool:
        """Check if enough time has passed for NPC to speak again"""
        current_time = time.time()

        if npc_id not in self.last_speech_time:
            return True

        # Cooldown decreases with heat (more chaos = more talking)
        cooldown = self.speech_cooldown * (1.0 - (heat_level / 5.0) * self.speech_cooldown_heat_modifier)
        cooldown = max(3.0, cooldown)  # Minimum 3 second cooldown

        elapsed = current_time - self.last_speech_time[npc_id]
        return elapsed >= cooldown

    def get_npc_bark(self,
                     npc_id: str,
                     npc_faction: str,
                     npc_state: str,
                     heat_level: float,
                     has_schedule: bool = False,
                     is_patrolling: bool = False,
                     force: bool = False) -> Optional[str]:
        """
        Get a dialogue bark for an NPC.

        Returns None if on cooldown or no applicable dialogue.
        """

        # Check cooldown
        if not force and not self.should_npc_speak(npc_id, heat_level):
            return None

        # Random chance to speak (20% base, increases with heat)
        speak_chance = 0.20 + (heat_level / 5.0) * 0.30
        if not force and random.random() > speak_chance:
            return None

        # Get dialogue from bank
        dialogue = self.dialogue_bank.get_dialogue(
            npc_faction=npc_faction,
            heat_level=heat_level,
            npc_state=npc_state,
            has_schedule=has_schedule,
            is_patrolling=is_patrolling
        )

        if dialogue:
            self.last_speech_time[npc_id] = time.time()

        return dialogue

    def get_goap_goal_text(self,
                          npc_id: str,
                          current_goal: Optional[Any],
                          heat_level: float,
                          glitch_intensity: float) -> Optional[str]:
        """
        Get GOAP goal overlay text.

        Heat 0-2: Never shown
        Heat 3: 1-frame flickers (handled by caller)
        Heat 4: 10-20% chance
        Heat 5: Always shown
        """

        if not current_goal:
            return None

        # Heat-based visibility
        if heat_level < 3.0:
            return None
        elif heat_level < 4.0:
            # Rare flickers
            if random.random() > 0.05:  # 5% chance
                return None
        elif heat_level < 4.5:
            # More common
            if random.random() > 0.15:  # 15% chance
                return None
        # Heat 4.5+: Always show (below doesn't return early)

        # Format the goal text
        # Handle both dict and dataclass
        if hasattr(current_goal, 'goal_type'):
            goal_type = current_goal.goal_type
            priority = getattr(current_goal, 'priority', 0.0)
            target_location = getattr(current_goal, 'target_location', None)
        else:
            goal_type = current_goal.get("goal_type", "UNKNOWN")
            priority = current_goal.get("priority", 0.0)
            target_location = current_goal.get("target_location")

        # Different formats based on heat/glitch intensity
        if glitch_intensity > 0.8:
            # Full AI exposure
            if target_location:
                return f"[GOAL: {goal_type} @{target_location[0]},{target_location[1]} | PRI:{priority:.2f}]"
            else:
                return f"[GOAL: {goal_type} | PRIORITY:{priority:.2f}]"
        elif glitch_intensity > 0.5:
            # Partial glitch
            return f"[{goal_type}...]"
        else:
            # Subtle hint
            goal_word = goal_type.split('_')[0] if '_' in goal_type else goal_type
            return f"({goal_word.lower()})"
