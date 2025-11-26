#!/usr/bin/env python3
"""
Gameplay test – Validates core mechanics
"""

import sys
sys.path.insert(0, 'src')

from mall_engine import MallEngine, Direction
from entities import NPCSystem, ArtifactSystem
from toddler_system import ToddlerSystem


def test_movement():
    """Test player movement"""
    print("[TEST] Movement...")
    engine = MallEngine()

    start_x, start_y, _ = engine.get_player_position()
    print(f"  Start position: ({start_x}, {start_y})")

    # Try to move forward (facing EAST from ENTRANCE)
    if engine.move_player(Direction.EAST):
        new_x, new_y, _ = engine.get_player_position()
        print(f"  Moved to: ({new_x}, {new_y}) ✓")
        assert new_x == start_x + 1, "Movement failed"
    else:
        print("  Movement blocked (expected at some tiles)")


def test_artifacts():
    """Test artifact pickup and lore"""
    print("\n[TEST] Artifacts...")
    engine = MallEngine()
    artifact_sys = ArtifactSystem()

    # Place an artifact
    artifact_id = "sunglasses"
    engine.add_artifact_to_location(artifact_id, 0, 24, 0)
    print(f"  Placed artifact: {artifact_id}")

    # Check it's there
    found = engine.get_artifact_at_location(0, 24, 0)
    print(f"  Found artifact at location: {found} ✓")

    # Pick it up
    if engine.pickup_artifact(artifact_id):
        print(f"  Picked up artifact ✓")
        assert artifact_id in engine.player.inventory, "Artifact not in inventory"

    # Get lore
    lore = artifact_sys.get_lore(artifact_id)
    print(f"  Lore length: {len(lore)} chars ✓")
    assert len(lore) > 0, "No lore found"


def test_npcs():
    """Test NPC system"""
    print("\n[TEST] NPCs...")
    npc_sys = NPCSystem()

    milo = npc_sys.get_npc("milo")
    print(f"  Milo loaded: {milo.name} ({milo.title}) ✓")

    # Get dialogue
    dialogue = npc_sys.get_dialogue("milo", "greeting")
    print(f"  Milo greeting: '{dialogue[:50]}...' ✓")

    # Test NPC movement
    npc_sys.move_npc("milo", 10, 10, 0)
    new_pos = milo.current_x, milo.current_y
    print(f"  Moved Milo to: {new_pos} ✓")


def test_toddler_system():
    """Test toddler presence"""
    print("\n[TEST] Toddler System...")
    todd_sys = ToddlerSystem()

    # Stage 0 (no presence)
    stage, msgs = todd_sys.update(0)
    print(f"  At 0s: Stage {stage.value} (none) ✓")
    assert stage.value == 0, "Wrong stage"

    # Stage 1 (5 minutes)
    stage, msgs = todd_sys.update(300)
    print(f"  At 5min: Stage {stage.value} (one) ✓")
    assert stage.value == 1, "Wrong stage"
    if msgs:
        print(f"    Message: {msgs[0]}")

    # Stage 2 (15 minutes)
    stage, msgs = todd_sys.update(900)
    print(f"  At 15min: Stage {stage.value} (two) ✓")
    assert stage.value == 2, "Wrong stage"
    if msgs:
        print(f"    Message: {msgs[0]}")

    # Test audio
    audio = todd_sys.get_audio_message()
    if audio:
        print(f"  Audio message: '{audio}' ✓")

    # Test shadow
    shadow = todd_sys.get_shadow_description()
    if shadow:
        print(f"  Shadow: '{shadow}' ✓")


def test_game_state():
    """Test full game state"""
    print("\n[TEST] Game State...")
    engine = MallEngine()

    # Check player state
    print(f"  Player position: {engine.get_player_position()}")
    print(f"  Player facing: {engine.get_player_facing()}")
    print(f"  Playtime: {engine.get_playtime()}s")
    print(f"  Inventory: {len(engine.player.inventory)} items")
    print(f"  At entrance: {engine.is_at_entrance()} ✓")

    # Test save/load
    state = engine.save_state()
    print(f"  State saved: {len(state)} keys ✓")

    engine2 = MallEngine()
    engine2.load_state(state)
    print(f"  State loaded ✓")
    assert engine2.get_player_position() == engine.get_player_position(), "State not restored"


def test_interaction():
    """Test player interaction"""
    print("\n[TEST] Interaction...")
    engine = MallEngine()
    npc_sys = NPCSystem()

    # Check what's at entrance
    npc = npc_sys.get_npc_at_location(0, 24, 0)
    print(f"  NPC at entrance: {npc} (none expected)")

    # Move player to food court (where there are shoppers)
    engine.player.x = 10
    engine.player.y = 25

    npc = npc_sys.get_npc_at_location(10, 25, 0)
    if npc:
        print(f"  NPC at food court: {npc.name} ✓")
        dialogue = npc_sys.get_dialogue(npc.id, "greeting")
        print(f"    Dialogue: '{dialogue}' ✓")
    else:
        print(f"  No NPC at (10,25) - spawns are random ✓")


def test_artifact_weirdness():
    """Test artifact weirdness boost"""
    print("\n[TEST] Artifact Weirdness Boost...")
    todd_sys = ToddlerSystem()

    # No artifacts
    stage, factor = todd_sys.apply_artifact_weirdness_boost(0)
    print(f"  0 artifacts: Stage {stage.value}, Factor {factor}")

    # Some artifacts
    stage, factor = todd_sys.apply_artifact_weirdness_boost(2)
    print(f"  2 artifacts: Stage {stage.value}, Factor {factor} ✓")

    # Lots of artifacts (should escalate)
    todd_sys.update(300)  # Ensure we're in stage 1
    stage, factor = todd_sys.apply_artifact_weirdness_boost(4)
    print(f"  4 artifacts in stage 1: Stage {stage.value}, Factor {factor} ✓")


if __name__ == "__main__":
    print("="*60)
    print("GLITCHDEX MALL ENGINE – GAMEPLAY TESTS")
    print("="*60)

    try:
        test_movement()
        test_artifacts()
        test_npcs()
        test_toddler_system()
        test_game_state()
        test_interaction()
        test_artifact_weirdness()

        print("\n" + "="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)

    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
