#!/usr/bin/env python3
"""
CUTSCENE MANAGER
Evaluates narrative triggers against game state.
"Plays" cutscenes by pausing simulation and rendering narrative description.
"""

import ast
import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional


def _eval_condition_safely(expr: str, context: Mapping[str, Any]) -> bool:
    """
    Safely evaluate a simple boolean expression like:
        "cloud.level >= 70 and player.health > 0"

    Supported:
      - Names (looked up in context)
      - Attribute access (cloud.level -> context["cloud"]["level"] if dicts)
      - Constants (numbers, strings, booleans)
      - Comparisons (==, !=, <, <=, >, >=) with chaining
      - Boolean ops: and / or
      - not x

    Anything else → treated as invalid → returns False.
    """
    def _resolve_name(name: str) -> Any:
        if name in context:
            return context[name]
        # fall back to KeyError if truly unknown
        raise KeyError(name)

    def _eval_node(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return _eval_node(node.body)
        if isinstance(node, ast.BoolOp):
            vals = [_eval_node(v) for v in node.values]
            if isinstance(node.op, ast.And):
                return all(vals)
            if isinstance(node.op, ast.Or):
                return any(vals)
            raise ValueError("Unsupported boolean operator")
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return not _eval_node(node.operand)
        if isinstance(node, ast.Compare):
            left = _eval_node(node.left)
            for op, comp in zip(node.ops, node.comparators):
                right = _eval_node(comp)
                if isinstance(op, ast.Eq) and not (left == right):
                    return False
                elif isinstance(op, ast.NotEq) and not (left != right):
                    return False
                elif isinstance(op, ast.Lt) and not (left < right):
                    return False
                elif isinstance(op, ast.LtE) and not (left <= right):
                    return False
                elif isinstance(op, ast.Gt) and not (left > right):
                    return False
                elif isinstance(op, ast.GtE) and not (left >= right):
                    return False
                left = right  # chaining: a < b < c
            return True
        if isinstance(node, ast.Name):
            return _resolve_name(node.id)
        if isinstance(node, ast.Attribute):
            base = _eval_node(node.value)
            # Support dict-style "cloud.level" → context["cloud"]["level"]
            if isinstance(base, Mapping):
                return base[node.attr]
            return getattr(base, node.attr)
        if isinstance(node, ast.Constant):
            return node.value
        # Anything else is not allowed
        raise ValueError(f"Unsupported expression node: {type(node).__name__}")

    try:
        tree = ast.parse(expr, mode="eval")
        return bool(_eval_node(tree))
    except Exception:
        # On any failure, treat condition as not satisfied
        return False


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
                if not _eval_condition_safely(cond, context):
                    return False
            except Exception:
                # If eval fails (e.g. missing variable), condition fails
                return False
        return True

# Helper to build context for eval
class ContextWrapper:
    def __init__(self, obj): self.obj = obj
    def __getattr__(self, name): return getattr(self.obj, name, None)