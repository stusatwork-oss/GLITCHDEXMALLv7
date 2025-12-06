#!/usr/bin/env python3
"""
Slushee - Coolant Consumable

Personal comfort buff that provides:

- Heat tolerance increase
- Small local Cloud relief
- Temporary resistance to Toddler presence

Usage:
    slushee = SlusheeItem("slushee_blue_raspberry")

    # Player drinks it
    result = drink_slushee(sim, player, slushee, current_time)
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


DEFAULT_OBJECT_DIR = Path(__file__).resolve().parents[2] / "data" / "objects"


@dataclass
class PurchaseInfo:
    vendor_zones: List[str]
    cost_credits: float
    stock_per_vendor: int


@dataclass
class SlusheeModifiers:
    heat_tolerance: int
    toddler_vision_resistance: float


@dataclass
class SlusheeEffects:
    player_heat_relief: float
    local_cloud_relief: float
    duration_seconds: float
    modifiers: SlusheeModifiers
    status_flags: List[str] = field(default_factory=list)
    flavor_text: List[str] = field(default_factory=list)


@dataclass
class SlusheeUsage:
    cooldown_seconds: float
    stacking: str
    max_active: int
    audio_cue: Optional[str] = None


@dataclass
class SlusheeDefinition:
    id: str
    display_name: str
    role: str
    description: str
    purchase: PurchaseInfo
    effects: SlusheeEffects
    usage: SlusheeUsage

    @staticmethod
    def from_dict(payload: Dict[str, Any]) -> "SlusheeDefinition":
        purchase = PurchaseInfo(**payload["purchase"])
        effects_payload = payload["effects"]
        modifiers = SlusheeModifiers(**effects_payload["modifiers"])
        effects = SlusheeEffects(
            player_heat_relief=effects_payload["player_heat_relief"],
            local_cloud_relief=effects_payload["local_cloud_relief"],
            duration_seconds=effects_payload["duration_seconds"],
            modifiers=modifiers,
            status_flags=effects_payload.get("status_flags", []),
            flavor_text=effects_payload.get("flavor_text", []),
        )
        usage = SlusheeUsage(**payload.get("usage", {}))
        return SlusheeDefinition(
            id=payload["id"],
            display_name=payload["display_name"],
            role=payload["role"],
            description=payload["description"],
            purchase=purchase,
            effects=effects,
            usage=usage,
        )


@dataclass
class SlusheeConsumptionResult:
    item_id: str
    display_name: str
    consumed_at: float
    expires_at: float
    duration_seconds: float
    heat_relief: float
    cloud_relief: float
    modifiers_applied: Dict[str, Any]
    status_flags: List[str]
    flavor_text_line: Optional[str]


@dataclass
class SlusheeReversionResult:
    item_id: str
    reverted_at: float
    modifiers_reverted: Dict[str, Any]
    status_flags_removed: List[str]


class SlusheeItem:
    """Runtime helper that applies Slushee effects to simulation state."""

    def __init__(self, item_id: str, data_dir: Optional[Path] = None) -> None:
        self.item_id = item_id
        self.data_dir = Path(data_dir) if data_dir else DEFAULT_OBJECT_DIR
        self.definition = self._load_definition()

    def _load_definition(self) -> SlusheeDefinition:
        path = self.data_dir / f"{self.item_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Slushee definition not found: {path}")

        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return SlusheeDefinition.from_dict(payload)

    def _choose_flavor_text(self) -> Optional[str]:
        if not self.definition.effects.flavor_text:
            return None
        return random.choice(self.definition.effects.flavor_text)

    def _extract_cloud_state(self, sim_state: Optional[Any]) -> Optional[Any]:
        """Return the cloud sub-structure from a dict-like or attribute-based sim snapshot."""

        if sim_state is None:
            return None

        if isinstance(sim_state, dict):
            return sim_state.get("cloud")

        if hasattr(sim_state, "cloud"):
            return getattr(sim_state, "cloud")

        raise TypeError(
            "sim_state must be a dict containing 'cloud' or expose a 'cloud' attribute"
        )

    def _ensure_has_level(self, cloud_state: Any) -> None:
        if cloud_state is None:
            return

        has_attr = hasattr(cloud_state, "level")
        has_key = isinstance(cloud_state, dict) and "level" in cloud_state
        if not (has_attr or has_key):
            raise AttributeError(
                "cloud_state must provide a 'level' field (attribute or dict key)"
            )

    def _apply_numeric(self, target: Any, attr: str, delta: float) -> Optional[float]:
        """Apply a numeric delta to a target object or dictionary."""
        if hasattr(target, attr):
            original = getattr(target, attr)
            try:
                new_value = original + delta
                setattr(target, attr, new_value)
                return new_value
            except TypeError:
                return None

        if isinstance(target, dict):
            original = target.get(attr, 0)
            try:
                target[attr] = original + delta
                return target[attr]
            except TypeError:
                return None
        return None

    def _append_status(self, target: Any, statuses: Iterable[str]) -> List[str]:
        updated: List[str] = []
        if hasattr(target, "statuses") and isinstance(getattr(target, "statuses"), list):
            status_list = getattr(target, "statuses")
            for status in statuses:
                if status not in status_list:
                    status_list.append(status)
                    updated.append(status)
        elif isinstance(target, dict):
            status_list = target.setdefault("statuses", [])
            for status in statuses:
                if status not in status_list:
                    status_list.append(status)
                    updated.append(status)
        return updated

    def _remove_status(self, target: Any, statuses: Iterable[str]) -> List[str]:
        removed: List[str] = []
        if hasattr(target, "statuses") and isinstance(getattr(target, "statuses"), list):
            status_list = getattr(target, "statuses")
            for status in statuses:
                if status in status_list:
                    status_list.remove(status)
                    removed.append(status)
        elif isinstance(target, dict):
            status_list = target.get("statuses", [])
            for status in statuses:
                if status in status_list:
                    status_list.remove(status)
                    removed.append(status)
        return removed

    def apply_to_player(
        self,
        sim_state: Optional[Dict[str, Any]],
        player_state: Any,
        current_time: float,
    ) -> SlusheeConsumptionResult:
        effects = self.definition.effects
        modifiers_applied: Dict[str, Any] = {}

        cloud_state = self._extract_cloud_state(sim_state)
        self._ensure_has_level(cloud_state)

        if cloud_state is not None:
            cloud_delta = -effects.local_cloud_relief
            cloud_applied = self._apply_numeric(cloud_state, "level", cloud_delta)
            if cloud_applied is not None:
                modifiers_applied["cloud_level_delta"] = cloud_delta

        heat_delta = -effects.player_heat_relief
        heat_applied = self._apply_numeric(player_state, "heat", heat_delta)
        if heat_applied is not None:
            modifiers_applied["heat_delta"] = heat_delta

        tolerance = self._apply_numeric(
            player_state, "heat_tolerance", effects.modifiers.heat_tolerance
        )
        if tolerance is not None:
            modifiers_applied["heat_tolerance_delta"] = effects.modifiers.heat_tolerance

        toddler_resist = self._apply_numeric(
            player_state,
            "toddler_vision_resistance",
            effects.modifiers.toddler_vision_resistance,
        )
        if toddler_resist is not None:
            modifiers_applied["toddler_vision_resistance_delta"] = (
                effects.modifiers.toddler_vision_resistance
            )

        added_statuses = self._append_status(player_state, effects.status_flags)
        if added_statuses:
            modifiers_applied["status_flags_added"] = added_statuses

        expires_at = current_time + effects.duration_seconds
        flavor = self._choose_flavor_text()

        return SlusheeConsumptionResult(
            item_id=self.definition.id,
            display_name=self.definition.display_name,
            consumed_at=current_time,
            expires_at=expires_at,
            duration_seconds=effects.duration_seconds,
            heat_relief=effects.player_heat_relief,
            cloud_relief=effects.local_cloud_relief,
            modifiers_applied=modifiers_applied,
            status_flags=added_statuses,
            flavor_text_line=flavor,
        )

    def revert_effects(
        self,
        player_state: Any,
        consumption_result: SlusheeConsumptionResult,
        current_time: float,
        remove_status_flags: bool = True,
    ) -> SlusheeReversionResult:
        """Revert the temporary modifiers applied by a Slushee when its buff expires."""

        deltas = consumption_result.modifiers_applied
        reverted: Dict[str, Any] = {}
        removed_statuses: List[str] = []

        tolerance_delta = deltas.get("heat_tolerance_delta")
        if tolerance_delta:
            reverted_value = self._apply_numeric(
                player_state, "heat_tolerance", -tolerance_delta
            )
            reverted["heat_tolerance_delta"] = -tolerance_delta if reverted_value is not None else None

        toddler_delta = deltas.get("toddler_vision_resistance_delta")
        if toddler_delta:
            reverted_value = self._apply_numeric(
                player_state, "toddler_vision_resistance", -toddler_delta
            )
            reverted["toddler_vision_resistance_delta"] = (
                -toddler_delta if reverted_value is not None else None
            )

        if remove_status_flags and deltas.get("status_flags_added"):
            removed_statuses = self._remove_status(
                player_state, deltas["status_flags_added"]
            )

        return SlusheeReversionResult(
            item_id=consumption_result.item_id,
            reverted_at=current_time,
            modifiers_reverted=reverted,
            status_flags_removed=removed_statuses,
        )


def drink_slushee(
    sim_state: Optional[Dict[str, Any]],
    player_state: Any,
    slushee: SlusheeItem,
    current_time: float,
) -> SlusheeConsumptionResult:
    """Convenience wrapper for consuming a slushee and returning the result."""

    return slushee.apply_to_player(sim_state, player_state, current_time)


def expire_slushee_effect(
    player_state: Any,
    slushee: SlusheeItem,
    consumption_result: SlusheeConsumptionResult,
    current_time: float,
    remove_status_flags: bool = True,
) -> SlusheeReversionResult:
    """Convenience wrapper for reverting a Slushee buff when it expires."""

    return slushee.revert_effects(
        player_state=player_state,
        consumption_result=consumption_result,
        current_time=current_time,
        remove_status_flags=remove_status_flags,
    )


__all__ = [
    "SlusheeItem",
    "drink_slushee",
    "expire_slushee_effect",
    "SlusheeDefinition",
    "SlusheeEffects",
    "SlusheeModifiers",
    "SlusheeUsage",
    "SlusheeConsumptionResult",
    "SlusheeReversionResult",
]
