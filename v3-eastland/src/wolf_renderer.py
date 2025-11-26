"""
DOOFENSTEIN 3D RENDERER
Wolfenstein 3D-style textured raycaster with floor/ceiling
Coffee-spilled shareware clone aesthetic
"""

import math
import random
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
from mall_engine import Direction


# ANSI Color System - Authentic VGA Palette
class Color:
    """ANSI 256-color codes for authentic early-3D visuals"""

    # Wall colors (VGA palette inspired)
    GRAY_DARK = 236
    GRAY_MED = 240
    GRAY_LIGHT = 246

    BRICK_DARK = 88
    BRICK_MED = 124
    BRICK_LIGHT = 167

    TILE_DARK = 23
    TILE_MED = 31
    TILE_LIGHT = 45

    CONCRETE_DARK = 234
    CONCRETE_MED = 238
    CONCRETE_LIGHT = 242

    GLASS_DARK = 25
    GLASS_MED = 33
    GLASS_LIGHT = 51

    METAL_DARK = 240
    METAL_MED = 248
    METAL_LIGHT = 255

    # Floor/ceiling
    FLOOR_DARK = 235
    FLOOR_MED = 237
    FLOOR_LIGHT = 239

    CEILING_DARK = 233
    CEILING_MED = 234
    CEILING_LIGHT = 235

    # UI
    HUD_BG = 17
    HUD_TEXT = 255
    HUD_WARN = 196

    @staticmethod
    def fg(code: int) -> str:
        """Get ANSI foreground color code"""
        return f"\033[38;5;{code}m"

    @staticmethod
    def bg(code: int) -> str:
        """Get ANSI background color code"""
        return f"\033[48;5;{code}m"

    @staticmethod
    def reset() -> str:
        """Reset all formatting"""
        return "\033[0m"


# Texture Definitions - Unicode block patterns
class Texture:
    """Wall texture patterns using Unicode blocks"""

    # Each texture is 8x8 pattern that tiles
    # 0=empty, 1=dark, 2=med, 3=light, 4=highlight

    BRICK = [
        "33333333",
        "31111113",
        "33333333",
        "13111131",
        "33333333",
        "31111113",
        "33333333",
        "13111131",
    ]

    TILE = [
        "44444444",
        "43333334",
        "43333334",
        "43333334",
        "44444444",
        "43333334",
        "43333334",
        "43333334",
    ]

    CONCRETE = [
        "22222222",
        "22212222",
        "22222222",
        "22222122",
        "22222222",
        "21222222",
        "22222222",
        "22222222",
    ]

    GLASS = [
        "33113311",
        "31111113",
        "11111111",
        "31111113",
        "33113311",
        "31111113",
        "11111111",
        "31111113",
    ]

    METAL = [
        "22222222",
        "44444444",
        "22222222",
        "44444444",
        "22222222",
        "44444444",
        "22222222",
        "44444444",
    ]

    CORRIDOR = [
        "11111111",
        "11111111",
        "11221122",
        "11221122",
        "11221122",
        "11221122",
        "11111111",
        "11111111",
    ]

    DOOR = [
        "44441111",
        "33331111",
        "33331111",
        "33331111",
        "33331111",
        "33331111",
        "33331111",
        "44441111",
    ]


@dataclass
class TextureMap:
    """Maps tile types to textures and colors"""
    pattern: List[str]
    colors: Tuple[int, int, int, int]  # (dark, med, light, highlight)


class WolfRenderer:
    """Wolfenstein 3D-style raycaster with textured walls"""

    def __init__(self, width: int = 120, height: int = 40):
        self.width = width
        self.height = height
        self.fov = 66  # Wolf3D FOV
        self.render_distance = 24

        # Screen buffer (for effects and post-processing)
        self.screen_buffer: List[List[Tuple[str, int]]] = []

        # Texture mapping
        self.textures = self._init_textures()

        # Unicode blocks for shading
        self.shade_chars = [" ", "░", "▒", "▓", "█"]

        # Extended shading for reality glitches (more detail)
        self.glitch_shade_chars = [" ", ".", "·", ":", "░", "▒", "▓", "█", "▓", "█"]

        # Photorealistic textures (revealed during glitches)
        self.photorealistic_textures = self._init_photorealistic_textures()

        # Previous frame for motion blur
        self.previous_buffer: List[List[Tuple[str, int]]] = []

    def _init_textures(self) -> Dict[str, TextureMap]:
        """Initialize texture mappings for each tile type"""
        return {
            "CORRIDOR": TextureMap(
                Texture.CORRIDOR,
                (Color.GRAY_DARK, Color.GRAY_MED, Color.GRAY_LIGHT, 255)
            ),
            "STORE_BORED": TextureMap(
                Texture.BRICK,
                (Color.BRICK_DARK, Color.BRICK_MED, Color.BRICK_LIGHT, 208)
            ),
            "STORE_MILO_OPTICS": TextureMap(
                Texture.GLASS,
                (Color.GLASS_DARK, Color.GLASS_MED, Color.GLASS_LIGHT, 87)
            ),
            "FOOD_COURT": TextureMap(
                Texture.TILE,
                (Color.TILE_DARK, Color.TILE_MED, Color.TILE_LIGHT, 51)
            ),
            "ANCHOR_STORE": TextureMap(
                Texture.CONCRETE,
                (Color.CONCRETE_DARK, Color.CONCRETE_MED, Color.CONCRETE_LIGHT, 244)
            ),
            "SERVICE_HALL": TextureMap(
                Texture.METAL,
                (Color.METAL_DARK, Color.METAL_MED, Color.METAL_LIGHT, 255)
            ),
            "KIOSK": TextureMap(
                Texture.TILE,
                (88, 94, 130, 165)
            ),
            "RESTROOM": TextureMap(
                Texture.TILE,
                (22, 28, 34, 40)
            ),
            "ENTRANCE": TextureMap(
                Texture.DOOR,
                (58, 64, 70, 76)
            ),
            "VOID": TextureMap(
                Texture.CONCRETE,
                (233, 234, 235, 236)
            ),
            "STORE_GENERIC": TextureMap(
                Texture.CORRIDOR,
                (239, 243, 247, 251)
            ),
        }

    def _init_photorealistic_textures(self) -> Dict[str, List[str]]:
        """
        High-resolution "photorealistic" textures that bleed through during glitches.
        These have MORE DETAIL than Wolf3D could ever handle - 16x16 patterns.
        """
        return {
            "CORRIDOR": [
                "4444444444444444",
                "4333333333333334",
                "4322222222222234",
                "4321111111111234",
                "4321111111111234",
                "4322111111112234",
                "4322211111122234",
                "4322221111222234",
                "4322222222222234",
                "4322221111222234",
                "4322211111122234",
                "4322111111112234",
                "4321111111111234",
                "4321111111111234",
                "4322222222222234",
                "4333333333333334",
            ],
            "BRICK": [
                "4444444444444444",
                "4332211443322114",
                "4332211443322114",
                "4444444444444444",
                "1443322114433221",
                "1443322114433221",
                "4444444444444444",
                "4332211443322114",
                "4332211443322114",
                "4444444444444444",
                "1443322114433221",
                "1443322114433221",
                "4444444444444444",
                "4332211443322114",
                "4332211443322114",
                "4444444444444444",
            ],
            # Add more if needed...
        }

    def cast_ray(self, player_x: float, player_y: float, ray_angle: float,
                 tile_grid: Dict[Tuple[int, int, int], Any]) -> Tuple[float, str, float, bool]:
        """
        Cast a single ray and return hit information.
        Returns: (distance, tile_type, wall_x, is_vertical_hit)
        """
        # Ray direction
        ray_dx = math.cos(math.radians(ray_angle))
        ray_dy = math.sin(math.radians(ray_angle))

        # DDA algorithm for grid traversal
        x = player_x
        y = player_y
        distance = 0.0
        step_size = 0.05

        while distance < self.render_distance:
            x += ray_dx * step_size
            y += ray_dy * step_size
            distance += step_size

            grid_x = int(x)
            grid_y = int(y)

            tile_key = (grid_x, grid_y, 0)
            if tile_key in tile_grid:
                tile = tile_grid[tile_key]
                if not tile.walkable:
                    # Calculate wall_x (texture coordinate)
                    wall_x = x - grid_x if abs(x - grid_x) > abs(y - grid_y) else y - grid_y
                    is_vertical = abs(x - grid_x) > abs(y - grid_y)
                    return distance, tile.type, wall_x, is_vertical

        return self.render_distance, "VOID", 0.0, False

    def get_texture_column(self, texture_map: TextureMap, wall_x: float,
                          distance: float, is_vertical: bool) -> List[Tuple[str, int]]:
        """
        Get a vertical slice of texture with colors.
        Returns list of (char, color) tuples.
        """
        pattern = texture_map.pattern
        colors = texture_map.colors

        # Get texture x coordinate (0-7)
        tex_x = int((wall_x % 1.0) * 8) % 8

        # Sample texture column
        column = []
        for tex_y in range(8):
            level = int(pattern[tex_y][tex_x])

            # Apply distance shading
            brightness = max(0.1, 1.0 - (distance / self.render_distance))

            # Darken vertical walls slightly (Wolf3D trick)
            if is_vertical:
                brightness *= 0.8

            # Map texture level to color
            if level == 0:
                char = " "
                color = colors[0]
            elif level == 1:
                color = colors[0]
                char = "░" if brightness > 0.7 else " "
            elif level == 2:
                color = colors[1]
                char = "▒" if brightness > 0.5 else "░"
            elif level == 3:
                color = colors[2]
                char = "▓" if brightness > 0.3 else "▒"
            else:  # level 4
                color = colors[3]
                char = "█"

            # Adjust color based on distance
            if brightness < 0.3:
                color = colors[0]
            elif brightness < 0.6:
                color = colors[1]

            column.append((char, color))

        return column

    def render_column(self, ray_index: int, distance: float, tile_type: str,
                     wall_x: float, is_vertical: bool) -> List[Tuple[str, int]]:
        """
        Render a single vertical column of screen.
        Returns list of (char, color) for each row.
        """
        column = []

        # Calculate wall height based on distance
        if distance < 0.5:
            distance = 0.5  # Prevent division by zero

        wall_height = int((self.height * 0.8) / distance)
        wall_height = min(self.height - 2, wall_height)

        # Get texture for this tile type
        texture_map = self.textures.get(tile_type, self.textures["VOID"])

        # Get textured column
        tex_column = self.get_texture_column(texture_map, wall_x, distance, is_vertical)

        # Sky/ceiling
        ceiling_height = (self.height - wall_height) // 2
        for i in range(ceiling_height):
            # Ceiling with gradient
            brightness = Color.CEILING_DARK + (i % 2)
            column.append((" ", brightness))

        # Wall (stretch texture to wall height)
        for i in range(wall_height):
            tex_y = int((i / wall_height) * len(tex_column))
            tex_y = min(tex_y, len(tex_column) - 1)
            column.append(tex_column[tex_y])

        # Floor
        floor_start = ceiling_height + wall_height
        for i in range(floor_start, self.height):
            # Floor with depth shading
            depth = (i - floor_start) / (self.height - floor_start) if (self.height - floor_start) > 0 else 0
            floor_char = "·" if (ray_index + i) % 3 == 0 else "."
            floor_color = Color.FLOOR_DARK + int(depth * 2)
            column.append((floor_char, floor_color))

        return column

    def render_frame(self, player_x: float, player_y: float, facing: Direction,
                    tile_grid: Dict[Tuple[int, int, int], Any],
                    distortions: Dict[str, float] = None,
                    reality_glitch_effects: Dict[str, float] = None) -> str:
        """
        Render complete frame in Wolfenstein 3D style.
        Now with reality glitches that reveal modern rendering underneath.
        """
        if distortions is None:
            distortions = {}
        if reality_glitch_effects is None:
            reality_glitch_effects = {}

        # Initialize screen buffer
        self.screen_buffer = [[(" ", 0) for _ in range(self.width)] for _ in range(self.height)]

        # Get player facing angle
        facing_angle = facing.value * 90

        # Cast rays for each column
        for col in range(self.width):
            # Calculate ray angle
            ray_offset = (col - self.width / 2) * (self.fov / self.width)
            ray_angle = facing_angle + ray_offset

            # Cast ray
            distance, tile_type, wall_x, is_vertical = self.cast_ray(
                player_x, player_y, ray_angle, tile_grid
            )

            # Render column
            column_data = self.render_column(col, distance, tile_type, wall_x, is_vertical)

            # Write to screen buffer
            for row, (char, color) in enumerate(column_data):
                if row < self.height:
                    self.screen_buffer[row][col] = (char, color)

        # Apply distortions
        self._apply_distortions(distortions)

        # Apply reality glitch effects (modern rendering bleeds through)
        self._apply_reality_glitches(reality_glitch_effects)

        # Convert buffer to string with ANSI codes
        return self._buffer_to_string()

    def _apply_distortions(self, distortions: Dict[str, float]):
        """Apply toddler-induced visual corruption"""
        vignette = distortions.get("vignette", 0)
        glitch = distortions.get("glitch", 0)

        # Vignette effect (darken edges)
        if vignette > 0.1:
            center_y = self.height // 2
            center_x = self.width // 2

            for y in range(self.height):
                for x in range(self.width):
                    dist_from_center = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    max_dist = math.sqrt(center_x**2 + center_y**2)

                    if dist_from_center / max_dist > (1.0 - vignette * 0.5):
                        char, color = self.screen_buffer[y][x]
                        # Darken
                        self.screen_buffer[y][x] = (char, max(233, color - 10))

        # Glitch effect (random corruption)
        if glitch > 0.1:
            glitch_count = int(self.width * self.height * glitch * 0.01)
            for _ in range(glitch_count):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                glitch_char = random.choice("█▓▒░#*@%")
                glitch_color = random.choice([196, 208, 226, 227])
                self.screen_buffer[y][x] = (glitch_char, glitch_color)

        # Chromatic aberration (color shift)
        chromatic = distortions.get("chromatic_aberration", 0)
        if chromatic > 0.2 and random.random() < 0.1:
            # Shift some lines
            y = random.randint(0, self.height - 1)
            shift = random.randint(-2, 2)
            if 0 <= y < self.height:
                row = self.screen_buffer[y]
                if shift > 0:
                    self.screen_buffer[y] = [(" ", 0)] * shift + row[:-shift]
                elif shift < 0:
                    self.screen_buffer[y] = row[-shift:] + [(" ", 0)] * (-shift)

    def _apply_reality_glitches(self, effects: Dict[str, float]):
        """
        Apply modern rendering effects that bleed through the facade.
        The simulation is breaking. You see what's really underneath.
        """
        # Depth of field (distant blur)
        dof = effects.get("depth_of_field", 0)
        if dof > 0.3:
            self._apply_depth_of_field(dof)

        # Motion blur (temporal sampling)
        motion_blur = effects.get("motion_blur", 0)
        if motion_blur > 0.3:
            self._apply_motion_blur(motion_blur)

        # Bloom (HDR light bleeding)
        bloom = effects.get("bloom", 0)
        if bloom > 0.3:
            self._apply_bloom(bloom)

        # Ambient occlusion (contact shadows)
        ao = effects.get("ambient_occlusion", 0)
        if ao > 0.3:
            self._apply_ambient_occlusion(ao)

        # Photorealistic texture leak
        photorealistic = effects.get("photorealistic", 0)
        if photorealistic > 0.5:
            self._apply_photorealistic_leak(photorealistic)

        # Debug wireframe
        if effects.get("wireframe", 0) > 0:
            self._apply_wireframe_overlay()

        # Simulation debug info
        if effects.get("debug_info", 0) > 0:
            self._apply_debug_overlay(effects.get("debug_text", []))

    def _apply_depth_of_field(self, strength: float):
        """Blur background naturally - like a camera lens (shouldn't exist in Wolf3D)"""
        # Blur edges more than center (fake DOF)
        center_y = self.height // 2
        center_x = self.width // 2

        for y in range(self.height):
            for x in range(0, self.width, 2):  # Sample every other column for performance
                dist_from_center = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                max_dist = math.sqrt(center_x**2 + center_y**2)
                blur_factor = (dist_from_center / max_dist) * strength

                if blur_factor > 0.4 and random.random() < blur_factor:
                    # Simple blur: replace with dimmer version
                    char, color = self.screen_buffer[y][x]
                    if char in "█▓▒░":
                        blur_chars = {"█": "▓", "▓": "▒", "▒": "░", "░": " "}
                        self.screen_buffer[y][x] = (blur_chars.get(char, char), color)

    def _apply_motion_blur(self, strength: float):
        """Temporal sampling - motion smears realistically"""
        if not self.previous_buffer or len(self.previous_buffer) != len(self.screen_buffer):
            # Save current as previous for next frame
            self.previous_buffer = [row[:] for row in self.screen_buffer]
            return

        # Blend current with previous frame
        for y in range(self.height):
            for x in range(0, self.width, 3):  # Sample sparse for performance
                if random.random() < strength * 0.5:
                    # Use previous frame's character
                    self.screen_buffer[y][x] = self.previous_buffer[y][x]

        # Update previous buffer
        self.previous_buffer = [row[:] for row in self.screen_buffer]

    def _apply_bloom(self, strength: float):
        """HDR light bleeding - bright areas glow"""
        # Find bright pixels and make them bleed
        bright_threshold = 200

        for y in range(self.height):
            for x in range(self.width):
                char, color = self.screen_buffer[y][x]

                if color >= bright_threshold and char in "█▓":
                    # Make neighbors brighter too (bloom effect)
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < self.height and 0 <= nx < self.width:
                                if random.random() < strength:
                                    n_char, n_color = self.screen_buffer[ny][nx]
                                    # Brighten neighbor
                                    self.screen_buffer[ny][nx] = (n_char, min(255, n_color + 10))

    def _apply_ambient_occlusion(self, strength: float):
        """Screen-space ambient occlusion - corners darken naturally"""
        # Darken areas near "edges" (character transitions)
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                char, color = self.screen_buffer[y][x]

                # Check neighbors for occlusion
                neighbors = [
                    self.screen_buffer[y-1][x][0],
                    self.screen_buffer[y+1][x][0],
                    self.screen_buffer[y][x-1][0],
                    self.screen_buffer[y][x+1][0],
                ]

                # Count solid neighbors
                solid_count = sum(1 for n in neighbors if n in "█▓▒")

                if solid_count >= 3 and random.random() < strength:
                    # Darken this pixel (contact shadow)
                    self.screen_buffer[y][x] = (char, max(233, color - 15))

    def _apply_photorealistic_leak(self, strength: float):
        """Textures become photographs - too detailed for Wolf3D"""
        # Randomly replace texture characters with higher detail versions
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < strength * 0.1:
                    char, color = self.screen_buffer[y][x]

                    # Replace with MORE DETAILED character
                    if char == "░":
                        self.screen_buffer[y][x] = (":", color)
                    elif char == "▒":
                        self.screen_buffer[y][x] = ("▓", min(255, color + 5))
                    elif char in ".·":
                        # Floor gets way too detailed
                        detail_chars = [".", ":", "·", "∙", "•"]
                        self.screen_buffer[y][x] = (random.choice(detail_chars), color)

    def _apply_wireframe_overlay(self):
        """Show geometry wireframe - reveals the mesh underneath"""
        # Draw grid lines (shows polygon edges bleeding through)
        for y in range(0, self.height, 4):
            for x in range(self.width):
                if random.random() < 0.3:
                    self.screen_buffer[y][x] = ("─", 46)  # Cyan wireframe

        for x in range(0, self.width, 8):
            for y in range(self.height):
                if random.random() < 0.3:
                    self.screen_buffer[y][x] = ("│", 46)

    def _apply_debug_overlay(self, debug_text: List[str]):
        """Show debug info from real engine underneath"""
        # Overlay debug text in corner
        start_y = 2
        start_x = 2

        for i, line in enumerate(debug_text[:min(10, self.height - 4)]):
            y = start_y + i
            if y >= self.height:
                break

            for j, char in enumerate(line[:min(40, self.width - 4)]):
                x = start_x + j
                if x >= self.width:
                    break

                # Bright green debug text
                self.screen_buffer[y][x] = (char, 46)

    def _buffer_to_string(self) -> str:
        """Convert screen buffer to ANSI string"""
        lines = []
        for row in self.screen_buffer:
            line = ""
            current_color = None
            for char, color in row:
                if color != current_color:
                    line += Color.fg(color)
                    current_color = color
                line += char
            line += Color.reset()
            lines.append(line)
        return "\n".join(lines)


class Wolf3DHUD:
    """Authentic Wolfenstein 3D-style HUD"""

    def __init__(self, width: int = 120):
        self.width = width

    def render(self, player_data: Dict[str, Any], toddler_stage: int) -> str:
        """Render HUD bar"""
        x, y = player_data.get("position", (0, 0))
        playtime = player_data.get("playtime", 0)
        inventory_count = player_data.get("inventory_count", 0)

        minutes = playtime // 60
        seconds = playtime % 60

        # Build HUD
        hud = f"{Color.bg(Color.HUD_BG)}{Color.fg(Color.HUD_TEXT)}"

        # Left side - position and time
        left = f" [{x:02d},{y:02d}] "

        # Center - inventory
        center = f" ITEMS:{inventory_count:02d} "

        # Right side - time and stage
        if toddler_stage >= 2:
            stage_color = Color.fg(Color.HUD_WARN)
            stage_text = "!DANGER!"
        elif toddler_stage >= 1:
            stage_color = Color.fg(208)
            stage_text = "CAUTION"
        else:
            stage_color = Color.fg(Color.HUD_TEXT)
            stage_text = "SECURE"

        right = f" {minutes:02d}:{seconds:02d} {stage_color}{stage_text}{Color.fg(Color.HUD_TEXT)} "

        # Calculate spacing
        total_content = len(left) + len(center) + len(right)
        # Account for color codes (approximately)
        remaining = self.width - (len(left) + len(center) + len(right))

        left_pad = remaining // 2
        right_pad = remaining - left_pad

        hud += left + (" " * left_pad) + center + (" " * right_pad) + right
        hud += Color.reset()

        return hud

    def render_message(self, message: str, msg_type: str = "normal") -> str:
        """Render a message bar"""
        if msg_type == "audio":
            color = Color.fg(208)
        elif msg_type == "danger":
            color = Color.fg(Color.HUD_WARN)
        elif msg_type == "shadow":
            color = Color.fg(240)
        else:
            color = Color.fg(Color.HUD_TEXT)

        return f"{color}>>> {message}{Color.reset()}"
