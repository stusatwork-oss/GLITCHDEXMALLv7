# EPISODE 0 PROCESSING 📹→🎮

**The mall's first remembered lifetime.**

Episode 0 treats your walkthrough video as the canonical reference run - the ground truth for:
- **Zone timeline** - What zones you visit and when
- **Motion patterns** - Where movement occurs per zone
- **Visual palettes** - Actual colors from the footage
- **NPC patrol routes** - Cameraman's path becomes Janitor's patrol
- **Geometry validation** - Verify voxel builder matches reality

---

## The Pipeline

```
RAW VIDEO (11 minutes of mall footage)
  ↓
[1] PROCESSOR - Extract frames, compute motion voxels
  ↓
  - episode0_voxels.npy (T, Y, X) motion grid
  - episode0_metadata.json
  ↓
[2] ANNOTATOR - Interactive zone timeline marking
  ↓
  - timeline.json (zone boundaries)
  ↓
[3] ANALYZER - Extract zone-specific data
  ↓
  - Zone heatmaps (PNG)
  - Zone palettes (JSON, K-means colors)
  ↓
[4] PATH - Generate NPC patrol route
  ↓
  - patrol_route.json (timed waypoints)
  ↓
[5] V7 INTEGRATION - Janitor follows Episode 0 path
```

---

## 1. Processor - Video to Voxels

**Purpose:** Convert raw video into sparse motion voxel grid.

**File:** `src/episode0/processor.py`

### What It Does

1. **Frame extraction** - Downsample to 5 fps
2. **Spatial downsampling** - Resize to 32×18 grid
3. **Motion detection** - Frame differencing (threshold: 20)
4. **Voxel generation** - (T, Y, X) array where value = motion intensity

### Usage

```bash
# CLI
cd v7-nextgen/src
python -m episode0.processor path/to/video.mp4 \
  --output ../../data/episode0 \
  --fps 5 \
  --grid 32x18 \
  --threshold 20 \
  --clip-id episode0_walkthrough
```

```python
# Python API
from episode0 import Episode0Processor

processor = Episode0Processor(
    video_path="media/walkthrough.mp4",
    output_dir="../../data/episode0",
    target_fps=5,
    grid_size=(32, 18),
    diff_threshold=20
)

metadata = processor.process(clip_id="episode0_walkthrough")
# Returns:
# {
#   "clip_id": "episode0_walkthrough",
#   "voxels_path": "data/episode0/episode0_walkthrough_voxels.npy",
#   "metadata_path": "data/episode0/episode0_walkthrough_metadata.json",
#   "fps": 5,
#   "duration_seconds": 660,
#   "num_frames": 3300
# }
```

### Output Files

**Voxel data:** `episode0_walkthrough_voxels.npy`
- NumPy array: (T, Y, X) = (3300, 18, 32)
- dtype: uint8 (0-255 motion intensity)
- Sparse: ~95% zeros (only moving pixels are nonzero)

**Metadata:** `episode0_walkthrough_metadata.json`
```json
{
  "clip_id": "episode0_walkthrough",
  "source_video": "media/walkthrough.mp4",
  "fps": 5,
  "original_fps": 30,
  "width_cells": 32,
  "height_cells": 18,
  "duration_seconds": 660,
  "num_frames": 3300,
  "voxels_path": "data/episode0/episode0_walkthrough_voxels.npy",
  "voxels_shape": [3300, 18, 32],
  "diff_threshold": 20,
  "processing": {
    "grid_size": [32, 18],
    "target_fps": 5,
    "frame_skip": 6
  }
}
```

**Sample frames:** `samples/episode0_walkthrough_frame_NNNN.png`
- 10 evenly-spaced frames for visual inspection

---

## 2. Annotator - Interactive Zone Timeline

**Purpose:** Scrub video and mark zone boundaries.

**File:** `src/episode0/annotator.py`

### What It Does

OpenCV-based interactive tool with keyboard controls:
- **SPACE** - Pause/play
- **Z** - Mark zone boundary (prompts for zone ID)
- **B** - Back 5 seconds
- **F** - Forward 5 seconds
- **S** - Save timeline
- **Q** - Quit

### Usage

```bash
cd v7-nextgen/src
python -m episode0.annotator \
  --video path/to/video.mp4 \
  --output ../../data/episode0/timeline.json
```

### Workflow

1. Run annotator, video starts paused at 0:00
2. Press SPACE to play
3. When zone changes, press Z
4. Enter zone ID (e.g., "ATRIUM", "FOOD_COURT", "FC-ARCADE")
5. Repeat for all zone transitions
6. Press S to save (auto-saves on quit)

### Output File

**Timeline:** `timeline.json`
```json
{
  "clip_id": "episode0_walkthrough",
  "source_video": "media/walkthrough.mp4",
  "duration_s": 660,
  "num_zones": 8,
  "zones_timeline": [
    {
      "start_s": 0,
      "end_s": 45,
      "zone_id": "ENTRANCE",
      "duration_s": 45
    },
    {
      "start_s": 45,
      "end_s": 180,
      "zone_id": "ATRIUM",
      "duration_s": 135
    },
    {
      "start_s": 180,
      "end_s": 330,
      "zone_id": "FOOD_COURT",
      "duration_s": 150
    },
    {
      "start_s": 330,
      "end_s": 660,
      "zone_id": "FC-ARCADE",
      "duration_s": 330
    }
  ]
}
```

**Note:** Timeline can be loaded/resumed if it already exists.

---

## 3. Analyzer - Zone Palettes & Heatmaps

**Purpose:** Extract zone-specific visual data.

**File:** `src/episode0/analyzer.py`

### What It Does

For each zone in the timeline:

1. **Motion heatmap** - Accumulate motion voxels over zone duration
2. **Color palette** - K-means clustering on video frames (5 dominant colors)
3. **Visualizations** - Save heatmaps as colorized PNG

### Usage

```bash
cd v7-nextgen/src
python -m episode0.analyzer \
  --voxels ../../data/episode0/episode0_walkthrough_voxels.npy \
  --timeline ../../data/episode0/timeline.json \
  --video path/to/video.mp4 \
  --output ../../data/episode0/analysis \
  --colors 5
```

```python
# Python API
from episode0 import Episode0Analyzer

analyzer = Episode0Analyzer(
    voxels_path="data/episode0/episode0_walkthrough_voxels.npy",
    timeline_path="data/episode0/timeline.json",
    video_path="media/walkthrough.mp4",
    output_dir="data/episode0/analysis"
)

results = analyzer.analyze_all_zones(palette_colors=5)
```

### Output Files

**Analysis JSON:** `episode0_walkthrough_analysis.json`
```json
{
  "clip_id": "episode0_walkthrough",
  "num_zones": 4,
  "zones": [
    {
      "zone_id": "ATRIUM",
      "start_s": 45,
      "end_s": 180,
      "duration_s": 135,
      "heatmap_path": "data/episode0/analysis/heatmaps/episode0_walkthrough_ATRIUM_heatmap.png",
      "palette": [
        {"hex": "#8b7d6b", "rgb": [139, 125, 107], "weight": 0.42},
        {"hex": "#e8dcc8", "rgb": [232, 220, 200], "weight": 0.28},
        {"hex": "#3a3a3a", "rgb": [58, 58, 58], "weight": 0.15},
        {"hex": "#c9b99e", "rgb": [201, 185, 158], "weight": 0.10},
        {"hex": "#5a4a3a", "rgb": [90, 74, 58], "weight": 0.05}
      ]
    }
  ]
}
```

**Heatmaps:** `heatmaps/episode0_walkthrough_ZONEID_heatmap.png`
- Colorized motion heatmap (TURBO colormap)
- Upscaled 32×18 → 640×360 for visibility
- Includes zone label and color scale legend

### Using Palettes

```python
# Load analysis
with open("data/episode0/analysis/episode0_walkthrough_analysis.json") as f:
    analysis = json.load(f)

# Get ATRIUM palette
for zone in analysis["zones"]:
    if zone["zone_id"] == "ATRIUM":
        palette = zone["palette"]
        # Use dominant color for zone fog/lighting
        dominant_color = palette[0]["rgb"]  # [139, 125, 107]
```

---

## 4. Path - NPC Patrol Route Generator

**Purpose:** Convert zone timeline into timed waypoints for Janitor.

**File:** `src/episode0/path.py`

### What It Does

1. Map zone IDs → 3D positions (centroids)
2. Generate timed waypoints from zone timeline
3. Optional: Interpolate transitions between zones
4. Output patrol route compatible with v7_integrated_demo

### Usage

```bash
cd v7-nextgen/src
python -m episode0.path \
  --timeline ../../data/episode0/timeline.json \
  --output ../../data/episode0/patrol_route.json \
  --speed 1.0 \
  --visualize
```

```python
# Python API
from episode0 import Episode0Path

path_gen = Episode0Path(timeline_path="data/episode0/timeline.json")

patrol_route = path_gen.generate_patrol_route(
    interpolate=True,
    speed_mps=1.0
)

path_gen.save_patrol_route(patrol_route, "data/episode0/patrol_route.json")
path_gen.visualize_route(patrol_route)
```

### Output File

**Patrol route:** `patrol_route.json`
```json
{
  "clip_id": "episode0_walkthrough",
  "duration_s": 660,
  "num_waypoints": 16,
  "waypoints": [
    {
      "time_s": 0,
      "position": [-10, 0, -40],
      "zone_id": "ENTRANCE",
      "event": "zone_entry"
    },
    {
      "time_s": 45,
      "position": [-10, 0, -40],
      "zone_id": "ENTRANCE",
      "event": "zone_exit"
    },
    {
      "time_s": 67.5,
      "position": [-5, 0, -20],
      "zone_id": "ENTRANCE→ATRIUM",
      "event": "zone_transition"
    },
    {
      "time_s": 90,
      "position": [0, 0, 0],
      "zone_id": "ATRIUM",
      "event": "zone_entry"
    }
  ],
  "metadata": {
    "generated_from": "data/episode0/timeline.json",
    "interpolated": true,
    "speed_mps": 1.0
  }
}
```

### ASCII Visualization

```
==============================================================
  Patrol Route Visualization
==============================================================

    0 → 00:00  ENTRANCE                        ( -10.0,    0.0,  -40.0)
    1 ← 00:45  ENTRANCE                        ( -10.0,    0.0,  -40.0)
    2 ↔ 01:07  ENTRANCE→ATRIUM                 (  -5.0,    0.0,  -20.0)
    3 → 01:30  ATRIUM                          (   0.0,    0.0,    0.0)
    4 ← 03:00  ATRIUM                          (   0.0,    0.0,    0.0)
    5 ↔ 03:45  ATRIUM→FOOD_COURT               (  25.0,    0.0,  -15.0)
    6 → 04:30  FOOD_COURT                      (  50.0,    0.0,  -30.0)
    ...
```

---

## 5. V7 Integration - Janitor Follows Episode 0

**Purpose:** Make Janitor retrace the cameraman's path during simulation.

**File:** `src/v7_integrated_demo.py` (modified)

### Integration Points

```python
from episode0 import Episode0Path
import json

# Load patrol route
with open("data/episode0/patrol_route.json") as f:
    patrol_route = json.load(f)

# In sim loop
def update_janitor_from_episode0(janitor, sim_time, patrol_route):
    """Move Janitor to match Episode 0 timeline."""

    # Find current waypoint
    for i, wp in enumerate(patrol_route["waypoints"]):
        if wp["time_s"] > sim_time:
            # Interpolate between previous and current waypoint
            if i > 0:
                prev_wp = patrol_route["waypoints"][i-1]

                # Lerp position
                t = (sim_time - prev_wp["time_s"]) / (wp["time_s"] - prev_wp["time_s"])
                janitor.position = lerp(prev_wp["position"], wp["position"], t)
                janitor.current_zone = wp["zone_id"]
            break
    else:
        # Past end of route
        final_wp = patrol_route["waypoints"][-1]
        janitor.position = final_wp["position"]
        janitor.current_zone = final_wp["zone_id"]

# In V7IntegratedSim.tick()
update_janitor_from_episode0(self.janitor, self.sim_time, patrol_route)
```

### Result

- **sim_time = 0s** → Janitor at ENTRANCE (-10, 0, -40)
- **sim_time = 90s** → Janitor at ATRIUM (0, 0, 0)
- **sim_time = 270s** → Janitor at FOOD_COURT (50, 0, -30)
- **sim_time = 540s** → Janitor at FC-ARCADE (80, 0, -20)

**When Cloud ≥ 70 AND Janitor in FC-ARCADE:**
- Janitor breaks rule (forbidden zone)
- LLM dialogue triggers
- "The arcade machines... they're humming in E-flat"

**The simulation now has a canonical memory - Episode 0 is the mall's first lifetime.**

---

## Complete Workflow Example

```bash
# 1. Process video → voxels
cd v7-nextgen/src
python -m episode0.processor media/walkthrough.mp4 \
  --output ../../data/episode0 \
  --clip-id episode0_walkthrough

# Output:
# data/episode0/episode0_walkthrough_voxels.npy
# data/episode0/episode0_walkthrough_metadata.json
# data/episode0/samples/*.png

# 2. Annotate zone timeline (interactive)
python -m episode0.annotator \
  --video media/walkthrough.mp4 \
  --output ../../data/episode0/timeline.json

# Output:
# data/episode0/timeline.json

# 3. Analyze zones → palettes + heatmaps
python -m episode0.analyzer \
  --voxels ../../data/episode0/episode0_walkthrough_voxels.npy \
  --timeline ../../data/episode0/timeline.json \
  --video media/walkthrough.mp4 \
  --output ../../data/episode0/analysis

# Output:
# data/episode0/analysis/episode0_walkthrough_analysis.json
# data/episode0/analysis/heatmaps/*.png

# 4. Generate NPC patrol route
python -m episode0.path \
  --timeline ../../data/episode0/timeline.json \
  --output ../../data/episode0/patrol_route.json \
  --visualize

# Output:
# data/episode0/patrol_route.json

# 5. Run integrated demo with Episode 0
python v7_integrated_demo.py --with-episode0
```

---

## File Dependencies

```
episode0/
  __init__.py         - Package exports
  processor.py        - Requires: cv2, numpy
  annotator.py        - Requires: cv2
  analyzer.py         - Requires: cv2, numpy, sklearn (K-means)
  path.py             - Requires: json, pathlib

Required packages:
  - opencv-python (cv2)
  - numpy
  - scikit-learn (for K-means clustering)

Install:
  pip install opencv-python numpy scikit-learn
```

---

## V2V Design Philosophy

**Episode 0 is Video-to-Voxel (V2V).**

The processor acts like an **event camera** - it only captures change:
- Static pixels → 0 (ignored)
- Moving pixels → motion intensity (0-255)
- Sparse voxel grid (95% zeros)

This creates a **perceptual bridge** between:
- **Real footage** (what the mall actually looks like)
- **Sim voxels** (how the game represents the mall)

The cameraman's walk becomes:
- **Ground truth** for zone boundaries
- **Visual reference** for renderer palettes
- **Behavioral template** for NPC patrols
- **Validation data** for voxel builder geometry

**Episode 0 is the mall's origin story.**

---

## Next Steps

### Optional Enhancements

1. **Multiple episodes**
   - Process other ERA_2020 clips
   - Build episode library: `episode1_foodcourt_closeup`, `episode2_service_corridor`
   - Janitor has multiple patrol patterns

2. **Motion-based Cloud amplification**
   ```python
   motion_level = sample_voxels_at_time(episode0_voxels, sim_time)
   cloud.add_pressure("EPISODE_MOTION", base_delta * (1 + motion_level))
   ```
   High-motion parts of footage → higher Cloud gain

3. **Palette-based zone lighting**
   ```python
   zone_palette = analysis["zones"]["ATRIUM"]["palette"]
   dominant_color = zone_palette[0]["rgb"]
   renderer.set_ambient_color(dominant_color)
   ```

4. **Geometry validation**
   - Compare motion heatmaps with VoxelBuilder.build_full_mall()
   - Verify cameraman stayed in walkable areas
   - Detect discrepancies (real footage vs designed geometry)

5. **Leon awareness of Episode 0**
   ```python
   # In Leon's prompt
   "The Janitor is retracing your first walk through the mall.
    At 3:15, you stood in the food court for 2 minutes.
    He's been there for 8 minutes now. Something's wrong."
   ```

---

## The Infrastructure Is Real

Before: "We have some footage of a mall"

After:
- Voxel grid of motion over time
- Zone timeline with second-level precision
- Color palettes extracted per zone
- NPC patrol routes ready for simulation
- Integration hooks for Cloud/QBIT/Leon

**Episode 0 stopped being footage. It became the mall's first memory.**

---

*The arcade machines hum in E-flat. They always have.*
