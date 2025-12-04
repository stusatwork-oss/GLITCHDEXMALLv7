# bridge_server.py
"""
V6 Mall Simulation Bridge Server
Flask HTTP wrapper for sim_bridge.py

Endpoints:
- GET  /health        - Health check
- POST /init          - Initialize world from config
- POST /tick          - Advance simulation one frame
- POST /reset         - Reset world state
- GET  /status        - Get current world stats
"""

from flask import Flask, request, jsonify
import os
import sys
from pathlib import Path
from typing import Optional

# Add src to path so imports work
sys.path.insert(0, str(Path(__file__).parent))

from sim_bridge import init_world, tick_world, WorldState

app = Flask(__name__)

# Global world state
WORLD: Optional[WorldState] = None
CONFIG_PATH: str = os.getenv("MALL_CONFIG_PATH", "config")


# ========== HELPER FUNCTIONS ==========

def get_cloud_dict(cloud) -> dict:
    """
    Extract cloud state as dict.

    IMPORTANT: This is the canonical cloud representation used by both
    /status and /tick to ensure consistency.
    """
    return {
        "level": cloud.cloud_level,
        "mood": cloud.mall_mood.value,
        "trend": cloud.pressure_trend.value,
        "bleed_tier": cloud.current_bleed_tier,
        "bleed_ready": cloud.bleed_threshold_reached
    }


# ========== LIFECYCLE ==========

@app.before_request
def _check_world():
    """Check if world is initialized for endpoints that need it."""
    if request.endpoint in ['tick', 'status', 'reset']:
        if WORLD is None:
            return jsonify({
                "error": "World not initialized. Call /init first."
            }), 503


# ========== ENDPOINTS ==========

@app.get("/health")
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "mall-sim-v6-bridge",
        "world_initialized": WORLD is not None
    })


@app.post("/init")
def init():
    """
    Initialize world from config.

    Request body (optional):
    {
        "config_path": "path/to/config/folder"
    }

    Response:
    {
        "status": "initialized",
        "cloud_level": 0.0,
        "zones_loaded": 11,
        "npcs_loaded": 4
    }
    """
    global WORLD, CONFIG_PATH

    try:
        data = request.get_json(force=True) or {}
        config_path = data.get("config_path", CONFIG_PATH)

        # Validate config path exists
        if not Path(config_path).exists():
            return jsonify({
                "error": f"Config path not found: {config_path}"
            }), 400

        # Initialize world
        print(f"[BRIDGE] Initializing world from {config_path}")
        WORLD = init_world(config_path)
        CONFIG_PATH = config_path

        return jsonify({
            "status": "initialized",
            "config_path": config_path,
            "cloud_level": WORLD.cloud.cloud_level,
            "zones_loaded": len(WORLD.zones),
            "npcs_loaded": len(WORLD.npcs)
        })

    except Exception as e:
        print(f"[BRIDGE] Init error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.post("/tick")
def tick():
    """
    Advance simulation one tick.

    Request body:
    {
        "dt": 0.25,
        "player_event": {
            "type": "move",
            "to_zone": "FC-ARCADE",
            "from_zone": "CORRIDOR"
        }
    }

    Response:
    {
        "timestamp": 1732649283.45,
        "cloud": { ... },
        "zones": { ... },
        "npcs": [ ... ],
        "events": [ ... ]
    }
    """
    global WORLD

    try:
        data = request.get_json(force=True) or {}
        dt = float(data.get("dt", 0.25))
        player_event = data.get("player_event")

        # Validate dt
        if dt <= 0 or dt > 10.0:
            return jsonify({
                "error": "dt must be in range (0, 10.0]"
            }), 400

        # Tick world
        frame = tick_world(WORLD, dt, player_event)

        return jsonify(frame.to_dict())

    except Exception as e:
        print(f"[BRIDGE] Tick error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.post("/reset")
def reset():
    """
    Reset world state.

    Request body (optional):
    {
        "keep_memory": false
    }

    Response:
    {
        "status": "reset",
        "cloud_level": 0.0
    }
    """
    global WORLD

    try:
        data = request.get_json(force=True) or {}
        keep_memory = data.get("keep_memory", False)

        # Reset Cloud
        WORLD.cloud.reset(keep_memory=keep_memory)

        # Reset NPCs
        from npc_state_machine import NPCState
        for npc_machine in WORLD.npcs.values():
            npc_machine.current_state = NPCState.IDLE
            npc_machine.contradiction_active = False

        return jsonify({
            "status": "reset",
            "keep_memory": keep_memory,
            "cloud_level": WORLD.cloud.cloud_level
        })

    except Exception as e:
        print(f"[BRIDGE] Reset error: {e}")
        return jsonify({"error": str(e)}), 500


@app.get("/status")
def status():
    """
    Get current world status.

    Response:
    {
        "cloud": {
            "level": 42.5,
            "mood": "uneasy",
            "trend": "rising",
            "bleed_tier": 1,
            "bleed_ready": false
        },
        "zones_count": 11,
        "npcs_count": 4,
        "session": {
            "count": 3,
            "total_playtime": 1847.2
        },
        "stats": {
            "discoveries": 12,
            "contradictions": 2,
            "entities_loaded": 15
        }
    }
    """
    global WORLD

    try:
        # Use canonical cloud representation (same as /tick)
        cloud_dict = get_cloud_dict(WORLD.cloud)

        return jsonify({
            "cloud": cloud_dict,
            "zones_count": len(WORLD.zones),
            "npcs_count": len(WORLD.npcs),
            "session": {
                "count": WORLD.cloud.session_count,
                "total_playtime": WORLD.cloud.total_playtime
            },
            "stats": {
                "discoveries": len(WORLD.cloud.discovery_history),
                "contradictions": len(WORLD.cloud.npc_contradiction_log),
                "entities_loaded": len(WORLD.cloud.entities)
            }
        })

    except Exception as e:
        print(f"[BRIDGE] Status error: {e}")
        return jsonify({"error": str(e)}), 500


# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "GET  /health",
            "POST /init",
            "POST /tick",
            "POST /reset",
            "GET  /status"
        ]
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "error": "Internal server error",
        "detail": str(e)
    }), 500


# ========== MAIN ==========

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Mall Sim V6 Bridge Server")
    parser.add_argument(
        "--config",
        default="config",
        help="Path to config folder (default: config)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5005,
        help="Port to run server on (default: 5005)"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--auto-init",
        action="store_true",
        help="Auto-initialize world on startup"
    )

    args = parser.parse_args()

    CONFIG_PATH = args.config

    # Auto-init if requested
    if args.auto_init:
        try:
            print(f"[BRIDGE] Auto-initializing world from {CONFIG_PATH}")
            WORLD = init_world(CONFIG_PATH)
            print(f"[BRIDGE] ✓ World initialized")
            print(f"  Zones: {len(WORLD.zones)}")
            print(f"  NPCs: {len(WORLD.npcs)}")
            print(f"  Cloud: {WORLD.cloud.cloud_level:.1f}")
        except Exception as e:
            print(f"[BRIDGE] ✗ Auto-init failed: {e}")
            import traceback
            traceback.print_exc()
            print(f"[BRIDGE] Server will start anyway. Use /init endpoint to initialize.")

    print(f"\n{'='*60}")
    print(f"MALL SIMULATION BRIDGE SERVER - V6")
    print(f"{'='*60}")
    print(f"Config path: {CONFIG_PATH}")
    print(f"Listening on: http://{args.host}:{args.port}")
    print(f"World initialized: {WORLD is not None}")
    print(f"\nEndpoints:")
    print(f"  GET  /health  - Health check")
    print(f"  POST /init    - Initialize world")
    print(f"  POST /tick    - Advance simulation")
    print(f"  POST /reset   - Reset world state")
    print(f"  GET  /status  - Get world status")
    print(f"{'='*60}\n")

    app.run(
        host=args.host,
        port=args.port,
        debug=True,
        use_reloader=False  # Prevent double initialization in debug mode
    )
