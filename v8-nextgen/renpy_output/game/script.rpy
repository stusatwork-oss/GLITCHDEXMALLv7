# GLITCHDEXMALLv7 - v8 NextGen Ren'Py Conversion
# Deep Space Probe Telemetry Format Applied to Mall Simulation

# Import measurements (source of truth)
$ import_measurements = True

# Import symbol registry
$ import_symbols = True

# Initialize game state
init python:
    # Cloud pressure system
    cloud_pressure = 0

    # Probe telemetry registry
    probe_entities = {}

    # Load GeoJSON spatial data
    import json
    from pathlib import Path
    geojson_path = Path(config.gamedir) / "geojson" / "mall_zones.geojson"
    if geojson_path.exists():
        with open(geojson_path) as f:
            spatial_data = json.load(f)

# Start label
label start:
    scene black

    "GLITCHDEXMALL v8"
    "Deep Space Probe Telemetry Format"
    "Same shape, different application."

    menu:
        "Where would you like to go?"

        "Central Atrium (🎪)":
            jump zone_central_atrium

        "Food Court (🍽️)":
            jump zone_food_court

        "Escalator Wells (⬆️)":
            jump zone_escalator_wells

    return

# Zone labels
label zone_central_atrium:
    scene atrium
    "You stand in the central atrium."
    "Diameter: [ATRIUM_DIAMETER_FEET] feet"
    "Height: [ATRIUM_HEIGHT_FEET] feet"
    jump start

label zone_food_court:
    scene food_court
    "You descend to the food court."
    "Drop: [ESCALATOR_DROP_FEET] feet (12 steps × 8 inches)"
    jump start

label zone_escalator_wells:
    scene escalator
    "The escalators hum quietly."
    "Vertical travel: [ESCALATOR_DROP_FEET] feet"
    "Source of truth: Verified measurement"
    jump start
