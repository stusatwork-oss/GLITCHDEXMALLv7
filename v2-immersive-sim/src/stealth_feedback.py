"""
STEALTH FEEDBACK SYSTEM - ANSI Alert Symbols for Wolf3D
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Minimal visual feedback for the AAA stealth system hiding underneath.

No modern UI. Just ASCII symbols:
- ! = Fully alerted (NPC sees player)
- ? = Suspicious (investigating, heard something)
- ~ = Noise ripple (sound propagation)

This is Metal Gear Solid rendered in ANSI terminal art.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class AlertSymbol(Enum):
    """Alert symbols shown above NPCs"""
    NONE = ""
    ALERT = "!"  # Fully alerted, sees player
    SUSPICIOUS = "?"  # Investigating, heard something
    SEARCHING = "??"  # Actively searching
    DETECTED = "!!"  # Just spotted player


@dataclass
class NoiseRipple:
    """Visual representation of noise propagating"""
    position: Tuple[int, int, int]
    timestamp: float
    radius: float
    max_radius: float
    duration: float = 2.0  # How long the ripple lasts
    intensity: float = 1.0  # Visual intensity

    def get_current_radius(self) -> float:
        """Get current radius based on time elapsed"""
        elapsed = time.time() - self.timestamp
        if elapsed >= self.duration:
            return self.max_radius
        # Expand over duration
        return (elapsed / self.duration) * self.max_radius

    def is_expired(self) -> bool:
        """Check if ripple has finished expanding"""
        return time.time() - self.timestamp >= self.duration


class StealthFeedbackSystem:
    """
    Provides minimal visual feedback for stealth mechanics.

    Philosophy:
    - No modern UI overlays
    - Just ASCII symbols above NPCs
    - Noise ripples as ~ characters expanding outward
    - Metal Gear Solid stealth in Wolf3D terminal art
    """

    def __init__(self):
        # Active noise ripples
        self.noise_ripples: List[NoiseRipple] = []

        # NPC alert states (for symbol display)
        self.npc_alert_symbols: Dict[str, AlertSymbol] = {}

        # Alert state durations
        self.alert_symbol_duration = 3.0  # Symbols fade after 3 seconds
        self.alert_symbol_timestamps: Dict[str, float] = {}

    def update(self, dt: float):
        """Update stealth feedback visuals"""
        # Remove expired noise ripples
        current_time = time.time()
        self.noise_ripples = [r for r in self.noise_ripples if not r.is_expired()]

        # Fade alert symbols over time
        expired_npcs = []
        for npc_id, timestamp in self.alert_symbol_timestamps.items():
            if current_time - timestamp > self.alert_symbol_duration:
                expired_npcs.append(npc_id)

        for npc_id in expired_npcs:
            if npc_id in self.npc_alert_symbols:
                del self.npc_alert_symbols[npc_id]
            del self.alert_symbol_timestamps[npc_id]

    def add_noise_ripple(self, position: Tuple[int, int, int], radius: float, intensity: float = 1.0):
        """
        Add a noise ripple at a position.

        Args:
            position: World position where noise originated
            radius: Maximum radius of noise propagation
            intensity: How loud (affects visual intensity)
        """
        ripple = NoiseRipple(
            position=position,
            timestamp=time.time(),
            radius=0.0,
            max_radius=radius,
            intensity=intensity
        )
        self.noise_ripples.append(ripple)

    def set_npc_alert_symbol(self, npc_id: str, symbol: AlertSymbol, duration: Optional[float] = None):
        """
        Set an alert symbol for an NPC.

        Args:
            npc_id: NPC identifier
            symbol: Alert symbol to show
            duration: How long to show symbol (None = use default)
        """
        if symbol == AlertSymbol.NONE:
            # Clear symbol
            if npc_id in self.npc_alert_symbols:
                del self.npc_alert_symbols[npc_id]
            if npc_id in self.alert_symbol_timestamps:
                del self.alert_symbol_timestamps[npc_id]
            return

        self.npc_alert_symbols[npc_id] = symbol
        self.alert_symbol_timestamps[npc_id] = time.time()

    def update_npc_alerts_from_awareness(self, npc_id: str, awareness_level: float, investigating: bool = False):
        """
        Update NPC alert symbol based on awareness level.

        Args:
            npc_id: NPC identifier
            awareness_level: 0.0 to 1.0 awareness
            investigating: Is NPC investigating something?
        """
        if awareness_level >= 0.8:
            # Fully alerted - sees player
            self.set_npc_alert_symbol(npc_id, AlertSymbol.ALERT)
        elif awareness_level >= 0.5:
            # Just detected
            self.set_npc_alert_symbol(npc_id, AlertSymbol.DETECTED)
        elif awareness_level >= 0.3 or investigating:
            # Suspicious
            symbol = AlertSymbol.SEARCHING if investigating else AlertSymbol.SUSPICIOUS
            self.set_npc_alert_symbol(npc_id, symbol)
        else:
            # Not alerted
            self.set_npc_alert_symbol(npc_id, AlertSymbol.NONE)

    def get_npc_alert_symbol(self, npc_id: str) -> str:
        """Get the alert symbol to display for an NPC"""
        symbol = self.npc_alert_symbols.get(npc_id, AlertSymbol.NONE)
        return symbol.value

    def get_noise_ripples_rendering_data(self) -> List[Dict[str, Any]]:
        """
        Get rendering data for noise ripples.

        Returns list of ripples with position, current radius, intensity.
        """
        ripples = []
        for ripple in self.noise_ripples:
            # Calculate fade
            elapsed = time.time() - ripple.timestamp
            fade = 1.0 - (elapsed / ripple.duration)  # Fade out over duration

            ripples.append({
                "position": ripple.position,
                "current_radius": ripple.get_current_radius(),
                "max_radius": ripple.max_radius,
                "intensity": ripple.intensity * fade,
                "symbol": "~"  # ASCII wave character
            })

        return ripples

    def get_all_rendering_data(self) -> Dict[str, Any]:
        """
        Get all stealth feedback rendering data.

        Returns:
            Dict with npc_symbols and noise_ripples
        """
        return {
            "npc_alert_symbols": {
                npc_id: symbol.value
                for npc_id, symbol in self.npc_alert_symbols.items()
            },
            "noise_ripples": self.get_noise_ripples_rendering_data()
        }

    def clear_all(self):
        """Clear all stealth feedback (for testing/reset)"""
        self.noise_ripples.clear()
        self.npc_alert_symbols.clear()
        self.alert_symbol_timestamps.clear()


# Helper function for common noise events
def create_noise_for_action(action_type: str) -> Tuple[float, float]:
    """
    Get noise radius and intensity for common actions.

    Returns:
        (radius, intensity) tuple
    """
    noise_profiles = {
        "footstep": (2.0, 0.2),
        "run": (4.0, 0.4),
        "kick": (8.0, 0.6),
        "break_glass": (15.0, 0.9),
        "vending_machine": (10.0, 0.7),
        "alarm": (30.0, 1.0),
        "throw": (6.0, 0.5),
        "door_slam": (12.0, 0.7),
    }
    return noise_profiles.get(action_type, (5.0, 0.5))
