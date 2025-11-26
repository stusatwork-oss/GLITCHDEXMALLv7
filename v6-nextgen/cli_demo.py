#!/usr/bin/env python3
"""
CLI Demo Client for V6 Bridge Server

Simple test client that exercises the bridge API without UE5.
Proves the bridge works independently of the game engine.

Usage:
    python cli_demo.py                    # Auto mode (loop)
    python cli_demo.py --once             # Single tick
    python cli_demo.py --status-only      # Just show status
    python cli_demo.py --reset            # Reset world state
"""

import requests
import time
import sys
import argparse
from typing import Dict, Any, Optional


BASE_URL = "http://localhost:5005"


class BridgeClient:
    """Simple client for V6 bridge server."""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    def health(self) -> Dict[str, Any]:
        """Check server health."""
        r = requests.get(f"{self.base_url}/health")
        r.raise_for_status()
        return r.json()

    def status(self) -> Dict[str, Any]:
        """Get current world status."""
        r = requests.get(f"{self.base_url}/status")
        r.raise_for_status()
        return r.json()

    def init(self, config_path: str = "config") -> Dict[str, Any]:
        """Initialize world."""
        r = requests.post(f"{self.base_url}/init", json={
            "config_path": config_path
        })
        r.raise_for_status()
        return r.json()

    def tick(self, dt: float = 0.25, player_event: Optional[Dict] = None) -> Dict[str, Any]:
        """Advance simulation one tick."""
        r = requests.post(f"{self.base_url}/tick", json={
            "dt": dt,
            "player_event": player_event
        })
        r.raise_for_status()
        return r.json()

    def reset(self, keep_memory: bool = False) -> Dict[str, Any]:
        """Reset world state."""
        r = requests.post(f"{self.base_url}/reset", json={
            "keep_memory": keep_memory
        })
        r.raise_for_status()
        return r.json()


def print_header(text: str):
    """Print section header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def print_cloud(cloud: Dict):
    """Print cloud state."""
    level = cloud["level"]
    mood = cloud["mood"]
    trend = cloud["trend"]

    # Color based on mood
    if mood == "calm":
        color = "\033[92m"  # Green
    elif mood == "uneasy":
        color = "\033[93m"  # Yellow
    elif mood == "strained":
        color = "\033[91m"  # Orange (red)
    else:  # critical
        color = "\033[95m"  # Magenta
    reset = "\033[0m"

    # Trend arrow
    if trend == "rising":
        arrow = "↑"
    elif trend == "falling":
        arrow = "↓"
    elif trend == "spiking":
        arrow = "⇈"
    else:
        arrow = "→"

    print(f"  Cloud: {color}{level:5.1f}/100{reset} | {mood:10} {arrow}")


def print_npcs(npcs: list, max_show: int = 3):
    """Print NPC states."""
    print(f"\n  NPCs ({len(npcs)} total):")

    for i, npc in enumerate(npcs[:max_show]):
        state = npc["state"]
        hint = npc["behavior_hint"]
        zone = npc["zone"]

        # State icon
        if state == "idle":
            icon = "○"
        elif state == "patrol":
            icon = "⊙"
        elif state == "alert":
            icon = "◎"
        elif state == "suspicious":
            icon = "⊗"
        elif state == "hostile":
            icon = "⊛"
        elif state == "contradiction":
            icon = "⊠"
        else:
            icon = "?"

        print(f"    {icon} {npc['id']:15} | {state:12} | {hint:20} | {zone}")

    if len(npcs) > max_show:
        print(f"    ... and {len(npcs) - max_show} more")


def print_events(events: list):
    """Print events that occurred."""
    if not events:
        return

    print(f"\n  Events:")
    for event in events:
        event_type = event["type"]
        details = event.get("details", {})

        if event_type == "cloud_mood_changed":
            print(f"    ⚡ Cloud mood: {details['from']} → {details['to']}")
        elif event_type == "contradiction_triggered":
            print(f"    ⚠️  Contradiction: {details.get('npc_name', 'Unknown')} broke rules")
        else:
            print(f"    • {event_type}")


def print_top_zones(zones: Dict, max_show: int = 3):
    """Print zones with highest turbulence."""
    # Sort by turbulence descending
    sorted_zones = sorted(
        zones.items(),
        key=lambda x: x[1].get("turbulence", 0),
        reverse=True
    )

    print(f"\n  Top Zones (by turbulence):")
    for zone_id, zone in sorted_zones[:max_show]:
        turb = zone.get("turbulence", 0)
        qbit = zone.get("qbit_aggregate", 0)
        print(f"    {zone_id:20} | turb={turb:4.1f} | QBIT={qbit:6.0f}")


def demo_status_only():
    """Just show current status."""
    client = BridgeClient()

    print_header("Health Check")
    health = client.health()
    print(f"  Status: {health['status']}")
    print(f"  World initialized: {health['world_initialized']}")

    if not health['world_initialized']:
        print("\n  ⚠️  World not initialized. Run server with --auto-init")
        return

    print_header("Current Status")
    status = client.status()

    cloud = status["cloud"]
    print_cloud(cloud)

    print(f"\n  Zones: {status['zones_count']}")
    print(f"  NPCs: {status['npcs_count']}")
    print(f"\n  Session:")
    print(f"    Count: {status['session']['count']}")
    print(f"    Playtime: {status['session']['total_playtime']:.1f}s ({status['session']['total_playtime']/60:.1f}m)")
    print(f"\n  Stats:")
    print(f"    Discoveries: {status['stats']['discoveries']}")
    print(f"    Contradictions: {status['stats']['contradictions']}")
    print(f"    Entities loaded: {status['stats']['entities_loaded']}")


def demo_single_tick():
    """Run a single tick with demo player action."""
    client = BridgeClient()

    print_header("Single Tick Demo")

    # Check health
    health = client.health()
    if not health['world_initialized']:
        print("  ⚠️  World not initialized. Run server with --auto-init")
        return

    # Demo player action
    player_event = {
        "type": "move",
        "to_zone": "FC-ARCADE",
        "from_zone": "CORRIDOR"
    }

    print(f"  Player action: {player_event['type']} to {player_event['to_zone']}")

    # Tick
    frame = client.tick(dt=0.25, player_event=player_event)

    # Display results
    print_cloud(frame["cloud"])
    print_npcs(frame["npcs"], max_show=5)
    print_events(frame["events"])
    print_top_zones(frame["zones"], max_show=3)


def demo_loop(iterations: int = 20, delay: float = 0.5):
    """Run tick loop with varying player actions."""
    client = BridgeClient()

    print_header("Loop Demo")

    # Check health
    health = client.health()
    if not health['world_initialized']:
        print("  ⚠️  World not initialized. Run server with --auto-init")
        return

    print(f"  Running {iterations} ticks with {delay}s delay between each")
    print(f"  Press Ctrl+C to stop\n")

    # Possible player actions
    actions = [
        {"type": "wait"},
        {"type": "move", "to_zone": "FC-ARCADE", "from_zone": "CORRIDOR"},
        {"type": "move", "to_zone": "SERVICE_HALL", "from_zone": "FC-ARCADE"},
        {"type": "interact", "target": "bag_of_screams", "zone": "FC-ARCADE"},
        {"type": "discover", "document": "log_017", "zone": "SERVICE_HALL"},
        {"type": "run", "zone": "CORRIDOR"},
    ]

    try:
        for i in range(iterations):
            # Cycle through actions
            player_event = actions[i % len(actions)]

            # Tick
            frame = client.tick(dt=0.25, player_event=player_event)

            # Display
            print(f"\n[Tick {i+1}/{iterations}]")

            # Player action summary
            if player_event["type"] == "move":
                print(f"  Action: {player_event['type']} → {player_event['to_zone']}")
            elif player_event["type"] == "interact":
                print(f"  Action: {player_event['type']} with {player_event['target']}")
            elif player_event["type"] == "discover":
                print(f"  Action: {player_event['type']} {player_event['document']}")
            else:
                print(f"  Action: {player_event['type']}")

            print_cloud(frame["cloud"])

            # Show top 2 NPCs with interesting states
            interesting_npcs = [
                npc for npc in frame["npcs"]
                if npc["state"] not in ["idle"]
            ]
            if not interesting_npcs:
                interesting_npcs = frame["npcs"][:2]

            print_npcs(interesting_npcs, max_show=2)

            # Show events
            if frame["events"]:
                print_events(frame["events"])

            time.sleep(delay)

    except KeyboardInterrupt:
        print("\n\n  Stopped by user")


def demo_reset():
    """Reset world state."""
    client = BridgeClient()

    print_header("Reset Demo")

    # Show current state
    print("\n  Current state:")
    status = client.status()
    print_cloud(status["cloud"])

    # Reset
    print("\n  Resetting world (keep_memory=False)...")
    result = client.reset(keep_memory=False)

    print(f"  Status: {result['status']}")
    print(f"  Cloud level: {result['cloud_level']}")

    # Show new state
    print("\n  After reset:")
    status = client.status()
    print_cloud(status["cloud"])


def main():
    parser = argparse.ArgumentParser(description="V6 Bridge CLI Demo Client")
    parser.add_argument(
        "--url",
        default=BASE_URL,
        help=f"Bridge server URL (default: {BASE_URL})"
    )
    parser.add_argument(
        "--status-only",
        action="store_true",
        help="Just show current status"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run single tick and exit"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset world state"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=20,
        help="Number of ticks in loop mode (default: 20)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between ticks in seconds (default: 0.5)"
    )

    args = parser.parse_args()

    # Update base URL
    global BASE_URL
    BASE_URL = args.url

    print(f"\n{'='*60}")
    print(f"  V6 BRIDGE CLI DEMO")
    print(f"{'='*60}")
    print(f"  Server: {BASE_URL}")

    try:
        if args.status_only:
            demo_status_only()
        elif args.once:
            demo_single_tick()
        elif args.reset:
            demo_reset()
        else:
            demo_loop(iterations=args.iterations, delay=args.delay)

    except requests.exceptions.ConnectionError:
        print(f"\n  ✗ Cannot connect to bridge server at {BASE_URL}")
        print(f"  Make sure the server is running:")
        print(f"    python bridge_server.py --auto-init")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"\n  ✗ HTTP Error: {e}")
        if e.response is not None:
            try:
                error_data = e.response.json()
                print(f"  {error_data.get('error', 'Unknown error')}")
            except:
                pass
        sys.exit(1)
    except Exception as e:
        print(f"\n  ✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  Demo complete")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
