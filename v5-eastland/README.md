# EASTLAND MALL V5 - CRD RECONSTRUCTION

**Version:** 5.0-alpha
**Status:** V1 Complete - Fidelity Pass Phase
**Base:** v4-renderist architecture + photographic evidence
**Methodology:** Classification Reference Document (CRD v0.1)

---

## ⚠️ CRITICAL: READ THIS FIRST ⚠️

**Before performing ANY measurement, classification, or reconstruction work:**

📖 **[READ: README_ARCHITECTURAL_CONTEXT.md](./README_ARCHITECTURAL_CONTEXT.md)**

This document contains critical scale warnings, architectural context, and design intent that fundamentally change how you must approach this reconstruction. **Failure to read this document will result in catastrophically incorrect measurements.**

**Key points:**
- This is a **1,000,000+ sq ft megastructure**, not a conventional mall
- KKT pioneered **tensile sail technology** in the early 1980s
- Scale: "**space station with a parking lot**" - think 60-80+ foot masts, not 35 feet
- Cultural context: Built for proto-Silicon Valley tech culture in Tulsa
- This is **architectural archaeology**, not game map creation

**READ THE CONTEXT DOCUMENT BEFORE PROCEEDING.**

---

## Purpose

V5 represents a **methodical reconstruction** of Eastland Mall using the Classification Reference Document (CRD) workflow. Unlike V3 (direct tile edits) or V4 (cloud-driven semantics), V5 follows a systematic evidence-based approach:

1. **Classify** all 153 photos into PRIMARY CLASSES
2. **Extract** measurable features using atomic units
3. **Build** zone graph from logical relationships
4. **Measure** geometry using calibrated features
5. **Document** contradictions and historical layers
6. **Propose** new map structure with full traceability

---

## Directory Structure

```
v5-eastland/
├── README.md                                 # This file
├── README_ARCHITECTURAL_CONTEXT.md           # ⚠️ REQUIRED READING - Scale warnings + intent
├── docs/
│   ├── BATCH_PROCESSING_PLAN.md              # Guide for fidelity passes
│   │
│   ├── crd/                                  # CRD Workflow Documents (V1 Complete)
│   │   ├── PHOTO_CLASSIFICATION_TABLE_V1_COMPLETE.md  # Step 1: 143 photos classified
│   │   ├── FEATURE_EXTRACTION_TABLE.md                # Step 2: 11 measurable features
│   │   ├── ZONE_GRAPH_V1.md                           # Step 3: 9 structural zones
│   │   ├── MEASUREMENT_SHEET_V1.csv                   # Step 5: 15 measurements extracted
│   │   ├── MAP_CORRECTIONS_LIST_V1.md                 # Step 6: 12 corrections synthesized
│   │   └── (future: BATCH_X classification tables)    # Additional photo batches
│   │
│   └── schemas/
│       └── world_spine_base.json             # Inherited from v4
│
├── data/
│   └── MALL_MAP_V5_PROPOSAL.json             # V1 Complete - Zone-based map with CRD measurements
│
└── (future: src/)                            # Implementation code if needed
```

---

## CRD Workflow Status

### V1 Baseline: COMPLETE ✅

| Step | Document | Status | Progress |
|------|----------|--------|----------|
| 1 | PHOTO_CLASSIFICATION_TABLE_V1_COMPLETE.md | ✅ COMPLETE | 100% (143/143 photos) |
| 2 | FEATURE_EXTRACTION_TABLE.md | ✅ COMPLETE | 100% (11 features) |
| 3 | ZONE_GRAPH_V1.md | ✅ COMPLETE | 100% (9 zones) |
| 4 | Stereo pairs (optional) | ⏸️ IDENTIFIED | 4 pairs identified, not processed |
| 5 | MEASUREMENT_SHEET_V1.csv | ✅ COMPLETE | 100% (15 measurements) |
| 6 | MAP_CORRECTIONS_LIST_V1.md | ✅ COMPLETE | 100% (12 corrections) |
| 7 | MALL_MAP_V5_PROPOSAL.json | ✅ COMPLETE | 100% (zone-based map) |

**V1 Deliverables:**
- 143 photos classified with PRIMARY/FEATURE/ZONE assignments
- 15 measurements extracted with confidence levels
- 12 corrections synthesized from measurements
- Complete zone-based map proposal with measured geometry
- Full photo traceability and contradiction tracking

### V2+ Fidelity Passes: PENDING 📋

**Goal:** Raise confidence levels on LOW and MEDIUM measurements using additional photo batches.

**Status:** Awaiting additional photos (older images, construction period, operational period)

**See:** [BATCH_PROCESSING_PLAN.md](./docs/BATCH_PROCESSING_PLAN.md) for detailed workflow

**Priority Targets:**
- Mast height: 35' (LOW) → 60-80+' (MEDIUM-HIGH)
- Atrium diameter: 60-80' (LOW) → 150-200+' (MEDIUM-HIGH)
- Pit depth: 8' (HIGH) → Verify or revise to 15-20+' if evidence supports
- Glass block size: Confirm 6" vs 8" for precise wall height

---

## Key Differences from V3/V4

### vs V3 (Tile-based immersive sim)
- **V3**: Direct x/y coordinate edits to existing map
- **V5**: Measurement-based reconstruction from evidence
- **Advantage**: V5 has full traceability and contradiction tracking

### vs V4 (Cloud-driven semantic spaces)
- **V4**: Zone-based adjacency with abstract relationships
- **V5**: Geometric precision with semantic zones
- **Advantage**: V5 merges both approaches - zones WITH measured geometry

---

## Measurable Atomic Units (From CRD)

V5 uses these features as "rulers" for accurate scaling:

| Feature | Dimensions | Use Case |
|---------|------------|----------|
| Glass Block | 6×6" or 8×8" | Atrium wall radius, grid alignment |
| Coca-Cola Vending Machine | 39" × 72" | Global scale calibration anchor |
| Exit Sign | 8.75" × 10.5" | Corridor scaling |
| Escalator Step | 8" rise | Z-level height differential |
| Ceiling Tile | 2' × 4' | Anchor store interior scale |
| Column Diameter | ~18-24" | Grid spacing estimation |

---

## Photo Evidence Base

**Total Photos:** 153 (in `/eastlandpics/`)

**Key Reference Photos:**
- Fountain: 453127566, 453126954, 453127262, 453127434
- Tensile Roof: 453124750, 64360891, 453125654
- Escalators: 3085976410, 3085979988
- Food Court: 453143417, 64360891
- Mickey's Wing: 46099761
- Coca-Cola Store: 3085977904, 3085977656
- Simon Map: 64360768

---

## Contradiction Tracking

Unlike V3 (which resolved conflicts immediately), V5 **documents contradictions as historical layers**:

- Corridor width mismatches between eras
- Food court angles changed over renovations
- Tent fabric replacement vs. original
- Anchor store footprint drift
- Escalator height inconsistencies

**Contradictions are NOT errors** — they are timeline variance.

---

## V1 Completed Actions ✅

1. ✅ Created directory structure
2. ✅ Created PHOTO_CLASSIFICATION_TABLE_V1_COMPLETE.md (143/143 photos)
3. ✅ Created FEATURE_EXTRACTION_TABLE.md (11 measurable features)
4. ✅ Created ZONE_GRAPH_V1.md (9 structural zones)
5. ✅ Created MEASUREMENT_SHEET_V1.csv (15 measurements)
6. ✅ Created MAP_CORRECTIONS_LIST_V1.md (12 corrections)
7. ✅ Created MALL_MAP_V5_PROPOSAL.json (complete zone-based map)
8. ✅ Created README_ARCHITECTURAL_CONTEXT.md (critical scale + intent documentation)
9. ✅ Created BATCH_PROCESSING_PLAN.md (guide for fidelity passes)

## Next Actions (V2+ Fidelity Passes)

1. ⏳ **CURRENT**: Awaiting additional photo batches
2. ⏳ Process Batch 1: Scale anchors (mast height, atrium diameter, pit depth verification)
3. ⏳ Process Batch 2: Zone footprints (1M+ sq ft mapping, subterranean access points)
4. ⏳ Process Batch 3: Corridor networks (full circulation system)
5. ⏳ Process Batch 4: Historical/operational period documentation
6. ⏳ Create MEASUREMENT_SHEET_V_FINAL.csv with highest confidence levels
7. ⏳ Create MALL_MAP_V5_FINAL.json with refined measurements
8. ⏳ Create HISTORICAL_COMPARISON_V_FINAL.md (future vs. decline timeline)

---

## Dependencies

- **Base Data**: v4-renderist/docs/schemas/world_spine.json
- **Photo Evidence**: /eastlandpics/ (153 images)
- **Reference Maps**: V3 mall_map.json, Simon map photo (64360768)

---

## Contact / Notes

This is a **systematic reconstruction**, not a quick fix. The goal is to create a fully-traceable, measurement-based map that can be validated against photographic evidence.

All decisions must be documented in CRD workflow files with confidence levels and source photo references.

---

*Last Updated: 2025-11-21*
*Maintainer: Claude (Architect Mode)*
