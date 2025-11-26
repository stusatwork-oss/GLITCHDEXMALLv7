# BATCH PROCESSING PLAN - EASTLAND MALL FIDELITY PASSES

**Version:** 2.0
**Date:** 2025-11-21
**Purpose:** Guide for processing additional photo batches to raise confidence levels on v5 measurements

---

## PROJECT CONTEXT

### What This Is
Eastland Mall was a **1 million+ square foot** pioneering tensile sail architecture project built by KKT architects in Tulsa, OK for SIMON in the early 1980s. This was not a conventional mall - this was **futurist megastructure architecture** for proto-Silicon Valley tech culture in Tulsa.

### Scale Revelation
**CRITICAL:** Do not use conventional mall metrics. This is a "space station with a parking lot."

- **Footprint:** 1,000,000+ sq ft above ground, plus subterranean level
- **Central Atrium:** 150-200+ feet diameter (not 60-80')
- **Tension Masts:** 60-80+ feet tall (not 35')
- **Food Court Bowl:** 8+ feet deep, possibly 15-20+ feet total descent
- **6-Screen Theater:** Underground at center of food court, visible as "black open mouth" at escalator terminus

### Architectural Significance
- **Pioneering tensile sail technology** (early 1980s experimental)
- **4 yellow lattice tension masts** with 32 radial cable geometry
- **Space-age engineering** as cultural statement for tech workers
- **"Reactor containment zone" food court** - industrial theater aesthetic
- **Cathedral-scale public spaces** - train station/airport terminal volumes

---

## V1 BASELINE (COMPLETED)

### Documents Created
- `PHOTO_CLASSIFICATION_TABLE_V1_COMPLETE.md` - 143 photos classified
- `FEATURE_EXTRACTION_TABLE.md` - 11 feature classes
- `ZONE_GRAPH_V1.md` - 9 structural zones
- `MEASUREMENT_SHEET_V1.csv` - 15 measurements extracted
- `MAP_CORRECTIONS_LIST_V1.md` - 12 corrections documented
- `MALL_MAP_V5_PROPOSAL.json` - Complete v5 zone-based map

### Photo Base
- **Source Folder:** `/eastlandpics/`
- **Count:** 143 photos classified
- **Coverage:** Heavy on central atrium/tensile roof (Z1), lower corridors (Z3, 68 photos), food court (Z4, 17 photos)
- **Gaps:** Z7 subterranean (0 photos), Z6 theater (1 photo), Z2 upper ring (8 photos)

### Current Confidence Levels

**HIGH Confidence:**
- Food court pit depth: 8 feet (12 escalator steps × 8" - **may be conservative**)
- Fountain tiers: 4 levels
- Tensile roof cables: 32 radial
- Balcony railings: 42 inches
- Door frames: 80 inches

**MEDIUM Confidence (targets for improvement):**
- Glass block wall height: 14-18 feet (depends on 6" vs 8" block verification)
- Glass block wall arc: 22.5 feet
- Fountain depth: ~6 feet
- Corridor widths: 12-20 feet

**LOW Confidence (priority targets):**
- Truss mast height: ~35 feet → **REVISE to 60-80+ feet**
- Atrium diameter: 60-80 feet → **REVISE to 150-200+ feet**
- FOOD COURT sign diameter: 6-8 feet
- Column spacing: ~20 feet
- Tensile roof span: 80-100 feet → **REVISE to 150-200+ feet**

**UNVERIFIED:**
- Z7 Subterranean interior (off-limits forever - but exterior access points can be documented)
- Z6 Theater interior (only 1 exterior photo in v1)

---

## BATCH PROCESSING STRATEGY

### New Photo Source
- **Folder:** To be specified (likely `/eastlandpics_batch2/` or similar)
- **Type:** Older photos, additional angles, construction/operational period images
- **Expected Volume:** Large batch requiring systematic processing

### BATCH 1: SCALE ANCHORS (Priority 1)

**Goal:** Raise LOW → MEDIUM or HIGH confidence on critical measurements

**Target Photos:**
- Mast height with ground reference visible (full base-to-top)
- Atrium diameter/span (perimeter-to-perimeter, wide-angle views)
- Theater entrance dimensions (facing "the black open mouth")
- Escalator full descent (may reveal deeper than 8 feet)
- Glass block wall closeups (confirm 6" vs 8" block size)
- Column spacing with clear reference points

**Processing Method:**
1. Classify photos by PRIMARY CLASS (same hierarchy as v1)
2. Extract measurements immediately when scale anchors visible
3. Cross-reference with v1 measurements
4. Document discrepancies (timeline variance vs. measurement error)

**Output Files:**
- `PHOTO_CLASSIFICATION_BATCH_1.md` (new photos classified)
- `MEASUREMENT_SHEET_V2.csv` (updated measurements with batch source noted)
- `SCALE_REVISION_NOTES_V2.md` (document changes from v1)

**Key Measurements to Revise:**
- Mast height: 35' → **60-80+' (target)**
- Atrium diameter: 60-80' → **150-200+' (target)**
- Pit depth: 8' → **Verify or increase to 15-20+' if evidence supports**

---

### BATCH 2: ZONE FOOTPRINTS (Priority 2)

**Goal:** Map the 1M+ sq ft footprint accurately

**Target Photos:**
- Overhead/aerial views (if available)
- Exterior facade showing full building extent
- Corridor termination points (wing endpoints)
- Anchor store exteriors and footprints (Dillard's, Mervyn's, Mickey's)
- Parking lot views showing scale
- Subterranean entrance locations (ramps, service doors, vent stacks)

**Processing Method:**
1. Identify cardinal directions and orientation
2. Map wing extents relative to central atrium
3. Document anchor store positions
4. Mark subterranean access points on exterior
5. Estimate zone square footage where possible

**Output Files:**
- `PHOTO_CLASSIFICATION_BATCH_2.md`
- `ZONE_FOOTPRINT_MAP_V2.md` (revised zone sq ft estimates)
- `SUBTERRANEAN_ACCESS_POINTS.md` (exterior entrances documented)

**Target Zones:**
- Z8 Anchor Stores: Document Mickey's concentric arch, other anchor footprints
- Z9 Exterior: Full perimeter, parking lot scale
- Z7 Subterranean: Change status from "UNVERIFIED" to "EXTERIOR ACCESS DOCUMENTED"

---

### BATCH 3: CORRIDOR NETWORKS (Priority 3)

**Goal:** Document the full circulation system across 1M+ sq ft

**Target Photos:**
- Main spine corridors (width measurements with scale references)
- T-junctions and cross-corridors
- Wing branches to anchor stores
- Service corridor access ("STAFF ONLY" areas)
- Store frontages for position triangulation
- Upper ring balconies (Z2 - currently only 8 photos)

**Processing Method:**
1. Map corridor connectivity
2. Measure widths using door frames (80") as scale
3. Document intersection types (T, cross, Y-junctions)
4. Track tile/carpet transitions (zone boundaries)
5. Identify store positions for spatial anchoring

**Output Files:**
- `PHOTO_CLASSIFICATION_BATCH_3.md`
- `CORRIDOR_NETWORK_V2.md` (connectivity map)
- `STORE_DIRECTORY_V2.md` (complete store list with positions)

**Coverage Gaps to Fill:**
- Z2 Upper Ring (currently 8 photos, 5.6%)
- Z3 Lower Ring extent (68 photos but only covers fraction of 1M sq ft)

---

### BATCH 4: HISTORICAL/OPERATIONAL (Priority 4)

**Goal:** Document "the future" before the decline

**Target Photos:**
- Opening day / early operational period (1980s)
- Tensile roof during construction/installation
- Food court when active (vendors operational)
- Theater when operational (marquee lit, crowds)
- Full atrium during peak use
- Construction documentation (if available)

**Processing Method:**
1. Classify by PRIMARY CLASS (same hierarchy)
2. Add temporal metadata: "construction", "operational", "decline"
3. Document contradictions vs. decline-era photos
4. Compare "future vision" vs. "ruin" aesthetic
5. Extract KKT design intent where visible

**Output Files:**
- `PHOTO_CLASSIFICATION_BATCH_4.md`
- `HISTORICAL_COMPARISON_V2.md` (timeline analysis)
- `KKT_DESIGN_INTENT.md` (architectural vision documented)

**Historical Contradictions (from v1):**
- Food court vendor layout variance
- Tensile roof color variance (white vs. beige)
- Theater operational status
- **New:** Compare futurist vision vs. decay aesthetic

---

## PROCESSING WORKFLOW

### Per-Batch Workflow

1. **Classify Photos**
   - Use same PRIMARY/FEATURE/ZONE hierarchy from v1
   - Create `PHOTO_CLASSIFICATION_BATCH_X.md`
   - Note batch source folder and photo count

2. **Extract Measurements**
   - Update `MEASUREMENT_SHEET_VX.csv` incrementally
   - Document batch source for each measurement
   - Cross-reference with v1 measurements
   - Flag discrepancies for review

3. **Update Confidence Levels**
   - Revise LOW → MEDIUM or HIGH where new evidence supports
   - Document reasoning in `SCALE_REVISION_NOTES_VX.md`
   - Preserve v1 values for comparison

4. **Commit Progress**
   - Commit after each batch completion
   - Use descriptive commit messages with batch number
   - Push to branch: `claude/fix-eastland-mall-map-01KVRJsjQj2RdFaEDXmpFc4k`

5. **Cross-Reference**
   - Link new photos to existing zone documentation
   - Update zone descriptions with new details
   - Maintain full photo ID traceability

---

## KEY GEOMETRIC INSIGHTS

### Theater Entrance Position
**CRITICAL:** The 6-screen theater entrance is **the black open mouth** visible at the bottom of the escalator descent.

- Not "adjacent to food court" - it's the **focal terminus** of the descent
- Direct sightline: Top of escalator → 8+ feet down → theater entrance void
- Axial composition: Theater entrance = gravitational center of food court bowl
- Food vendors wrap the perimeter around theater entrance

**Impact:** Z5 (escalators) → Z6 (theater) is a direct axial relationship, not adjacency.

### Food Court as "Reactor Containment Zone"
- 8+ feet descent (possibly 15-20+ total)
- Industrial theater aesthetic - exposed structure, metal, hard surfaces
- Cathedral-scale volume above (40-60+ feet to tensile roof)
- Descent sequence creates enclosed, technological experience
- Not functional retail - **experiential architecture**

### Tensile Roof as Futurist Statement
- 32 radial cables = precision engineering made visible
- Yellow masts = structure as sculpture
- Experimental 1980s material technology
- Cultural statement: "This is what the future looks like"
- Built for minds that think in systems and engineering

---

## MEASUREMENT TARGETS

### Priority 1: Revise These First

| Feature | V1 Value | V1 Confidence | Target Value | Target Confidence | Evidence Needed |
|---------|----------|---------------|--------------|-------------------|-----------------|
| Mast Height | 35 feet | LOW | 60-80+ feet | MEDIUM-HIGH | Ground-to-top visible |
| Atrium Diameter | 60-80 feet | LOW | 150-200+ feet | MEDIUM-HIGH | Perimeter spans |
| Tensile Roof Span | 80-100 feet | LOW | 150-200+ feet | MEDIUM | Cable anchor points |
| Pit Depth | 8 feet | HIGH | 8-20+ feet | HIGH | Full descent visible |
| Glass Block Size | 6" or 8" | MEDIUM | Confirmed size | HIGH | Closeup measurement |

### Priority 2: Improve These

| Feature | V1 Value | V1 Confidence | Target Confidence | Evidence Needed |
|---------|----------|---------------|-------------------|-----------------|
| Glass Block Wall Height | 14-18 feet | MEDIUM | HIGH | Confirmed block size |
| Corridor Widths | 12-20 feet | MEDIUM | HIGH | Door frame scaling |
| Food Court Bowl Diameter | Not measured | N/A | MEDIUM | Perimeter measurement |
| Theater Entrance Width | Not measured | N/A | MEDIUM | Facing photos |

---

## ZONE DOCUMENTATION STATUS

### Well Documented (Keep Refining)
- **Z1 Central Atrium:** 32 photos - but revise scale estimates
- **Z3 Lower Ring:** 68 photos - but covers small fraction of 1M sq ft footprint
- **Z4 Food Court:** 17 photos - need theater entrance details

### Under-Documented (Priority for New Photos)
- **Z2 Upper Ring:** 8 photos (5.6%) - need more balcony/overlook views
- **Z6 Theater:** 1 photo (0.7%) - need entrance facade details (interior off-limits)
- **Z8 Anchor Stores:** 12 photos - need individual anchor footprints
- **Z9 Exterior:** 16 photos - need full perimeter/aerial views

### Special Case
- **Z7 Subterranean:** 0 photos, interior off-limits forever
  - **Strategy:** Document exterior access points only
  - Mark ramp entrances, service doors, vent stacks on exterior photos
  - Change status from "UNVERIFIED" to "EXTERIOR ACCESS DOCUMENTED"

---

## OUTPUT FILES TO CREATE

### Per Batch
- `PHOTO_CLASSIFICATION_BATCH_X.md` - Classified photos from new batch
- `MEASUREMENT_SHEET_VX.csv` - Updated measurements (incremental versions)
- `SCALE_REVISION_NOTES_VX.md` - Document changes from previous versions

### Final Deliverables (After All Batches)
- `MEASUREMENT_SHEET_V_FINAL.csv` - All measurements with highest confidence
- `ZONE_FOOTPRINT_MAP_V_FINAL.md` - Complete 1M+ sq ft zone mapping
- `CORRIDOR_NETWORK_V_FINAL.md` - Full circulation system
- `MALL_MAP_V5_FINAL.json` - Updated map proposal with refined measurements
- `HISTORICAL_COMPARISON_V_FINAL.md` - Future vs. decline timeline
- `KKT_DESIGN_INTENT.md` - Architectural vision and innovation documentation

---

## COMMIT STRATEGY

**After Each Batch:**
```
git add v5-eastland/docs/crd/PHOTO_CLASSIFICATION_BATCH_X.md
git add v5-eastland/docs/crd/MEASUREMENT_SHEET_VX.csv
git commit -m "Batch X: [brief description of findings]

- Processed [N] photos from [source]
- Revised [measurements changed]
- Confidence levels: [changes]
- Key findings: [notable discoveries]"
git push -u origin claude/fix-eastland-mall-map-01KVRJsjQj2RdFaEDXmpFc4k
```

---

## INSTRUCTIONS FOR FRESH INSTANCE

If you are a new Claude instance continuing this work:

1. **Read Context First:**
   - Read this document completely
   - Review `v5-eastland/README.md` for workflow overview
   - Read `ZONE_GRAPH_V1.md` for spatial logic
   - Read `MEASUREMENT_SHEET_V1.csv` for baseline measurements

2. **Understand Scale:**
   - This is 1M+ sq ft, not a conventional mall
   - Use "space station" scale, not retail scale
   - Masts are 60-80+ feet, not 35 feet
   - Atrium is 150-200+ feet diameter, not 60-80 feet

3. **Check Photo Source:**
   - Ask user for new photo batch folder location
   - Determine batch number (1, 2, 3, 4 based on priorities above)
   - Check which batches have already been completed

4. **Process Systematically:**
   - Follow the batch workflow above
   - Classify → Extract → Update → Commit
   - Maintain traceability to photo IDs
   - Cross-reference with v1 baseline

5. **Preserve History:**
   - Don't overwrite v1 files - create v2, v3, etc.
   - Document all changes in SCALE_REVISION_NOTES
   - Maintain measurement provenance (which batch, which photo)

---

## CRITICAL REMINDERS

- **This is architectural archaeology** of a pioneering 1980s tensile structure
- **This is historical preservation** of KKT's futurist vision for Tulsa
- **This is engineering documentation** of experimental technology
- **This is not a game map** - this was a real place where real people worked and gathered

**Every measurement matters. Every photo is evidence. Full traceability always.**

---

*Document created: 2025-11-21*
*For continuation by fresh Claude instances processing additional photo batches*
*Current baseline: V1 (143 photos, 15 measurements)*
*Target: Raise confidence levels and map full 1M+ sq ft footprint*
