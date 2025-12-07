#!/usr/bin/env python3
"""
LAW SYSTEM - Thin wrapper over QBIT
Treats QBIT as single source of truth, never touches core math.

Laws are weighted vectors in QBIT space.
Political power = dot product of law weights × actor QBIT states.
Law strength determines interpretation freedom for AI constructors.

Philosophy: Laws can't be broken, but strong laws allow less creative interpretation.
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime


# ============================================================================
# QBIT INTERFACE (assumes your existing system)
# ============================================================================

def get_qbit_state(entity_id: str) -> Dict[str, float]:
    """
    Get QBIT state for an actor or zone.

    This is YOUR existing implementation - don't change it.
    We just call it from here.

    Returns dict with keys like:
        {"heat": 0.7, "debt": 0.3, "coherence": 0.9, "gravity": 0.5, ...}

    TODO: Replace with actual import from your QBIT system
    """
    # Placeholder - replace with:
    # from qbit_engine import get_entity_qbit
    # return get_entity_qbit(entity_id)

    # Stub for now
    return {
        "heat": 0.5,
        "debt": 0.3,
        "coherence": 0.8,
        "gravity": 0.6,
        "resonance": 0.4
    }


def capture_global_qbit() -> Dict[str, Any]:
    """
    Capture snapshot of entire QBIT system state.

    This is YOUR existing system snapshot method.

    TODO: Replace with actual implementation
    """
    # Placeholder - replace with:
    # from qbit_engine import snapshot_global_state
    # return snapshot_global_state()

    return {
        "timestamp": datetime.now().isoformat(),
        "global_heat": 0.6,
        "global_debt": 0.4,
        "global_coherence": 0.7,
        "zone_states": {},  # Your actual zone data
        "actor_states": {}  # Your actual actor data
    }


# ============================================================================
# LAW SCHEMA
# ============================================================================

@dataclass
class Law:
    """
    A law is a weighted vector in QBIT space + effects.

    The qbit_weights define the "political direction" of the law.
    The effects define what happens when the law is active.
    """
    law_id: str
    title: str
    qbit_weights: Dict[str, float]  # How this law votes in QBIT space
    scope: List[str]  # ["ZONE:FOOD_COURT", "ACTOR:SECURITY", "GLOBAL"]
    effects: Dict[str, Any]  # Gameplay effects
    description: str = ""
    enacted_timestamp: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Law':
        return cls(**data)


# Example laws
EXAMPLE_LAWS = [
    {
        "law_id": "LC_0231",
        "title": "Food Court Curfew",
        "description": "After hours, only maintenance and security allowed in food court",
        "qbit_weights": {
            "heat": -0.4,      # Reduces activity/chaos
            "debt": -0.1,      # Slight reduction in economic activity
            "coherence": 0.3,  # Increases order
            "gravity": 0.2     # Strengthens institutional pull
        },
        "scope": ["ZONE:FOOD_COURT"],
        "effects": {
            "npc_density_max": 0.35,
            "allowed_classes": ["JANITOR", "SECURITY"],
            "lighting_profile": "CURFEW_DIM",
            "time_window": {"start": "22:00", "end": "06:00"}
        }
    },
    {
        "law_id": "LC_0145",
        "title": "Central Atrium Free Speech Zone",
        "description": "Public assembly permitted in central atrium during business hours",
        "qbit_weights": {
            "heat": 0.3,       # Increases activity
            "debt": 0.0,       # Neutral economic
            "coherence": -0.2, # Reduces order (dissent allowed)
            "gravity": -0.1    # Weakens institutional control
        },
        "scope": ["ZONE:CENTRAL_ATRIUM"],
        "effects": {
            "allow_assembly": True,
            "max_crowd_size": 50,
            "security_monitoring": "passive",
            "time_window": {"start": "10:00", "end": "21:00"}
        }
    },
    {
        "law_id": "LC_0089",
        "title": "Mickey's Wing Smoking Ban",
        "description": "No smoking in restaurant wing (health code)",
        "qbit_weights": {
            "heat": -0.1,      # Slight reduction in transgressive activity
            "debt": 0.05,      # Minor economic impact (fewer smokers)
            "coherence": 0.4,  # Strong order/compliance signal
            "gravity": 0.3     # Institutional health authority
        },
        "scope": ["ZONE:MICKEYS_WING"],
        "effects": {
            "smoking_allowed": False,
            "enforcement_level": "moderate",
            "signage_required": True,
            "designated_outdoor_area": "SOUTHEAST_PARKING"
        }
    }
]


# ============================================================================
# POLITICAL POWER CALCULATION
# ============================================================================

def score_law_for_actor(law: Law, qbit_state: Dict[str, float]) -> float:
    """
    How much does this actor's QBIT state support this law?

    Dot product: law weights · actor state
    Positive = actor supports law
    Negative = actor opposes law

    This is pure math on YOUR existing QBIT values.
    """
    score = 0.0

    for dimension, weight in law.qbit_weights.items():
        if dimension in qbit_state:
            score += weight * qbit_state[dimension]

    return score


def political_power_for_law(
    law: Law,
    actors: List[Dict[str, Any]]
) -> Tuple[float, Dict[str, float]]:
    """
    Calculate total political power supporting this law.

    Args:
        law: The law to evaluate
        actors: List of dicts with keys:
            - id: entity identifier
            - influence_weight: political power (1.0 = average, 2.0 = double)

    Returns:
        (total_power, breakdown_by_actor)
    """
    total = 0.0
    breakdown = {}

    for actor in actors:
        actor_id = actor["id"]
        influence = actor.get("influence_weight", 1.0)

        # Get QBIT state from YOUR existing system
        qbit_state = get_qbit_state(actor_id)

        # Score this actor's alignment with the law
        alignment_score = score_law_for_actor(law, qbit_state)

        # Weight by political influence
        weighted_score = alignment_score * influence

        total += weighted_score
        breakdown[actor_id] = weighted_score

    return total, breakdown


# ============================================================================
# LAW STRENGTH & INTERPRETATION FREEDOM
# ============================================================================

def law_strength(political_power: float, system_coherence: float = 1.0) -> float:
    """
    How strongly is this law enforced?

    High strength = well-supported, clear enforcement
    Low strength = contested, ambiguous

    system_coherence: global modifier (Cloud state, institutional decay, etc.)
    """
    return abs(political_power) * system_coherence


def interpretation_radius(strength: float) -> float:
    """
    How much "wiggle room" do AI constructors have?

    Strong laws (high strength) = low wiggle room (tight interpretation)
    Weak laws (low strength) = high wiggle room (creative interpretation)

    Returns: 0.0 (no freedom) to 1.0 (maximum freedom)
    """
    return 1.0 / (1.0 + strength)


def enforcement_profile(strength: float, interpretation: float) -> Dict[str, Any]:
    """
    Generate enforcement parameters for AI constructors.

    Returns dict that behavior trees / LLM constructors can use:
        - violation_penalty: How harsh are violations?
        - patrol_frequency: How often is compliance checked?
        - warning_threshold: How close can you get before warning?
        - creative_freedom: Can you be "creative" with interpretation?
    """
    return {
        "violation_penalty": strength * 10.0,  # 0-10 scale
        "patrol_frequency": strength * 0.5,    # checks per game-minute
        "warning_threshold": interpretation,   # distance from strict compliance
        "creative_freedom": interpretation,    # how much AI can improvise
        "strict_mode": strength > 0.7,         # binary flag for critical laws
    }


# ============================================================================
# CONSTITUTIONAL LOG (QBIT SNAPSHOTS)
# ============================================================================

class ConstitutionLog:
    """
    Historical record of laws and the QBIT states that birthed them.

    This is your "game bible" - AI constructors and Jupyter analysis can query:
    - "What was the world like when this law passed?"
    - "How has QBIT drifted since this law was enacted?"
    - "Which laws are outdated based on current QBIT state?"
    """

    def __init__(self, log_path: Path = None):
        self.log_path = log_path or Path("data/constitution_log.jsonl")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def enact_law(
        self,
        law: Law,
        political_power: float,
        power_breakdown: Dict[str, float],
        game_time: str = None
    ):
        """
        Log a law enactment with QBIT snapshot.

        This creates a constitutional record that AI can analyze later.
        """
        # Capture QBIT state at moment of enactment
        qbit_snapshot = capture_global_qbit()

        # Create log entry
        entry = {
            "law": law.to_dict(),
            "political_power": political_power,
            "power_breakdown": power_breakdown,
            "qbit_snapshot": qbit_snapshot,
            "timestamp": game_time or datetime.now().isoformat(),
            "strength": law_strength(political_power),
            "interpretation_radius": interpretation_radius(law_strength(political_power))
        }

        # Append to log (JSONL format for easy streaming)
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')

        # Update law's enacted timestamp
        law.enacted_timestamp = entry["timestamp"]

        return entry

    def query_laws_at_time(self, game_time: str) -> List[Dict]:
        """Query all laws active at a specific game time."""
        active_laws = []

        with open(self.log_path, 'r') as f:
            for line in f:
                entry = json.loads(line)
                if entry["timestamp"] <= game_time:
                    active_laws.append(entry)

        return active_laws

    def analyze_qbit_drift(self, law_id: str) -> Dict[str, Any]:
        """
        Compare QBIT state when law was enacted vs now.

        Returns:
            - original_qbit: QBIT when law passed
            - current_qbit: QBIT right now
            - drift: difference vector
            - relevance_score: is this law still aligned with world state?
        """
        # Find law enactment
        original_entry = None
        with open(self.log_path, 'r') as f:
            for line in f:
                entry = json.loads(line)
                if entry["law"]["law_id"] == law_id:
                    original_entry = entry
                    break

        if not original_entry:
            return {"error": f"Law {law_id} not found in log"}

        # Get current QBIT
        current_qbit = capture_global_qbit()
        original_qbit = original_entry["qbit_snapshot"]

        # Calculate drift (simplified - you'd do this properly)
        drift = {}
        for key in ["global_heat", "global_debt", "global_coherence"]:
            if key in original_qbit and key in current_qbit:
                drift[key] = current_qbit[key] - original_qbit[key]

        # Relevance score: how much has the world changed?
        total_drift = sum(abs(v) for v in drift.values())
        relevance_score = 1.0 / (1.0 + total_drift)  # 1.0 = no drift, 0.0 = massive drift

        return {
            "law_id": law_id,
            "original_qbit": original_qbit,
            "current_qbit": current_qbit,
            "drift": drift,
            "relevance_score": relevance_score,
            "interpretation": (
                "Law still relevant" if relevance_score > 0.7 else
                "Law becoming outdated" if relevance_score > 0.4 else
                "Law obsolete - world has changed"
            )
        }


# ============================================================================
# HIGH-LEVEL API
# ============================================================================

class LawSystem:
    """
    Main interface for law/politics layer over QBIT.

    Usage:
        laws = LawSystem()

        # Evaluate a law
        power, breakdown = laws.evaluate_law(food_court_curfew, current_actors)

        # Enact it
        laws.enact(food_court_curfew, power, breakdown)

        # Query enforcement params for AI constructor
        params = laws.get_enforcement_params(food_court_curfew)
        # AI behavior tree uses params["creative_freedom"] to decide actions
    """

    def __init__(self, constitution_log_path: Path = None):
        self.constitution = ConstitutionLog(constitution_log_path)
        self.active_laws: Dict[str, Law] = {}

    def evaluate_law(
        self,
        law: Law,
        actors: List[Dict[str, Any]]
    ) -> Tuple[float, Dict[str, float]]:
        """
        Evaluate political power for a law without enacting it.

        Returns: (total_power, breakdown_by_actor)
        """
        return political_power_for_law(law, actors)

    def enact(
        self,
        law: Law,
        political_power: float,
        power_breakdown: Dict[str, float],
        game_time: str = None
    ):
        """
        Enact a law and log to constitution.

        This makes it active and creates historical record.
        """
        self.constitution.enact_law(law, political_power, power_breakdown, game_time)
        self.active_laws[law.law_id] = law

    def get_enforcement_params(self, law: Law, system_coherence: float = 1.0) -> Dict:
        """
        Get enforcement parameters for this law.

        AI constructors / behavior trees use this to determine:
        - How strictly to enforce
        - How much creative freedom they have
        - What penalties to apply
        """
        # Recalculate current political power (world may have changed)
        # You'd pass current actors here - placeholder for now
        strength_val = law_strength(0.5, system_coherence)  # TODO: use real power
        interp = interpretation_radius(strength_val)

        return enforcement_profile(strength_val, interp)

    def analyze_drift(self, law_id: str) -> Dict:
        """Analyze how QBIT has drifted since law was enacted."""
        return self.constitution.analyze_qbit_drift(law_id)

    def get_laws_for_scope(self, scope: str) -> List[Law]:
        """Get all active laws affecting a scope (zone, actor class, etc.)."""
        return [
            law for law in self.active_laws.values()
            if scope in law.scope or "GLOBAL" in law.scope
        ]


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("LAW SYSTEM - QBIT Political Layer")
    print("="*80)
    print()

    # Initialize system
    law_sys = LawSystem()

    # Load example law
    food_court_curfew = Law.from_dict(EXAMPLE_LAWS[0])

    print(f"Evaluating: {food_court_curfew.title}")
    print(f"QBIT weights: {food_court_curfew.qbit_weights}")
    print()

    # Example actors (in real system, query from your actor/faction registry)
    actors = [
        {"id": "FACTION_MALL_MANAGEMENT", "influence_weight": 2.0},
        {"id": "FACTION_FOOD_VENDORS", "influence_weight": 1.5},
        {"id": "FACTION_SECURITY_UNION", "influence_weight": 1.2},
        {"id": "NPC_ANGRY_TEENAGER", "influence_weight": 0.3},
    ]

    # Evaluate political power
    power, breakdown = law_sys.evaluate_law(food_court_curfew, actors)

    print(f"Political Power: {power:.3f}")
    print()
    print("Breakdown by actor:")
    for actor_id, actor_power in breakdown.items():
        print(f"  {actor_id}: {actor_power:+.3f}")
    print()

    # Calculate enforcement params
    strength_val = law_strength(power)
    interp = interpretation_radius(strength_val)
    params = enforcement_profile(strength_val, interp)

    print(f"Law Strength: {strength_val:.3f}")
    print(f"Interpretation Radius: {interp:.3f}")
    print()
    print("Enforcement Parameters (for AI constructors):")
    for key, val in params.items():
        print(f"  {key}: {val}")
    print()

    # Enact the law
    law_sys.enact(food_court_curfew, power, breakdown)
    print(f"✓ Law enacted and logged to constitution")
    print(f"  Log: {law_sys.constitution.log_path}")
    print()

    # Example: AI constructor queries this before generating NPC behavior
    print("="*80)
    print("AI CONSTRUCTOR USAGE")
    print("="*80)
    print()
    print("# When generating NPC behavior in food court at 11pm:")
    print("law_params = law_sys.get_enforcement_params(food_court_curfew)")
    print(f"creative_freedom = law_params['creative_freedom']  # {params['creative_freedom']:.2f}")
    print()
    print("if creative_freedom > 0.5:")
    print("    # High wiggle room - NPC can bend rules")
    print("    allow_loitering = True")
    print("else:")
    print("    # Strict enforcement - NPC must leave immediately")
    print("    force_exit = True")
    print()

    print("="*80)
    print("CONSTITUTION LOG")
    print("="*80)
    print()
    print(f"View complete constitutional history:")
    print(f"  cat {law_sys.constitution.log_path}")
    print()
    print("Each entry contains:")
    print("  - Law definition")
    print("  - Political power at enactment")
    print("  - Complete QBIT snapshot")
    print("  - Timestamp")
    print()
    print("AI can query:")
    print("  'What was the mall like when this law passed?'")
    print("  'How has QBIT drifted since then?'")
    print("  'Is this law still relevant?'")
    print()
