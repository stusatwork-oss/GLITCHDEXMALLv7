"""Rejected consensus tracking and scrap-line synthesis helpers."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple


@dataclass
class RejectedConsensusRecord:
    """A piece of rejected consensus captured for later recycling."""

    id: str
    source: str
    zone_id: Optional[str]
    conditions: Dict[str, Any]
    qbit_signature: Dict[str, Any]
    reason: str
    tick_recorded: int
    metadata: Dict[str, Any] = field(default_factory=dict)


class ScrapPool:
    """Central pool where rejected consensus fragments accumulate."""

    def __init__(self, id_prefix: str = "RC") -> None:
        self.records: List[RejectedConsensusRecord] = []
        self.id_prefix = id_prefix
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f"{self.id_prefix}_{self._counter:06d}"

    def record_rejection(
        self,
        source: str,
        zone_id: Optional[str],
        conditions: Optional[Dict[str, Any]] = None,
        qbit_signature: Optional[Dict[str, Any]] = None,
        reason: str = "",
        tick_recorded: Optional[int] = None,
        record_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> RejectedConsensusRecord:
        """Capture a rejected consensus fragment for recycling."""

        record = RejectedConsensusRecord(
            id=record_id or self._next_id(),
            source=source,
            zone_id=zone_id,
            conditions=conditions or {},
            qbit_signature=qbit_signature or {},
            reason=reason,
            tick_recorded=tick_recorded if tick_recorded is not None else int(time.time()),
            metadata=metadata or {},
        )
        self.records.append(record)
        return record

    def harvest(self, limit: Optional[int] = None) -> List[RejectedConsensusRecord]:
        """Pop up to ``limit`` records for downstream processing."""

        if limit is None or limit < 0 or limit > len(self.records):
            limit = len(self.records)
        batch = self.records[:limit]
        self.records = self.records[limit:]
        return batch

    def consume_ids(
        self, ids: Sequence[str]
    ) -> Tuple[List[RejectedConsensusRecord], List[str]]:
        """Remove specific records by id, returning (consumed, missing).

        This method is permissive: requested ids that are not present are
        returned in ``missing`` rather than raising.
        """

        consumed: List[RejectedConsensusRecord] = []
        missing: List[str] = []

        remaining: List[RejectedConsensusRecord] = []
        requested = set(ids)

        for record in self.records:
            if record.id in requested:
                consumed.append(record)
            else:
                remaining.append(record)

        # Anything still requested that we didn't find is missing.
        missing = [rid for rid in requested if all(r.id != rid for r in consumed)]

        self.records = remaining
        return consumed, missing

    def snapshot(self) -> List[RejectedConsensusRecord]:
        """Return a shallow copy of current records (without mutating state)."""

        return list(self.records)

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self.records)


def record_rejected_consensus(
    target: Any,
    source: str,
    zone_id: Optional[str],
    conditions: Optional[Dict[str, Any]] = None,
    qbit_signature: Optional[Dict[str, Any]] = None,
    reason: str = "",
    tick_recorded: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> RejectedConsensusRecord:
    """Convenience wrapper that writes to ``target.scrap_pool`` if available."""

    scrap_pool: Optional[ScrapPool] = getattr(target, "scrap_pool", None)
    if scrap_pool is None:
        raise AttributeError("Target does not expose a scrap_pool for recording rejections")

    return scrap_pool.record_rejection(
        source=source,
        zone_id=zone_id,
        conditions=conditions,
        qbit_signature=qbit_signature,
        reason=reason,
        tick_recorded=tick_recorded,
        metadata=metadata,
    )


@dataclass
class MorphFirmware:
    """Synthesizes new objects/events from recycled scrap."""

    blueprints: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    DEFAULT_BLUEPRINTS: Dict[str, Dict[str, str]] = field(
        default_factory=lambda: {
            "dialogue_branch": {"output_type": "anomaly_event"},
            "npc_route": {"output_type": "voxel_object"},
            "player_option": {"output_type": "rare_prop"},
            "default": {"output_type": "anomaly_event"},
        }
    )

    def _rarity_from_qbit(self, qbit_signature: Dict[str, Any]) -> str:
        charisma = float(qbit_signature.get("charisma", 0) or 0)
        power = float(qbit_signature.get("power", 0) or 0)

        if charisma >= 900 or power >= 900:
            return "legendary"
        if charisma >= 400 or power >= 400:
            return "rare"
        if charisma >= 150 or power >= 150:
            return "uncommon"
        return "common"

    def synthesize(
        self,
        scrap_batch: Sequence[RejectedConsensusRecord],
        zone_hint: Optional[str] = None,
        output_seed: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Turn recycled scrap into spawnable specifications."""

        synthesized: List[Dict[str, Any]] = []
        for record in scrap_batch:
            blueprint = self.blueprints.get(record.source) or self.DEFAULT_BLUEPRINTS.get(
                record.source, self.DEFAULT_BLUEPRINTS["default"]
            )
            rarity = blueprint.get("rarity") or self._rarity_from_qbit(record.qbit_signature)
            output_type = blueprint.get("output_type", "anomaly_event")
            zone = zone_hint or record.zone_id or "GLOBAL"

            synthesized.append(
                {
                    "id": f"MORPH_{record.id}",
                    "source_record": record.id,
                    "output_type": output_type,
                    "zone": zone,
                    "rarity": rarity,
                    "seed_reason": record.reason,
                    "conditions": record.conditions,
                    "qbit_signature": record.qbit_signature,
                    "metadata": record.metadata,
                    "output_seed": output_seed,
                }
            )
        return synthesized

    def synthesize_object(
        self,
        scrap_batch: Sequence[RejectedConsensusRecord],
        job_id: str,
        target_zone: Optional[str],
    ) -> Dict[str, Any]:
        """Combine multiple scrap records into a single morph output spec."""

        if not scrap_batch:
            scrap_batch = [
                RejectedConsensusRecord(
                    id=f"RC_PLACEHOLDER_{job_id}",
                    source="placeholder",
                    zone_id=target_zone,
                    conditions={},
                    qbit_signature={},
                    reason="no_scrap_available",
                    tick_recorded=int(time.time()),
                )
            ]

        sources = {record.source for record in scrap_batch}
        dominant_source = next(iter(sources)) if sources else "default"
        blueprint = self.blueprints.get(dominant_source) or self.DEFAULT_BLUEPRINTS.get(
            dominant_source, self.DEFAULT_BLUEPRINTS["default"]
        )

        zone = target_zone or scrap_batch[0].zone_id or "GLOBAL"

        qbit_vector: Dict[str, float] = {"power": 0.0, "charisma": 0.0}
        cloud_pressure_delta = 0.0
        scripts: List[str] = []
        conditions: Dict[str, Any] = {}

        for record in scrap_batch:
            power = float(record.qbit_signature.get("power", 0) or 0)
            charisma = float(record.qbit_signature.get("charisma", 0) or 0)
            qbit_vector["power"] += power
            qbit_vector["charisma"] += charisma
            cloud_pressure_delta += max(power, charisma) * 0.001

            if record.conditions:
                conditions.update(record.conditions)
            scripts.append(f"seed:{record.source}")

        rarity = blueprint.get("rarity") or self._rarity_from_qbit(qbit_vector)

        return {
            "new_object_id": f"SCRAP_MORPH_{job_id}",
            "base_type": blueprint.get("output_type", "anomaly_event"),
            "qbit_vector": qbit_vector,
            "scripts": scripts,
            "rarity": rarity,
            "spawn_conditions": {
                "zone_id": zone,
                "cloud_min": conditions.get("cloud_min", 0),
                "scrap_pool_min": len(scrap_batch),
            },
            "cloud_pressure_delta": cloud_pressure_delta,
            "source_records": [record.id for record in scrap_batch],
        }


@dataclass
class ConstraintSpec:
    """Structured constraint descriptor for morph jobs."""

    constraint_id: str
    type: str
    priority: str
    weight: float = 1.0
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MorphJob:
    """Canonical morph job envelope carrying metadata and constraints."""

    job_id: str
    inputs: List[str] = field(default_factory=list)
    job_type: str = "MORPH"
    source_entity_id: Optional[str] = None
    morph_target: Dict[str, Any] = field(default_factory=dict)
    snapshots: Dict[str, Any] = field(
        default_factory=lambda: {
            "pre_morph_state": {
                "pose": {},
                "inventory": {},
                "relationships": {},
                "location": {},
                "firmware_stack": [],
                "qbit_vector": {},
                "cloud_pressure": {},
            }
        }
    )
    constraints: List[ConstraintSpec] = field(default_factory=list)
    morph_params: Dict[str, Any] = field(
        default_factory=lambda: {
            "intensity": 0.7,
            "randomness": 0.3,
            "max_iterations": 8,
            "max_penalty_score": 25.0,
        }
    )
    context: Dict[str, Any] = field(default_factory=dict)
    target_zone: Optional[str] = None


@dataclass
class MorphPenalty:
    constraint: str
    constraint_type: Optional[str] = None
    priority: Optional[str] = None
    weight: Optional[float] = None
    qbit_delta: Dict[str, float] = field(default_factory=dict)
    cloud_pressure_delta: float = 0.0
    note: Optional[str] = None


@dataclass
class MorphResult:
    job_id: str
    descriptor: Dict[str, Any]
    base_spec: Dict[str, Any]
    consumed_inputs: List[str]
    missing_inputs: List[str]
    penalties_applied: List[MorphPenalty]


def _merge_snapshot_defaults(snapshots: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure snapshot payloads include the canonical pre-morph skeleton."""

    default_pre_morph = {
        "pose": {},
        "inventory": {},
        "relationships": {},
        "location": {},
        "firmware_stack": [],
        "qbit_vector": {},
        "cloud_pressure": {},
    }

    provided = snapshots or {}
    pre_morph = {**default_pre_morph, **(provided.get("pre_morph_state") or {})}
    merged = dict(provided)
    merged["pre_morph_state"] = pre_morph
    return merged


def _collect_numeric_constraints(constraints: List[ConstraintSpec]) -> Dict[str, Any]:
    numeric: Dict[str, Any] = {}
    for constraint in constraints:
        for key, value in constraint.parameters.items():
            numeric[key] = value
    return numeric


def _translate_constraint_violation(
    spec: Dict[str, Any], constraint: ConstraintSpec, morph_params: Dict[str, Any]
) -> MorphPenalty:
    """Convert a structured constraint into QBIT/cloud deltas instead of failing."""

    priority_boost = {"CRITICAL": 2.0, "HIGH": 1.5, "MEDIUM": 1.1, "LOW": 1.0}
    base_weight = float(constraint.weight or 1.0)
    weight = base_weight * priority_boost.get(constraint.priority, 1.0)
    intensity = float(morph_params.get("intensity", 0.5) or 0.0)

    qbit_vector: Dict[str, float] = spec.setdefault("qbit_vector", {})
    qbit_delta = {"WEIRDNESS": weight * 0.1 * intensity}
    qbit_vector["WEIRDNESS"] = qbit_vector.get("WEIRDNESS", 0.0) + qbit_delta["WEIRDNESS"]

    cloud_delta = weight * 0.02 * (1.0 + float(morph_params.get("randomness", 0.0) or 0.0))
    spec["cloud_pressure_delta"] = float(spec.get("cloud_pressure_delta", 0.0) or 0.0) + cloud_delta

    return MorphPenalty(
        constraint=constraint.constraint_id,
        constraint_type=constraint.type,
        priority=constraint.priority,
        weight=constraint.weight,
        qbit_delta=qbit_delta,
        cloud_pressure_delta=cloud_delta,
        note="constraint translated into penalty rather than failing",
    )


def _apply_permissive_constraints(
    spec: Dict[str, Any], morph_job: MorphJob
) -> List[MorphPenalty]:
    penalties: List[MorphPenalty] = []
    qbit_vector: Dict[str, float] = spec.setdefault("qbit_vector", {})
    cloud_pressure_delta = float(spec.get("cloud_pressure_delta", 0) or 0)

    numeric_constraints = _collect_numeric_constraints(morph_job.constraints)

    # First, satisfy QBIT constraints (min/max) and translate violations into deltas.
    for key, value in numeric_constraints.items():
        if key.startswith("min_qbit_"):
            field = key.replace("min_qbit_", "")
            current = float(qbit_vector.get(field, 0) or 0)
            if current < float(value):
                delta = float(value) - current
                qbit_vector[field] = current + delta
                cloud_adjustment = delta * 0.01
                cloud_pressure_delta += cloud_adjustment
                penalties.append(
                    MorphPenalty(
                        constraint=key,
                        qbit_delta={field: delta},
                        cloud_pressure_delta=cloud_adjustment,
                    )
                )
        elif key.startswith("max_qbit_"):
            field = key.replace("max_qbit_", "")
            current = float(qbit_vector.get(field, 0) or 0)
            if current > float(value):
                delta = float(value) - current
                qbit_vector[field] = float(value)
                cloud_adjustment = delta * 0.01
                cloud_pressure_delta += cloud_adjustment
                penalties.append(
                    MorphPenalty(
                        constraint=key,
                        qbit_delta={field: delta},
                        cloud_pressure_delta=cloud_adjustment,
                    )
                )

    # Then clamp cloud delta after all QBIT adjustments so we never exceed caps.
    for key, value in numeric_constraints.items():
        if key == "max_cloud_delta":
            if cloud_pressure_delta > float(value):
                delta = float(value) - cloud_pressure_delta
                cloud_pressure_delta = float(value)
                penalties.append(
                    MorphPenalty(
                        constraint=key,
                        qbit_delta={},
                        cloud_pressure_delta=delta,
                    )
                )

    spec["qbit_vector"] = qbit_vector
    spec["cloud_pressure_delta"] = cloud_pressure_delta

    # Apply translation penalties for any constraints that lack explicit numeric handling.
    for constraint in morph_job.constraints:
        if not constraint.parameters:
            penalties.append(_translate_constraint_violation(spec, constraint, morph_job.morph_params))

    # Re-clamp cloud delta after translation so soft caps are honored without failing jobs.
    if "max_cloud_delta" in numeric_constraints:
        max_cloud = float(numeric_constraints["max_cloud_delta"])
        if spec["cloud_pressure_delta"] > max_cloud:
            delta = max_cloud - spec["cloud_pressure_delta"]
            spec["cloud_pressure_delta"] = max_cloud
            penalties.append(
                MorphPenalty(
                    constraint="max_cloud_delta",
                    cloud_pressure_delta=delta,
                    note="post-translation clamp",
                )
            )

    return penalties


def _build_morph_descriptor(
    spec: Dict[str, Any], penalties: List[MorphPenalty], morph_job: MorphJob, snapshots: Dict[str, Any]
) -> Dict[str, Any]:
    """Translate a raw morph spec into a transient descriptor for quorum review."""

    qbit_deltas: Dict[str, float] = {}
    delta_map: Dict[str, Dict[str, Any]] = {}

    for penalty in penalties:
        for field, delta in penalty.qbit_delta.items():
            qbit_deltas[field] = qbit_deltas.get(field, 0.0) + delta

        delta_map[penalty.constraint] = {
            "qbit_delta": penalty.qbit_delta,
            "cloud_pressure_delta": penalty.cloud_pressure_delta,
            **({"note": penalty.note} if penalty.note else {}),
        }

    total_qbit_delta = sum(abs(delta) for delta in qbit_deltas.values())
    cloud_delta = float(spec.get("cloud_pressure_delta", 0) or 0)
    stability_penalty = (len(penalties) * 0.05) + (abs(cloud_delta) * 0.1) + (total_qbit_delta * 0.001)
    max_penalty = float(morph_job.morph_params.get("max_penalty_score", 25.0) or 1.0)
    stability_score = max(0.0, 1.0 - min(stability_penalty, max_penalty) / max_penalty)

    return {
        "prototype_id": spec.get("new_object_id"),
        "delta_map": delta_map,
        "suggested_spawn_class": spec.get("base_type"),
        "stability_score": stability_score,
        "qbit_deltas": qbit_deltas,
        "requires_confirmation": True,
        "job_type": morph_job.job_type,
        "source_entity_id": morph_job.source_entity_id,
        "morph_target": morph_job.morph_target,
        "snapshots": snapshots,
        "context": morph_job.context,
    }


def process_morph_job(
    scrap_pool: ScrapPool, firmware: MorphFirmware, morph_job: MorphJob
) -> MorphResult:
    """Process a morph job permissively, never failing on constraints or inputs."""

    consumed, missing = scrap_pool.consume_ids(morph_job.inputs)

    target_zone = (
        morph_job.target_zone
        or morph_job.context.get("zone_id")
        if morph_job.context
        else None
    )

    object_spec = firmware.synthesize_object(
        scrap_batch=consumed,
        job_id=morph_job.job_id,
        target_zone=target_zone,
    )

    snapshots = _merge_snapshot_defaults(morph_job.snapshots)

    object_spec["morph_job_metadata"] = {
        "job_id": morph_job.job_id,
        "job_type": morph_job.job_type,
        "source_entity_id": morph_job.source_entity_id,
        "morph_target": morph_job.morph_target,
        "snapshots": snapshots,
        "context": morph_job.context,
    }

    penalties = _apply_permissive_constraints(object_spec, morph_job)

    return MorphResult(
        job_id=morph_job.job_id,
        descriptor=_build_morph_descriptor(object_spec, penalties, morph_job, snapshots),
        base_spec=object_spec,
        consumed_inputs=[record.id for record in consumed],
        missing_inputs=missing,
        penalties_applied=penalties,
    )


__all__ = [
    "RejectedConsensusRecord",
    "ScrapPool",
    "record_rejected_consensus",
    "MorphFirmware",
    "ConstraintSpec",
    "MorphJob",
    "MorphPenalty",
    "MorphResult",
    "process_morph_job",
]
