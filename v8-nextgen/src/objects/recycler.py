#!/usr/bin/env python3
"""
Recycler Trash Can - Cloud Relief Node

Prototype interaction object that converts discarded items into Cloud relief.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from rejected_consensus import RejectedConsensusRecord, ScrapPool


@dataclass
class RecyclerResult:
    used_at: float
    cloud_delta: float
    cooldown_ready_at: float
    success: bool
    reason: Optional[str] = None
    scrap_harvested: Optional[List[RejectedConsensusRecord]] = None


class RecyclerTrashCan:
    def __init__(self, zone_id: str, cloud_relief: float = 4.0, cooldown_seconds: float = 8.0) -> None:
        self.zone_id = zone_id
        self.cloud_relief = cloud_relief
        self.cooldown_seconds = cooldown_seconds
        self._next_ready_time: float = 0.0

    def can_use(self, current_time: float) -> bool:
        return current_time >= self._next_ready_time

    def use(
        self,
        sim_state: Optional[Dict[str, Any]],
        current_time: float,
        scrap_pool: Optional[ScrapPool] = None,
        harvest_limit: int = 5,
    ) -> RecyclerResult:
        if not self.can_use(current_time):
            return RecyclerResult(
                used_at=current_time,
                cloud_delta=0.0,
                cooldown_ready_at=self._next_ready_time,
                success=False,
                reason="cooldown",
            )

        harvested: Optional[List[RejectedConsensusRecord]] = None

        if sim_state and isinstance(sim_state, dict) and "cloud" in sim_state:
            cloud_state = sim_state["cloud"]
            if isinstance(cloud_state, dict):
                cloud_state["level"] = cloud_state.get("level", 0.0) - self.cloud_relief

        if scrap_pool is not None:
            harvested = scrap_pool.harvest(limit=harvest_limit)

        self._next_ready_time = current_time + self.cooldown_seconds
        return RecyclerResult(
            used_at=current_time,
            cloud_delta=-self.cloud_relief,
            cooldown_ready_at=self._next_ready_time,
            success=True,
            scrap_harvested=harvested,
        )


def use_recycler(
    sim_state: Optional[Dict[str, Any]],
    recycler: RecyclerTrashCan,
    current_time: float,
    scrap_pool: Optional[ScrapPool] = None,
    harvest_limit: int = 5,
) -> RecyclerResult:
    return recycler.use(sim_state, current_time, scrap_pool=scrap_pool, harvest_limit=harvest_limit)


__all__ = ["RecyclerTrashCan", "RecyclerResult", "use_recycler"]
