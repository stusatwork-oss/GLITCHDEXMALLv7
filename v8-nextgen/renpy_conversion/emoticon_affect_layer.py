#!/usr/bin/env python3
"""
EMOTICON AFFECT LAYER
Adds emotional/narrative tone on top of structural emoji layers.

Philosophy:
  Emoji layers = WHAT it is (structure, meaning, properties)
  Emoticon = HOW it FEELS (affect, tone, player response)

The same voxel can have different affect depending on:
  - Cloud pressure level
  - Toddler proximity
  - Time of day / era
  - Player actions
  - NPC presence

Example:
  Voxel: 🟨🕐⬇️🌓⚙️🏃 (escalator step - structural)

  At Cloud 20:   :| (neutral, normal)
  At Cloud 70:   :/ (unsettling, strained)
  At Cloud 90:   :( (disturbing, glitching)
  Toddler near:  D: (alarming, manifesting)
  Post-cutscene: :o (shocked, aftermath)
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


# ============================================================================
# AFFECT CATEGORIES
# ============================================================================

class AffectCategory(Enum):
    """Emotional affect categories."""
    NEUTRAL = "neutral"           # Normal, baseline
    UNSETTLING = "unsettling"     # Mildly disturbing
    DISTURBING = "disturbing"     # Deeply wrong
    ALARMING = "alarming"         # Immediate threat
    COMFORTING = "comforting"     # Safe, reassuring
    MELANCHOLIC = "melancholic"   # Sad, nostalgic
    OMINOUS = "ominous"           # Foreboding
    SHOCKED = "shocked"           # Aftermath, realization
    CURIOUS = "curious"           # Interesting, engaging
    RESIGNED = "resigned"         # Defeated, acceptance


# ============================================================================
# EMOTICON MAPPINGS
# ============================================================================

# Classic emoticons for each affect
AFFECT_EMOTICONS = {
    # Neutral / Baseline
    AffectCategory.NEUTRAL: {
        "primary": ":|",
        "variants": [":-|", ":I", ":|]"],
        "intensity_scale": {
            0.0: ":|",    # Completely neutral
            0.5: ":-|",   # Slightly aware
            1.0: ":I",    # Observant
        }
    },

    # Unsettling (Cloud 50-70)
    AffectCategory.UNSETTLING: {
        "primary": ":/",
        "variants": [":-/", ":\\", ":/]"],
        "intensity_scale": {
            0.0: ":|",    # Not quite there yet
            0.5: ":/",    # Something's off
            1.0: ":\\",   # Definitely wrong
        }
    },

    # Disturbing (Cloud 70-85)
    AffectCategory.DISTURBING: {
        "primary": ":(",
        "variants": [":'(", ":[", ":c"],
        "intensity_scale": {
            0.0: ":/",    # Starting to worry
            0.5: ":(",    # This is bad
            1.0: ":'(",   # This is very bad
        }
    },

    # Alarming (Cloud 85+, Toddler manifesting)
    AffectCategory.ALARMING: {
        "primary": "D:",
        "variants": ["D:<", "D:>", "O_O", "o_o"],
        "intensity_scale": {
            0.0: ":(",    # Bad but not critical
            0.5: "D:",    # Oh no
            1.0: "D:<",   # OH NO
        }
    },

    # Comforting (1981 era, low Cloud)
    AffectCategory.COMFORTING: {
        "primary": ":)",
        "variants": [":-)", ":D", "^_^"],
        "intensity_scale": {
            0.0: ":|",    # Okay
            0.5: ":)",    # Nice
            1.0: ":D",    # Wonderful
        }
    },

    # Melancholic (Decline era, abandoned)
    AffectCategory.MELANCHOLIC: {
        "primary": ":(",
        "variants": [":'(", ";_;", "T_T"],
        "intensity_scale": {
            0.0: ":/",    # Wistful
            0.5: ":(",    # Sad
            1.0: ";_;",   # Mournful
        }
    },

    # Ominous (Pre-cutscene, threshold approaching)
    AffectCategory.OMINOUS: {
        "primary": ">:|",
        "variants": [">:(", ">:I", "O_o"],
        "intensity_scale": {
            0.0: ":/",    # Tension building
            0.5: ">:|",   # Something's coming
            1.0: ">:(",   # It's here
        }
    },

    # Shocked (Post-cutscene, revelation)
    AffectCategory.SHOCKED: {
        "primary": ":o",
        "variants": [":O", "o_o", "O.O", "@_@"],
        "intensity_scale": {
            0.0: ":o",    # Surprised
            0.5: ":O",    # Very surprised
            1.0: "@_@",   # Overwhelmed
        }
    },

    # Curious (Discovery, exploration)
    AffectCategory.CURIOUS: {
        "primary": ":?",
        "variants": ["o_O", "O_o", "?_?"],
        "intensity_scale": {
            0.0: ":|",    # Noticing
            0.5: ":?",    # Wondering
            1.0: "o_O",   # Very intrigued
        }
    },

    # Resigned (Decline era, acceptance)
    AffectCategory.RESIGNED: {
        "primary": ":/",
        "variants": ["-_-", "¯\\_(ツ)_/¯", "._.", "u_u"],
        "intensity_scale": {
            0.0: ":/",    # Giving up
            0.5: "-_-",   # It is what it is
            1.0: "u_u",   # Total acceptance
        }
    },
}


# ============================================================================
# AFFECT RULES (Context → Emoticon)
# ============================================================================

def get_affect_from_cloud(cloud_level: float) -> AffectCategory:
    """Determine affect based on Cloud pressure level."""
    if cloud_level < 30:
        return AffectCategory.NEUTRAL
    elif cloud_level < 50:
        return AffectCategory.CURIOUS
    elif cloud_level < 70:
        return AffectCategory.UNSETTLING
    elif cloud_level < 85:
        return AffectCategory.DISTURBING
    else:
        return AffectCategory.ALARMING


def get_affect_from_era(era: str) -> AffectCategory:
    """Determine affect based on timeline era."""
    era_affects = {
        "1981_OPENING": AffectCategory.COMFORTING,
        "1995_PEAK": AffectCategory.NEUTRAL,
        "2005_DECLINE": AffectCategory.MELANCHOLIC,
        "2011_ABANDONED": AffectCategory.RESIGNED,
    }
    return era_affects.get(era, AffectCategory.NEUTRAL)


def get_affect_from_toddler(toddler_visibility: float, distance: float) -> Optional[AffectCategory]:
    """Determine affect based on Toddler proximity and manifestation."""
    if toddler_visibility < 0.3:
        return None  # Not visible enough to affect

    if distance < 15 and toddler_visibility > 0.7:
        return AffectCategory.ALARMING  # Close and manifested
    elif distance < 30 and toddler_visibility > 0.5:
        return AffectCategory.OMINOUS  # Approaching
    elif toddler_visibility > 0.4:
        return AffectCategory.UNSETTLING  # Visible but distant

    return None


def get_affect_from_event(event_type: str) -> AffectCategory:
    """Determine affect based on narrative event."""
    event_affects = {
        "CUTSCENE_TRIGGERED": AffectCategory.SHOCKED,
        "RULE_BROKEN": AffectCategory.OMINOUS,
        "DISCOVERY": AffectCategory.CURIOUS,
        "CONTRADICTION": AffectCategory.DISTURBING,
        "SAFE_ZONE_ENTERED": AffectCategory.COMFORTING,
    }
    return event_affects.get(event_type, AffectCategory.NEUTRAL)


# ============================================================================
# AFFECT RESOLVER
# ============================================================================

@dataclass
class AffectContext:
    """Context for determining voxel emotional affect."""
    cloud_level: float = 50.0
    era: str = "1995_PEAK"
    toddler_visibility: float = 0.0
    toddler_distance: float = 999.0
    recent_event: Optional[str] = None
    time_of_day: float = 12.0  # 0-24 hour
    player_sanity: float = 1.0  # 0-1
    zone_disturbance: float = 0.0  # 0-1


def resolve_affect(context: AffectContext) -> tuple[AffectCategory, float]:
    """
    Resolve the dominant affect and intensity from context.

    Returns:
        (affect_category, intensity) where intensity is 0.0-1.0
    """
    # Collect all potential affects with weights
    affects: Dict[AffectCategory, float] = {}

    # Cloud affect (base weight 0.5)
    cloud_affect = get_affect_from_cloud(context.cloud_level)
    cloud_intensity = min(1.0, context.cloud_level / 100.0)
    affects[cloud_affect] = 0.5 * cloud_intensity

    # Era affect (weight 0.3)
    era_affect = get_affect_from_era(context.era)
    affects[era_affect] = affects.get(era_affect, 0.0) + 0.3

    # Toddler affect (weight 0.8 - very strong)
    toddler_affect = get_affect_from_toddler(
        context.toddler_visibility,
        context.toddler_distance
    )
    if toddler_affect:
        toddler_intensity = context.toddler_visibility
        affects[toddler_affect] = affects.get(toddler_affect, 0.0) + (0.8 * toddler_intensity)

    # Recent event affect (weight 1.0 - immediate)
    if context.recent_event:
        event_affect = get_affect_from_event(context.recent_event)
        affects[event_affect] = affects.get(event_affect, 0.0) + 1.0

    # Zone disturbance modifier
    if context.zone_disturbance > 0.5:
        affects[AffectCategory.DISTURBING] = affects.get(AffectCategory.DISTURBING, 0.0) + 0.4

    # Find dominant affect
    if not affects:
        return AffectCategory.NEUTRAL, 0.0

    dominant_affect = max(affects.items(), key=lambda x: x[1])
    affect_category = dominant_affect[0]
    intensity = min(1.0, dominant_affect[1])  # Clamp to 1.0

    return affect_category, intensity


def get_emoticon(context: AffectContext) -> str:
    """
    Get the emoticon representation for the current context.

    Returns ASCII emoticon like ":)", ":/", "D:", etc.
    """
    affect_category, intensity = resolve_affect(context)

    emoticon_data = AFFECT_EMOTICONS[affect_category]
    intensity_scale = emoticon_data["intensity_scale"]

    # Find closest intensity match
    if intensity < 0.33:
        return intensity_scale[0.0]
    elif intensity < 0.66:
        return intensity_scale[0.5]
    else:
        return intensity_scale[1.0]


# ============================================================================
# VOXEL WITH AFFECT
# ============================================================================

@dataclass
class VoxelWithAffect:
    """Voxel with both structural emoji layers AND emotional affect."""
    # Structural layers (emoji)
    emoji_compact: str  # e.g., "🟨🕐⬇️🌓⚙️🏃"

    # Affective layer (emoticon)
    emoticon: str  # e.g., ":/" or "D:"
    affect_category: AffectCategory
    affect_intensity: float  # 0.0-1.0

    # Context that determined affect
    context: AffectContext

    def __str__(self) -> str:
        """String representation: emoji + emoticon."""
        return f"{self.emoji_compact} {self.emoticon}"

    def to_dict(self) -> Dict[str, Any]:
        """Export to dictionary."""
        return {
            "emoji_compact": self.emoji_compact,
            "emoticon": self.emoticon,
            "affect": self.affect_category.value,
            "affect_intensity": self.affect_intensity,
            "context": {
                "cloud_level": self.context.cloud_level,
                "era": self.context.era,
                "toddler_visibility": self.context.toddler_visibility,
            }
        }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def add_affect_to_voxel(
    emoji_compact: str,
    context: AffectContext
) -> VoxelWithAffect:
    """Add affect layer to a structural emoji voxel."""
    affect_category, intensity = resolve_affect(context)
    emoticon = get_emoticon(context)

    return VoxelWithAffect(
        emoji_compact=emoji_compact,
        emoticon=emoticon,
        affect_category=affect_category,
        affect_intensity=intensity,
        context=context
    )


# ============================================================================
# CLI TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("EMOTICON AFFECT LAYER TEST")
    print("=" * 80)

    # Example escalator voxel (structural)
    escalator = "🟨🕐⬇️🌓⚙️🏃"

    print(f"\nStructural voxel: {escalator}")
    print("(Metal, Active, Moving down, Semi-gloss, Mechanical hum, Fast)")
    print("\n" + "-" * 80)

    # Test different contexts
    print("\n[AFFECT VARIATIONS]")

    # Normal operation
    context1 = AffectContext(cloud_level=20, era="1995_PEAK")
    voxel1 = add_affect_to_voxel(escalator, context1)
    print(f"\nCloud 20, Peak era (normal):")
    print(f"  {voxel1}")
    print(f"  Affect: {voxel1.affect_category.value} (intensity {voxel1.affect_intensity:.2f})")

    # Rising tension
    context2 = AffectContext(cloud_level=65, era="1995_PEAK")
    voxel2 = add_affect_to_voxel(escalator, context2)
    print(f"\nCloud 65 (unsettling):")
    print(f"  {voxel2}")
    print(f"  Affect: {voxel2.affect_category.value} (intensity {voxel2.affect_intensity:.2f})")

    # High strain
    context3 = AffectContext(cloud_level=90, era="1995_PEAK")
    voxel3 = add_affect_to_voxel(escalator, context3)
    print(f"\nCloud 90 (alarming):")
    print(f"  {voxel3}")
    print(f"  Affect: {voxel3.affect_category.value} (intensity {voxel3.affect_intensity:.2f})")

    # Toddler manifestation
    context4 = AffectContext(
        cloud_level=75,
        era="1995_PEAK",
        toddler_visibility=0.8,
        toddler_distance=12.0
    )
    voxel4 = add_affect_to_voxel(escalator, context4)
    print(f"\nCloud 75 + Toddler manifesting 12 feet away:")
    print(f"  {voxel4}")
    print(f"  Affect: {voxel4.affect_category.value} (intensity {voxel4.affect_intensity:.2f})")

    # Abandoned era
    context5 = AffectContext(cloud_level=30, era="2011_ABANDONED")
    voxel5 = add_affect_to_voxel(escalator, context5)
    print(f"\nCloud 30, Abandoned 2011:")
    print(f"  {voxel5}")
    print(f"  Affect: {voxel5.affect_category.value} (intensity {voxel5.affect_intensity:.2f})")

    # Opening day
    context6 = AffectContext(cloud_level=10, era="1981_OPENING")
    voxel6 = add_affect_to_voxel(escalator, context6)
    print(f"\nCloud 10, Opening 1981:")
    print(f"  {voxel6}")
    print(f"  Affect: {voxel6.affect_category.value} (intensity {voxel6.affect_intensity:.2f})")

    print("\n" + "=" * 80)
    print("STRUCTURE vs AFFECT")
    print("  Emoji = WHAT (objective properties)")
    print("  Emoticon = HOW IT FEELS (subjective affect)")
    print("=" * 80)
