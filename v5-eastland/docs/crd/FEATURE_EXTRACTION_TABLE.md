# FEATURE EXTRACTION TABLE - EASTLAND MALL V5

**Version:** 1.0
**Date:** 2025-11-21
**Purpose:** Catalog measurable atomic units for geometric calibration
**Methodology:** CRD v0.1 FEATURE CLASSES

---

## FEATURE CLASS DEFINITIONS

Features are measurable atomic units with known real-world dimensions.
They serve as "rulers" for calculating all other mall geometry.

---

## A. GLASS_BLOCK_FEATURE

**Dimensions:** 6×6" or 8×8" (to be measured from photos)
**Precision:** HIGHEST — Most consistent ruler in dataset
**Location Zones:** Z1 (atrium), Z4 (food court retaining walls)

### Instances

| Instance ID | Zone | Photo Ref | Position | Notes |
|-------------|------|-----------|----------|-------|
| GBF-001 | Z1 | 453127566 | Fountain rear wall | Curved wall behind fountain stage |
| GBF-002 | Z1 | 453124750 | Atrium glass wall | 2-story height visible |
| GBF-003 | Z4 | 453143417 | Food court pit wall | Retaining wall perimeter |
| GBF-004 | Z1 | 453125654 | Atrium detail | Close-up glass block pattern |

**Use Cases:**
- Atrium wall radius calculation
- Grid alignment verification
- Vertical scale (2-story height)
- Retaining wall dimensions

**Measurement Status:** PENDING photo pixel analysis

---

## B. VENDING_MACHINE_FEATURE

**Dimensions:** 39" width × 72" height (standard Coca-Cola machine)
**Precision:** HIGH — Known standard industrial size
**Location Zones:** Z3 (lower corridors, near escalators)

### Instances

| Instance ID | Zone | Photo Ref | Position | Notes |
|-------------|------|-----------|----------|-------|
| VMF-001 | Z3 | 3085977904 | Near escalators | Coca-Cola Enterprises storefront |
| VMF-002 | Z3 | 3085977656 | Interior view | Same location, different angle |

**Use Cases:**
- **PRIMARY GLOBAL SCALE ANCHOR**
- Corridor width calibration
- Pixel-to-inch ratio calculation
- All other measurements reference this

**Measurement Status:** CRITICAL — Must measure first

---

## C. EXIT_SIGN_FEATURE

**Dimensions:** 8.75" × 10.5" (standard commercial exit sign)
**Precision:** MEDIUM — Standardized but may vary
**Location Zones:** Z2, Z3 (corridors)

### Instances

| Instance ID | Zone | Photo Ref | Position | Notes |
|-------------|------|-----------|----------|-------|
| ESF-001 | TBD | TBD | Corridor exits | Pending photo review |

**Use Cases:**
- Corridor scaling verification
- Cross-check against vending machine measurements
- Height reference at standard door height

**Measurement Status:** PENDING photo identification

---

## D. ESCALATOR_STEP_FEATURE

**Dimensions:** 8" rise per step (standard escalator code)
**Precision:** VERY HIGH — Building code regulated
**Location Zones:** Z3→Z4 (escalator descent)

### Instances

| Instance ID | Zone | Photo Ref | Position | Notes |
|-------------|------|-----------|----------|-------|
| ESF-001 | Z3→Z4 | 3085976410 | Escalator upper | Step count visible |
| ESF-002 | Z3→Z4 | 3085979988 | Escalator view | Angle shows rise |
| ESF-003 | Z3→Z4 | 453147491 | Escalator area | Lighting context |

**Use Cases:**
- **Z-LEVEL HEIGHT CALIBRATION**
- Calculate exact pit depth (8' ÷ 8" = 12 steps expected)
- Verify ~8-12 step count from photos
- Food court descent geometry

**Measurement Status:** HIGH PRIORITY — Count steps in photos

**Expected Calculation:**
```
Pit Depth = (Step Count × 8 inches)
If 10 steps visible → 80 inches = 6.67 feet
If 12 steps visible → 96 inches = 8 feet ✓ (matches observations)
```

---

## E. CEILING_TILE_FEATURE

**Dimensions:** 2' × 4' (standard drop ceiling grid)
**Precision:** HIGH — Commercial standard
**Location Zones:** Z5 (anchor stores)

### Instances

| Instance ID | Zone | Photo Ref | Position | Notes |
|-------------|------|-----------|----------|-------|
| CTF-001 | Z5 | TBD | Anchor store interior | Pending photo classification |

**Use Cases:**
- Anchor store interior scale
- Room dimensions
- Ceiling height calculation

**Measurement Status:** PENDING photo review

---

## F. TERRACOTTA_SCALLOP_FEATURE

**Dimensions:** TBD (repeating pattern — measure via photo)
**Precision:** MEDIUM — Decorative element, may vary
**Location Zones:** Z2 (upper ring corridors)

### Instances

| Instance ID | Zone | Photo Ref | Position | Notes |
|-------------|------|-----------|----------|-------|
| TSF-001 | Z2 | TBD | Upper corridor trim | Semicircle repeating pattern |

**Use Cases:**
- Perimeter measurement
- Upper level corridor length
- Grid spacing estimation

**Measurement Status:** PENDING photo review

---

## G. COLUMN_FEATURE

**Dimensions:** ~18-24" diameter (estimated from photos)
**Precision:** MEDIUM — Varies by location
**Location Zones:** Z1 (atrium radial grid)

### Instances

| Instance ID | Zone | Photo Ref | Position | Notes |
|-------------|------|-----------|----------|-------|
| COL-001 | Z1 | 453124750 | Atrium | Visible near truss mast |
| COL-002 | Z1 | 64360891 | Atrium | Column grid spacing |
| COL-003 | Z1 | 453125654 | Atrium | Radial pattern |

**Use Cases:**
- Grid spacing estimation
- Radial alignment with truss masts
- Column density mapping

**Measurement Status:** PENDING — Measure against vending machine scale

---

## H. TILE_MOSAIC_FEATURE

**Dimensions:** Variable (measure individual tiles)
**Precision:** LOW-MEDIUM — Decorative, inconsistent
**Location Zones:** Z3, Z4 (floor transitions)

### Instances

| Instance ID | Zone | Photo Ref | Position | Notes |
|-------------|------|-----------|----------|-------|
| TMF-001 | Z4 | 453143417 | Food court floor | Staggered geometric pattern |
| TMF-002 | Z3 | TBD | Corridor transition | Tile→carpet boundary |

**Use Cases:**
- Zone boundary detection
- Floor pattern mapping
- Spatial orientation reference

**Measurement Status:** SECONDARY — Use after primary rulers established

---

## I. TRUSS_MAST_FEATURE

**Dimensions:** ~35' height (from special_features in v4 base)
**Precision:** HIGH — Structural element
**Location Zones:** Z1 (atrium, 4 masts at quadrants)

### Instances

| Instance ID | Zone | Photo Ref | Position | Notes |
|-------------|------|-----------|----------|-------|
| TRF-001 | Z1 | 453124750 | Northwest quadrant | Yellow painted steel |
| TRF-002 | Z1 | 453124750 | Northeast quadrant | Visible in same photo |
| TRF-003 | Z1 | 453125654 | Atrium center view | Radial cable pattern |
| TRF-004 | Z1 | 64360891 | Food court view | Mast visible from below |

**Use Cases:**
- Vertical scale reference
- Atrium height calculation
- Cable radial pattern geometry
- Quadrant alignment

**Measurement Status:** REFERENCE — 35' assumed from v4 data

---

## J. NEON_SIGN_FEATURE (FOOD COURT)

**Dimensions:** TBD (measure width/height from photo)
**Precision:** MEDIUM — Custom signage
**Location Zones:** Z4 (food court entry arch)

### Instances

| Instance ID | Zone | Photo Ref | Position | Notes |
|-------------|------|-----------|----------|-------|
| NSF-001 | Z4 | 64360891 | Food court arch | "FOOD COURT" neon sign clearly visible |

**Use Cases:**
- Food court entry span
- Arch width calculation
- Vertical clearance reference

**Measurement Status:** PENDING — Measure against escalator steps

---

## K. ARCH_CURVATURE_FEATURE (MICKEY'S)

**Dimensions:** TBD (measure radius from photo)
**Precision:** MEDIUM — Architectural element
**Location Zones:** Z6 (Mickey's entrance)

### Instances

| Instance ID | Zone | Photo Ref | Position | Notes |
|-------------|------|-----------|----------|-------|
| ACF-001 | Z6 | 46099761 | Exterior entrance | Concentric red/orange rings |

**Use Cases:**
- Mickey's wing geometry
- Arch depth calculation
- Corridor approach alignment

**Measurement Status:** PENDING — Requires exterior scale reference

---

## MEASUREMENT PRIORITY ORDER

1. **CRITICAL (Global Scale):**
   - B. Vending Machine (39" × 72") — Establishes pixel-to-inch ratio
   - D. Escalator Steps (8" rise) — Z-level height calibration

2. **HIGH (Primary Geometry):**
   - A. Glass Blocks (6×6" or 8×8") — Atrium dimensions
   - I. Truss Masts (35' height) — Vertical reference

3. **MEDIUM (Secondary Verification):**
   - G. Columns (18-24" diameter) — Grid spacing
   - J. Neon Sign — Food court dimensions
   - E. Ceiling Tiles (2'×4') — Anchor store scale

4. **LOW (Detail/Cross-check):**
   - C. Exit Signs
   - F. Terracotta Scallops
   - H. Tile Mosaics
   - K. Mickey's Arch

---

## NEXT STEPS

1. ⏳ **Measure Vending Machine** (VMF-001) in photo 3085977904
   - Count pixels (width × height)
   - Calculate: `1 pixel = (39 inches / pixel_width)`

2. ⏳ **Count Escalator Steps** (ESF-001, ESF-002) in photos 3085976410, 3085979988
   - Verify 8-12 step range
   - Calculate: `Pit Depth = steps × 8 inches`

3. ⏳ **Measure Glass Blocks** (GBF-001) in photo 453127566
   - Count blocks in known dimension
   - Determine if 6×6" or 8×8"
   - Calculate wall radius

4. ⏳ **Create stereo pairs** for depth measurement
   - Atrium: 453124750 + 453125654
   - Food court: 64360891 + 453143417
   - Escalators: 3085976410 + 3085979988

5. ⏳ **Generate MEASUREMENT_SHEET_V1.csv** with all calculated dimensions

---

*All measurements must reference back to primary scale anchors (vending machine & escalator steps)*
