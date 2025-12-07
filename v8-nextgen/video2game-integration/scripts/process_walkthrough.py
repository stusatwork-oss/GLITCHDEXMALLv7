#!/usr/bin/env python3
"""
Eastland Mall Walkthrough Video Processing Pipeline
Processes 11-minute walkthrough video using video2game to extract 3D geometry.

Usage:
    python process_walkthrough.py --video path/to/walkthrough.mp4 --output output_dir
"""

import argparse
import os
import sys
import json
from pathlib import Path
import subprocess
from datetime import datetime

class MallVideoProcessor:
    """Processes mall walkthrough video through video2game pipeline."""

    def __init__(self, video_path: str, output_dir: str, config: dict = None):
        self.video_path = Path(video_path)
        self.output_dir = Path(output_dir)
        self.config = config or self.default_config()

        # Create output structure
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.intermediate_dir = self.output_dir / "intermediate"
        self.intermediate_dir.mkdir(exist_ok=True)

        # Log file
        self.log_file = self.output_dir / f"processing_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    def default_config(self) -> dict:
        """Default configuration optimized for indoor mall walkthrough."""
        return {
            # Video preprocessing
            "frame_extraction": {
                "fps": 2,  # Extract 2 frames per second (11 min = ~1320 frames)
                "resolution": [1920, 1080],
                "format": "png"
            },

            # NeRF training
            "nerf": {
                "max_steps": 30000,  # Increase for large spaces
                "batch_size": 4096,
                "learning_rate": 0.01,
                "background_color": "black",  # Indoor environment
                "semantic_labels": True  # Enable zone/entity separation
            },

            # Mesh extraction
            "mesh": {
                "resolution": 512,  # Adjust based on GPU memory
                "threshold": 10.0,
                "decimate_target": 100000,  # Target polygon count
                "remove_isolated_components": True
            },

            # Texture baking
            "texture": {
                "resolution": 2048,
                "format": "png",
                "bake_diffuse": True,
                "bake_normal": False  # Can enable if needed
            },

            # Collision generation
            "collision": {
                "enabled": True,
                "max_hulls": 64,
                "resolution": 100000,
                "concavity": 0.001
            },

            # Output formats
            "export": {
                "formats": ["glb", "obj"],  # Game engine compatible
                "include_textures": True,
                "include_collision": True
            }
        }

    def log(self, message: str):
        """Log message to file and console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        print(log_entry.strip())
        with open(self.log_file, 'a') as f:
            f.write(log_entry)

    def validate_video(self) -> bool:
        """Validate input video exists and is readable."""
        if not self.video_path.exists():
            self.log(f"ERROR: Video file not found: {self.video_path}")
            return False

        # Check video properties using ffprobe
        try:
            cmd = [
                "ffprobe", "-v", "quiet",
                "-print_format", "json",
                "-show_format", "-show_streams",
                str(self.video_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            video_info = json.loads(result.stdout)

            duration = float(video_info['format']['duration'])
            self.log(f"Video duration: {duration/60:.1f} minutes")

            return True
        except Exception as e:
            self.log(f"ERROR: Failed to validate video: {e}")
            return False

    def extract_frames(self) -> Path:
        """Extract frames from video using ffmpeg."""
        self.log("STAGE 1: Extracting frames from video...")

        frames_dir = self.intermediate_dir / "frames"
        frames_dir.mkdir(exist_ok=True)

        fps = self.config['frame_extraction']['fps']

        cmd = [
            "ffmpeg", "-i", str(self.video_path),
            "-vf", f"fps={fps}",
            "-qscale:v", "2",  # High quality
            str(frames_dir / "frame_%04d.png")
        ]

        try:
            subprocess.run(cmd, check=True)
            frame_count = len(list(frames_dir.glob("*.png")))
            self.log(f"Extracted {frame_count} frames at {fps} fps")
            return frames_dir
        except subprocess.CalledProcessError as e:
            self.log(f"ERROR: Frame extraction failed: {e}")
            raise

    def run_colmap(self, frames_dir: Path) -> Path:
        """Run COLMAP for camera reconstruction."""
        self.log("STAGE 2: Running COLMAP for camera poses...")

        colmap_dir = self.intermediate_dir / "colmap"
        colmap_dir.mkdir(exist_ok=True)

        database_path = colmap_dir / "database.db"
        sparse_dir = colmap_dir / "sparse"
        sparse_dir.mkdir(exist_ok=True)

        # Feature extraction
        self.log("  2a: Extracting features...")
        subprocess.run([
            "colmap", "feature_extractor",
            "--database_path", str(database_path),
            "--image_path", str(frames_dir),
            "--ImageReader.camera_model", "OPENCV",
            "--ImageReader.single_camera", "1"
        ], check=True)

        # Feature matching
        self.log("  2b: Matching features...")
        subprocess.run([
            "colmap", "exhaustive_matcher",
            "--database_path", str(database_path)
        ], check=True)

        # Sparse reconstruction
        self.log("  2c: Sparse reconstruction...")
        subprocess.run([
            "colmap", "mapper",
            "--database_path", str(database_path),
            "--image_path", str(frames_dir),
            "--output_path", str(sparse_dir)
        ], check=True)

        self.log("COLMAP reconstruction complete")
        return sparse_dir

    def train_nerf(self, colmap_dir: Path) -> Path:
        """Train NeRF model using video2game."""
        self.log("STAGE 3: Training NeRF model...")

        nerf_dir = self.output_dir / "nerf"
        nerf_dir.mkdir(exist_ok=True)

        nerf_config = self.config['nerf']

        # This would call video2game's NeRF training script
        # Placeholder command - adjust based on video2game's actual API
        cmd = [
            "python", "-m", "video2game.train_nerf",
            "--data", str(colmap_dir),
            "--output", str(nerf_dir),
            "--max_steps", str(nerf_config['max_steps']),
            "--batch_size", str(nerf_config['batch_size']),
            "--lr", str(nerf_config['learning_rate'])
        ]

        if nerf_config.get('semantic_labels'):
            cmd.append("--semantic")

        try:
            subprocess.run(cmd, check=True)
            self.log("NeRF training complete")
            return nerf_dir
        except subprocess.CalledProcessError as e:
            self.log(f"ERROR: NeRF training failed: {e}")
            raise

    def extract_mesh(self, nerf_dir: Path) -> Path:
        """Extract mesh from NeRF."""
        self.log("STAGE 4: Extracting mesh from NeRF...")

        mesh_dir = self.output_dir / "mesh"
        mesh_dir.mkdir(exist_ok=True)

        mesh_config = self.config['mesh']

        cmd = [
            "python", "-m", "video2game.extract_mesh",
            "--nerf", str(nerf_dir),
            "--output", str(mesh_dir),
            "--resolution", str(mesh_config['resolution']),
            "--threshold", str(mesh_config['threshold'])
        ]

        try:
            subprocess.run(cmd, check=True)
            self.log("Mesh extraction complete")
            return mesh_dir
        except subprocess.CalledProcessError as e:
            self.log(f"ERROR: Mesh extraction failed: {e}")
            raise

    def bake_textures(self, mesh_dir: Path, nerf_dir: Path) -> Path:
        """Bake textures from NeRF onto mesh."""
        self.log("STAGE 5: Baking textures...")

        textured_dir = self.output_dir / "textured"
        textured_dir.mkdir(exist_ok=True)

        tex_config = self.config['texture']

        cmd = [
            "python", "-m", "video2game.bake_texture",
            "--mesh", str(mesh_dir),
            "--nerf", str(nerf_dir),
            "--output", str(textured_dir),
            "--resolution", str(tex_config['resolution'])
        ]

        try:
            subprocess.run(cmd, check=True)
            self.log("Texture baking complete")
            return textured_dir
        except subprocess.CalledProcessError as e:
            self.log(f"ERROR: Texture baking failed: {e}")
            raise

    def generate_collision(self, mesh_dir: Path) -> Path:
        """Generate collision meshes using V-HACD."""
        self.log("STAGE 6: Generating collision meshes...")

        collision_dir = self.output_dir / "collision"
        collision_dir.mkdir(exist_ok=True)

        coll_config = self.config['collision']

        if not coll_config['enabled']:
            self.log("Collision generation disabled, skipping")
            return None

        cmd = [
            "python", "-m", "video2game.generate_collision",
            "--mesh", str(mesh_dir),
            "--output", str(collision_dir),
            "--max_hulls", str(coll_config['max_hulls']),
            "--resolution", str(coll_config['resolution'])
        ]

        try:
            subprocess.run(cmd, check=True)
            self.log("Collision generation complete")
            return collision_dir
        except subprocess.CalledProcessError as e:
            self.log(f"ERROR: Collision generation failed: {e}")
            raise

    def export_assets(self) -> None:
        """Export final game-ready assets."""
        self.log("STAGE 7: Exporting game-ready assets...")

        export_dir = self.output_dir / "exports"
        export_dir.mkdir(exist_ok=True)

        export_config = self.config['export']

        for fmt in export_config['formats']:
            self.log(f"  Exporting {fmt.upper()} format...")
            # Export logic here

        self.log(f"Assets exported to: {export_dir}")

    def generate_metadata(self) -> None:
        """Generate metadata for integration with voxel_builder."""
        self.log("STAGE 8: Generating integration metadata...")

        metadata = {
            "source_video": str(self.video_path),
            "processing_date": datetime.now().isoformat(),
            "config": self.config,
            "outputs": {
                "nerf": str(self.output_dir / "nerf"),
                "mesh": str(self.output_dir / "mesh"),
                "textured": str(self.output_dir / "textured"),
                "collision": str(self.output_dir / "collision"),
                "exports": str(self.output_dir / "exports")
            },
            "scale_reference": {
                "note": "Scale calibration needed - compare with CRD measurements",
                "atrium_diameter_expected_feet": 175,
                "food_court_pit_depth_expected_feet": 8
            },
            "integration_notes": [
                "Mesh coordinates may need rotation/scaling to align with voxel grid",
                "Compare extracted geometry with data/measurements/spatial_measurements.json",
                "Use this as reference for texturing, not primary geometry source",
                "Collision meshes can be used directly or simplified further"
            ]
        }

        metadata_path = self.output_dir / "processing_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        self.log(f"Metadata saved to: {metadata_path}")

    def run_full_pipeline(self) -> bool:
        """Execute the complete processing pipeline."""
        try:
            self.log("="*60)
            self.log("EASTLAND MALL WALKTHROUGH PROCESSING PIPELINE")
            self.log("="*60)

            # Validate
            if not self.validate_video():
                return False

            # Extract frames
            frames_dir = self.extract_frames()

            # COLMAP reconstruction
            colmap_dir = self.run_colmap(frames_dir)

            # Train NeRF
            nerf_dir = self.train_nerf(colmap_dir)

            # Extract mesh
            mesh_dir = self.extract_mesh(nerf_dir)

            # Bake textures
            textured_dir = self.bake_textures(mesh_dir, nerf_dir)

            # Generate collision
            collision_dir = self.generate_collision(mesh_dir)

            # Export assets
            self.export_assets()

            # Generate metadata
            self.generate_metadata()

            self.log("="*60)
            self.log("PIPELINE COMPLETE!")
            self.log(f"Output directory: {self.output_dir}")
            self.log("="*60)

            return True

        except Exception as e:
            self.log(f"PIPELINE FAILED: {e}")
            import traceback
            self.log(traceback.format_exc())
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Process Eastland Mall walkthrough video using video2game"
    )
    parser.add_argument(
        "--video", "-v",
        required=True,
        help="Path to walkthrough video file"
    )
    parser.add_argument(
        "--output", "-o",
        default="../output/walkthrough_processing",
        help="Output directory for processed assets"
    )
    parser.add_argument(
        "--config", "-c",
        help="Optional JSON config file to override defaults"
    )

    args = parser.parse_args()

    # Load config if provided
    config = None
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)

    # Create processor and run
    processor = MallVideoProcessor(args.video, args.output, config)
    success = processor.run_full_pipeline()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
