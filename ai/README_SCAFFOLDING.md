# AI SCAFFOLDING — Complete Setup Guide

This directory contains all AI-facing tools, templates, and canonical schemas for GLUTCHDEXMALL development.

---

## Quick Start

### For New Sessions
1. **Copy-paste:** `ai/COLD_BOOT_MACRO.md` into new Claude session
2. **Fill in mission:** Today's goal, deliverables, priority universe
3. **Begin work:** AI loads all context instantly

### For Ongoing Work
- **Sora prompts:** Use `ai/sora/PROMPT_TEMPLATE_SCENE.md`
- **Character spines:** Use `ai/spynt/anchor_npc_template.json`
- **Zone docs:** Use `ai/mallOS/zone_template.json`

---

## Directory Map

```
ai/
├── COLD_BOOT_MACRO.md          # Copy-paste into new sessions
├── SESSION_OPENER.md           # Ready-to-run templates
├── README_SCAFFOLDING.md       # This file
│
├── spynt/                      # Character behavior spines
│   ├── README.md
│   ├── anchor_npc_template.json
│   ├── swarm_npc_template.json
│   ├── EXAMPLE_janitor.json
│   └── EXAMPLE_al_gorithm.json
│
├── sora/                       # Video generation templates
│   ├── README.md
│   ├── SHOT_COMMANDS.md
│   ├── ANCHOR_NPC_POSITIONING.json
│   └── PROMPT_TEMPLATE_SCENE.md
│
├── mallOS/                     # Cloud state, zones, bleed
│   ├── README.md
│   ├── zone_template.json
│   ├── cloud_state_schema.json
│   └── bleed_rules.md
│
├── renderist/                  # Metaphysics, lore
│   └── README.md
│
├── pipelines/                  # Automation, CI/CD
│   └── README.md
│
└── models/                     # ML artifacts (future)
    └── README.md
```

---

## Usage Patterns

### Pattern 1: Generate Sora Prompt
```bash
1. Load: ai/sora/PROMPT_TEMPLATE_SCENE.md
2. Reference: ai/sora/SHOT_COMMANDS.md
3. Use: ai/sora/ANCHOR_NPC_POSITIONING.json for character selection
4. Output: Filled template ready for Sora/Runway
```

### Pattern 2: Create Anchor NPC
```bash
1. Copy: ai/spynt/anchor_npc_template.json
2. Reference examples: EXAMPLE_janitor.json, EXAMPLE_al_gorithm.json
3. Fill spine: core_memory, contradictions, triggers, relationships
4. Update: ai/sora/ANCHOR_NPC_POSITIONING.json
5. Save: ai/spynt/[character_name].json
```

### Pattern 3: Document New Zone
```bash
1. Copy: ai/mallOS/zone_template.json
2. Reference: v6-nextgen/canon/zones/FC-ARCADE_jolly_time.md
3. Fill all sections: spatial, architecture, cloud_state, metaphysics
4. Classify photos: 3-layer semantic sort
5. Save: v6-nextgen/canon/zones/[ZONE_CODE]_[zone_name].md
```

### Pattern 4: Check Cloud/Bleed Rules
```bash
1. Read: ai/mallOS/cloud_state_schema.json (system mechanics)
2. Read: ai/mallOS/bleed_rules.md (canonical behavior)
3. Apply to: Sora prompts, NPC spines, zone definitions
```

---

## Integration Points

### SORA ↔ SPYNT
- Sora prompts use anchor NPCs defined in SPYNT
- `ANCHOR_NPC_POSITIONING.json` bridges the two systems
- Character `zone_affinity` determines which NPCs appear in which scenes

### SPYNT ↔ MallOS
- Character `cloud_pressure_response` links to cloud state
- NPC `triggers` reference bleed tiers
- `zone_preferences` map to zone definitions

### SORA ↔ MallOS
- Shot commands include `cloud:` and `bleed:` modifiers
- Prompt templates reference zone canonical docs
- Visual/audio effects match bleed tier specifications

### All Systems ↔ Canon
- Canonical zone docs (v6-nextgen/canon/zones/) are source of truth
- Photo evidence anchors all definitions
- v5 CRD measurements referenced (no hallucination)

---

## Workflow Examples

### Example: Complete FC-ARCADE Video Sequence

1. **Load canonical doc:**
   ```
   Read: v6-nextgen/canon/zones/FC-ARCADE_jolly_time.md
   ```

2. **Select anchor NPCs:**
   ```
   Use: ai/sora/ANCHOR_NPC_POSITIONING.json
   Characters: Janitor, Husband, AL GORITHM
   ```

3. **Generate 3 prompts:**
   ```
   Prompt 1: <<cold-open>> (empty, high cloud)
   Prompt 2: <<anchor-three>> (Janitor/Husband/AL interaction)
   Prompt 3: <<memory-loop>> (Wife remembering arcade layout)
   ```

4. **Run through Sora:**
   ```
   Output: 3 video clips (10s, 20s, 12s)
   ```

5. **Integrate:**
   ```
   Clips become evidence for V6 narrative sequences
   ```

---

### Example: Develop New Anchor NPC (Security Guard)

1. **Copy template:**
   ```
   cp ai/spynt/anchor_npc_template.json ai/spynt/security_guard.json
   ```

2. **Fill spine:**
   ```json
   {
     "character_id": "npc_security_01",
     "name": "Security Guard",
     "role": "Mall Security",
     "era": "universal",
     "spine": {
       "core_memory": [
         "Trained to watch but not intervene",
         "Walks perimeter, never shortcuts through zones",
         "Carries radio that only receives static at night"
       ],
       "contradictions": [
         "Sees everything but reports nothing",
         "Enforces rules that no longer exist",
         "Avoids areas he's supposed to patrol (FC-ARCADE, Cinema 6)"
       ],
       ...
     }
   }
   ```

3. **Update positioning:**
   ```
   Add to ai/sora/ANCHOR_NPC_POSITIONING.json:
   {
     "id": "npc_security_01",
     "zone_affinity": "corridors_perimeter",
     "positioning_weight": 0.7
   }
   ```

4. **Define zone behaviors:**
   ```
   Add to FC-ARCADE canonical doc:
   "Security Guard: Patrols outer perimeter, never enters pit, radio static increases near glass block wall"
   ```

---

## AI-Native Development Principles

1. **Structured Data > Prose**
   - Use JSON schemas for NPCs, zones
   - Markdown for narrative/metaphysics
   - Templates enforce consistency

2. **Explicit References**
   - Link to photo evidence
   - Cite v5 CRD measurements
   - Reference canonical docs

3. **Version Awareness**
   - Tag which version (v4, v5, v6) artifact targets
   - Note era appropriateness (1981 vs 2005 vs V6)

4. **Metrology First**
   - Use measured dimensions (v5 CRD)
   - No hallucinated measurements
   - Mark proxies explicitly

5. **Reconstruction > Hallucination**
   - Base on evidence (photos, memories)
   - Fill gaps with "TBD" not guesses
   - Contradictions are features, not bugs

---

## Validation Checklists

### Sora Prompt Validation
- [ ] Zone code matches canonical definition
- [ ] Era-appropriate details (signage, fashion, tech)
- [ ] Cloud pressure justified (time, population, modifiers)
- [ ] Camera movement physically possible
- [ ] Photo references cited
- [ ] Anchor NPC count ≤ 3
- [ ] Measurements reference v5 CRD

### SPYNT Character Validation
- [ ] Unique character_id
- [ ] Core memory (3+ defining experiences)
- [ ] Contradictions (3+ internal conflicts)
- [ ] Triggers (cloud/zone/npc/temporal)
- [ ] Cloud pressure response defined
- [ ] Zone preferences specified
- [ ] Visual/audio markers described
- [ ] Metadata complete

### Zone Documentation Validation
- [ ] Photo evidence documented
- [ ] Zone ID assigned
- [ ] Cloud Prime Node status evaluated
- [ ] Architectural features documented
- [ ] MallOS integration defined
- [ ] Cloud behavior rules specified
- [ ] Renderist metaphysics explained
- [ ] SPYNT character behaviors defined
- [ ] Sora prompt anchors written
- [ ] 3-layer photo classification
- [ ] Timeline documented

---

## Next Steps After Scaffolding

1. **Populate remaining anchor NPCs** (currently 4/13 defined)
2. **Document additional zones** (FC-ARCADE is template, expand to all zones)
3. **Generate batch Sora prompts** (10-20 prompts per zone)
4. **Create swarm NPC definitions** (era-specific crowds)
5. **Build automation pipelines** (photo classification, CRD batch processing)
6. **Integrate with v6 source code** (Python simulation, rendering)

---

## Maintenance

### When Adding New Systems
1. Create README.md in ai/[system_name]/
2. Add templates (JSON/MD)
3. Add examples
4. Update this scaffolding README
5. Update COLD_BOOT_MACRO.md if needed

### When Updating Templates
1. Increment version number
2. Note changes in metadata
3. Update examples
4. Regenerate any artifacts using old template

### When Locking Canon
1. Mark `canonical_status: "locked"` in metadata
2. Update integration checklists
3. Reference in dependent systems
4. Git commit with "CANONICAL:" prefix

---

## Status: SCAFFOLDING COMPLETE ✓

**Created:** 2025-11-21
**Version:** 1.0
**Coverage:**
- ✓ SORA templates (3 files)
- ✓ SPYNT templates (4 files)
- ✓ MallOS templates (3 files)
- ✓ Cold-boot macro (1 file)
- ✓ Session opener (1 file)
- ✓ This README

**Next Session:**
Use `ai/COLD_BOOT_MACRO.md` to begin work on next phase (anchor NPCs, zone docs, batch prompts).

---

*This scaffolding enables instant context loading for ALL future AI sessions.*
