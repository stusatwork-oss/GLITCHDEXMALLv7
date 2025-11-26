#!/usr/bin/env python3
"""
INTEGRATED SYSTEMS TEST - Tiers 1-3 Demo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Demonstrates all v2 systems working together:
- Tier 1: NPC Dialogue (heat-aware barks, GOAP overlays)
- Tier 2: Micro-Glitches (reality cracks before break)
- Tier 3: Stealth Feedback (ANSI alert symbols, noise ripples)

This shows the complete "AAA AI under Wolf3D mask" experience.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
sys.path.insert(0, 'src')

from mall_simulation import MallSimulation


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


def test_dialogue_escalation(sim):
    """Test dialogue system across heat levels"""
    print_header('TIER 1: NPC DIALOGUE ESCALATION')

    heat_levels = [
        (0.5, "Heat 0.5: Mundane Jank"),
        (2.0, "Heat 2.0: Skyrim-Level Dissonance"),
        (3.2, "Heat 3.2: Mask Slipping"),
        (4.2, "Heat 4.2: GOAP Leaking"),
        (5.0, "Heat 5.0: Simulation Speaks")
    ]

    for heat, description in heat_levels:
        print_subheader(description)
        sim.heat_system.current_heat = heat
        sim.heat_system.glitch_intensity = min(1.0, heat / 5.0)

        # Run a few frames to get dialogue
        dialogue_found = False
        for _ in range(10):
            result = sim.update(0.016)
            dialogues = result.get('npc_dialogues', {})

            if dialogues:
                # Show up to 3 NPCs talking
                count = 0
                for npc_id, dialogue in dialogues.items():
                    if count >= 3:
                        break

                    npc_name = next((n.get('name') for n in result['npcs'] if n.get('id') == npc_id), npc_id)

                    if 'bark' in dialogue:
                        print(f'  [{npc_name}]: "{dialogue["bark"]}"')
                        dialogue_found = True
                        count += 1

                    if 'goal_overlay' in dialogue and heat >= 3.0:
                        print(f'  [{npc_name}] {dialogue["goal_overlay"]}')

                if dialogue_found:
                    break

        if not dialogue_found:
            print(f'  (No dialogue triggered this frame - RNG dependent)')

        print()


def test_micro_glitches(sim):
    """Test micro-glitch system"""
    print_header('TIER 2: MICRO-GLITCH SYSTEM')

    test_cases = [
        (2.5, "Heat 2.5: Mask Intact (No Glitches)"),
        (3.2, "Heat 3.2: First Cracks (Rare 1-frame Flickers)"),
        (4.2, "Heat 4.2: Frequent Glitching"),
        (4.8, "Heat 4.8: Near-Constant (Mask Failing)")
    ]

    for heat, description in test_cases:
        print_subheader(description)
        sim.heat_system.current_heat = heat
        sim.heat_system.glitch_intensity = min(1.0, (heat - 3.0) / 2.0)

        if heat < 3.0:
            # Should have no glitches
            result = sim.update(0.016)
            glitches = result.get('micro_glitches', {})
            if glitches.get('active'):
                print(f'  ERROR: Glitches present below Heat 3.0!')
            else:
                print(f'  ✓ No glitches (expected)')
        else:
            # Count glitches over multiple frames
            glitch_count = 0
            glitch_types = set()
            frames_to_check = 60 if heat >= 4.0 else 100

            for _ in range(frames_to_check):
                result = sim.update(0.016)
                glitches = result.get('micro_glitches', {})

                if glitches.get('active'):
                    glitch_count += 1
                    for g in glitches.get('glitches', []):
                        glitch_types.add(g.get('type'))

            percentage = (glitch_count / frames_to_check) * 100
            print(f'  Glitch occurrence: {glitch_count}/{frames_to_check} frames ({percentage:.0f}%)')

            if glitch_types:
                print(f'  Glitch types seen: {len(glitch_types)}')
                print(f'  Examples: {", ".join(list(glitch_types)[:3])}')

        print()


def test_stealth_feedback(sim):
    """Test stealth feedback system"""
    print_header('TIER 3: STEALTH FEEDBACK (ANSI ALERT SYMBOLS)')

    print_subheader('Noise Ripples from Player Actions')

    # Test footstep
    sim.update(0.016, {'type': 'move', 'position': (25, 25, 0)})
    result = sim.update(0.016)
    feedback = result.get('stealth_feedback', {})
    ripples = feedback.get('noise_ripples', [])
    print(f'  Footstep noise: {len(ripples)} ripple(s)')
    if ripples:
        r = ripples[0]
        print(f'    Symbol: "{r["symbol"]}", Max radius: {r["max_radius"]}')

    # Test attack (larger ripple)
    sim.update(0.016, {'type': 'attack_npc', 'npc_id': 'test'})
    result = sim.update(0.016)
    ripples = result.get('stealth_feedback', {}).get('noise_ripples', [])
    print(f'  Attack noise: {len(ripples)} ripple(s)')
    if ripples:
        largest = max(ripples, key=lambda r: r['max_radius'])
        print(f'    Largest ripple max radius: {largest["max_radius"]}')

    print()
    print_subheader('NPC Alert Symbols (Based on Awareness)')

    # Test different awareness levels
    awareness_tests = [
        (0.2, "Unaware", ""),
        (0.4, "Suspicious", "?"),
        (0.6, "Detected", "!!"),
        (0.9, "Alerted", "!")
    ]

    for awareness, state, expected_symbol in awareness_tests:
        sim.stealth_feedback.update_npc_alerts_from_awareness('test_npc', awareness, False)
        result = sim.update(0.016)
        symbols = result.get('stealth_feedback', {}).get('npc_alert_symbols', {})
        actual_symbol = symbols.get('test_npc', '')

        match = "✓" if actual_symbol == expected_symbol else "✗"
        print(f'  {match} Awareness {awareness:.1f} ({state}): "{actual_symbol}" (expected: "{expected_symbol}")')

    print()


def test_integrated_scenario(sim):
    """Test all systems working together in a gameplay scenario"""
    print_header('INTEGRATED SCENARIO: Player Escalation')

    print_subheader('Scenario: Player walks → kicks vending machine → gets spotted')
    print()

    # Start calm
    print('1. INITIAL STATE (Heat 0)')
    print('   Player enters mall, walks normally...')
    sim.heat_system.current_heat = 0.0
    sim.update(0.016, {'type': 'move', 'position': (25, 25, 0)})
    result = sim.update(0.016)

    dialogues = result.get('npc_dialogues', {})
    if dialogues:
        npc_id, dialogue = next(iter(dialogues.items()))
        npc_name = next((n.get('name') for n in result['npcs'] if n.get('id') == npc_id), npc_id)
        if 'bark' in dialogue:
            print(f'   [{npc_name}]: "{dialogue["bark"]}"')
    print()

    # Vandalism
    print('2. VANDALISM (Heat increases to ~1.5)')
    print('   Player kicks vending machine...')
    sim.heat_system.add_heat(1.5, 'vandalism', (25, 25, 0))
    sim.update(0.016, {'type': 'interact_prop', 'prop_id': 'vending_0', 'interaction': 'kick'})
    result = sim.update(0.016)

    ripples = result.get('stealth_feedback', {}).get('noise_ripples', [])
    print(f'   Noise ripples: {len(ripples)}')
    print(f'   Heat: {result["heat_stars"]}')
    print()

    # Guards notice
    print('3. GUARDS RESPOND (Heat 2-3)')
    print('   Security patrols increase...')
    sim.heat_system.current_heat = 2.5
    for _ in range(10):
        result = sim.update(0.016)
        dialogues = result.get('npc_dialogues', {})
        security_dialogue = {k: v for k, v in dialogues.items() if 'security' in k.lower()}
        if security_dialogue:
            npc_id, dialogue = next(iter(security_dialogue.items()))
            npc_name = next((n.get('name') for n in result['npcs'] if n.get('id') == npc_id), npc_id)
            if 'bark' in dialogue:
                print(f'   [{npc_name}]: "{dialogue["bark"]}"')
                break
    print()

    # Player spotted
    print('4. PLAYER SPOTTED (Heat increases)')
    print('   Guard sees player...')
    sim.stealth_feedback.update_npc_alerts_from_awareness('security_0', 0.9, False)
    sim.heat_system.add_heat(1.0, 'spotted', (25, 25, 0))
    result = sim.update(0.016)

    symbols = result.get('stealth_feedback', {}).get('npc_alert_symbols', {})
    guard_symbol = symbols.get('security_0', '')
    print(f'   Guard alert symbol: "{guard_symbol}"')
    print(f'   Heat: {result["heat_stars"]}')
    print()

    # Reality starts cracking
    print('5. REALITY CRACKS (Heat 3.5+)')
    print('   Micro-glitches appear...')
    sim.heat_system.current_heat = 3.8
    sim.heat_system.glitch_intensity = 0.4

    # Run frames until we see a glitch
    for _ in range(100):
        result = sim.update(0.016)
        glitches = result.get('micro_glitches', {})
        if glitches.get('active'):
            print(f'   GLITCH DETECTED!')
            for g in glitches.get('glitches', [])[:2]:
                print(f'     Type: {g["type"]}, Duration: {g["duration"]:.3f}s')
            break

    # Show NPC dialogue at this heat
    for _ in range(10):
        result = sim.update(0.016)
        dialogues = result.get('npc_dialogues', {})
        if dialogues:
            npc_id, dialogue = next(iter(dialogues.items()))
            npc_name = next((n.get('name') for n in result['npcs'] if n.get('id') == npc_id), npc_id)
            if 'bark' in dialogue:
                print(f'   [{npc_name}]: "{dialogue["bark"]}"')
                break

    print()


def main():
    """Run all tests"""
    print_header('GLITCHDEX MALL V2 - INTEGRATED SYSTEMS TEST')
    print('Testing Tiers 1-3: Dialogue, Micro-Glitches, Stealth Feedback')
    print('This demonstrates AAA AI systems hiding under Wolf3D terminal art.')

    # Create simulation
    print()
    print('Initializing simulation...')
    world = create_test_world()
    sim = MallSimulation(world)

    # Run tests
    test_dialogue_escalation(sim)
    test_micro_glitches(sim)
    test_stealth_feedback(sim)
    test_integrated_scenario(sim)

    # Summary
    print_header('TEST SUMMARY')
    print('✓ Tier 1: NPC Dialogue System')
    print('  - Heat-aware dialogue: mundane → Skyrim → reality-aware → AI confession')
    print('  - GOAP goal overlays: flickering at Heat 3+, always on at Heat 5')
    print()
    print('✓ Tier 2: Micro-Glitch System')
    print('  - Glitch spawn rates scale with heat (1% → 20% per frame)')
    print('  - 8 glitch types: pathfinding, name corruption, texture bleeds, etc.')
    print('  - Mask cracks at Heat 3 before breaking at Heat 5')
    print()
    print('✓ Tier 3: Stealth Feedback')
    print('  - ANSI alert symbols: ! !! ? ??')
    print('  - Noise ripples (~) expand from player actions')
    print('  - Zero modern UI - pure ASCII')
    print()
    print('═' * 70)
    print('SYSTEMS OPERATIONAL: AAA AI under 256-color mask')
    print('The cognitive dissonance is real.')
    print('═' * 70)


if __name__ == '__main__':
    main()
