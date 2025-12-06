#!/usr/bin/env python3
"""
Episode 0 Annotator - Interactive Zone Timeline Tool

Interactive OpenCV-based tool for annotating zone transitions in Episode 0 video.

Controls:
- SPACE: Pause/play
- Z: Mark zone boundary (prompts for zone ID)
- B: Go back 5 seconds
- F: Go forward 5 seconds
- S: Save current timeline
- Q: Quit

Output:
- timeline.json with zone boundaries and IDs
"""

import cv2
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional


class Episode0Annotator:
    """
    Interactive tool for annotating zone timeline.

    Usage:
        annotator = Episode0Annotator("video.mp4", "timeline.json")
        annotator.run()
    """

    def __init__(self, video_path: str, output_path: str):
        self.video_path = Path(video_path)
        self.output_path = Path(output_path)

        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {self.video_path}")

        self.zones_timeline: List[Dict] = []
        self.current_time = 0.0
        self.last_zone_end = 0.0

        self.cap = None
        self.fps = 0
        self.total_frames = 0
        self.duration = 0

        # Load existing timeline if present
        if self.output_path.exists():
            self._load_timeline()

    def _load_timeline(self):
        """Load existing timeline."""
        with open(self.output_path) as f:
            data = json.load(f)
            self.zones_timeline = data.get("zones_timeline", [])
            if self.zones_timeline:
                self.last_zone_end = self.zones_timeline[-1]["end_s"]

        print(f"Loaded existing timeline: {len(self.zones_timeline)} zones")
        for zone in self.zones_timeline:
            print(f"  {zone['zone_id']}: {zone['start_s']:.1f}s - {zone['end_s']:.1f}s")
        print()

    def run(self):
        """
        Run interactive annotation session.
        """
        self.cap = cv2.VideoCapture(str(self.video_path))

        if not self.cap.isOpened():
            print(f"Error: Could not open video: {self.video_path}")
            return

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.total_frames / self.fps

        print(f"\n{'='*60}")
        print(f"  Episode 0 Annotator")
        print(f"  Video: {self.video_path.name}")
        print(f"  Duration: {self.duration:.1f}s ({self.duration/60:.1f} min)")
        print(f"  FPS: {self.fps:.2f}")
        print(f"{'='*60}")
        print()
        print("Controls:")
        print("  SPACE - Pause/play")
        print("  Z     - Mark zone boundary")
        print("  B     - Back 5 seconds")
        print("  F     - Forward 5 seconds")
        print("  S     - Save timeline")
        print("  Q     - Quit")
        print()

        # Seek to last zone end if continuing
        if self.last_zone_end > 0:
            self.cap.set(cv2.CAP_PROP_POS_MSEC, self.last_zone_end * 1000)
            print(f"Resuming from {self.last_zone_end:.1f}s")
            print()

        paused = True  # Start paused

        while True:
            if not paused:
                ret, frame = self.cap.read()
                if not ret:
                    print("\nEnd of video reached")
                    break

                self.current_time = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            else:
                # Re-read current frame when paused
                current_pos = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, current_pos - 1)
                ret, frame = self.cap.read()
                if not ret:
                    break
                self.current_time = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

            # Create display
            display = self._create_display(frame)

            cv2.imshow("Episode 0 Annotator", display)

            # Handle keys
            wait_time = 1 if paused else int(1000 / self.fps)
            key = cv2.waitKey(wait_time) & 0xFF

            if key == ord(' '):
                paused = not paused
                status = "PAUSED" if paused else "PLAYING"
                print(f"\r[{status}] Time: {self.current_time:.1f}s", end='')

            elif key == ord('z'):
                self._mark_zone_boundary()
                paused = True  # Pause after marking

            elif key == ord('b'):
                # Back 5 seconds
                new_time = max(0, self.current_time - 5.0)
                self.cap.set(cv2.CAP_PROP_POS_MSEC, new_time * 1000)
                print(f"\r← Back to {new_time:.1f}s", end='')

            elif key == ord('f'):
                # Forward 5 seconds
                new_time = min(self.duration, self.current_time + 5.0)
                self.cap.set(cv2.CAP_PROP_POS_MSEC, new_time * 1000)
                print(f"\r→ Forward to {new_time:.1f}s", end='')

            elif key == ord('s'):
                self.save_timeline()
                print(f"\r✓ Saved timeline ({len(self.zones_timeline)} zones)", end='')

            elif key == ord('q'):
                print("\nQuitting...")
                break

        self.cap.release()
        cv2.destroyAllWindows()

        # Auto-save on exit
        if self.zones_timeline:
            self.save_timeline()
            print(f"\n✓ Final save: {len(self.zones_timeline)} zones")

    def _create_display(self, frame):
        """Create display frame with overlay."""
        display = frame.copy()
        h, w = display.shape[:2]

        # Add black bar at top for info
        cv2.rectangle(display, (0, 0), (w, 60), (0, 0, 0), -1)

        # Time info
        time_str = f"Time: {self.current_time:.1f}s / {self.duration:.1f}s"
        cv2.putText(display, time_str, (10, 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Current zone info
        if self.zones_timeline:
            last_zone = self.zones_timeline[-1]
            zone_str = f"Last: {last_zone['zone_id']} (ended {last_zone['end_s']:.1f}s)"
            cv2.putText(display, zone_str, (10, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        else:
            cv2.putText(display, "No zones marked yet", (10, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        # Timeline bar
        if self.duration > 0:
            bar_width = w - 20
            bar_x = 10
            bar_y = h - 30
            bar_height = 10

            # Background
            cv2.rectangle(display, (bar_x, bar_y),
                         (bar_x + bar_width, bar_y + bar_height),
                         (50, 50, 50), -1)

            # Progress
            progress = int((self.current_time / self.duration) * bar_width)
            cv2.rectangle(display, (bar_x, bar_y),
                         (bar_x + progress, bar_y + bar_height),
                         (0, 255, 0), -1)

            # Zone markers
            for zone in self.zones_timeline:
                marker_x = bar_x + int((zone['start_s'] / self.duration) * bar_width)
                cv2.line(display, (marker_x, bar_y), (marker_x, bar_y + bar_height),
                        (0, 255, 255), 2)

        return display

    def _mark_zone_boundary(self):
        """Mark a zone boundary."""
        print(f"\n\n{'='*60}")
        print(f"Mark Zone Boundary")
        print(f"  Start: {self.last_zone_end:.1f}s")
        print(f"  End:   {self.current_time:.1f}s")
        print(f"  Duration: {self.current_time - self.last_zone_end:.1f}s")
        print(f"{'='*60}")

        zone_id = input("Enter zone ID (or press Enter to cancel): ").strip().upper()

        if not zone_id:
            print("Cancelled")
            return

        # Add zone
        self.zones_timeline.append({
            "start_s": self.last_zone_end,
            "end_s": self.current_time,
            "zone_id": zone_id,
            "duration_s": self.current_time - self.last_zone_end
        })

        self.last_zone_end = self.current_time

        print(f"✓ Added: {zone_id}")
        print(f"  Total zones: {len(self.zones_timeline)}")
        print()

    def save_timeline(self):
        """Save annotated zone timeline."""
        timeline_data = {
            "clip_id": self.video_path.stem,
            "source_video": str(self.video_path),
            "duration_s": self.duration,
            "num_zones": len(self.zones_timeline),
            "zones_timeline": self.zones_timeline
        }

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, 'w') as f:
            json.dump(timeline_data, f, indent=2)

        print(f"\n✓ Saved timeline to: {self.output_path}")


def main():
    """CLI for Episode 0 annotator."""
    import argparse

    parser = argparse.ArgumentParser(description="Episode 0 Zone Timeline Annotator")
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument("--output", required=True, help="Output timeline.json path")

    args = parser.parse_args()

    annotator = Episode0Annotator(args.video, args.output)
    annotator.run()


if __name__ == "__main__":
    main()
