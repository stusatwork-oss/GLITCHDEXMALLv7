#!/usr/bin/env python3
"""
SPINE ANCHORS ↔ RETRO DISPATCH LOOP
Step 2 of 5-part integration

Treats NPC "never" rules (anchors) as sacred pre-conditions for state transitions.
Under Cloud pressure, anchors strain → degrade → break → tragedy.

Architecture:
- Anchors = behavioral invariants from NPCSpine
- Cloud pressure = strain on anchor integrity
- Tolerance = QBIT power-based resistance to breakdown
- Breakdown = predictable NPC collapse signature

Usage:
    from spine_anchor_dispatcher import dispatch_npc_action, AnchorBreakEvent

    result = dispatch_npc_action(
        npc=mall_cop_npc,
        action="enter_forbidden_zone",
        zone="FC-ARCADE",
        cloud_pressure=75.0
    )

    if result.blocked:
        print("Action blocked by spine anchor")
    elif result.anchor_broken:
        print(f"TRAGEDY: {result.broken_anchor} collapsed")

Reference:
- SPINES pitch deck
- Retro dispatcher rules
- QBIT integration summary
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class ActionResult(Enum):
    """Result of action dispatch."""
    ALLOW = "allow"                    # Action permitted
    BLOCK = "block"                    # Blocked by anchor
    DEGRADE_ANCHOR = "degrade"         # Anchor weakening but holding
    BREAK_ANCHOR = "break"             # Anchor shattered (contradiction)


@dataclass
class AnchorState:
    """
    Tracking state for a spine anchor.

    Attributes:
        anchor_text: The "never" rule text
        integrity: Structural integrity (0-100)
        strain_accumulation: Total strain applied
        break_threshold: Cloud pressure needed to break
        degradation_rate: How fast integrity decays under strain
    """
    anchor_text: str
    integrity: float = 100.0           # 0-100
    strain_accumulation: float = 0.0
    break_threshold: float = 75.0      # Cloud level when this breaks
    degradation_rate: float = 1.0      # Per-tick decay rate

    def apply_strain(self, cloud_pressure: float, qbit_power: int):
        """
        Apply Cloud pressure strain to anchor.

        High QBIT power provides resistance.
        """
        # Base strain = (cloud_pressure - 50) / 10 (negative if Cloud < 50)
        base_strain = max(0, (cloud_pressure - 50) / 10.0)

        # QBIT power reduces strain (high-power NPCs resist longer)
        resistance = qbit_power / 3000.0  # 0-1
        effective_strain = base_strain * (1.0 - resistance * 0.5)

        self.strain_accumulation += effective_strain

        # Degrade integrity
        if cloud_pressure > 60:
            self.integrity -= self.degradation_rate * effective_strain

        self.integrity = max(0, self.integrity)


@dataclass
class AnchorBreakEvent:
    """
    Record of an anchor breaking (contradiction event).

    Attributes:
        npc_id: NPC who broke the anchor
        anchor_text: The rule that was broken
        cloud_pressure: Cloud level at time of break
        zone_id: Where it happened
        timestamp: Game time
        narrative_impact: Story significance (0-1)
    """
    npc_id: str
    anchor_text: str
    cloud_pressure: float
    zone_id: str
    timestamp: float
    narrative_impact: float = 1.0


@dataclass
class DispatchResult:
    """
    Result of action dispatch through anchor system.

    Attributes:
        result: ALLOW | BLOCK | DEGRADE_ANCHOR | BREAK_ANCHOR
        blocked: Whether action was blocked
        anchor_broken: Whether anchor shattered
        broken_anchor: Text of broken anchor (if any)
        degradation_applied: Integrity lost (if degraded)
        message: Human-readable explanation
    """
    result: ActionResult
    blocked: bool = False
    anchor_broken: bool = False
    broken_anchor: Optional[str] = None
    degradation_applied: float = 0.0
    message: str = ""


class SpineAnchorDispatcher:
    """
    Dispatcher that enforces spine anchors as pre-conditions.

    This is the "sacred rules" system. NPCs CANNOT violate their
    "never" rules unless Cloud pressure overwhelms their anchor integrity.

    When an anchor breaks, it's a TRAGEDY - a predictable collapse signature.
    """

    def __init__(self):
        # Track anchor states per NPC
        self.anchor_states: Dict[str, Dict[str, AnchorState]] = {}

        # History of broken anchors
        self.break_events: List[AnchorBreakEvent] = []

    def initialize_npc_anchors(self, npc_id: str, never_rules: List[str], qbit_power: int):
        """
        Initialize anchor tracking for an NPC.

        Args:
            npc_id: NPC identifier
            never_rules: List of "never" rule texts
            qbit_power: QBIT power score (affects break threshold)
        """
        if npc_id not in self.anchor_states:
            self.anchor_states[npc_id] = {}

        for rule in never_rules:
            # Break threshold scales with QBIT power
            # High-power NPCs can resist until higher Cloud levels
            base_threshold = 75.0
            power_bonus = (qbit_power / 3000.0) * 15.0  # 0-15
            break_threshold = base_threshold + power_bonus

            self.anchor_states[npc_id][rule] = AnchorState(
                anchor_text=rule,
                break_threshold=break_threshold
            )

    def check_anchor_violation(
        self,
        npc,  # NPCSpine or NPCStateMachine
        action: str,
        context: Dict
    ) -> Optional[str]:
        """
        Check if action violates any "never" rules.

        Args:
            npc: NPC object with spine
            action: Action being attempted
            context: Additional context (zone_id, target, etc.)

        Returns:
            Violated anchor text, or None if no violation
        """
        spine = npc.spine if hasattr(npc, 'spine') else npc

        never_rules = spine.never_rules if hasattr(spine, 'never_rules') else []

        # Check zone violations
        zone_id = context.get('zone_id', '')
        if zone_id:
            forbidden_zones = spine.forbidden_zones if hasattr(spine, 'forbidden_zones') else []
            if zone_id in forbidden_zones:
                for rule in never_rules:
                    if zone_id.lower() in rule.lower() or "forbidden" in rule.lower():
                        return rule

        # Check spatial constraint violations
        if action == "enter_forbidden_zone" or action == "move_to_zone":
            for rule in never_rules:
                if "never enter" in rule.lower() or "never go to" in rule.lower():
                    if zone_id.lower() in rule.lower():
                        return rule

        # Check behavioral violations
        if action in ["abandon_post", "ignore_duty", "flee"]:
            for rule in never_rules:
                if "never abandon" in rule.lower() or "never leave" in rule.lower():
                    return rule

        return None

    def dispatch_action(
        self,
        npc,  # NPCSpine or NPCStateMachine
        action: str,
        context: Dict,
        cloud_pressure: float
    ) -> DispatchResult:
        """
        Dispatch an action through the anchor enforcement system.

        This is the core logic:
        1. Check if action violates anchor
        2. If no violation → ALLOW
        3. If violation:
           a. Check anchor integrity
           b. If integrity high → BLOCK
           c. If integrity degraded but holding → DEGRADE_ANCHOR
           d. If integrity broken → BREAK_ANCHOR (contradiction)

        Args:
            npc: NPC attempting action
            action: Action type
            context: Additional context
            cloud_pressure: Current Cloud level

        Returns:
            DispatchResult with action outcome
        """
        spine = npc.spine if hasattr(npc, 'spine') else npc
        npc_id = spine.npc_id if hasattr(spine, 'npc_id') else str(id(spine))
        qbit_power = spine.qbit_power if hasattr(spine, 'qbit_power') else 0

        # Initialize if needed
        never_rules = spine.never_rules if hasattr(spine, 'never_rules') else []
        if npc_id not in self.anchor_states and never_rules:
            self.initialize_npc_anchors(npc_id, never_rules, qbit_power)

        # Check for anchor violation
        violated_anchor = self.check_anchor_violation(npc, action, context)

        if not violated_anchor:
            return DispatchResult(
                result=ActionResult.ALLOW,
                message="No anchor violation"
            )

        # Anchor violation detected - check integrity
        if npc_id in self.anchor_states and violated_anchor in self.anchor_states[npc_id]:
            anchor = self.anchor_states[npc_id][violated_anchor]

            # Apply strain
            anchor.apply_strain(cloud_pressure, qbit_power)

            # Check if anchor breaks
            if cloud_pressure >= anchor.break_threshold and anchor.integrity < 30:
                # ANCHOR BREAKS - TRAGEDY
                self.break_events.append(AnchorBreakEvent(
                    npc_id=npc_id,
                    anchor_text=violated_anchor,
                    cloud_pressure=cloud_pressure,
                    zone_id=context.get('zone_id', 'UNKNOWN'),
                    timestamp=context.get('game_time', 0),
                    narrative_impact=qbit_power / 3000.0  # Higher power = more tragic
                ))

                return DispatchResult(
                    result=ActionResult.BREAK_ANCHOR,
                    anchor_broken=True,
                    broken_anchor=violated_anchor,
                    message=f"ANCHOR SHATTERED: '{violated_anchor}' collapsed at Cloud {cloud_pressure:.1f}"
                )

            # Anchor holding but degrading
            elif anchor.integrity < 70:
                return DispatchResult(
                    result=ActionResult.DEGRADE_ANCHOR,
                    blocked=True,
                    degradation_applied=anchor.degradation_rate,
                    message=f"Anchor degrading (integrity: {anchor.integrity:.1f}%), action blocked"
                )

            # Anchor intact - BLOCK
            else:
                return DispatchResult(
                    result=ActionResult.BLOCK,
                    blocked=True,
                    message=f"Action blocked by spine anchor: '{violated_anchor}'"
                )
        else:
            # No anchor state tracked (shouldn't happen, but default to block)
            return DispatchResult(
                result=ActionResult.BLOCK,
                blocked=True,
                message=f"Action violates spine rule: '{violated_anchor}'"
            )

    def get_anchor_integrity(self, npc_id: str, anchor_text: str) -> float:
        """Get current integrity of a specific anchor."""
        if npc_id in self.anchor_states and anchor_text in self.anchor_states[npc_id]:
            return self.anchor_states[npc_id][anchor_text].integrity
        return 100.0

    def get_break_events_for_npc(self, npc_id: str) -> List[AnchorBreakEvent]:
        """Get all anchor break events for an NPC."""
        return [event for event in self.break_events if event.npc_id == npc_id]

    def get_narrative_tragedy_score(self) -> float:
        """
        Calculate narrative weight of all anchor breaks.

        High-power NPCs breaking anchors = high tragedy.
        Returns 0-1 scale.
        """
        if not self.break_events:
            return 0.0

        total_impact = sum(event.narrative_impact for event in self.break_events)
        return min(1.0, total_impact / 10.0)  # Cap at 1.0


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def dispatch_npc_action(npc, action: str, zone: str, cloud_pressure: float) -> DispatchResult:
    """
    Convenience wrapper for action dispatch.

    Args:
        npc: NPCSpine or NPCStateMachine
        action: Action type
        zone: Target zone ID
        cloud_pressure: Current Cloud level

    Returns:
        DispatchResult
    """
    dispatcher = SpineAnchorDispatcher()

    spine = npc.spine if hasattr(npc, 'spine') else npc
    npc_id = spine.npc_id if hasattr(spine, 'npc_id') else str(id(spine))
    never_rules = spine.never_rules if hasattr(spine, 'never_rules') else []
    qbit_power = spine.qbit_power if hasattr(spine, 'qbit_power') else 0

    if never_rules:
        dispatcher.initialize_npc_anchors(npc_id, never_rules, qbit_power)

    return dispatcher.dispatch_action(
        npc,
        action,
        {"zone_id": zone},
        cloud_pressure
    )


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    from npc_state_machine import NPCSpine

    print("="*60)
    print("SPINE ANCHOR DISPATCHER TEST")
    print("="*60)

    # Create Mall Cop with "never abandon post" anchor
    mall_cop = NPCSpine(
        npc_id="mall-cop-01",
        name="Mall Cop",
        role="Primary",
        never_rules=["Never abandon post at main entrance"],
        qbit_power=1200
    )

    dispatcher = SpineAnchorDispatcher()
    dispatcher.initialize_npc_anchors(
        mall_cop.npc_id,
        mall_cop.never_rules,
        mall_cop.qbit_power
    )

    # Test 1: Low Cloud - Anchor holds
    print("\n--- Test 1: Cloud = 50 (UNEASY) ---")
    result = dispatcher.dispatch_action(
        mall_cop,
        "abandon_post",
        {"zone_id": "SERVICE_HALL"},
        cloud_pressure=50.0
    )
    print(f"  Result: {result.result.value}")
    print(f"  Blocked: {result.blocked}")
    print(f"  Message: {result.message}")

    # Test 2: Medium Cloud - Anchor degrades
    print("\n--- Test 2: Cloud = 70 (STRAINED) ---")
    result = dispatcher.dispatch_action(
        mall_cop,
        "abandon_post",
        {"zone_id": "SERVICE_HALL"},
        cloud_pressure=70.0
    )
    print(f"  Result: {result.result.value}")
    print(f"  Blocked: {result.blocked}")
    print(f"  Message: {result.message}")
    integrity = dispatcher.get_anchor_integrity(mall_cop.npc_id, mall_cop.never_rules[0])
    print(f"  Anchor Integrity: {integrity:.1f}%")

    # Test 3: High Cloud - Anchor breaks
    print("\n--- Test 3: Cloud = 85 (CRITICAL) ---")
    # Apply more strain
    for _ in range(5):
        dispatcher.dispatch_action(
            mall_cop,
            "abandon_post",
            {"zone_id": "SERVICE_HALL"},
            cloud_pressure=85.0
        )

    result = dispatcher.dispatch_action(
        mall_cop,
        "abandon_post",
        {"zone_id": "SERVICE_HALL", "game_time": 120.0},
        cloud_pressure=85.0
    )
    print(f"  Result: {result.result.value}")
    print(f"  Anchor Broken: {result.anchor_broken}")
    print(f"  Broken Anchor: {result.broken_anchor}")
    print(f"  Message: {result.message}")

    # Show break events
    print("\n--- Anchor Break History ---")
    events = dispatcher.get_break_events_for_npc(mall_cop.npc_id)
    for event in events:
        print(f"  {event.npc_id}: '{event.anchor_text}'")
        print(f"    Cloud: {event.cloud_pressure:.1f}")
        print(f"    Zone: {event.zone_id}")
        print(f"    Narrative Impact: {event.narrative_impact:.2f}")

    print("\n" + "="*60)
    print("ANCHORS NOW BEHAVE LIKE SACRED RULES")
    print("Cloud rises → Anchors strain → Break → Tragedy")
    print("="*60)
