# SORA SCENE PROMPT TEMPLATE

Complete template for generating video scenes. Copy, fill parameters, run.

---

## TEMPLATE (Copy Below)

```
[SHOT COMMAND]
<<command-name>>

[LOCATION]
Zone: {zone_code}
Zone Name: {canonical_name}
Elevation: {Z=0 main floor | Z=-1 sunken | Z=+1 upper level}
Era: {1981 | 1985 | 1995 | 2005 | 2011 | V6}

[ARCHITECTURE]
Key Features: {glass block wall | elevator shaft | escalator | fountain | etc.}
Measurements: {reference v5 CRD if available}
Signage: {store names, marquees, wayfinding}
Condition: {pristine | worn | abandoned | demolished}

[CLOUD STATE]
Pressure: {0-100}
Mood: {tension | wander | surge | bleed}
Bleed Tier: {0 | 1 | 2 | 3+}
Effect: {visual/audio glitches, geometry distortion, temporal anomalies}

[POPULATION]
Density: {empty | sparse | moderate | crowded}
Anchor NPCs: {list 0-3 anchor NPCs by name}
Swarm NPCs: {count, behavior pattern}
Blocking: {triangular | linear | scattered | centered}

[CAMERA]
Type: {static | slow dolly | tracking | POV walk | crane | orbital}
Movement: {describe path/speed}
Focal Length: {wide 24mm | standard 50mm | tight 85mm}
Height: {eye level | low | elevated | aerial}
Duration: {5s | 10s | 30s | etc.}

[LIGHTING]
Source: {natural sunlight through tensile roof | fluorescent | dim emergency | exterior twilight}
Quality: {bright even | harsh shadows | soft ambient | stale}
Color Temp: {warm | neutral | cool | flickering}
Time of Day: {morning | midday | afternoon | evening | night}

[AUDIO]
Ambient: {HVAC hum | fountain splash | footsteps | silence}
Foreground: {dialogue muffled | arcade machines | elevator bell | music}
Effects: {echo | reverb | spatial desync | auditory hallucination}
Contradictions: {sound sources that don't match visuals}

[NARRATIVE TAGS]
Mood: {liminal | nostalgic | ominous | playful | melancholic}
Contradiction: {optional: core contradiction being expressed}
Memory Type: {echo | recursion | bleed | anchor}

[REFERENCES]
Photos: {eastlandpics IDs or file paths}
CRD Zone: {v5 zone graph reference}
Measurements: {v5 measurement sheet if applicable}
Canon Doc: {path to canonical zone definition}

[MODIFIERS]
Apply: {<<glitch-soft>> | <<memory-loop>> | <<echo-drift>> | etc.}
```

---

## EXAMPLE: FC-ARCADE Cold Open

```
[SHOT COMMAND]
<<cold-open>>

[LOCATION]
Zone: FC-ARCADE
Zone Name: JOLLY TIME (1985-2002) / HARD COPY (V6)
Elevation: Z=-1 (sunken pit, -12 to -15 feet below main floor)
Era: 2005 (post-JOLLY TIME relocation, pre-closure)

[ARCHITECTURE]
Key Features: Glass block acoustic wall (green/teal, multi-story), four-story blue glass elevator shaft (arched top), red JOLLY TIME marquee (background), vertical well structure, balcony walkways above
Measurements: Glass block wall ~15ft height, pit depth -12ft, elevator shaft 4 stories
Signage: "JOLLY TIME" red bold lettering (distant, partially visible)
Condition: Abandoned but clean, preserved, eerie

[CLOUD STATE]
Pressure: 74
Mood: High Cloud (abandoned, liminal, entropy manifest)
Bleed Tier: 1
Effect: Auditory hallucination (arcade pings in silence)

[POPULATION]
Density: Empty
Anchor NPCs: None
Swarm NPCs: 0
Blocking: N/A

[CAMERA]
Type: Static wide
Movement: Slight slow push-in toward marquee (barely perceptible)
Focal Length: Wide 24mm
Height: Elevated (upper balcony perspective looking down into pit)
Duration: 12s

[LIGHTING]
Source: Fluorescent overhead
Quality: Even, stale, flat
Color Temp: Cool white (institutional)
Time of Day: Indeterminate (interior, no windows)

[AUDIO]
Ambient: HVAC hum, fluorescent buzz
Foreground: Silence
Effects: Faint arcade machine pings (auditory hallucination), spatial echo
Contradictions: Machine sounds from cabinets that are powered off

[NARRATIVE TAGS]
Mood: Liminal, nostalgic, ominous
Contradiction: "A place built for chaos that is remembered as quiet"
Memory Type: Echo persistence (memories linger in this space)

[REFERENCES]
Photos: v6-nextgen/assets/photos/eastland-archive/453147355_7b0ad2b93e_c.jpg
CRD Zone: v5-eastland/docs/crd/zones/FC-ARCADE.json (if exists)
Measurements: Glass block wall 15ft, pit depth -12ft
Canon Doc: v6-nextgen/canon/zones/FC-ARCADE_jolly_time.md

[MODIFIERS]
Apply: <<glitch-soft>> (5s overlay at end), <<echo-drift>> (arcade pings)
```

---

## EXAMPLE: Anchor Three Character Scene

```
[SHOT COMMAND]
<<anchor-three>>

[LOCATION]
Zone: FC-ARCADE
Zone Name: JOLLY TIME / HARD COPY
Elevation: Z=-1
Era: V6 (HARD COPY vault era)

[ARCHITECTURE]
Key Features: Glass block wall (acoustic barrier), arcade cabinet remnants integrated with bookshelves, elevator shaft visible in background
Measurements: Per v5 CRD
Signage: HARD COPY signage (repurposed JOLLY TIME marquee structure)
Condition: Hybrid bookstore-arcade reliquary, eclectic, dense with media

[CLOUD STATE]
Pressure: 62
Mood: Wander (nostalgic, ambient)
Bleed Tier: 0-1
Effect: Subtle temporal layering

[POPULATION]
Density: Sparse
Anchor NPCs: Janitor, Husband, Wife (Bookstore)
Swarm NPCs: 1 (background browser)
Blocking: Triangular - Janitor at outer boundary (refuses to cross threshold), Husband examining arcade cabinet integrated into bookshelf, Wife at center (spatial memory gestures)

[CAMERA]
Type: Slow dolly
Movement: Arc from left to right, 90° over 20s
Focal Length: Standard 50mm
Height: Eye level
Duration: 20s

[LIGHTING]
Source: Mixed fluorescent + warm shelf lighting
Quality: Soft ambient, layered shadows
Color Temp: Warm (bookstore) blending with cool (arcade remnants)
Time of Day: Afternoon

[AUDIO]
Ambient: Page turns, soft footsteps, HVAC
Foreground: Muffled dialogue (Wife explaining layout), Husband's tool sounds
Effects: Faint arcade echo (memory bleed)
Contradictions: Wife describes machines she "never saw" with perfect accuracy

[NARRATIVE TAGS]
Mood: Nostalgic, uncanny recognition
Contradiction: "Remembering what was never experienced"
Memory Type: Echo recursion (Wife's spatial memory impossibility)

[REFERENCES]
Photos: TBD (HARD COPY V6 reference)
CRD Zone: FC-ARCADE canonical doc
Measurements: v5 measurement sheet
Canon Doc: v6-nextgen/canon/zones/FC-ARCADE_jolly_time.md

[MODIFIERS]
Apply: <<memory-loop>> (8s Wife overlay: 1985 arcade → V6 bookstore), subtle <<glitch-soft>> on Husband's tool appearance
```

---

## USAGE NOTES

1. **Copy template** → Fill all fields → Run through Sora/Runway
2. **Mandatory fields:** Location, Cloud State, Camera, Lighting
3. **Optional fields:** Can be omitted if not relevant (e.g., Audio contradictions)
4. **References:** Always link to photo evidence and canon docs
5. **Era accuracy:** Match details to era (no post-2011 content in 1981 scenes)
6. **Measurements:** Use v5 CRD measurements when available (no hallucination)

---

## VALIDATION CHECKLIST

Before running prompt:
- [ ] Zone code matches canonical zone definition
- [ ] Era-appropriate details (signage, condition, technology)
- [ ] Cloud pressure justified (matches mood/population)
- [ ] Camera movement physically possible in space
- [ ] Photo references cited correctly
- [ ] Anchor NPC count ≤ 3 (unless special case)
- [ ] Measurements reference v5 CRD (no guessing)
- [ ] Contradictions/glitches align with bleed tier

---

*Template version: 1.0*
*Last updated: 2025-11-21*
*Integration: ai/sora/SHOT_COMMANDS.md, ai/sora/ANCHOR_NPC_POSITIONING.json*
