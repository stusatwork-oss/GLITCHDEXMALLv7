#!/usr/bin/env python3
"""
V7 INTEGRATED DEMO - The Horror Stack in Motion

Wires together:
1. Toddler reality catalyst → Cloud amplification
2. Janitor NPC → LLM dialogue (at Cloud 70+ when breaking rules)
3. Leon → game_state awareness and narration

This is the "make it scream" demo.

Usage:
    python v7_integrated_demo.py

    # With LLM (requires API key):
    export ANTHROPIC_API_KEY=...
    python v7_integrated_demo.py --with-llm

    # Specific scenario:
    python v7_integrated_demo.py --scenario toddler_manifests
"""

import sys
import time
import json
import os
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import V7 systems
from cloud import Cloud, MallMood
from ai.toddler.toddler_system import ToddlerSystem
from ai.toddler.toddler_config import TODDLER_CONFIG
from ai.npc_llm.janitor_llm import build_janitor_prompt, parse_npc_response


# ============================================================================
# MOCK CLASSES (for components not yet implemented)
# ============================================================================

class MockRenderer:
    """Mock renderer for glitch/strain tracking."""
    def __init__(self):
        self.glitch_intensity = 0.0
        self.reality_strain = 0.0
        self.camera_shake = 0.0

    def export_state(self) -> Dict:
        return {
            "glitch_intensity": self.glitch_intensity,
            "reality_strain": self.reality_strain,
            "camera_shake": self.camera_shake
        }


class MockPlayer:
    """Mock player for position/action tracking."""
    def __init__(self, position=(0, 0, 0)):
        self.position = position
        self.zone = "Z1_CENTRAL_ATRIUM"
        self.looking_at_toddler = False

    def update(self, dt: float, direction=(0, 0, 0)):
        """Move player."""
        speed = 10.0  # 10 ft/s
        self.position = (
            self.position[0] + direction[0] * speed * dt,
            self.position[1] + direction[1] * speed * dt,
            self.position[2] + direction[2] * speed * dt
        )

    def export_state(self) -> Dict:
        return {
            "position": self.position,
            "zone": self.zone
        }


class MockJanitor:
    """Mock Janitor NPC with rule tracking."""
    def __init__(self):
        self.power = 1478
        self.threshold = 70.0
        self.position = (50, 0, 0)  # SERVICE_HALL
        self.zone = "SERVICE_HALL"
        self.rule_description = "Never cross into FC-ARCADE"
        self.in_forbidden_zone = False
        self.has_spoken_contradiction = False

    def update(self, dt: float, cloud_level: float):
        """
        Simple rule: if Cloud >= 70, move toward FC-ARCADE (breaking rule).
        """
        if cloud_level >= self.threshold and not self.in_forbidden_zone:
            # Move toward FC-ARCADE
            self.position = (80, 20, 0)  # FC-ARCADE position
            self.zone = "FC-ARCADE"
            self.in_forbidden_zone = True
            print(f"\n  [!] Janitor BREAKS RULE: Enters FC-ARCADE (Cloud {cloud_level:.1f})")

    def export_state(self) -> Dict:
        return {
            "power": self.power,
            "threshold": self.threshold,
            "position": self.position,
            "zone": self.zone,
            "rule": self.rule_description,
            "in_forbidden_zone": self.in_forbidden_zone
        }


class MockLLMClient:
    """
    Mock LLM client that returns canned responses.
    Replace with real Anthropic/OpenAI client.
    """
    def __init__(self, use_real_llm=False):
        self.use_real_llm = use_real_llm
        if use_real_llm:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
                self.model = "claude-3-5-haiku-20241022"
                print("[LLM] Using real Anthropic API (Claude 3.5 Haiku)")
            except ImportError:
                print("[LLM] anthropic package not found, falling back to mock")
                self.use_real_llm = False
            except Exception as e:
                print(f"[LLM] Failed to initialize Anthropic client: {e}")
                self.use_real_llm = False

    def chat(self, system: str, user: str) -> str:
        """Send chat request and return response."""
        if self.use_real_llm:
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=500,
                    system=system,
                    messages=[{"role": "user", "content": user}]
                )
                return response.content[0].text
            except Exception as e:
                print(f"[LLM] API call failed: {e}")
                return self._mock_response(system, user)
        else:
            return self._mock_response(system, user)

    def _mock_response(self, system: str, user: str) -> str:
        """Return canned response based on context."""
        # Parse Cloud level from system prompt
        if "Cloud level: " in system:
            try:
                cloud_str = system.split("Cloud level: ")[1].split(" ")[0]
                cloud_level = float(cloud_str)
            except:
                cloud_level = 0

        # Parse zone from system prompt
        zone = "UNKNOWN"
        if "Current zone: " in system:
            zone = system.split("Current zone: ")[1].split(" ")[0]

        # Generate appropriate response based on context
        if "RULE_BROKEN" in user and cloud_level >= 70:
            return json.dumps({
                "utterance": "The arcade machines... they're humming in E-flat. Same as the escalators. Same as the fountain pump. It's all connected. I tried to ignore it from the service hall, but the sound - it's pulling at the walls.",
                "emotional_state": "obsessed",
                "tags": ["arcade_machines", "escalators", "fountain", "E-flat", "service_hall"],
                "action_hint": "touching arcade cabinet, listening intently"
            })
        elif cloud_level > 50:
            return json.dumps({
                "utterance": "Something's not right with the ventilation. The air feels thick.",
                "emotional_state": "uneasy",
                "tags": ["ventilation", "air"],
                "action_hint": "checking vents"
            })
        else:
            return json.dumps({
                "utterance": "Just another shift. Nothing unusual.",
                "emotional_state": "weary",
                "tags": [],
                "action_hint": "pushing mop cart"
            })


# ============================================================================
# V7 INTEGRATED SIMULATION
# ============================================================================

class V7IntegratedSim:
    """
    The Horror Stack in motion.

    Integrates:
    - Toddler (reality catalyst)
    - Cloud (mood/pressure system)
    - Janitor (NPC with LLM dialogue)
    - Leon (game_state narrator)
    - Renderer (glitch/strain)
    """

    def __init__(self, use_real_llm=False):
        print("\n" + "="*60)
        print("  V7 INTEGRATED SIMULATION")
        print("  The Horror Stack: ONLINE")
        print("="*60 + "\n")

        # Initialize systems
        self.cloud = Cloud()
        self.toddler = ToddlerSystem(
            initial_position=(100, 0, -8),  # Food Court
            config=TODDLER_CONFIG
        )
        self.player = MockPlayer(position=(0, 0, 0))  # Atrium
        self.janitor = MockJanitor()
        self.renderer = MockRenderer()
        self.llm = MockLLMClient(use_real_llm=use_real_llm)

        # Sim state
        self.time = 0.0
        self.tick_count = 0
        self.janitor_has_spoken = False

        print("[SIM] Systems initialized:")
        print(f"  - Cloud: {self.cloud.cloud_level:.1f} ({self.cloud.mall_mood.value})")
        print(f"  - Toddler: {self.toddler.position} (invisible)")
        print(f"  - Player: {self.player.position} (Atrium)")
        print(f"  - Janitor: {self.janitor.position} (Service Hall)")
        print(f"  - LLM: {'REAL' if use_real_llm else 'MOCK'}")
        print()

    def tick(self, dt: float = 1.0):
        """
        Single simulation tick.

        1. Update toddler → get effects
        2. Apply toddler effects to Cloud/QBIT/renderer
        3. Update Cloud
        4. Update Janitor (check for contradiction)
        5. If Janitor breaks rule + not spoken → LLM dialogue
        6. Export game_state for Leon
        """
        self.tick_count += 1
        self.time += dt

        # 1. Update toddler
        toddler_effects = self.toddler.update(
            dt=dt,
            player_position=self.player.position,
            current_cloud=self.cloud.cloud_level,
            player_looking_at_toddler=self.player.looking_at_toddler,
            npc_contradiction_triggered=self.janitor.in_forbidden_zone
        )

        # 2. Apply toddler → Cloud/QBIT/renderer
        self._apply_toddler_to_cloud(toddler_effects)
        self._apply_toddler_to_qbit(toddler_effects)
        self._apply_toddler_to_renderer(toddler_effects)

        # 3. Update Cloud
        self.cloud.update(dt, player_action=None)

        # 4. Update Janitor
        self.janitor.update(dt, self.cloud.cloud_level)

        # 5. Check for Janitor LLM trigger
        if (self.cloud.cloud_level >= 70 and
            self.janitor.in_forbidden_zone and
            not self.janitor_has_spoken):
            self._trigger_janitor_llm(toddler_effects)
            self.janitor_has_spoken = True

        # 6. Export game_state (for Leon)
        game_state = self._build_game_state(toddler_effects)

        return game_state

    def _apply_toddler_to_cloud(self, toddler_effects: Dict):
        """Wire toddler heat_multiplier → Cloud pressure."""
        # Get base Cloud delta (would normally come from player actions)
        base_delta = 0.5  # Passive Cloud gain per tick

        # Amplify by toddler
        heat_mult = toddler_effects.get("heat_multiplier", 1.0)
        amplified_delta = base_delta * heat_mult

        # Extra spike if toddler very close + visible
        distance = toddler_effects.get("distance_to_player", 999)
        visible = toddler_effects.get("toddler_visible", 0)
        if distance < 5 and visible > 0.5:
            amplified_delta += 0.5  # Close encounter spike

        # Apply to Cloud (direct manipulation for demo)
        self.cloud.cloud_level = min(100, self.cloud.cloud_level + amplified_delta)

        # Update mood
        if self.cloud.cloud_level < 25:
            self.cloud.mall_mood = MallMood.CALM
        elif self.cloud.cloud_level < 50:
            self.cloud.mall_mood = MallMood.UNEASY
        elif self.cloud.cloud_level < 75:
            self.cloud.mall_mood = MallMood.STRAINED
        else:
            self.cloud.mall_mood = MallMood.CRITICAL

    def _apply_toddler_to_qbit(self, toddler_effects: Dict):
        """Wire toddler reality_strain → Zone QBIT agitation."""
        toddler_pos = toddler_effects.get("toddler_position")
        reality_strain = toddler_effects.get("reality_strain", 0)

        # Determine which zone toddler is in (simplified)
        # In real implementation, would use zone geometry
        zone_id = "Z4_FOOD_COURT"  # Hardcoded for demo

        # Get or create zone microstate
        if zone_id in self.cloud.zones:
            zone = self.cloud.zones[zone_id]
            # Agitate zone turbulence
            zone.turbulence += reality_strain * 0.5
            zone.turbulence = min(10.0, zone.turbulence)

    def _apply_toddler_to_renderer(self, toddler_effects: Dict):
        """Wire toddler glitch_multiplier → Renderer strain."""
        glitch_mult = toddler_effects.get("glitch_multiplier", 1.0)
        reality_strain = toddler_effects.get("reality_strain", 0)

        self.renderer.glitch_intensity = (glitch_mult - 1.0) / 3.0
        self.renderer.reality_strain = reality_strain

        # Camera shake if very close
        if toddler_effects.get("distance_to_player", 999) < 10:
            self.renderer.camera_shake = reality_strain * 0.2
        else:
            self.renderer.camera_shake = 0.0

    def _trigger_janitor_llm(self, toddler_effects: Dict):
        """
        Generate Janitor dialogue via LLM.

        Trigger: Cloud >= 70 AND janitor.in_forbidden_zone == True
        """
        print("\n" + "="*60)
        print("  [LLM TRIGGER] Janitor breaks rule - generating dialogue")
        print("="*60 + "\n")

        # Build game metadata for prompt
        metadata = {
            "atrium_diameter": 175,
            "tensile_masts": 32
        }

        # Build zone context
        zone = {
            "id": self.janitor.zone,
            "qbit_aggregate": 6112  # FC-ARCADE QBIT influence
        }

        # Build event context
        event = {
            "type": "RULE_BROKEN",
            "zone": self.janitor.zone,
            "prev_cloud": self.cloud.cloud_level - 5,  # Approximate
            "time": self.time
        }

        # Build cloud context
        cloud_state = {
            "cloud_level": self.cloud.cloud_level,
            "mall_mood": self.cloud.mall_mood.value
        }

        # Generate prompt
        system, user = build_janitor_prompt(
            janitor=self.janitor.export_state(),
            cloud=cloud_state,
            zone=zone,
            metadata=metadata,
            event=event
        )

        print("[LLM] Sending prompt to model...")
        print(f"  System: {len(system)} chars")
        print(f"  User: {len(user)} chars")
        print()

        # Call LLM
        response = self.llm.chat(system, user)

        # Parse response
        dialogue = parse_npc_response(response)

        # Display result
        print("="*60)
        print(f"  JANITOR (Cloud {self.cloud.cloud_level:.1f}, {self.cloud.mall_mood.value})")
        print("="*60)
        print(f"\n  \"{dialogue['utterance']}\"\n")
        print(f"  [Emotional state: {dialogue['emotional_state']}]")
        if dialogue.get('action_hint'):
            print(f"  [{dialogue['action_hint']}]")
        if dialogue.get('tags'):
            print(f"  Tags: {', '.join(dialogue['tags'])}")
        print("\n" + "="*60 + "\n")

    def _build_game_state(self, toddler_effects: Dict) -> Dict:
        """
        Build complete game_state for Leon.

        This is what Leon sees when generating narration.
        """
        return {
            "game_time": self.time,
            "tick_count": self.tick_count,
            "player": self.player.export_state(),
            "cloud": {
                "level": self.cloud.cloud_level,
                "mood": self.cloud.mall_mood.value,
                "pressure_trend": self.cloud.pressure_trend.value
            },
            "toddler": {
                "visible": toddler_effects["toddler_visible"],
                "distance": toddler_effects["distance_to_player"],
                "reality_strain": toddler_effects["reality_strain"],
                "in_distortion_field": toddler_effects["in_distortion_field"],
                "behavior": toddler_effects["behavior"],
                "position": toddler_effects["toddler_position"]
            },
            "janitor": self.janitor.export_state(),
            "renderer": self.renderer.export_state()
        }

    def run_scenario(self, scenario="default", max_ticks=100):
        """
        Run a predefined scenario.

        Scenarios:
        - default: Normal simulation until Janitor speaks
        - toddler_manifests: Accelerated Cloud, toddler becomes visible
        - critical_spiral: Fast progression to critical mood
        """
        print(f"\n[SCENARIO] Running: {scenario}")
        print(f"  Max ticks: {max_ticks}")
        print()

        for tick in range(max_ticks):
            game_state = self.tick(dt=1.0)

            # Print status every 10 ticks
            if tick % 10 == 0:
                self._print_status(game_state, tick)

            # Stop if Janitor has spoken
            if self.janitor_has_spoken:
                print(f"\n[SCENARIO] Complete: Janitor spoke at tick {tick}")
                break

            # Scenario-specific modifiers
            if scenario == "toddler_manifests":
                # Accelerate Cloud gain
                self.cloud.cloud_level += 1.0
            elif scenario == "critical_spiral":
                # Rapid Cloud increase
                self.cloud.cloud_level += 2.0

        # Final status
        print("\n" + "="*60)
        print("  FINAL STATE")
        print("="*60)
        self._print_status(game_state, tick)

    def _print_status(self, game_state: Dict, tick: int):
        """Print current simulation status."""
        cloud = game_state["cloud"]
        toddler = game_state["toddler"]
        renderer = game_state["renderer"]

        print(f"\nTick {tick:3d} | Time {game_state['game_time']:.1f}s")
        print(f"  Cloud: {cloud['level']:5.1f} ({cloud['mood']:>9s})")
        print(f"  Toddler: vis={toddler['visible']:.2f} dist={toddler['distance']:5.1f}ft behavior={toddler['behavior']}")
        print(f"  Janitor: {game_state['janitor']['zone']} (rule: {'BROKEN' if game_state['janitor']['in_forbidden_zone'] else 'intact'})")
        print(f"  Renderer: glitch={renderer['glitch_intensity']:.2f} strain={renderer['reality_strain']:.2f}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run V7 integrated demo."""
    import argparse

    parser = argparse.ArgumentParser(description="V7 Integrated Horror Stack Demo")
    parser.add_argument("--with-llm", action="store_true", help="Use real LLM (requires API key)")
    parser.add_argument("--scenario", default="default", choices=["default", "toddler_manifests", "critical_spiral"])
    parser.add_argument("--max-ticks", type=int, default=100, help="Maximum simulation ticks")

    args = parser.parse_args()

    # Create sim
    sim = V7IntegratedSim(use_real_llm=args.with_llm)

    # Run scenario
    sim.run_scenario(scenario=args.scenario, max_ticks=args.max_ticks)

    print("\n[DEMO] Complete. The mall spoke.\n")


if __name__ == "__main__":
    main()
