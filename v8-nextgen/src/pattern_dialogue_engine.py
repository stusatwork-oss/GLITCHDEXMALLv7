#!/usr/bin/env python3
"""
PATTERN ABSORPTION ↔ DIALOGUE BUCKETS & CHOICE LOGIC
Step 4 of 5-part integration

NPCs speak in patterns they've absorbed, not static lines.
This binds: Lore + Mythology + Synthesis rules + Emotional state.

Architecture:
- Voice buckets = tonal/stylistic containers
- Pattern profiles = what an entity has "learned" from the world
- Mythology field = zone/world lore compression
- QBIT charisma = how much pattern bleeding occurs

Result: Westworld-grade voices - entities speak from absorbed patterns.

Usage:
    from pattern_dialogue_engine import generate_dialogue, PatternProfile

    profile = PatternProfile(
        absorbed_patterns=["e-flat", "fountain_hum", "escalator_rhythm"],
        mythology_exposure={"fc-arcade": 0.8, "atrium": 0.6}
    )

    line = generate_dialogue(
        voice_bucket="obsessive_technician",
        pattern_profile=profile,
        zone_mythology={"fc-arcade": "everything_hums_in_e_flat"},
        qbit_charisma=1200,
        emotional_state="stressed"
    )

Reference:
- Spynt Case Study
- Vector dialogue bucket system
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import random


@dataclass
class PatternProfile:
    """
    Record of what patterns an entity has absorbed from the world.

    Attributes:
        absorbed_patterns: Set of pattern IDs entity has encountered
        mythology_exposure: Dict of zone/lore → exposure level (0-1)
        synthesis_depth: How many layers of pattern combination (0-5)
        resonance_memories: Specific moments that stuck
    """
    absorbed_patterns: Set[str] = field(default_factory=set)
    mythology_exposure: Dict[str, float] = field(default_factory=dict)
    synthesis_depth: int = 1  # 0-5 (how many pattern layers combine)
    resonance_memories: List[str] = field(default_factory=list)

    def add_pattern(self, pattern_id: str):
        """Absorb a new pattern."""
        self.absorbed_patterns.add(pattern_id)

    def add_mythology_exposure(self, zone_id: str, exposure: float):
        """Record exposure to zone mythology."""
        current = self.mythology_exposure.get(zone_id, 0.0)
        self.mythology_exposure[zone_id] = min(1.0, current + exposure)

    def has_pattern(self, pattern_id: str) -> bool:
        """Check if entity has absorbed a pattern."""
        return pattern_id in self.absorbed_patterns

    def get_mythology_weight(self, zone_id: str) -> float:
        """Get how much zone lore has influenced this entity."""
        return self.mythology_exposure.get(zone_id, 0.0)


# ============================================================================
# VOICE BUCKETS
# ============================================================================

VOICE_BUCKETS = {
    "obsessive_technician": {
        "base_style": "clinical, pattern-focused, detail-oriented",
        "sentence_structure": "short declarative",
        "common_words": ["exactly", "measure", "pattern", "frequency", "consistent"],
        "punctuation": [".", "..."],
        "pattern_bleed_chance": 0.9  # Very likely to reference patterns
    },
    "demoralized_worker": {
        "base_style": "defeated, passive, resigned",
        "sentence_structure": "fragments, trailing",
        "common_words": ["whatever", "doesn't matter", "used to", "back when"],
        "punctuation": ["...", "."],
        "pattern_bleed_chance": 0.4
    },
    "dutiful_authority": {
        "base_style": "formal, procedure-focused, by-the-book",
        "sentence_structure": "complete, structured",
        "common_words": ["protocol", "regulation", "authorized", "procedure"],
        "punctuation": [".", "!"],
        "pattern_bleed_chance": 0.2  # Rarely breaks from script
    },
    "unraveling_witness": {
        "base_style": "fractured, contradictory, pattern-obsessed",
        "sentence_structure": "fragmented, repetitive",
        "common_words": ["all", "same", "pattern", "everywhere", "can't", "stop"],
        "punctuation": ["...", ".", "—"],
        "pattern_bleed_chance": 1.0  # Always bleeding patterns
    },
    "neutral_shopper": {
        "base_style": "casual, transactional, unremarkable",
        "sentence_structure": "simple complete",
        "common_words": ["just", "looking", "sale", "thanks", "excuse me"],
        "punctuation": [". ", "?"],
        "pattern_bleed_chance": 0.1
    }
}


# ============================================================================
# PATTERN FRAGMENTS
# ============================================================================

PATTERN_FRAGMENTS = {
    "e-flat": [
        "the arcade machines hum in E-flat",
        "everything's tuned to E-flat",
        "same frequency, E-flat",
        "it's always E-flat"
    ],
    "fountain_hum": [
        "the fountain pump has the same tone",
        "fountain's humming that frequency",
        "even the water resonates"
    ],
    "escalator_rhythm": [
        "the escalators match the rhythm",
        "steps grinding in sync",
        "escalator frequency matches"
    ],
    "all_connected": [
        "it's all connected",
        "everything's tied together",
        "same system running through it all",
        "whole mall's on the same circuit"
    ],
    "wrong_space": [
        "this space feels wrong",
        "geometry doesn't make sense here",
        "walls aren't where they should be",
        "the dimensions shifted"
    ],
    "time_loop": [
        "I've been here before",
        "this already happened",
        "time's folding back",
        "same moment, different day"
    ],
    "child_presence": [
        "there's a kid somewhere",
        "hear that crying?",
        "small footsteps echoing",
        "child's voice in the vents"
    ]
}


# ============================================================================
# MYTHOLOGY FIELDS
# ============================================================================

ZONE_MYTHOLOGY = {
    "FC-ARCADE": {
        "core_truth": "everything_hums_in_e_flat",
        "ambient_lore": "arcade_machines_as_signal_nodes",
        "pattern_density": 0.9
    },
    "Z1_CENTRAL_ATRIUM": {
        "core_truth": "fountain_is_the_heart",
        "ambient_lore": "tensile_sails_as_breathing_lungs",
        "pattern_density": 0.7
    },
    "SERVICE_HALL": {
        "core_truth": "behind_scenes_awareness",
        "ambient_lore": "janitors_know_the_real_layout",
        "pattern_density": 0.5
    },
    "Z7_SUBTERRANEAN": {
        "core_truth": "forbidden_depth",
        "ambient_lore": "what_lies_beneath",
        "pattern_density": 1.0
    }
}


# ============================================================================
# DIALOGUE GENERATION
# ============================================================================

def generate_dialogue(
    voice_bucket: str,
    pattern_profile: PatternProfile,
    zone_mythology: Optional[Dict] = None,
    qbit_charisma: float = 0.0,
    emotional_state: str = "neutral",
    context: Optional[Dict] = None
) -> str:
    """
    Generate dialogue line from pattern absorption.

    This is the core synthesis: voice + patterns + lore + emotion + charisma.

    Args:
        voice_bucket: Tonal container (e.g., "obsessive_technician")
        pattern_profile: What patterns entity has absorbed
        zone_mythology: Current zone's lore field
        qbit_charisma: Entity's charisma score (0-3000)
        emotional_state: Current emotion (from Vector)
        context: Additional context (event, target, etc.)

    Returns:
        Generated dialogue line
    """
    if voice_bucket not in VOICE_BUCKETS:
        voice_bucket = "neutral_shopper"

    bucket = VOICE_BUCKETS[voice_bucket]
    context = context or {}

    # Determine if pattern bleeding occurs
    charisma_boost = (qbit_charisma / 3000.0) * 0.3  # 0-0.3
    bleed_chance = bucket["pattern_bleed_chance"] + charisma_boost

    # Emotional state modifiers
    if emotional_state in ["stressed", "fearful", "breaking_down"]:
        bleed_chance += 0.2  # More pattern bleeding under stress

    will_bleed_pattern = random.random() < bleed_chance

    # Base utterance
    if will_bleed_pattern and pattern_profile.absorbed_patterns:
        # Generate pattern-infused line
        line = _generate_pattern_line(
            pattern_profile,
            zone_mythology,
            bucket,
            emotional_state
        )
    else:
        # Generate bucket-style line without pattern
        line = _generate_bucket_line(bucket, emotional_state, context)

    return line


def _generate_pattern_line(
    profile: PatternProfile,
    zone_mythology: Optional[Dict],
    bucket: Dict,
    emotional_state: str
) -> str:
    """Generate line that references absorbed patterns."""

    # Pick a pattern the entity has absorbed
    if not profile.absorbed_patterns:
        return _generate_bucket_line(bucket, emotional_state, {})

    pattern_id = random.choice(list(profile.absorbed_patterns))

    # Get pattern fragments
    if pattern_id not in PATTERN_FRAGMENTS:
        return _generate_bucket_line(bucket, emotional_state, {})

    fragment = random.choice(PATTERN_FRAGMENTS[pattern_id])

    # Synthesis depth - combine multiple patterns
    if profile.synthesis_depth > 1 and len(profile.absorbed_patterns) > 1:
        # Add connecting pattern
        other_patterns = [p for p in profile.absorbed_patterns if p != pattern_id]
        if other_patterns:
            other_id = random.choice(other_patterns)
            if other_id in PATTERN_FRAGMENTS:
                other_fragment = random.choice(PATTERN_FRAGMENTS[other_id])
                fragment = f"{fragment}. {other_fragment}."

    # Mythology weighting
    if zone_mythology and "core_truth" in zone_mythology:
        # Chance to reference zone's core truth
        if random.random() < zone_mythology.get("pattern_density", 0.5):
            # Blend pattern with mythology
            truth = zone_mythology["core_truth"]
            if truth == "everything_hums_in_e_flat":
                fragment = f"{fragment}. It's all the same frequency."

    # Emotional state affects delivery
    if emotional_state == "stressed":
        fragment = fragment.replace(".", "...").lower()
    elif emotional_state == "breaking_down":
        # Repetition, fragmentation
        words = fragment.split()
        if len(words) > 2:
            fragment = f"{words[0]} {words[1]}... {words[0]} {words[1]}."

    return fragment


def _generate_bucket_line(bucket: Dict, emotional_state: str, context: Dict) -> str:
    """Generate generic line from voice bucket without pattern bleed."""

    # Template lines per bucket style
    templates = {
        "obsessive_technician": [
            "The measurements are consistent.",
            "I've been tracking the data.",
            "Pattern holds across all samples."
        ],
        "demoralized_worker": [
            "Doesn't matter anymore.",
            "Used to care about that...",
            "Whatever. Do what you want."
        ],
        "dutiful_authority": [
            "Please follow the designated path.",
            "This area is restricted to authorized personnel.",
            "Procedure dictates I ask for identification."
        ],
        "unraveling_witness": [
            "It's happening again...",
            "Can't... can't stop seeing it.",
            "All the same. Everything's the same."
        ],
        "neutral_shopper": [
            "Excuse me, do you work here?",
            "Just looking, thanks.",
            "Is there a sale on today?"
        ]
    }

    # Get matching template set
    for key, lines in templates.items():
        if key in bucket["base_style"] or key == context.get("bucket_override"):
            return random.choice(lines)

    return "..."


def condition_dialogue_with_qbit(
    raw_line: str,
    qbit_charisma: float,
    qbit_power: float
) -> str:
    """
    Post-process dialogue based on QBIT scores.

    High charisma = more compelling delivery
    High power = more authoritative tone

    Args:
        raw_line: Generated line
        qbit_charisma: Charisma score (0-3000)
        qbit_power: Power score (0-3000)

    Returns:
        Conditioned dialogue
    """
    # High charisma adds intensity
    if qbit_charisma > 2000:
        # More vivid language
        raw_line = raw_line.replace("see", "witness")
        raw_line = raw_line.replace("hear", "sense")

    # High power adds authority markers
    if qbit_power > 2000:
        if not raw_line.endswith((".", "!", "?")):
            raw_line += "."

    return raw_line


# ============================================================================
# PATTERN ABSORPTION LOGIC
# ============================================================================

def entity_absorbs_pattern(
    profile: PatternProfile,
    zone_id: str,
    event_type: str,
    duration_in_zone: float
):
    """
    Entity absorbs patterns from zone/events.

    Args:
        profile: Entity's pattern profile
        zone_id: Current zone
        event_type: What's happening
        duration_in_zone: Time spent in zone (seconds)
    """
    # Zone mythology exposure
    if zone_id in ZONE_MYTHOLOGY:
        exposure_rate = 0.01 * (duration_in_zone / 60.0)  # 1% per minute
        profile.add_mythology_exposure(zone_id, exposure_rate)

    # Event-triggered pattern absorption
    if event_type == "hears_e_flat_hum" and zone_id == "FC-ARCADE":
        profile.add_pattern("e-flat")
        profile.add_pattern("arcade_hum")

    if event_type == "observes_fountain" and zone_id == "Z1_CENTRAL_ATRIUM":
        profile.add_pattern("fountain_hum")

    if event_type == "uses_escalator":
        profile.add_pattern("escalator_rhythm")

    if event_type == "toddler_sighting":
        profile.add_pattern("child_presence")

    # Synthesis depth increases with mythology exposure
    total_exposure = sum(profile.mythology_exposure.values())
    profile.synthesis_depth = min(5, int(total_exposure))


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("PATTERN DIALOGUE ENGINE TEST")
    print("="*60)

    # Create Janitor profile (has absorbed E-flat pattern)
    janitor_profile = PatternProfile()
    janitor_profile.add_pattern("e-flat")
    janitor_profile.add_pattern("fountain_hum")
    janitor_profile.add_pattern("escalator_rhythm")
    janitor_profile.add_mythology_exposure("FC-ARCADE", 0.8)
    janitor_profile.synthesis_depth = 2

    print("\n--- Janitor (Obsessive Technician) ---")
    for i in range(3):
        line = generate_dialogue(
            voice_bucket="obsessive_technician",
            pattern_profile=janitor_profile,
            zone_mythology=ZONE_MYTHOLOGY["FC-ARCADE"],
            qbit_charisma=1200,
            emotional_state="stressed"
        )
        print(f"  {i+1}. \"{line}\"")

    # Shopper (no patterns absorbed)
    shopper_profile = PatternProfile()

    print("\n--- Generic Shopper (Neutral) ---")
    for i in range(3):
        line = generate_dialogue(
            voice_bucket="neutral_shopper",
            pattern_profile=shopper_profile,
            qbit_charisma=300,
            emotional_state="neutral"
        )
        print(f"  {i+1}. \"{line}\"")

    # NPC breaks down (unraveling witness)
    broken_profile = PatternProfile()
    broken_profile.add_pattern("e-flat")
    broken_profile.add_pattern("all_connected")
    broken_profile.add_pattern("wrong_space")
    broken_profile.synthesis_depth = 3

    print("\n--- Broken NPC (Unraveling Witness) ---")
    for i in range(3):
        line = generate_dialogue(
            voice_bucket="unraveling_witness",
            pattern_profile=broken_profile,
            zone_mythology=ZONE_MYTHOLOGY["FC-ARCADE"],
            qbit_charisma=1800,
            emotional_state="breaking_down"
        )
        print(f"  {i+1}. \"{line}\"")

    print("\n" + "="*60)
    print("NPCs NOW SPEAK FROM ABSORBED PATTERNS")
    print("Westworld-grade synthesis: Lore + Emotion + Experience")
    print("="*60)
