#!/usr/bin/env python3
"""
CUTSCENE MANAGER
Evaluates narrative triggers against game state.
"Plays" cutscenes by pausing simulation and rendering narrative description.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class Cutscene:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data.get("display_name", self.id)
        self.data = data
        self.trigger = data.get("trigger", {})
        self.played_count = 0
    
    def get_description(self) -> str:
        return self.data.get("sora_prompt", {}).get("scene_description", "...")

class CutsceneManager:
    def __init__(self, assets_root: Path):
        self.scenes: Dict[str, Cutscene] = {}
        self.active_cutscene: Optional[Cutscene] = None
        self.load_assets(assets_root / "assets" / "cutscenes")

    def load_assets(self, path: Path):
        if not path.exists(): return
        for f in path.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                c = Cutscene(data)
                self.scenes[c.id] = c
                print(f"[CUTSCENE] Loaded: {c.name}")
            except Exception as e:
                print(f"[CUTSCENE] Error loading {f.name}: {e}")

    def check_triggers(self, event_type: str, context: Dict[str, Any]) -> Optional[Cutscene]:
        """
        Evaluates all cutscenes against the event and context.
        Returns the Cutscene object if triggered, else None.
        """
        if self.active_cutscene: return None # Busy

        for scene in self.scenes.values():
            trig = scene.trigger
            
            # 1. Check Event Type match
            if trig.get("event") != event_type:
                continue

            # 2. Check Replay Policy
            policy = scene.data.get("replay_policy", "always")
            if policy == "once_per_save" and scene.played_count > 0:
                continue
            if policy == "once_per_run" and scene.played_count > 0:
                continue

            # 3. Check Specific Conditions (Eval)
            conditions = trig.get("conditions", [])
            if self._evaluate_conditions(conditions, context):
                return scene
        
        return None

    def play(self, cutscene: Cutscene):
        """Starts the cutscene (sets active state)."""
        self.active_cutscene = cutscene
        cutscene.played_count += 1
        print("\n" + "="*60)
        print(f"🎬 CUTSCENE: {cutscene.name.upper()}")
        print("-" * 60)
        print(f"\"{cutscene.get_description()}\"")
        print("="*60 + "\n")

    def update(self, dt: float):
        """Advance cutscene timer. For now, instant finish for text mode."""
        if self.active_cutscene:
            # In a real engine, wait for duration. Here, we clear it immediately
            # after one 'frame' of blocking logic in the main loop.
            pass

    def clear_active(self):
        self.active_cutscene = None

    def _evaluate_conditions(self, conditions: List[str], context: Dict[str, Any]) -> bool:
        """
        Safely evaluates string conditions against context dict.
        Supports: 'obj.prop >= val' logic.
        """
        for cond in conditions:
            # Very basic parser: "a.b >= c"
            # In production, use AST parsing or a rule engine.
            # Here we just use python's eval with a restricted scope
            try:
                # context must flatten "cloud.level" to context["cloud"]["level"] access?
                # Actually, eval works if we pass objects in locals.
                # But to be safe for JSON strings like "cloud.level >= 70":
                if not eval(cond, {}, context):
                    return False
            except Exception:
                # If eval fails (e.g. missing variable), condition fails
                return False
        return True

# Helper to build context for eval
class ContextWrapper:
    def __init__(self, obj): self.obj = obj
    def __getattr__(self, name): return getattr(self.obj, name, None)