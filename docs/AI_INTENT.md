# AI Intent for GLUTCHDEXMALL

This repository is an AI-native, multi-era simulation of a dead regional mall
(Eastland Mall) treated as a civic-scale megastructure, not a “simple game level.”

All AI agents (GitHub Models, Copilot, external LLMs) should treat this repo as:

- A **historical timeline** of engines and ideas (v1–v6)
- A **civic architecture reconstruction** project (not just a tileset or map)
- A **technical artifact** for metrology, zoning, and worldgraph design
- A **story spine** for Renderist / Cloud / Mall-as-space-station mythology

## Core Intent

AI working in this repo should:

1. **Honor Version Chronology**

   - v1–v2 are early experiments / prototypes.
   - v3-eastland is intentionally corrupted / wrong-scale.
   - v4-renderist introduces the Cloud + Renderist worldview.
   - v5-eastland contains CRD reconstruction, zoning, and measurements.
   - v6-nextgen is the future canonical implementation.

   Do **not** “fix” v3; treat it as a historical failure and reference point.

2. **Maintain Civic-Scale Architecture**

   Eastland Mall is:

   - A **civic-scale interior** (airport concourse / space-station-with-parking-lot),
   - Approximately **1M+ sq ft**, on the order of ~15–17 football fields,
   - Two-level, with a **sunken food court** and atrium.

   Do **not** shrink the geometry to “building” or “Bradbury Building” scale.

3. **Use Metrology Correctly**

   When reasoning about size and layout:

   - Use **escalator standards** as primary calibration (see `MEASUREMENT_SHEET` in v5).
   - Use civic corridor widths, atrium heights, and anchor footprints.
   - Use the **Coca-Cola vending machine**, glass block walls, and ceiling tiles
     only as *secondary* checks against the escalator anchor.

4. **Follow CRD Workflow**

   When proposing changes, new systems, or new code:

   - Classify → Reference → Document before implementing.
   - Prefer structured tables / CSVs / JSON specs over ad-hoc comments.
   - Keep new features tied to zones, features, and measurements defined in v5/v6.

5. **Prefer Reconstruction Over Hallucination**

   - Base geometry and layout on photo evidence + CRD docs.
   - When inventing content (stores, NPCs, events), keep it **lore-consistent**
     but never contradict the physical constraints established by v5/v6.
   - If information is missing, mark it explicitly as “proxy” or “fictionalized.”

6. **Respect the Shareware Loader Canon**

   The mid-90s style shareware launcher is not a toy; it encodes:

   - The **era** of each version,
   - The **structure** of the project’s evolution,
   - The **intended UX** for exploring versions.

   Do not bypass or ignore it when adding or referencing versions.

---

In short: AI in this repo should behave like a **careful reconstruction architect + software historian**, not a “quick code helper.” The goal is long-lived coherence, not one-off hacks.

