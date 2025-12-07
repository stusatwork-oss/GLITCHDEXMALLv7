"""
qbit_law_engine.py

Thin wrapper around your existing QBIT system to:
- score laws in QBIT space
- decide passage
- compute law strength & interpretation radius
- log to a Constitution file for your future auto-construction pipeline
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Callable
import json
import time
import os


# -----------------------------
# 1. Interfaces / placeholders
# -----------------------------

# You already have this somewhere.
# Just import your real function instead.
GetQbitStateFn = Callable[[str], Dict[str, float]]

# Example shape: tweak keys to match your real QBIT structure.
# This is just the "default expected" interface, not the implementation.
def get_qbit_state(actor_or_zone_id: str) -> Dict[str, float]:
    """
    TODO: Replace this stub with your existing QBIT function.
    Must return something like:
    {
      "heat": 0.3,
      "debt": 0.7,
      "coherence": 0.5,
      "gravity": 0.2
    }
    """
    raise NotImplementedError("Hook this into your existing QBIT system.")


@dataclass
class Actor:
    """Minimal actor/faction struct for political weighting."""
    id: str
    influence_weight: float = 1.0


# -----------------------------
# 2. Law structure
# -----------------------------

@dataclass
class Law:
    law_id: str
    title: str
    # Direction in QBIT space; keys must match your QBIT state keys.
    qbit_weights: Dict[str, float]
    # Optional scope / effect payload; the sim & constructors use this.
    scope: List[str]
    effects: Dict[str, Any]


# -----------------------------
# 3. Core QBIT law math
# -----------------------------

def score_law_for_actor(law: Law, qbit_state: Dict[str, float]) -> float:
    """
    Dot product of law.qbit_weights and qbit_state.
    Positive = law feels good for this actor.
    Negative = law feels bad.
    """
    score = 0.0
    for k, w in law.qbit_weights.items():
        v = qbit_state.get(k, 0.0)
        score += w * v
    return score


def political_power_for_law(
    law: Law,
    actors: List[Actor],
    get_qbit: GetQbitStateFn = get_qbit_state
) -> float:
    """
    Weighted sum of scores across all actors/factions.
    """
    total = 0.0
    for actor in actors:
        q = get_qbit(actor.id)
        b = score_law_for_actor(law, q)
        total += actor.influence_weight * b
    return total


def pass_probability(
    political_power: float,
    friction: float = 0.0,
    sharpness: float = 1.0
) -> float:
    """
    Turn political power into a [0,1] probability using a logistic curve.
    friction shifts the curve; sharpness controls steepness.
    """
    import math
    x = sharpness * (political_power - friction)
    # Simple logistic
    return 1.0 / (1.0 + math.exp(-x))


def law_strength(
    political_power: float,
    system_coherence: float = 1.0
) -> float:
    """
    How rigid the law is once passed.
    Higher strength = less wiggle room for interpretation.
    """
    return abs(political_power) * system_coherence


def interpretation_radius(strength: float) -> float:
    """
    How much freedom NPCs/constructors have to interpret a law.
    Higher strength -> smaller radius (less freedom).
    """
    return 1.0 / (1.0 + strength)


# -----------------------------
# 4. Evaluate & log a law
# -----------------------------

def capture_global_qbit(snapshot_ids: List[str],
                        get_qbit: GetQbitStateFn = get_qbit_state) -> Dict[str, Any]:
    """
    Simple snapshot of QBIT state for a set of ids (zones, factions, key NPCs).
    You can replace this with your existing telemetry aggregator.
    """
    return {sid: get_qbit(sid) for sid in snapshot_ids}


def evaluate_law(
    law: Law,
    actors: List[Actor],
    snapshot_ids: List[str],
    friction: float = 0.0,
    sharpness: float = 1.0,
    system_coherence: float = 1.0,
    constitution_log_path: str = "data/constitution_log.jsonl",
    get_qbit: GetQbitStateFn = get_qbit_state
) -> Dict[str, Any]:
    """
    Full evaluation pipeline:
    - compute political power
    - probability of passage
    - strength & interpretation radius
    - capture QBIT snapshot
    - append to constitution log
    - return a result dict the game can act on
    """
    P = political_power_for_law(law, actors, get_qbit=get_qbit)
    prob = pass_probability(P, friction=friction, sharpness=sharpness)
    strength = law_strength(P, system_coherence=system_coherence)
    wiggle = interpretation_radius(strength)
    qbit_snapshot = capture_global_qbit(snapshot_ids, get_qbit=get_qbit)

    result = {
        "law": asdict(law),
        "political_power": P,
        "pass_probability": prob,
        "strength": strength,
        "interpretation_radius": wiggle,
        "qbit_snapshot": qbit_snapshot,
        "timestamp_real": time.time()
    }

    # Ensure directory exists
    os.makedirs(os.path.dirname(constitution_log_path), exist_ok=True)
    with open(constitution_log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(result) + "\n")

    return result


# -----------------------------
# 5. Example wiring (delete or adapt)
# -----------------------------

if __name__ == "__main__":
    # Example actors & dummy get_qbit for quick smoke tests
    def dummy_get_qbit(_id: str) -> Dict[str, float]:
        return {
            "heat": 0.6,
            "debt": 0.4,
            "coherence": 0.5,
            "gravity": 0.7
        }

    actors = [
        Actor(id="FACTION_MALLWALKERS", influence_weight=1.0),
        Actor(id="FACTION_MALL_CORP", influence_weight=3.0),
        Actor(id="FACTION_JANITOR_UNION", influence_weight=1.5),
    ]

    law = Law(
        law_id="LC_0231",
        title="Food Court Curfew",
        qbit_weights={
            "heat": -0.4,
            "debt": -0.1,
            "coherence": +0.3,
            "gravity": +0.2
        },
        scope=["ZONE:FOOD_COURT"],
        effects={
            "npc_density_max": 0.35,
            "allowed_classes": ["JANITOR", "SECURITY"],
            "lighting_profile": "CURFEW_DIM"
        }
    )

    result = evaluate_law(
        law,
        actors,
        snapshot_ids=["ZONE:FOOD_COURT", "ZONE:ARCADE"],
        friction=0.2,
        sharpness=1.2,
        system_coherence=1.0,
        constitution_log_path="data/constitution_log.jsonl",
        get_qbit=dummy_get_qbit
    )

    print(json.dumps(result, indent=2))
