# ZONE GRAPH V1 - EASTLAND MALL

**Version:** 1.0
**Date:** 2025-11-21
**Purpose:** Clean spatial logic graph using CRD class hierarchy
**Base:** v4 adjacency model + photographic evidence

---

## ZONE HIERARCHY

### Level 0: STRUCTURAL ZONES (Physical Architecture)

These are the major architectural divisions of the mall:

```
Z1 — CENTRAL_ATRIUM
Z2 — UPPER_RING_CORRIDORS
Z3 — LOWER_RING_CORRIDORS
Z4 — FOOD_COURT_BOWL
Z5 — ANCHOR_STORE_ZONES
Z6 — MICKEYS_WING
Z7 — SUBTERRANEAN_ACCESS_DECK
Z8 — THEATER_ZONE
Z9 — EXTERIOR_ENVELOPE
```

---

### Level 1: ZONE DEFINITIONS

#### Z1 — CENTRAL_ATRIUM

**Bounds:**
- North: Glass block wall (behind fountain stage)
- South: Food court overlook railing
- East: Column grid perimeter
- West: Column grid perimeter

**Contains:**
- Terraced amphitheater fountain
- Glass block wall (curved, 2-story)
- 4 truss masts (35' height)
- White tensile roof canopy
- Radial column grid
- Glass elevator tower

**Adjacent to:** Z2 (upper ring), Z3 (lower ring), Z4 (food court via escalators)

**Z-levels:** 0 (ground), partial -1 (fountain basin lower tier)

**Features:**
- `GLASS_BLOCK_FEATURE` (6×6" or 8×8" blocks)
- `TRUSS_MAST_FEATURE` (4 yellow steel towers)
- `FOUNTAIN_TIER_FEATURE` (4-tier amphitheater)
- `COLUMN_FEATURE` (radial grid, 18-24" diameter)

**Photo refs:** 453124750, 453127566, 64360891, 453125654

---

#### Z2 — UPPER_RING_CORRIDORS

**Bounds:**
- Wraps around Z1 (atrium perimeter)
- Connects to anchor stores
- Contains scallop trim detail

**Contains:**
- Blue/green metal railings
- Terracotta scalloped trim
- Storefronts with closed grates
- T-junction intersections

**Adjacent to:** Z1 (atrium), Z5 (anchor stores), Z3 (stairwells/ramps)

**Z-level:** 0 (ground floor)

**Features:**
- `TERRACOTTA_SCALLOP_FEATURE` (repeating semicircle trim)
- `EXIT_SIGN_FEATURE` (8.75" × 10.5")
- `RAILING_FEATURE` (blue/green painted metal)

**Photo refs:** TBD (pending classification)

---

#### Z3 — LOWER_RING_CORRIDORS

**Bounds:**
- Ground-level circulation around atrium
- Connects to Z1, Z4, Z5

**Contains:**
- Tile → carpet transitions
- Kiosk sites
- Coca-Cola vending machine (SCALE ANCHOR)
- Service hall access points
- Mickey's wing corridor (southeast)

**Adjacent to:** Z1 (atrium), Z4 (food court escalators), Z6 (Mickey's), Z5 (anchor stores)

**Z-level:** 0 (ground floor)

**Features:**
- `VENDING_MACHINE_FEATURE` (39" × 72" — PRIMARY SCALE RULER)
- `TILE_MOSAIC_FEATURE` (floor pattern transitions)
- `CORRIDOR_WIDTH_FEATURE` (measured via vending machine)

**Photo refs:** TBD (pending classification)

**Critical Store:**
- Coca-Cola Enterprises, Inc. (near escalator entrance) — Photo: 3085977904

---

#### Z4 — FOOD_COURT_BOWL

**Bounds:**
- Sunken level ~8 feet below ground
- Accessed via escalators from Z3
- Amphitheater-style stepped edges

**Contains:**
- Neon FOOD COURT sign arch
- Vendor bays (asymmetric arrangement)
- Secondary decorative fountain pit
- Staggered tile geometry
- Glass block retaining walls
- Multi-tier stepped basin

**Adjacent to:** Z3 (escalators), Z8 (theater entrance), Z1 (atrium visual connection)

**Z-level:** -1 (8' pit depth)

**Features:**
- `ESCALATOR_STEP_FEATURE` (8" rise — Z-LEVEL CALIBRATION)
- `GLASS_BLOCK_FEATURE` (retaining walls)
- `TILE_MOSAIC_FEATURE` (staggered geometric pattern)
- `NEON_SIGN_FEATURE` (FOOD COURT arch)

**Photo refs:** 64360891, 453143417, 46100233

**Vendors:**
1. Slush Puppy Paradise (operational)
2. Wok This Way (closed)
3. Pizza Planet Express (closed)
4. Pretzel Hut (never opened — "NOW CLOSED" taped over "COMING SOON")
5. Burger Bunker (closed)
6. Taco Tiempo (closed)

---

#### Z5 — ANCHOR_STORE_ZONES

**Stores:**
- West Anchor (Mervyn's or similar)
- East Anchor (Dillard's)
- Southeast: Mickey's Family Restaurant (separate wing)

**Bounds:**
- Large rectangular masses off corridor rings
- Deep floor plates (2×4 ceiling grid)

**Contains:**
- Exposed ceiling grids
- Mannequin displays
- Clearance fixtures
- Service access corridors

**Adjacent to:** Z2 (upper corridors), Z3 (lower corridors), Z7 (service access)

**Z-level:** 0 (ground) + partial upper floors

**Features:**
- `CEILING_TILE_FEATURE` (2' × 4' drop ceiling — INTERIOR SCALE)
- `COLUMN_FEATURE` (structural grid spacing)

**Photo refs:** TBD (pending classification)

---

#### Z6 — MICKEYS_WING

**Bounds:**
- Southeast exterior wing
- Shallow corridor approach
- Concentric arch entrance

**Contains:**
- Domed archway (concentric red/orange rings)
- Tile color transition corridor
- Vestibule with glass doors
- Dining area interior
- Exterior parking access

**Adjacent to:** Z3 (southeast corridor junction), Z9 (exterior)

**Z-level:** 0 (ground)

**Features:**
- `ARCH_CURVATURE_FEATURE` (concentric rings — geometric reference)
- `TILE_COLOR_TRANSITION` (corridor boundary marker)
- `GLASS_DOOR_FEATURE` (vestibule to exterior)

**Photo refs:** 46099761 (exterior arch)

---

#### Z7 — SUBTERRANEAN_ACCESS_DECK

**Status:** UNKNOWN (no photos in collection)

**Hypothetical Bounds:**
- Below Z5 (anchor stores)
- Service ramp access
- Loading bays

**Contains (if exists):**
- Vehicle ramp
- Truck loading doors
- Employee infrastructure

**Adjacent to (hypothetical):** Z5 (anchor service elevators), Z9 (exterior ramp)

**Z-level:** -2 (hypothetical)

**Features:** UNKNOWN — requires verification

---

#### Z8 — THEATER_ZONE

**Bounds:**
- 6-Plex theater at food court edge
- Shallow depth from food court rail

**Contains:**
- Box office (protrudes into corridor)
- Velvet rope queue area
- Theater lobby
- Screen 1 (operational in photos)
- Screens 2-6 (dark, unused)
- Marquee (flickering)

**Adjacent to:** Z4 (food court), Z3 (corridor access)

**Z-level:** -1 (same as food court)

**Features:**
- `MARQUEE_FEATURE` (entrance signage)
- `VELVET_ROPE_FEATURE` (queue spatial logic)

**Photo refs:** 64360768 (map context), 46625814 (theater area)

---

#### Z9 — EXTERIOR_ENVELOPE

**Bounds:**
- Parking lot perimeter
- Building façade
- HVAC stack (north side)
- Entrance canopies

**Contains:**
- West entrance canopy
- East entrance canopy
- Mickey's arch (southeast)
- HVAC cylinder ("nuclear reactor" appearance)
- Ring road
- Parking striping

**Adjacent to:** All interior zones via entrance points, Z6 (Mickey's exterior)

**Z-level:** 0 (parking lot grade)

**Features:**
- `HVAC_STACK_FEATURE` (vertical shaft — north anchor)
- `ENTRANCE_CANOPY_FEATURE` (scale reference)
- `PARKING_STRIPE_FEATURE` (world alignment to satellite)

**Photo refs:** 46099761 (Mickey's exterior), TBD (parking/facade shots)

---

## ADJACENCY MATRIX

| Zone | Adjacent Zones | Connection Type |
|------|---------------|-----------------|
| Z1 | Z2, Z3, Z4 | Open visual/physical |
| Z2 | Z1, Z3, Z5 | Corridor ring |
| Z3 | Z1, Z2, Z4, Z5, Z6, Z9 | Circulation spine |
| Z4 | Z1, Z3, Z8 | Escalator descent + visual |
| Z5 | Z2, Z3, Z7 | Anchor store access |
| Z6 | Z3, Z9 | Mickey's corridor |
| Z7 | Z5, Z9 | Service ramp (hypothetical) |
| Z8 | Z4, Z3 | Theater entrance |
| Z9 | Z3, Z6, Z7 | Exterior envelope |

---

## ZONE CLASS MAPPINGS

### PRIMARY CLASSES → ZONES

| Primary Class (CRD) | Zone(s) | Notes |
|---------------------|---------|-------|
| ATRIUM_CLASS | Z1 | Central atrium only |
| ESCALATOR_CLASS | Z3 → Z4 | Connection geometry |
| FOUNTAIN_TIER_CLASS | Z1 | Fountain within atrium |
| TRUSS_TENT_CLASS | Z1 | Tensile roof over atrium |
| CORRIDOR_UPPER_CLASS | Z2 | Upper ring |
| CORRIDOR_LOWER_CLASS | Z3 | Lower ring |
| FOODCOURT_CLASS | Z4 | Sunken bowl |
| ANCHOR_STORE_CLASS | Z5 | Anchor stores |
| SERVICE_ACCESS_CLASS | Z7 | Subterranean (if exists) |
| SUBTERRANEAN_RAMP_CLASS | Z7 | Same as above |
| HVAC_STACK_CLASS | Z9 | Exterior feature |
| EXTERIOR_FACADE_CLASS | Z9 | Building envelope |

---

## FEATURE ANCHOR POINTS

### Measurable Features by Zone

**Z1 (Atrium):**
- Glass blocks (6×6" or 8×8") — Wall radius calculation
- Truss masts (35' height) — Vertical scale
- Columns (18-24" diameter) — Grid spacing

**Z3 (Lower Corridors):**
- **Coca-Cola vending machine (39" × 72")** — **GLOBAL SCALE ANCHOR**
- Exit signs (8.75" × 10.5") — Corridor width verification

**Z4 (Food Court):**
- Escalator steps (8" rise each) — **Z-LEVEL HEIGHT CALIBRATION**
- Neon sign (width TBD) — Spatial reference

**Z5 (Anchor Stores):**
- Ceiling tiles (2' × 4') — Interior dimensions

**Z6 (Mickey's):**
- Arch curvature (radius TBD via photo measurement)

---

## CONTRADICTION ZONES

Zones where photo evidence shows variance over time:

| Zone | Contradiction Type | Notes |
|------|-------------------|-------|
| Z4 | Vendor layout changed | Asymmetric vs. symmetric arrangements |
| Z1 | Tensile fabric replacement | White vs. aged yellowing |
| Z3 | Corridor width drift | Expansion/contraction over renovations |
| Z8 | Theater operation status | Screens 1 active, 2-6 dark (timeline?) |

---

## NEXT STEPS

1. ✅ Zone graph structure defined
2. ⏳ Map feature anchors to specific photo measurements
3. ⏳ Create stereo pairs per zone for depth calculation
4. ⏳ Extract precise measurements using feature rulers
5. ⏳ Document contradictions as separate timeline layers
6. ⏳ Synthesize into MEASUREMENT_SHEET_V1.csv

---

*This graph provides the spatial logic foundation before geometric measurements.*
