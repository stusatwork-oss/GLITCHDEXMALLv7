# V6 Mall Simulation Bridge API

**Version:** 6.0
**Base URL:** `http://localhost:5005`
**Protocol:** HTTP/JSON
**Status:** LOCKED (contracts are stable)

---

## 📋 Locked JSON Contracts

These contracts are **stable** and will not change without major version bump.

---

## Endpoints

### `GET /health`

Health check endpoint. Always responds if server is running.

**Request:** None

**Response:**
```json
{
  "status": "ok",
  "service": "mall-sim-v6-bridge",
  "world_initialized": true
}
```

**Status Codes:**
- `200` - Server is healthy

---

### `POST /init`

Initialize world from config directory.

**Request:**
```json
{
  "config_path": "config"
}
```

**Fields:**
- `config_path` (string, optional) - Path to config folder. Default: `"config"`

**Response:**
```json
{
  "status": "initialized",
  "config_path": "config",
  "cloud_level": 0.0,
  "zones_loaded": 11,
  "npcs_loaded": 4
}
```

**Status Codes:**
- `200` - World initialized successfully
- `400` - Config path not found
- `500` - Initialization failed

---

### `GET /status`

Get current world state snapshot.

**Request:** None

**Response:**
```json
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
```

**Fields:**
- `cloud.level` (float) - Cloud pressure (0-100)
- `cloud.mood` (string) - One of: `"calm"`, `"uneasy"`, `"strained"`, `"critical"`
- `cloud.trend` (string) - One of: `"stable"`, `"rising"`, `"falling"`, `"spiking"`
- `cloud.bleed_tier` (int) - Current bleed tier (0-3)
- `cloud.bleed_ready` (bool) - Has Cloud reached bleed threshold
- `zones_count` (int) - Number of zones loaded
- `npcs_count` (int) - Number of NPCs loaded
- `session.count` (int) - Total sessions across all playthroughs
- `session.total_playtime` (float) - Total playtime in seconds
- `stats.discoveries` (int) - Number of discoveries logged
- `stats.contradictions` (int) - Number of NPC contradictions logged
- `stats.entities_loaded` (int) - Number of QBIT entities loaded

**Status Codes:**
- `200` - Status retrieved successfully
- `503` - World not initialized

---

### `POST /tick`

Advance simulation by one timestep.

**⚠️ CRITICAL:** This is the main integration point for UE5.

**Request:**
```json
{
  "dt": 0.25,
  "player_event": {
    "type": "move",
    "to_zone": "FC-ARCADE",
    "from_zone": "CORRIDOR"
  }
}
```

**Fields:**
- `dt` (float, required) - Delta time in seconds. Range: `(0, 10.0]`. Recommended: `0.25` (4Hz tick rate)
- `player_event` (object, optional) - Player action this frame. Can be `null` for idle/wait.

**Player Event Types:**

#### Type: `"move"`
```json
{
  "type": "move",
  "to_zone": "FC-ARCADE",
  "from_zone": "CORRIDOR"
}
```
- `to_zone` (string, required) - Destination zone ID
- `from_zone` (string, optional) - Origin zone ID

#### Type: `"interact"`
```json
{
  "type": "interact",
  "target": "bag_of_screams",
  "zone": "FC-ARCADE"
}
```
- `target` (string, required) - Entity/object ID being interacted with
- `zone` (string, required) - Zone where interaction occurred

#### Type: `"discover"`
```json
{
  "type": "discover",
  "document": "log_017",
  "zone": "SERVICE_HALL"
}
```
- `document` (string, required) - Document/log ID discovered
- `zone` (string, required) - Zone where discovery occurred

#### Type: `"wait"`
```json
{
  "type": "wait"
}
```
- No additional fields. Indicates player is idle.

#### Type: `"run"`
```json
{
  "type": "run",
  "zone": "FC-ARCADE"
}
```
- `zone` (string, required) - Zone where running occurred

---

**Response (FrameUpdate):**

```json
{
  "timestamp": 1732649283.45,
  "cloud": {
    "level": 42.8,
    "mood": "uneasy",
    "trend": "rising",
    "pressure_rate": 0.1
  },
  "zones": {
    "FC-ARCADE": {
      "zone_id": "FC-ARCADE",
      "turbulence": 5.2,
      "resonance": 12.5,
      "qbit_aggregate": 1154.0,
      "qbit_power": 850.0,
      "qbit_charisma": 304.0,
      "qbit_entity_count": 3,
      "swarm_bias": {
        "color_weight": 0.65,
        "clustering": 0.52,
        "speed": 1.26,
        "avoidance": []
      },
      "adjacency": {
        "CORRIDOR": 0.35,
        "SERVICE_HALL": 0.40,
        "MAIN_HALL": 0.25
      }
    },
    "CORRIDOR": {
      "zone_id": "CORRIDOR",
      "turbulence": 2.1,
      "resonance": 3.0,
      "qbit_aggregate": 100.0,
      "qbit_power": 50.0,
      "qbit_charisma": 50.0,
      "qbit_entity_count": 1,
      "swarm_bias": {
        "color_weight": 0.26,
        "clustering": 0.21,
        "speed": 1.11,
        "avoidance": []
      },
      "adjacency": {
        "FC-ARCADE": 0.45,
        "SERVICE_HALL": 0.30,
        "MAIN_HALL": 0.25
      }
    }
  },
  "npcs": [
    {
      "id": "janitor-001",
      "zone": "CORRIDOR",
      "state": "patrol",
      "behavior_hint": "patrol_route"
    },
    {
      "id": "uncle-danny",
      "zone": "FC-ARCADE",
      "state": "idle",
      "behavior_hint": "cooking_idle"
    },
    {
      "id": "security-wolf",
      "zone": "MAIN_HALL",
      "state": "alert",
      "behavior_hint": "scan_area"
    }
  ],
  "events": [
    {
      "type": "cloud_mood_changed",
      "timestamp": 1732649283.45,
      "details": {
        "from": "calm",
        "to": "uneasy",
        "level": 42.8
      }
    }
  ]
}
```

**Response Fields:**

**`timestamp`** (float)
- Unix timestamp of this frame

**`cloud`** (object)
- `level` (float) - Cloud pressure (0-100)
- `mood` (string) - One of: `"calm"`, `"uneasy"`, `"strained"`, `"critical"`
- `trend` (string) - One of: `"stable"`, `"rising"`, `"falling"`, `"spiking"`
- `pressure_rate` (float) - Rate of change (delta per second)

**`zones`** (object)
- Keys are zone IDs (e.g., `"FC-ARCADE"`)
- Values are zone state objects:
  - `zone_id` (string) - Zone identifier
  - `turbulence` (float) - Local instability (0-10)
  - `resonance` (float) - Memory accumulation (0-100+)
  - `qbit_aggregate` (float) - Total entity influence in zone (0-6000+)
  - `qbit_power` (float) - Structural leverage weight (0-3000+)
  - `qbit_charisma` (float) - Attention/resonance weight (0-3000+)
  - `qbit_entity_count` (int) - Number of entities in zone
  - `swarm_bias` (object) - NPC crowd behavior modifiers
    - `color_weight` (float) - Beige uniformity (0-1)
    - `clustering` (float) - Grouping tendency (0-1)
    - `speed` (float) - Movement speed multiplier (0.5-2.0)
    - `avoidance` (array[string]) - Zones to avoid
  - `adjacency` (object) - QBIT-weighted zone connections
    - Keys: adjacent zone IDs
    - Values: probability weights (0-1, sum to 1.0)

**`npcs`** (array[object])
- `id` (string) - NPC identifier
- `zone` (string) - Current zone ID
- `state` (string) - One of: `"idle"`, `"patrol"`, `"alert"`, `"suspicious"`, `"hostile"`, `"contradiction"`
- `behavior_hint` (string) - Suggested animation/behavior for renderer
  - Examples: `"patrol_route"`, `"cooking_idle"`, `"scan_area"`, `"pace_near_player"`, `"freeze_loop"`

**`events`** (array[object])
- Discrete events that occurred this tick
- Each event has:
  - `type` (string) - Event type
  - `timestamp` (float) - When it occurred
  - `details` (object) - Event-specific data

**Event Types:**
- `"cloud_mood_changed"` - Cloud mood transition
- `"contradiction_triggered"` - NPC broke spine rule
- `"zone_entered"` - Player entered new zone
- `"discovery_made"` - Player discovered document/artifact

**Status Codes:**
- `200` - Tick successful
- `400` - Invalid dt value
- `503` - World not initialized
- `500` - Simulation error

---

### `POST /reset`

Reset world state to initial conditions.

**Request:**
```json
{
  "keep_memory": false
}
```

**Fields:**
- `keep_memory` (bool, optional) - If true, preserve discovery/contradiction history. Default: `false`

**Response:**
```json
{
  "status": "reset",
  "keep_memory": false,
  "cloud_level": 0.0
}
```

**Status Codes:**
- `200` - Reset successful
- `503` - World not initialized
- `500` - Reset failed

---

## Data Type Reference

### Cloud Mood Values
- `"calm"` - Cloud level 0-24
- `"uneasy"` - Cloud level 25-49
- `"strained"` - Cloud level 50-74
- `"critical"` - Cloud level 75-100

### Cloud Trend Values
- `"stable"` - Minimal change
- `"rising"` - Increasing pressure
- `"falling"` - Decreasing pressure
- `"spiking"` - Rapid increase (event-driven)

### NPC State Values
- `"idle"` - Default state, minimal activity
- `"patrol"` - Following route
- `"alert"` - Aware of anomaly, not hostile
- `"suspicious"` - Investigating unusual behavior
- `"hostile"` - Actively responding to threat
- `"contradiction"` - Breaking spine rules (bleed event)

### Bleed Tier Values
- `0` - No bleed effects
- `1` - Visual/audio effects only (Cloud 75+)
- `2` - Visual + NPC contradictions (Cloud 80+)
- `3` - Visual + NPC + space distortion (Cloud 90+)

---

## Integration Examples

### UE5 C++ (Minimal)

```cpp
// BeginPlay - check server is up
FHttpModule::Get().CreateRequest()
    ->SetURL("http://127.0.0.1:5005/health")
    ->SetVerb("GET")
    ->OnProcessRequestComplete().BindLambda([](FHttpRequestPtr Req, FHttpResponsePtr Res, bool bSuccess) {
        if (bSuccess) {
            UE_LOG(LogTemp, Log, TEXT("Bridge server is online"));
        }
    })
    ->ProcessRequest();

// Tick - advance simulation
TSharedPtr<FJsonObject> RequestJson = MakeShareable(new FJsonObject);
RequestJson->SetNumberField("dt", DeltaTime);

TSharedPtr<FJsonObject> PlayerEvent = MakeShareable(new FJsonObject);
PlayerEvent->SetStringField("type", "move");
PlayerEvent->SetStringField("to_zone", "FC-ARCADE");
RequestJson->SetObjectField("player_event", PlayerEvent);

FString RequestBody;
TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&RequestBody);
FJsonSerializer::Serialize(RequestJson.ToSharedRef(), Writer);

FHttpModule::Get().CreateRequest()
    ->SetURL("http://127.0.0.1:5005/tick")
    ->SetVerb("POST")
    ->SetHeader("Content-Type", "application/json")
    ->SetContentAsString(RequestBody)
    ->OnProcessRequestComplete().BindUObject(this, &UMySubsystem::OnTickResponse)
    ->ProcessRequest();
```

### Python CLI (Minimal)

```python
import requests

# Health check
r = requests.get("http://localhost:5005/health")
print(r.json())  # {"status": "ok", ...}

# Tick
r = requests.post("http://localhost:5005/tick", json={
    "dt": 0.25,
    "player_event": {
        "type": "move",
        "to_zone": "FC-ARCADE"
    }
})
frame = r.json()
print(f"Cloud: {frame['cloud']['level']:.1f} ({frame['cloud']['mood']})")
print(f"NPCs: {len(frame['npcs'])}")
```

---

## Consistency Guarantees

### `/status` and `/tick` Agreement

The `cloud` object returned by `/status` and `/tick` use **identical structure**:

```json
{
  "level": 42.5,
  "mood": "uneasy",
  "trend": "rising",
  "bleed_tier": 1,
  "bleed_ready": false
}
```

**Invariants:**
- If `/status` shows `cloud.level = 42.5`, the next `/tick` will show a cloud level ≈ 42.5 (± drift)
- `cloud.mood` is deterministic based on `cloud.level`:
  - `0-24` → `"calm"`
  - `25-49` → `"uneasy"`
  - `50-74` → `"strained"`
  - `75-100` → `"critical"`
- `zones_count` and `npcs_count` from `/status` match the number of entries in `/tick` response arrays

### Tick Rate Recommendations

**Recommended:** 4Hz (dt=0.25s)
- Good balance of responsiveness and performance
- Cloud updates feel smooth
- NPC state changes are noticeable
- Low network overhead

**Acceptable Range:** 1-10Hz (dt=0.1-1.0s)
- Below 1Hz (dt > 1.0s): NPCs may appear jerky
- Above 10Hz (dt < 0.1s): Diminishing returns, network overhead

**Fixed Tick vs Variable dt:**
- UE5 should accumulate DeltaTime and call `/tick` at fixed intervals
- Example: Accumulate until ≥ 0.25s, then call with actual accumulated time

---

## Error Handling

All error responses follow this format:

```json
{
  "error": "Human-readable error message",
  "traceback": "Python traceback (only in debug mode)"
}
```

**Common Errors:**

**503 Service Unavailable**
```json
{
  "error": "World not initialized. Call /init first."
}
```
Solution: Call `POST /init` before calling `/tick`, `/status`, or `/reset`

**400 Bad Request**
```json
{
  "error": "dt must be in range (0, 10.0]"
}
```
Solution: Ensure `dt` is a positive float ≤ 10.0

**500 Internal Server Error**
```json
{
  "error": "Simulation error: <details>",
  "traceback": "<stack trace>"
}
```
Solution: Check server logs, verify config files are valid

---

## Version History

**6.0 (2025-11-26)**
- Initial locked contract
- QBIT integration in zone data
- NPC contradiction system
- Cloud bleed tiers

---

**End of API Documentation**
