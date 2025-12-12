#!/usr/bin/env python3
"""
PYGAME RAYCASTER RENDERER - V3 Eastland Mall
Proper Wolf3D-style raycasting with texture support and era-bleed effects.
"""

import pygame
import math
import os
import random
from typing import Dict, List, Tuple, Optional

# Initialize Pygame
pygame.init()


class TextureManager:
    """Manages textures with decay/modern variants for era-bleed effect."""

    def __init__(self):
        self.textures: Dict[str, pygame.Surface] = {}
        self.decay_textures: Dict[str, pygame.Surface] = {}
        self.modern_textures: Dict[str, pygame.Surface] = {}
        self.texture_size = 64

        # Generate procedural textures
        self._generate_textures()

    def _generate_textures(self):
        """Generate procedural textures for different tile types."""
        # Wall textures (decay era - late 80s worn look)
        self.textures['CORRIDOR'] = self._create_tile_texture((80, 85, 75), (60, 65, 55))
        self.textures['VOID'] = self._create_solid_texture((20, 20, 25))
        self.textures['ENTRANCE'] = self._create_glass_texture((100, 120, 130))
        self.textures['ANCHOR_STORE'] = self._create_brick_texture((90, 80, 70), (70, 60, 50))
        self.textures['FOOD_COURT'] = self._create_tile_texture((120, 90, 60), (100, 70, 40))
        self.textures['SERVICE_HALL'] = self._create_concrete_texture((100, 95, 90))
        self.textures['KIOSK'] = self._create_glass_texture((80, 100, 110))
        self.textures['RESTROOM'] = self._create_tile_texture((150, 150, 140), (130, 130, 120))
        self.textures['RAMP_DOWN'] = self._create_tile_texture((70, 75, 80), (50, 55, 60))

        # Store textures
        self.textures['STORE_BORED'] = self._create_graffiti_texture()
        self.textures['STORE_MILO_OPTICS'] = self._create_tile_texture((100, 120, 140), (80, 100, 120))
        self.textures['STORE_HARD_COPY'] = self._create_neon_texture()
        self.textures['STORE_COMPHUT'] = self._create_tile_texture((150, 140, 80), (130, 120, 60))
        self.textures['STORE_WIZARD_BUNKER'] = self._create_tile_texture((100, 80, 120), (80, 60, 100))
        self.textures['STORE_OUT_OF_SERVICE'] = self._create_tile_texture((140, 140, 140), (120, 120, 120))
        self.textures['STORE_GENERIC'] = self._create_tile_texture((110, 105, 100), (90, 85, 80))

        # Theater textures
        self.textures['THEATER_ENTRANCE'] = self._create_velvet_texture((120, 30, 40))
        self.textures['THEATER_LOBBY'] = self._create_carpet_texture((80, 30, 35))
        self.textures['THEATER_SCREEN_1'] = self._create_solid_texture((20, 20, 30))
        self.textures['THEATER_EMPTY'] = self._create_solid_texture((15, 15, 20))

        # Modern textures (for era-bleed at high heat)
        self._generate_modern_textures()

    def _generate_modern_textures(self):
        """Generate modern/renovated versions of textures."""
        # Clean, bright, modern mall aesthetic
        self.modern_textures['CORRIDOR'] = self._create_tile_texture((200, 200, 195), (180, 180, 175))
        self.modern_textures['ANCHOR_STORE'] = self._create_tile_texture((220, 215, 210), (200, 195, 190))
        self.modern_textures['FOOD_COURT'] = self._create_tile_texture((210, 180, 150), (190, 160, 130))
        self.modern_textures['STORE_HARD_COPY'] = self._create_modern_neon_texture()

    def _create_solid_texture(self, color: Tuple[int, int, int]) -> pygame.Surface:
        """Create a solid color texture."""
        surf = pygame.Surface((self.texture_size, self.texture_size))
        surf.fill(color)
        return surf

    def _create_tile_texture(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> pygame.Surface:
        """Create a tiled floor/wall texture."""
        surf = pygame.Surface((self.texture_size, self.texture_size))
        surf.fill(color1)

        # Draw tile pattern
        tile_size = 16
        for y in range(0, self.texture_size, tile_size):
            for x in range(0, self.texture_size, tile_size):
                if (x // tile_size + y // tile_size) % 2 == 0:
                    pygame.draw.rect(surf, color2, (x, y, tile_size, tile_size))

        # Add grout lines
        grout_color = (color2[0] - 20, color2[1] - 20, color2[2] - 20)
        for i in range(0, self.texture_size, tile_size):
            pygame.draw.line(surf, grout_color, (i, 0), (i, self.texture_size - 1))
            pygame.draw.line(surf, grout_color, (0, i), (self.texture_size - 1, i))

        return surf

    def _create_brick_texture(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> pygame.Surface:
        """Create a brick wall texture."""
        surf = pygame.Surface((self.texture_size, self.texture_size))
        surf.fill(color2)

        brick_h = 8
        brick_w = 16

        for row in range(self.texture_size // brick_h):
            offset = (row % 2) * (brick_w // 2)
            for col in range(-1, self.texture_size // brick_w + 1):
                x = col * brick_w + offset
                y = row * brick_h
                pygame.draw.rect(surf, color1, (x + 1, y + 1, brick_w - 2, brick_h - 2))

        return surf

    def _create_glass_texture(self, tint: Tuple[int, int, int]) -> pygame.Surface:
        """Create a glass/window texture."""
        surf = pygame.Surface((self.texture_size, self.texture_size))
        surf.fill(tint)

        # Add reflection lines
        for i in range(0, self.texture_size, 8):
            highlight = (min(255, tint[0] + 30), min(255, tint[1] + 30), min(255, tint[2] + 30))
            pygame.draw.line(surf, highlight, (i, 0), (0, i))

        return surf

    def _create_concrete_texture(self, base: Tuple[int, int, int]) -> pygame.Surface:
        """Create a concrete texture."""
        surf = pygame.Surface((self.texture_size, self.texture_size))
        surf.fill(base)

        # Add noise/speckles
        import random
        for _ in range(200):
            x = random.randint(0, self.texture_size - 1)
            y = random.randint(0, self.texture_size - 1)
            variance = random.randint(-15, 15)
            color = (
                max(0, min(255, base[0] + variance)),
                max(0, min(255, base[1] + variance)),
                max(0, min(255, base[2] + variance))
            )
            surf.set_at((x, y), color)

        return surf

    def _create_graffiti_texture(self) -> pygame.Surface:
        """Create BORED's skateshop graffiti texture."""
        surf = pygame.Surface((self.texture_size, self.texture_size))
        surf.fill((30, 30, 35))  # Dark base

        # Random color splotches (stickers/posters)
        import random
        colors = [(200, 50, 50), (50, 200, 50), (50, 50, 200), (200, 200, 50), (200, 50, 200)]
        for _ in range(10):
            x = random.randint(0, self.texture_size - 10)
            y = random.randint(0, self.texture_size - 10)
            w = random.randint(5, 15)
            h = random.randint(5, 15)
            color = random.choice(colors)
            pygame.draw.rect(surf, color, (x, y, w, h))

        return surf

    def _create_neon_texture(self) -> pygame.Surface:
        """Create HARD COPY neon/arcade texture."""
        surf = pygame.Surface((self.texture_size, self.texture_size))
        surf.fill((10, 5, 20))  # Dark purple-black

        # Neon lines
        pygame.draw.line(surf, (255, 0, 255), (0, 16), (self.texture_size, 16), 2)  # Magenta
        pygame.draw.line(surf, (0, 255, 255), (0, 32), (self.texture_size, 32), 2)  # Cyan
        pygame.draw.line(surf, (255, 0, 255), (0, 48), (self.texture_size, 48), 2)  # Magenta

        # Glow effect
        for y in [16, 32, 48]:
            for offset in [1, 2]:
                alpha_color = (100, 0, 100) if y != 32 else (0, 100, 100)
                pygame.draw.line(surf, alpha_color, (0, y - offset), (self.texture_size, y - offset))
                pygame.draw.line(surf, alpha_color, (0, y + offset), (self.texture_size, y + offset))

        return surf

    def _create_modern_neon_texture(self) -> pygame.Surface:
        """Create modern/high-res version of HARD COPY."""
        surf = pygame.Surface((self.texture_size, self.texture_size))
        surf.fill((15, 10, 30))

        # Brighter, cleaner neon
        pygame.draw.line(surf, (255, 50, 255), (0, 16), (self.texture_size, 16), 3)
        pygame.draw.line(surf, (50, 255, 255), (0, 32), (self.texture_size, 32), 3)
        pygame.draw.line(surf, (255, 255, 50), (0, 48), (self.texture_size, 48), 3)

        return surf

    def _create_velvet_texture(self, color: Tuple[int, int, int]) -> pygame.Surface:
        """Create theater velvet texture."""
        surf = pygame.Surface((self.texture_size, self.texture_size))
        surf.fill(color)

        # Vertical stripe pattern
        for x in range(0, self.texture_size, 4):
            darker = (max(0, color[0] - 20), max(0, color[1] - 10), max(0, color[2] - 10))
            pygame.draw.line(surf, darker, (x, 0), (x, self.texture_size - 1))

        return surf

    def _create_carpet_texture(self, color: Tuple[int, int, int]) -> pygame.Surface:
        """Create carpet texture."""
        surf = pygame.Surface((self.texture_size, self.texture_size))
        surf.fill(color)

        # Speckled pattern
        import random
        for _ in range(300):
            x = random.randint(0, self.texture_size - 1)
            y = random.randint(0, self.texture_size - 1)
            variance = random.randint(-10, 10)
            speckle = (
                max(0, min(255, color[0] + variance)),
                max(0, min(255, color[1] + variance)),
                max(0, min(255, color[2] + variance))
            )
            surf.set_at((x, y), speckle)

        return surf

    def get_texture(self, tile_type: str, heat_level: float = 0) -> pygame.Surface:
        """Get texture with era-bleed based on heat level."""
        # At high heat, blend toward modern textures
        if heat_level >= 4 and tile_type in self.modern_textures:
            blend = (heat_level - 4) / 2  # 0-1 blend factor
            decay = self.textures.get(tile_type, self.textures['CORRIDOR'])
            modern = self.modern_textures[tile_type]
            return self._blend_textures(decay, modern, blend)

        return self.textures.get(tile_type, self.textures['CORRIDOR'])

    def _blend_textures(self, tex1: pygame.Surface, tex2: pygame.Surface, blend: float) -> pygame.Surface:
        """Blend two textures together."""
        result = tex1.copy()
        tex2_copy = tex2.copy()
        tex2_copy.set_alpha(int(blend * 255))
        result.blit(tex2_copy, (0, 0))
        return result


class PygameRaycaster:
    """Wolf3D-style raycaster renderer using Pygame."""

    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("EASTLAND MALL - V3")

        # Rendering settings
        self.fov = math.pi / 3  # 60 degrees
        self.half_fov = self.fov / 2
        self.num_rays = width // 2  # One ray per 2 pixels for performance
        self.max_depth = 50
        self.wall_height_scale = 300

        # Textures
        self.textures = TextureManager()

        # Colors
        self.ceiling_color = (40, 45, 50)  # Dark gray-blue
        self.floor_color = (60, 55, 50)  # Brown-gray

        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)

        # Clock for FPS
        self.clock = pygame.time.Clock()

    def cast_rays(self, player_x: float, player_y: float, player_angle: float,
                  world_tiles: Dict) -> List[Tuple[float, str, float]]:
        """Cast rays and return wall distances and types."""
        rays = []
        ray_angle_step = self.fov / self.num_rays

        for i in range(self.num_rays):
            ray_angle = player_angle - self.half_fov + i * ray_angle_step

            # Ray direction
            ray_dx = math.cos(ray_angle)
            ray_dy = math.sin(ray_angle)

            # DDA algorithm for raycasting
            distance = 0
            hit_type = 'VOID'
            texture_x = 0

            # Step through the map
            for depth in range(self.max_depth * 10):
                distance = depth * 0.1
                check_x = player_x + ray_dx * distance
                check_y = player_y + ray_dy * distance

                tile_x = int(check_x)
                tile_y = int(check_y)

                # Check if we hit a wall
                tile = world_tiles.get((tile_x, tile_y, 0))
                if tile is None or not tile.get('walkable', False):
                    hit_type = tile['type'] if tile else 'VOID'

                    # Calculate texture X coordinate
                    if abs(ray_dx) > abs(ray_dy):
                        texture_x = check_y % 1
                    else:
                        texture_x = check_x % 1

                    break

            # Fix fisheye effect
            distance *= math.cos(ray_angle - player_angle)
            rays.append((distance, hit_type, texture_x))

        return rays

    def render_3d_view(self, rays: List[Tuple[float, str, float]], heat_level: float = 0):
        """Render the 3D raycasted view."""
        # Draw ceiling and floor
        pygame.draw.rect(self.screen, self.ceiling_color, (0, 0, self.width, self.height // 2))
        pygame.draw.rect(self.screen, self.floor_color, (0, self.height // 2, self.width, self.height // 2))

        # Draw walls
        strip_width = self.width // len(rays)

        for i, (distance, tile_type, tex_x) in enumerate(rays):
            if distance <= 0:
                distance = 0.001

            # Calculate wall height
            wall_height = min(self.height, int(self.wall_height_scale / distance))

            # Get texture column
            texture = self.textures.get_texture(tile_type, heat_level)
            tex_column = int(tex_x * texture.get_width())

            # Extract and scale texture column
            column_rect = pygame.Rect(tex_column, 0, 1, texture.get_height())
            column = texture.subsurface(column_rect)
            scaled_column = pygame.transform.scale(column, (strip_width, wall_height))

            # Apply distance shading
            shade = max(0.2, 1.0 - distance / self.max_depth)
            shaded = scaled_column.copy()
            dark_surface = pygame.Surface(shaded.get_size())
            dark_surface.fill((0, 0, 0))
            dark_surface.set_alpha(int((1 - shade) * 200))
            shaded.blit(dark_surface, (0, 0))

            # Draw the wall strip
            wall_y = (self.height - wall_height) // 2
            self.screen.blit(shaded, (i * strip_width, wall_y))

    def render_minimap(self, player_x: float, player_y: float, player_angle: float,
                       world_tiles: Dict, npc_states: Dict = None, size: int = 150):
        """Render a minimap in the corner with NPC positions."""
        if npc_states is None:
            npc_states = {}

        # Create minimap surface
        minimap = pygame.Surface((size, size))
        minimap.fill((20, 20, 20))

        scale = 3  # Pixels per tile
        offset_x = size // 2 - int(player_x * scale)
        offset_y = size // 2 - int(player_y * scale)

        # Draw tiles
        for (tx, ty, tz), tile in world_tiles.items():
            if tz != 0:
                continue  # Only draw current floor

            screen_x = tx * scale + offset_x
            screen_y = ty * scale + offset_y

            if 0 <= screen_x < size and 0 <= screen_y < size:
                # Handle both dict and Tile object formats
                walkable = tile.get('walkable') if isinstance(tile, dict) else getattr(tile, 'walkable', False)
                if walkable:
                    color = (60, 60, 60)  # Walkable
                else:
                    color = (100, 100, 100)  # Wall

                # Color code special areas
                tile_type = tile.get('type', '') if isinstance(tile, dict) else getattr(tile, 'type', '')
                if 'STORE' in tile_type:
                    color = (40, 100, 40)
                elif 'FOOD_COURT' in tile_type:
                    color = (100, 100, 40)
                elif 'ANCHOR' in tile_type:
                    color = (100, 40, 100)

                pygame.draw.rect(minimap, color, (screen_x, screen_y, scale, scale))

        # Draw NPCs on minimap
        for npc_id, npc_data in npc_states.items():
            if not isinstance(npc_data, dict) or 'position' not in npc_data:
                continue

            pos = npc_data['position']
            npc_x, npc_y = pos[0], pos[1]
            npc_screen_x = int(npc_x * scale + offset_x)
            npc_screen_y = int(npc_y * scale + offset_y)

            if 0 <= npc_screen_x < size and 0 <= npc_screen_y < size:
                # Color by faction
                faction = npc_data.get('faction', 'neutral')
                if faction == 'security':
                    npc_color = (100, 100, 255)
                elif faction == 'workers':
                    npc_color = (100, 255, 100)
                elif faction == 'teens':
                    npc_color = (255, 255, 100)
                else:
                    npc_color = (200, 200, 200)

                pygame.draw.circle(minimap, npc_color, (npc_screen_x, npc_screen_y), 2)

        # Draw player
        player_screen_x = size // 2
        player_screen_y = size // 2
        pygame.draw.circle(minimap, (255, 255, 0), (player_screen_x, player_screen_y), 3)

        # Draw player direction
        dir_x = player_screen_x + int(math.cos(player_angle) * 8)
        dir_y = player_screen_y + int(math.sin(player_angle) * 8)
        pygame.draw.line(minimap, (255, 255, 0), (player_screen_x, player_screen_y), (dir_x, dir_y), 2)

        # Draw border
        pygame.draw.rect(minimap, (100, 100, 100), (0, 0, size, size), 1)

        # Blit to screen
        self.screen.blit(minimap, (self.width - size - 10, 10))

    def render_hud(self, player_x: float, player_y: float, player_z: int,
                   heat_level: float, fps: int, heat_stars: str = '', reality_stability: float = 100):
        """Render the HUD elements with simulation data."""
        # Heat meter - use simulation heat_stars if available
        if heat_stars:
            heat_text = f"HEAT: {heat_stars}"
        else:
            heat_text = f"HEAT: {'★' * int(heat_level)}{'☆' * (5 - int(heat_level))}"

        heat_color = (255, 255, 255)
        if heat_level >= 3:
            heat_color = (255, 200, 0)
        if heat_level >= 4:
            heat_color = (255, 100, 0)
        if heat_level >= 5:
            heat_color = (255, 0, 0)

        heat_surf = self.font.render(heat_text, True, heat_color)
        self.screen.blit(heat_surf, (10, 10))

        # Reality stability meter
        if reality_stability < 100:
            stability_color = (100, 255, 100) if reality_stability > 50 else (255, 100, 100)
            stability_text = f"REALITY: {int(reality_stability)}%"
            stability_surf = self.font.render(stability_text, True, stability_color)
            self.screen.blit(stability_surf, (10, 55))

        # Position
        z_str = f"B{abs(player_z)}" if player_z < 0 else f"L{player_z}"
        pos_text = f"[{int(player_x)}, {int(player_y)}, {z_str}]"
        pos_surf = self.font.render(pos_text, True, (200, 200, 200))
        self.screen.blit(pos_surf, (10, 35))

        # FPS
        fps_surf = self.font.render(f"FPS: {fps}", True, (150, 150, 150))
        self.screen.blit(fps_surf, (10, self.height - 30))

        # Controls hint
        controls = "WASD: Move | Q: Quit | E: Interact | H/G: Heat"
        controls_surf = self.font.render(controls, True, (100, 100, 100))
        self.screen.blit(controls_surf, (self.width // 2 - controls_surf.get_width() // 2, self.height - 30))

    def render_glitch_overlay(self, heat_level: float, micro_glitches: Dict = None, reality_breaking: bool = False):
        """Render glitch effects from simulation data."""
        if micro_glitches is None:
            micro_glitches = {}

        # Always check for active glitches from simulation
        active_glitches = micro_glitches.get('active_glitches', [])

        # Render micro-glitches from simulation
        for glitch in active_glitches:
            glitch_type = glitch.get('type', '')
            intensity = glitch.get('intensity', 0.5)

            if glitch_type == 'color_shift':
                overlay = pygame.Surface((self.width, self.height))
                overlay.fill((255, 0, 255))
                overlay.set_alpha(int(intensity * 50))
                self.screen.blit(overlay, (0, 0))
            elif glitch_type == 'scanline_tear':
                y = random.randint(0, self.height - 20)
                for i in range(20):
                    offset = int(random.random() * intensity * 20)
                    line = pygame.Surface((self.width, 1))
                    line.fill((0, 0, 0))
                    line.set_alpha(int(intensity * 100))
                    self.screen.blit(line, (offset, y + i))

        # Heat-based effects (fallback when no simulation)
        if heat_level < 2 and not active_glitches and not reality_breaking:
            return

        # Scanlines
        if heat_level >= 2:
            for y in range(0, self.height, 4):
                alpha = int((heat_level - 2) * 30)
                line = pygame.Surface((self.width, 1))
                line.fill((0, 0, 0))
                line.set_alpha(alpha)
                self.screen.blit(line, (0, y))

        # Color aberration at high heat
        if heat_level >= 4:
            # Shift red channel
            offset = int((heat_level - 4) * 3)
            if offset > 0:
                overlay = pygame.Surface((self.width, self.height))
                overlay.fill((255, 0, 0))
                overlay.set_alpha(20)
                self.screen.blit(overlay, (offset, 0))

        # Static noise at heat 5 or reality breaking
        if heat_level >= 5 or reality_breaking:
            noise_amount = int(heat_level * 100) if heat_level >= 5 else 300
            for _ in range(noise_amount):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                color = random.choice([(255, 255, 255), (0, 0, 0)])
                self.screen.set_at((x, y), color)

            # Extra reality break effects
            if reality_breaking:
                # Magenta tears
                for _ in range(10):
                    x = random.randint(0, self.width)
                    pygame.draw.line(self.screen, (255, 0, 255),
                                   (x, 0), (x + random.randint(-30, 30), self.height), 2)

    def render(self, player_x: float, player_y: float, player_z: int,
               player_angle: float, world_tiles: Dict, heat_level: float = 0,
               npcs: List = None, render_hints: Dict = None):
        """Main render function with AI simulation data."""
        if render_hints is None:
            render_hints = {}

        # Cast rays
        rays = self.cast_rays(player_x, player_y, player_angle, world_tiles)

        # Render 3D view
        self.render_3d_view(rays, heat_level)

        # Render NPCs from simulation
        npc_states = render_hints.get('npcs', {})
        if npc_states:
            self.render_npc_sprites(npc_states, player_x, player_y, player_angle)

        # Render glitch effects (enhanced by simulation)
        micro_glitches = render_hints.get('micro_glitches', {})
        reality_breaking = render_hints.get('reality_breaking', False)
        self.render_glitch_overlay(heat_level, micro_glitches, reality_breaking)

        # Render revelation effects at Heat 5
        revelation = render_hints.get('revelation', {})
        if revelation.get('active'):
            self.render_revelation_effects(revelation)

        # Render HUD with simulation data
        fps = int(self.clock.get_fps())
        heat_stars = render_hints.get('heat_stars', '')
        reality_stability = render_hints.get('reality_stability', 100)
        self.render_hud(player_x, player_y, player_z, heat_level, fps, heat_stars, reality_stability)

        # Render minimap with NPC positions
        self.render_minimap(player_x, player_y, player_angle, world_tiles, npc_states)

        # Update display
        pygame.display.flip()
        self.clock.tick(60)

    def render_npc_sprites(self, npc_states: Dict, player_x: float, player_y: float, player_angle: float):
        """Render NPCs as sprites in the 3D view (billboarding)."""
        # Collect NPC distances for depth sorting
        npc_distances = []
        for npc_id, npc_data in npc_states.items():
            if not isinstance(npc_data, dict) or 'position' not in npc_data:
                continue

            pos = npc_data['position']
            npc_x, npc_y = pos[0], pos[1]

            # Calculate distance and angle to NPC
            dx = npc_x - player_x
            dy = npc_y - player_y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 0.5:  # Too close
                continue

            # Calculate angle to NPC relative to player facing
            npc_angle = math.atan2(dy, dx)
            relative_angle = npc_angle - player_angle

            # Normalize angle to [-pi, pi]
            while relative_angle > math.pi:
                relative_angle -= 2 * math.pi
            while relative_angle < -math.pi:
                relative_angle += 2 * math.pi

            # Check if NPC is in field of view
            if abs(relative_angle) < math.pi / 3:  # 60 degree FOV
                npc_distances.append((distance, relative_angle, npc_id, npc_data))

        # Sort by distance (far to near for proper overdraw)
        npc_distances.sort(reverse=True)

        for distance, relative_angle, npc_id, npc_data in npc_distances:
            # Calculate screen position
            screen_x = int(self.width / 2 + relative_angle * self.width / (math.pi / 3))

            # Calculate sprite size based on distance
            sprite_height = int(self.height * 0.6 / distance)
            sprite_width = sprite_height // 2

            if sprite_height < 2:
                continue

            # Draw simple NPC representation (colored rectangle for now)
            faction = npc_data.get('faction', 'neutral')
            if faction == 'security':
                color = (100, 100, 255)  # Blue for security
            elif faction == 'workers':
                color = (100, 255, 100)  # Green for workers
            elif faction == 'teens':
                color = (255, 255, 100)  # Yellow for teens
            else:
                color = (200, 200, 200)  # Gray for others

            # Draw sprite
            sprite_y = self.height // 2 - sprite_height // 2
            pygame.draw.rect(self.screen, color,
                           (screen_x - sprite_width // 2, sprite_y,
                            sprite_width, sprite_height))

            # Draw NPC indicator dot on top
            pygame.draw.circle(self.screen, (255, 200, 200),
                             (screen_x, sprite_y - 5),
                             max(2, sprite_width // 4))

    def render_revelation_effects(self, revelation: Dict):
        """Render Heat 5 revelation visual effects."""
        phase = revelation.get('phase', 0)

        if phase >= 1:
            # Color inversion patches
            for _ in range(phase * 5):
                x = random.randint(0, self.width - 50)
                y = random.randint(0, self.height - 50)
                w = random.randint(20, 100)
                h = random.randint(20, 100)

                # Create inverted color surface
                patch = pygame.Surface((w, h))
                patch.fill((255, 255, 255))
                patch.set_alpha(50 + phase * 20)
                self.screen.blit(patch, (x, y), special_flags=pygame.BLEND_SUB)

        if phase >= 2:
            # Reality tear lines
            for _ in range(phase * 3):
                x = random.randint(0, self.width)
                pygame.draw.line(self.screen, (255, 0, 255),
                               (x, 0), (x + random.randint(-50, 50), self.height), 2)

        if phase >= 3:
            # The mask is fully breaking
            overlay = pygame.Surface((self.width, self.height))
            overlay.fill((255, 0, 255))
            overlay.set_alpha(30 + phase * 10)
            self.screen.blit(overlay, (0, 0))

    def handle_events(self) -> Tuple[bool, Dict]:
        """Handle pygame events and return input state."""
        running = True
        inputs = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False,
            'strafe_left': False,
            'strafe_right': False,
            'interact': False,
            'quit': False,
            'map': False,
            'inventory': False
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    inputs['quit'] = True
                elif event.key == pygame.K_e:
                    inputs['interact'] = True
                elif event.key == pygame.K_m:
                    inputs['map'] = True
                elif event.key == pygame.K_TAB:
                    inputs['inventory'] = True

        # Continuous key states
        keys = pygame.key.get_pressed()
        inputs['forward'] = keys[pygame.K_w] or keys[pygame.K_UP]
        inputs['backward'] = keys[pygame.K_s] or keys[pygame.K_DOWN]
        inputs['left'] = keys[pygame.K_a] or keys[pygame.K_LEFT]
        inputs['right'] = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        inputs['strafe_left'] = keys[pygame.K_a] and keys[pygame.K_LSHIFT]
        inputs['strafe_right'] = keys[pygame.K_d] and keys[pygame.K_LSHIFT]

        return running, inputs

    def cleanup(self):
        """Clean up pygame resources."""
        pygame.quit()


# Test function
if __name__ == "__main__":
    # Quick test of the renderer
    renderer = PygameRaycaster(800, 600)

    # Create test world
    test_tiles = {}
    for x in range(50):
        for y in range(50):
            walkable = not (x == 0 or y == 0 or x == 49 or y == 49)
            test_tiles[(x, y, 0)] = {
                'type': 'CORRIDOR' if walkable else 'VOID',
                'walkable': walkable
            }

    # Add some walls
    for x in range(10, 20):
        test_tiles[(x, 15, 0)] = {'type': 'ANCHOR_STORE', 'walkable': False}

    # Player state
    player_x, player_y = 25.0, 25.0
    player_angle = 0.0
    player_z = 0
    move_speed = 0.1
    turn_speed = 0.05

    running = True
    heat = 0

    while running:
        running, inputs = renderer.handle_events()

        if inputs['quit']:
            running = False

        # Movement
        if inputs['forward']:
            new_x = player_x + math.cos(player_angle) * move_speed
            new_y = player_y + math.sin(player_angle) * move_speed
            if test_tiles.get((int(new_x), int(new_y), 0), {}).get('walkable', False):
                player_x, player_y = new_x, new_y

        if inputs['backward']:
            new_x = player_x - math.cos(player_angle) * move_speed
            new_y = player_y - math.sin(player_angle) * move_speed
            if test_tiles.get((int(new_x), int(new_y), 0), {}).get('walkable', False):
                player_x, player_y = new_x, new_y

        if inputs['left']:
            player_angle -= turn_speed
        if inputs['right']:
            player_angle += turn_speed

        # Test heat increase
        keys = pygame.key.get_pressed()
        if keys[pygame.K_h]:
            heat = min(5, heat + 0.01)

        # Render
        renderer.render(player_x, player_y, player_z, player_angle, test_tiles, heat)

    renderer.cleanup()
