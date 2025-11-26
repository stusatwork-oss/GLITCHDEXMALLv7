"""
Toddler Presence System – Audio, Shadow, Intensity, Chaos Events
"""

import random
from typing import List, Tuple, Optional, Dict
from enum import Enum


class ToddlerStage(Enum):
    """Toddler intensity stages based on playtime"""
    NONE = 0         # 0–300 seconds (0–5 min)
    ONE = 1          # 300–900 seconds (5–15 min)
    TWO = 2          # 900+ seconds (15+ min)


class ToddlerSystem:
    """Manages the invisible toddler's presence and effects"""

    def __init__(self):
        """Initialize the toddler system"""
        self.cry_counter = 0
        self.shadow_intensity = 0.0  # 0.0 to 1.0
        self.chaos_events: List[str] = []
        self.stage = ToddlerStage.NONE

        # Audio sounds (textual descriptions)
        self.stage_1_cries = [
            "A distant wail echoes through the mall.",
            "You hear a faint cry from somewhere deeper inside.",
            "A baby's whimper, muffled by vents.",
        ]

        self.stage_2_wails = [
            "Frequent cries echo from multiple directions.",
            "The wails are getting louder. And closer.",
            "A child's screams, impossible to ignore now.",
            "The crying is constant. It's everywhere.",
        ]

        self.stage_3_screams = [
            "SCREAMING. Constant, piercing screaming.",
            "THE CRYING DOESN'T STOP. IT'S EVERYWHERE.",
            "Wails that seem to come from the walls themselves.",
            "The sound is unbearable. It won't stop.",
        ]

        self.chaos_event_descriptions = [
            "The escalators rattle. Metal on metal. Awful sound.",
            "Fluorescent lights strobe. On. Off. On. Off.",
            "Everyone in the food court suddenly stands up and leaves.",
            "The mall seems to... shift. Corridors look slightly different.",
            "A shadow passes across the wall. You don't see what casts it.",
            "The vents hum with a new frequency. Discordant. Wrong.",
            "Objects on shelves rattle without being touched.",
            "The air feels colder. Much colder.",
            "A shape moves at the edge of your vision. It's gone when you look.",
        ]

    def update(self, playtime_seconds: int) -> Tuple[ToddlerStage, List[str]]:
        """
        Update toddler state based on playtime.
        Returns (new_stage, new_messages).
        """
        old_stage = self.stage
        messages = []

        # Determine stage based on playtime
        if playtime_seconds < 300:  # First 5 minutes
            self.stage = ToddlerStage.NONE
            self.shadow_intensity = 0.0
        elif playtime_seconds < 900:  # 5–15 minutes
            self.stage = ToddlerStage.ONE
            self.shadow_intensity = min(0.5, (playtime_seconds - 300) / 600)
        else:  # 15+ minutes
            self.stage = ToddlerStage.TWO
            self.shadow_intensity = min(1.0, (playtime_seconds - 900) / 600 + 0.5)

        # Trigger stage transition messages
        if self.stage != old_stage:
            if self.stage == ToddlerStage.ONE:
                messages.append("[TODDLER STAGE 1] First cry heard. Something's in the mall.")
            elif self.stage == ToddlerStage.TWO:
                messages.append("[TODDLER STAGE 2] Intensity escalates. Get out.")

        return self.stage, messages

    def get_audio_message(self) -> Optional[str]:
        """
        Get audio message for current stage.
        Returns None if no audio this tick (to avoid overwhelming the player).
        """
        if self.stage == ToddlerStage.NONE:
            return None
        elif self.stage == ToddlerStage.ONE:
            # Random chance of cry every ~30 seconds (1 in 30 ticks at 1 tick/sec)
            if random.random() < 0.033:
                return random.choice(self.stage_1_cries)
        elif self.stage == ToddlerStage.TWO:
            # More frequent wails
            if random.random() < 0.1:
                return random.choice(self.stage_2_wails)
            if random.random() < 0.05:
                return random.choice(self.stage_3_screams)

        return None

    def get_shadow_intensity(self) -> float:
        """Get shadow visibility (0.0 to 1.0)"""
        return self.shadow_intensity

    def should_trigger_chaos_event(self) -> bool:
        """Check if a chaos event should trigger (Stage 2 only)"""
        if self.stage != ToddlerStage.TWO:
            return False
        # ~10% chance per tick during stage 2
        return random.random() < 0.1

    def get_chaos_event(self) -> str:
        """Get a random chaos event description"""
        return random.choice(self.chaos_event_descriptions)

    def get_shadow_description(self) -> Optional[str]:
        """Get text description of shadow visibility"""
        if self.shadow_intensity < 0.1:
            return None
        elif self.shadow_intensity < 0.3:
            return "A shadow flickers at the edge of your vision."
        elif self.shadow_intensity < 0.6:
            return "Shadows move in the corners of the mall. You don't want to look too close."
        elif self.shadow_intensity < 0.9:
            return "The shadow fills most of the visible space. It's watching."
        else:
            return "Everything is shadow. You can barely see."

    def get_stage(self) -> ToddlerStage:
        """Get current toddler stage"""
        return self.stage

    def get_stage_number(self) -> int:
        """Get stage as integer (0, 1, 2)"""
        return self.stage.value

    def apply_visual_distortion(self, strength: float = None) -> Dict[str, float]:
        """
        Generate visual distortion parameters for renderer.
        Strength based on stage and shadow intensity.
        Enhanced for Wolfenstein 3D-style rendering.
        """
        if strength is None:
            strength = self.shadow_intensity

        # Base distortions scaled by stage
        base_intensity = strength

        # Add random spikes during Stage 2
        if self.stage == ToddlerStage.TWO:
            if random.random() < 0.1:
                base_intensity = min(1.0, base_intensity + random.uniform(0.2, 0.5))

        distortions = {
            "chromatic_aberration": base_intensity * 0.5,  # Color separation/shift
            "vignette": base_intensity * 0.7,  # Screen edge darkening
            "wobble": base_intensity * 0.3,  # Screen shake/wobble
            "glitch": base_intensity * 0.4,  # Random pixel corruption
            "oversaturation": base_intensity * 0.2,  # Color oversaturation
            "texture_corruption": base_intensity * 0.3,  # Texture glitches
            "scanlines": base_intensity * 0.2,  # CRT scanline effect
        }

        # Stage-specific effects
        if self.stage == ToddlerStage.TWO:
            # Extreme corruption in final stage
            distortions["glitch"] = min(1.0, distortions["glitch"] * 2.0)
            distortions["vignette"] = min(1.0, distortions["vignette"] * 1.5)

            # Occasional full-screen corruption
            if random.random() < 0.05:
                distortions["screen_tear"] = 1.0
            else:
                distortions["screen_tear"] = 0.0

        return distortions

    def get_npc_reaction_intensity(self) -> float:
        """Get intensity multiplier for NPC reactions (0.0 to 1.0)"""
        if self.stage == ToddlerStage.NONE:
            return 0.0
        elif self.stage == ToddlerStage.ONE:
            return 0.5
        else:
            return 1.0

    def apply_artifact_weirdness_boost(self, num_artifacts: int) -> Tuple[ToddlerStage, float]:
        """
        Apply weirdness boost when player carries multiple artifacts.
        Each artifact amplifies toddler presence.
        Returns (effective_stage, weirdness_factor).
        """
        if num_artifacts == 0:
            return self.stage, 1.0

        # Each artifact adds 20% weirdness boost
        weirdness_factor = 1.0 + (num_artifacts * 0.2)

        # At 4+ artifacts, escalate stage
        if num_artifacts >= 4 and self.stage == ToddlerStage.ONE:
            return ToddlerStage.TWO, weirdness_factor
        elif num_artifacts >= 3 and self.stage == ToddlerStage.NONE:
            return ToddlerStage.ONE, weirdness_factor

        return self.stage, weirdness_factor

    def get_pressure_text(self) -> str:
        """Get urgency text based on stage"""
        if self.stage == ToddlerStage.NONE:
            return ""
        elif self.stage == ToddlerStage.ONE:
            return "You should probably leave soon."
        else:
            return "GET OUT NOW. THIS IS NOT SAFE."

    def get_tile_presence_multiplier(self, tile_type: str) -> float:
        """
        Get multiplier for toddler presence at specific tile type.
        Some tiles amplify the presence (service halls, food court with echoes).
        """
        multipliers = {
            "FOOD_COURT": 1.3,          # Crowds, noise, echoes
            "SERVICE_HALL": 1.5,        # Vents carry sound
            "ANCHOR_STORE": 1.2,        # Large echoing space
            "ESCALATOR_UP": 1.1,
            "ESCALATOR_DOWN": 1.1,
            "CORRIDOR": 1.0,            # Baseline
            "STORE_BORED": 1.0,
            "STORE_MILO_OPTICS": 1.0,
        }
        return multipliers.get(tile_type, 1.0)
