# GLITCHDEX MALL - AI-Native Reconstruction Project

**Status:** 🏗️ Active Development - AI-Native Cohort (GitHub)
**Canonical Version:** **v6-nextgen/**
**Philosophy:** Reconstruction > Hallucination | Canon Emerges from Evidence

---

## 🎯 Quick Start

### For New Contributors / AI Agents

**Read these first (in order):**
1. [`.github/model-instructions.md`](.github/model-instructions.md) - AI agent guidelines
2. [`docs/AI_INTENT.md`](docs/AI_INTENT.md) - Project philosophy
3. [`v6-nextgen/README.md`](v6-nextgen/README.md) - **Canonical entry point**

### For Players

**Launch the shareware collection:**
```bash
./LAUNCH_GUI.sh   # Mid-90s GUI launcher (mouse + keyboard)
# OR
./LAUNCH.sh       # Classic text launcher (keyboard only)
```

Playable versions are in `/archive/`:
- **v3-eastland**: Full graphical game (Pygame)
- **v4-renderist**: Cloud simulation demo

---

## 📁 Repository Structure

```
GLUTCHDEXMALL/
│
├── v6-nextgen/              ⭐ CANONICAL - Primary development target
│   ├── README.md            # Start here for v6 work
│   ├── canon/               # Authoritative entity definitions
│   ├── docs/                # Documentation
│   ├── src/                 # Source code (white box skeleton)
│   ├── data/                # Game data
│   └── assets/              # Photos, maps, media
│
├── ai/                      🤖 AI-Native Tooling
│   ├── spynt/               # Character spine schemas
│   ├── sora/                # Video generation templates
│   ├── mallOS/              # Simulation state management
│   ├── renderist/           # Lore and metaphysics
│   ├── pipelines/           # Automation scripts
│   └── models/              # ML artifacts (future)
│
├── archive/                 📚 Historical Context (v1-v5)
│   ├── v1-doofenstein/      # Original Wolf3D-style game
│   ├── v2-immersive-sim/    # Advanced AI architecture
│   ├── v3-eastland/         # Pygame graphical engine
│   ├── v4-renderist/        # Cloud-driven world
│   ├── v5-eastland/         # CRD reconstruction docs
│   └── misc_unused_assets/  # Legacy files
│
├── docs/                    📖 Project Documentation
│   ├── AI_INTENT.md         # AI philosophy
│   ├── AI_MEMORY.md         # Project memory/context
│   ├── AI_FILES_SUMMARY.md  # File reference guide
│   └── VERSION_MATRIX.md    # Version comparison
│
├── .github/
│   └── model-instructions.md  # AI agent behavior guidelines
│
├── launcher_gui.py          # GUI launcher (Windows 95 style)
├── shareware_gen_v2.py      # Program generator
├── LAUNCH_GUI.sh / LAUNCH.sh  # Quick launch scripts
│
├── VERSION_GUIDE.md         # Detailed version history
├── LAUNCHER_README.md       # Launcher documentation
└── README.md                # This file
```

---

## 🎮 What is GLUTCHDEXMALL?

An AI-native, multi-era simulation of **Eastland Mall** (Tulsa, OK, 1981-2011), treated as a **civic-scale interior megastructure**, not a simple game level.

### Key Concepts

**Civic-Scale Architecture**
- ~1,000,000+ sq ft total footprint (~15-17 football fields)
- Tensile sail roof with masts reaching 60-80+ feet
- Atrium diameter: 150-200+ feet (space station scale, not building scale)
- Two-level structure with sunken food court

**Multi-Era Timeline**
- **1981**: Opening year - optimistic, tensile roof new
- **1995**: Peak era - fully occupied, bustling
- **2005**: Decline period - vacancies, atmosphere shift
- **2011**: Closure year - abandonment, memory

**All eras are canon.** Contradictions reveal layers.

**Cloud-Driven Reality**
- Global Cloud pressure (0-100)
- Four moods: tension, wander, surge, bleed
- Reality shifts based on NPC contradictions
- 60fps simulation, Cloud tick every 10 frames

---

## 🏗️ Development Status

### V6-NextGen (Canonical Target)
**Status:** White box - clean slate for AI-assisted rebuild

**What exists:**
- Directory skeleton (canon/, docs/, src/, data/, assets/)
- Comprehensive READMEs
- Entry point placeholder (`src/main.py`)

**What's next:**
- Canon entity definitions (characters, zones, items)
- MallOS simulation engine implementation
- NPC AI system
- Multi-era timeline switching
- Video generation integration

### Archive (v1-v5)
**Status:** Frozen - reference only, do not modify

Historical versions preserved for:
- Architecture patterns (v2 AI, v4 Cloud)
- Metrology foundation (v5 CRD measurements)
- Gameplay reference (v1, v3)
- Evolution context

---

## 🤖 AI-Native Development

GLUTCHDEXMALL is part of GitHub's AI-Native Development Cohort.

### For AI Agents

**Before generating code:**
1. Read `.github/model-instructions.md` (non-negotiable)
2. Check `docs/AI_INTENT.md` for philosophical constraints
3. Reference `archive/v5-eastland/` for scale/measurements
4. Use schemas from `/ai/` (spynt, mallOS, renderist)

**Key principles:**
- **Reconstruction > Hallucination** - base on photo evidence
- **Metrology first** - escalator = 8" step height, 30° incline
- **Civic scale** - airport concourse interior, not small building
- **CRD workflow** - classify, reference, document before implementing

### For Human Developers

When building in v6:
- All new work goes in `v6-nextgen/`
- Use `/archive/` for context only (don't modify)
- Validate against `/ai/` schemas
- Follow CRD methodology (v5 patterns)
- Reference `archive/v5-eastland/README_ARCHITECTURAL_CONTEXT.md` for scale

---

## 📚 Key Documents

### Essential Reading
- [`v6-nextgen/README.md`](v6-nextgen/README.md) - **Start here for v6 development**
- [`.github/model-instructions.md`](.github/model-instructions.md) - AI agent rules
- [`docs/AI_INTENT.md`](docs/AI_INTENT.md) - Project philosophy
- [`archive/v5-eastland/README_ARCHITECTURAL_CONTEXT.md`](archive/v5-eastland/README_ARCHITECTURAL_CONTEXT.md) - **Critical scale warnings**

### Reference Materials
- [`VERSION_GUIDE.md`](VERSION_GUIDE.md) - Version history and comparison
- [`LAUNCHER_README.md`](LAUNCHER_README.md) - How to use launchers
- [`docs/VERSION_MATRIX.md`](docs/VERSION_MATRIX.md) - Version feature matrix
- [`ai/README.md`](ai/README.md) - AI tooling overview

### Technical Specs
- [`archive/v5-eastland/docs/crd/`](archive/v5-eastland/docs/crd/) - CRD workflow documents
- [`archive/v4-renderist/README.md`](archive/v4-renderist/README.md) - Cloud architecture
- [`archive/v2-immersive-sim/README.md`](archive/v2-immersive-sim/README.md) - AI systems reference

---

## 🚀 Getting Started

### Play Existing Versions

```bash
# Launch GUI (recommended)
./LAUNCH_GUI.sh

# Or launch text-based
./LAUNCH.sh

# Or directly run a version
cd archive/v3-eastland && python src/main_pygame.py
cd archive/v4-renderist && python src/main.py
```

### Develop on V6

```bash
# 1. Read the canonical README
cat v6-nextgen/README.md

# 2. Review AI guidelines
cat .github/model-instructions.md

# 3. Check scale context
cat archive/v5-eastland/README_ARCHITECTURAL_CONTEXT.md

# 4. Explore AI tooling
ls -R ai/

# 5. Start building!
cd v6-nextgen/src/
```

### Run Validation

```bash
# (Future) Validate schemas
python ai/pipelines/validation/validate_all.py

# (Future) Process photos
python ai/pipelines/photo_processing/batch_classify.py
```

---

## 🎯 Project Goals

1. **Accurate Reconstruction**
   - Use CRD methodology to measure and document Eastland Mall from photos
   - Maintain civic-scale architecture (no shrinking!)
   - Multi-era timeline with full contradictions preserved

2. **AI-Native Implementation**
   - Structured schemas for all entities (characters, zones, items)
   - Automated pipelines for photo classification and validation
   - Integration with video generation (Sora/Runway)

3. **Playable Experience**
   - Cloud-driven simulation with reality shifts
   - NPC AI with memory and contradictions
   - Multi-era exploration (switch between 1981/1995/2005/2011)

4. **Historical Preservation**
   - Document mall architecture and culture
   - Honor original KKT design (tensile roof pioneers)
   - Archive community memories

---

## 🤝 Contributing

**For contributors:**
1. Work in `v6-nextgen/` (never modify `/archive/`)
2. Follow CRD workflow (classify, reference, document)
3. Validate measurements (escalator standards, civic scale)
4. Reference photos from `v6-nextgen/assets/photos/`
5. Check AI guidelines before committing

**For AI agents:**
1. **Always** read `.github/model-instructions.md` first
2. Respect version chronology (v1-v5 are historical)
3. Build in v6, reference archive for context
4. Validate against metrology constraints
5. Mark assumptions explicitly

---

## 📜 Credits

**Architecture:** KKT Architects (original Eastland Mall design, 1981)
**Photos:** Community archives, historical documentation
**Code:** Open source, AI-assisted development
**Project:** AI-native reconstruction of civic-scale architecture

**Special thanks:**
- Historical Tulsa archivists
- Mall culture preservationists
- AI-native development community

---

## 🔗 Quick Links

- **Canonical Version:** [`v6-nextgen/`](v6-nextgen/) ⭐
- **AI Tooling:** [`ai/`](ai/)
- **Archive:** [`archive/`](archive/) (v1-v5)
- **Documentation:** [`docs/`](docs/)
- **Launchers:** [`LAUNCH_GUI.sh`](LAUNCH_GUI.sh) | [`LAUNCH.sh`](LAUNCH.sh)

---

## 📞 Status & Contact

**Status:** Active development - AI-native cohort (GitHub)
**Version:** 6.0-dev (white box)
**Last Updated:** 2025-11-21

---

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  "V6 is the future. Everything else is archaeology."          ║
║  "Canon emerges from resonance and repetition, not ego."      ║
║  "Reconstruction > Hallucination"                             ║
║  "Space station with a parking lot, not a building."          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

**Read [v6-nextgen/README.md](v6-nextgen/README.md) to begin.**
