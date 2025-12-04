#!/usr/bin/env python3
"""
Cutscene Engine - Sora-Powered FMV Omen System

Turns rare simulation events into Full Motion Video cutscenes.

The mall doesn't just simulate - it REMEMBERS. Sora generates cinematic
moments for specific events:
- Janitor breaks his rule
- Cloud crosses critical threshold
- Toddler manifests
- HOLOmister glitches

Usage:
    engine = CutsceneEngine(cutscene_dir="data/cutscenes")
    engine.load_all()

    # In sim loop
    if janitor.in_forbidden_zone and cloud.level >= 70:
        event = SimulationEvent("JANITOR_RULE_BROKEN", zone="FC-ARCADE", cloud=cloud.level)
        playback = handle_event(event, sim_state, engine, current_time)
"""

from __future__ import annotations

import json
import operator
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


DEFAULT_CUTSCENE_DIR = Path(__file__).resolve().parents[2] / "data" / "cutscenes"


class ReplayPolicy(str, Enum):
    ONCE_PER_RUN = "once_per_run"
    ONCE_PER_SAVE = "once_per_save"
    ONCE_PER_PROFILE = "once_per_profile"
    ALWAYS = "always"


@dataclass
class CutsceneTrigger:
    event: str
    zone: Optional[str] = None
    cloud_min: Optional[float] = None
    cloud_max: Optional[float] = None
    threshold: Optional[float] = None
    direction: Optional[str] = None
    conditions: List[str] = field(default_factory=list)


@dataclass
class SoraPrompt:
    scene_description: str
    style: Optional[str] = None
    sfx: List[str] = field(default_factory=list)
    camera: Optional[str] = None
    lighting: Optional[str] = None
    rating: Optional[str] = None


@dataclass
class CutsceneDefinition:
    id: str
    display_name: str
    type: str
    duration_seconds: float
    trigger: CutsceneTrigger
    sora_prompt_id: str
    sora_prompt: SoraPrompt
    replay_policy: ReplayPolicy = ReplayPolicy.ONCE_PER_RUN
    blocking: bool = True
    post_actions: List[str] = field(default_factory=list)

    @staticmethod
    def from_dict(payload: Dict[str, Any]) -> "CutsceneDefinition":
        trigger = CutsceneTrigger(**payload["trigger"])
        prompt = SoraPrompt(**payload["sora_prompt"])
        replay_policy = ReplayPolicy(payload.get("replay_policy", ReplayPolicy.ONCE_PER_RUN))
        return CutsceneDefinition(
            id=payload["id"],
            display_name=payload.get("display_name", payload["id"]),
            type=payload.get("type", "event_cutscene"),
            duration_seconds=payload.get("duration_seconds", 10),
            trigger=trigger,
            sora_prompt_id=payload["sora_prompt_id"],
            sora_prompt=prompt,
            replay_policy=replay_policy,
            blocking=payload.get("blocking", True),
            post_actions=payload.get("post_actions", []),
        )


class AttrDict(dict):
    """Dict that allows attribute access, recursively."""

    def __getattr__(self, item: str) -> Any:
        if item in self:
            value = self[item]
            return self._wrap(value)
        raise AttributeError(item)

    def _wrap(self, value: Any) -> Any:
        if isinstance(value, dict):
            return AttrDict(value)
        return value


@dataclass
class SimulationEvent:
    name: str
    zone: Optional[str] = None
    cloud: Optional[float] = None
    threshold: Optional[float] = None
    direction: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def matches(self, cutscene: CutsceneDefinition, context: Dict[str, Any]) -> bool:
        trigger = cutscene.trigger
        if trigger.event != self.name:
            return False
        if trigger.zone and trigger.zone != self.zone:
            return False
        if trigger.threshold is not None and self.threshold is not None:
            if trigger.threshold != self.threshold:
                return False
        if trigger.direction and self.direction and trigger.direction != self.direction:
            return False
        if trigger.cloud_min is not None and self.cloud is not None and self.cloud < trigger.cloud_min:
            return False
        if trigger.cloud_max is not None and self.cloud is not None and self.cloud > trigger.cloud_max:
            return False
        return _conditions_pass(trigger.conditions, context)


@dataclass
class PlaybackDecision:
    cutscene: CutsceneDefinition
    event: SimulationEvent
    allowed: bool
    reason: Optional[str] = None
    seen_key: Optional[str] = None


class CutsceneEngine:
    def __init__(self, cutscene_dir: Optional[Path] = None) -> None:
        self.cutscene_dir = Path(cutscene_dir) if cutscene_dir else DEFAULT_CUTSCENE_DIR
        self.cutscenes: List[CutsceneDefinition] = []
        self.seen_cutscenes: Dict[str, List[str]] = {}

    def load_all(self) -> None:
        self.cutscenes.clear()
        if not self.cutscene_dir.exists():
            raise FileNotFoundError(f"Cutscene directory missing: {self.cutscene_dir}")
        for path in sorted(self.cutscene_dir.glob("*.json")):
            with path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            self.cutscenes.append(CutsceneDefinition.from_dict(payload))

    def _make_seen_key(self, cutscene_id: str, policy: ReplayPolicy, profile_id: str, save_id: str) -> str:
        if policy == ReplayPolicy.ONCE_PER_PROFILE:
            return f"profile:{profile_id}:{cutscene_id}"
        if policy == ReplayPolicy.ONCE_PER_SAVE:
            return f"save:{save_id}:{cutscene_id}"
        if policy == ReplayPolicy.ONCE_PER_RUN:
            return f"run:{cutscene_id}"
        return f"always:{cutscene_id}"

    def _has_seen(self, key: str) -> bool:
        bucket = self.seen_cutscenes.setdefault("seen", [])
        return key in bucket

    def _mark_seen(self, key: str) -> None:
        bucket = self.seen_cutscenes.setdefault("seen", [])
        if key not in bucket:
            bucket.append(key)

    def should_play(
        self,
        cutscene: CutsceneDefinition,
        event: SimulationEvent,
        context: Dict[str, Any],
        profile_id: str,
        save_id: str,
    ) -> PlaybackDecision:
        key = self._make_seen_key(cutscene.id, cutscene.replay_policy, profile_id, save_id)
        if cutscene.replay_policy != ReplayPolicy.ALWAYS and self._has_seen(key):
            return PlaybackDecision(cutscene, event, False, reason="replay_policy_block", seen_key=key)

        if not event.matches(cutscene, context):
            return PlaybackDecision(cutscene, event, False, reason="trigger_mismatch", seen_key=key)

        return PlaybackDecision(cutscene, event, True, seen_key=key)

    def record_played(self, decision: PlaybackDecision) -> None:
        if decision.allowed and decision.seen_key:
            self._mark_seen(decision.seen_key)


def _build_context(event: SimulationEvent, sim_state: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    context: Dict[str, Any] = {}
    if sim_state:
        for key, value in sim_state.items():
            context[key] = AttrDict(value) if isinstance(value, dict) else value
    context.update(event.metadata or {})
    context["cloud"] = context.get("cloud") or AttrDict({"level": event.cloud})
    context["event"] = event
    context["janitor"] = context.get("janitor", AttrDict({"in_forbidden_zone": False}))
    context["toddler"] = context.get("toddler", AttrDict({"visible": 0.0, "behavior": None}))
    context["player"] = context.get("player", AttrDict({"distance_to_toddler": None}))
    context["holomister"] = context.get("holomister", AttrDict({"glitched": False, "distance_to_holomister": None}))
    return context


def _conditions_pass(conditions: Iterable[str], context: Dict[str, Any]) -> bool:
    if not conditions:
        return True
    for condition in conditions:
        condition = condition.strip()
        if condition in {"first_occurrence", "first_glitch_occurrence"}:
            continue  # handled by replay policy via seen_key
        if not _evaluate_condition(condition, context):
            return False
    return True


def _evaluate_condition(condition: str, context: Dict[str, Any]) -> bool:
    # Very small, explicit interpreter to avoid unrestricted eval
    ops = {
        "==": operator.eq,
        "!=": operator.ne,
        ">=": operator.ge,
        "<=": operator.le,
        ">": operator.gt,
        "<": operator.lt,
    }
    for symbol, func in ops.items():
        if symbol in condition:
            left, right = [part.strip() for part in condition.split(symbol, 1)]
            left_val = _resolve_value(left, context)
            right_val = _resolve_value(right, context)
            try:
                return func(left_val, right_val)
            except Exception:
                return False
    # Fallback: truthy lookup (e.g., "holomister.glitched")
    value = _resolve_value(condition, context)
    return bool(value)


def _resolve_value(path: str, context: Dict[str, Any]) -> Any:
    # Supports dotted lookups like "cloud.level"
    parts = path.split(".")
    current: Any = context
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        else:
            current = getattr(current, part, None)
    # Cast strings that look like numbers
    if isinstance(current, str):
        try:
            if "." in current:
                return float(current)
            return int(current)
        except ValueError:
            return current
    return current


def handle_event(
    event: SimulationEvent,
    sim_state: Optional[Dict[str, Any]],
    engine: CutsceneEngine,
    current_time: float,
    profile_id: str = "default_profile",
    save_id: str = "default_save",
) -> Optional[PlaybackDecision]:
    """Evaluate a simulation event against all known cutscenes."""

    context = _build_context(event, sim_state)
    for cutscene in engine.cutscenes:
        decision = engine.should_play(cutscene, event, context, profile_id, save_id)
        if decision.allowed:
            engine.record_played(decision)
            decision.reason = "play"
            return decision
    return None


__all__ = [
    "CutsceneEngine",
    "CutsceneDefinition",
    "CutsceneTrigger",
    "SoraPrompt",
    "ReplayPolicy",
    "SimulationEvent",
    "PlaybackDecision",
    "handle_event",
]
