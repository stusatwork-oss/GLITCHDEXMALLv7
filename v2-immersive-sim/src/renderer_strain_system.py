"""
RENDERER STRAIN SYSTEM - The Wolf3D Mask Failing Under AAA Load
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The raycaster was NEVER built for this.

It was built for:
- 20 sprites max
- Simple AI (patrol, shoot, die)
- 320x200 resolution

What it's actually rendering:
- 50+ AI agents with GOAP
- A* pathfinding for every NPC
- Faction memory and gossip systems
- Vision cones and stealth calculations
- Heat system tracking thousands of events

At high heat + high NPC counts, the renderer VISIBLY STRUGGLES:
- Fake frame drops (smooth 60fps → stuttering)
- Error messages: "[WARN] TOO MANY AI AGENTS FOR RAYCAST RENDERER"
- "Buffer underrun detected"
- "Fallback renderer unavailable"
- FPS counter drops (even though it's fake)

The game is LYING about its performance to maintain the retro aesthetic.
At Heat 5, it stops lying.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import random
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class StrainLevel(Enum):
    """Renderer strain levels"""
    STABLE = "stable"  # No issues
    MINOR = "minor"  # Occasional warnings
    MODERATE = "moderate"  # Frequent warnings, slight stutters
    HEAVY = "heavy"  # Constant warnings, fake frame drops
    CRITICAL = "critical"  # System failing, error messages everywhere
    WARMUP = "warmup"  # Shader warmup ritual - renderer psychologically preparing


class WarmupPhase(Enum):
    """Shader warmup phase states"""
    INACTIVE = "inactive"
    INIT_SHADERS = "init_shaders"
    PRIME_HARDWARE = "prime_hardware"
    BLESS_PIPELINE = "bless_pipeline"
    RUN_DOOM = "run_doom"  # The sacred ritual
    PRETEND_SUCCESS = "pretend_success"
    RESUME = "resume"


@dataclass
class PerformanceError:
    """A fake performance error/warning"""
    message: str
    error_type: str  # "WARNING", "ERROR", "CRITICAL"
    timestamp: float
    duration: float = 3.0  # How long to show error
    persistent: bool = False  # Stays on screen until resolved


@dataclass
class FrameDropEvent:
    """A fake frame drop (rendering stutter)"""
    timestamp: float
    duration: float  # How long the stutter lasts
    intensity: float  # 0.0 to 1.0 (how severe)


class RendererStrainSystem:
    """
    Simulates renderer strain from AAA AI under Wolf3D mask.

    The philosophy:
    - Low NPC count + low heat = stable (the lie holds)
    - High NPC count OR high heat = warnings appear
    - High NPC count AND high heat = critical strain
    - Toddler presence amplifies strain significantly
    """

    def __init__(self):
        # Active errors/warnings
        self.active_errors: List[PerformanceError] = []

        # Frame drop simulation
        self.frame_drop_events: List[FrameDropEvent] = []
        self.time_since_last_frame_drop = 0.0

        # Fake FPS counter
        self.displayed_fps = 60.0
        self.target_fps = 60.0

        # Strain accumulation
        self.cumulative_strain = 0.0
        self.strain_level = StrainLevel.STABLE

        # SHADER WARMUP PHASE (the renderer's prayer ritual)
        self.warmup_phase = WarmupPhase.INACTIVE
        self.warmup_timer = 0.0
        self.warmup_triggered_this_session = False
        self.doom_frames_remaining = 0  # Frames left of DOOM ritual

        # Error message catalog
        self.warning_messages = [
            "[WARN] Raycaster: Too many active sprites (limit: 20, current: {npc_count})",
            "[WARN] AI system: Pathfinding budget exceeded",
            "[WARN] Memory: Agent state buffer approaching capacity",
            "[WARN] Render pipeline: Frame budget exceeded by {overdraw}ms",
            "[WARN] Wolf3D renderer not designed for {npc_count} concurrent agents",
            "[WARN] Vision cone calculations exceeding frame time budget",
            "[WARN] Faction system: Gossip propagation delayed",
            "[WARN] Stealth system: Sound propagation queue overflow"
        ]

        self.error_messages = [
            "[ERROR] Buffer underrun detected in sprite renderer",
            "[ERROR] Raycaster: Failed to allocate memory for agent {agent_id}",
            "[ERROR] AI pathfinding: Exceeded maximum iterations",
            "[ERROR] Render queue: Dropped {drop_count} draw calls",
            "[ERROR] Wolf3D mode incompatible with modern AI load",
            "[ERROR] Failed to maintain 60 FPS target (actual: {fps})",
        ]

        self.critical_messages = [
            "[CRITICAL] Renderer strain at maximum capacity",
            "[CRITICAL] Fallback renderer unavailable",
            "[CRITICAL] Wolf3D raycaster cannot handle AAA AI systems",
            "[CRITICAL] Frame time budget exceeded by {overdraw}ms - stuttering inevitable",
            "[CRITICAL] System attempting to render {npc_count} agents with 1993 technology",
            "[CRITICAL] SIMULATION INTEGRITY COMPROMISED",
            "[FATAL] TODDLER IN SYSTEM BUS",
            "[ERR] TOO MANY AGENTS FOR RAYCASTER",
            "[ERR] CANNOT COMPILE SHADER THAT DOES NOT EXIST"
        ]

        # WARMUP PHASE MESSAGES (the renderer's coping mechanisms)
        self.warmup_messages = [
            "[INFO] Shader cache warming...",
            "[INFO] Mask integrity checking...",
            "[INFO] VRAM stretching...",
            "[INFO] Compiling temporal stabilizer...",
            "[INFO] Blessing pipeline...",
            "[INFO] Preparing hardware that does not exist...",
            "[INFO] Attempting to host Vulkan on 256-color raycaster...",
            "[INFO] Running pre-flight jank scrubbing...",
            "[INFO] Letting the silicon breathe...",
            "[RITUAL] Compiling shaders that do not exist...",
            "[RITUAL] Allocating textures that cannot fit...",
            "[RITUAL] Priming memory that is not available...",
            "[RITUAL] Please work please work please work...",
            "[RITUAL] Running DOOM for psychological stability..."  # THE SACRED RITE
        ]

    def update(self, dt: float, npc_count: int, current_heat: float,
               toddler_strain: float = 0.0) -> Dict[str, Any]:
        """
        Update renderer strain state.

        Args:
            dt: Delta time
            npc_count: Number of active NPCs
            current_heat: Current heat level (0-5)
            toddler_strain: Reality strain from toddler (0-1)

        Returns:
            Strain state and effects
        """
        self.time_since_last_frame_drop += dt

        # Calculate strain level
        strain = self._calculate_strain(npc_count, current_heat, toddler_strain)
        self.cumulative_strain = strain

        # Check for SHADER WARMUP PHASE trigger conditions
        self._check_warmup_trigger(strain, current_heat, npc_count, toddler_strain, dt)

        # Update warmup ritual if active
        if self.warmup_phase != WarmupPhase.INACTIVE:
            self._update_warmup_ritual(dt)
            # During warmup, strain level is locked to WARMUP
            self.strain_level = StrainLevel.WARMUP
        else:
            self.strain_level = self._get_strain_level(strain)

        # Update FPS display (fake degradation)
        self._update_fake_fps(strain, dt)

        # Spawn errors/warnings (suppressed during warmup ritual)
        if self.warmup_phase == WarmupPhase.INACTIVE:
            self._maybe_spawn_error(strain, npc_count, dt)

        # Spawn frame drops
        self._maybe_spawn_frame_drop(strain, dt)

        # Remove expired errors
        self._cleanup_expired_errors()
        self._cleanup_expired_frame_drops()

        # Return rendering data
        return self._get_rendering_data(npc_count)

    def _calculate_strain(self, npc_count: int, current_heat: float,
                         toddler_strain: float) -> float:
        """Calculate overall renderer strain (0.0 to 1.0+)"""

        # Base strain from NPC count
        # Wolf3D was designed for ~20 sprites
        npc_strain = max(0.0, (npc_count - 20) / 30.0)  # Strain starts at 20 NPCs

        # Heat contributes to strain
        heat_strain = current_heat / 5.0

        # Toddler dramatically amplifies strain
        toddler_multiplier = 1.0 + (toddler_strain * 2.0)

        # Combined strain
        total_strain = (npc_strain * 0.4 + heat_strain * 0.6) * toddler_multiplier

        return min(2.0, total_strain)  # Can exceed 1.0 for critical situations

    def _get_strain_level(self, strain: float) -> StrainLevel:
        """Get strain level category from strain value"""
        if strain < 0.2:
            return StrainLevel.STABLE
        elif strain < 0.5:
            return StrainLevel.MINOR
        elif strain < 0.8:
            return StrainLevel.MODERATE
        elif strain < 1.2:
            return StrainLevel.HEAVY
        else:
            return StrainLevel.CRITICAL

    def _update_fake_fps(self, strain: float, dt: float):
        """Update fake FPS counter to show degradation"""

        if strain < 0.2:
            # Stable - perfect 60 FPS
            self.target_fps = 60.0
        elif strain < 0.5:
            # Minor - occasional dips
            self.target_fps = random.uniform(55, 60)
        elif strain < 0.8:
            # Moderate - frequent dips
            self.target_fps = random.uniform(45, 58)
        elif strain < 1.2:
            # Heavy - significant drops
            self.target_fps = random.uniform(30, 50)
        else:
            # Critical - severe drops
            self.target_fps = random.uniform(15, 35)

        # Smoothly interpolate displayed FPS toward target
        self.displayed_fps += (self.target_fps - self.displayed_fps) * dt * 2.0

    def _maybe_spawn_error(self, strain: float, npc_count: int, dt: float):
        """Spawn error messages based on strain"""

        # Error spawn chance based on strain
        if strain < 0.2:
            spawn_chance = 0.0
        elif strain < 0.5:
            spawn_chance = 0.01  # Rare warnings
        elif strain < 0.8:
            spawn_chance = 0.03  # Occasional warnings
        elif strain < 1.2:
            spawn_chance = 0.08  # Frequent warnings + some errors
        else:
            spawn_chance = 0.15  # Constant errors

        if random.random() < spawn_chance:
            error = self._generate_error(strain, npc_count)
            if error:
                self.active_errors.append(error)

    def _generate_error(self, strain: float, npc_count: int) -> Optional[PerformanceError]:
        """Generate an appropriate error for current strain"""

        if strain < 0.5:
            # Minor warnings only
            message = random.choice(self.warning_messages)
            error_type = "WARNING"
            duration = 3.0

        elif strain < 0.8:
            # Mix of warnings and errors
            if random.random() < 0.7:
                message = random.choice(self.warning_messages)
                error_type = "WARNING"
            else:
                message = random.choice(self.error_messages)
                error_type = "ERROR"
            duration = 4.0

        elif strain < 1.2:
            # Mostly errors
            if random.random() < 0.3:
                message = random.choice(self.warning_messages)
                error_type = "WARNING"
            else:
                message = random.choice(self.error_messages)
                error_type = "ERROR"
            duration = 5.0

        else:
            # Critical errors, some persistent
            message = random.choice(self.critical_messages)
            error_type = "CRITICAL"
            duration = 8.0
            persistent = random.random() < 0.3

        # Format message with context
        message = message.format(
            npc_count=npc_count,
            agent_id=f"AI_{random.randint(100, 999)}",
            overdraw=random.randint(8, 45),
            drop_count=random.randint(3, 15),
            fps=int(self.displayed_fps)
        )

        return PerformanceError(
            message=message,
            error_type=error_type,
            timestamp=time.time(),
            duration=duration,
            persistent=persistent if error_type == "CRITICAL" else False
        )

    def _maybe_spawn_frame_drop(self, strain: float, dt: float):
        """Spawn fake frame drops (visual stutters)"""

        # Frame drop frequency based on strain
        if strain < 0.5:
            cooldown = 999.0  # Never
        elif strain < 0.8:
            cooldown = 10.0  # Rare stutters
        elif strain < 1.2:
            cooldown = 3.0  # Frequent stutters
        else:
            cooldown = 1.0  # Constant stuttering

        if self.time_since_last_frame_drop >= cooldown:
            if random.random() < 0.3:  # 30% chance when cooldown expires
                # Create frame drop event
                duration = random.uniform(0.05, 0.2) if strain < 1.0 else random.uniform(0.1, 0.5)
                intensity = min(1.0, strain)

                frame_drop = FrameDropEvent(
                    timestamp=time.time(),
                    duration=duration,
                    intensity=intensity
                )
                self.frame_drop_events.append(frame_drop)
                self.time_since_last_frame_drop = 0.0

    def _cleanup_expired_errors(self):
        """Remove expired error messages"""
        current_time = time.time()
        self.active_errors = [
            e for e in self.active_errors
            if e.persistent or (current_time - e.timestamp) < e.duration
        ]

    def _cleanup_expired_frame_drops(self):
        """Remove expired frame drops"""
        current_time = time.time()
        self.frame_drop_events = [
            fd for fd in self.frame_drop_events
            if (current_time - fd.timestamp) < fd.duration
        ]

    def _check_warmup_trigger(self, strain: float, heat: float, npc_count: int,
                              toddler_strain: float, dt: float):
        """
        Check if renderer should enter SHADER WARMUP PHASE

        Trigger conditions (from the internal document):
        - Heat >= 4.8
        - Toddler interacting with system (high strain)
        - FPS EXACTLY 23 (the cursed number)
        - More than 12 NPCs thinking at once
        - Renderer existential crisis (strain > 1.5)
        """
        if self.warmup_phase != WarmupPhase.INACTIVE:
            return  # Already in warmup

        if self.warmup_triggered_this_session:
            return  # Only trigger once per session

        trigger = False

        # Heat >= 4.8
        if heat >= 4.8:
            trigger = True

        # Toddler causing reality strain
        if toddler_strain > 0.8:
            trigger = True

        # FPS EXACTLY 23 (the cursed framerate)
        if 22.5 <= self.displayed_fps <= 23.5:
            trigger = True

        # Too many NPCs thinking
        if npc_count > 12 and strain > 0.7:
            trigger = True

        # Existential crisis (strain way over limit)
        if strain > 1.5:
            trigger = True

        if trigger:
            self._start_warmup_ritual()

    def _start_warmup_ritual(self):
        """
        Initialize the SHADER WARMUP PHASE
        The renderer's psychological coping mechanism
        """
        self.warmup_phase = WarmupPhase.INIT_SHADERS
        self.warmup_timer = 0.0
        self.warmup_triggered_this_session = True

        # Clear existing errors - the renderer is now FOCUSED on the ritual
        self.active_errors.clear()

        # Add initial warmup message
        self.active_errors.append(PerformanceError(
            message="[INFO] Entering Shader Warmup Phase...",
            error_type="INFO",
            timestamp=time.time(),
            duration=2.0
        ))

        print("[RENDERER] ⚠️  SHADER WARMUP PHASE INITIATED")
        print("[RENDERER] The renderer is psychologically preparing itself...")

    def _update_warmup_ritual(self, dt: float):
        """
        Progress through the warmup ritual steps

        Ritual sequence:
        1. INIT_SHADERS (1.0s) - "Compiling shaders that do not exist..."
        2. PRIME_HARDWARE (0.8s) - "Priming hardware..."
        3. BLESS_PIPELINE (0.5s) - "Blessing pipeline..."
        4. RUN_DOOM (0.1s, ~6 frames at 60fps) - THE SACRED RITE
        5. PRETEND_SUCCESS (0.5s) - "Warmup complete!"
        6. RESUME - Back to normal
        """
        self.warmup_timer += dt

        if self.warmup_phase == WarmupPhase.INIT_SHADERS:
            if self.warmup_timer < 1.0:
                # Show shader compilation messages
                if int(self.warmup_timer * 10) % 3 == 0:
                    msg = random.choice(self.warmup_messages[:4])
                    self.active_errors.append(PerformanceError(
                        message=msg,
                        error_type="INFO",
                        timestamp=time.time(),
                        duration=0.5
                    ))
            else:
                self.warmup_phase = WarmupPhase.PRIME_HARDWARE
                self.warmup_timer = 0.0

        elif self.warmup_phase == WarmupPhase.PRIME_HARDWARE:
            if self.warmup_timer < 0.8:
                # Show hardware priming messages
                if int(self.warmup_timer * 10) % 2 == 0:
                    msg = random.choice(self.warmup_messages[4:8])
                    self.active_errors.append(PerformanceError(
                        message=msg,
                        error_type="INFO",
                        timestamp=time.time(),
                        duration=0.5
                    ))
            else:
                self.warmup_phase = WarmupPhase.BLESS_PIPELINE
                self.warmup_timer = 0.0

        elif self.warmup_phase == WarmupPhase.BLESS_PIPELINE:
            if self.warmup_timer < 0.5:
                # "Blessing the pipeline..."
                self.active_errors.append(PerformanceError(
                    message="[RITUAL] Blessing the frame buffer...",
                    error_type="RITUAL",
                    timestamp=time.time(),
                    duration=0.5
                ))
            else:
                # Begin THE SACRED RITE
                self.warmup_phase = WarmupPhase.RUN_DOOM
                self.warmup_timer = 0.0
                self.doom_frames_remaining = random.randint(2, 4)  # 2-4 frames of DOOM

                self.active_errors.clear()
                self.active_errors.append(PerformanceError(
                    message="[RITUAL] Running DOOM for psychological stability...",
                    error_type="RITUAL",
                    timestamp=time.time(),
                    duration=0.5,
                    persistent=False
                ))

                print("[RENDERER] 🔥 RUNNING DOOM RITUAL...")

        elif self.warmup_phase == WarmupPhase.RUN_DOOM:
            # THE SACRED RITE: Run DOOM for a few frames
            self.doom_frames_remaining -= 1

            if self.doom_frames_remaining <= 0:
                # DOOM ritual complete
                self.warmup_phase = WarmupPhase.PRETEND_SUCCESS
                self.warmup_timer = 0.0

                self.active_errors.clear()
                self.active_errors.append(PerformanceError(
                    message="[INFO] Shader warmup complete!",
                    error_type="INFO",
                    timestamp=time.time(),
                    duration=1.0
                ))
                self.active_errors.append(PerformanceError(
                    message="[INFO] Renderer stabilized (probably)",
                    error_type="INFO",
                    timestamp=time.time(),
                    duration=1.0
                ))

                print("[RENDERER] ✓ WARMUP RITUAL COMPLETE")

        elif self.warmup_phase == WarmupPhase.PRETEND_SUCCESS:
            if self.warmup_timer > 0.5:
                # Ritual complete, resume normal operation
                self.warmup_phase = WarmupPhase.INACTIVE
                self.warmup_timer = 0.0

                # The renderer FEELS better now (even though nothing changed)
                # Briefly improve displayed FPS to simulate "success"
                self.displayed_fps = min(60.0, self.displayed_fps + 10.0)

    def _get_rendering_data(self, npc_count: int) -> Dict[str, Any]:
        """Get rendering data for display"""
        return {
            "strain_level": self.strain_level.value,
            "cumulative_strain": self.cumulative_strain,
            "fake_fps": int(self.displayed_fps),
            "target_fps": 60,

            # Active errors
            "active_errors": [
                {
                    "message": e.message,
                    "type": e.error_type,
                    "age": time.time() - e.timestamp,
                    "persistent": e.persistent
                }
                for e in self.active_errors
            ],

            # Frame drops
            "frame_drops_active": len(self.frame_drop_events) > 0,
            "frame_drop_intensity": max([fd.intensity for fd in self.frame_drop_events], default=0.0),

            # Stats for display
            "npc_count": npc_count,
            "npc_limit_classic": 20,  # Wolf3D limit
            "npc_over_limit": max(0, npc_count - 20),

            # SHADER WARMUP PHASE data
            "warmup_active": self.warmup_phase != WarmupPhase.INACTIVE,
            "warmup_phase": self.warmup_phase.value,
            "doom_ritual_active": self.warmup_phase == WarmupPhase.RUN_DOOM,
            "doom_frames_remaining": self.doom_frames_remaining
        }

    def force_error(self, message: str, error_type: str = "ERROR", duration: float = 5.0):
        """Force a specific error to appear (for testing/scripting)"""
        error = PerformanceError(
            message=message,
            error_type=error_type,
            timestamp=time.time(),
            duration=duration
        )
        self.active_errors.append(error)

    def get_strain_description(self) -> str:
        """Get text description of current strain"""
        descriptions = {
            StrainLevel.STABLE: "Renderer stable. Wolf3D mask holding.",
            StrainLevel.MINOR: "Minor strain detected. Occasional warnings.",
            StrainLevel.MODERATE: "Renderer struggling. Frequent warnings.",
            StrainLevel.HEAVY: "Heavy strain. Performance degradation visible.",
            StrainLevel.CRITICAL: "CRITICAL: Renderer failing. Mask shattered."
        }
        return descriptions.get(self.strain_level, "Unknown")

    def clear_all_errors(self):
        """Clear all errors (for testing/reset)"""
        self.active_errors.clear()
        self.frame_drop_events.clear()
        self.displayed_fps = 60.0
        self.cumulative_strain = 0.0
        self.strain_level = StrainLevel.STABLE
