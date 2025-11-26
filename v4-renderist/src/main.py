#!/usr/bin/env python3
"""
RENDERIST MALL OS - V4
The Cloud-Driven World

Where canon emerges from resonance and repetition.

V4.0.2 Phase 2 Integration Demo
- 60fps loop with Cloud tick every 10 frames
- Interpolation for NPC/Swarm reads between ticks
- Contradiction cascade with 30-second zone cooldown
- Bleed Events with three tiers and wind-down
- AO3 logging for all events
- Console output for debugging
"""

import sys
import os
import json
import time
from typing import Dict, List, Optional

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from cloud import Cloud, MallMood
from anchor_npcs import AnchorNPCSystem, NPCState
from swarm import SwarmSystem
from bleed_events import BleedEventSystem, BleedState

# LOCKED CONSTANTS
CLOUD_UPDATE_INTERVAL = 10  # frames - Cloud updates every 10 frames
ZONE_CONTRADICTION_COOLDOWN = 30.0  # seconds between contradictions in same zone
BLEED_WINDDOWN_TIME = 7.5  # seconds for Bleed to fade
TARGET_FPS = 60
FRAME_TIME = 1.0 / TARGET_FPS

# Demo settings
DEMO_DURATION = 45.0  # seconds (increased for bleed events)
CONSOLE_OUTPUT_INTERVAL = 60  # frames (1 second at 60fps)


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b by t."""
    return a + (b - a) * t


class MallDemo:
    """
    V4.0.2 Phase 2 Integration Demo

    Exercises Cloud + Anchors + Swarm + Cascade + Bleed.
    """

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')

        # Core systems
        self.cloud: Optional[Cloud] = None
        self.anchors: Optional[AnchorNPCSystem] = None
        self.swarm: Optional[SwarmSystem] = None
        self.bleed: Optional[BleedEventSystem] = None

        # World spine data
        self.spine_data: Dict = {}
        self.zones: Dict = {}
        self.zone_graph: Dict = {}

        # Cloud interpolation state
        self.previous_cloud_level: float = 0.0
        self.current_cloud_level: float = 0.0
        self.previous_cloud_hints: Dict = {}
        self.current_cloud_hints: Dict = {}

        # Frame tracking
        self.frame_count: int = 0
        self.dt: float = FRAME_TIME

        # Contradiction cascade tracking
        self.active_contradictions: List[Dict] = []

        # AO3 Logs (all events)
        self.ao3_log: List[Dict] = []

        # Demo state
        self.running: bool = False
        self.start_time: float = 0.0

    def load_spine(self) -> bool:
        """Load world_spine.json and initialize world state."""
        spine_path = os.path.join(self.docs_dir, 'schemas', 'world_spine.json')

        if not os.path.exists(spine_path):
            print(f"[ERROR] World spine not found: {spine_path}")
            return False

        try:
            with open(spine_path, 'r') as f:
                self.spine_data = json.load(f)

            # Extract zone data
            for zone in self.spine_data.get("world", {}).get("zones", []):
                zone_id = zone["id"]
                self.zones[zone_id] = {
                    "type": zone.get("type", "STORE"),
                    "turbulence": zone.get("turbulence", 1.0),
                    "adjacent_to": zone.get("adjacent_to", []),
                    "microstate": zone.get("microstate", "normal"),
                    "bleed_mod": zone.get("bleed_mod", 1.0),
                    "last_contradiction_time": 0.0  # For cascade cooldown
                }
                # Build adjacency graph
                self.zone_graph[zone_id] = zone.get("adjacent_to", [])

            print(f"[SPINE] Loaded {len(self.zones)} zones from world_spine.json")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to load spine: {e}")
            return False

    def initialize(self) -> bool:
        """Initialize all V4 systems."""
        print("\n" + "=" * 60)
        print("V4.0.2 PHASE 2 INTEGRATION DEMO")
        print("=" * 60)
        print("\n[INIT] Loading systems...")

        # Load world spine
        if not self.load_spine():
            return False

        # Initialize Cloud
        try:
            self.cloud = Cloud()
            self.cloud.cloud_level = 0.0  # Start fresh for demo
            self.previous_cloud_level = 0.0
            self.current_cloud_level = 0.0
            print("[CLOUD] Global state initialized")
        except Exception as e:
            print(f"[ERROR] Cloud init failed: {e}")
            return False

        # Initialize Anchor NPCs
        try:
            self.anchors = AnchorNPCSystem(self.cloud)
            self.anchors.reset_contradictions()  # Fresh start
            npc_count = len(self.anchors.npcs)
            print(f"[ANCHORS] {npc_count} NPCs initialized")
        except Exception as e:
            print(f"[ERROR] Anchors init failed: {e}")
            return False

        # Initialize Swarm
        try:
            zone_list = list(self.zones.keys())
            self.swarm = SwarmSystem(zones=zone_list)
            print(f"[SWARM] System initialized with {len(zone_list)} zones")
        except Exception as e:
            print(f"[ERROR] Swarm init failed: {e}")
            return False

        # Initialize Bleed Events
        try:
            self.bleed = BleedEventSystem()
            print(f"[BLEED] System initialized (tiers @ 60/75/90)")
        except Exception as e:
            print(f"[ERROR] Bleed init failed: {e}")
            return False

        print("\n[INIT] All systems online")
        return True

    def tick_cloud(self) -> Dict:
        """
        Update Cloud state (called every CLOUD_UPDATE_INTERVAL frames).

        Returns render hints for the new state.
        """
        # Store previous state for interpolation
        self.previous_cloud_level = self.current_cloud_level
        self.previous_cloud_hints = self.current_cloud_hints.copy()

        # Accumulate dt for the batched update
        batch_dt = self.dt * CLOUD_UPDATE_INTERVAL

        # Simulate player action (wandering the mall, more aggressive for demo)
        player_action = {
            "type": "move",
            "zone": "FOOD_COURT" if self.frame_count < 300 else "SERVICE_HALL",
            "time_in_zone": (self.frame_count % 300) * self.dt
        }

        # Frequent discoveries to drive pressure up faster
        if self.frame_count % 60 == 0:  # Every 1 second
            player_action = {
                "type": "interact",
                "target": "artifact_fragment",
                "zone": player_action["zone"]
            }

        # Frequent AO3 log discoveries (high pressure)
        if self.frame_count % 180 == 0 and self.frame_count > 0:  # Every 3 seconds
            player_action = {
                "type": "interact",
                "target": "ao3_log_entry",
                "zone": player_action["zone"]
            }

        # NPC events (from contradiction cascade)
        npc_events = []
        for contradiction in self.active_contradictions:
            npc_events.append({
                "type": "npc_contradiction",
                "npc_id": contradiction["npc_id"],
                "broken_rule": contradiction["action"]
            })
        self.active_contradictions.clear()

        # Update Cloud
        hints = self.cloud.update(batch_dt, player_action, npc_events)
        self.current_cloud_level = self.cloud.cloud_level
        self.current_cloud_hints = hints

        # Apply swarm feedback (confirming only, ±5% cap)
        if self.swarm:
            swarm_result = self.swarm.update(
                batch_dt,
                self.cloud.cloud_level,
                self.cloud.mall_mood.value,
                self.current_cloud_level - self.previous_cloud_level,
                self.cloud.zones
            )
            # Apply capped swarm feedback
            swarm_delta = swarm_result.get("cloud_feedback", 0.0)
            self.cloud.cloud_level = max(0, min(100, self.cloud.cloud_level + swarm_delta))

        return hints

    def update_bleed(self, current_time: float):
        """
        Update Bleed system and log events to AO3.

        Called after Cloud update.
        """
        if not self.bleed or not self.swarm:
            return

        # Get zone turbulence from Cloud
        zone_turbulence = {}
        for zone_id in self.zones:
            if zone_id in self.cloud.zones:
                zone_turbulence[zone_id] = self.cloud.zones[zone_id].turbulence
            else:
                zone_turbulence[zone_id] = self.zones[zone_id].get("turbulence", 1.0)

        # Get zone density from Swarm
        zone_density = self.swarm.density_by_zone

        # Update bleed system
        bleed_result = self.bleed.update(
            self.dt * CLOUD_UPDATE_INTERVAL,  # Use batched dt
            self.cloud.cloud_level,
            zone_turbulence,
            zone_density
        )

        # Log bleed events to AO3
        for event in bleed_result.get("events", []):
            ao3_event = {
                "type": event["type"],
                "timestamp": current_time,
                "tick": self.frame_count,
                "tier": event["tier"],
                "origin_zone": event["origin_zone"],
                "cloud_level": event["cloud_level"],
                "turbulence_snapshot": event["turbulence_snapshot"],
            }
            # Add extra fields if present
            if "old_tier" in event:
                ao3_event["old_tier"] = event["old_tier"]
            if "new_tier" in event:
                ao3_event["new_tier"] = event["new_tier"]
            if "resumed_from_winddown" in event:
                ao3_event["resumed_from_winddown"] = event["resumed_from_winddown"]

            self.ao3_log.append(ao3_event)

            # Print bleed transitions
            if event["type"] == "BLEED_START":
                print(f"\n  >>> BLEED START: Tier {event['tier']} from {event['origin_zone']}")
            elif event["type"] == "BLEED_TIER_CHANGE":
                if "old_tier" in event:
                    print(f"\n  >>> BLEED TIER: {event['old_tier']} -> {event['new_tier']}")
                else:
                    print(f"\n  >>> BLEED RESUMED: Tier {event.get('new_tier', event['tier'])}")
            elif event["type"] == "BLEED_WINDDOWN_START":
                print(f"\n  >>> BLEED WINDDOWN: {BLEED_WINDDOWN_TIME}s remaining")
            elif event["type"] == "BLEED_END":
                print(f"\n  >>> BLEED END")

    def get_interpolated_cloud(self) -> Dict:
        """
        Get interpolated Cloud state for smooth NPC/Swarm reads.

        NPCs and Swarm read interpolated values between Cloud ticks.
        """
        # Calculate interpolation factor
        frames_since_tick = self.frame_count % CLOUD_UPDATE_INTERVAL
        t = frames_since_tick / CLOUD_UPDATE_INTERVAL

        # Interpolate cloud level
        interp_level = lerp(self.previous_cloud_level, self.current_cloud_level, t)

        # Build interpolated hints
        interp_hints = {
            "cloud_level": interp_level,
            "mood": self.cloud.mall_mood.value,
            "trend": self.cloud.pressure_trend.value,
            "bleed_tier": self.cloud.current_bleed_tier
        }

        return interp_hints

    def check_contradiction_cascade(self, current_time: float):
        """
        Check for and trigger contradiction cascade.

        LOCKED: Zone-local cooldown = 30 seconds
        Only one contradiction per zone per cooldown period.
        """
        if not self.anchors:
            return

        cloud_level = self.cloud.cloud_level
        cloud_hints = self.get_interpolated_cloud()

        # Get zone states for NPC update
        zone_states = {}
        for zone_id, zone in self.zones.items():
            if zone_id in self.cloud.zones:
                zone_states[zone_id] = self.cloud.zones[zone_id].to_dict()
            else:
                zone_states[zone_id] = {"turbulence": zone.get("turbulence", 0)}

        # Update all NPCs
        npc_updates = self.anchors.update(cloud_hints, zone_states)

        # Check for contradiction triggers
        for npc_id, npc_data in npc_updates.items():
            if not npc_data.get("contradiction_available", False):
                continue

            npc = self.anchors.get_npc(npc_id)
            if not npc or npc.contradiction_used:
                continue

            # Check if Cloud level meets threshold
            if cloud_level < npc.spine.contradiction_trigger:
                continue

            # Check zone cooldown (LOCKED: 30 seconds)
            zone_id = npc.home_zone
            zone_data = self.zones.get(zone_id, {})
            last_contradiction = zone_data.get("last_contradiction_time", 0.0)

            if current_time - last_contradiction < ZONE_CONTRADICTION_COOLDOWN:
                # Zone still on cooldown
                continue

            # TRIGGER CONTRADICTION
            action = self.anchors.trigger_contradiction(npc_id)
            if action:
                # Update zone cooldown (skip if zone not in our map)
                if zone_id in self.zones:
                    self.zones[zone_id]["last_contradiction_time"] = current_time

                # Record in active contradictions (for next Cloud tick)
                contradiction_event = {
                    "type": "NPC_CONTRADICTION",
                    "timestamp": current_time,
                    "tick": self.frame_count,
                    "npc_id": npc_id,
                    "npc_name": npc.name,
                    "zone": zone_id,
                    "action": action,
                    "cloud_level": cloud_level
                }
                self.active_contradictions.append(contradiction_event)

                # Log to AO3
                self.ao3_log.append(contradiction_event)

                print(f"\n  !!! CONTRADICTION: {npc.name} in {zone_id}")
                print(f"      \"{action}\"")

    def update_frame(self, current_time: float):
        """Update a single frame."""
        # Cloud ticks every CLOUD_UPDATE_INTERVAL frames
        if self.frame_count % CLOUD_UPDATE_INTERVAL == 0:
            self.tick_cloud()
            # Update Bleed after Cloud
            self.update_bleed(current_time)

        # Check for contradiction cascade (every frame)
        self.check_contradiction_cascade(current_time)

        # Increment frame counter
        self.frame_count += 1

    def output_status(self):
        """Output current status to console."""
        # Get interpolated state for display
        interp = self.get_interpolated_cloud()

        # Count events by type
        bleed_events = len([e for e in self.ao3_log if e["type"].startswith("BLEED")])
        contradictions = len([e for e in self.ao3_log if e["type"] == "NPC_CONTRADICTION"])

        # Get NPC emotional summary
        npc_summary = []
        if self.anchors:
            for npc_id, npc in self.anchors.npcs.items():
                if npc.state != NPCState.NORMAL:
                    npc_summary.append(f"{npc.name}:{npc.state.value}")

        # Swarm population
        swarm_pop = self.swarm.current_population if self.swarm else 0

        # Bleed status
        bleed_info = ""
        if self.bleed:
            if self.bleed.state == BleedState.ACTIVE:
                bleed_info = f" | Bleed: T{self.bleed.current_tier.value}"
            elif self.bleed.state == BleedState.WINDDOWN:
                bleed_info = f" | Bleed: WIND({self.bleed.winddown_remaining:.1f}s)"

        print(f"\n[TICK {self.frame_count:>5}] "
              f"Cloud: {interp['cloud_level']:.1f} ({interp['mood']}) "
              f"| Swarm: {swarm_pop}"
              f"{bleed_info}")

        if npc_summary:
            print(f"  NPCs: {', '.join(npc_summary[:5])}")

        # Zone activity
        if self.swarm:
            top_zones = sorted(
                self.swarm.density_by_zone.items(),
                key=lambda x: -x[1]
            )[:3]
            zones_str = ", ".join(f"{z}:{c}" for z, c in top_zones if c > 0)
            if zones_str:
                print(f"  Zones: {zones_str}")

    def run(self, duration: float = DEMO_DURATION) -> bool:
        """
        Run the integration demo.

        Args:
            duration: How long to run in seconds

        Returns:
            True if completed successfully
        """
        if not self.initialize():
            return False

        print(f"\n[DEMO] Running for {duration} seconds at {TARGET_FPS} fps")
        print(f"[DEMO] Cloud updates every {CLOUD_UPDATE_INTERVAL} frames")
        print(f"[DEMO] Bleed tiers @ 60/75/90, wind-down: {BLEED_WINDDOWN_TIME}s")
        print(f"[DEMO] Zone cooldown: {ZONE_CONTRADICTION_COOLDOWN}s")
        print("\n" + "-" * 60)

        self.running = True
        self.start_time = time.time()
        self.frame_count = 0

        try:
            while self.running:
                frame_start = time.time()
                current_time = frame_start - self.start_time

                # Check duration
                if current_time >= duration:
                    self.running = False
                    break

                # Update frame
                self.update_frame(current_time)

                # Output status periodically
                if self.frame_count % CONSOLE_OUTPUT_INTERVAL == 0:
                    self.output_status()

                # Frame timing
                elapsed = time.time() - frame_start
                if elapsed < FRAME_TIME:
                    time.sleep(FRAME_TIME - elapsed)

        except KeyboardInterrupt:
            print("\n[DEMO] Interrupted by user")
            self.running = False

        # Final summary
        self.print_summary()
        return True

    def print_summary(self):
        """Print demo summary."""
        print("\n" + "=" * 60)
        print("DEMO SUMMARY")
        print("=" * 60)

        elapsed = time.time() - self.start_time
        print(f"\nDuration: {elapsed:.1f}s ({self.frame_count} frames)")
        print(f"Final Cloud: {self.cloud.cloud_level:.1f} ({self.cloud.mall_mood.value})")
        print(f"Swarm Population: {self.swarm.current_population if self.swarm else 0}")

        # Event counts
        bleed_events = [e for e in self.ao3_log if e["type"].startswith("BLEED")]
        contradictions = [e for e in self.ao3_log if e["type"] == "NPC_CONTRADICTION"]

        print(f"\nBleed Events: {len(bleed_events)}")
        if self.bleed:
            print(f"  Total Bleeds: {self.bleed.get_event_count()}")

        print(f"Contradictions: {len(contradictions)}")

        # AO3 Log
        if self.ao3_log:
            print("\nAO3 Event Log:")
            for event in self.ao3_log[-10:]:  # Last 10 events
                event_type = event["type"]
                timestamp = event.get("timestamp", 0)

                if event_type == "NPC_CONTRADICTION":
                    print(f"  [{timestamp:.1f}s] {event_type}: {event['npc_name']}")
                elif event_type.startswith("BLEED"):
                    tier = event.get("tier", 0)
                    origin = event.get("origin_zone", "")
                    if event_type == "BLEED_START":
                        print(f"  [{timestamp:.1f}s] {event_type}: Tier {tier} @ {origin}")
                    elif event_type == "BLEED_TIER_CHANGE":
                        old_t = event.get("old_tier", "?")
                        new_t = event.get("new_tier", tier)
                        print(f"  [{timestamp:.1f}s] {event_type}: {old_t} -> {new_t}")
                    else:
                        print(f"  [{timestamp:.1f}s] {event_type}")

        # NPC states
        print("\nFinal NPC States:")
        if self.anchors:
            states = {}
            for npc in self.anchors.npcs.values():
                state = npc.state.value
                states[state] = states.get(state, 0) + 1
            for state, count in states.items():
                print(f"  {state}: {count}")

        print("\n" + "=" * 60)


def mall_demo():
    """Entry point for the integration demo."""
    demo = MallDemo()
    return demo.run()


def main():
    """Main entry point."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                      RENDERIST MALL OS v4.0.2                        ║
║                                                                      ║
║                   Phase 2 Integration Demo                           ║
║                                                                      ║
║  "Canon emerges from resonance and repetition, not ego."            ║
╚══════════════════════════════════════════════════════════════════════╝
""")

    try:
        # Run the demo
        success = mall_demo()

        if success:
            print("\nPress ENTER to return to launcher...")
            input()
        else:
            print("\n[ERROR] Demo failed to run")
            sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
