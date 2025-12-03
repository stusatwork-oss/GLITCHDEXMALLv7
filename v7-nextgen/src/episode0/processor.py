#!/usr/bin/env python3
"""
Episode 0 Processor - Frame Extraction & Motion Voxels

Processes walkthrough video into:
- Downsampled frames (5-10 fps)
- Frame differences (motion detection)
- Sparse voxel grid (X, Y, T)

Output:
- .npy file: (T, Y, X) motion voxels
- .json metadata: fps, dimensions, thresholds
"""

import cv2
import numpy as np
import json
from pathlib import Path
from typing import Tuple, Optional, Dict
import sys


class Episode0Processor:
    """
    Process walkthrough video into Episode 0 canonical reference.

    Args:
        video_path: Path to input video
        output_dir: Directory for output files (default: data/episode0)
        target_fps: Downsample to this fps (default: 5)
        grid_size: Spatial grid dimensions (width, height) (default: 32x18)
        diff_threshold: Motion detection threshold 0-255 (default: 20)
    """

    def __init__(
        self,
        video_path: str,
        output_dir: str = "../../data/episode0",
        target_fps: int = 5,
        grid_size: Tuple[int, int] = (32, 18),
        diff_threshold: int = 20
    ):
        self.video_path = Path(video_path)

        # Resolve output_dir relative to this file
        self.output_dir = Path(__file__).parent / output_dir
        self.output_dir = self.output_dir.resolve()

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Config
        self.target_fps = target_fps
        self.grid_size = grid_size  # (width, height)
        self.diff_threshold = diff_threshold

        # Video info (populated on load)
        self.original_fps = None
        self.total_frames = None
        self.duration_s = None

        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {self.video_path}")

    def process(self, clip_id: Optional[str] = None) -> Dict:
        """
        Full processing pipeline.

        Returns:
            metadata dict with paths to outputs
        """
        if clip_id is None:
            clip_id = self.video_path.stem

        print(f"\n{'='*60}")
        print(f"  Episode 0 Processor")
        print(f"  Video: {self.video_path.name}")
        print(f"  Clip ID: {clip_id}")
        print(f"{'='*60}\n")

        # Step 1: Load video info
        self._load_video_info()

        # Step 2: Extract frames
        print(f"[1/3] Extracting frames...")
        print(f"  Target FPS: {self.target_fps}")
        print(f"  Grid size: {self.grid_size[0]}x{self.grid_size[1]}")
        frames = self.extract_frames()
        print(f"  ✓ Extracted {len(frames)} frames")

        # Step 3: Compute motion voxels
        print(f"\n[2/3] Computing motion voxels...")
        print(f"  Diff threshold: {self.diff_threshold}")
        voxels = self.compute_motion_voxels(frames)
        print(f"  ✓ Generated voxel grid: {voxels.shape}")

        # Step 4: Save outputs
        print(f"\n[3/3] Saving outputs...")
        metadata = self.save_voxels(voxels, clip_id)

        # Save sample frames for visualization
        self._save_sample_frames(frames, clip_id, num_samples=10)

        print(f"  ✓ Saved to: {self.output_dir}")
        print(f"\n{'='*60}")
        print(f"  Processing complete!")
        print(f"  Voxels: {metadata['voxels_path']}")
        print(f"  Metadata: {metadata['metadata_path']}")
        print(f"{'='*60}\n")

        return metadata

    def _load_video_info(self):
        """Load video metadata."""
        cap = cv2.VideoCapture(str(self.video_path))

        self.original_fps = cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration_s = self.total_frames / self.original_fps

        cap.release()

        print(f"Video info:")
        print(f"  FPS: {self.original_fps:.2f}")
        print(f"  Frames: {self.total_frames}")
        print(f"  Duration: {self.duration_s:.1f}s ({self.duration_s/60:.1f} min)")
        print()

    def extract_frames(self) -> np.ndarray:
        """
        Extract downsampled frames from video.

        Returns:
            (num_frames, height, width) grayscale frames
        """
        cap = cv2.VideoCapture(str(self.video_path))

        frame_skip = max(1, int(self.original_fps / self.target_fps))

        frames = []
        frame_idx = 0

        total_to_extract = int(self.total_frames / frame_skip)
        last_progress = -1

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % frame_skip == 0:
                # Downsample spatially (width x height)
                small = cv2.resize(frame, self.grid_size, interpolation=cv2.INTER_AREA)
                # Convert to grayscale for motion detection
                gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
                frames.append(gray)

                # Progress
                progress = int((frame_idx / self.total_frames) * 100)
                if progress != last_progress and progress % 10 == 0:
                    print(f"  Progress: {progress}%")
                    last_progress = progress

            frame_idx += 1

        cap.release()

        return np.array(frames, dtype=np.uint8)

    def compute_motion_voxels(self, frames: np.ndarray) -> np.ndarray:
        """
        Compute frame differences → motion voxel grid.

        Args:
            frames: (num_frames, height, width) grayscale frames

        Returns:
            voxels: (T, Y, X) array where value = motion intensity (0-255)
        """
        num_frames = len(frames)
        voxels = np.zeros_like(frames, dtype=np.uint8)

        last_progress = -1

        for t in range(1, num_frames):
            # Absolute difference between consecutive frames
            diff = np.abs(frames[t].astype(int) - frames[t-1].astype(int))

            # Threshold: only keep motion above threshold
            motion = np.where(diff > self.diff_threshold, diff, 0)
            voxels[t] = motion.astype(np.uint8)

            # Progress
            progress = int((t / num_frames) * 100)
            if progress != last_progress and progress % 10 == 0:
                print(f"  Progress: {progress}%")
                last_progress = progress

        # Stats
        nonzero_voxels = np.count_nonzero(voxels)
        total_voxels = voxels.size
        sparsity = (1.0 - nonzero_voxels / total_voxels) * 100

        print(f"  Voxel stats:")
        print(f"    Total: {total_voxels:,}")
        print(f"    Nonzero: {nonzero_voxels:,}")
        print(f"    Sparsity: {sparsity:.1f}%")

        return voxels

    def save_voxels(self, voxels: np.ndarray, clip_id: str) -> Dict:
        """
        Save motion voxels + metadata.

        Returns:
            metadata dict
        """
        # Save voxel data
        voxel_path = self.output_dir / f"{clip_id}_voxels.npy"
        np.save(voxel_path, voxels)
        print(f"  ✓ Voxels: {voxel_path}")

        # Build metadata
        metadata = {
            "clip_id": clip_id,
            "source_video": str(self.video_path),
            "fps": self.target_fps,
            "original_fps": self.original_fps,
            "width_cells": self.grid_size[0],
            "height_cells": self.grid_size[1],
            "duration_seconds": len(voxels) / self.target_fps,
            "num_frames": len(voxels),
            "voxels_path": str(voxel_path),
            "voxels_shape": list(voxels.shape),
            "diff_threshold": self.diff_threshold,
            "processing": {
                "grid_size": list(self.grid_size),
                "target_fps": self.target_fps,
                "frame_skip": int(self.original_fps / self.target_fps)
            }
        }

        # Save metadata
        metadata_path = self.output_dir / f"{clip_id}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"  ✓ Metadata: {metadata_path}")

        # Add path to metadata dict for return
        metadata['metadata_path'] = str(metadata_path)

        return metadata

    def _save_sample_frames(self, frames: np.ndarray, clip_id: str, num_samples: int = 10):
        """Save sample frames for visualization."""
        sample_dir = self.output_dir / "samples"
        sample_dir.mkdir(exist_ok=True)

        indices = np.linspace(0, len(frames)-1, num_samples, dtype=int)

        for i, idx in enumerate(indices):
            sample_path = sample_dir / f"{clip_id}_frame_{idx:04d}.png"
            cv2.imwrite(str(sample_path), frames[idx])

        print(f"  ✓ Samples: {sample_dir} ({num_samples} frames)")


def main():
    """CLI for Episode 0 processor."""
    import argparse

    parser = argparse.ArgumentParser(description="Episode 0 Video Processor")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--output", default="../../data/episode0", help="Output directory")
    parser.add_argument("--fps", type=int, default=5, help="Target FPS (default: 5)")
    parser.add_argument("--grid", default="32x18", help="Grid size WxH (default: 32x18)")
    parser.add_argument("--threshold", type=int, default=20, help="Motion threshold (default: 20)")
    parser.add_argument("--clip-id", help="Clip ID (default: video filename)")

    args = parser.parse_args()

    # Parse grid size
    try:
        width, height = map(int, args.grid.lower().split('x'))
        grid_size = (width, height)
    except:
        print(f"Error: Invalid grid size '{args.grid}', expected format: WxH (e.g., 32x18)")
        sys.exit(1)

    # Create processor
    processor = Episode0Processor(
        video_path=args.video,
        output_dir=args.output,
        target_fps=args.fps,
        grid_size=grid_size,
        diff_threshold=args.threshold
    )

    # Process
    metadata = processor.process(clip_id=args.clip_id)

    print("\nNext steps:")
    print(f"  1. Annotate zone timeline:")
    print(f"     python -m episode0.annotator --video {args.video} --output {args.output}/timeline.json")
    print(f"  2. Extract zone palettes:")
    print(f"     python -m episode0.analyzer --voxels {metadata['voxels_path']} --timeline {args.output}/timeline.json --video {args.video}")


if __name__ == "__main__":
    main()
