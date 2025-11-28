#!/usr/bin/env python3
"""
HOLOmister - Environmental FX Node

SEG HoloMister™ Environmental System - Climate comfort through mist projection
and integrated holographic advertising.

Activates at medium Cloud levels (40-85), projects mist + holograms.
Glitches when Toddler nearby or Cloud critical.

Usage:
    holomister = HoloMister(zone_id="ATRIUM", position=(0, 5, 0))

    # Update every tick
    holomister.update(
        current_time=sim_time,
        cloud_level=sim.cloud.cloud_level,
        toddler_in_zone=sim.toddler.zone_id == "ATRIUM",
        toddler_reality_strain=sim.toddler.reality_strain
    )
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


DEFAULT_OBJECT_DIR = Path(__file__).resolve().parents[2] / "data" / "objects"


@dataclass
class HoloMisterTriggers:
    cloud_min: float
    cloud_max: float
    activation_delay_seconds: float
    deactivation_delay_seconds: float
    glitch_cloud_threshold: float
    toddler_strain_glitch: float


@dataclass
class HoloMisterEffects:
    mist_rate_ml_per_min: float
    cloud_relief: float
    comfort_delta: float
    heat_relief: float
    hologram_messages: List[str]
    glitch_messages: List[str]
    glitch_haze_strength: float
    glitch_color: str


@dataclass
class HoloMisterDefinition:
    id: str
    display_name: str
    manufacturer: str
    role: str
    description: str
    zone_affinity: List[str]
    triggers: HoloMisterTriggers
    effects: HoloMisterEffects
    maintenance: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(payload: Dict[str, Any]) -> "HoloMisterDefinition":
        triggers = HoloMisterTriggers(**payload["triggers"])
        effects = HoloMisterEffects(**payload["effects"])
        return HoloMisterDefinition(
            id=payload["id"],
            display_name=payload["display_name"],
            manufacturer=payload["manufacturer"],
            role=payload["role"],
            description=payload["description"],
            zone_affinity=payload.get("zone_affinity", []),
            triggers=triggers,
            effects=effects,
            maintenance=payload.get("maintenance", {}),
        )


@dataclass
class HoloMisterState:
    state: str = "inactive"  # inactive, arming, active, glitching, cooling
    last_state_change: float = 0.0
    active_since: Optional[float] = None
    pending_activation_at: Optional[float] = None
    pending_deactivation_at: Optional[float] = None
    last_message: Optional[str] = None
    glitch_logged: bool = False


class HoloMister:
    def __init__(self, zone_id: str, position: Tuple[float, float, float], data_dir: Optional[Path] = None) -> None:
        self.zone_id = zone_id
        self.position = position
        self.data_dir = Path(data_dir) if data_dir else DEFAULT_OBJECT_DIR
        self.definition = self._load_definition()
        self.state = HoloMisterState()

    def _load_definition(self) -> HoloMisterDefinition:
        path = self.data_dir / "holomister_unit.json"
        if not path.exists():
            raise FileNotFoundError(f"HoloMister definition not found: {path}")
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return HoloMisterDefinition.from_dict(payload)

    # --- State helpers -------------------------------------------------
    def _change_state(self, new_state: str, now: float) -> None:
        self.state.state = new_state
        self.state.last_state_change = now
        if new_state == "active":
            self.state.active_since = now
        if new_state in {"inactive", "cooling"}:
            self.state.active_since = None

    def _should_activate(self, cloud_level: float) -> bool:
        triggers = self.definition.triggers
        return triggers.cloud_min <= cloud_level <= triggers.cloud_max

    def _should_glitch(self, cloud_level: float, toddler_reality_strain: float, toddler_in_zone: bool) -> bool:
        triggers = self.definition.triggers
        if cloud_level >= triggers.glitch_cloud_threshold:
            return True
        if toddler_in_zone and toddler_reality_strain >= triggers.toddler_strain_glitch:
            return True
        return False

    def _pick_message(self, glitch: bool = False) -> Optional[str]:
        messages = (
            self.definition.effects.glitch_messages if glitch else self.definition.effects.hologram_messages
        )
        if not messages:
            return None
        return random.choice(messages)

    # --- Public API ----------------------------------------------------
    def update(
        self,
        current_time: float,
        cloud_level: float,
        toddler_in_zone: bool = False,
        toddler_reality_strain: float = 0.0,
    ) -> Dict[str, Any]:
        events: List[str] = []
        triggers = self.definition.triggers

        # Glitch check first so it can override activation state
        if self._should_glitch(cloud_level, toddler_reality_strain, toddler_in_zone):
            if self.state.state != "glitching":
                self._change_state("glitching", current_time)
                events.append("HOLOMISTER_GLITCH")
            self.state.last_message = self._pick_message(glitch=True)
            self.state.glitch_logged = True
        else:
            # Normal activation window
            if self._should_activate(cloud_level):
                if self.state.state == "inactive":
                    if self.state.pending_activation_at is None:
                        self.state.pending_activation_at = current_time
                    elif current_time - self.state.pending_activation_at >= triggers.activation_delay_seconds:
                        self._change_state("active", current_time)
                        self.state.pending_activation_at = None
                        events.append("HOLOMISTER_ACTIVATED")
                        self.state.last_message = self._pick_message()
                elif self.state.state == "cooling":
                    # Cancel cooling if we drifted back into range
                    self.state.pending_deactivation_at = None
                    self._change_state("active", current_time)
            else:
                # Outside activation window
                if self.state.state == "active":
                    if self.state.pending_deactivation_at is None:
                        self.state.pending_deactivation_at = current_time
                    elif current_time - self.state.pending_deactivation_at >= triggers.deactivation_delay_seconds:
                        self._change_state("cooling", current_time)
                        events.append("HOLOMISTER_COOLING")
                elif self.state.state == "glitching":
                    # After a glitch, allow the unit to cool off
                    if self.state.pending_deactivation_at is None:
                        self.state.pending_deactivation_at = current_time
                    elif current_time - self.state.pending_deactivation_at >= triggers.deactivation_delay_seconds:
                        self._change_state("cooling", current_time)
                        events.append("HOLOMISTER_RECOVERING")
                elif self.state.state == "cooling":
                    if current_time - self.state.last_state_change >= triggers.deactivation_delay_seconds:
                        self._change_state("inactive", current_time)
                        self.state.pending_deactivation_at = None
                        events.append("HOLOMISTER_INACTIVE")
                else:
                    self.state.pending_activation_at = None

        return {
            "state": self.state.state,
            "last_message": self.state.last_message,
            "glitch_logged": self.state.glitch_logged,
            "events": events,
            "cloud_relief": self.definition.effects.cloud_relief if self.state.state == "active" else 0.0,
            "comfort_delta": self.definition.effects.comfort_delta if self.state.state == "active" else 0.0,
            "heat_relief": self.definition.effects.heat_relief if self.state.state == "active" else 0.0,
            "mist_rate_ml_per_min": self.definition.effects.mist_rate_ml_per_min if self.state.state == "active" else 0.0,
        }

    def flag(self, label: str) -> None:
        """Track one-off flags for analytics/cutscenes."""
        setattr(self.state, label, True)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "zone": self.zone_id,
            "position": self.position,
            "state": self.state.state,
            "active_since": self.state.active_since,
            "last_message": self.state.last_message,
            "glitch_logged": self.state.glitch_logged,
        }


__all__ = ["HoloMister", "HoloMisterDefinition", "HoloMisterEffects", "HoloMisterTriggers", "HoloMisterState"]
