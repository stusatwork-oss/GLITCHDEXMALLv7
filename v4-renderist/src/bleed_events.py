#!/usr/bin/env python3
"""
BLEED EVENTS SYSTEM - V4 Renderist Mall OS

Bleed Events are reality-warping moments triggered by high Cloud pressure.
They temporarily alter the world's tone through visual/audio degradation.

Tier Thresholds (different from Cloud mood thresholds):
- Tier 1 @ Cloud >= 60: Visual/Audio only
- Tier 2 @ Cloud >= 75: Visual + NPC contradictions enabled
- Tier 3 @ Cloud >= 90: Visual + NPC + Space effects

LOCKED: Wind-down time = 7.5 seconds
"Storm fades. Drama maintained. Player agency respected."
"""

import time
import random
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# LOCKED CONSTANT
BLEED_WINDDOWN_TIME = 7.5  # seconds for Bleed to fade when Cloud drops


class BleedState(Enum):
    """State of the Bleed system."""
    OFF = "off"
    ACTIVE = "active"
    WINDDOWN = "winddown"


class BleedTier(Enum):
    """Bleed intensity tiers."""
    NONE = 0
    TIER_1 = 1  # Visual/Audio only
    TIER_2 = 2  # Visual + NPC contradictions
    TIER_3 = 3  # Visual + NPC + Space effects


# Tier thresholds (Cloud level)
TIER_THRESHOLDS = {
    BleedTier.TIER_1: 60,
    BleedTier.TIER_2: 75,
    BleedTier.TIER_3: 90,
}


@dataclass
class DegradationProfile:
    """Visual/audio degradation parameters for a tier."""
    # Visual
    vhs_drag: float = 0.0           # 0-1, tape drag effect
    color_banding: float = 0.0      # 0-1, reduced color depth
    jpeg_artifacts: float = 0.0     # 0-1, compression artifacts
    flicker_intensity: float = 0.0  # 0-1, light flickering
    perspective_drift: float = 0.0  # 0-1, spatial distortion

    # Audio
    detune: float = 0.0             # 0-1, pitch variance
    hum_intensity: float = 0.0      # 0-1, electrical hum
    silence_pockets: bool = False   # Zones of unnatural quiet

    # Space (Tier 3 only)
    tile_drift: bool = False        # Tile positions shift
    length_fluctuation: float = 0.0 # Hallway length variance
    gravity_variance: float = 0.0   # Subtle gravity changes


# Degradation profiles per tier
DEGRADATION_PROFILES = {
    BleedTier.TIER_1: DegradationProfile(
        vhs_drag=0.3,
        color_banding=0.2,
        jpeg_artifacts=0.1,
        flicker_intensity=0.4,
        perspective_drift=0.1,
        detune=0.2,
        hum_intensity=0.3,
        silence_pockets=True,
    ),
    BleedTier.TIER_2: DegradationProfile(
        vhs_drag=0.5,
        color_banding=0.4,
        jpeg_artifacts=0.3,
        flicker_intensity=0.6,
        perspective_drift=0.3,
        detune=0.4,
        hum_intensity=0.5,
        silence_pockets=True,
    ),
    BleedTier.TIER_3: DegradationProfile(
        vhs_drag=0.8,
        color_banding=0.6,
        jpeg_artifacts=0.5,
        flicker_intensity=0.8,
        perspective_drift=0.5,
        detune=0.6,
        hum_intensity=0.7,
        silence_pockets=True,
        tile_drift=True,
        length_fluctuation=0.3,
        gravity_variance=0.2,
    ),
}


@dataclass
class BleedEvent:
    """Record of a single bleed event."""
    start_time: float
    end_time: Optional[float] = None
    peak_tier: BleedTier = BleedTier.TIER_1
    origin_zone: str = ""
    peak_cloud_level: float = 0.0
    turbulence_snapshot: Dict[str, float] = field(default_factory=dict)


class BleedEventSystem:
    """
    Manages Bleed Events - reality warps triggered by high Cloud pressure.

    State machine: OFF -> ACTIVE -> WINDDOWN -> OFF

    Bleed activates when Cloud crosses tier thresholds.
    Bleed winds down over 7.5 seconds when Cloud drops below tier.
    """

    def __init__(self):
        """Initialize Bleed system."""
        self.state: BleedState = BleedState.OFF
        self.current_tier: BleedTier = BleedTier.NONE
        self.origin_zone: str = ""

        # Timing
        self.active_since: float = 0.0
        self.winddown_remaining: float = 0.0

        # Event tracking
        self.current_event: Optional[BleedEvent] = None
        self.event_history: List[BleedEvent] = []

        # Peak tracking (for logging)
        self.peak_tier_this_event: BleedTier = BleedTier.NONE
        self.peak_cloud_this_event: float = 0.0

    def update(self, dt: float, cloud_level: float,
               zone_turbulence: Dict[str, float],
               zone_density: Dict[str, int]) -> Dict:
        """
        Update Bleed state based on Cloud level.

        Args:
            dt: Delta time in seconds
            cloud_level: Current Cloud pressure (0-100)
            zone_turbulence: Turbulence per zone
            zone_density: Swarm density per zone

        Returns:
            Dict with bleed state and events for logging
        """
        events = []  # AO3 log events to emit

        # Determine target tier based on Cloud level
        target_tier = self._get_tier_for_level(cloud_level)

        # State machine logic
        if self.state == BleedState.OFF:
            if target_tier != BleedTier.NONE:
                # Transition: OFF -> ACTIVE
                self._start_bleed(cloud_level, zone_turbulence, zone_density)
                self.current_tier = target_tier
                events.append(self._make_event("BLEED_START", cloud_level, zone_turbulence))

        elif self.state == BleedState.ACTIVE:
            # Track peaks
            if cloud_level > self.peak_cloud_this_event:
                self.peak_cloud_this_event = cloud_level

            if target_tier.value > self.peak_tier_this_event.value:
                self.peak_tier_this_event = target_tier

            # Check for tier changes
            if target_tier != self.current_tier:
                old_tier = self.current_tier
                self.current_tier = target_tier

                if target_tier == BleedTier.NONE:
                    # Transition: ACTIVE -> WINDDOWN
                    self.state = BleedState.WINDDOWN
                    self.winddown_remaining = BLEED_WINDDOWN_TIME
                    events.append(self._make_event("BLEED_WINDDOWN_START", cloud_level, zone_turbulence))
                else:
                    # Tier change within ACTIVE
                    events.append(self._make_event("BLEED_TIER_CHANGE", cloud_level, zone_turbulence,
                                                   extra={"old_tier": old_tier.value, "new_tier": target_tier.value}))

        elif self.state == BleedState.WINDDOWN:
            self.winddown_remaining -= dt

            if self.winddown_remaining <= 0:
                # Transition: WINDDOWN -> OFF
                self._end_bleed()
                events.append(self._make_event("BLEED_END", cloud_level, zone_turbulence))
            elif target_tier != BleedTier.NONE:
                # Cloud rose again during winddown - return to ACTIVE
                self.state = BleedState.ACTIVE
                self.current_tier = target_tier
                self.winddown_remaining = 0.0
                events.append(self._make_event("BLEED_TIER_CHANGE", cloud_level, zone_turbulence,
                                               extra={"resumed_from_winddown": True, "new_tier": target_tier.value}))

        # Get current degradation profile
        profile = self._get_current_profile()

        return {
            "state": self.state.value,
            "tier": self.current_tier.value,
            "origin_zone": self.origin_zone,
            "winddown_remaining": self.winddown_remaining,
            "degradation": self._profile_to_dict(profile) if profile else {},
            "events": events,
            "active_duration": time.time() - self.active_since if self.state != BleedState.OFF else 0.0
        }

    def _get_tier_for_level(self, cloud_level: float) -> BleedTier:
        """Determine which tier applies for a given Cloud level."""
        if cloud_level >= TIER_THRESHOLDS[BleedTier.TIER_3]:
            return BleedTier.TIER_3
        elif cloud_level >= TIER_THRESHOLDS[BleedTier.TIER_2]:
            return BleedTier.TIER_2
        elif cloud_level >= TIER_THRESHOLDS[BleedTier.TIER_1]:
            return BleedTier.TIER_1
        else:
            return BleedTier.NONE

    def _start_bleed(self, cloud_level: float,
                     zone_turbulence: Dict[str, float],
                     zone_density: Dict[str, int]):
        """Start a new bleed event."""
        self.state = BleedState.ACTIVE
        self.active_since = time.time()
        self.winddown_remaining = 0.0

        # Select origin zone based on turbulence * density
        self.origin_zone = self._select_origin_zone(zone_turbulence, zone_density)

        # Reset peak tracking
        self.peak_tier_this_event = BleedTier.TIER_1
        self.peak_cloud_this_event = cloud_level

        # Create event record
        self.current_event = BleedEvent(
            start_time=time.time(),
            origin_zone=self.origin_zone,
            peak_cloud_level=cloud_level,
            turbulence_snapshot=zone_turbulence.copy()
        )

    def _end_bleed(self):
        """End the current bleed event."""
        self.state = BleedState.OFF
        self.current_tier = BleedTier.NONE
        self.winddown_remaining = 0.0

        # Finalize event record
        if self.current_event:
            self.current_event.end_time = time.time()
            self.current_event.peak_tier = self.peak_tier_this_event
            self.current_event.peak_cloud_level = self.peak_cloud_this_event
            self.event_history.append(self.current_event)
            self.current_event = None

        self.origin_zone = ""

    def _select_origin_zone(self, zone_turbulence: Dict[str, float],
                            zone_density: Dict[str, int]) -> str:
        """
        Select origin zone based on turbulence * swarm density.

        The bleed originates from where tension is highest.
        """
        if not zone_turbulence:
            return "UNKNOWN"

        # Calculate weighted scores
        scores = {}
        for zone_id, turbulence in zone_turbulence.items():
            density = zone_density.get(zone_id, 1)
            # Ensure minimum density of 1 to avoid zero scores
            scores[zone_id] = turbulence * max(1, density)

        # Return zone with highest score
        if scores:
            return max(scores, key=scores.get)
        return "UNKNOWN"

    def _get_current_profile(self) -> Optional[DegradationProfile]:
        """Get degradation profile for current state."""
        if self.state == BleedState.OFF:
            return None

        tier = self.current_tier
        if tier == BleedTier.NONE:
            # During winddown, use tier 1 profile with reduced intensity
            tier = BleedTier.TIER_1

        profile = DEGRADATION_PROFILES.get(tier)

        # During winddown, scale down the profile
        if self.state == BleedState.WINDDOWN and profile:
            scale = self.winddown_remaining / BLEED_WINDDOWN_TIME
            return self._scale_profile(profile, scale)

        return profile

    def _scale_profile(self, profile: DegradationProfile, scale: float) -> DegradationProfile:
        """Scale a degradation profile by a factor (for winddown)."""
        return DegradationProfile(
            vhs_drag=profile.vhs_drag * scale,
            color_banding=profile.color_banding * scale,
            jpeg_artifacts=profile.jpeg_artifacts * scale,
            flicker_intensity=profile.flicker_intensity * scale,
            perspective_drift=profile.perspective_drift * scale,
            detune=profile.detune * scale,
            hum_intensity=profile.hum_intensity * scale,
            silence_pockets=profile.silence_pockets and scale > 0.3,
            tile_drift=profile.tile_drift and scale > 0.5,
            length_fluctuation=profile.length_fluctuation * scale,
            gravity_variance=profile.gravity_variance * scale,
        )

    def _profile_to_dict(self, profile: DegradationProfile) -> Dict:
        """Convert profile to dict for render hints."""
        return {
            "vhs_drag": profile.vhs_drag,
            "color_banding": profile.color_banding,
            "jpeg_artifacts": profile.jpeg_artifacts,
            "flicker_intensity": profile.flicker_intensity,
            "perspective_drift": profile.perspective_drift,
            "detune": profile.detune,
            "hum_intensity": profile.hum_intensity,
            "silence_pockets": profile.silence_pockets,
            "tile_drift": profile.tile_drift,
            "length_fluctuation": profile.length_fluctuation,
            "gravity_variance": profile.gravity_variance,
        }

    def _make_event(self, event_type: str, cloud_level: float,
                    zone_turbulence: Dict[str, float],
                    extra: Optional[Dict] = None) -> Dict:
        """Create an AO3 log event."""
        event = {
            "type": event_type,
            "timestamp": time.time(),
            "tier": self.current_tier.value,
            "origin_zone": self.origin_zone,
            "cloud_level": cloud_level,
            "turbulence_snapshot": zone_turbulence.copy(),
        }
        if extra:
            event.update(extra)
        return event

    def get_status(self) -> str:
        """Get human-readable status."""
        if self.state == BleedState.OFF:
            return "Bleed: OFF"
        elif self.state == BleedState.ACTIVE:
            duration = time.time() - self.active_since
            return f"Bleed: ACTIVE (Tier {self.current_tier.value}) - {duration:.1f}s - Origin: {self.origin_zone}"
        else:
            return f"Bleed: WINDDOWN ({self.winddown_remaining:.1f}s remaining)"

    def is_active(self) -> bool:
        """Check if bleed is currently active or winding down."""
        return self.state != BleedState.OFF

    def get_event_count(self) -> int:
        """Get total number of bleed events this session."""
        count = len(self.event_history)
        if self.current_event:
            count += 1
        return count


# ========== MODULE INTERFACE ==========

def create_bleed_system() -> BleedEventSystem:
    """Factory function to create Bleed Event system."""
    return BleedEventSystem()


if __name__ == "__main__":
    # Test Bleed system
    print("=" * 60)
    print("BLEED EVENT SYSTEM - V4 Renderist Mall OS")
    print("=" * 60)

    bleed = BleedEventSystem()

    # Mock zone data
    zone_turbulence = {
        "FOOD_COURT": 5.0,
        "SERVICE_HALL": 7.0,
        "CORRIDOR": 3.0,
    }
    zone_density = {
        "FOOD_COURT": 15,
        "SERVICE_HALL": 5,
        "CORRIDOR": 20,
    }

    print("\nSimulating Cloud pressure rising...")

    # Simulate pressure rise
    test_levels = [30, 45, 55, 62, 70, 78, 85, 92, 88, 72, 58, 45, 30]

    for level in test_levels:
        result = bleed.update(0.5, level, zone_turbulence, zone_density)

        print(f"\nCloud: {level}")
        print(f"  {bleed.get_status()}")

        for event in result["events"]:
            print(f"  EVENT: {event['type']} (tier {event['tier']})")

    # Let winddown complete
    print("\n--- Completing winddown ---")
    for _ in range(20):
        result = bleed.update(0.5, 30, zone_turbulence, zone_density)
        if result["events"]:
            for event in result["events"]:
                print(f"  EVENT: {event['type']}")
        if bleed.state == BleedState.OFF:
            break

    print(f"\nTotal bleed events: {bleed.get_event_count()}")
    print(f"\nDegradation profiles:")
    for tier in [BleedTier.TIER_1, BleedTier.TIER_2, BleedTier.TIER_3]:
        profile = DEGRADATION_PROFILES[tier]
        print(f"\n  Tier {tier.value}:")
        print(f"    VHS drag: {profile.vhs_drag}")
        print(f"    Flicker: {profile.flicker_intensity}")
        print(f"    Tile drift: {profile.tile_drift}")
