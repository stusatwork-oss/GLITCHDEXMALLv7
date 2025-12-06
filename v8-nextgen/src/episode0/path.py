#!/usr/bin/env python3
"""
Episode 0 Path - NPC Patrol Route Generator

Converts Episode 0 zone timeline into NPC patrol routes.

The cameraman's path through the mall becomes the Janitor's canonical patrol.

Input:
- Zone timeline .json (from annotator.py)
- Optional: Zone centroids from voxel builder

Output:
- Patrol route JSON with timed waypoints
- Compatible with v7_integrated_demo.py

Usage:
    from episode0 import Episode0Path

    path_gen = Episode0Path("timeline.json")
    patrol_route = path_gen.generate_patrol_route()
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import sys


# Default zone centroids (approx positions in mall coordinate system)
# These match the voxel builder's zone layout
DEFAULT_ZONE_CENTROIDS = {
    "Z1_CENTRAL_ATRIUM": (0, 0, 0),
    "Z2_FOOD_COURT": (50, 0, -30),
    "Z3_ARCADE": (80, 0, -20),
    "Z4_SERVICE_CORRIDOR": (-20, 0, 15),
    "Z5_FOUNTAIN_COURT": (0, 0, 30),
    "Z6_ESCALATOR_LOBBY": (25, 5, 0),
    "Z7_RESTROOM_HALL": (-30, 0, -10),
    "Z8_LOADING_DOCK": (-40, 0, 25),

    # Abbreviated zone IDs (common in annotations)
    "ATRIUM": (0, 0, 0),
    "FOOD_COURT": (50, 0, -30),
    "FC-ARCADE": (80, 0, -20),
    "ARCADE": (80, 0, -20),
    "SERVICE_HALL": (-20, 0, 15),
    "SERVICE_CORRIDOR": (-20, 0, 15),
    "FOUNTAIN": (0, 0, 30),
    "ESCALATOR": (25, 5, 0),
    "RESTROOMS": (-30, 0, -10),
    "LOADING": (-40, 0, 25),
    "ENTRANCE": (-10, 0, -40),
}


class Episode0Path:
    """
    Convert Episode 0 zone timeline into NPC patrol routes.

    Args:
        timeline_path: Path to timeline.json (from annotator)
        zone_centroids: Optional dict mapping zone_id → (x, y, z) position
    """

    def __init__(
        self,
        timeline_path: str,
        zone_centroids: Optional[Dict[str, Tuple[float, float, float]]] = None
    ):
        self.timeline_path = Path(timeline_path)

        if not self.timeline_path.exists():
            raise FileNotFoundError(f"Timeline not found: {self.timeline_path}")

        # Load timeline
        with open(self.timeline_path) as f:
            timeline_data = json.load(f)
            self.zones_timeline = timeline_data.get("zones_timeline", [])
            self.clip_id = timeline_data.get("clip_id", "episode0")
            self.duration_s = timeline_data.get("duration_s", 0)

        # Zone centroids (use default or provided)
        self.zone_centroids = zone_centroids if zone_centroids else DEFAULT_ZONE_CENTROIDS

        print(f"Loaded timeline: {self.clip_id}")
        print(f"  Zones: {len(self.zones_timeline)}")
        print(f"  Duration: {self.duration_s:.1f}s ({self.duration_s/60:.1f} min)")
        print()

    def generate_patrol_route(
        self,
        interpolate: bool = True,
        speed_mps: float = 1.0
    ) -> Dict:
        """
        Generate NPC patrol route from zone timeline.

        Args:
            interpolate: If True, add intermediate waypoints between zones
            speed_mps: NPC movement speed in meters/second (for timing)

        Returns:
            patrol_route dict with waypoints and metadata
        """
        print(f"{'='*60}")
        print(f"  Generating Patrol Route")
        print(f"  Clip: {self.clip_id}")
        print(f"{'='*60}\n")

        waypoints = []

        for i, zone in enumerate(self.zones_timeline):
            zone_id = zone["zone_id"]
            start_s = zone["start_s"]
            end_s = zone["end_s"]
            duration_s = zone["duration_s"]

            # Get zone position
            position = self.zone_centroids.get(zone_id)

            if position is None:
                print(f"[WARNING] Zone '{zone_id}' not in centroid map, skipping")
                continue

            # Add waypoint at zone entry
            waypoints.append({
                "time_s": start_s,
                "position": list(position),
                "zone_id": zone_id,
                "event": "zone_entry"
            })

            # Add waypoint at zone exit (if different from next entry)
            if i < len(self.zones_timeline) - 1:
                # Stay in zone until transition
                waypoints.append({
                    "time_s": end_s,
                    "position": list(position),
                    "zone_id": zone_id,
                    "event": "zone_exit"
                })
            else:
                # Last zone, add final waypoint
                waypoints.append({
                    "time_s": end_s,
                    "position": list(position),
                    "zone_id": zone_id,
                    "event": "patrol_end"
                })

        # Optional: Interpolate path
        if interpolate and len(waypoints) > 1:
            waypoints = self._interpolate_waypoints(waypoints, speed_mps)

        patrol_route = {
            "clip_id": self.clip_id,
            "duration_s": self.duration_s,
            "num_waypoints": len(waypoints),
            "waypoints": waypoints,
            "metadata": {
                "generated_from": str(self.timeline_path),
                "interpolated": interpolate,
                "speed_mps": speed_mps
            }
        }

        print(f"✓ Generated {len(waypoints)} waypoints")
        print(f"  Duration: {self.duration_s:.1f}s")
        print(f"  Interpolated: {interpolate}")
        print()

        return patrol_route

    def _interpolate_waypoints(
        self,
        waypoints: List[Dict],
        speed_mps: float
    ) -> List[Dict]:
        """
        Add intermediate waypoints for smooth transitions.

        Args:
            waypoints: Original zone entry/exit waypoints
            speed_mps: Movement speed for timing

        Returns:
            interpolated waypoints with transition points
        """
        interpolated = []

        for i in range(len(waypoints) - 1):
            current = waypoints[i]
            next_wp = waypoints[i + 1]

            # Add current waypoint
            interpolated.append(current)

            # Check if zone transition
            if current["zone_id"] != next_wp["zone_id"]:
                # Calculate midpoint between zones
                curr_pos = current["position"]
                next_pos = next_wp["position"]

                mid_pos = [
                    (curr_pos[0] + next_pos[0]) / 2,
                    (curr_pos[1] + next_pos[1]) / 2,
                    (curr_pos[2] + next_pos[2]) / 2
                ]

                # Time at midpoint (average of transition times)
                mid_time = (current["time_s"] + next_wp["time_s"]) / 2

                # Add transition waypoint
                interpolated.append({
                    "time_s": mid_time,
                    "position": mid_pos,
                    "zone_id": f"{current['zone_id']}→{next_wp['zone_id']}",
                    "event": "zone_transition"
                })

        # Add final waypoint
        interpolated.append(waypoints[-1])

        return interpolated

    def save_patrol_route(self, patrol_route: Dict, output_path: str):
        """
        Save patrol route to JSON file.

        Args:
            patrol_route: Route dict from generate_patrol_route()
            output_path: Path to output JSON file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(patrol_route, f, indent=2)

        print(f"✓ Saved patrol route: {output_path}")

    def visualize_route(self, patrol_route: Dict):
        """
        Print ASCII visualization of patrol route.

        Args:
            patrol_route: Route dict from generate_patrol_route()
        """
        print(f"\n{'='*60}")
        print(f"  Patrol Route Visualization")
        print(f"{'='*60}\n")

        for i, wp in enumerate(patrol_route["waypoints"]):
            time_s = wp["time_s"]
            zone = wp["zone_id"]
            pos = wp["position"]
            event = wp.get("event", "waypoint")

            # Format time
            minutes = int(time_s // 60)
            seconds = int(time_s % 60)

            # Event symbol
            symbol = {
                "zone_entry": "→",
                "zone_exit": "←",
                "zone_transition": "↔",
                "patrol_end": "■"
            }.get(event, "·")

            print(f"  {i:3d} {symbol} {minutes:02d}:{seconds:02d}  {zone:30s}  "
                  f"({pos[0]:6.1f}, {pos[1]:6.1f}, {pos[2]:6.1f})")

        print(f"\n{'='*60}\n")


def main():
    """CLI for Episode 0 path generator."""
    import argparse

    parser = argparse.ArgumentParser(description="Episode 0 Patrol Route Generator")
    parser.add_argument("--timeline", required=True, help="Path to timeline.json")
    parser.add_argument("--output", required=True, help="Output patrol route JSON path")
    parser.add_argument("--no-interpolate", action="store_true",
                       help="Disable waypoint interpolation")
    parser.add_argument("--speed", type=float, default=1.0,
                       help="NPC movement speed in m/s (default: 1.0)")
    parser.add_argument("--visualize", action="store_true",
                       help="Print ASCII visualization of route")

    args = parser.parse_args()

    # Create path generator
    path_gen = Episode0Path(timeline_path=args.timeline)

    # Generate patrol route
    patrol_route = path_gen.generate_patrol_route(
        interpolate=not args.no_interpolate,
        speed_mps=args.speed
    )

    # Save
    path_gen.save_patrol_route(patrol_route, args.output)

    # Visualize if requested
    if args.visualize:
        path_gen.visualize_route(patrol_route)

    print("\nNext steps:")
    print(f"  1. Load patrol route in v7_integrated_demo:")
    print(f"     from episodes.loader import load_patrol_route")
    print(f"     route = load_patrol_route('{args.output}')")
    print(f"  2. Update Janitor position in sim loop:")
    print(f"     janitor.follow_patrol_route(route, sim_time)")
    print(f"  3. Watch Janitor retrace Episode 0 path while Cloud rises")


if __name__ == "__main__":
    main()
