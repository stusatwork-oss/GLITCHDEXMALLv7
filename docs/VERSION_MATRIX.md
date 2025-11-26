# Version Matrix – GLUTCHDEXMALL

This table defines the role, status, and AI usage pattern of each version in
this repository. AI tools should use this to decide **where to read from** and
**where to write to.**

| Version     | Era / Flavor          | Purpose / Focus                            | Status       | AI Usage Guidance                                         |
|-------------|-----------------------|--------------------------------------------|-------------|-----------------------------------------------------------|
| v1-doofenstein | DOS / shareware parody | Proto game; joke-y retro shooter shell     | Frozen      | Read only. Do not update. Useful for tone & history.     |
| v2-immersive-sim | Early immersive sim | AI/interaction scaffolding, early systems  | Frozen      | Read for ideas. Do not treat as up-to-date architecture. |
| v3-eastland | First Eastland attempt | Initial mall layout; wrong ruler / scale   | Corrupted   | **Do NOT** use as geometric ground truth. Historical only. |
| v4-renderist | Renderist engine phase | Cloud, Renderist theology, systemic framing| Active (lore/systems) | Read for philosophy + systemic ideas. Extend carefully. |
| v5-eastland | CRD reconstruction     | Photo-based CRD, measurement sheets, zone graphs, v5 map proposal | Canonical reference | **Primary source of structural truth. Use as geometry + metrology backbone.** |
| v6-nextgen | Next-generation build   | Future engine + game implementation based on v5 | Future / In development | Target for new code, systems, and gameplay. Tie to v5’s constraints. |

## Key Points for AI

- **Canonical Geometry & Scale:**  
  Pull from **v5-eastland** (CRD docs, measurement sheets, map proposals).

- **Philosophy & Systems (Cloud, Renderist):**  
  Pull from **v4-renderist**.

- **New Implementation Work:**  
  Write into **v6-nextgen** (under `src/`, `data/`, `docs/`).

- **Historical Context / Mistakes:**  
  v3-eastland is intentionally kept as the **“wrong ruler era.”**  
  Do not silently reintroduce its scale errors.

- **Launcher / Shareware Experience:**  
  The top-level launcher + GUI are part of the project’s identity.  
  Changes to version flow should respect the existing numbering (Program 387–392).

AI agents should always identify **which version** they are reading from and
explicitly reference it when proposing changes.

