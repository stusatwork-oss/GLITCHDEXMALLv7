"""Interaction + spawn helpers for voxel objects."""
from __future__ import annotations

from typing import Any, Iterable, List, Mapping, MutableMapping

from voxel_object_loader import VoxelObject


# ---------------------------------------------------------------------------
# Spawn helpers
# ---------------------------------------------------------------------------


def _extract_object_spawns(game_state: Any) -> List[Mapping[str, Any]]:
    """Return object spawn records from a dict-like or attribute-based game state."""

    if isinstance(game_state, Mapping):
        spawns = game_state.get("object_spawns", [])
    else:
        spawns = getattr(game_state, "object_spawns", [])
    return list(spawns or [])


def instantiate_objects(game_state: Any, registry: Any, world: Any) -> int:
    """Instantiate voxel objects into the world based on a game state's spawn table."""

    spawns = _extract_object_spawns(game_state)
    placed = 0

    for spawn in spawns:
        object_id = spawn.get("object_id") or spawn.get("voxel_object_id")
        if not object_id:
            raise ValueError("Spawn entry missing 'object_id'")

        obj: VoxelObject = registry.get(object_id)
        pos = spawn.get("pos") or spawn.get("tile")
        if pos is None:
            raise ValueError(f"Spawn for {object_id} missing 'pos'")

        tile = tuple(pos)
        zone = spawn.get("zone")
        if zone is not None:
            world.place_object(obj, tile=tile, zone=zone)
        else:
            world.place_object(obj, tile=tile)
        placed += 1

    return placed


# ---------------------------------------------------------------------------
# Interaction helpers
# ---------------------------------------------------------------------------


def _set_subtitle(game_state: Any, text: str) -> None:
    if isinstance(game_state, MutableMapping):
        game_state["subtitle"] = text
    elif hasattr(game_state, "subtitle"):
        setattr(game_state, "subtitle", text)


def _ensure_flags(game_state: Any) -> MutableMapping[str, Any]:
    if isinstance(game_state, MutableMapping):
        flags = game_state.setdefault("flags", {})
        if not isinstance(flags, MutableMapping):
            raise TypeError("flags must be a mapping")
        return flags

    if not hasattr(game_state, "flags"):
        raise AttributeError("game_state must expose a 'flags' mapping")

    flags_obj = getattr(game_state, "flags")
    if not isinstance(flags_obj, MutableMapping):
        raise TypeError("game_state.flags must be a mapping")
    return flags_obj


def _adjust_cloud(game_state: Any, delta: int) -> None:
    if isinstance(game_state, MutableMapping):
        current = game_state.get("cloud_pressure", 0)
        game_state["cloud_pressure"] = current + delta
        updater = game_state.get("update_cloud_state")
        if callable(updater):
            updater()
    else:
        if not hasattr(game_state, "cloud_pressure"):
            raise AttributeError("game_state must expose cloud_pressure")
        game_state.cloud_pressure += delta
        if hasattr(game_state, "update_cloud_state"):
            updater = getattr(game_state, "update_cloud_state")
            if callable(updater):
                updater()


def apply_action(game_state: Any, action: str) -> None:
    """Apply a single scripted action to the game state."""

    if action.startswith("cloud_pressure+"):
        delta = int(action.split("+", 1)[1])
        _adjust_cloud(game_state, delta)
    elif action.startswith("cloud_pressure-"):
        delta = int(action.split("-", 1)[1])
        _adjust_cloud(game_state, -delta)
    elif action.startswith("subtitle:"):
        text = action.split(":", 1)[1].strip()
        _set_subtitle(game_state, text)
    elif action.startswith("flag:"):
        _, kv = action.split(":", 1)
        key, val = kv.split("=", 1)
        flags = _ensure_flags(game_state)
        flags[key.strip().upper()] = val.strip()


def _apply_actions(game_state: Any, actions: Iterable[str]) -> None:
    for action in actions:
        apply_action(game_state, action)


def handle_object_interaction(game_state: Any, voxel_object: VoxelObject) -> None:
    """Handle the interaction flow for a voxel object."""

    behavior = voxel_object.behavior or {}
    behavior_type = str(behavior.get("type", "STATIC")).upper()

    if behavior_type == "PICKUP":
        _apply_actions(game_state, behavior.get("on_pickup", []))
        if hasattr(game_state, "remove_object") and callable(
            getattr(game_state, "remove_object")
        ):
            game_state.remove_object(voxel_object.id)
    elif behavior_type == "NPC_PROP":
        _apply_actions(game_state, behavior.get("on_pickup", []))
    else:
        _apply_actions(game_state, behavior.get("on_use", []))
