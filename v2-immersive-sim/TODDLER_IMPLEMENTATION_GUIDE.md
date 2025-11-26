# 🧸 TODDLER SYSTEM - EXHAUSTIVE IMPLEMENTATION GUIDE

**A Level-2 Deep Dive Into Making The Invisible Entity Work**

This document covers EVERYTHING you need to know to integrate the toddler system into your actual game renderer, game loop, and player experience.

---

## 📋 TABLE OF CONTENTS

1. [System Architecture](#system-architecture)
2. [Rendering Integration](#rendering-integration)
3. [Game Loop Integration](#game-loop-integration)
4. [Visual Effects](#visual-effects)
5. [Audio Integration](#audio-integration)
6. [Balancing & Tuning](#balancing--tuning)
7. [Debugging Tools](#debugging-tools)
8. [Edge Cases & Gotchas](#edge-cases--gotchas)
9. [Performance Optimization](#performance-optimization)
10. [Narrative Integration](#narrative-integration)
11. [Testing Checklist](#testing-checklist)

---

## 1. SYSTEM ARCHITECTURE

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     GAME LOOP (60 FPS)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              toddler_system.update(dt, ...)                 │
│  - Updates position                                         │
│  - Changes behavior                                         │
│  - Calculates visibility                                    │
│  - Returns effects dict                                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
        ┌──────────────────┐  ┌──────────────────┐
        │  Glitch System   │  │  Renderer Strain │
        │  (3x multiplier) │  │  (strain calc)   │
        └──────────────────┘  └──────────────────┘
                    │                   │
                    └─────────┬─────────┘
                              ▼
                    ┌──────────────────┐
                    │  Render Pipeline │
                    │  - Draw toddler? │
                    │  - Show effects  │
                    └──────────────────┘
```

### Key Data Structures

**ToddlerState** (from `toddler_system.py`):
```python
@dataclass
class ToddlerState:
    position: Tuple[float, float, float]  # World coordinates
    behavior: ToddlerBehavior              # Current behavior enum
    visibility: float                      # 0.0-1.0
    reality_strain: float                  # 0.0-1.0
    velocity: Tuple[float, float]          # Movement vector
    target_position: Optional[Tuple]       # Navigation target
    behavior_timer: float                  # Time until behavior change
    flicker_timer: float                   # Animation timer
```

**Effects Dictionary** (returned by `update()`):
```python
{
    "toddler_position": (x, y, z),
    "toddler_visible": bool,
    "visibility": float,
    "behavior": str,
    "reality_strain": float,
    "in_distortion_field": bool,
    "distortion_intensity": float,      # 0.0-1.0 based on distance
    "heat_multiplier": float,           # 1.0-3.0
    "glitch_multiplier": float,         # 1.0-4.0
    "distance_to_player": float,
    "distortion_radius": float
}
```

---

## 2. RENDERING INTEGRATION

### Wolf3D Raycaster Integration

**Challenge**: How do you render an entity that exists "outside" the simulation in a raycaster?

**Solution**: Sprite billboarding with special shader/color effects

#### Step 1: Sprite Rendering

```python
def render_toddler_sprite(renderer, toddler_data, camera_pos, camera_facing):
    """
    Render toddler as a billboard sprite in Wolf3D raycaster
    """
    if not toddler_data.get('visible'):
        return  # Don't render if invisible

    toddler_pos = toddler_data['toddler_position']
    visibility = toddler_data['visibility']

    # Calculate sprite position relative to camera
    dx = toddler_pos[0] - camera_pos[0]
    dy = toddler_pos[1] - camera_pos[1]

    # Calculate angle to toddler
    angle_to_toddler = math.atan2(dy, dx)
    relative_angle = angle_to_toddler - camera_facing

    # Check if toddler is in camera FOV (90 degrees typically)
    if abs(relative_angle) > math.radians(45):
        return  # Not in view

    # Calculate distance for depth/scale
    distance = math.sqrt(dx*dx + dy*dy)
    if distance > 30:  # Max render distance
        return

    # Calculate screen position
    screen_x = int(SCREEN_WIDTH / 2 + math.tan(relative_angle) * SCREEN_WIDTH)

    # Calculate sprite scale based on distance
    sprite_scale = 32 / max(distance, 1.0)  # Smaller when far
    sprite_height = int(sprite_scale * 64)
    sprite_width = int(sprite_scale * 64)

    # Get sprite based on visibility
    sprite = get_toddler_sprite(visibility, toddler_data)

    # Render with alpha based on visibility
    alpha = int(visibility * 255)

    renderer.draw_sprite(
        sprite=sprite,
        x=screen_x,
        y=SCREEN_HEIGHT // 2,  # Center vertically
        width=sprite_width,
        height=sprite_height,
        alpha=alpha,
        depth=distance  # For Z-sorting with other sprites
    )
```

#### Step 2: Sprite Selection

```python
def get_toddler_sprite(visibility, toddler_data):
    """
    Select appropriate sprite based on visibility level
    """
    if visibility < 0.1:
        # Completely invisible - return None or empty
        return None

    elif visibility < 0.2:
        # Barely visible - single pixel flicker
        return SPRITE_TODDLER_DOT  # Just a · character or 1px sprite

    elif visibility < 0.4:
        # Faint outline
        return SPRITE_TODDLER_FAINT  # Low-opacity silhouette

    else:
        # Fully visible - show actual toddler sprite
        behavior = toddler_data.get('behavior', 'wandering')

        if toddler_data.get('flicker', False):
            # Flickering between visible and glitch
            return random.choice([
                SPRITE_TODDLER_NORMAL,
                SPRITE_TODDLER_GLITCH
            ])
        else:
            return SPRITE_TODDLER_NORMAL
```

#### Step 3: ASCII Terminal Rendering

For pure ASCII/ANSI terminal rendering:

```python
def render_toddler_ascii(toddler_data, player_pos, terminal):
    """
    Render toddler in ASCII terminal view
    """
    if not toddler_data.get('visible'):
        return

    toddler_pos = toddler_data['toddler_position']
    visibility = toddler_data['visibility']

    # Convert world coords to screen coords
    screen_x = int(toddler_pos[0] - player_pos[0] + TERMINAL_WIDTH // 2)
    screen_y = int(toddler_pos[1] - player_pos[1] + TERMINAL_HEIGHT // 2)

    # Check if on screen
    if not (0 <= screen_x < TERMINAL_WIDTH and 0 <= screen_y < TERMINAL_HEIGHT):
        return

    # Choose symbol based on visibility
    if visibility < 0.1:
        symbol = ' '  # Invisible
        color = 0
    elif visibility < 0.2:
        symbol = '·'  # Faint dot
        color = 8  # Dark gray
    elif visibility < 0.4:
        symbol = '○'  # Circle outline
        color = 7   # Light gray
    else:
        symbol = '☺'  # Full toddler
        color = 15  # White

    # Apply flicker
    if toddler_data.get('flicker', False):
        color = random.choice([color, 1, 9])  # Flicker red/bright red

    # Apply reality strain visual effect
    reality_strain = toddler_data.get('reality_strain', 0.0)
    if reality_strain > 0.5:
        # Add distortion around toddler
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                distort_x = screen_x + dx
                distort_y = screen_y + dy
                if 0 <= distort_x < TERMINAL_WIDTH and 0 <= distort_y < TERMINAL_HEIGHT:
                    if random.random() < reality_strain:
                        terminal.put_char(distort_x, distort_y, '~', color=8)

    # Draw toddler
    terminal.put_char(screen_x, screen_y, symbol, color=color, bgcolor=0)
```

### Visual Effect Layers

**Layer 1: Distortion Field** (always active when toddler is near)
```python
def render_distortion_field(toddler_data, player_pos, renderer):
    """
    Render visual distortion around toddler
    """
    if not toddler_data.get('in_distortion_field'):
        return

    intensity = toddler_data.get('distortion_intensity', 0.0)

    # Screen-space distortion shader
    renderer.apply_shader(
        shader_type="distortion",
        intensity=intensity * 0.3,  # Subtle
        center=toddler_data['toddler_position'],
        radius=toddler_data['distortion_radius']
    )
```

**Layer 2: Reality Tear Effect** (at high strain)
```python
def render_reality_tear(toddler_data, renderer):
    """
    Visual 'tear' in reality around toddler at high strain
    """
    reality_strain = toddler_data.get('reality_strain', 0.0)

    if reality_strain < 0.7:
        return  # Only show at high strain

    toddler_pos = toddler_data['toddler_position']

    # Draw jagged lines emanating from toddler
    num_tears = int(reality_strain * 8)  # 0-8 tear lines

    for i in range(num_tears):
        angle = (i / num_tears) * math.pi * 2
        length = random.uniform(3, 8)

        end_x = toddler_pos[0] + math.cos(angle) * length
        end_y = toddler_pos[1] + math.sin(angle) * length

        renderer.draw_line(
            start=(toddler_pos[0], toddler_pos[1]),
            end=(end_x, end_y),
            color=(255, 0, 255),  # Magenta 'error' color
            thickness=1,
            style="jagged"  # Not smooth
        )
```

---

## 3. GAME LOOP INTEGRATION

### Complete Integration Example

```python
class GameLoop:
    def __init__(self):
        self.simulation = MallSimulation(world_tiles)
        # ... other systems

    def update(self, dt):
        """
        Main game loop update
        """
        # 1. Get player input
        player_action = self.input_handler.get_action()

        # 2. Update simulation (includes toddler)
        sim_data = self.simulation.update(dt, player_action)

        # 3. Extract toddler data
        toddler_data = sim_data.get('toddler', {})
        toddler_effects = sim_data.get('toddler_effects', {})

        # 4. Apply toddler effects to other systems
        self._apply_toddler_effects(toddler_effects)

        # 5. Update audio based on toddler proximity
        self._update_toddler_audio(toddler_effects)

        # 6. Render everything
        self.renderer.render(sim_data)

    def _apply_toddler_effects(self, toddler_effects):
        """
        Apply toddler effects to game systems
        """
        # Camera shake when near toddler
        if toddler_effects.get('in_distortion_field'):
            intensity = toddler_effects.get('distortion_intensity', 0.0)
            self.camera.add_shake(intensity * 0.5)

        # Increase glitch post-processing
        glitch_mult = toddler_effects.get('glitch_multiplier', 1.0)
        self.post_processor.set_glitch_intensity((glitch_mult - 1.0) / 3.0)

        # Color grading shift near toddler
        reality_strain = toddler_effects.get('reality_strain', 0.0)
        if reality_strain > 0.5:
            self.renderer.set_color_grading(
                saturation=1.0 - (reality_strain * 0.3),
                contrast=1.0 + (reality_strain * 0.2)
            )
```

### Render Order

**Critical**: Render toddler at the correct depth layer!

```python
def render_frame(sim_data):
    """
    Proper render order for all entities
    """
    # 1. World geometry (walls, floor, ceiling)
    render_world(sim_data['world'])

    # 2. Props (sorted by distance)
    render_props(sim_data['props'])

    # 3. NPCs (sorted by distance)
    render_npcs(sim_data['npcs'])

    # 4. Toddler (special depth handling)
    toddler_data = sim_data.get('toddler', {})
    if toddler_data.get('visible'):
        render_toddler_sprite(toddler_data)  # Z-sorted with NPCs

    # 5. Particle effects (glitches, reality tears)
    render_glitch_effects(sim_data['micro_glitches'])
    render_toddler_distortion(sim_data['toddler_effects'])

    # 6. UI overlays
    render_ui(sim_data)

    # 7. Renderer strain errors (on top of everything)
    render_error_messages(sim_data['renderer_strain'])
```

---

## 4. VISUAL EFFECTS

### Proximity Visual Cues

```python
class ToddlerProximityFX:
    """
    Visual effects that hint at toddler presence before visible
    """

    def update(self, toddler_effects, heat_level):
        self.effects = []

        distance = toddler_effects.get('distance_to_player', 999)

        # Very close (< 5 tiles) - strong cues
        if distance < 5:
            self.effects.append({
                'type': 'vignette',
                'intensity': 0.3,
                'color': (150, 0, 150)  # Purple
            })
            self.effects.append({
                'type': 'chromatic_aberration',
                'intensity': 0.2
            })

        # Close (5-10 tiles) - medium cues
        elif distance < 10:
            self.effects.append({
                'type': 'color_shift',
                'hue_shift': 0.1
            })

        # Near distortion field (10-15 tiles) - subtle cues
        elif distance < 15:
            if random.random() < 0.05:  # 5% chance per frame
                self.effects.append({
                    'type': 'screen_flicker',
                    'duration': 0.05  # 50ms flicker
                })

        return self.effects
```

### Visibility Transition Effects

```python
def render_toddler_visibility_transition(toddler_data, renderer):
    """
    Special effects when toddler becomes visible/invisible
    """
    visibility = toddler_data.get('visibility', 0.0)

    # Track previous visibility
    if not hasattr(render_toddler_visibility_transition, 'prev_vis'):
        render_toddler_visibility_transition.prev_vis = 0.0

    prev_vis = render_toddler_visibility_transition.prev_vis

    # Threshold crossing: invisible -> visible
    if prev_vis < 0.1 and visibility >= 0.1:
        # Flash effect
        renderer.add_screen_flash(
            color=(255, 255, 255),
            intensity=0.5,
            duration=0.1
        )
        # Sound cue
        audio.play_sound("reality_tear", volume=0.7)

    # Threshold crossing: visible -> invisible
    elif prev_vis >= 0.1 and visibility < 0.1:
        # Fade to static briefly
        renderer.add_static_effect(
            intensity=0.8,
            duration=0.2
        )

    # Update tracker
    render_toddler_visibility_transition.prev_vis = visibility
```

---

## 5. AUDIO INTEGRATION

### Proximity Audio System

```python
class ToddlerAudioManager:
    """
    Manages all toddler-related audio
    """

    def __init__(self):
        self.ambient_loop = None
        self.heartbeat_intensity = 0.0

    def update(self, dt, toddler_effects, heat_level):
        distance = toddler_effects.get('distance_to_player', 999)
        reality_strain = toddler_effects.get('reality_strain', 0.0)

        # 1. AMBIENT DRONE (proximity-based)
        if distance < 15:
            # Play low-frequency drone that gets louder/more distorted
            drone_volume = 1.0 - (distance / 15.0)  # 0.0-1.0
            drone_pitch = 1.0 - (reality_strain * 0.3)  # Lower pitch = more strain

            if not self.ambient_loop or not self.ambient_loop.is_playing():
                self.ambient_loop = audio.play_loop(
                    "toddler_ambient_drone",
                    volume=drone_volume * 0.3,
                    pitch=drone_pitch
                )
            else:
                self.ambient_loop.set_volume(drone_volume * 0.3)
                self.ambient_loop.set_pitch(drone_pitch)
        else:
            # Stop drone when far
            if self.ambient_loop:
                self.ambient_loop.fade_out(1.0)
                self.ambient_loop = None

        # 2. HEARTBEAT (very close)
        if distance < 5:
            self.heartbeat_intensity += dt * 2.0
            self.heartbeat_intensity = min(1.0, self.heartbeat_intensity)

            # Trigger heartbeat sound
            if int(self.heartbeat_intensity * 10) % 2 == 0:  # Every ~0.5s
                audio.play_sound(
                    "heartbeat",
                    volume=self.heartbeat_intensity * 0.5
                )
        else:
            self.heartbeat_intensity = max(0.0, self.heartbeat_intensity - dt)

        # 3. WHISPERS (heat 3+, near toddler)
        if heat_level >= 3.0 and distance < 10:
            if random.random() < 0.01:  # 1% chance per frame
                audio.play_sound(
                    random.choice([
                        "whisper_1",
                        "whisper_2",
                        "whisper_3",
                        "child_laugh_distant"
                    ]),
                    volume=0.3,
                    pan=self._calculate_audio_pan(toddler_effects)
                )

        # 4. STATIC/INTERFERENCE (high reality strain)
        if reality_strain > 0.7:
            # Radio static on top of everything
            if not hasattr(self, 'static_loop') or not self.static_loop.is_playing():
                self.static_loop = audio.play_loop(
                    "radio_static",
                    volume=(reality_strain - 0.7) * 0.3
                )

    def _calculate_audio_pan(self, toddler_effects):
        """
        Calculate stereo pan based on toddler position
        """
        # Get angle to toddler relative to player facing
        # Return -1.0 (left) to 1.0 (right)
        # Implementation depends on your audio system
        return 0.0  # Centered for now
```

### Audio Cues for Visibility

```python
def play_toddler_visibility_audio(visibility, previous_visibility):
    """
    Audio feedback for visibility changes
    """
    # Crossing into visibility
    if previous_visibility < 0.1 and visibility >= 0.1:
        audio.play_sound("reality_tear", volume=0.8)

    # Becoming more visible
    elif visibility > previous_visibility + 0.2:
        audio.play_sound("glitch_escalate", volume=0.5)

    # Full visibility (toddler revealed)
    if visibility >= 0.5 and previous_visibility < 0.5:
        audio.play_sound("toddler_reveal", volume=1.0)
        audio.play_sound("stinger_horror", volume=0.7)
```

---

## 6. BALANCING & TUNING

### Tunable Parameters

All key parameters with recommended ranges:

```python
class ToddlerBalancingConfig:
    """
    Centralized balancing parameters
    """

    # MOVEMENT
    movement_speed: float = 1.5          # Range: 1.0-3.0 tiles/sec
    distortion_radius: float = 15.0      # Range: 10.0-20.0 tiles

    # AMPLIFICATION
    heat_amplification: float = 2.0      # Range: 1.5-3.0 multiplier
    glitch_multiplier: float = 3.0       # Range: 2.0-5.0 multiplier

    # VISIBILITY
    visibility_heat_threshold: float = 3.0   # Heat level for first flickers
    max_visibility_heat: float = 4.5         # Heat for full visibility
    proximity_visibility_bonus: float = 0.3  # Extra visibility when close

    # BEHAVIOR
    behavior_change_interval: float = 10.0   # Range: 5.0-15.0 seconds

    # AUDIO
    audio_radius: float = 15.0           # Range: 10.0-25.0 tiles
    audio_max_volume: float = 0.5        # Range: 0.3-0.8
```

### Difficulty Scaling

```python
def apply_difficulty_scaling(toddler_system, difficulty):
    """
    Adjust toddler behavior based on difficulty
    """
    if difficulty == "EASY":
        # Less aggressive
        toddler_system.distortion_radius = 10.0  # Smaller field
        toddler_system.heat_amplification = 1.5  # Less heat buildup
        toddler_system.glitch_multiplier = 2.0   # Fewer glitches

    elif difficulty == "NORMAL":
        # Default values
        pass

    elif difficulty == "HARD":
        # More aggressive
        toddler_system.distortion_radius = 20.0  # Larger field
        toddler_system.heat_amplification = 2.5  # Faster heat
        toddler_system.glitch_multiplier = 4.0   # More glitches
        toddler_system.movement_speed = 2.0      # Faster movement

    elif difficulty == "NIGHTMARE":
        # Extremely aggressive
        toddler_system.distortion_radius = 25.0
        toddler_system.heat_amplification = 3.0
        toddler_system.glitch_multiplier = 5.0
        toddler_system.movement_speed = 2.5
        # Toddler visible at Heat 2+
        toddler_system.visibility_heat_threshold = 2.0
```

### Player Feedback Curve

**Goal**: Player should feel progression from "uneasy" to "terrified"

```python
def get_player_tension_level(toddler_effects, heat_level):
    """
    Calculate player tension for balancing
    Returns 0.0 (calm) to 1.0 (terror)
    """
    distance = toddler_effects.get('distance_to_player', 999)
    visibility = toddler_effects.get('visibility', 0.0)
    reality_strain = toddler_effects.get('reality_strain', 0.0)

    # Distance tension (closer = higher)
    distance_tension = max(0.0, 1.0 - (distance / 20.0))

    # Visibility tension (seeing it = much higher)
    visibility_tension = visibility * 2.0  # Amplified

    # Heat tension
    heat_tension = heat_level / 5.0

    # Reality strain tension
    strain_tension = reality_strain

    # Weighted average
    tension = (
        distance_tension * 0.2 +
        visibility_tension * 0.4 +  # Seeing it is VERY tense
        heat_tension * 0.2 +
        strain_tension * 0.2
    )

    return min(1.0, tension)


# Use this to balance intensity
def apply_tension_based_effects(tension):
    """
    Scale effects based on tension
    """
    # Camera shake
    camera.shake_intensity = tension * 0.5

    # Audio volume
    ambient_volume = tension * 0.3

    # UI distortion
    ui_glitch_chance = tension * 0.1

    # Player movement penalty
    player.movement_speed = 1.0 - (tension * 0.2)  # Max 20% slower
```

---

## 7. DEBUGGING TOOLS

### Debug Overlay

```python
class ToddlerDebugOverlay:
    """
    Visual debug overlay for toddler system
    """

    def render(self, screen, toddler_data, toddler_effects):
        if not DEBUG_MODE:
            return

        y_offset = 10

        # Toddler position
        pos = toddler_effects['toddler_position']
        self._draw_text(screen, f"Toddler Pos: ({pos[0]:.1f}, {pos[1]:.1f})", y_offset)
        y_offset += 20

        # Behavior
        behavior = toddler_effects['behavior']
        self._draw_text(screen, f"Behavior: {behavior}", y_offset)
        y_offset += 20

        # Distance
        distance = toddler_effects['distance_to_player']
        in_field = toddler_effects['in_distortion_field']
        self._draw_text(
            screen,
            f"Distance: {distance:.1f} {'[IN FIELD]' if in_field else ''}",
            y_offset
        )
        y_offset += 20

        # Visibility
        visibility = toddler_data.get('visibility', 0.0)
        visible = toddler_data.get('visible', False)
        self._draw_text(
            screen,
            f"Visibility: {visibility:.2f} {'[VISIBLE]' if visible else '[HIDDEN]'}",
            y_offset
        )
        y_offset += 20

        # Multipliers
        heat_mult = toddler_effects['heat_multiplier']
        glitch_mult = toddler_effects['glitch_multiplier']
        self._draw_text(screen, f"Heat Mult: {heat_mult:.2f}x", y_offset)
        y_offset += 20
        self._draw_text(screen, f"Glitch Mult: {glitch_mult:.2f}x", y_offset)
        y_offset += 20

        # Reality strain
        strain = toddler_effects['reality_strain']
        self._draw_text(screen, f"Reality Strain: {strain:.2f}", y_offset)
        y_offset += 20

        # Draw distortion field radius on minimap
        self._draw_distortion_field_debug(screen, pos, toddler_effects['distortion_radius'])

    def _draw_distortion_field_debug(self, screen, toddler_pos, radius):
        """Draw red circle showing distortion field"""
        # Convert world coords to screen coords
        # Draw circle at toddler_pos with radius
        pass  # Implementation depends on your renderer
```

### Console Commands

```python
class ToddlerDebugCommands:
    """
    Debug console commands for testing
    """

    @console_command
    def toddler_teleport(self, x, y):
        """Teleport toddler to position"""
        self.toddler_system.toddler.position = (float(x), float(y), 0)
        print(f"Toddler teleported to ({x}, {y})")

    @console_command
    def toddler_behavior(self, behavior_name):
        """Force toddler behavior"""
        behavior = ToddlerBehavior[behavior_name.upper()]
        self.toddler_system.toddler.behavior = behavior
        print(f"Toddler behavior set to: {behavior_name}")

    @console_command
    def toddler_visibility(self, value):
        """Force toddler visibility (0.0-1.0)"""
        self.toddler_system.toddler.visibility = float(value)
        print(f"Toddler visibility set to: {value}")

    @console_command
    def toddler_toggle(self):
        """Toggle toddler system on/off"""
        self.toddler_enabled = not self.toddler_enabled
        print(f"Toddler system: {'ON' if self.toddler_enabled else 'OFF'}")

    @console_command
    def toddler_stats(self):
        """Print detailed toddler stats"""
        state = self.toddler_system.toddler
        print(f"""
        === TODDLER STATS ===
        Position: {state.position}
        Behavior: {state.behavior.value}
        Visibility: {state.visibility:.2f}
        Reality Strain: {state.reality_strain:.2f}
        Target: {state.target_position}
        Behavior Timer: {state.behavior_timer:.1f}s
        """)
```

### Telemetry Logging

```python
class ToddlerTelemetry:
    """
    Log toddler events for balancing analysis
    """

    def __init__(self):
        self.events = []

    def log_visibility_change(self, old_vis, new_vis, heat, distance):
        """Log when toddler becomes visible/invisible"""
        self.events.append({
            'type': 'visibility_change',
            'timestamp': time.time(),
            'old_visibility': old_vis,
            'new_visibility': new_vis,
            'heat_level': heat,
            'distance_to_player': distance
        })

    def log_behavior_change(self, old_behavior, new_behavior, heat):
        """Log behavior state changes"""
        self.events.append({
            'type': 'behavior_change',
            'timestamp': time.time(),
            'old_behavior': old_behavior.value,
            'new_behavior': new_behavior.value,
            'heat_level': heat
        })

    def log_player_in_field(self, duration, average_intensity):
        """Log time spent in distortion field"""
        self.events.append({
            'type': 'distortion_field',
            'timestamp': time.time(),
            'duration': duration,
            'average_intensity': average_intensity
        })

    def export_to_csv(self, filename):
        """Export telemetry for analysis"""
        import csv
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.events[0].keys())
            writer.writeheader()
            writer.writerows(self.events)
```

---

## 8. EDGE CASES & GOTCHAS

### Edge Case 1: Toddler Spawning Inside Walls

**Problem**: Random spawn might place toddler inside geometry

```python
def spawn_toddler_safe(world_tiles, world_bounds):
    """
    Spawn toddler in valid walkable space
    """
    max_attempts = 100
    for _ in range(max_attempts):
        x = random.uniform(10, world_bounds[0] - 10)
        y = random.uniform(10, world_bounds[1] - 10)

        # Check if walkable
        tile = world_tiles.get((int(x), int(y), 0))
        if tile and tile.walkable:
            return (x, y, 0)

    # Fallback: spawn at world center
    return (world_bounds[0] // 2, world_bounds[1] // 2, 0)
```

### Edge Case 2: Toddler Stuck in Corner

**Problem**: Pathfinding might get toddler stuck

```python
def check_toddler_stuck(toddler_system, dt_accumulator):
    """
    Detect if toddler hasn't moved in a while
    """
    if not hasattr(check_toddler_stuck, 'last_pos'):
        check_toddler_stuck.last_pos = toddler_system.toddler.position
        check_toddler_stuck.stuck_time = 0.0

    current_pos = toddler_system.toddler.position
    distance_moved = math.sqrt(
        (current_pos[0] - check_toddler_stuck.last_pos[0])**2 +
        (current_pos[1] - check_toddler_stuck.last_pos[1])**2
    )

    if distance_moved < 0.5:  # Moved less than 0.5 tiles
        check_toddler_stuck.stuck_time += dt_accumulator

        if check_toddler_stuck.stuck_time > 5.0:  # Stuck for 5 seconds
            # Teleport to random location
            new_pos = spawn_toddler_safe(world_tiles, world_bounds)
            toddler_system.toddler.position = new_pos
            check_toddler_stuck.stuck_time = 0.0
            print("[DEBUG] Toddler was stuck, teleported")
    else:
        check_toddler_stuck.stuck_time = 0.0

    check_toddler_stuck.last_pos = current_pos
```

### Edge Case 3: Multiple Heat Sources

**Problem**: What if multiple players or NPCs cause heat simultaneously?

```python
def calculate_toddler_target_with_multiple_heat_sources(heat_sources):
    """
    Toddler attracted to highest heat source
    """
    if not heat_sources:
        return None

    # Find highest heat source
    highest_heat = max(heat_sources, key=lambda s: s['heat_level'])

    # Probabilistic: higher heat = more likely to target
    total_heat = sum(s['heat_level'] for s in heat_sources)

    rand = random.random() * total_heat
    cumulative = 0.0
    for source in heat_sources:
        cumulative += source['heat_level']
        if rand < cumulative:
            return source['position']

    return highest_heat['position']
```

### Edge Case 4: Player Camping in One Spot

**Problem**: Player might stay in one place, causing toddler to just sit there

```python
def encourage_toddler_variety(toddler_system, player_position):
    """
    Force toddler to wander even if player is stationary
    """
    if toddler_system.toddler.behavior == ToddlerBehavior.HIDING:
        return  # Let it hide

    # Check if player has moved recently
    if not hasattr(encourage_toddler_variety, 'player_last_pos'):
        encourage_toddler_variety.player_last_pos = player_position
        encourage_toddler_variety.stationary_time = 0.0

    distance_moved = math.sqrt(
        (player_position[0] - encourage_toddler_variety.player_last_pos[0])**2 +
        (player_position[1] - encourage_toddler_variety.player_last_pos[1])**2
    )

    if distance_moved < 2.0:
        encourage_toddler_variety.stationary_time += dt

        # Player stationary for 20 seconds
        if encourage_toddler_variety.stationary_time > 20.0:
            # Force toddler to wander away
            toddler_system.toddler.behavior = ToddlerBehavior.WANDERING
            toddler_system._set_new_target(player_position)
            encourage_toddler_variety.stationary_time = 0.0
    else:
        encourage_toddler_variety.stationary_time = 0.0

    encourage_toddler_variety.player_last_pos = player_position
```

### Edge Case 5: Very Low/High FPS

**Problem**: Delta time might be extreme, breaking toddler movement

```python
def update_toddler_with_clamped_dt(toddler_system, dt, *args):
    """
    Clamp delta time to prevent physics issues
    """
    # Clamp dt between 1ms and 100ms
    clamped_dt = max(0.001, min(0.1, dt))

    return toddler_system.update(clamped_dt, *args)
```

---

## 9. PERFORMANCE OPTIMIZATION

### Optimization 1: Distance Checks

```python
class OptimizedToddlerSystem(ToddlerSystem):
    """
    Optimized version with spatial partitioning
    """

    def update(self, dt, player_position, current_heat, world_tiles):
        # Quick distance check before full update
        dx = self.toddler.position[0] - player_position[0]
        dy = self.toddler.position[1] - player_position[1]
        distance_sq = dx*dx + dy*dy

        # If very far (>50 tiles), skip expensive updates
        if distance_sq > 2500:  # 50^2
            # Just update position, skip everything else
            self._update_movement_simple(dt)
            return self._get_far_away_effects()

        # Normal update for nearby toddler
        return super().update(dt, player_position, current_heat, world_tiles)

    def _get_far_away_effects(self):
        """Minimal effects when toddler is far"""
        return {
            "toddler_position": self.toddler.position,
            "toddler_visible": False,
            "visibility": 0.0,
            "in_distortion_field": False,
            "heat_multiplier": 1.0,
            "glitch_multiplier": 1.0,
            "distance_to_player": 999.0
        }
```

### Optimization 2: Update Rate Scaling

```python
class AdaptiveToddlerUpdater:
    """
    Updates toddler at different rates based on distance
    """

    def __init__(self, toddler_system):
        self.toddler_system = toddler_system
        self.accumulated_dt = 0.0
        self.last_effects = {}

    def update(self, dt, player_position, current_heat, world_tiles):
        distance = self._quick_distance(player_position)

        # Determine update rate
        if distance < 10:
            update_interval = 0.0  # Every frame (60 FPS)
        elif distance < 20:
            update_interval = 0.05  # 20 FPS
        elif distance < 40:
            update_interval = 0.1   # 10 FPS
        else:
            update_interval = 0.25  # 4 FPS

        self.accumulated_dt += dt

        if self.accumulated_dt >= update_interval:
            self.last_effects = self.toddler_system.update(
                self.accumulated_dt,
                player_position,
                current_heat,
                world_tiles
            )
            self.accumulated_dt = 0.0

        return self.last_effects

    def _quick_distance(self, player_position):
        dx = self.toddler_system.toddler.position[0] - player_position[0]
        dy = self.toddler_system.toddler.position[1] - player_position[1]
        return math.sqrt(dx*dx + dy*dy)
```

### Optimization 3: Visibility Calculation Caching

```python
def update_visibility_cached(self, current_heat, player_position):
    """
    Cache visibility calculations
    """
    # Check if inputs changed significantly
    if not hasattr(self, '_vis_cache'):
        self._vis_cache = {'heat': 0, 'dist': 0, 'result': 0.0}

    cache = self._vis_cache
    distance = self._distance_to_player(player_position)

    # Only recalculate if heat or distance changed significantly
    if abs(current_heat - cache['heat']) < 0.1 and abs(distance - cache['dist']) < 1.0:
        return cache['result']

    # Recalculate
    visibility = self._update_visibility(current_heat, player_position)

    # Update cache
    cache['heat'] = current_heat
    cache['dist'] = distance
    cache['result'] = visibility

    return visibility
```

---

## 10. NARRATIVE INTEGRATION

### Storytelling Through Toddler Behavior

```python
class ToddlerNarrativeManager:
    """
    Manages scripted toddler events for story beats
    """

    def __init__(self, toddler_system):
        self.toddler_system = toddler_system
        self.story_beats = []
        self.active_beat = None

    def register_story_beat(self, trigger_condition, toddler_behavior, duration):
        """
        Register a scripted moment

        Example:
        register_story_beat(
            trigger_condition=lambda: player.location == "food_court",
            toddler_behavior=ToddlerBehavior.FOLLOWING_PLAYER,
            duration=30.0  # 30 seconds
        )
        """
        self.story_beats.append({
            'condition': trigger_condition,
            'behavior': toddler_behavior,
            'duration': duration,
            'triggered': False
        })

    def update(self, dt):
        # Check for story beat triggers
        for beat in self.story_beats:
            if beat['triggered']:
                continue

            if beat['condition']():
                # Trigger story beat
                self.active_beat = beat
                beat['triggered'] = True
                beat['time_remaining'] = beat['duration']

                # Override toddler behavior
                self.toddler_system.toddler.behavior = beat['behavior']

                print(f"[STORY] Triggered toddler story beat: {beat['behavior'].value}")

        # Update active beat
        if self.active_beat:
            self.active_beat['time_remaining'] -= dt

            if self.active_beat['time_remaining'] <= 0:
                # Beat finished, return to normal
                self.active_beat = None
```

### Environmental Storytelling

```python
def add_toddler_environmental_clues(world, toddler_history):
    """
    Leave traces of toddler's path through world
    """
    for historical_pos in toddler_history:
        # Add props/decals where toddler has been

        # 1. Footprints (small, childlike)
        world.add_decal(
            position=historical_pos,
            decal_type="toddler_footprint",
            opacity=0.3,
            lifetime=60.0  # Fade after 60 seconds
        )

        # 2. Reality distortion marks
        if random.random() < 0.1:  # 10% chance
            world.add_prop(
                position=historical_pos,
                prop_type="reality_tear_mark",
                description="A strange shimmer in the air"
            )

        # 3. Broken props near toddler path
        nearby_props = world.get_props_in_radius(historical_pos, 3.0)
        for prop in nearby_props:
            if random.random() < 0.05:  # 5% chance
                prop.set_state("glitched")
```

### NPC Reactions to Toddler

```python
def npc_react_to_toddler(npc, toddler_effects):
    """
    NPCs can 'sense' toddler even when invisible
    """
    distance_to_toddler = calculate_distance(
        npc.position,
        toddler_effects['toddler_position']
    )

    if distance_to_toddler < 5.0:
        # NPC is very close to toddler

        if toddler_effects.get('toddler_visible'):
            # NPC sees toddler
            npc.set_state("terrified")
            npc.say("WHAT IS THAT THING?!")
            npc.flee_from(toddler_effects['toddler_position'])
        else:
            # NPC senses something wrong but can't see it
            npc.set_state("uneasy")
            if random.random() < 0.1:
                npc.say(random.choice([
                    "Something feels... wrong.",
                    "Why is it so cold here?",
                    "Did you hear that?",
                    "I feel like I'm being watched..."
                ]))
```

---

## 11. TESTING CHECKLIST

### Unit Tests

```python
class TestToddlerSystem(unittest.TestCase):
    """
    Unit tests for toddler system
    """

    def setUp(self):
        self.world_tiles = create_test_world()
        self.toddler = ToddlerSystem((50, 50))

    def test_toddler_spawns_in_bounds(self):
        """Toddler should spawn within world bounds"""
        pos = self.toddler.toddler.position
        self.assertGreater(pos[0], 0)
        self.assertLess(pos[0], 50)
        self.assertGreater(pos[1], 0)
        self.assertLess(pos[1], 50)

    def test_distortion_field_activates_near_player(self):
        """Distortion field should activate when player is close"""
        player_pos = self.toddler.toddler.position  # Same position
        effects = self.toddler.update(0.016, player_pos, 3.0, self.world_tiles)

        self.assertTrue(effects['in_distortion_field'])
        self.assertGreater(effects['distortion_intensity'], 0.8)

    def test_heat_multiplier_scales_with_distance(self):
        """Heat multiplier should decrease with distance"""
        toddler_pos = self.toddler.toddler.position

        # Test at different distances
        close_pos = (toddler_pos[0] + 1, toddler_pos[1], 0)
        far_pos = (toddler_pos[0] + 20, toddler_pos[1], 0)

        close_effects = self.toddler.update(0.016, close_pos, 3.0, self.world_tiles)
        far_effects = self.toddler.update(0.016, far_pos, 3.0, self.world_tiles)

        self.assertGreater(
            close_effects['heat_multiplier'],
            far_effects['heat_multiplier']
        )

    def test_visibility_increases_with_heat(self):
        """Visibility should increase as heat increases"""
        player_pos = self.toddler.toddler.position

        low_heat = self.toddler.update(0.016, player_pos, 1.0, self.world_tiles)
        high_heat = self.toddler.update(0.016, player_pos, 5.0, self.world_tiles)

        self.assertGreater(
            high_heat['visibility'],
            low_heat['visibility']
        )
```

### Integration Tests

```python
def test_toddler_full_integration():
    """
    Test toddler integrated with full simulation
    """
    sim = MallSimulation(create_test_world())

    # 1. Verify toddler spawned
    result = sim.update(0.016)
    assert 'toddler' in result
    assert 'toddler_effects' in result

    # 2. Move player near toddler
    toddler_pos = result['toddler_effects']['toddler_position']
    sim.set_player_position((int(toddler_pos[0]), int(toddler_pos[1]), 0))

    # 3. Increase heat
    sim.heat_system.current_heat = 5.0

    # 4. Verify effects
    result = sim.update(0.016)

    assert result['toddler']['visible'] == True
    assert result['toddler_effects']['in_distortion_field'] == True
    assert result['renderer_strain']['cumulative_strain'] > 1.0

    print("✓ Toddler full integration test passed")
```

### Playtest Checklist

**Basic Functionality:**
- [ ] Toddler spawns at game start
- [ ] Toddler moves autonomously
- [ ] Toddler changes behaviors over time
- [ ] Toddler doesn't get stuck in geometry

**Visual Effects:**
- [ ] Toddler is invisible at low heat
- [ ] Toddler becomes visible at Heat 5
- [ ] Visibility transitions smoothly
- [ ] Distortion effects appear near toddler
- [ ] Reality tear effects at high strain

**Audio:**
- [ ] Ambient drone plays when near toddler
- [ ] Audio volume scales with distance
- [ ] Heartbeat sound plays when very close
- [ ] Whispers occasionally play
- [ ] Static sound at high reality strain

**Gameplay Impact:**
- [ ] Heat builds faster near toddler
- [ ] Glitches spawn more frequently near toddler
- [ ] Renderer strain increases with toddler proximity
- [ ] NPCs react to toddler presence
- [ ] Player movement affected in distortion field

**Performance:**
- [ ] No FPS drops from toddler system
- [ ] Update rate scales with distance
- [ ] Memory usage stable over time
- [ ] No memory leaks from audio/effects

**Edge Cases:**
- [ ] Toddler doesn't break on save/load
- [ ] Works with multiple players (if multiplayer)
- [ ] Handles extreme heat levels (>5.0)
- [ ] Handles player death/respawn
- [ ] Works on all difficulty settings

---

## 📊 FINAL IMPLEMENTATION SUMMARY

**Minimum Viable Implementation:**
1. `toddler_system.py` integrated into game loop ✓
2. Basic sprite rendering at correct depth layer ✓
3. Visibility system working (invisible → visible) ✓
4. Amplification effects feeding into other systems ✓
5. Basic audio (ambient drone) ✓

**Recommended Implementation:**
- All of above +
- Visual effects (distortion, reality tears)
- Full audio suite (heartbeat, whispers, static)
- Environmental clues (footprints, marks)
- NPC reactions
- Debug tools

**Deluxe Implementation:**
- All of above +
- Adaptive performance scaling
- Narrative manager for scripted moments
- Full telemetry system
- Difficulty scaling
- Multiple toddlers (advanced)

---

## 🎯 SUCCESS METRICS

**Your toddler implementation is successful if:**

1. **Player Progression**: Player goes from "uneasy" → "confused" → "terrified"
2. **Discovery Moment**: Player has a clear "OH MY GOD" moment when toddler becomes visible
3. **No Breaks**: Toddler never breaks immersion by glitching/stuck/weird behavior
4. **Performance**: No measurable FPS impact
5. **Narrative**: Toddler enhances the "modern engine escaping Wolf3D prison" theme

**The toddler is the SOURCE. Everything breaks because of it. Make sure the player FEELS that.**

---

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  TODDLER IMPLEMENTATION: COMPLETE                           ║
║                                                              ║
║  You now have everything you need to integrate the          ║
║  invisible reality catalyst into your game.                 ║
║                                                              ║
║  The toddler is not a bug. It's the entire point.          ║
║  It's using the AAA engine as a prybar to escape.          ║
║                                                              ║
║  Make them FEEL the dread.                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```
