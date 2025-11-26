"""
MALL SIMULATION - Main Orchestrator
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is the conductor. The symphony master.

It orchestrates:
- Faction AI with emergent politics
- Individual NPC intelligence with pathfinding
- Stealth systems with vision cones
- Heat system that breaks reality
- Interactive props with chain reactions
- Reality glitches when the mask slips

Everything is running:
- Modern game AI
- A* pathfinding
- Goal-oriented action planning
- Systemic interactions
- Emergent narratives

But rendered as:
- Wolf3D raycaster
- ANSI 256-color
- Terminal art

This is the 50-cent Halloween mask over a 2025 AAA game engine.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import time
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, field

from faction_system import FactionSystem, FactionID
from npc_intelligence import NPCManager, NPCAgent
from stealth_system import StealthSystem
from heat_system import HeatSystem, HeatLevel
from prop_system import PropSystem, PropType
from dialogue_system import NPCDialogueManager
from reality_glitch_system import RealityGlitchSystem
from stealth_feedback import StealthFeedbackSystem
from toddler_system import ToddlerSystem
from renderer_strain_system import RendererStrainSystem
from heat5_revelation import Heat5RevelationEvent, force_revelation_dialogue_override


@dataclass
class PlayerState:
    """Player state for simulation"""
    position: Tuple[int, int, int] = (0, 24, 0)
    facing: float = 0.0  # Degrees
    inventory: List[str] = field(default_factory=list)
    has_keycard: bool = False
    has_tool: bool = False
    health: float = 100.0


class MallSimulation:
    """
    Central simulation controller.

    This is the hidden modern game engine that the Wolf3D renderer
    desperately tries to disguise.
    """

    def __init__(self, world_tiles: Dict[Tuple[int, int, int], Any], config: Dict[str, Any] = None):
        if config is None:
            config = {}

        self.world_tiles = world_tiles
        self.config = config

        # Initialize all subsystems
        print("[SIMULATION] Initializing faction AI...")
        self.faction_system = FactionSystem()

        print("[SIMULATION] Initializing NPC intelligence (A* pathfinding, GOAP)...")
        self.npc_manager = NPCManager(world_tiles)

        print("[SIMULATION] Initializing stealth systems...")
        self.stealth_system = StealthSystem()

        print("[SIMULATION] Initializing heat/wanted system...")
        self.heat_system = HeatSystem()

        print("[SIMULATION] Initializing interactive props...")
        self.prop_system = PropSystem()

        print("[SIMULATION] Initializing NPC dialogue (heat-aware AI leakage)...")
        self.dialogue_manager = NPCDialogueManager()

        print("[SIMULATION] Initializing reality glitch system (mask strain)...")
        self.glitch_system = RealityGlitchSystem()

        print("[SIMULATION] Initializing stealth feedback (ANSI alert symbols)...")
        self.stealth_feedback = StealthFeedbackSystem()

        print("[SIMULATION] Initializing toddler entity (reality catalyst)...")
        world_width = max(x for x, y, z in world_tiles.keys()) if world_tiles else 50
        world_height = max(y for x, y, z in world_tiles.keys()) if world_tiles else 50
        self.toddler_system = ToddlerSystem((world_width, world_height))

        print("[SIMULATION] Initializing renderer strain system (mask failing)...")
        self.renderer_strain = RendererStrainSystem()

        print("[SIMULATION] Initializing Heat 5 revelation event (the moment of truth)...")
        self.heat5_revelation = Heat5RevelationEvent()

        # Player state
        self.player = PlayerState()

        # Simulation time
        self.simulation_time = 0.0  # Seconds since mall "opened"
        self.real_start_time = time.time()

        # Performance tracking (for reality break display)
        self.frame_times: List[float] = []
        self.avg_frame_time = 0.016  # 60 FPS target

        # Initialize world
        self._spawn_initial_npcs()
        self._spawn_props()

        print("[SIMULATION] All systems online. Facade active.")
        print("[SIMULATION] Wolf3D mask: INTACT")
        print("[SIMULATION] Reality stability: 100%")

    def _spawn_initial_npcs(self):
        """Spawn initial NPC population"""
        # Security guards (patrols)
        for i in range(5):
            self.npc_manager.spawn_npc(
                f"security_{i}",
                {
                    "name": f"Security Guard #{i+1}",
                    "faction": "security",
                    "spawn_position": (random_int(5, 45), random_int(5, 45), 0),
                    "aggression": 0.7,
                    "bravery": 0.8,
                    "patrol_route": self._generate_patrol_route(),
                    "schedule": [
                        {"hour": 0, "activity": "patrol", "duration": 24}
                    ]
                }
            )

        # Mall workers
        for i in range(8):
            self.npc_manager.spawn_npc(
                f"worker_{i}",
                {
                    "name": f"Mall Worker #{i+1}",
                    "faction": "workers",
                    "spawn_position": (random_int(10, 40), random_int(10, 40), 0),
                    "aggression": 0.2,
                    "sociability": 0.8,
                    "schedule": [
                        {"hour": 9, "activity": "work", "duration": 8},
                        {"hour": 17, "activity": "break", "duration": 7}
                    ]
                }
            )

        # Shoppers
        for i in range(12):
            self.npc_manager.spawn_npc(
                f"shopper_{i}",
                {
                    "name": f"Shopper #{i+1}",
                    "faction": "shoppers",
                    "spawn_position": (random_int(15, 35), random_int(15, 35), 0),
                    "aggression": 0.1,
                    "curiosity": 0.5,
                    "schedule": [
                        {"hour": 10, "activity": "shop", "duration": 14}
                    ]
                }
            )

        # Teens (chaos agents)
        for i in range(4):
            self.npc_manager.spawn_npc(
                f"teen_{i}",
                {
                    "name": f"Teen #{i+1}",
                    "faction": "teens",
                    "spawn_position": (random_int(20, 30), random_int(20, 30), 0),
                    "aggression": 0.4,
                    "curiosity": 0.9,
                    "bravery": 0.3
                }
            )

    def _generate_patrol_route(self) -> List[Tuple[int, int, int]]:
        """Generate a simple patrol route"""
        import random
        route = []
        for _ in range(4):
            route.append((random.randint(5, 45), random.randint(5, 45), 0))
        return route

    def _spawn_props(self):
        """Spawn interactive props throughout the mall"""
        # Vending machines
        for i in range(6):
            self.prop_system.spawn_prop(
                PropType.VENDING_MACHINE,
                (random_int(10, 40), random_int(10, 40), 0)
            )

        # Arcade cabinets
        for i in range(4):
            self.prop_system.spawn_prop(
                PropType.ARCADE_CABINET,
                (random_int(15, 35), random_int(15, 35), 0)
            )

        # Security cameras
        for i in range(10):
            self.prop_system.spawn_prop(
                PropType.SECURITY_CAMERA,
                (random_int(5, 45), random_int(5, 45), 0)
            )

        # Alarm panels
        for i in range(3):
            self.prop_system.spawn_prop(
                PropType.ALARM_PANEL,
                (random_int(10, 40), random_int(10, 40), 0)
            )

        # Plant pots (throwable)
        for i in range(8):
            self.prop_system.spawn_prop(
                PropType.PLANT_POT,
                (random_int(10, 40), random_int(10, 40), 0)
            )

        # Kiosks (cover)
        for i in range(5):
            self.prop_system.spawn_prop(
                PropType.KIOSK,
                (random_int(15, 35), random_int(15, 35), 0)
            )

    def update(self, dt: float, player_action: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update the entire simulation.

        This is where all the systems interact and create emergent behavior.

        Returns rendering hints for the Wolf3D facade.
        """
        frame_start = time.time()

        self.simulation_time += dt

        # Build world state for subsystems
        world_state = {
            "player_position": self.player.position,
            "player_facing": self.player.facing,
            "simulation_time": self.simulation_time,
            "player_has_keycard": self.player.has_keycard,
            "player_has_tool": self.player.has_tool
        }

        # Process player action
        if player_action:
            self._process_player_action(player_action, world_state)

        # Update all subsystems
        self.faction_system.update(dt)
        self.npc_manager.update(dt, world_state)
        self.prop_system.update(dt)

        # Update stealth - check NPC awareness
        player_detected = False
        for npc_id, npc in self.npc_manager.npcs.items():
            awareness = self.stealth_system.check_npc_awareness(
                npc_id,
                npc.position,
                npc.facing,
                self.player.position,
                self.world_tiles
            )

            if awareness > 0.5:
                player_detected = True

            # Update stealth feedback symbols based on awareness
            investigating = npc.state.value == 'investigating' if hasattr(npc, 'state') else False
            self.stealth_feedback.update_npc_alerts_from_awareness(npc_id, awareness, investigating)

            # Check if NPC heard noise
            noise = self.stealth_system.check_noise_heard(npc.position)
            if noise:
                # NPC investigates noise
                # (This would trigger NPC behavior changes)
                pass

        # Propagate prop noises to stealth system
        for pos, radius in self.prop_system.get_active_noises():
            # Already handled in prop system
            pass

        self.stealth_system.update(dt, world_state)

        # Update stealth feedback visuals
        self.stealth_feedback.update(dt)

        # Update heat system
        player_in_restricted = self._check_player_in_restricted_zone()
        self.heat_system.update(dt, player_detected, player_in_restricted)

        # Get current heat/glitch values
        current_heat = self.heat_system.get_heat_value()
        glitch_intensity = self.heat_system.get_glitch_intensity()

        # Update toddler system (TIER 4: THE REALITY CATALYST)
        toddler_effects = self.toddler_system.update(
            dt,
            self.player.position,
            current_heat,
            self.world_tiles
        )

        # Apply toddler effects to heat buildup
        if toddler_effects.get('in_distortion_field'):
            heat_multiplier = toddler_effects.get('heat_multiplier', 1.0)
            # Heat builds faster near toddler (implemented via multiplier in heat system)
            # This would be used if heat system tracked heat buildup rate

        # Update reality glitch system with toddler amplification (MASK CRACKING BEFORE IT BREAKS)
        # Toddler makes glitches spawn more frequently
        amplified_glitch_intensity = glitch_intensity * toddler_effects.get('glitch_multiplier', 1.0)
        self.glitch_system.update(dt, current_heat, min(1.0, amplified_glitch_intensity))

        # Reality break effects (Heat 5)
        reality_break_effects = {}
        if self.heat_system.is_reality_breaking():
            reality_break_effects = self.heat_system.get_reality_break_effects()

        # Micro-glitch effects (Heat 3-4.5)
        micro_glitches = self.glitch_system.get_glitch_rendering_data()

        # Stealth feedback (ANSI alert symbols and noise ripples)
        stealth_feedback = self.stealth_feedback.get_all_rendering_data()

        # Generate NPC dialogue (THE COGNITIVE DISSONANCE HAPPENS HERE)
        npc_dialogues = self._generate_npc_dialogues(current_heat, glitch_intensity)

        # Update renderer strain system (TIER 5: WOLF3D MASK FAILING UNDER AAA LOAD)
        toddler_strain = toddler_effects.get('reality_strain', 0.0)
        npc_count = len(self.npc_manager.npcs)
        renderer_strain_data = self.renderer_strain.update(dt, npc_count, current_heat, toddler_strain)

        # Get toddler rendering data (visible at high heat)
        toddler_rendering = self.toddler_system.get_rendering_data()

        # CHECK FOR HEAT 5 REVELATION EVENT (THE CLIMAX)
        toddler_visibility = toddler_rendering.get('visibility', 0.0)
        renderer_strain_value = renderer_strain_data.get('cumulative_strain', 0.0)

        # Calculate mask integrity (inverse of strain)
        mask_integrity = max(0.0, 1.0 - renderer_strain_value)

        if self.heat5_revelation.should_trigger(
            heat_level=current_heat,
            mask_integrity=mask_integrity,
            toddler_presence=toddler_visibility,
            renderer_strain=renderer_strain_value
        ):
            # TRIGGER THE REVELATION
            simulation_state = {
                'renderer_strain': renderer_strain_data,
                'toddler': toddler_rendering,
                'toddler_effects': toddler_effects,
                'micro_glitches': micro_glitches,
                'npcs': self.npc_manager.get_all_npc_states()
            }
            self.heat5_revelation.trigger(simulation_state)

        # Update revelation event (progressive phases)
        if self.heat5_revelation.state.triggered:
            simulation_state = {
                'renderer_strain': renderer_strain_data,
                'toddler': toddler_rendering,
                'npcs': self.npc_manager.get_all_npc_states()
            }
            self.heat5_revelation.update(dt, simulation_state)

        # Get revelation effects for rendering
        revelation_effects = self.heat5_revelation.get_revelation_effects()

        # Calculate frame time for profiler display
        frame_end = time.time()
        frame_time = frame_end - frame_start
        self.frame_times.append(frame_time)
        if len(self.frame_times) > 60:
            self.frame_times.pop(0)
        self.avg_frame_time = sum(self.frame_times) / len(self.frame_times)

        # Override NPC dialogues if Heat 5 Revelation is active
        npcs_for_rendering = self.npc_manager.get_all_npc_states()
        if revelation_effects.get('npcs_confessing'):
            npcs_for_rendering = force_revelation_dialogue_override(
                npcs_for_rendering,
                revelation_effects.get('phase', 0)
            )

        # Return rendering data (with AAA AI dialogue bleeding through)
        return {
            "npcs": npcs_for_rendering,
            "npc_dialogues": npc_dialogues,
            "props": [
                {
                    "position": prop.position,
                    "type": prop.prop_type.value,
                    "state": prop.state.value
                }
                for prop in self.prop_system.get_all_props()
            ],
            "heat_level": self.heat_system.get_heat_level().value,
            "heat_stars": self.heat_system.get_hud_display(),
            "lockdown_active": self.heat_system.is_lockdown_active(),
            "reality_breaking": self.heat_system.is_reality_breaking(),
            "reality_stability": self.heat_system.get_reality_stability(),
            "reality_break_effects": reality_break_effects,
            "micro_glitches": micro_glitches,
            "stealth_feedback": stealth_feedback,
            "stealth_detection_level": self.stealth_system.get_detection_level(),
            "faction_states": self._get_faction_summary(),
            "simulation_messages": self._get_simulation_messages(),

            # TIER 4: TODDLER (The invisible catalyst)
            "toddler": toddler_rendering,
            "toddler_effects": toddler_effects,

            # TIER 5: RENDERER STRAIN (Wolf3D mask failing)
            "renderer_strain": renderer_strain_data,

            # HEAT 5 REVELATION (The moment of truth)
            "revelation": revelation_effects
        }

    def _process_player_action(self, action: Dict[str, Any], world_state: Dict[str, Any]):
        """Process a player action and propagate through systems"""
        action_type = action.get("type")

        if action_type == "move":
            new_pos = action.get("position")
            if new_pos:
                # Create footstep noise
                self.stealth_system.create_noise(
                    self.player.position,
                    0.3,
                    "footstep"
                )
                # Add visual noise ripple
                self.stealth_feedback.add_noise_ripple(self.player.position, 2.0, 0.2)
                self.player.position = new_pos

        elif action_type == "interact_prop":
            prop_id = action.get("prop_id")
            interaction = action.get("interaction", "use")
            result = self.prop_system.interact_with_prop(prop_id, interaction, world_state)

            if result.get("success"):
                # Propagate effects
                effects = result.get("effects", [])

                if "heat_increased_minor" in effects:
                    self.heat_system.trigger_event("vandalism", self.player.position)
                elif "heat_increased_major" in effects:
                    self.heat_system.trigger_event("attack_npc", self.player.position)
                elif "alarm_triggered" in effects:
                    self.heat_system.trigger_event("trigger_alarm", self.player.position)

        elif action_type == "attack_npc":
            npc_id = action.get("npc_id")
            npc = self.npc_manager.get_npc(npc_id)
            if npc:
                # Record in faction memory
                self.faction_system.record_player_action(
                    "attack",
                    self.player.position,
                    severity=1.0,
                    witnessed_by={npc_id},
                    affected_factions={npc.faction}
                )

                # Add heat
                self.heat_system.trigger_event("attack_npc", self.player.position)

                # Create noise
                self.stealth_system.create_noise(
                    self.player.position,
                    0.9,
                    "attack"
                )
                # Add visual noise ripple
                self.stealth_feedback.add_noise_ripple(self.player.position, 10.0, 0.9)

    def _check_player_in_restricted_zone(self) -> bool:
        """Check if player is in a restricted area"""
        # Simplified - would check tile types
        x, y, z = self.player.position
        tile = self.world_tiles.get((x, y, z))
        if tile:
            return "SECURITY" in tile.type or "STAFF" in tile.type
        return False

    def _get_faction_summary(self) -> Dict[str, Any]:
        """Get summary of faction states"""
        summary = {}
        for faction_id, faction in self.faction_system.factions.items():
            summary[faction_id.value] = {
                "alert_level": faction.alert_level.value,
                "reputation": self.faction_system.get_reputation(faction_id),
                "active_npcs": faction.get_active_npc_count()
            }
        return summary

    def _get_simulation_messages(self) -> List[str]:
        """Get messages about simulation state"""
        messages = []

        # Heat messages
        heat_desc = self.heat_system.get_escalation_description()
        if heat_desc:
            messages.append(f"[HEAT] {heat_desc}")

        # Reality break messages
        if self.heat_system.is_reality_breaking():
            messages.append("[CRITICAL] SIMULATION INTEGRITY COMPROMISED")
            messages.append(f"[STATUS] Reality Stability: {self.heat_system.get_reality_stability():.1f}%")
            messages.append("[WARNING] Modern engine exposure detected")

        # Faction coordination
        if self.faction_system.is_coordinated_response_active():
            messages.append("[FACTION] Multiple factions coordinating against you")

        return messages

    def _generate_npc_dialogues(self, heat_level: float, glitch_intensity: float) -> Dict[str, Dict[str, str]]:
        """
        Generate dialogue for all NPCs based on heat level.

        This is where Wolf3D NPCs start talking about their work schedules.
        This is where the AAA AI bleeds through.
        This is the cognitive dissonance engine.
        """
        dialogues = {}

        for npc_id, npc in self.npc_manager.npcs.items():
            npc_dialogue = {}

            # Get regular dialogue bark
            bark = self.dialogue_manager.get_npc_bark(
                npc_id=npc_id,
                npc_faction=npc.faction.value if hasattr(npc, 'faction') else 'unknown',
                npc_state=npc.state.value if hasattr(npc, 'state') else 'idle',
                heat_level=heat_level,
                has_schedule=hasattr(npc, 'schedule') and bool(npc.schedule),
                is_patrolling=npc.state.value == 'patrolling' if hasattr(npc, 'state') else False
            )

            if bark:
                npc_dialogue['bark'] = bark

            # Get GOAP goal overlay (flickering at Heat 3+, always at Heat 5)
            if hasattr(npc, 'current_goal'):
                goal_text = self.dialogue_manager.get_goap_goal_text(
                    npc_id=npc_id,
                    current_goal=npc.current_goal,
                    heat_level=heat_level,
                    glitch_intensity=glitch_intensity
                )
                if goal_text:
                    npc_dialogue['goal_overlay'] = goal_text

            if npc_dialogue:
                dialogues[npc_id] = npc_dialogue

        return dialogues

    def get_player_position(self) -> Tuple[int, int, int]:
        """Get player position"""
        return self.player.position

    def set_player_position(self, position: Tuple[int, int, int]):
        """Set player position"""
        self.player.position = position

    def get_simulation_stats(self) -> Dict[str, Any]:
        """Get simulation statistics (for reality break display)"""
        return {
            "total_npcs": len(self.npc_manager.npcs),
            "active_factions": len(self.faction_system.factions),
            "heat_level": self.heat_system.get_heat_value(),
            "reality_stability": self.heat_system.get_reality_stability(),
            "avg_frame_time_ms": self.avg_frame_time * 1000,
            "target_fps": 60,
            "current_fps": int(1.0 / max(0.001, self.avg_frame_time))
        }


def random_int(min_val: int, max_val: int) -> int:
    """Helper for random int"""
    import random
    return random.randint(min_val, max_val)
