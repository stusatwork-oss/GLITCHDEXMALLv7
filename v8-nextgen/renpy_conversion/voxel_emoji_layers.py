#!/usr/bin/env python3
"""
VOXEL EMOJI LAYERS
Multi-layer semantic encoding using emoji symbols.

Instead of text labels, voxels have emoji-encoded properties:
  Material layer: 🧱 💎 🟫 🌳
  State layer: 🔥 ❄️ 💧 ⚡
  Behavior layer: 🚪 🪜 💡 🔒
  Surface layer: ✨ 🌫️ 💨 🌊

Each voxel = position + emoji layers + metadata

Example voxel:
  Position: (10, 20, 0)
  Material: 💎 (glass)
  State: 💧 (wet)
  Behavior: 💡 (emits light)
  Surface: ✨ (shiny)

  Compact encoding: 💎💧💡✨
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
from enum import IntEnum


# ============================================================================
# EMOJI LAYER DEFINITIONS
# ============================================================================

class LayerType(IntEnum):
    """Voxel layer types."""
    MATERIAL = 0    # What it's made of
    STATE = 1       # Current condition
    BEHAVIOR = 2    # How it acts
    SURFACE = 3     # Visual appearance
    AUDIO = 4       # Sound properties
    PHYSICS = 5     # Physical properties


# MATERIAL LAYER (What is it made of?)
MATERIAL_EMOJI = {
    # Building materials
    '🧱': 'BRICK',
    '💎': 'GLASS',
    '🟫': 'WOOD',
    '🌳': 'WOOD_NATURAL',
    '⬛': 'CONCRETE',
    '🟨': 'METAL_STEEL',
    '🟦': 'METAL_ALUMINUM',

    # Tiles & flooring
    '⬜': 'TILE_WHITE',
    '🟧': 'TILE_TERRACOTTA',
    '🟥': 'CARPET_RED',
    '🟩': 'CARPET_GREEN',
    '🟪': 'CARPET_PURPLE',

    # Special materials
    '💧': 'WATER',
    '🌫️': 'FOG_VOLUME',
    '💨': 'AIR',
    '🔲': 'VOID',

    # Mall-specific
    '🪟': 'GLASS_BLOCK',
    '🏪': 'STOREFRONT',
    '🚪': 'DOOR_MATERIAL',
    '🪜': 'METAL_GRATE',
}

# STATE LAYER (What condition is it in?)
STATE_EMOJI = {
    # Temperature
    '🔥': 'HOT',
    '❄️': 'COLD',
    '🌡️': 'WARM',
    '🧊': 'FROZEN',

    # Moisture
    '💧': 'WET',
    '💦': 'DRIPPING',
    '🌊': 'FLOODED',
    '☁️': 'DRY',

    # Energy
    '⚡': 'POWERED',
    '🔋': 'CHARGED',
    '💀': 'DEAD',
    '🔌': 'UNPLUGGED',

    # Condition
    '✨': 'PRISTINE',
    '🧹': 'CLEAN',
    '💩': 'DIRTY',
    '🦠': 'CONTAMINATED',
    '🩹': 'DAMAGED',
    '💔': 'BROKEN',

    # Temporal
    '🕐': 'ACTIVE',
    '⏸️': 'PAUSED',
    '⏹️': 'STOPPED',
    '🔄': 'CYCLING',
}

# BEHAVIOR LAYER (What does it do?)
BEHAVIOR_EMOJI = {
    # Interactive
    '🚪': 'DOOR',
    '🪜': 'CLIMBABLE',
    '🪑': 'SITTABLE',
    '🛏️': 'SLEEPABLE',
    '🚿': 'CLEANABLE',

    # Light & visual
    '💡': 'LIGHT_SOURCE',
    '🔦': 'DIRECTIONAL_LIGHT',
    '🌟': 'GLOW',
    '👁️': 'VISIBLE',
    '👻': 'INVISIBLE',

    # Physics
    '🔒': 'SOLID',
    '🌬️': 'PASSABLE',
    '⬆️': 'FLOATS',
    '⬇️': 'SINKS',
    '🌀': 'ROTATES',

    # Interactive systems
    '🔊': 'AUDIO_TRIGGER',
    '📡': 'SENSOR',
    '⚙️': 'MECHANICAL',
    '🎛️': 'CONTROLLABLE',

    # Mall-specific
    '🛒': 'PUSHABLE',
    '🪙': 'COLLECTIBLE',
    '🎫': 'TICKET_REQUIRED',
    '🔑': 'KEY_REQUIRED',
}

# SURFACE LAYER (How does it look?)
SURFACE_EMOJI = {
    # Texture
    '✨': 'SHINY',
    '🌟': 'SPARKLY',
    '💫': 'GLITTERY',
    '🌫️': 'FOGGY',
    '💨': 'DUSTY',
    '🕸️': 'COBWEBBED',

    # Reflectivity
    '🪞': 'MIRROR',
    '💎': 'REFLECTIVE',
    '🌑': 'MATTE',
    '🌓': 'SEMI_GLOSS',

    # Patterns
    '🎨': 'PAINTED',
    '🖼️': 'TEXTURED',
    '📐': 'GEOMETRIC',
    '🌈': 'RAINBOW',

    # Effects
    '💧': 'DROPLETS',
    '🔥': 'FLAMES',
    '⚡': 'ELECTRIC',
    '🌊': 'RIPPLES',
}

# AUDIO LAYER (What does it sound like?)
AUDIO_EMOJI = {
    # Ambient
    '🔇': 'SILENT',
    '🔉': 'QUIET',
    '🔊': 'LOUD',
    '📢': 'AMPLIFIED',
    '🌬️': 'WIND',
    '👻': 'EERIE',

    # Tones
    '🎵': 'MUSICAL',
    '🎶': 'MELODIC',
    '🥁': 'RHYTHMIC',
    '📻': 'STATIC',

    # Mall sounds
    '🛎️': 'BELL',
    '⏰': 'ALARM',
    '📞': 'PHONE_RING',
    '🚨': 'SIREN',
    '💧': 'DRIPPING',
    '🌊': 'FLOWING_WATER',

    # Mechanical
    '⚙️': 'MECHANICAL_HUM',
    '🚗': 'ENGINE',
    '🔔': 'CHIME',
}

# PHYSICS LAYER (Physical properties)
PHYSICS_EMOJI = {
    # Density
    '🪨': 'HEAVY',
    '🪶': 'LIGHT',
    '💨': 'WEIGHTLESS',
    '⚓': 'DENSE',

    # Interaction
    '🧲': 'MAGNETIC',
    '⚡': 'CONDUCTIVE',
    '🛡️': 'PROTECTIVE',
    '💥': 'EXPLOSIVE',
    '🧊': 'SLIPPERY',
    '🍯': 'STICKY',
    '🌬️': 'PASSABLE',

    # Movement
    '🏃': 'FAST',
    '🐌': 'SLOW',
    '🛑': 'STOPPED',
    '🌀': 'SPINNING',
    '⬇️': 'SINKS',
    '⬆️': 'FLOATS',
}


# ============================================================================
# VOXEL LAYER ENCODING
# ============================================================================

@dataclass
class VoxelLayers:
    """Multi-layer emoji encoding for a single voxel."""
    position: Tuple[float, float, float]  # (x, y, z) in feet
    material: Optional[str] = None         # Material emoji
    state: Optional[str] = None            # State emoji
    behavior: Optional[str] = None         # Behavior emoji
    surface: Optional[str] = None          # Surface emoji
    audio: Optional[str] = None            # Audio emoji
    physics: Optional[str] = None          # Physics emoji

    def to_compact(self) -> str:
        """
        Compact representation: concatenate all emoji.

        Example: 💎💧💡✨ = glass, wet, light-emitting, shiny
        """
        layers = [
            self.material or '',
            self.state or '',
            self.behavior or '',
            self.surface or '',
            self.audio or '',
            self.physics or ''
        ]
        return ''.join(filter(None, layers))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with readable names."""
        return {
            'position': self.position,
            'material': {
                'emoji': self.material,
                'name': MATERIAL_EMOJI.get(self.material, 'UNKNOWN')
            } if self.material else None,
            'state': {
                'emoji': self.state,
                'name': STATE_EMOJI.get(self.state, 'UNKNOWN')
            } if self.state else None,
            'behavior': {
                'emoji': self.behavior,
                'name': BEHAVIOR_EMOJI.get(self.behavior, 'UNKNOWN')
            } if self.behavior else None,
            'surface': {
                'emoji': self.surface,
                'name': SURFACE_EMOJI.get(self.surface, 'UNKNOWN')
            } if self.surface else None,
            'audio': {
                'emoji': self.audio,
                'name': AUDIO_EMOJI.get(self.audio, 'UNKNOWN')
            } if self.audio else None,
            'physics': {
                'emoji': self.physics,
                'name': PHYSICS_EMOJI.get(self.physics, 'UNKNOWN')
            } if self.physics else None,
        }

    @classmethod
    def from_compact(cls, position: Tuple[float, float, float], compact: str) -> 'VoxelLayers':
        """
        Parse compact emoji string back to layers.

        Note: Order matters - must match layer order
        """
        # Simple implementation: first emoji of each type found
        material = None
        state = None
        behavior = None
        surface = None
        audio = None
        physics = None

        for char in compact:
            if char in MATERIAL_EMOJI and not material:
                material = char
            elif char in STATE_EMOJI and not state:
                state = char
            elif char in BEHAVIOR_EMOJI and not behavior:
                behavior = char
            elif char in SURFACE_EMOJI and not surface:
                surface = char
            elif char in AUDIO_EMOJI and not audio:
                audio = char
            elif char in PHYSICS_EMOJI and not physics:
                physics = char

        return cls(
            position=position,
            material=material,
            state=state,
            behavior=behavior,
            surface=surface,
            audio=audio,
            physics=physics
        )


# ============================================================================
# LAYER QUERIES
# ============================================================================

def has_layer(voxel: VoxelLayers, layer_type: LayerType) -> bool:
    """Check if voxel has a specific layer."""
    layer_map = {
        LayerType.MATERIAL: voxel.material,
        LayerType.STATE: voxel.state,
        LayerType.BEHAVIOR: voxel.behavior,
        LayerType.SURFACE: voxel.surface,
        LayerType.AUDIO: voxel.audio,
        LayerType.PHYSICS: voxel.physics,
    }
    return layer_map.get(layer_type) is not None


def get_layer_name(voxel: VoxelLayers, layer_type: LayerType) -> Optional[str]:
    """Get human-readable name for a layer."""
    emoji_maps = {
        LayerType.MATERIAL: MATERIAL_EMOJI,
        LayerType.STATE: STATE_EMOJI,
        LayerType.BEHAVIOR: BEHAVIOR_EMOJI,
        LayerType.SURFACE: SURFACE_EMOJI,
        LayerType.AUDIO: AUDIO_EMOJI,
        LayerType.PHYSICS: PHYSICS_EMOJI,
    }

    layer_values = {
        LayerType.MATERIAL: voxel.material,
        LayerType.STATE: voxel.state,
        LayerType.BEHAVIOR: voxel.behavior,
        LayerType.SURFACE: voxel.surface,
        LayerType.AUDIO: voxel.audio,
        LayerType.PHYSICS: voxel.physics,
    }

    emoji = layer_values.get(layer_type)
    if not emoji:
        return None

    emoji_map = emoji_maps.get(layer_type, {})
    return emoji_map.get(emoji)


# ============================================================================
# MALL-SPECIFIC VOXEL RECIPES
# ============================================================================

def create_glass_block_voxel(position: Tuple[float, float, float]) -> VoxelLayers:
    """Create a glass block voxel (fountain wall)."""
    return VoxelLayers(
        position=position,
        material='🪟',      # Glass block
        state='✨',         # Pristine
        behavior='🔒',      # Solid
        surface='💎',       # Reflective
        physics='🧊',       # Slippery
    )


def create_escalator_step_voxel(position: Tuple[float, float, float]) -> VoxelLayers:
    """Create an escalator step voxel."""
    return VoxelLayers(
        position=position,
        material='🟨',      # Metal steel
        state='🕐',         # Active
        behavior='⬆️',      # Moving up
        surface='🌓',       # Semi-gloss
        audio='⚙️',        # Mechanical hum
        physics='🏃',       # Fast
    )


def create_fountain_water_voxel(position: Tuple[float, float, float]) -> VoxelLayers:
    """Create a fountain water voxel."""
    return VoxelLayers(
        position=position,
        material='💧',      # Water
        state='💦',         # Dripping
        behavior='🌬️',     # Passable
        surface='🌊',       # Ripples
        audio='🌊',        # Flowing water
        physics='⬇️',       # Sinks
    )


def create_neon_sign_voxel(position: Tuple[float, float, float], color: str = '🔴') -> VoxelLayers:
    """Create a neon sign voxel."""
    return VoxelLayers(
        position=position,
        material='🪟',      # Glass (neon tube)
        state='⚡',         # Powered
        behavior='💡',      # Light source
        surface='🌟',       # Sparkly
        audio='📻',        # Static (transformer hum)
        physics='🪶',       # Light
    )


def create_janitor_mop_voxel(position: Tuple[float, float, float]) -> VoxelLayers:
    """Create janitor mop voxel (from JANITOR_MOP.json)."""
    return VoxelLayers(
        position=position,
        material='🟫',      # Wood (handle)
        state='💧',         # Wet
        behavior='🧹',      # Cleanable/cleaning tool
        surface='🕸️',      # Used/dirty
        physics='🪶',       # Light
    )


# ============================================================================
# RENPY INTEGRATION
# ============================================================================

def voxel_to_renpy_define(voxel: VoxelLayers, voxel_id: str) -> str:
    """Convert voxel with emoji layers to Ren'Py define."""
    compact = voxel.to_compact()
    data = voxel.to_dict()

    lines = []
    lines.append(f"# Voxel: {voxel_id}")
    lines.append(f"# Emoji layers: {compact}")
    lines.append("")

    lines.append(f"define voxel_{voxel_id.lower()} = {{")
    lines.append(f'    "position": {list(voxel.position)},')
    lines.append(f'    "emoji_compact": "{compact}",')
    lines.append(f'    "layers": {{')

    if voxel.material:
        lines.append(f'        "material": {{ "emoji": "{voxel.material}", "name": "{MATERIAL_EMOJI[voxel.material]}" }},')
    if voxel.state:
        lines.append(f'        "state": {{ "emoji": "{voxel.state}", "name": "{STATE_EMOJI[voxel.state]}" }},')
    if voxel.behavior:
        lines.append(f'        "behavior": {{ "emoji": "{voxel.behavior}", "name": "{BEHAVIOR_EMOJI[voxel.behavior]}" }},')
    if voxel.surface:
        lines.append(f'        "surface": {{ "emoji": "{voxel.surface}", "name": "{SURFACE_EMOJI[voxel.surface]}" }},')
    if voxel.audio:
        lines.append(f'        "audio": {{ "emoji": "{voxel.audio}", "name": "{AUDIO_EMOJI[voxel.audio]}" }},')
    if voxel.physics:
        lines.append(f'        "physics": {{ "emoji": "{voxel.physics}", "name": "{PHYSICS_EMOJI[voxel.physics]}" }},')

    lines.append(f'    }}')
    lines.append(f'}}\n')

    return '\n'.join(lines)


# ============================================================================
# GEOJSON WITH LAYERS
# ============================================================================

def voxel_to_geojson_feature(voxel: VoxelLayers, voxel_id: str) -> Dict[str, Any]:
    """Convert voxel with layers to GeoJSON feature."""
    return {
        "type": "Feature",
        "id": voxel_id,
        "geometry": {
            "type": "Point",
            "coordinates": list(voxel.position)
        },
        "properties": {
            "voxel_id": voxel_id,
            "emoji_compact": voxel.to_compact(),
            **voxel.to_dict()
        }
    }


# ============================================================================
# CLI TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("VOXEL EMOJI LAYERS TEST")
    print("=" * 80)

    # Create example voxels
    print("\n[GLASS BLOCK VOXEL]")
    glass = create_glass_block_voxel((10, 20, 0))
    print(f"  Position: {glass.position}")
    print(f"  Compact: {glass.to_compact()}")
    print(f"  Material: {glass.material} ({MATERIAL_EMOJI[glass.material]})")
    print(f"  State: {glass.state} ({STATE_EMOJI[glass.state]})")
    print(f"  Behavior: {glass.behavior} ({BEHAVIOR_EMOJI[glass.behavior]})")
    print(f"  Surface: {glass.surface} ({SURFACE_EMOJI[glass.surface]})")
    print(f"  Physics: {glass.physics} ({PHYSICS_EMOJI[glass.physics]})")

    print("\n[ESCALATOR STEP VOXEL]")
    escalator = create_escalator_step_voxel((0, -100, -4))
    print(f"  Position: {escalator.position}")
    print(f"  Compact: {escalator.to_compact()}")
    print(f"  Layers: {len([l for l in [escalator.material, escalator.state, escalator.behavior, escalator.surface, escalator.audio, escalator.physics] if l])}")

    print("\n[FOUNTAIN WATER VOXEL]")
    water = create_fountain_water_voxel((0, 0, 0))
    print(f"  Compact: {water.to_compact()}")
    print(f"  Material: {water.material} (WATER)")
    print(f"  Audio: {water.audio} (FLOWING_WATER)")

    print("\n[JANITOR MOP VOXEL]")
    mop = create_janitor_mop_voxel((50, 30, 0))
    print(f"  Compact: {mop.to_compact()}")
    print(f"  State: {mop.state} (WET)")
    print(f"  Behavior: {mop.behavior} (CLEANABLE)")

    print("\n[REN'PY DEFINE]")
    renpy_code = voxel_to_renpy_define(glass, "GLASS_BLOCK_001")
    print(renpy_code)

    print("\n[GEOJSON FEATURE]")
    import json
    geojson = voxel_to_geojson_feature(escalator, "ESCALATOR_STEP_042")
    print(json.dumps(geojson, indent=2))

    print("\n[LAYER COMPOSITION EXAMPLES]")
    print(f"  Wet glass: 💎💧 = {VoxelLayers((0,0,0), material='💎', state='💧').to_compact()}")
    print(f"  Glowing door: 🚪💡✨ = {VoxelLayers((0,0,0), material='🚪', behavior='💡', surface='✨').to_compact()}")
    print(f"  Hot metal: 🟨🔥⚡ = {VoxelLayers((0,0,0), material='🟨', state='🔥', physics='⚡').to_compact()}")

    print("\n" + "=" * 80)
    print("EMOJI LAYERS = SEMANTIC COMPRESSION")
    print("  Each emoji adds meaning without text labels")
    print("  Stackable, composable, visual")
    print("  Same principle as wingdings IDs, applied to voxel properties")
    print("=" * 80)
