#!/usr/bin/env python3
"""
MARBLE PROMPT GENERATOR
Converts spatial measurement data into Marble-compatible scene descriptions.

Uses escalator-calibrated measurements from v8-nextgen/data/measurements/
to generate dimensionally-accurate prompts for World Labs Marble.

Usage:
    python generate_marble_prompts.py --output marble_prompts.txt
    python generate_marble_prompts.py --zone Z4_FOOD_COURT --output food_court_marble.txt
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional


def load_measurements(base_path: Path = Path("v8-nextgen/data/measurements")):
    """Load all measurement JSONs."""
    spatial = json.loads((base_path / "spatial_measurements.json").read_text())
    zones = json.loads((base_path / "zone_measurements.json").read_text())
    return spatial, zones


def generate_zone_prompt(zone_id: str, zone_data: Dict, spatial_data: Dict) -> str:
    """
    Generate a rich Marble prompt for a single zone.

    Marble accepts text descriptions and generates Gaussian splat representations.
    Our prompts include:
    - Dimensional constraints (from escalator measurements)
    - Architectural features
    - Lighting and atmosphere
    - Material descriptions
    """

    prompts = []

    # Zone header
    name = zone_data.get("name", zone_id)
    prompts.append(f"# {zone_id}: {name}")
    prompts.append("")

    # Core spatial prompt
    prompt_parts = []

    # Add zone type and scale
    if "diameter_feet" in zone_data:
        diameter = zone_data["diameter_feet"]["value"]
        prompt_parts.append(f"A {name.lower()} space, {diameter} feet in diameter")
    elif "corridor_width_feet" in zone_data:
        width = zone_data["corridor_width_feet"]["value"]
        prompt_parts.append(f"A {name.lower()} corridor, {width} feet wide")
    else:
        prompt_parts.append(f"A {name.lower()} space")

    # Add ceiling height if available
    if "ceiling_height_feet" in zone_data:
        height = zone_data["ceiling_height_feet"]["value"]
        prompt_parts.append(f"with {height}-foot-tall ceilings")
    elif "vertical_clearance_feet" in zone_data:
        clearance = zone_data["vertical_clearance_feet"]["value"]
        prompt_parts.append(f"with {clearance} feet of vertical clearance")

    # Add elevation info
    if "elevation_feet" in zone_data:
        elevation = zone_data["elevation_feet"]
        if elevation < 0:
            prompt_parts.append(f"sunken {abs(elevation)} feet below ground level")
        elif elevation > 0:
            prompt_parts.append(f"elevated {elevation} feet above ground level")

    # Zone-specific features
    if "contains" in zone_data:
        contains = zone_data["contains"][:3]  # Top 3 features
        features_str = ", ".join(contains)
        prompt_parts.append(f"featuring {features_str}")

    # Assemble main prompt
    main_prompt = ", ".join(prompt_parts) + "."
    prompts.append(f"**Main Prompt:**")
    prompts.append(main_prompt)
    prompts.append("")

    # Enhanced description with atmosphere
    prompts.append(f"**Enhanced Description:**")
    enhanced = generate_enhanced_description(zone_id, zone_data, spatial_data)
    prompts.append(enhanced)
    prompts.append("")

    # Technical specs for reference
    prompts.append(f"**Technical Specs:**")
    if "area_sqft" in zone_data:
        prompts.append(f"- Area: ~{zone_data['area_sqft']['value']:,} sq ft")
    if "ceiling_height_feet" in zone_data:
        prompts.append(f"- Ceiling Height: {zone_data['ceiling_height_feet']['value']} ft")
    if "diameter_feet" in zone_data:
        prompts.append(f"- Diameter: {zone_data['diameter_feet']['value']} ft")
    if "level" in zone_data:
        prompts.append(f"- Level: {zone_data['level']} (elevation: {zone_data.get('elevation_feet', 0)} ft)")

    prompts.append("")
    prompts.append("---")
    prompts.append("")

    return "\n".join(prompts)


def generate_enhanced_description(zone_id: str, zone_data: Dict, spatial_data: Dict) -> str:
    """
    Generate atmosphere-rich descriptions for Marble.
    These help the AI understand the mood and visual style.
    """

    descriptions = {
        "Z1_CENTRAL_ATRIUM": (
            "A cathedral-scale central atrium with a dramatic tensile fabric roof "
            "suspended from four yellow lattice steel tension masts 70 feet tall. "
            "The space features a four-tiered terraced amphitheater fountain with "
            "a curved glass block wall backdrop. Radial cables span 175 feet from "
            "center to perimeter in a 32-segment geometric pattern. The architecture "
            "combines proto-Silicon Valley tech aesthetics with 1980s mall grandeur. "
            "Natural light filters through white tensile fabric creating a soft, "
            "diffused glow. The space has an airport terminal or train station scale - "
            "monumentally oversized for a retail environment."
        ),
        "Z4_FOOD_COURT": (
            "A sunken amphitheater bowl 120 feet in diameter, descended to via "
            "chrome escalators with 12 measured steps (8 feet total drop). The space "
            "has a 'reactor containment zone' aesthetic with industrial theater vibes. "
            "Asymmetric vendor bays line the perimeter with striped metal and glass "
            "construction. A large circular neon sign reading 'FOOD COURT' (6-8 feet "
            "in diameter) hovers at the center. Beige carpet with abstract patterns "
            "covers the floor. At the gravitational center sits the theater entrance - "
            "a black void visible from the escalator descent. The pit has 50 feet of "
            "vertical clearance to the tensile roof above, creating a cathedral-like volume. "
            "Staggered tile geometry and glass block retaining walls add geometric complexity. "
            "The lighting is warm but dim, with vendor signs providing colorful accents. "
            "1980s mall decline aesthetic - some vendors dark, 'Coming Soon' signs flickering."
        ),
        "Z3_LOWER_RING": (
            "Wide circulation corridors 25 feet across - train station scale, not typical "
            "12-foot mall corridors. Yellow/beige painted walls with 12-foot ceilings. "
            "Beige carpet with abstract patterns throughout. Kiosk sites with metal and "
            "glass structures dot the corridor. Transitions from tile to carpet mark zone "
            "boundaries. The Coca-Cola Enterprises store provides a colorful anchor with "
            "red display cases and cursive signage. Service hall access points branch off. "
            "Exposed black ceiling grids visible in some areas. The scale feels monumental - "
            "more civic architecture than retail. Fluorescent lighting creates even, slightly "
            "harsh illumination. Empty storefronts with security grates add to the liminal "
            "space quality."
        ),
        "Z5_ESCALATOR_WELLS": (
            "A dedicated vertical circulation zone with bidirectional chrome escalators. "
            "Two parallel escalators (up and down) connect ground level (Level 0) to the "
            "sunken food court (Level -1). Each escalator has exactly 12 steps with 8-inch "
            "rise, totaling 8 feet of elevation change. The escalator bay is approximately "
            "25 feet wide and 25 feet long. Chrome and stainless steel finishes catch light. "
            "Views open up as you descend - the yellow lattice tower visible above, the "
            "food court bowl spreading out below. Glass and metal railings provide safety. "
            "The perspective shift during descent is dramatic - transitioning from the grand "
            "atrium to the intimate theater bowl. The escalators themselves are sculptural "
            "elements - their angles and chrome surfaces defining the space."
        ),
        "Z6_THEATER": (
            "A 6-screen underground cinema positioned at the gravitational center of the "
            "food court bowl. The entrance appears as a 'black open mouth' - a dark void "
            "that draws the eye from the escalator descent. The composition creates a "
            "three-stage spatial sequence: upper level → escalator descent → theater void. "
            "The box office protrudes into the corridor with velvet rope queue areas. "
            "A flickering marquee displays movie titles from 2006-2007. The theater lobby "
            "has standard 1980s multiplex finishes - patterned carpet, wood-grain paneling, "
            "backlit movie posters. Most screens (2-6) are dark and unused during the mall's "
            "decline period. Screen 1 shows occasional signs of operation. The spatial position "
            "is critical - it's the focal point that the entire food court bowl architecture "
            "directs attention toward."
        ),
        "Z6_MICKEYS_WING": (
            "A distinctive southeast wing featuring a dramatic concentric arch entrance. "
            "Multiple layered arches create a depth effect with concentric red and orange "
            "rings. The approach is a shallow corridor with tile color transitions - moving "
            "from mall standard beige to the restaurant's distinct palette. Glass doors at "
            "the vestibule provide separation. The arch feature is monumental - clearly "
            "visible and photogenic. Beyond lies the dining area interior and exterior "
            "parking access. The architecture makes a bold statement - breaking from the "
            "mall's restrained modernism with expressive, almost postmodern geometry. "
            "The concentric arches create a forced-perspective tunnel effect."
        )
    }

    return descriptions.get(zone_id, zone_data.get("note", "No enhanced description available."))


def generate_camera_prompts(spatial_ref_path: Path = Path("v8-nextgen/assets/photos/eastland-archive/SPATIAL_REFERENCE_NERF.md")) -> List[str]:
    """
    Generate camera position prompts for multi-view capture.

    Marble can use these to understand spatial relationships across views.
    """
    prompts = []
    prompts.append("# CAMERA POSITION PROMPTS FOR MULTI-VIEW CAPTURE")
    prompts.append("")
    prompts.append("Use these as guidance for generating consistent multi-view scenes:")
    prompts.append("")

    # Ground floor key positions
    prompts.append("## Ground Floor (Level 0) Views:")
    prompts.append("")
    prompts.append("1. **Central Fountain View (facing East)**")
    prompts.append("   - Position: Center of atrium near fountain")
    prompts.append("   - Height: 5.5 feet (human eye level)")
    prompts.append("   - View: Yellow tower center, escalators visible, upper level balconies")
    prompts.append("   - Wide FOV to capture cathedral scale")
    prompts.append("")

    prompts.append("2. **Escalator Overlook (looking down to food court)**")
    prompts.append("   - Position: Edge of sunken area at ground level")
    prompts.append("   - Height: 5.5 feet")
    prompts.append("   - View: Down and south toward food court bowl")
    prompts.append("   - Chrome escalators, food court seating below visible")
    prompts.append("")

    prompts.append("3. **Main Corridor Perspective (facing East)**")
    prompts.append("   - Position: Mid-corridor in lower ring")
    prompts.append("   - Height: 5.5 feet")
    prompts.append("   - View: Long perspective down 25-foot-wide corridor")
    prompts.append("   - Yellow/beige walls, storefronts, EXIT signs at vanishing point")
    prompts.append("")

    # Food court views
    prompts.append("## Food Court (Level -1) Views:")
    prompts.append("")
    prompts.append("4. **Food Court Floor (looking up at escalators)**")
    prompts.append("   - Position: Food court floor near escalator base")
    prompts.append("   - Height: 5.0 feet")
    prompts.append("   - View: Up toward chrome escalators and ground level")
    prompts.append("   - Yellow tower and upper shops visible above")
    prompts.append("")

    prompts.append("5. **Vendor Row Perspective**")
    prompts.append("   - Position: Food court seating area")
    prompts.append("   - Height: 5.0 feet")
    prompts.append("   - View: Across bowl toward vendor stalls")
    prompts.append("   - White architectural canopy, maroon counters, neon signs")
    prompts.append("")

    return prompts


def main():
    parser = argparse.ArgumentParser(
        description="Generate Marble-compatible prompts from spatial measurements"
    )
    parser.add_argument(
        "--zone",
        help="Generate prompt for specific zone only (e.g., Z4_FOOD_COURT)",
        default=None
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path",
        default="marble_prompts.txt"
    )
    parser.add_argument(
        "--include-cameras",
        action="store_true",
        help="Include camera position guidance"
    )

    args = parser.parse_args()

    # Load measurement data
    print(f"Loading measurements...")
    spatial, zones = load_measurements()

    # Generate prompts
    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append("EASTLAND MALL - MARBLE PROMPT GENERATION")
    output_lines.append("=" * 80)
    output_lines.append("")
    output_lines.append("Generated from escalator-calibrated spatial measurements.")
    output_lines.append("Source: v8-nextgen/data/measurements/")
    output_lines.append("")
    output_lines.append("=" * 80)
    output_lines.append("")

    # Filter zones if specified
    if args.zone:
        if args.zone in zones:
            print(f"Generating prompt for {args.zone}...")
            output_lines.append(generate_zone_prompt(args.zone, zones[args.zone], spatial))
        else:
            print(f"Error: Zone {args.zone} not found.")
            print(f"Available zones: {', '.join(zones.keys())}")
            return
    else:
        # Generate all zones
        zone_ids = [
            "Z1_CENTRAL_ATRIUM",
            "Z4_FOOD_COURT",
            "Z3_LOWER_RING",
            "Z5_ESCALATOR_WELLS",
            "Z6_THEATER",
            "Z6_MICKEYS_WING"
        ]

        for zone_id in zone_ids:
            if zone_id in zones:
                print(f"Generating prompt for {zone_id}...")
                output_lines.append(generate_zone_prompt(zone_id, zones[zone_id], spatial))

    # Add camera guidance if requested
    if args.include_cameras:
        output_lines.append("")
        output_lines.extend(generate_camera_prompts())

    # Write output
    output_path = Path(args.output)
    output_path.write_text("\n".join(output_lines))

    print(f"\n✅ Generated {len(output_lines)} lines")
    print(f"✅ Saved to: {output_path}")
    print(f"\n🎨 Ready to use with Marble at https://marble.worldlabs.ai/create")
    print(f"\nTip: Copy prompts and paste into Marble's text input.")
    print(f"     Marble will generate Gaussian splat representations from the descriptions.")


if __name__ == "__main__":
    main()
