# UE5 Integration - One Pager

**V6 Mall Simulation Bridge**
**Target Engine:** Unreal Engine 5.1+
**Integration Pattern:** Python-as-Service via HTTP/JSON

---

## 🎯 Minimal Implementation (3 Things)

### What You Get from `/tick`

```json
{
  "cloud": {
    "level": 42.8,
    "mood": "uneasy",
    "trend": "rising"
  },
  "npcs": [
    {"id": "janitor-001", "zone": "CORRIDOR", "state": "patrol", "behavior_hint": "patrol_route"},
    {"id": "uncle-danny", "zone": "FC-ARCADE", "state": "idle", "behavior_hint": "cooking_idle"}
  ],
  "zones": { ... },
  "events": [
    {"type": "cloud_mood_changed", "details": {"from": "calm", "to": "uneasy"}}
  ]
}
```

### What To Do With It

#### 1. **`frame["cloud"]["mood"]`** → Tint Walls
```cpp
void UMallSimSubsystem::ApplyCloudMood(FString Mood)
{
    // Get post-process material parameter collection
    if (CloudMPC)
    {
        if (Mood == "calm")
            CloudMPC->SetVectorParameterValue("WallTint", FLinearColor(1.0, 1.0, 1.0));  // White
        else if (Mood == "uneasy")
            CloudMPC->SetVectorParameterValue("WallTint", FLinearColor(1.0, 0.95, 0.9));  // Warm yellow
        else if (Mood == "strained")
            CloudMPC->SetVectorParameterValue("WallTint", FLinearColor(1.0, 0.8, 0.7));  // Orange
        else if (Mood == "critical")
            CloudMPC->SetVectorParameterValue("WallTint", FLinearColor(1.0, 0.6, 0.5));  // Red
    }
}
```

#### 2. **`frame["npcs"]`** → Draw NPCs on Minimap
```cpp
void UMallMinimapWidget::UpdateNPCMarkers(TArray<FNPCData> NPCs)
{
    // Clear old markers
    NPCMarkers.Empty();

    for (const FNPCData& NPC : NPCs)
    {
        // Get zone position (map zone_id to 2D minimap coords)
        FVector2D MinimapPos = ZoneToMinimapPosition(NPC.Zone);

        // Create marker widget
        UImage* Marker = NewObject<UImage>();
        Marker->SetBrushFromTexture(NPCIconTexture);

        // Color by state
        if (NPC.State == "alert" || NPC.State == "suspicious")
            Marker->SetColorAndOpacity(FLinearColor::Yellow);
        else if (NPC.State == "hostile")
            Marker->SetColorAndOpacity(FLinearColor::Red);
        else if (NPC.State == "contradiction")
            Marker->SetColorAndOpacity(FLinearColor::Magenta);  // Glitching
        else
            Marker->SetColorAndOpacity(FLinearColor::White);

        // Position on minimap
        MinimapCanvas->AddChildToCanvas(Marker);
        Marker->SetRenderTranslation(MinimapPos);

        NPCMarkers.Add(Marker);
    }
}
```

#### 3. **`frame["events"]`** → Show "Glitch" Lines
```cpp
void UMallSimSubsystem::ProcessEvents(TArray<FGameEvent> Events)
{
    for (const FGameEvent& Event : Events)
    {
        if (Event.Type == "cloud_mood_changed")
        {
            // Trigger screen glitch VFX
            SpawnGlitchEffect(GlitchType::ScreenDistortion, 0.5f);
        }
        else if (Event.Type == "contradiction_triggered")
        {
            // Trigger heavy glitch + camera shake
            SpawnGlitchEffect(GlitchType::HeavyDistortion, 2.0f);
            PlayerController->ClientStartCameraShake(ContradictionCameraShake);

            // Show glitch lines on screen
            ShowGlitchLines(Event.Details["npc_id"]);
        }
        else if (Event.Type == "zone_entered")
        {
            // Minor glitch on zone transition
            SpawnGlitchEffect(GlitchType::Flicker, 0.2f);
        }
    }
}

void UMallSimSubsystem::SpawnGlitchEffect(EGlitchType Type, float Duration)
{
    // Spawn Niagara VFX or adjust post-process
    switch (Type)
    {
        case GlitchType::Flicker:
            // Brief brightness flash
            PostProcessMID->SetScalarParameterValue("GlitchIntensity", 0.3f);
            break;
        case GlitchType::ScreenDistortion:
            // Chromatic aberration spike
            PostProcessMID->SetScalarParameterValue("ChromaShift", 0.5f);
            break;
        case GlitchType::HeavyDistortion:
            // Full screen glitch lines + distortion
            PostProcessMID->SetScalarParameterValue("GlitchIntensity", 1.0f);
            PostProcessMID->SetScalarParameterValue("ScanLines", 1.0f);
            break;
    }

    // Fade out effect over duration
    GetWorld()->GetTimerManager().SetTimer(
        GlitchTimer,
        [this]() { PostProcessMID->SetScalarParameterValue("GlitchIntensity", 0.0f); },
        Duration,
        false
    );
}

void UMallSimSubsystem::ShowGlitchLines(FString NPCID)
{
    // Spawn 2D glitch line widget
    if (GlitchLineWidgetClass)
    {
        UGlitchLineWidget* Widget = CreateWidget<UGlitchLineWidget>(GetWorld(), GlitchLineWidgetClass);
        Widget->SetNPCID(NPCID);
        Widget->AddToViewport(1000);  // High Z-order
        Widget->PlayGlitchAnimation();
    }
}
```

---

## 🎯 Quick Start

### 1. Start the Bridge Server

```bash
cd v6-nextgen
python src/bridge_server.py --auto-init --port 5005
```

Server runs on `http://127.0.0.1:5005`

### 2. UE5 Calls Bridge from Game Instance

**BeginPlay:** Check server is online
**Tick:** Call `/tick` every 0.25s of game time
**EndPlay:** Optional cleanup (server persists state)

---

## 📡 UE5 Integration Points

### On Game Start (BeginPlay)

```cpp
// UMallSimSubsystem::Initialize()
void UMallSimSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);

    // 1. Health check
    CheckBridgeHealth();
}

void UMallSimSubsystem::CheckBridgeHealth()
{
    TSharedRef<IHttpRequest> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL("http://127.0.0.1:5005/health");
    Request->SetVerb("GET");
    Request->OnProcessRequestComplete().BindUObject(this, &UMallSimSubsystem::OnHealthResponse);
    Request->ProcessRequest();
}

void UMallSimSubsystem::OnHealthResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess)
{
    if (bSuccess && Response.IsValid())
    {
        UE_LOG(LogMall, Log, TEXT("Bridge server is online"));
        bBridgeReady = true;
    }
    else
    {
        UE_LOG(LogMall, Error, TEXT("Bridge server not responding"));
        bBridgeReady = false;
    }
}
```

---

### On Game Tick (Fixed Interval)

**Recommended Tick Rate:** 4Hz (every 0.25s of game time)

```cpp
// UMallSimSubsystem::Tick()
void UMallSimSubsystem::Tick(float DeltaTime)
{
    if (!bBridgeReady) return;

    // Accumulate delta time
    SimAccumulator += DeltaTime;

    // Tick simulation at fixed interval (4Hz)
    if (SimAccumulator >= 0.25f)
    {
        SendTickRequest(SimAccumulator);
        SimAccumulator = 0.0f;
    }
}

void UMallSimSubsystem::SendTickRequest(float dt)
{
    // Build JSON request
    TSharedPtr<FJsonObject> RequestJson = MakeShareable(new FJsonObject);
    RequestJson->SetNumberField("dt", dt);

    // Add player event if player did something
    if (PlayerMovedThisFrame)
    {
        TSharedPtr<FJsonObject> PlayerEvent = MakeShareable(new FJsonObject);
        PlayerEvent->SetStringField("type", "move");
        PlayerEvent->SetStringField("to_zone", CurrentZone);
        PlayerEvent->SetStringField("from_zone", PreviousZone);
        RequestJson->SetObjectField("player_event", PlayerEvent);
    }

    // Serialize to JSON string
    FString RequestBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&RequestBody);
    FJsonSerializer::Serialize(RequestJson.ToSharedRef(), Writer);

    // Send request
    TSharedRef<IHttpRequest> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL("http://127.0.0.1:5005/tick");
    Request->SetVerb("POST");
    Request->SetHeader("Content-Type", "application/json");
    Request->SetContentAsString(RequestBody);
    Request->OnProcessRequestComplete().BindUObject(this, &UMallSimSubsystem::OnTickResponse);
    Request->ProcessRequest();
}
```

---

### On Tick Response (Apply to UE5)

**Use Case:** Update Cloud effects, NPC AI, environment

```cpp
void UMallSimSubsystem::OnTickResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess)
{
    if (!bSuccess || !Response.IsValid()) return;

    // Parse JSON response
    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Response->GetContentAsString());
    if (!FJsonSerializer::Deserialize(Reader, JsonObject)) return;

    // 1. Update Cloud state
    const TSharedPtr<FJsonObject>* CloudObj;
    if (JsonObject->TryGetObjectField("cloud", CloudObj))
    {
        float CloudLevel = (*CloudObj)->GetNumberField("level");
        FString CloudMood = (*CloudObj)->GetStringField("mood");

        // Apply to environment (post-process, lighting, audio)
        ApplyCloudEffects(CloudLevel, CloudMood);
    }

    // 2. Update NPCs
    const TArray<TSharedPtr<FJsonValue>>* NPCArray;
    if (JsonObject->TryGetArrayField("npcs", NPCArray))
    {
        for (const TSharedPtr<FJsonValue>& NPCValue : *NPCArray)
        {
            const TSharedPtr<FJsonObject>& NPCObj = NPCValue->AsObject();

            FString NPCID = NPCObj->GetStringField("id");
            FString State = NPCObj->GetStringField("state");
            FString BehaviorHint = NPCObj->GetStringField("behavior_hint");

            // Apply to NPC actor
            UpdateNPCBehavior(NPCID, State, BehaviorHint);
        }
    }

    // 3. Check for events
    const TArray<TSharedPtr<FJsonValue>>* EventArray;
    if (JsonObject->TryGetArrayField("events", EventArray))
    {
        for (const TSharedPtr<FJsonValue>& EventValue : *EventArray)
        {
            const TSharedPtr<FJsonObject>& EventObj = EventValue->AsObject();
            FString EventType = EventObj->GetStringField("type");

            if (EventType == "contradiction_triggered")
            {
                // Trigger VFX, sound, camera shake, etc.
                OnContradictionEvent(EventObj);
            }
        }
    }
}
```

---

## 🎨 Minimal Implementation (Phase 1)

**For prototype, you only need to use:**

### 1. Cloud Level → Post-Process
```cpp
void UMallSimSubsystem::ApplyCloudEffects(float CloudLevel, FString CloudMood)
{
    // Map Cloud level to post-process intensity
    float GrainIntensity = FMath::Clamp(CloudLevel / 100.0f, 0.0f, 1.0f);
    float ChromaShift = FMath::Clamp((CloudLevel - 50.0f) / 50.0f, 0.0f, 1.0f);

    // Update post-process material parameters
    if (PostProcessMID)
    {
        PostProcessMID->SetScalarParameterValue("GrainIntensity", GrainIntensity);
        PostProcessMID->SetScalarParameterValue("ChromaShift", ChromaShift);
    }

    // Audio mix
    if (CloudMood == "critical")
    {
        UAudioMixerBlueprintLibrary::SetSubmixEffectChainOverride(
            this, CriticalAudioSubmix, CriticalEffectChain, 2.0f
        );
    }
}
```

### 2. NPC Behavior Hints → Behavior Trees
```cpp
void UMallSimSubsystem::UpdateNPCBehavior(FString NPCID, FString State, FString BehaviorHint)
{
    // Find NPC actor by ID
    AMallNPC* NPC = FindNPCByID(NPCID);
    if (!NPC) return;

    // Update blackboard
    if (UBlackboardComponent* BB = NPC->GetBlackboardComponent())
    {
        // Map simulation state to blackboard keys
        if (State == "contradiction")
        {
            BB->SetValueAsBool("IsContradicting", true);
        }

        // Map behavior hint to BT task
        if (BehaviorHint == "patrol_route")
        {
            BB->SetValueAsEnum("BehaviorMode", 0); // Patrol
        }
        else if (BehaviorHint == "freeze_loop")
        {
            BB->SetValueAsEnum("BehaviorMode", 1); // Freeze
        }
    }
}
```

---

## 📊 Data You Get from Bridge

### Every Tick, You Receive:

**Cloud State:**
- `cloud.level` (0-100) → Use for post-process intensity
- `cloud.mood` ("calm", "uneasy", "strained", "critical") → Use for audio mix snapshots

**NPC Updates:**
- `npc.state` → Map to AI state (idle, patrol, alert, contradiction)
- `npc.behavior_hint` → Suggested animation/BT task

**Events (Optional):**
- `contradiction_triggered` → Play VFX/SFX
- `cloud_mood_changed` → Transition audio/visuals

**Zones (Advanced):**
- `zone.turbulence` → Per-zone VFX intensity
- `zone.adjacency` → Dynamic navigation weights (optional)

---

## 🔧 Player Event Types

**What UE5 Sends to Bridge:**

### Move Event
```json
{
  "type": "move",
  "to_zone": "FC-ARCADE",
  "from_zone": "CORRIDOR"
}
```
**When:** Player enters new zone trigger volume

### Interact Event
```json
{
  "type": "interact",
  "target": "bag_of_screams",
  "zone": "FC-ARCADE"
}
```
**When:** Player presses E on interactable object

### Discover Event
```json
{
  "type": "discover",
  "document": "log_017",
  "zone": "SERVICE_HALL"
}
```
**When:** Player picks up lore document

### Wait Event
```json
{
  "type": "wait"
}
```
**When:** Player is idle (no significant action)

---

## 🏗️ Implementation Checklist

### Phase 1: Minimal Integration (Week 1)
- [ ] Create `UMallSimSubsystem` (Game Instance Subsystem)
- [ ] Implement health check on `BeginPlay`
- [ ] Implement tick accumulator (4Hz fixed rate)
- [ ] Parse `/tick` response JSON
- [ ] Map `cloud.level` → post-process material parameter
- [ ] Map `cloud.mood` → audio mix snapshot (4 snapshots)

### Phase 2: NPC Integration (Week 2)
- [ ] Create zone trigger volumes
- [ ] Send `move` events when player enters zones
- [ ] Parse `npcs` array from `/tick` response
- [ ] Map `npc.state` → blackboard enum
- [ ] Map `npc.behavior_hint` → BT task selector
- [ ] Test janitor NPC patrol → contradiction transition

### Phase 3: Events & Polish (Week 3)
- [ ] Parse `events` array from `/tick` response
- [ ] Trigger VFX on `contradiction_triggered` event
- [ ] Trigger camera shake on `cloud_mood_changed` to "critical"
- [ ] Add interactable objects (send `interact` events)
- [ ] Add discoverable documents (send `discover` events)

### Phase 4: Advanced Features (Optional)
- [ ] Per-zone turbulence VFX (from `zones` object)
- [ ] Dynamic NPC navigation using `zone.adjacency` weights
- [ ] Cloud persistence (bridge saves state between sessions)
- [ ] Debug UI showing Cloud level + NPC states

---

## 🚨 Error Handling

### Bridge Not Responding
```cpp
void UMallSimSubsystem::OnHealthResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess)
{
    if (!bSuccess)
    {
        UE_LOG(LogMall, Warning, TEXT("Bridge not responding. Falling back to local simulation."));
        bBridgeReady = false;
        // Optionally: run simplified local Cloud logic
    }
}
```

### Tick Request Failed
```cpp
void UMallSimSubsystem::OnTickResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess)
{
    if (!bSuccess)
    {
        UE_LOG(LogMall, Warning, TEXT("Tick request failed. Using last known state."));
        // Continue using cached Cloud/NPC state from previous tick
        return;
    }
}
```

---

## 📈 Performance Notes

**Network Overhead:**
- 4Hz tick rate = ~240 requests/minute
- Response size: ~2-5KB per tick (depends on zone/NPC count)
- Total bandwidth: ~500KB-1.2MB per minute
- **Impact:** Negligible on localhost

**Latency:**
- Local bridge (127.0.0.1): <5ms per request
- Python simulation: ~1-5ms per tick
- JSON serialization: <1ms
- **Total:** <10ms per tick (acceptable for 4Hz)

**Optimization (if needed):**
- Use binary protocol (MessagePack, Protocol Buffers)
- Reduce tick rate to 2Hz (dt=0.5s)
- Filter NPC updates (only send NPCs near player)

---

## 🧪 Testing Without UE5

Use the CLI demo client:

```bash
# Check bridge is up
python cli_demo.py --status-only

# Run single tick
python cli_demo.py --once

# Run loop (simulates gameplay)
python cli_demo.py --iterations 50 --delay 0.25
```

This proves the bridge works before building UE5 integration.

---

## 📖 Further Reading

- **API.md** - Complete API reference with locked JSON contracts
- **V6_BRIDGE_IMPLEMENTATION_SPEC.md** - Bridge architecture details
- **V6_UE5_ACE_INTEGRATION_ANALYSIS.md** - Strategic overview

---

**Questions?** Check logs in bridge server terminal. All errors include stack traces.

**End of UE5 Integration Guide**
