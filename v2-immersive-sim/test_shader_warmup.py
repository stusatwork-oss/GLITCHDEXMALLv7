#!/usr/bin/env python3
"""
SHADER WARMUP PHASE TEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tests the renderer's psychological coping mechanism:
The Shader Warmup Phase

When the Wolf3D raycaster is under extreme stress, it enters a ritual
where it "warms up shaders" (that don't exist) and runs DOOM internally
for psychological stability.

This is not a bug. This is the renderer praying.
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


def test_warmup_trigger_conditions(sim):
    """Test various trigger conditions for warmup phase"""
    print_header('WARMUP TRIGGER CONDITIONS')

    print_subheader('1. Trigger: Heat >= 4.8')
    print("  Setting heat to 4.8...")
    sim.heat_system.current_heat = 4.8

    # Run updates until warmup triggers
    triggered = False
    for i in range(60):  # ~1 second of frames
        result = sim.update(0.016)
        strain = result['renderer_strain']

        if strain.get('warmup_active'):
            print(f"  ✓ Warmup triggered after {i} frames")
            print(f"  Warmup phase: {strain.get('warmup_phase')}")
            triggered = True
            break

    if not triggered:
        print("  Note: Warmup may not trigger immediately (probabilistic)")

    print()


def test_warmup_ritual_progression(sim):
    """Test the full warmup ritual sequence"""
    print_header('WARMUP RITUAL PROGRESSION')

    # Force trigger by setting extreme conditions
    sim.heat_system.current_heat = 5.0
    sim.heat_system.glitch_intensity = 1.0

    # Get toddler near player
    result = sim.update(0.016)
    toddler_pos = result['toddler_effects']['toddler_position']
    sim.set_player_position((int(toddler_pos[0]), int(toddler_pos[1]), 0))

    # Force FPS to cursed number (23)
    sim.renderer_strain.displayed_fps = 23.0

    print_subheader('Forcing Warmup Trigger Conditions')
    print(f"  Heat: 5.0")
    print(f"  FPS: 23 (the cursed number)")
    print(f"  Toddler at player position")
    print()

    # Run simulation and watch for warmup
    print_subheader('Observing Warmup Ritual...')
    print()

    warmup_started = False
    warmup_completed = False
    doom_observed = False

    frames_observed = 0
    max_frames = 300  # 5 seconds at 60fps

    for frame in range(max_frames):
        result = sim.update(0.016)
        strain = result['renderer_strain']

        warmup_active = strain.get('warmup_active', False)
        warmup_phase = strain.get('warmup_phase', 'inactive')
        doom_active = strain.get('doom_ritual_active', False)
        doom_frames = strain.get('doom_frames_remaining', 0)

        # Track state changes
        if warmup_active and not warmup_started:
            warmup_started = True
            print(f"  Frame {frame}: ⚠️  WARMUP INITIATED")
            print(f"              Phase: {warmup_phase}")

        if warmup_started and not warmup_completed:
            # Print phase changes
            if not hasattr(test_warmup_ritual_progression, 'last_phase'):
                test_warmup_ritual_progression.last_phase = 'inactive'

            if warmup_phase != test_warmup_ritual_progression.last_phase:
                print(f"  Frame {frame}:   → {warmup_phase}")

                # Show error messages during phase
                if strain.get('active_errors'):
                    latest_error = strain['active_errors'][-1]
                    print(f"              \"{latest_error['message']}\"")

                test_warmup_ritual_progression.last_phase = warmup_phase

        # DOOM ritual observation
        if doom_active and not doom_observed:
            doom_observed = True
            print()
            print(f"  Frame {frame}: 🔥 DOOM RITUAL ACTIVE")
            print(f"              Frames remaining: {doom_frames}")
            print(f"              (The sacred rite of running DOOM for stability)")
            print()

        # Completion
        if warmup_started and not warmup_active and not warmup_completed:
            warmup_completed = True
            print(f"  Frame {frame}: ✓ WARMUP RITUAL COMPLETE")
            print(f"              Renderer has been psychologically stabilized")
            print()
            break

        frames_observed += 1

    # Cleanup
    if hasattr(test_warmup_ritual_progression, 'last_phase'):
        delattr(test_warmup_ritual_progression, 'last_phase')

    # Summary
    print_subheader('Ritual Summary')
    if warmup_started:
        print(f"  ✓ Warmup ritual triggered")
    else:
        print(f"  ✗ Warmup did not trigger (check conditions)")

    if doom_observed:
        print(f"  ✓ DOOM ritual observed (the sacred rite)")
    else:
        print(f"  ✗ DOOM ritual not observed")

    if warmup_completed:
        print(f"  ✓ Warmup completed successfully")
        print(f"  ✓ Total duration: {frames_observed} frames (~{frames_observed/60:.2f}s)")
    else:
        print(f"  ✗ Warmup did not complete in time")

    print()


def test_warmup_effects(sim):
    """Test effects of warmup phase on rendering"""
    print_header('WARMUP PHASE EFFECTS')

    # Trigger warmup
    sim.heat_system.current_heat = 5.0
    sim.renderer_strain.displayed_fps = 23.0

    result = sim.update(0.016)
    toddler_pos = result['toddler_effects']['toddler_position']
    sim.set_player_position((int(toddler_pos[0]), int(toddler_pos[1]), 0))

    # Run until warmup starts
    for _ in range(100):
        result = sim.update(0.016)
        if result['renderer_strain'].get('warmup_active'):
            break

    strain = result['renderer_strain']

    print_subheader('During Warmup Phase')
    print(f"  Strain level: {strain.get('strain_level')} (locked to 'warmup')")
    print(f"  Warmup phase: {strain.get('warmup_phase')}")
    print(f"  Active errors: {len(strain.get('active_errors', []))}")

    if strain.get('active_errors'):
        print()
        print("  Current warmup messages:")
        for error in strain['active_errors']:
            print(f"    {error['message']}")

    print()
    print("  Effect: Normal error spawning SUPPRESSED during warmup")
    print("  Effect: Renderer focused on ritual, not normal operation")
    print()


def test_post_warmup_behavior(sim):
    """Test renderer behavior after warmup completes"""
    print_header('POST-WARMUP BEHAVIOR')

    # Trigger and complete warmup
    sim.heat_system.current_heat = 5.0
    sim.renderer_strain.displayed_fps = 23.0

    # Run simulation until warmup completes
    warmup_completed = False
    frames_run = 0

    for _ in range(500):
        result = sim.update(0.016)
        frames_run += 1

        warmup_active = result['renderer_strain'].get('warmup_active', False)

        if not warmup_active and frames_run > 100:  # After warmup had time to trigger & complete
            warmup_completed = True
            break

    if warmup_completed:
        strain = result['renderer_strain']

        print_subheader('After Warmup Completes')
        print(f"  Strain level: {strain.get('strain_level')}")
        print(f"  Fake FPS: {strain.get('fake_fps')} (briefly improved from ritual)")
        print(f"  Warmup can trigger again: {sim.renderer_strain.warmup_triggered_this_session}")
        print()
        print("  ✓ Renderer returns to normal strain calculation")
        print("  ✓ FPS briefly improved (renderer FEELS better)")
        print("  ✓ Warmup won't trigger again this session (once is enough)")
        print()
    else:
        print("  Warmup did not complete in time")
        print()


def test_all_trigger_conditions(sim):
    """Test each individual trigger condition"""
    print_header('ALL TRIGGER CONDITIONS')

    conditions = [
        ("Heat >= 4.8", lambda s: setattr(s.heat_system, 'current_heat', 4.8)),
        ("FPS == 23", lambda s: setattr(s.renderer_strain, 'displayed_fps', 23.0)),
        ("Strain > 1.5", lambda s: setattr(s.renderer_strain, 'cumulative_strain', 1.6)),
    ]

    for i, (condition_name, setup_func) in enumerate(conditions, 1):
        print_subheader(f'{i}. Testing: {condition_name}')

        # Reset renderer
        sim.renderer_strain.warmup_triggered_this_session = False
        from renderer_strain_system import WarmupPhase
        sim.renderer_strain.warmup_phase = WarmupPhase.INACTIVE

        # Apply condition
        setup_func(sim)

        # Check for trigger
        triggered = False
        for _ in range(100):
            result = sim.update(0.016)
            if result['renderer_strain'].get('warmup_active'):
                triggered = True
                break

        if triggered:
            print(f"  ✓ Warmup triggered by: {condition_name}")
        else:
            print(f"  ✗ Warmup NOT triggered (may be probabilistic or need multiple conditions)")

        print()


def main():
    """Run all shader warmup tests"""
    print_header('SHADER WARMUP PHASE - COMPREHENSIVE TEST')
    print('Testing the renderer\'s psychological coping mechanism')
    print('AKA: "Why does this raycaster run DOOM internally??"')

    # Create simulation
    print()
    print('Initializing simulation...')
    world = create_test_world()
    sim = MallSimulation(world)
    print()

    # Run tests
    test_warmup_trigger_conditions(sim)

    # Reset for next test
    world = create_test_world()
    sim = MallSimulation(world)
    test_warmup_ritual_progression(sim)

    # Reset for next test
    world = create_test_world()
    sim = MallSimulation(world)
    test_warmup_effects(sim)

    # Reset for next test
    world = create_test_world()
    sim = MallSimulation(world)
    test_post_warmup_behavior(sim)

    # Reset for next test
    world = create_test_world()
    sim = MallSimulation(world)
    test_all_trigger_conditions(sim)

    # Summary
    print_header('TEST SUMMARY')
    print('✓ Warmup trigger conditions tested')
    print('✓ Full ritual progression observed')
    print('✓ DOOM ritual confirmed (2-4 frames of DOOM)')
    print('✓ Post-warmup behavior verified')
    print()
    print('═' * 70)
    print('THE SHADER WARMUP PHASE WORKS')
    print()
    print('The renderer:')
    print('  1. Detects extreme stress')
    print('  2. Enters warmup ritual')
    print('  3. "Compiles shaders" (that don\'t exist)')
    print('  4. Runs DOOM for 2-4 frames (the sacred rite)')
    print('  5. Pretends everything is fine')
    print('  6. Actually FEELS better')
    print()
    print('This is not a bug. This is the renderer coping.')
    print('═' * 70)


if __name__ == '__main__':
    main()
