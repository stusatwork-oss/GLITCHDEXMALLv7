"""
DOOFENSTEIN 3D SPRITE SYSTEM
Billboard sprites for items, NPCs, and effects
Authentic Wolf3D-style sprite rendering
"""

import math
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Sprite:
    """A billboard sprite in 3D space"""
    x: float
    y: float
    z: float
    sprite_type: str
    char: str
    color: int
    size: float = 1.0  # Relative size multiplier


class SpriteRenderer:
    """Renders billboard sprites in 3D space"""

    # Sprite definitions (char, color, size)
    SPRITE_DEFS = {
        # Artifacts
        "sunglasses": ("@", 226, 0.8),
        "sticker_sheets": ("*", 208, 0.6),
        "arcade_token": ("o", 220, 0.5),
        "keychain": ("k", 246, 0.6),
        "graffiti_marker": ("|", 196, 0.7),
        "leather_wallet": ("W", 94, 0.7),
        "gift_card": ("=", 51, 0.6),
        "film_roll": ("O", 240, 0.7),
        "escalator_grease": ("~", 58, 0.6),
        "necronomicon_bookmark": ("†", 88, 0.8),
        "food_tray": ("□", 244, 1.0),
        "phone_charm": ("¤", 207, 0.5),
        "utility_keychain": ("k", 250, 0.6),
        "old_receipt": ("¦", 252, 0.5),

        # NPCs
        "milo": ("M", 33, 1.5),
        "bored": ("B", 208, 1.5),
        "r0mba": ("R", 240, 1.0),
        "mall_cop": ("C", 196, 1.5),
        "generic_shopper_1": ("S", 246, 1.5),
        "generic_shopper_2": ("S", 244, 1.5),

        # Effects
        "shadow_presence": ("?", 235, 2.0),
        "glitch_artifact": ("#", 226, 1.0),
    }

    def __init__(self):
        self.sprites: List[Sprite] = []

    def add_sprite(self, x: float, y: float, z: float, sprite_type: str):
        """Add a sprite to render list"""
        if sprite_type in self.SPRITE_DEFS:
            char, color, size = self.SPRITE_DEFS[sprite_type]
            self.sprites.append(Sprite(x, y, z, sprite_type, char, color, size))

    def clear_sprites(self):
        """Clear all sprites"""
        self.sprites = []

    def get_sprites_to_render(self, player_x: float, player_y: float,
                             facing_angle: float, fov: float,
                             max_distance: float = 20) -> List[Tuple[float, float, Sprite]]:
        """
        Get list of sprites to render with their screen positions.
        Returns list of (screen_x, distance, sprite).
        """
        sprites_to_render = []

        for sprite in self.sprites:
            # Calculate relative position
            dx = sprite.x - player_x
            dy = sprite.y - player_y
            distance = math.sqrt(dx**2 + dy**2)

            if distance > max_distance or distance < 0.1:
                continue

            # Calculate angle to sprite
            angle_to_sprite = math.degrees(math.atan2(dy, dx))

            # Normalize angles
            angle_diff = angle_to_sprite - facing_angle
            while angle_diff > 180:
                angle_diff -= 360
            while angle_diff < -180:
                angle_diff += 360

            # Check if sprite is in FOV
            if abs(angle_diff) > fov / 2 + 10:  # Small margin
                continue

            # Calculate screen X position (-1 to 1, then scaled to screen width)
            screen_x_normalized = angle_diff / (fov / 2)

            sprites_to_render.append((screen_x_normalized, distance, sprite))

        # Sort by distance (far to near) for proper occlusion
        sprites_to_render.sort(key=lambda s: s[1], reverse=True)

        return sprites_to_render

    def render_sprite_to_buffer(self, screen_buffer: List[List[Tuple[str, int]]],
                               sprite: Sprite, screen_x: int, distance: float,
                               screen_width: int, screen_height: int,
                               z_buffer: List[float]):
        """
        Render a sprite to the screen buffer.
        Uses z_buffer for depth testing.
        """
        # Calculate sprite size on screen
        base_height = int((screen_height * 0.6 * sprite.size) / (distance + 0.1))
        base_height = max(1, min(screen_height, base_height))

        base_width = max(1, int(base_height * 0.5))  # Sprites are narrower

        # Calculate sprite bounds
        sprite_top = (screen_height - base_height) // 2
        sprite_bottom = sprite_top + base_height
        sprite_left = screen_x - base_width // 2
        sprite_right = sprite_left + base_width

        # Render sprite
        for y in range(sprite_top, sprite_bottom):
            if y < 0 or y >= screen_height:
                continue

            for x in range(sprite_left, sprite_right):
                if x < 0 or x >= screen_width:
                    continue

                # Z-buffer test
                if z_buffer[x] < distance:
                    continue  # Wall is closer, don't draw sprite pixel

                # Determine sprite character based on position
                # Center is the main char, edges are shaded
                rel_x = (x - sprite_left) / max(1, base_width)
                rel_y = (y - sprite_top) / max(1, base_height)

                # Simple circular sprite shape
                center_dist = math.sqrt((rel_x - 0.5)**2 + (rel_y - 0.5)**2)

                if center_dist < 0.3:
                    # Center - main character
                    screen_buffer[y][x] = (sprite.char, sprite.color)
                elif center_dist < 0.5:
                    # Edge - dimmed
                    screen_buffer[y][x] = ("·", sprite.color - 10)
                # Else: transparent (don't draw)


def create_sprite_list_from_game_state(engine: Any, npc_system: Any,
                                       artifact_system: Any) -> SpriteRenderer:
    """
    Create sprite renderer with current game state.
    """
    renderer = SpriteRenderer()

    # Add artifact sprites
    for artifact_id, (x, y, z) in engine.artifact_locations.items():
        # Add slight offset so sprites don't z-fight with walls
        renderer.add_sprite(float(x) + 0.5, float(y) + 0.5, float(z), artifact_id)

    # Add NPC sprites
    for npc_id, npc in npc_system.npcs.items():
        renderer.add_sprite(
            float(npc.current_x) + 0.5,
            float(npc.current_y) + 0.5,
            float(npc.current_z),
            npc_id
        )

    return renderer
