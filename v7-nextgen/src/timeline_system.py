#!/usr/bin/env python3
"""
TIMELINE SYSTEM - V7 NextGen
Multi-era timeline support integrated with Cloud/mood states.

Per user answer 8-B: Use Cloud/mood states to toggle between eras dynamically.

Eras: 1981 (Opening), 1995 (Peak), 2005 (Decline), 2011 (Closure)
Contradictions between eras are CANON, not errors.
"""

import json
import random
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

try:
    from measurements_loader import load_measurements
except ImportError:
    load_measurements = None


# ============================================================================
# ERA DEFINITIONS
# ============================================================================

class MallEra(Enum):
    """Four canonical eras of Eastland Mall."""
    OPENING_1981 = "1981"
    PEAK_1995 = "1995"
    DECLINE_2005 = "2005"
    CLOSURE_2011 = "2011"


@dataclass
class EraState:
    """State configuration for a specific era."""
    era: MallEra
    year: int
    mood_baseline: str  # CALM, UNEASY, STRAINED, CRITICAL
    cloud_pressure_baseline: float  # 0-100

    # Visual state
    tensile_roof_condition: str
    fountain_status: str
    lighting_quality: str
    store_occupancy_percent: float

    # Atmospheric
    description: str
    narrative_tone: str

    # Vendor states (food court)
    food_court_vendors: Dict[str, str]  # name -> status

    # Entity behaviors
    entity_state_overrides: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# ERA CONFIGURATIONS
# ============================================================================

ERA_1981 = EraState(
    era=MallEra.OPENING_1981,
    year=1981,
    mood_baseline="CALM",
    cloud_pressure_baseline=10.0,
    tensile_roof_condition="Brilliant white, pristine, new fabric",
    fountain_status="Operational - crystalline water, clean tiers",
    lighting_quality="Bright, steady, everything new",
    store_occupancy_percent=100.0,
    description="Opening year - optimistic, futurist, experimental architecture fresh and new",
    narrative_tone="The white tensile canopy stretches overhead like a sail catching the future. Everything gleams. This is what tomorrow was supposed to look like.",
    food_court_vendors={
        "Slush Puppy Paradise": "Opening soon",
        "Wok This Way": "Opening soon",
        "Pizza Planet Express": "Opening soon",
        "Pretzel Hut": "Coming soon",
        "Burger Bunker": "Opening soon",
        "Taco Tiempo": "Opening soon"
    },
    entity_state_overrides={
        "food-court-neon-sign": {"state": "Fully operational - bright, steady glow"},
        "tensile-roof-mast": {"condition": "New steel, bright yellow paint"},
        "the-janitor": {"present": False, "note": "Not yet hired"}
    }
)

ERA_1995 = EraState(
    era=MallEra.PEAK_1995,
    year=1995,
    mood_baseline="CALM",
    cloud_pressure_baseline=15.0,
    tensile_roof_condition="White with slight aging, well-maintained",
    fountain_status="Operational - some algae buildup, still running",
    lighting_quality="Bright, minor flickering in some areas",
    store_occupancy_percent=95.0,
    description="Peak era - bustling, fully occupied, mall at its apex",
    narrative_tone="The food court hums with activity. Lines at every vendor. The neon sign glows steady. This is the mall at its apex - when the vision still held.",
    food_court_vendors={
        "Slush Puppy Paradise": "Operational - busy",
        "Wok This Way": "Operational - busy",
        "Pizza Planet Express": "Operational - busy",
        "Pretzel Hut": "Never opened (CONTRADICTION: 'COMING SOON' + 'NOW CLOSED')",
        "Burger Bunker": "Operational - busy",
        "Taco Tiempo": "Operational - moderate"
    },
    entity_state_overrides={
        "food-court-neon-sign": {"state": "Operational with minor degradation"},
        "coca-cola-store": {"status": "Operational - peak corporate retail"},
        "the-janitor": {"present": True, "routine": "Established patterns"}
    }
)

ERA_2005 = EraState(
    era=MallEra.DECLINE_2005,
    year=2005,
    mood_baseline="UNEASY",
    cloud_pressure_baseline=35.0,
    tensile_roof_condition="Yellowing/beige, fabric aging visible",
    fountain_status="Dry or intermittent - tiers bone-dry most of time",
    lighting_quality="Flickering fluorescents, some sections dark",
    store_occupancy_percent=50.0,
    description="Decline period - vacancies appearing, atmosphere shift, something wrong here",
    narrative_tone="Half the storefronts dark behind security grates. The fountain tiers are dry. The neon sign flickers - blue arc stutters, catches, holds. Something feels wrong.",
    food_court_vendors={
        "Slush Puppy Paradise": "Operational - slow",
        "Wok This Way": "Closed - gate down",
        "Pizza Planet Express": "Closed - gate down",
        "Pretzel Hut": "Never opened (sign: 'COMING SOON!' + 'NOW CLOSED' taped over)",
        "Burger Bunker": "Closed - gate down",
        "Taco Tiempo": "Closed - gate down"
    },
    entity_state_overrides={
        "food-court-neon-sign": {"state": "Flickering, partial failure", "cloud_sensitivity": "High"},
        "coca-cola-store": {"status": "Recently closed or closing"},
        "the-janitor": {"present": True, "behavior": "Mops floors no one walks on"}
    }
)

ERA_2011 = EraState(
    era=MallEra.CLOSURE_2011,
    year=2011,
    mood_baseline="STRAINED",
    cloud_pressure_baseline=55.0,
    tensile_roof_condition="Heavily degraded, tears visible, structural concerns",
    fountain_status="Completely dry - dust in basin, dead leaves in tiers",
    lighting_quality="Many lights out, emergency lighting only in sections",
    store_occupancy_percent=10.0,
    description="Closure year - abandoned, memorial, temporal horror of watching the future die",
    narrative_tone="The escalators are silent. Only one theater screen flickers. The janitor still comes. This is what happens when the future dies - it becomes a monument to itself.",
    food_court_vendors={
        "Slush Puppy Paradise": "Closed - equipment removed",
        "Wok This Way": "Closed - vacant",
        "Pizza Planet Express": "Closed - vacant",
        "Pretzel Hut": "Never opened (paradox persists)",
        "Burger Bunker": "Closed - clearance signs",
        "Taco Tiempo": "Closed - vacant"
    },
    entity_state_overrides={
        "food-court-neon-sign": {"state": "Strobing, unstable, sections dark"},
        "coca-cola-store": {"status": "Closed - empty storefront"},
        "the-janitor": {"present": True, "behavior": "Ritual maintenance of empty space"}
    }
)


# ============================================================================
# TIMELINE MANAGER
# ============================================================================

class TimelineManager:
    """
    Manages multi-era timeline system.

    Integrates with Cloud state (user answer 8-B):
    - Cloud mood can trigger era shifts
    - Player discoveries can unlock era transitions
    - Contradictions between eras are preserved as features
    """

    def __init__(self, initial_era: MallEra = MallEra.PEAK_1995):
        self.current_era = initial_era
        self.era_states = {
            MallEra.OPENING_1981: ERA_1981,
            MallEra.PEAK_1995: ERA_1995,
            MallEra.DECLINE_2005: ERA_2005,
            MallEra.CLOSURE_2011: ERA_2011
        }
        self.unlocked_eras = {MallEra.PEAK_1995}  # Start with 1995 unlocked
        self.era_transition_history = [initial_era]

        # Load measurements for context
        if load_measurements:
            self.ml = load_measurements()
            self.contradictions = self.ml.get_timeline_contradictions()
        else:
            self.ml = None
            self.contradictions = {}

    def get_current_era_state(self) -> EraState:
        """Get current era configuration."""
        return self.era_states[self.current_era]

    def transition_to_era(self, new_era: MallEra, force: bool = False) -> bool:
        """
        Transition to a different era.

        Args:
            new_era: Target era
            force: If True, skip unlock check

        Returns:
            True if transition succeeded
        """
        if not force and new_era not in self.unlocked_eras:
            return False

        self.current_era = new_era
        self.era_transition_history.append(new_era)
        return True

    def unlock_era(self, era: MallEra):
        """Unlock an era for future transitions."""
        self.unlocked_eras.add(era)

    def get_vendor_state(self, vendor_name: str) -> str:
        """Get vendor operational state for current era."""
        era_state = self.get_current_era_state()
        return era_state.food_court_vendors.get(vendor_name, "Unknown")

    def get_entity_state_override(self, entity_id: str) -> Optional[Dict]:
        """Get era-specific entity state override."""
        era_state = self.get_current_era_state()
        return era_state.entity_state_overrides.get(entity_id)

    def get_cloud_baseline_for_era(self) -> float:
        """Get baseline Cloud pressure for current era."""
        return self.get_current_era_state().cloud_pressure_baseline

    def get_mood_baseline_for_era(self) -> str:
        """Get baseline mood for current era."""
        return self.get_current_era_state().mood_baseline

    # ========================================================================
    # ERA TRANSITION TRIGGERS
    # ========================================================================

    def check_cloud_triggered_transition(self, cloud_pressure: float) -> Optional[MallEra]:
        """
        Check if Cloud state should trigger era transition.

        High Cloud pressure might cause temporal bleeding:
        - 75-100 (CRITICAL): Random era transitions
        - 50-74 (STRAINED): Transition to decline eras
        - 25-49 (UNEASY): Transition between peak/decline
        - 0-24 (CALM): Stable in current era
        """
        if cloud_pressure >= 75 and MallEra.CLOSURE_2011 in self.unlocked_eras:
            # CRITICAL: Temporal chaos - random era
            import random
            return random.choice(list(self.unlocked_eras))
        elif cloud_pressure >= 50:
            # STRAINED: Pull toward decline
            if MallEra.CLOSURE_2011 in self.unlocked_eras:
                return MallEra.CLOSURE_2011
            elif MallEra.DECLINE_2005 in self.unlocked_eras:
                return MallEra.DECLINE_2005
        elif cloud_pressure >= 25:
            # UNEASY: Shift between peak/decline
            if self.current_era == MallEra.PEAK_1995 and MallEra.DECLINE_2005 in self.unlocked_eras:
                return MallEra.DECLINE_2005

        return None  # No transition

    def check_discovery_triggered_transition(self, discovery: str) -> Optional[MallEra]:
        """
        Check if player discovery should unlock/trigger era transition.

        Example discoveries:
        - "pretzel_hut_paradox" -> Unlock 2005 (see the contradiction)
        - "janitor_memory" -> Unlock 1981 (see the beginning)
        - "final_clearance_sign" -> Unlock 2011 (see the end)
        """
        discovery_triggers = {
            "pretzel_hut_paradox": MallEra.DECLINE_2005,
            "dry_fountain": MallEra.DECLINE_2005,
            "janitor_memory": MallEra.OPENING_1981,
            "pristine_mast": MallEra.OPENING_1981,
            "final_clearance_sign": MallEra.CLOSURE_2011,
            "silent_escalators": MallEra.CLOSURE_2011,
            "theater_marquee_flicker": MallEra.DECLINE_2005
        }

        if discovery in discovery_triggers:
            era = discovery_triggers[discovery]
            self.unlock_era(era)
            return era

        return None

    # ========================================================================
    # NARRATIVE HELPERS
    # ========================================================================

    def get_narrative_context(self) -> Dict[str, Any]:
        """Get narrative context for LLM DM."""
        era_state = self.get_current_era_state()
        return {
            "era": era_state.era.value,
            "year": era_state.year,
            "description": era_state.description,
            "narrative_tone": era_state.narrative_tone,
            "roof_condition": era_state.tensile_roof_condition,
            "fountain_status": era_state.fountain_status,
            "lighting": era_state.lighting_quality,
            "occupancy": f"{era_state.store_occupancy_percent}%"
        }

    def get_contradictions_description(self) -> str:
        """Get contradiction philosophy description."""
        if self.contradictions:
            return self.contradictions.get("note", "Contradictions are timeline variance.")
        return "All eras are canon. Contradictions reveal layers, not errors."

    # ========================================================================
    # EXPORT
    # ========================================================================

    def export_state(self) -> Dict:
        """Export timeline state for save/load."""
        return {
            "current_era": self.current_era.value,
            "unlocked_eras": [e.value for e in self.unlocked_eras],
            "transition_history": [e.value for e in self.era_transition_history]
        }

    def import_state(self, state: Dict):
        """Import timeline state from save."""
        self.current_era = MallEra(state["current_era"])
        self.unlocked_eras = {MallEra(e) for e in state["unlocked_eras"]}
        self.era_transition_history = [MallEra(e) for e in state["transition_history"]]


# ============================================================================
# CLI TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TIMELINE SYSTEM - MULTI-ERA MALL")
    print("=" * 80)

    tm = TimelineManager(initial_era=MallEra.PEAK_1995)

    print("\n[CURRENT ERA]")
    context = tm.get_narrative_context()
    print(f"Era: {context['year']} - {context['description']}")
    print(f"Narrative: {context['narrative_tone'][:80]}...")

    print("\n[VENDOR STATES]")
    vendors = ["Slush Puppy Paradise", "Wok This Way", "Pretzel Hut"]
    for vendor in vendors:
        state = tm.get_vendor_state(vendor)
        print(f"  {vendor}: {state}")

    print("\n[ERA UNLOCK SIMULATION]")
    tm.unlock_era(MallEra.DECLINE_2005)
    print("Unlocked: 2005 (Decline)")

    tm.transition_to_era(MallEra.DECLINE_2005)
    print(f"Transitioned to: {tm.current_era.value}")

    context = tm.get_narrative_context()
    print(f"Narrative: {context['narrative_tone'][:80]}...")

    print("\n[CLOUD-TRIGGERED TRANSITION]")
    cloud_pressure = 78.0  # CRITICAL
    suggested_era = tm.check_cloud_triggered_transition(cloud_pressure)
    if suggested_era:
        print(f"Cloud pressure {cloud_pressure} suggests transition to: {suggested_era.value}")

    print("\n[CONTRADICTIONS]")
    print(tm.get_contradictions_description())

    print("\n" + "=" * 80)
    print("TIMELINE SYSTEM READY")
    print("=" * 80)
