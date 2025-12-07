# Ren'Py Host Validation Snapshot (v8-nextgen)

This report captures the current runtime behaviors and loader rules directly from the codebase after the Ren'Py migration pass. It focuses on the multi-layer voxel grid, PNG-to-voxel loader expectations, and the no-sprite fallback path that keeps validation unblocked.

**Remember:** run-time builds/tests should not be started without explicit approval; use this document to plan and review before executing anything interactive.

## Runtime Surface (No Sprites, Control Map)
- The `VisualRuntime` entrypoint boots a 1280x800 window at 60 FPS, wires the Ninja game mode, and maps arrow keys/F1/F2/space/1-4 for movement, level loading, and construct placement.
- Rendering relies on primitive `pygame` rects/circles instead of external sprites, so validation covers logic without needing Pillow assets.

### Narrative Hooks & Signposts
- The bowl layout (neon sign anchor on the south rim, glass wall along the north edge, escalator runs at the pit) is intentionally “story-ready.” Use these anchors as Ren'Py scene beats without changing loader constraints.
- Keep dialog and cut-scene overlays lightweight so they do not obscure FPS/debug overlays or pit/rim depth cues during validation.
- If you annotate the run with tester notes, drop markers near these anchors (e.g., “Neon Signpost,” “Glass Wall,” “Pit Escalator”) so cross-team reviewers can align observations with spatial context.

## Multi-Layer Voxel Geometry
- `NinjaGrid` builds a 40x40 tile map at 100 ft scale with explicit `z_level` layering for the pit (-1) versus rim (0), establishing the multi-layer voxel encoding baseline.
- Feature anchors are baked in for neon signage, glass wall segments, and escalator runs so Ren'Py scenes can preserve their placement.

## Loader Rules (PNG → Voxel Mesh)
- Palette keys are normalized for case-insensitive lookups, and PNG decoding only accepts 8-bit RGBA images that use filter type 0; other filters are rejected.
- Heightmap conversion skips fully transparent pixels, maps remaining colors through the palette, and emits columnar voxel bounds tagged with zone/material metadata.

## Asset Seeding (Sprite-Free Safety Nets)
- Tiny base64 PNGs are auto-written into `assets/voxel_sources` so loader discovery always finds source images even when the toolkit lacks system sprite packs.

## Post-Run Ren'Py Host Questionnaire (Respect Loader Rules)
Use these questions immediately after a Ren'Py-hosted validation run to capture regression details without violating the PNG loader rules (8-bit RGBA, filter type 0, case-insensitive palettes):

1. **Control Map Parity** – Inside Ren'Py, did arrows/space/1–4/F1/F2/ESC behave exactly like the Python loop, or were any keys dead, double-bound, or mapped differently?
2. **Multi-Layer Voxel Bowl Behavior** – Did the rim (`z_level = 0`) versus pit (`z_level = -1`) separation affect movement/LOS/light as expected, or did actors/rays/constructs ignore depth (floating/clipping/shadow errors)?
3. **PNG → Voxel Loader Conformance** – Were all accepted meshes sourced from 8-bit RGBA PNGs using filter type 0 with case-insensitive palette lookups, and did out-of-spec PNGs get rejected with clear warnings rather than silently loading?
4. **Seeded Voxel Sources vs Missing Sprites** – Were the auto-seeded rectangle-only voxel sources sufficient for Ren'Py UI understanding, or do testers now require higher-fidelity sprite packs before the next cycle?
5. **Warning Surfacing & Narrative Flow** – How did loader warnings (missing level JSONs, palette mismatches, rejected filters) present in Ren'Py: log-only, unobtrusive overlay, or blocking dialog? Did they respect loader rules while letting the narrative continue, or did they interrupt story flow?

## Validation Checklist (Code-Grounded)
1. Set `PYTHONPATH=$PWD:$PWD/src` and launch `NEW-needs_integration/Visual_Runtime_Entry.py`; expect the HUD/camera loop to tick at 60 FPS with construct placement via spacebar.
2. During runtime, confirm pit/rim depth separation by checking `z_level` output when tracing light/line-of-sight across the bowl radius.
3. Run `VoxelObjectLoader` against a palette/heightmap pair that uses PNG filter type 0 to ensure mesh export succeeds; other filters should be treated as errors.
4. Verify seeded voxel source images exist under `assets/voxel_sources` and that rectangular rendering appears in lieu of missing sprite sheets.
5. If integrating with Ren'Py, mirror the same control map and loader assumptions to keep parity with the Python loop before layering in visual novel UI.
