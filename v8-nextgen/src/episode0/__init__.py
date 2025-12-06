"""
Episode 0 - Canonical Reference Processor

Treats walkthrough video as "Episode 0" - the canonical reference run for:
- Zone timeline (what you see and when)
- Motion patterns (where things move per zone)
- Visual palettes (actual colors from footage)
- NPC patrol routes (cameraman's path)
- Geometry validation (ground truth for voxel builder)

Pipeline:
1. processor.py - Extract frames, compute motion voxels (X, Y, T)
2. annotator.py - Interactive zone timeline annotation
3. analyzer.py - Extract palettes, heatmaps, validate geometry
4. path.py - Convert to NPC patrol routes

Usage:
    from episode0 import Episode0Processor, Episode0Annotator, Episode0Analyzer, Episode0Path

    # 1. Process video → voxels + metadata
    processor = Episode0Processor("video.mp4")
    metadata = processor.process()

    # 2. Annotate zone timeline interactively
    annotator = Episode0Annotator("video.mp4", "timeline.json")
    annotator.run()

    # 3. Analyze zones → palettes + heatmaps
    analyzer = Episode0Analyzer(metadata["voxels_path"], "timeline.json", "video.mp4")
    results = analyzer.analyze_all_zones()

    # 4. Generate NPC patrol route
    path_gen = Episode0Path("timeline.json")
    patrol_route = path_gen.generate_patrol_route()
    path_gen.save_patrol_route(patrol_route, "patrol_route.json")

See: docs/EPISODE0_PROCESSING.md for full specification
"""

__version__ = "1.0.0"
__all__ = [
    "Episode0Processor",
    "Episode0Annotator",
    "Episode0Analyzer",
    "Episode0Path"
]

from .processor import Episode0Processor
from .annotator import Episode0Annotator
from .analyzer import Episode0Analyzer
from .path import Episode0Path
