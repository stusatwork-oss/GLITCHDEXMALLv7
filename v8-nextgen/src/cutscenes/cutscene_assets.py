#!/usr/bin/env python3
"""
CUTSCENE ASSET SEEDER
Writes cinematic definitions to assets/cutscenes/
"""

import json
from pathlib import Path

def seed_cutscene_assets(repo_root: Path):
    output_dir = repo_root / "assets" / "cutscenes"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. THE JANITOR BREAKS HIS RULE
    _write(output_dir, "janitor_fc_arcade_first_time.json", {
      "id": "janitor_enters_fc_arcade_first_time",
      "display_name": "The Janitor Breaks His Rule",
      "type": "event_cutscene",
      "trigger": {
        "event": "JANITOR_RULE_BROKEN",
        "zone": "FC-ARCADE",
        "conditions": ["janitor.in_forbidden_zone == True", "cloud.level >= 70"]
      },
      "sora_prompt": {
        "scene_description": "Interior mall arcade at dusk. A weary janitor stops, stares at a cabinet displaying 'E-flat'. Mist forms from ceiling vents. He doesn't move. Cinematic, unsettling.",
        "style": "Analog neon arcade haze"
      },
      "replay_policy": "once_per_save",
      "blocking": True
    })

    # 2. THE CLOUD GOES CRITICAL
    _write(output_dir, "cloud_crosses_85.json", {
      "id": "cloud_crosses_critical_threshold",
      "display_name": "The Cloud Goes Critical",
      "type": "threshold_cutscene",
      "trigger": {
        "event": "CLOUD_THRESHOLD_CROSSED",
        "threshold": 85,
        "direction": "rising",
        "conditions": ["cloud.level >= 85", "cloud.mood == 'critical'"]
      },
      "sora_prompt": {
        "scene_description": "Interior mall atrium. Lights pulse. Fountain water reverses. Security feeds freeze. A balloon stops mid-air. Everything holds for five seconds.",
        "style": "Surveillance footage aesthetic"
      },
      "replay_policy": "once_per_run",
      "blocking": True,
      "post_actions": ["cloud.set_memory('critical_breach', True)"]
    })

    # 3. THE TODDLER MANIFESTS
    _write(output_dir, "toddler_manifests.json", {
      "id": "toddler_manifests_service_corridor",
      "display_name": "The Toddler Becomes Real",
      "type": "entity_cutscene",
      "trigger": {
        "event": "TODDLER_MANIFESTING",
        "conditions": ["toddler.visible >= 0.9", "cloud.level >= 75"]
      },
      "sora_prompt": {
        "scene_description": "Dark service corridor. Small figure in overalls stands still. Lights pulse. Figure shimmers. Cut to black.",
        "style": "Liminal horror"
      },
      "replay_policy": "once_per_save",
      "blocking": True
    })

    # 4. HOLOMISTER GLITCH
    _write(output_dir, "holomister_glitch.json", {
      "id": "holomister_first_major_glitch",
      "display_name": "The Mist Speaks Wrong",
      "type": "environmental_cutscene",
      "trigger": {
        "event": "HOLOMISTER_GLITCH",
        "conditions": ["holomister.glitched == True", "cloud.level >= 70"]
      },
      "sora_prompt": {
        "scene_description": "HoloMister unit sprays gel-like mist. Text corrupts: 'CREDIT DEFAULT SLUSHEE'. Shows a child's face. Powers down.",
        "style": "Mall tech-horror"
      },
      "replay_policy": "once_per_run",
      "blocking": False
    })

    print(f"[CUTSCENES] Seeded 4 cinematic definitions to {output_dir}")

def _write(directory, filename, data):
    with open(directory / filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    seed_cutscene_assets(Path("."))