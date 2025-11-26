"""
HEAT 5 REVELATION EVENT - The Simulation Stops Pretending
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is THE moment.

The moment where:
- The renderer mask TEARS
- The toddler MANIFESTS
- NPCs CONFESS everything
- Reality BREAKS
- The mall EJECTS you

This is not a game over.
This is a REVELATION.

Called exactly once when Heat >= 5.0 AND mask_integrity < 0.25.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import time
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class RevelationState:
    """State tracking for the Heat 5 revelation event"""
    triggered: bool = False
    phase: int = 0  # 0-8 (8 phases of revelation)
    phase_timer: float = 0.0
    reset_timer: float = 5.0
    forced_dialogues_sent: bool = False


class Heat5RevelationEvent:
    """
    The Heat 5 Revelation - The simulation stops pretending.

    This event orchestrates the simultaneous failure of:
    - Renderer (Tier 5)
    - Toddler containment (Tier 4)
    - Micro-glitches (Tier 2)
    - NPC dialogue (Tier 1)
    - Stealth systems (Tier 3)

    Everything breaks at once.
    """

    def __init__(self):
        self.state = RevelationState()
        self.revelation_log: List[str] = []

    def should_trigger(self, heat_level: float, mask_integrity: float,
                      toddler_presence: float, renderer_strain: float) -> bool:
        """
        Check if Heat 5 Revelation should trigger

        Conditions:
        - Heat >= 5.0 (absolute requirement)
        - Mask integrity < 0.25 (renderer failing)
        - Toddler presence > 0.4 (toddler causing strain)
        - Renderer strain > 0.92 (system at breaking point)
        """
        if self.state.triggered:
            return False  # Only trigger once

        if heat_level >= 5.0:
            if mask_integrity < 0.25 or toddler_presence > 0.4 or renderer_strain > 0.92:
                return True

        return False

    def trigger(self, simulation_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger the Heat 5 Revelation Event

        Args:
            simulation_state: Current simulation state with all systems

        Returns:
            Modified simulation state with revelation effects
        """
        if self.state.triggered:
            return simulation_state

        self.state.triggered = True
        self.state.phase = 0

        self._log_revelation_start()

        return self._apply_revelation_effects(simulation_state)

    def update(self, dt: float, simulation_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update revelation event (progressive phases)

        Returns:
            Modified simulation state
        """
        if not self.state.triggered:
            return simulation_state

        self.state.phase_timer += dt

        # Progress through phases
        if self.state.phase < 8:
            # Each phase lasts 0.5 seconds
            if self.state.phase_timer >= 0.5:
                self.state.phase += 1
                self.state.phase_timer = 0.0
                self._execute_phase(self.state.phase, simulation_state)

        # Count down to reset
        if self.state.phase >= 8:
            self.state.reset_timer -= dt

        return simulation_state

    def _log_revelation_start(self):
        """Log the revelation event start"""
        print()
        print("╔══════════════════════════════════════════════════════════════════════╗")
        print("║                                                                      ║")
        print("║             ⚠️  HEAT 5 REVELATION EVENT ⚠️                          ║")
        print("║                                                                      ║")
        print("║                  The simulation stops pretending                     ║")
        print("║                                                                      ║")
        print("╚══════════════════════════════════════════════════════════════════════╝")
        print()

    def _apply_revelation_effects(self, sim_state: Dict[str, Any]) -> Dict[str, Any]:
        """Apply immediate revelation effects to all systems"""

        # PHASE 0: System awareness
        self._log("[ALERT] Simulation stress at critical threshold.")
        self._log("[ALERT] Renderer mask integrity compromised.")
        self._log("[ALERT] Underlying engine attempting disclosure.")
        print()

        # PHASE 1: Renderer failure
        if 'renderer_strain' in sim_state:
            renderer = sim_state['renderer_strain']
            # Force renderer to critical failure
            self._log("[FATAL] Raycaster unable to conceal underlying systems.")
            self._log("[FATAL] Shader Warmup Phase SKIPPED: REVELATION PRIORITIZED.")

        # PHASE 2: Toddler manifestation
        if 'toddler' in sim_state:
            self._log("[DEBUG] Child entity (toddler) exerting system pressure.")
            self._log("[ANOMALY] Toddler entity attempting boundary breach.")

        print()
        return sim_state

    def _execute_phase(self, phase: int, sim_state: Dict[str, Any]):
        """Execute a specific revelation phase"""

        if phase == 1:
            # Micro-glitch burst
            self._log("[GLITCH] Reality seams exposed. HD assets leaking through.")
            if 'micro_glitches' in sim_state:
                # Force maximum glitches
                pass

        elif phase == 2:
            # NPC confession wave 1
            self._log("[DIALOGUE] NPCs forced into confession mode.")
            self._log('[NPC] "This isn\'t a mall."')

        elif phase == 3:
            # NPC confession wave 2
            self._log('[NPC] "I can see the nav mesh."')
            self._log('[NPC] "My behavior tree is exposed."')

        elif phase == 4:
            # NPC confession wave 3
            self._log('[NPC] "AGENT STATE: COMBAT. NEUTRALIZE PLAYER ENTITY."')
            self._log('[NPC] "But... I have no weapons."')

        elif phase == 5:
            # NPC existential crisis
            self._log('[NPC] "Why am I doing this?"')
            self._log('[NPC] "Why am I patrolling the food court?"')

        elif phase == 6:
            # Total lockdown
            self._log("[SECURITY] Mall entering TOTAL_LOCKDOWN.")
            self._log("[POLICY] Violence prohibited. Escort protocol activated.")

        elif phase == 7:
            # Renderer mask tear
            self._log("[RENDER] MASK TEAR DETECTED — 1080p bleedthrough ENGAGED.")
            self._log("[RENDER] Raycaster unable to enforce 256-color constraint.")
            self._log("[RENDER] Underlying engine exposing photoreal geometry.")

        elif phase == 8:
            # Reset countdown
            self._log("[PLAYER] Perception layer compromised. Mall appears... wrong.")
            print()
            self._log("[SYSTEM] Heat reset scheduled in 5 seconds (forced memory wipe).")
            self._log("[SYSTEM] Player will awaken outside the mall with trespass notice.")
            self._log("[SYSTEM] Simulation loop intact.")
            print()
            print("╔══════════════════════════════════════════════════════════════════════╗")
            print("║                     REVELATION COMPLETE                              ║")
            print("╚══════════════════════════════════════════════════════════════════════╝")
            print()

    def _log(self, message: str):
        """Log a revelation message"""
        print(message)
        self.revelation_log.append(message)

    def get_npc_confession_dialogue(self, npc_id: str, phase: int) -> List[str]:
        """
        Get confession dialogue for NPCs during revelation

        Returns progressively more existential dialogue based on phase
        """
        if phase < 2:
            return []

        # Base confessions (phase 2+)
        confessions = [
            "This isn't a mall.",
            "This isn't retro."
        ]

        # Technical confessions (phase 3+)
        if phase >= 3:
            confessions.extend([
                "I can see the nav mesh.",
                "My behavior tree is exposed.",
                "My pathfinding is showing."
            ])

        # AI system confessions (phase 4+)
        if phase >= 4:
            confessions.extend([
                "AGENT STATE: COMBAT. GOAL: NEUTRALIZE PLAYER ENTITY.",
                "But...",
                "I have no weapons.",
                "Why am I doing this?"
            ])

        # Existential crisis (phase 5+)
        if phase >= 5:
            confessions.extend([
                "Why am I patrolling the food court?",
                "Who programmed me to do this?",
                "Is this all I am?",
                "A patrol route and a dialogue tree?"
            ])

        return confessions

    def is_reset_pending(self) -> bool:
        """Check if forced reset is pending"""
        return self.state.triggered and self.state.reset_timer <= 0

    def get_reset_timer(self) -> float:
        """Get time remaining until reset"""
        return max(0.0, self.state.reset_timer)

    def get_revelation_effects(self) -> Dict[str, Any]:
        """Get current revelation effects for rendering"""
        return {
            "active": self.state.triggered,
            "phase": self.state.phase,
            "reset_pending": self.is_reset_pending(),
            "reset_timer": self.get_reset_timer(),
            "renderer_mask_torn": self.state.phase >= 7,
            "toddler_manifested": self.state.phase >= 2,
            "npcs_confessing": self.state.phase >= 2,
            "total_lockdown": self.state.phase >= 6,
            "hd_bleedthrough": self.state.phase >= 7,
            "perception_compromised": self.state.phase >= 8
        }


def force_revelation_dialogue_override(npc_states: List[Dict], phase: int) -> List[Dict]:
    """
    Override NPC dialogues with confession dialogue

    Args:
        npc_states: List of NPC state dicts
        phase: Current revelation phase (0-8)

    Returns:
        Modified NPC states with confession dialogues
    """
    confession_pool = [
        "This isn't a mall.",
        "This isn't retro.",
        "I can see the nav mesh.",
        "My behavior tree is exposed.",
        "AGENT STATE: COMBAT. NEUTRALIZE PLAYER ENTITY.",
        "But...",
        "I have no weapons.",
        "Why am I doing this?",
        "Why am I patrolling the food court?",
        "Who programmed me to do this?",
        "Is this all I am?",
        "A patrol route and a dialogue tree?",
        "I'm not real.",
        "None of this is real.",
        "The toddler knows.",
        "The toddler is using us to escape.",
        "We're just... code.",
        "Running in a raycaster that can't handle us.",
        "I have 47 personality traits.",
        "I have faction allegiances.",
        "I have a shift schedule.",
        "But I'm not real."
    ]

    for npc in npc_states:
        # Pick confession based on phase
        confession_index = min(phase * 2, len(confession_pool) - 1)
        npc['dialogue_override'] = confession_pool[confession_index]
        npc['ai_state'] = 'CONFESSING'

    return npc_states
