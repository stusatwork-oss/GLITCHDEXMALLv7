# AI Directory - GLUTCHDEXMALL

This directory contains all AI-facing tools, schemas, and integration logic for AI-native development.

---

## Directory Structure

### `spynt/`
**JSON spines, character schemas, NPC definitions**

Character spines define NPC identities, memories, contradictions, and behavioral patterns. These are the fundamental identity documents that AI systems use to understand character consistency.

---

### `sora/`
**Prompt templates, anchor sets, shot logic for video generation**

Templates and logic for generating video content via Sora or similar systems. Includes:
- Scene composition rules
- Anchor NPC placement logic
- Shot transition specifications
- Bleed event triggers

---

### `mallOS/`
**Cloud state, bleed rules, zones, simulation orchestration**

The MallOS orchestration layer that manages:
- Cloud pressure/mood/bleed tiers (v4 architecture)
- Zone definitions and relationships
- Simulation tick logic
- NPC swarm behavior

---

### `renderist/`
**Codex fragments, metaphysics, lore documentation**

Renderist mythology and metaphysical framework:
- Canon emergence principles
- Reality/contradiction mechanics
- Architectural philosophy
- Story fragments

---

### `pipelines/`
**GitHub Actions, Collab notebooks, automation scripts**

CI/CD and collaboration tooling:
- Automated testing
- Photo classification pipelines
- CRD batch processing
- Integration scripts

---

### `models/`
**Embeddings, semantic maps, ML artifacts (future)**

Machine learning artifacts for advanced AI features:
- Zone embeddings
- Character similarity maps
- Semantic search indices
- Training data (future)

---

## AI-Native Development Principles

1. **Structured Data > Prose**: Prefer JSON/CSV schemas over markdown descriptions
2. **Explicit References**: Link to photo evidence, CRD docs, measurement sheets
3. **Version Awareness**: Tag which version (v4, v5, v6) each artifact targets
4. **Metrology First**: Anchor measurements to escalators, not vibes
5. **Reconstruction > Hallucination**: Base on evidence, mark proxies explicitly

---

## Integration Points

- **v6-nextgen/src/**: Consumes schemas from `spynt/`, `mallOS/`, `renderist/`
- **v6-nextgen/canon/**: Defines authoritative entities that AI tools reference
- **.github/model-instructions.md**: Governs AI agent behavior across repo
- **docs/AI_INTENT.md**: High-level AI philosophy for this project

---

*This directory is the interface between human reconstruction work and AI simulation/generation systems.*
