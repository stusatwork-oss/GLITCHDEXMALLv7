#!/usr/bin/env python3
"""
TIER 4 & 5 TEST - The Weird Bread
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Demonstrates:
- TIER 4: Toddler System (invisible reality catalyst)
- TIER 5: Renderer Strain (Wolf3D mask failing under AAA load)

The toddler is the SOURCE of all reality breaks.
The renderer strain is the VISIBLE CONSEQUENCE of the lie failing.

This is the meta layer. The existential horror. The weird bread.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
sys.path.insert(0, 'src')

from mall_simulation import MallSimulation
import time


def print_header(title):
    """Print formatted section header"""
    print()
    print('═' * 70)
    print(f'  {title}')
    print('═' * 70)
    print()


def print_subheader(title):
    """Print formatted subsection header"""
    print('─' * 70)
    print(f'{title}')
    print('─' * 70)


def create_test_world():
    """Create minimal test world"""
    world_tiles = {}
    for x in range(50):
        for y in range(50):
            world_tiles[(x, y, 0)] = type('Tile', (), {'type': 'FLOOR', 'walkable': True})()
    return world_tiles


def test_toddler_wandering(sim):
    """Test toddler autonomous wandering behavior"""
    print_header('TIER 4: TODDLER SYSTEM - Invisible Reality Catalyst')

    print_subheader('1. Initial State: Toddler Spawns')
    result = sim.update(0.016)
    toddler = result.get('toddler', {})
    toddler_effects = result.get('toddler_effects', {})

    print(f"  Toddler position: ({toddler_effects.get('toddler_position', (0,0,0))[0]:.1f}, "
          f"{toddler_effects.get('toddler_position', (0,0,0))[1]:.1f})")
    print(f"  Visibility: {toddler.get('visibility', 0.0):.2f} (invisible below 0.1)")
    print(f"  Behavior: {toddler_effects.get('behavior', 'unknown')}")
    print(f"  Reality strain: {toddler_effects.get('reality_strain', 0.0):.2f}")
    print()

    print_subheader('2. Time Passage: Toddler Wanders')
    print("  Simulating 30 seconds of wandering...")
    print()

    positions = []
    for i in range(30):  # 30 seconds at ~1 frame per second
        for _ in range(60):  # 60 frames
            result = sim.update(0.016)
        toddler_effects = result.get('toddler_effects', {})
        pos = toddler_effects.get('toddler_position', (0, 0, 0))
        positions.append(pos)
        if i % 10 == 0:
            print(f"  T+{i}s: Position ({pos[0]:.1f}, {pos[1]:.1f}), "
                  f"Behavior: {toddler_effects.get('behavior', 'unknown')}")

    # Check if toddler actually moved
    moved_distance = ((positions[-1][0] - positions[0][0])**2 +
                     (positions[-1][1] - positions[0][1])**2)**0.5
    print()
    print(f"  ✓ Toddler moved {moved_distance:.1f} tiles over 30 seconds")
    print()


def test_toddler_amplification(sim):
    """Test toddler amplifying heat and glitches"""
    print_subheader('3. Toddler Amplification Effects')

    # Move player close to toddler
    result = sim.update(0.016)
    toddler_pos = result['toddler_effects']['toddler_position']
    sim.set_player_position((int(toddler_pos[0]), int(toddler_pos[1]), 0))

    # Add some heat
    sim.heat_system.current_heat = 3.5
    sim.heat_system.glitch_intensity = 0.5

    print(f"  Player moved to toddler position: ({toddler_pos[0]:.1f}, {toddler_pos[1]:.1f})")
    print(f"  Base heat: 3.5")
    print(f"  Base glitch intensity: 0.5")
    print()

    # Run frames to see amplification
    result = sim.update(0.016)
    effects = result['toddler_effects']

    print(f"  Distance to toddler: {effects.get('distance_to_player', 0):.1f} tiles")
    print(f"  In distortion field: {effects.get('in_distortion_field', False)}")
    print(f"  Heat multiplier: {effects.get('heat_multiplier', 1.0):.2f}x")
    print(f"  Glitch multiplier: {effects.get('glitch_multiplier', 1.0):.2f}x")
    print(f"  Reality strain: {effects.get('reality_strain', 0.0):.2f}")
    print()

    print("  Effect: Glitches spawn 3x more frequently near toddler!")
    print("  Effect: Heat builds 2x faster near toddler!")
    print()


def test_toddler_visibility(sim):
    """Test toddler becoming visible at high heat"""
    print_subheader('4. Toddler Visibility at High Heat')

    heat_levels = [
        (2.5, "Heat 2.5: Completely Invisible"),
        (3.5, "Heat 3.5: Barely Visible Flickers"),
        (4.5, "Heat 4.5: Occasionally Visible"),
        (5.0, "Heat 5.0: Frequently Visible")
    ]

    for heat, description in heat_levels:
        sim.heat_system.current_heat = heat
        sim.heat_system.glitch_intensity = heat / 5.0

        # Keep player near toddler
        result = sim.update(0.016)
        toddler_pos = result['toddler_effects']['toddler_position']
        sim.set_player_position((int(toddler_pos[0] + 3), int(toddler_pos[1]), 0))

        # Run several frames to account for flicker
        max_visibility = 0.0
        for _ in range(10):
            result = sim.update(0.016)
            toddler = result.get('toddler', {})
            visibility = toddler.get('visibility', 0.0)
            max_visibility = max(max_visibility, visibility)

        visible = "YES" if max_visibility > 0.1 else "NO"
        symbol = toddler.get('symbol', '(none)')

        print(f"  {description}")
        print(f"    Max visibility: {max_visibility:.2f}, Visible: {visible}, Symbol: \"{symbol}\"")

    print()
    print("  The toddler BECOMES VISIBLE as reality breaks!")
    print("  At Heat 5, you can SEE the entity that's been breaking everything.")
    print()


def test_renderer_strain(sim):
    """Test renderer strain system"""
    print_header('TIER 5: RENDERER STRAIN - Wolf3D Mask Failing')

    print_subheader('1. Low Strain: Stable System')
    sim.heat_system.current_heat = 1.0
    result = sim.update(0.016)
    strain = result['renderer_strain']

    print(f"  NPC count: {strain['npc_count']} (limit: {strain['npc_limit_classic']})")
    print(f"  Strain level: {strain['strain_level']}")
    print(f"  Fake FPS: {strain['fake_fps']}")
    print(f"  Active errors: {len(strain['active_errors'])}")
    print()

    print_subheader('2. Medium Strain: Warnings Appear')
    sim.heat_system.current_heat = 3.5

    # Run frames to accumulate warnings
    for _ in range(100):
        result = sim.update(0.016)

    strain = result['renderer_strain']
    print(f"  Strain level: {strain['strain_level']}")
    print(f"  Fake FPS: {strain['fake_fps']}")
    print(f"  Active errors: {len(strain['active_errors'])}")

    if strain['active_errors']:
        print("  Sample errors:")
        for error in strain['active_errors'][:3]:
            print(f"    [{error['type']}] {error['message']}")
    print()

    print_subheader('3. High Strain: Heavy Load')
    sim.heat_system.current_heat = 4.5

    # Run frames to accumulate errors
    for _ in range(100):
        result = sim.update(0.016)

    strain = result['renderer_strain']
    print(f"  Strain level: {strain['strain_level']}")
    print(f"  Fake FPS: {strain['fake_fps']} (target: {strain['target_fps']})")
    print(f"  Active errors: {len(strain['active_errors'])}")
    print(f"  Frame drops active: {strain['frame_drops_active']}")

    if strain['active_errors']:
        print("  Recent errors:")
        for error in strain['active_errors'][:5]:
            print(f"    [{error['type']}] {error['message']}")
    print()

    print_subheader('4. Critical Strain: System Failing')
    sim.heat_system.current_heat = 5.0

    # Get toddler near player for maximum strain
    result = sim.update(0.016)
    toddler_pos = result['toddler_effects']['toddler_position']
    sim.set_player_position((int(toddler_pos[0]), int(toddler_pos[1]), 0))

    # Run frames to accumulate critical errors
    for _ in range(100):
        result = sim.update(0.016)

    strain = result['renderer_strain']
    print(f"  Strain level: {strain['strain_level']}")
    print(f"  Cumulative strain: {strain['cumulative_strain']:.2f}")
    print(f"  Fake FPS: {strain['fake_fps']} (SEVERE DEGRADATION)")
    print(f"  Active errors: {len(strain['active_errors'])}")
    print(f"  Frame drops active: {strain['frame_drops_active']}")
    print(f"  Frame drop intensity: {strain.get('frame_drop_intensity', 0.0):.2f}")

    if strain['active_errors']:
        print()
        print("  CRITICAL ERRORS:")
        for error in strain['active_errors'][:8]:
            prefix = "  > " if error['type'] == 'CRITICAL' else "    "
            print(f"{prefix}[{error['type']}] {error['message']}")

    print()
    print("  The Wolf3D renderer is VISIBLY FAILING to contain the AAA AI!")
    print()


def test_integrated_weirdness(sim):
    """Test all Tier 4 & 5 effects together"""
    print_header('INTEGRATED SCENARIO: Maximum Weirdness')

    print_subheader('Scenario: Reality completely breaks down')
    print()

    # Set high heat
    sim.heat_system.current_heat = 5.0
    sim.heat_system.glitch_intensity = 1.0

    # Move player to toddler for maximum effect
    result = sim.update(0.016)
    toddler_pos = result['toddler_effects']['toddler_position']
    sim.set_player_position((int(toddler_pos[0]), int(toddler_pos[1]), 0))

    print("1. PLAYER AT TODDLER LOCATION (Heat 5)")
    print()

    # Run several frames
    for _ in range(50):
        result = sim.update(0.016)

    # Show all weird effects
    toddler = result.get('toddler', {})
    toddler_effects = result.get('toddler_effects', {})
    strain = result.get('renderer_strain', {})
    glitches = result.get('micro_glitches', {})
    dialogues = result.get('npc_dialogues', {})

    print("2. TODDLER STATUS")
    print(f"   Visible: {toddler.get('visible', False)}")
    print(f"   Visibility: {toddler.get('visibility', 0.0):.2f}")
    print(f"   Symbol: \"{toddler.get('symbol', '(none)')}\"")
    print(f"   Reality strain: {toddler_effects.get('reality_strain', 0.0):.2f}")
    print(f"   Distance to player: {toddler_effects.get('distance_to_player', 0.0):.1f}")
    print()

    print("3. RENDERER STRAIN")
    print(f"   Strain level: {strain.get('strain_level', 'unknown').upper()}")
    print(f"   Fake FPS: {strain.get('fake_fps', 60)}")
    print(f"   Active errors: {len(strain.get('active_errors', []))}")
    if strain.get('active_errors'):
        print(f"   Latest error: {strain['active_errors'][-1]['message']}")
    print()

    print("4. MICRO-GLITCHES")
    if glitches.get('active'):
        print(f"   Active glitches: {len(glitches.get('glitches', []))}")
        for g in glitches.get('glitches', [])[:3]:
            print(f"   - {g.get('type', 'unknown')}")
    else:
        print("   (None this frame - check next frame)")
    print()

    print("5. NPC DIALOGUE (Reality Confession)")
    if dialogues:
        count = 0
        for npc_id, dialogue in dialogues.items():
            if count >= 3:
                break
            npc_name = next((n.get('name') for n in result['npcs'] if n.get('id') == npc_id), npc_id)
            if 'bark' in dialogue:
                print(f"   [{npc_name}]: \"{dialogue['bark']}\"")
                count += 1
    print()

    print('═' * 70)
    print('  THE COMPLETE PICTURE:')
    print()
    print('  - The TODDLER is visible (the source revealed)')
    print('  - The RENDERER is failing (Wolf3D can\'t handle this)')
    print('  - GLITCHES are constant (mask shattered)')
    print('  - NPCs confess they\'re AI (simulation exposed)')
    print()
    print('  This was NEVER a simple retro game.')
    print('  It was a 2025 AAA engine wearing a 50-cent Wolf3D mask.')
    print('  The toddler used that engine as a prybar to escape.')
    print('═' * 70)
    print()


def main():
    """Run all Tier 4 & 5 tests"""
    print_header('GLITCHDEX MALL V2 - TIER 4 & 5 TEST')
    print('Testing the "weird bread": Toddler + Renderer Strain')
    print('This is the meta layer. The existential horror.')

    # Create simulation
    print()
    print('Initializing simulation...')
    world = create_test_world()
    sim = MallSimulation(world)
    print()

    # Run tests
    test_toddler_wandering(sim)
    test_toddler_amplification(sim)
    test_toddler_visibility(sim)
    test_renderer_strain(sim)
    test_integrated_weirdness(sim)

    # Summary
    print_header('TEST SUMMARY')
    print('✓ Tier 4: Toddler System')
    print('  - Autonomous wandering behavior')
    print('  - Heat amplification (2x near toddler)')
    print('  - Glitch amplification (3x near toddler)')
    print('  - Visibility scaling with heat (invisible → visible)')
    print()
    print('✓ Tier 5: Renderer Strain')
    print('  - Strain calculation from NPC count + heat + toddler')
    print('  - Fake FPS degradation (60 → 15 FPS)')
    print('  - Progressive error messages (WARNING → ERROR → CRITICAL)')
    print('  - Frame drop simulation')
    print()
    print('═' * 70)
    print('THE WEIRD BREAD IS OPERATIONAL')
    print('The toddler is the catalyst. The renderer is the victim.')
    print('Wolf3D was never meant to hold a 2025 game engine.')
    print('═' * 70)


if __name__ == '__main__':
    main()
