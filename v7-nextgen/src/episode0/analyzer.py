#!/usr/bin/env python3
"""
Episode 0 Analyzer - Zone Palettes & Motion Heatmaps

Analyzes processed Episode 0 data to extract:
- Zone motion heatmaps (where does motion occur per zone)
- Zone color palettes (dominant colors via K-means)
- Geometry validation (compare motion patterns with voxel builder)

Input:
- Voxels .npy file (from processor.py)
- Zone timeline .json (from annotator.py)
- Original video (for palette extraction)

Output:
- Zone heatmaps (PNG visualizations)
- Zone palettes (JSON with hex colors)
- Validation report (JSON comparing motion vs geometry)
"""

import cv2
import numpy as np
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from sklearn.cluster import KMeans
import sys


class Episode0Analyzer:
    """
    Analyze Episode 0 canonical reference for zone-specific data.

    Args:
        voxels_path: Path to .npy voxel file (from processor)
        timeline_path: Path to timeline.json (from annotator)
        video_path: Path to original video (for palette extraction)
        output_dir: Directory for output files (default: data/episode0/analysis)
    """

    def __init__(
        self,
        voxels_path: str,
        timeline_path: str,
        video_path: str,
        output_dir: str = "../../data/episode0/analysis"
    ):
        self.voxels_path = Path(voxels_path)
        self.timeline_path = Path(timeline_path)
        self.video_path = Path(video_path)

        # Resolve output_dir relative to this file
        self.output_dir = Path(__file__).parent / output_dir
        self.output_dir = self.output_dir.resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load data
        if not self.voxels_path.exists():
            raise FileNotFoundError(f"Voxels not found: {self.voxels_path}")
        if not self.timeline_path.exists():
            raise FileNotFoundError(f"Timeline not found: {self.timeline_path}")
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {self.video_path}")

        print(f"Loading Episode 0 data...")
        self.voxels = np.load(self.voxels_path)
        print(f"  Voxels: {self.voxels.shape}")

        with open(self.timeline_path) as f:
            timeline_data = json.load(f)
            self.zones_timeline = timeline_data.get("zones_timeline", [])
            self.fps = timeline_data.get("fps", 5)  # Try to get fps from timeline
            self.clip_id = timeline_data.get("clip_id", "episode0")

        print(f"  Timeline: {len(self.zones_timeline)} zones")
        print(f"  FPS: {self.fps}")
        print()

    def analyze_all_zones(self, palette_colors: int = 5) -> Dict:
        """
        Run full analysis pipeline for all zones.

        Args:
            palette_colors: Number of dominant colors to extract per zone

        Returns:
            analysis_data dict with paths to outputs
        """
        print(f"\n{'='*60}")
        print(f"  Episode 0 Zone Analysis")
        print(f"  Clip: {self.clip_id}")
        print(f"{'='*60}\n")

        analysis_results = {
            "clip_id": self.clip_id,
            "num_zones": len(self.zones_timeline),
            "zones": []
        }

        for i, zone in enumerate(self.zones_timeline):
            zone_id = zone["zone_id"]
            print(f"[{i+1}/{len(self.zones_timeline)}] Analyzing {zone_id}...")

            zone_result = {
                "zone_id": zone_id,
                "start_s": zone["start_s"],
                "end_s": zone["end_s"],
                "duration_s": zone["duration_s"]
            }

            # 1. Extract motion heatmap
            print(f"  [1/2] Computing motion heatmap...")
            heatmap = self.extract_zone_motion_heatmap(zone)
            heatmap_path = self._save_heatmap(heatmap, zone_id)
            zone_result["heatmap_path"] = str(heatmap_path)
            print(f"    ✓ Saved: {heatmap_path.name}")

            # 2. Extract color palette
            print(f"  [2/2] Extracting color palette...")
            palette = self.extract_zone_palette(zone, num_colors=palette_colors)
            zone_result["palette"] = palette
            print(f"    ✓ {len(palette)} colors extracted")

            analysis_results["zones"].append(zone_result)
            print()

        # Save analysis results
        output_path = self.output_dir / f"{self.clip_id}_analysis.json"
        with open(output_path, 'w') as f:
            json.dump(analysis_results, f, indent=2)

        print(f"{'='*60}")
        print(f"  Analysis complete!")
        print(f"  Output: {output_path}")
        print(f"{'='*60}\n")

        return analysis_results

    def extract_zone_motion_heatmap(self, zone: Dict) -> np.ndarray:
        """
        Accumulate motion over zone duration into 2D heatmap.

        Args:
            zone: Zone dict with start_s, end_s

        Returns:
            heatmap: (height, width) normalized 0-255 intensity map
        """
        # Convert time to frame indices
        start_frame = int(zone["start_s"] * self.fps)
        end_frame = int(zone["end_s"] * self.fps)

        # Clamp to voxel bounds
        start_frame = max(0, start_frame)
        end_frame = min(len(self.voxels), end_frame)

        if start_frame >= end_frame:
            # Empty zone, return zeros
            return np.zeros(self.voxels.shape[1:], dtype=np.uint8)

        # Extract zone voxel slice
        zone_voxels = self.voxels[start_frame:end_frame]

        # Accumulate motion over time (sum across T axis)
        heatmap = np.sum(zone_voxels, axis=0).astype(float)

        # Normalize to 0-255
        if heatmap.max() > 0:
            heatmap = (heatmap / heatmap.max() * 255).astype(np.uint8)
        else:
            heatmap = heatmap.astype(np.uint8)

        return heatmap

    def extract_zone_palette(self, zone: Dict, num_colors: int = 5) -> List[Dict]:
        """
        Extract dominant colors from zone using K-means clustering.

        Args:
            zone: Zone dict with start_s, end_s
            num_colors: Number of dominant colors to extract

        Returns:
            palette: List of {"hex": "#rrggbb", "rgb": [r, g, b], "weight": 0.0-1.0}
        """
        cap = cv2.VideoCapture(str(self.video_path))

        # Get original video fps (might differ from processed fps)
        video_fps = cap.get(cv2.CAP_PROP_FPS)

        # Convert zone time to video frame indices
        start_frame = int(zone["start_s"] * video_fps)
        end_frame = int(zone["end_s"] * video_fps)

        # Sample frames from zone (max 30 frames to avoid memory issues)
        num_samples = min(30, end_frame - start_frame)
        sample_indices = np.linspace(start_frame, end_frame - 1, num_samples, dtype=int)

        pixels = []

        for frame_idx in sample_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                continue

            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Downsample for speed (use every 4th pixel)
            sampled = rgb_frame[::4, ::4].reshape(-1, 3)
            pixels.append(sampled)

        cap.release()

        if not pixels:
            # Failed to extract frames, return empty palette
            return []

        # Combine all pixels
        all_pixels = np.vstack(pixels)

        # K-means clustering
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(all_pixels)

        # Get cluster centers (dominant colors)
        colors = kmeans.cluster_centers_.astype(int)

        # Get cluster sizes (color weights)
        labels = kmeans.labels_
        unique, counts = np.unique(labels, return_counts=True)
        weights = counts / counts.sum()

        # Build palette
        palette = []
        for i, (color, weight) in enumerate(zip(colors, weights)):
            r, g, b = color
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            palette.append({
                "hex": hex_color,
                "rgb": [int(r), int(g), int(b)],
                "weight": float(weight)
            })

        # Sort by weight (most dominant first)
        palette.sort(key=lambda x: x["weight"], reverse=True)

        return palette

    def _save_heatmap(self, heatmap: np.ndarray, zone_id: str) -> Path:
        """
        Save motion heatmap as colorized PNG.

        Args:
            heatmap: (height, width) grayscale intensity
            zone_id: Zone identifier

        Returns:
            path to saved heatmap PNG
        """
        heatmap_dir = self.output_dir / "heatmaps"
        heatmap_dir.mkdir(exist_ok=True)

        # Apply colormap (TURBO for better visibility)
        colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_TURBO)

        # Upscale for visibility (32x18 → 640x360)
        scale_factor = 20
        upscaled = cv2.resize(colored, None, fx=scale_factor, fy=scale_factor,
                             interpolation=cv2.INTER_NEAREST)

        # Add legend
        legend_height = 40
        display = np.zeros((upscaled.shape[0] + legend_height, upscaled.shape[1], 3),
                          dtype=np.uint8)
        display[:upscaled.shape[0]] = upscaled

        # Add zone label
        cv2.putText(display, f"Zone: {zone_id}", (10, upscaled.shape[0] + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Add color scale
        scale_bar = np.linspace(0, 255, 200).astype(np.uint8).reshape(1, -1)
        scale_bar = np.repeat(scale_bar, 10, axis=0)
        scale_colored = cv2.applyColorMap(scale_bar, cv2.COLORMAP_TURBO)

        # Place scale bar
        scale_x = display.shape[1] - 220
        scale_y = upscaled.shape[0] + 10
        display[scale_y:scale_y+10, scale_x:scale_x+200] = scale_colored

        # Labels
        cv2.putText(display, "Low", (scale_x - 35, scale_y + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        cv2.putText(display, "High", (scale_x + 205, scale_y + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

        # Save
        output_path = heatmap_dir / f"{self.clip_id}_{zone_id}_heatmap.png"
        cv2.imwrite(str(output_path), display)

        return output_path

    def validate_geometry(self, voxel_builder_output: Optional[Dict] = None) -> Dict:
        """
        Compare Episode 0 motion patterns with voxel builder geometry.

        Args:
            voxel_builder_output: Optional dict from VoxelBuilder.build_full_mall()

        Returns:
            validation_report: Dict with coverage, discrepancies, confidence
        """
        # Placeholder for geometry validation
        # This would compare motion heatmaps with expected walkable areas
        # from the voxel builder's zone geometry

        print(f"[Geometry Validation] Not yet implemented")
        print(f"  Future: Compare motion heatmaps with VoxelBuilder zone masks")
        print(f"  Purpose: Validate that cameraman stayed in walkable areas")
        print()

        return {
            "status": "not_implemented",
            "note": "Compare motion patterns with voxel builder geometry"
        }


def main():
    """CLI for Episode 0 analyzer."""
    import argparse

    parser = argparse.ArgumentParser(description="Episode 0 Zone Analyzer")
    parser.add_argument("--voxels", required=True, help="Path to voxels .npy file")
    parser.add_argument("--timeline", required=True, help="Path to timeline.json")
    parser.add_argument("--video", required=True, help="Path to original video")
    parser.add_argument("--output", default="../../data/episode0/analysis",
                       help="Output directory")
    parser.add_argument("--colors", type=int, default=5,
                       help="Number of palette colors per zone (default: 5)")

    args = parser.parse_args()

    # Create analyzer
    analyzer = Episode0Analyzer(
        voxels_path=args.voxels,
        timeline_path=args.timeline,
        video_path=args.video,
        output_dir=args.output
    )

    # Run analysis
    results = analyzer.analyze_all_zones(palette_colors=args.colors)

    print("\nNext steps:")
    print(f"  1. Review heatmaps in: {analyzer.output_dir}/heatmaps/")
    print(f"  2. Use palettes for zone rendering")
    print(f"  3. Generate NPC patrol routes:")
    print(f"     python -m episode0.path --timeline {args.timeline} --output {args.output}/patrol_routes.json")


if __name__ == "__main__":
    main()
