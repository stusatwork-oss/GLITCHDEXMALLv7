"""
REALITY GLITCH SYSTEM
The facade slips. The simulation reveals its true nature.

What appears to be a coffee-spilled 1992 Wolf3D clone is actually running
on sophisticated modern rendering tech. The toddler's presence causes the
mask to crack, revealing glimpses of what's really underneath.
"""

import random
import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class GlitchEvent:
    """A moment where modern rendering bleeds through"""
    name: str
    description: str
    intensity: float  # 0.0 to 1.0
    duration: int  # frames
    active: bool = False
    remaining_frames: int = 0


class RealityGlitch:
    """
    Manages moments where the game's true sophisticated nature is revealed.

    The toddler doesn't just corrupt the visuals - it breaks the SIMULATION
    itself, causing modern rendering techniques to bleed through the retro facade.
    """

    def __init__(self):
        self.active_glitches: List[GlitchEvent] = []

        # Glitch types that can trigger
        self.glitch_catalog = {
            # LIGHTING GLITCHES - Ray traced lighting bleeds through
            "raytraced_shadows": GlitchEvent(
                "RAYTRACED_SHADOWS",
                "Shadows become too realistic - soft edges, proper occlusion",
                0.7, 30
            ),

            "global_illumination": GlitchEvent(
                "GLOBAL_ILLUMINATION",
                "Light bounces appear - walls glow with reflected light",
                0.8, 45
            ),

            "volumetric_lighting": GlitchEvent(
                "VOLUMETRIC_LIGHT",
                "Light shafts through vents - god rays that shouldn't exist in 1992",
                0.6, 60
            ),

            # TEXTURE GLITCHES - Too much detail
            "photorealistic_leak": GlitchEvent(
                "PHOTOREALISTIC_TEXTURE",
                "Wall textures momentarily become photographs - too detailed",
                0.9, 20
            ),

            "procedural_detail": GlitchEvent(
                "PROCEDURAL_SURFACE",
                "Surfaces gain infinite detail - fractal complexity emerges",
                0.8, 40
            ),

            "normal_mapping": GlitchEvent(
                "NORMAL_MAPS",
                "Walls gain depth that shouldn't be there - bumps and grooves appear",
                0.7, 35
            ),

            # POST-PROCESSING GLITCHES - Modern effects leak
            "depth_of_field": GlitchEvent(
                "DEPTH_OF_FIELD",
                "Background blurs naturally - like a camera lens",
                0.6, 50
            ),

            "motion_blur": GlitchEvent(
                "MOTION_BLUR",
                "Movement smears realistically - temporal sampling bleeds through",
                0.5, 25
            ),

            "bloom_leak": GlitchEvent(
                "BLOOM_EFFECT",
                "Lights glow and bleed - HDR bloom from the real renderer",
                0.6, 40
            ),

            "ambient_occlusion": GlitchEvent(
                "SCREEN_SPACE_AO",
                "Corners darken naturally - contact shadows that Wolf3D couldn't do",
                0.7, 45
            ),

            # PHYSICS GLITCHES - Things move when they shouldn't
            "particle_systems": GlitchEvent(
                "PARTICLE_SIM",
                "Dust particles float in air - full physics simulation visible",
                0.8, 60
            ),

            "cloth_physics": GlitchEvent(
                "CLOTH_SIMULATION",
                "Fabric ripples, curtains move - soft body physics emerge",
                0.7, 30
            ),

            # GEOMETRY GLITCHES - Too many polygons
            "subdivision_surface": GlitchEvent(
                "MESH_SUBDIVISION",
                "Walls become smooth curves - subdivision surfaces appear",
                0.9, 25
            ),

            "tessellation": GlitchEvent(
                "DYNAMIC_TESSELLATION",
                "Geometry gains impossible detail - millions of polygons",
                0.95, 20
            ),

            # REALITY BREAKS - Full simulation crack
            "matrix_glitch": GlitchEvent(
                "SIMULATION_BREACH",
                "The mall flickers - you see the real engine underneath",
                1.0, 15
            ),

            "recursive_reflection": GlitchEvent(
                "INFINITE_MIRRORS",
                "Reflections reflect reflections - ray traced recursion exposed",
                0.85, 35
            ),
        }

    def update(self, toddler_stage: int, shadow_intensity: float,
               artifact_count: int) -> List[str]:
        """
        Update glitch state. Returns list of new glitch messages.
        The more intense the toddler presence, the more the facade cracks.
        """
        messages = []

        # Update active glitches
        for glitch in self.active_glitches[:]:
            glitch.remaining_frames -= 1
            if glitch.remaining_frames <= 0:
                glitch.active = False
                self.active_glitches.remove(glitch)

        # Calculate glitch probability
        base_chance = 0.0

        if toddler_stage == 0:
            base_chance = 0.001  # Extremely rare hints
        elif toddler_stage == 1:
            base_chance = 0.02 + (shadow_intensity * 0.03)
        elif toddler_stage == 2:
            base_chance = 0.08 + (shadow_intensity * 0.12)

        # Artifacts amplify reality breaks
        base_chance *= (1.0 + artifact_count * 0.15)

        # Try to trigger new glitch
        if random.random() < base_chance and len(self.active_glitches) < 3:
            new_glitch = self._select_glitch(toddler_stage)
            if new_glitch:
                new_glitch.active = True
                new_glitch.remaining_frames = new_glitch.duration
                self.active_glitches.append(new_glitch)

                # Generate message
                if toddler_stage == 0:
                    msg = f"[GLITCH] Something wrong with the rendering... {new_glitch.name}"
                elif toddler_stage == 1:
                    msg = f"[REALITY SLIP] {new_glitch.description}"
                else:
                    msg = f"[SIMULATION BREAKING] {new_glitch.description.upper()}"

                messages.append(msg)

        return messages

    def _select_glitch(self, stage: int) -> GlitchEvent:
        """Select a random glitch appropriate for the stage"""

        # Stage 0: Only subtle texture/lighting glitches
        if stage == 0:
            candidates = ["normal_mapping", "ambient_occlusion", "motion_blur"]

        # Stage 1: More variety, medium intensity
        elif stage == 1:
            candidates = [
                "raytraced_shadows", "volumetric_lighting", "procedural_detail",
                "depth_of_field", "bloom_leak", "particle_systems", "ambient_occlusion"
            ]

        # Stage 2: Everything, including reality breaks
        else:
            candidates = list(self.glitch_catalog.keys())

        if not candidates:
            return None

        glitch_name = random.choice(candidates)
        # Create a copy of the glitch template
        template = self.glitch_catalog[glitch_name]
        return GlitchEvent(
            template.name, template.description,
            template.intensity, template.duration
        )

    def get_active_effects(self) -> Dict[str, float]:
        """
        Get rendering modifications for currently active glitches.
        Returns dict of effect_name -> intensity.
        """
        effects = {}

        for glitch in self.active_glitches:
            # Fade in/out based on remaining frames
            fade_in_frames = 5
            fade_out_frames = 10

            if glitch.remaining_frames > glitch.duration - fade_in_frames:
                # Fading in
                progress = (glitch.duration - glitch.remaining_frames) / fade_in_frames
                intensity = glitch.intensity * progress
            elif glitch.remaining_frames < fade_out_frames:
                # Fading out
                intensity = glitch.intensity * (glitch.remaining_frames / fade_out_frames)
            else:
                # Full intensity
                intensity = glitch.intensity

            effects[glitch.name] = intensity

        return effects

    def should_show_wireframe(self) -> bool:
        """Check if wireframe should bleed through (geometry glitches)"""
        for glitch in self.active_glitches:
            if glitch.name in ["MESH_SUBDIVISION", "DYNAMIC_TESSELLATION"]:
                return random.random() < 0.3
        return False

    def should_show_debug_info(self) -> bool:
        """Check if debug info should appear (simulation breaks)"""
        for glitch in self.active_glitches:
            if glitch.name in ["SIMULATION_BREACH", "INFINITE_MIRRORS"]:
                return random.random() < 0.5
        return False

    def get_photorealistic_intensity(self) -> float:
        """Get intensity of photorealistic texture bleeding"""
        for glitch in self.active_glitches:
            if glitch.name == "PHOTOREALISTIC_TEXTURE":
                return glitch.intensity
        return 0.0

    def get_lighting_complexity(self) -> float:
        """Get how complex lighting should be (0=Wolf3D, 1=ray traced)"""
        max_complexity = 0.0

        lighting_glitches = {
            "RAYTRACED_SHADOWS": 0.7,
            "GLOBAL_ILLUMINATION": 0.9,
            "VOLUMETRIC_LIGHT": 0.6,
        }

        for glitch in self.active_glitches:
            if glitch.name in lighting_glitches:
                complexity = lighting_glitches[glitch.name] * glitch.intensity
                max_complexity = max(max_complexity, complexity)

        return max_complexity

    def get_detail_multiplier(self) -> float:
        """Get texture detail multiplier (1.0=normal, 4.0=photorealistic)"""
        multiplier = 1.0

        for glitch in self.active_glitches:
            if glitch.name == "PHOTOREALISTIC_TEXTURE":
                multiplier = max(multiplier, 4.0 * glitch.intensity)
            elif glitch.name == "PROCEDURAL_SURFACE":
                multiplier = max(multiplier, 3.0 * glitch.intensity)
            elif glitch.name == "NORMAL_MAPS":
                multiplier = max(multiplier, 2.0 * glitch.intensity)

        return multiplier

    def get_post_processing_effects(self) -> Dict[str, float]:
        """Get modern post-processing effects that are bleeding through"""
        effects = {
            "depth_of_field": 0.0,
            "motion_blur": 0.0,
            "bloom": 0.0,
            "ambient_occlusion": 0.0,
        }

        for glitch in self.active_glitches:
            if glitch.name == "DEPTH_OF_FIELD":
                effects["depth_of_field"] = glitch.intensity
            elif glitch.name == "MOTION_BLUR":
                effects["motion_blur"] = glitch.intensity
            elif glitch.name == "BLOOM_EFFECT":
                effects["bloom"] = glitch.intensity
            elif glitch.name == "SCREEN_SPACE_AO":
                effects["ambient_occlusion"] = glitch.intensity

        return effects

    def generate_debug_text(self) -> List[str]:
        """Generate fake debug text that appears during simulation breaks"""
        debug_lines = [
            "RENDER_ENGINE: Unity 2023.1.4f1",
            "PIPELINE: Universal RP (Forward+)",
            "DRAWCALLS: 2847 (batched: 2203)",
            "TRIS: 184,392 | VERTS: 94,281",
            "TEXTURES: 2.4GB VRAM",
            "RAYTRACING: ENABLED (DXR 1.1)",
            "LIGHTING: Realtime GI + Baked",
            "SHADOWS: PCF 5x5 + Contact",
            "POST: TAA, Bloom, AO, DOF, MB",
            "TARGET: 60 FPS | CURRENT: 58.3",
            "",
            "SIMULATION_LAYER: MALL_01",
            "ENTITY_COUNT: 847 (visible: 23)",
            "PHYSICS_ACTIVE: 14 rigid bodies",
            "AI_THREADS: 4 (pathfinding active)",
            "",
            "[WARNING] Presence detection spike",
            "[ERROR] Facade integrity: 67%",
            "[CRITICAL] Toddler containment failing",
        ]

        # Return random subset
        count = random.randint(5, 10)
        return random.sample(debug_lines, min(count, len(debug_lines)))

    def is_reality_breaking(self) -> bool:
        """Check if we're in full reality break mode"""
        for glitch in self.active_glitches:
            if glitch.name in ["SIMULATION_BREACH", "INFINITE_MIRRORS"]:
                if glitch.intensity > 0.8:
                    return True
        return False
