#!/usr/bin/env python3
"""
Test Reality Glitch System
The mask slips. The simulation reveals its true nature.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from reality_glitch import RealityGlitch
from wolf_renderer import Color

def test_reality_glitch():
    """Test the reality glitch system"""
    print(f"{Color.fg(46)}Testing REALITY GLITCH SYSTEM...{Color.reset()}\n")

    glitch = RealityGlitch()

    # Test Stage 0 (rare glitches)
    print(f"{Color.fg(255)}Stage 0 - Mostly stable facade:{Color.reset()}")
    for _ in range(10):
        messages = glitch.update(0, 0.1, 0)
        if messages:
            print(f"  {Color.fg(226)}{messages[0]}{Color.reset()}")

    # Test Stage 1 (moderate glitches)
    print(f"\n{Color.fg(208)}Stage 1 - Facade beginning to crack:{Color.reset()}")
    for _ in range(20):
        messages = glitch.update(1, 0.5, 2)
        if messages:
            print(f"  {Color.fg(208)}{messages[0]}{Color.reset()}")

    # Test Stage 2 (reality breaks)
    print(f"\n{Color.fg(196)}Stage 2 - SIMULATION BREAKING:{Color.reset()}")
    for _ in range(30):
        messages = glitch.update(2, 0.9, 4)
        if messages:
            print(f"  {Color.fg(196)}{messages[0]}{Color.reset()}")

    # Test active effects
    print(f"\n{Color.fg(46)}Active Glitch Effects:{Color.reset()}")
    effects = glitch.get_active_effects()
    for effect, intensity in effects.items():
        print(f"  {effect}: {intensity:.2f}")

    # Test post-processing
    print(f"\n{Color.fg(46)}Post-Processing Effects:{Color.reset()}")
    post_fx = glitch.get_post_processing_effects()
    for fx, value in post_fx.items():
        if value > 0:
            print(f"  {fx}: {value:.2f}")

    # Test photorealistic leak
    photorealistic = glitch.get_photorealistic_intensity()
    print(f"\n{Color.fg(46)}Photorealistic Leak: {photorealistic:.2f}{Color.reset()}")

    # Test lighting complexity
    lighting = glitch.get_lighting_complexity()
    print(f"{Color.fg(46)}Lighting Complexity: {lighting:.2f} (0=Wolf3D, 1=Ray Traced){Color.reset()}")

    # Test detail multiplier
    detail = glitch.get_detail_multiplier()
    print(f"{Color.fg(46)}Detail Multiplier: {detail:.2f}x{Color.reset()}")

    # Test reality breaking
    breaking = glitch.is_reality_breaking()
    print(f"{Color.fg(46)}Reality Breaking: {breaking}{Color.reset()}")

    # Test debug text
    if glitch.should_show_debug_info():
        print(f"\n{Color.fg(46)}DEBUG INFO LEAK:{Color.reset()}")
        debug_text = glitch.generate_debug_text()
        for line in debug_text:
            print(f"  {Color.fg(46)}{line}{Color.reset()}")

    # Test wireframe
    if glitch.should_show_wireframe():
        print(f"\n{Color.fg(46)}[WIREFRAME] Geometry mesh visible{Color.reset()}")

    print(f"\n{Color.fg(46)}✓ Reality glitch system operational!{Color.reset()}")
    print(f"{Color.fg(244)}The facade is sophisticated. The cracks are intentional.{Color.reset()}")
    print(f"{Color.fg(240)}This is not a bug. This is the toddler revealing what's real.{Color.reset()}")

if __name__ == "__main__":
    test_reality_glitch()
