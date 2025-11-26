# AI Memory – Core Facts & Constraints

This file encodes persistent facts about the GLUTCHDEXMALL project that AI
agents should treat as stable “long-term memory.”

## 1. The Mall

- The real-world reference is **Eastland Mall** in Tulsa.
- Approximate scale: **~1,000,000+ sq ft**, roughly **15–17 football fields**.
- Treated as a **civic-scale interior megastructure** (airport concourse / space
  station with a parking lot), not a simple “mall level.”
- Two primary levels, with a **sunken food court pit** and **central atrium**.

## 2. Key Structural Anchors

These are the “fixed stars” for metrology and layout:

- **Escalators**
  - Step height: **8 inches**.
  - Step depth (tread): ~**15.7 inches**.
  - Incline: **30°**.
  - Visible step count in Eastland reference photos: approx. **24**.
  - → Vertical drop: ~**16 feet** from upper level to pit.
  - → Horizontal run: ~**31–32 feet**.

- **Food Court Pit**
  - Depth anchored to escalator rise (~16 ft).
  - Forms the core of the sunken zone, surrounded by vendor bays.

- **Glass Block Walls**
  - Act as **high-precision measurement rulers** (blocks of 6" or 8").
  - Used to validate atrium heights and curved wall lengths.

- **Coca-Cola Vending Machine**
  - Standard height ~72".
  - Used as a **secondary scale check**, never primary.

## 3. Version Roles

- **v1-doofenstein**  
  Retro prototype; comedic / early gameplay experiment. Frozen.

- **v2-immersive-sim**  
  Early AI/immersive ideas. Reference only.

- **v3-eastland**  
  First Eastland pass. **Wrong ruler / wrong scale.** Kept for history; DO NOT
  base new work on its geometry.

- **v4-renderist**  
  Introduces the Cloud, Renderist theology, and higher-level world logic.

- **v5-eastland**  
  CRD (Classification-Reference-Document) reconstruction:  
  - Photo classification,  
  - Feature extraction,  
  - Zone graph,  
  - Measurement sheets,  
  - Map proposals.

  Treat this as the primary **geometric / structural truth.**

- **v6-nextgen**  
  “Next generation” implementation: where the **actual engine + gameplay** should
  converge, using v5 as ground truth.

## 4. Zoning & Worldgraph

- The mall is divided into **zones** (atrium, food court, corridors, anchors,
  under-mall service areas, etc.).
- Zone adjacency and “worldgraph” logic are defined in CRD docs under v5.
- AI should **preserve** this graph when adding or refactoring systems.

## 5. The Cloud & Renderist Frame

- The **Cloud** is the systemic layer that:
  - Observes player behavior,
  - Adjusts world responses,
  - Enforces (or toys with) constraints,
  - Resists trivial speedruns and abuse.

- **Renderist** framing:
  - Treats the world as layered realities (retro veneer over modern systems).
  - Prioritizes **discovery, inference, and self-reflection** over raw exposition.

## 6. Non-Negotiables for AI

When generating code / docs / maps:

- Do **not**:
  - Shrink the mall to “building scale.”
  - Redefine the escalator geometry arbitrarily.
  - Treat v3 as canonical.
  - Ignore v5 CRD results.

- Always:
  - Anchor scale to escalator metrology.
  - Keep the mall in the “airport concourse / space station” size class.
  - Preserve version chronology.
  - Maintain clarity between **reconstruction** and **fictional lore.**

This file should be treated as a **stable backbone** for all future AI work.

