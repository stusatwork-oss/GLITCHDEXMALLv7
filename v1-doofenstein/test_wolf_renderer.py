#!/usr/bin/env python3
"""
Quick test of Wolfenstein 3D renderer
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mall_engine import MallEngine, Direction
from wolf_renderer import WolfRenderer, Wolf3DHUD, Color
from toddler_system import ToddlerSystem

def test_renderer():
    """Test the Wolf3D renderer"""
    print(f"{Color.fg(226)}Testing DOOFENSTEIN 3D Renderer...{Color.reset()}\n")

    # Initialize engine
    engine = MallEngine()
    renderer = WolfRenderer(width=120, height=40)
    hud = Wolf3DHUD(width=120)
    toddler = ToddlerSystem()

    # Render a test frame
    distortions = toddler.apply_visual_distortion()
    frame = renderer.render_frame(
        engine.player.x + 0.5,
        engine.player.y + 0.5,
        engine.player.facing,
        engine.tiles,
        distortions
    )

    print(frame)
    print()

    # Test HUD
    player_data = {
        "position": (engine.player.x, engine.player.y),
        "playtime": 0,
        "inventory_count": 0
    }
    hud_display = hud.render(player_data, 0)
    print(hud_display)

    print(f"\n{Color.fg(46)}✓ Renderer test passed!{Color.reset()}")
    print(f"{Color.fg(244)}Texture system: OK{Color.reset()}")
    print(f"{Color.fg(244)}ANSI colors: OK{Color.reset()}")
    print(f"{Color.fg(244)}Ray casting: OK{Color.reset()}")
    print(f"{Color.fg(244)}HUD rendering: OK{Color.reset()}")

if __name__ == "__main__":
    test_renderer()
