"""
Toddler Configuration - Behavioral Parameters

Defines movement, visibility, distortion, and behavior trigger parameters.
"""

TODDLER_CONFIG = {
    "movement": {
        "base_speed": 3.0,              # feet per second (walking pace)
        "curious_speed": 5.0,           # when following player
        "fleeing_speed": 8.0,           # when running away
        "teleport_distance": 200.0,     # instant relocation if too far from player
        "wander_radius": 50.0,          # how far to wander when WANDERING
    },

    "visibility": {
        "base_rate": 0.01,              # visibility gain per second (ambient)
        "cloud_amplifier": 0.02,        # extra gain per Cloud point (Cloud 70 = +1.4/s)
        "decay_rate": 0.05,             # visibility loss when not triggered
        "max_visibility": 1.0,
        "instant_fade_threshold": 0.3,  # fade to 0 if direct look + below threshold
    },

    "distortion": {
        "base_radius": 15.0,            # feet (minimum effect radius)
        "max_radius": 40.0,             # at full visibility
        "reality_strain_threshold": 0.5,  # when effects become noticeable
        "intensity_falloff": 0.7,       # exponential falloff with distance
    },

    "behavior_triggers": {
        "curious_distance": 50.0,       # switch to CURIOUS if player within
        "manifesting_cloud": 70.0,      # switch to MANIFESTING at Cloud 70+
        "fleeing_direct_look": True,    # flee if player looks directly
        "static_on_contradiction": True,  # become STATIC when NPC contradicts
        "static_duration": 30.0,        # seconds to remain STATIC
    },

    "heat_generation": {
        "base_multiplier": 1.0,         # no toddler effect
        "distance_curve": "inverse_square",  # how heat scales with distance
        "max_multiplier": 3.0,          # when right next to player + visible
        "visibility_weight": 0.6,       # how much visibility affects heat vs distance
    },

    "glitch_generation": {
        "base_multiplier": 1.0,
        "max_multiplier": 4.0,          # severe glitches when manifested + close
        "reality_strain_factor": 2.0,   # reality_strain directly scales glitches
    },

    "spawn": {
        "initial_position": (0, 0, 0),  # Override in initialization
        "initial_behavior": "WANDERING",
        "initial_visibility": 0.0,
        "safe_spawn_distance": 100.0,   # spawn at least this far from player
    }
}


# Behavioral mode parameters
BEHAVIOR_PARAMS = {
    "WANDERING": {
        "visibility_rate": 0.005,       # slow visibility gain
        "movement_pattern": "random_walk",
        "distance_preference": "any",
    },

    "CURIOUS": {
        "visibility_rate": 0.02,        # moderate visibility gain
        "movement_pattern": "follow_at_distance",
        "distance_preference": "20-40ft",  # Sweet spot for following
    },

    "MANIFESTING": {
        "visibility_rate": 0.05,        # rapid visibility gain
        "movement_pattern": "approach",
        "distance_preference": "5-15ft",  # Gets close
    },

    "FLEEING": {
        "visibility_rate": -0.1,        # rapid visibility loss
        "movement_pattern": "flee",
        "distance_preference": "100+ft",
    },

    "STATIC": {
        "visibility_rate": 0.0,         # frozen visibility
        "movement_pattern": "none",
        "distance_preference": "fixed",  # Doesn't move
        "creates_haunted_zone": True,
    }
}


# Zone-specific toddler preferences (where it likes to manifest)
ZONE_PREFERENCES = {
    "Z4_FOOD_COURT": 2.0,       # Sunken bowl = favorite
    "SERVICE_HALL": 1.8,        # Liminal spaces
    "ESCALATORS": 1.5,          # Vertical transitions
    "FC-ARCADE": 1.3,           # High QBIT zones
    "Z1_CENTRAL_ATRIUM": 0.5,   # Too open, dislikes
    "ENTRANCE": 0.3,            # Too public, avoids
}
