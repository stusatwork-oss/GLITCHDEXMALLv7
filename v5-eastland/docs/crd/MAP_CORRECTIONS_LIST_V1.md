# MAP CORRECTIONS LIST - EASTLAND MALL V5

**Version:** 1.0
**Date:** 2025-11-21
**Methodology:** CRD v0.1 - Measurement-based correction synthesis
**Base Maps Referenced:** v3 mall_map.json, v4 world_spine.json, Simon map (photo 64360768)

---

## CORRECTION METHODOLOGY

This document synthesizes corrections from three data sources:

1. **MEASUREMENT_SHEET_V1.csv** - Extracted measurements from 143 classified photos
2. **ZONE_GRAPH_V1.md** - Spatial logic and adjacency relationships
3. **PHOTO_CLASSIFICATION_TABLE_V1_COMPLETE.md** - Visual evidence catalog

All corrections are **traceable to photographic evidence** with documented confidence levels.

---

## SECTION 1: CRITICAL GEOMETRIC CORRECTIONS (HIGH CONFIDENCE)

### 1.1 Food Court Pit Depth: 8 feet (Z=0 to Z=-1)

**Current State (v3):** Pit depth approximately 6-7 feet
**Correction Required:** **8 feet (96 inches)**
**Evidence:** MEASUREMENT_SHEET_V1.csv, entries ESF-001, ESF-002
**Source Photos:** 3085976410, 3085979988
**Measurement Method:** Escalator step count

**Details:**
- Photo 3085976410 shows **12 visible escalator steps** descending into food court
- Standard escalator step rise: **8 inches** (universal code requirement)
- Calculation: 12 steps × 8 inches = **96 inches = 8 feet**
- Photo 3085979988 confirms 11-12 step count from different angle
- **CONFIDENCE: HIGH** (based on countable steps and standard step height)

**Map Impact:**
- Food court floor at **Z = -1** (8 feet below ground level Z=0)
- Escalator landing geometry requires 12-step descent path
- Affects theater entrance positioning (theater at Z=-1 level)

---

### 1.2 Glass Block Wall Height: 14 feet

**Current State (v3):** Glass block wall extends 5 tiles vertically
**Correction Required:** **14 feet vertical height**
**Evidence:** MEASUREMENT_SHEET_V1.csv, entry GBF-001
**Source Photo:** 453127566
**Measurement Method:** Glass block count

**Details:**
- Photo 453127566 shows **28 glass blocks vertical** in fountain wall
- Assuming standard 6"×6" glass block: 28 × 6" = **168 inches = 14 feet**
- If 8"×8" blocks used: 28 × 8" = **224 inches = 18.7 feet**
- **CONFIDENCE: MEDIUM** (depends on block size verification)

**Map Impact:**
- Glass block wall reaches from Z=0 to ceiling (~14-18 feet)
- Wall forms curved backdrop for fountain tiers
- Provides visual barrier between fountain and adjacent zones

---

### 1.3 Glass Block Wall Arc Length: 22.5 feet

**Current State (v3):** Glass block wall extends 5 tiles horizontally
**Correction Required:** **22.5 feet arc length (curved)**
**Evidence:** MEASUREMENT_SHEET_V1.csv, entry GBF-001
**Source Photo:** 453127566
**Measurement Method:** Glass block count along curve

**Details:**
- Photo 453127566 shows **45 glass blocks horizontal** along curved arc
- Assuming 6"×6" blocks: 45 × 6" = **270 inches = 22.5 feet**
- Wall curves in semicircular or fan-shaped arc
- **CONFIDENCE: MEDIUM** (arc measurement affected by perspective)

**Map Impact:**
- Extends v3 wall from 5 tiles to 9+ tiles (if tiles = 3 feet each)
- Curved geometry requires arc notation, not straight line
- Fountain positioned in front of wall's concave side

---

### 1.4 Fountain Tier Count: 4 levels

**Current State (v3):** Fountain with 4 tiers
**Correction Required:** **CONFIRMED - 4 terraced levels**
**Evidence:** MEASUREMENT_SHEET_V1.csv, entry FTF-001
**Source Photos:** 453127566, 453126954, 453127262, 453127434
**Measurement Method:** Visual tier count

**Details:**
- All fountain photos consistently show **4 distinct terraced levels**
- Amphitheater-style descending toward center
- Each tier approximately 18-24 inches rise
- Total fountain depth: ~6 feet (top tier to bottom basin)
- **CONFIDENCE: HIGH** (confirmed across multiple photos)

**Map Impact:**
- V3 fountain geometry is CORRECT (4 tiers already implemented)
- Verify tier spacing: ~18-24 inches per level
- Total descent: ~6 feet

---

## SECTION 2: STRUCTURAL CORRECTIONS (MEDIUM-HIGH CONFIDENCE)

### 2.1 Tensile Roof Geometry: 4 truss masts, 32 radial cables

**Current State (v3):** Tensile roof with 4 masts
**Correction Required:** **4 masts + 32 radial cable pattern**
**Evidence:** MEASUREMENT_SHEET_V1.csv, entries TMF-001, TMF-002
**Source Photos:** 453124750, 453125654, 64360891
**Measurement Method:** Cable count

**Details:**
- Photo 453124750 shows **32 radial cables** emanating from mast tops
- Photo 453125654 confirms ~28-32 cable pattern from different angle
- 4 truss masts arranged in quadrilateral pattern (likely rectangular)
- Mast height estimated **35 feet** (very low confidence without ground reference)
- White fabric canopy tensioned between cables
- **CONFIDENCE: HIGH** (cable count), **LOW** (mast height)

**Map Impact:**
- Roof cable geometry creates 32-segment radial subdivision
- Each cable anchors to perimeter ring or balcony structure
- Mast positions define atrium center quadrilateral
- Fabric panels fill gaps between cables

---

### 2.2 Balcony Railing Height: 42 inches (standard)

**Current State:** Not explicitly defined in v3
**Correction Required:** **42 inch railing height (upper level)**
**Evidence:** MEASUREMENT_SHEET_V1.csv, entries RBF-001, RBF-002
**Source Photos:** 453143417, 3085979988
**Measurement Method:** Standard building code height

**Details:**
- Commercial building code requires **42 inch minimum railing height**
- Photos show standard railing at balcony edges and escalator landings
- Used as scaling reference for corridor measurements
- **CONFIDENCE: HIGH** (universal code requirement)

**Map Impact:**
- Upper level (Z=0) balcony has 42" railings overlooking atrium and food court
- Escalator landings have matching 42" railings
- Can be used to scale corridor widths in photos

---

### 2.3 Door Frame Heights: 80 inches (standard)

**Current State:** Not explicitly defined
**Correction Required:** **80 inch door height (6'8") for commercial doors**
**Evidence:** MEASUREMENT_SHEET_V1.csv, entry DRF-001
**Source Photos:** Multiple corridor photos
**Measurement Method:** Standard building code

**Details:**
- Standard commercial door height: **80 inches (6 feet 8 inches)**
- Visible in store entrances and corridor access points
- Provides reliable scaling reference when doors visible in photos
- **CONFIDENCE: HIGH** (universal standard)

**Map Impact:**
- Store entrance doors: 80" height
- Corridor ceiling heights can be estimated relative to door frames
- Typical mall corridor ceiling: 10-12 feet (120-144 inches)

---

## SECTION 3: ZONE ADJACENCY CORRECTIONS (BASED ON ZONE_GRAPH_V1.md)

### 3.1 Zone Z3 (Lower Corridors) → Z4 (Food Court) Connection

**Current State (v3):** Corridors connect to food court at same level
**Correction Required:** **8-foot descent via escalators (Z=0 to Z=-1)**
**Evidence:** ZONE_GRAPH_V1.md, MEASUREMENT_SHEET_V1.csv
**Source Photos:** 3085976410, 3085979988

**Details:**
- Z3 (lower corridors) at Z=0 (ground level)
- Z4 (food court) at Z=-1 (8 feet below ground)
- Connection requires escalator or stair descent
- Photos show **bidirectional escalator pair**
- **CONFIDENCE: HIGH**

**Map Impact:**
- Escalator geometry: 12 steps × 8" rise
- Escalator length: ~20-25 feet (based on standard escalator angle)
- Requires vertical transition zone between Z3 and Z4

---

### 3.2 Zone Z1 (Central Atrium) Contains Fountain + Tensile Roof

**Current State (v3):** Atrium and fountain separate entities
**Correction Required:** **Fountain is WITHIN atrium, under tensile roof**
**Evidence:** ZONE_GRAPH_V1.md, photos 453124750, 453127566
**Source Photos:** Multiple atrium photos showing roof + fountain together

**Details:**
- Fountain positioned at atrium center (or offset to one side)
- Tensile roof covers both fountain and surrounding atrium space
- Glass block wall forms curved backdrop for fountain
- 4 truss masts positioned around atrium perimeter
- **CONFIDENCE: HIGH**

**Map Impact:**
- Fountain is interior to atrium zone, not adjacent
- Atrium diameter must accommodate: fountain (22.5' arc) + walkway space
- Estimated atrium diameter: 60-80 feet

---

### 3.3 Zone Z5 (Escalator Wells) Connects Z3 ↔ Z4

**Current State (v3):** Escalators positioned near food court
**Correction Required:** **Escalators are dedicated transition zone (Z5)**
**Evidence:** ZONE_GRAPH_V1.md
**Source Photos:** 3085976410, 3085979988, 453143417

**Details:**
- Escalators form bidirectional pair (up/down)
- Positioned at edge of food court bowl
- Accessible from lower corridors (Z3)
- Descend into food court pit (Z4)
- **CONFIDENCE: HIGH**

**Map Impact:**
- Z5 is distinct zone type: vertical circulation
- Requires dedicated footprint: ~10-15 feet wide × 25 feet long per escalator
- Total escalator well: ~20-30 feet wide (including safety clearances)

---

## SECTION 4: STORE & FEATURE LOCATIONS (BASED ON PHOTO EVIDENCE)

### 4.1 Coca-Cola Enterprises, Inc. Store

**Current State (v3):** Not present in map
**Correction Required:** **Add Coca-Cola store to Z3 (lower corridors)**
**Evidence:** PHOTO_CLASSIFICATION_TABLE_V1_COMPLETE.md
**Source Photos:** 3085977904, 3085140933
**Zone:** Z3 (lower ring corridors)

**Details:**
- Glass storefront with "Coca-Cola Enterprises, Inc." signage
- Red and white color scheme
- Store displays Coca-Cola merchandise and branded items
- Located in lower level corridor (Z=0)
- **CONFIDENCE: HIGH** (clearly visible in photos)

**Map Impact:**
- Add store entity to v5 map at Z3 corridor position
- Store type: retail/specialty merchandise
- Approximate size: standard mall inline store (~1000-1500 sq ft)

---

### 4.2 Mickey's Family Restaurant Exterior Wing

**Current State (v3):** Partial implementation
**Correction Required:** **Extend Mickey's wing with concentric arch entrance**
**Evidence:** Photo 46099761
**Source Photo:** 46099761
**Zone:** Z9 (exterior) → Z8 (anchor stores)

**Details:**
- Exterior features distinctive **concentric arch entrance**
- Multiple layered arches creating depth effect
- Restaurant entrance at exterior facade
- **CONFIDENCE: HIGH**

**Map Impact:**
- Extend Z8 anchor store footprint to include exterior wing
- Add architectural feature: concentric arch entrance
- Connects exterior (Z9) to interior restaurant space (Z8)

---

### 4.3 FOOD COURT Neon Sign

**Current State (v3):** Not documented
**Correction Required:** **Add circular neon sign above food court**
**Evidence:** MEASUREMENT_SHEET_V1.csv, entry NSF-001
**Source Photos:** 64360891, 453143417
**Zone:** Z4 (food court)

**Details:**
- Large circular neon sign reading "FOOD COURT"
- Blue neon arc surrounding red text
- Suspended above food court entrance/overlook
- Estimated diameter: **6-8 feet**
- Positioned under tensile roof, visible from upper level
- **CONFIDENCE: HIGH** (clearly visible)

**Map Impact:**
- Add signage element to food court zone
- Sign positioned at Z4 entrance viewpoint
- Landmark for navigation

---

## SECTION 5: CORRIDOR & INTERSECTION CORRECTIONS

### 5.1 Lower Corridor Widths

**Current State (v3):** Corridors approximately 12-15 feet wide
**Correction Required:** **Verify width using railing/door scaling**
**Evidence:** Multiple corridor photos with door frames and railings
**Source Photos:** Corridor photos from PHOTO_CLASSIFICATION_TABLE
**Measurement Method:** Door frame (80") as scaling reference

**Details:**
- Standard mall corridor: 12-20 feet wide
- Can be measured in photos relative to 80" door frames
- Requires photo-specific pixel analysis
- **CONFIDENCE: MEDIUM** (requires detailed photogrammetry)

**Map Impact:**
- Pending: Extract corridor widths from door-visible photos
- Update v3 corridor tile widths if measurements differ significantly

---

### 5.2 T-Junction Intersections

**Current State (v3):** Some T-junctions present
**Correction Required:** **Verify T-junction positions from photos**
**Evidence:** Corridor intersection photos
**Source Photos:** Multiple corridor photos (pending detailed review)

**Details:**
- User originally requested T-junction corrections in Section 2
- Requires matching photo locations to map positions
- **CONFIDENCE: LOW** (requires spatial triangulation)

**Map Impact:**
- Pending: Cross-reference corridor photos with existing v3 T-junctions
- Document any missing or misplaced intersections

---

## SECTION 6: HISTORICAL CONTRADICTIONS (TIMELINE VARIANCE)

These are NOT errors, but documented differences across time periods:

### 6.1 Food Court Vendor Layout Variance

**Evidence:** Photos show different vendor configurations
**Photos:** 64360891, 453143417
**Issue:** Vendor booth positions and count vary between photos
**Interpretation:** Vendor turnover over time (1995-2010 span)
**Resolution:** Document multiple configurations, do not force consistency

---

### 6.2 Tensile Roof Color Variance

**Evidence:** Photos show white vs. beige fabric
**Photos:** 453124750 (white), 64360891 (off-white/beige)
**Issue:** Fabric color appears different
**Interpretation:** Aging, replacement, or lighting conditions
**Resolution:** Document as "white tensile fabric" with note on variance

---

### 6.3 Theater Status (Open vs. Closed)

**Evidence:** Some photos show dark theater entrance, others show activity
**Photos:** Multiple theater entrance photos
**Issue:** Theater operational status varies
**Interpretation:** Business hours, closure periods, or permanent closure
**Resolution:** Map theater location but note variable operational status

---

## SECTION 7: COVERAGE GAPS (ZONES WITH INSUFFICIENT PHOTOS)

### 7.1 Zone Z7 (Subterranean Ramp/Service Deck)

**Photo Count:** 0
**Issue:** No photographic evidence of underground service access
**Resolution:** Cannot verify Z7 existence. Mark as "UNVERIFIED" in v5 map.

---

### 7.2 Zone Z6 (Theater Interior)

**Photo Count:** 1 (exterior only)
**Issue:** Theater interior not documented
**Resolution:** Map exterior entrance only. Interior marked "UNVERIFIED".

---

### 7.3 Zone Z2 (Upper Ring Corridors)

**Photo Count:** 8 (5.6% of collection)
**Issue:** Upper level under-documented compared to lower level (68 photos)
**Resolution:** Upper level geometry has LOWER confidence. Rely on Z3 measurements and symmetry assumptions.

---

## SECTION 8: MEASUREMENT SUMMARY & PRIORITY ORDER

### 8.1 Established Measurements (HIGH CONFIDENCE)

| Feature | Measurement | Source | Use Case |
|---------|-------------|--------|----------|
| Food Court Pit Depth | **8 feet** | 12 escalator steps × 8" | Z-level calibration |
| Fountain Tier Count | **4 levels** | Visual count | Fountain geometry |
| Tensile Roof Cables | **32 radial** | Cable count | Roof geometry |
| Balcony Railing Height | **42 inches** | Building code | Corridor scaling |
| Door Frame Height | **80 inches** | Building code | Corridor scaling |

---

### 8.2 Estimated Measurements (MEDIUM CONFIDENCE)

| Feature | Measurement | Source | Use Case |
|---------|-------------|--------|----------|
| Glass Block Wall Height | **14-18 feet** | 28 blocks × 6-8" | Wall dimensions |
| Glass Block Wall Arc | **22.5 feet** | 45 blocks × 6" | Wall curvature |
| Fountain Depth | **~6 feet** | 4 tiers × 18" | Fountain dimensions |
| FOOD COURT Sign Diameter | **6-8 feet** | Visual estimate | Signage scaling |

---

### 8.3 Uncertain Measurements (LOW CONFIDENCE)

| Feature | Measurement | Source | Use Case |
|---------|-------------|--------|----------|
| Truss Mast Height | **~35 feet** | Visual estimate | Atrium vertical scale |
| Atrium Diameter | **60-80 feet** | Inference from features | Atrium footprint |
| Corridor Widths | **12-20 feet** | Standard mall range | Corridor geometry |
| Column Spacing | **~20 feet** | Typical grid | Structural grid |

---

## SECTION 9: CORRECTIONS STAGED FOR V5 MAP PROPOSAL

The following corrections are **LOCKED** for inclusion in MALL_MAP_V5_PROPOSAL.json:

1. ✅ **Food court pit depth: 8 feet (Z=0 to Z=-1)** - HIGH confidence
2. ✅ **Glass block wall: 14 feet height × 22.5 feet arc** - MEDIUM confidence
3. ✅ **Fountain: 4 tiers, 6 feet total depth** - HIGH confidence
4. ✅ **Tensile roof: 4 masts, 32 radial cables** - HIGH confidence
5. ✅ **Escalators: 12 steps, bidirectional pair** - HIGH confidence
6. ✅ **Balcony railings: 42 inches** - HIGH confidence
7. ✅ **Add Coca-Cola store to Z3** - HIGH confidence
8. ✅ **Add FOOD COURT neon sign to Z4** - HIGH confidence
9. ✅ **Verify Mickey's wing with concentric arches** - HIGH confidence
10. ⏳ **Corridor widths** - PENDING photogrammetry
11. ⏳ **T-junction positions** - PENDING triangulation
12. ⏳ **Atrium diameter** - PENDING measurement synthesis

---

## NEXT STEPS

1. ✅ **Measurements extracted** (MEASUREMENT_SHEET_V1.csv complete)
2. ✅ **Corrections documented** (this file complete)
3. ⏳ **Create MALL_MAP_V5_PROPOSAL.json** using locked corrections
4. ⏳ **Decide map format:** Tile-based (like v3) or zone-based (like v4)?
5. ⏳ **Implement high-confidence corrections first**
6. ⏳ **Mark uncertain elements with confidence metadata**

---

*Document Status: COMPLETE*
*Ready for Step 7: MALL_MAP_V5_PROPOSAL.json construction*
*All corrections traceable to MEASUREMENT_SHEET_V1.csv and photo evidence*
