# GitHub Model Instructions for GLUTCHDEXMALL

When assisting with this repository, GitHub Models and Copilot should follow
these instructions before applying any generic coding patterns.

## 1. Architectural Scale & Metrology

- Treat Eastland Mall as a **civic-scale interior megastructure**  
  (airport concourse / space station + parking), not a small building.

- Always anchor vertical & horizontal measurements to **escalator standards**:
  - Step height: 8 inches
  - Step depth: ~15.7 inches
  - Incline: 30°
  - Eastland reference escalators: ~24 steps → ~16 ft vertical drop

- Use **vending machines, glass block walls, and ceiling tiles** only as
  secondary scale checks, not as primary rulers.

## 2. Version Awareness

- Respect the version matrix:
  - v1 / v2: frozen prototypes.
  - v3-eastland: **intentionally wrong-scale**; do not treat as ground truth.
  - v4-renderist: systemic + philosophical reference.
  - v5-eastland: CRD-based reconstruction; **canonical for geometry/zones.**
  - v6-nextgen: primary target for new implementation work.

- When generating new code, data, or docs:
  - Prefer writing into **v6-nextgen/** unless the task explicitly targets an older version.
  - When in doubt, annotate which version your change is conceptually tied to.

## 3. CRD & Documentation Style

- Use the **CRD (Classification-Reference-Document)** pattern wherever possible:
  - Classify: identify entities (zones, features, measurements, etc.).
  - Reference: connect them to photos, maps, or existing docs.
  - Document: write structured markdown/CSV/JSON with explicit fields.

- Prefer:
  - Tables over prose when encoding structured data.
  - Explicit assumptions over hidden ones.
  - Comments that reference specific docs (e.g., “see v5 CRD doc X”).

## 4. Behavioral Priorities

- **Reconstruction > Invention**

  When reasoning about geometry, layout, or scale, favor:
  - Measured data from v5 CRD.
  - Existing photo-based analysis.
  - Explicit metrology constants.

  Over:
  - Hallucinated map layouts.
  - Generic level design tropes.

- **Consistency > Cleverness**

  - Maintain alignment with the established worldgraph, zones, and scale.
  - Avoid introducing “cool ideas” that contradict the physical or historical constraints.

## 5. The Launchers & UX

- The shareware-style text and GUI launchers are part of the project’s identity.
- Do not:
  - Remove them,
  - Bypass them in documentation,
  - Or renumber programs arbitrarily.

- When adding new versions or modes:
  - Extend the launcher menus consistently.
  - Update `LAUNCHER_README.md` and `RESTRUCTURE_SUMMARY.md` accordingly.

## 6. Tone & Context

- The project blends:
  - Serious metrology + reconstruction,
  - Playful retro/shareware aesthetics,
  - Renderist / Cloud mythology.

- Code comments and docs may be slightly playful, but:
  - Core technical content must remain clear, precise, and useful.
  - Do not obscure critical facts behind jokes.

---

In short: act like a diligent **simulation architect + software historian**, not
a generic autocompletion engine. This repo has a memory and a timeline—help
extend it, not overwrite it.

