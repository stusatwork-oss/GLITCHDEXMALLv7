"""Minimal board-level perseverance layer to stabilize substrate state.

This module provides passive recovery behaviors that drift stressed zones
back toward their designed baselines without requiring explicit events:

- Cloud pressure decays exponentially toward calm.
- QBIT aggregates lerp toward their captured baselines.
- Routing overrides bleed back to baseline topology as TTLs expire.

Call :func:`tick_perseverance` once per frame after applying gameplay events
to gently heal the board.
"""

from typing import Any

from cloud import RoutingOverride


def relax_cloud(zone: Any, dt: float, half_life_ticks: float = 300) -> None:
    """Exponential decay of local cloud pressure toward baseline calm."""

    decay_factor = 0.5 ** (dt / half_life_ticks)
    zone.cloud_pressure *= decay_factor


def heal_qbit(zone: Any, dt: float, rate: float = 0.01) -> None:
    """Lerp QBIT aggregate back toward its baseline to recover coherence."""

    baseline = getattr(zone, "qbit_baseline", 0.0)
    zone.qbit_aggregate += (baseline - zone.qbit_aggregate) * rate * dt


def update_routing(zone: Any, dt: float) -> None:
    """Decay routing overrides so adjacency drifts back to baseline."""

    overrides = getattr(zone, "routing_overrides", None)
    if overrides is None:
        return

    for override in list(overrides):
        if isinstance(override, RoutingOverride):
            override.ttl -= dt
        else:
            override.ttl = getattr(override, "ttl", 0) - dt

        if override.ttl <= 0:
            overrides.remove(override)


def tick_perseverance(world: Any, dt: float = 1) -> None:
    """Apply passive healing across all zones in the world."""

    zones = getattr(world, "zones", {}) or {}
    for zone in zones.values():
        relax_cloud(zone, dt)
        heal_qbit(zone, dt)
        update_routing(zone, dt)
