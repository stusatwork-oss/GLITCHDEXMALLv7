# Foodcourt 2010 — Frame Extraction

**Source:** `raw/reference-video/foodcourt_2010.mp4`
**Extracted:** 2025-11-22
**Agent:** Claude (Sonnet 4.5) via Claude Code

---

## Frame Details

- **Total frames extracted:** 40
- **Source duration:** 66.8 seconds (2002 frames @ 29.97 fps)
- **Extraction interval:** ~50 frames (~1.67 seconds)
- **Format:** PNG (lossless)
- **Naming:** `frame_0001.png` through `frame_0040.png`
- **Average file size:** ~230KB per frame

---

## Source Material Context

**Architecture:** 1986 (tensile fabric roof)
**Footage era:** 2010 (24 years after construction)
**Sampled:** 2025 (15 years after capture)

### Key Visual Characteristics:
- Tensile fabric roof diffused lighting
- Pre-smartphone era aesthetic (2010)
- Mature mall atmosphere (mid-life documentation)
- Specific temporal quality: architecture remembering its 80s origin through 2010 lens

---

## Use Cases

### VIBES Sampling
The soft, filtered daylight through tensile fabric creates signature lighting quality. These frames capture that specific atmospheric character.

### Mall-as-Character (Sora Material)
Each frame = different "expression" of the Mall across a 67-second moment. Good reference for:
- Scene composition
- Light/shadow patterns
- Spatial relationships
- Temporal breathing patterns

### Reference Stills
- Shot composition templates
- Anchor point identification
- Temporal benchmarking
- Architectural documentation

---

## Technical Notes

### Extraction Method
```python
# OpenCV-based even distribution sampling
frame_interval = total_frames / 40  # ~50 frames
# Each frame represents ~1.67s interval
```

### Frame Numbering
Frames are zero-padded for sorting:
- `frame_0001.png` = 0.00s
- `frame_0020.png` = ~33.4s (midpoint)
- `frame_0040.png` = ~66.8s (end)

---

## Integration Points

See `ai/SESSION_LOG_2025-11-22_foodcourt_frames.md` for:
- Full extraction details
- Sora integration suggestions
- Character development notes
- Next steps for analysis

---

## For Future AI Collaborators

These frames are ready for:
- Semantic classification
- Sora prompt template development
- Visual analysis and cataloging
- Comparison with other temporal footage (ERA_2020, etc.)

**Metadata manifest:** Not yet created (good next task!)

---

*The mall has eyes. These are 40 snapshots of how it was looking at the world in 2010.* 👁️🏬
