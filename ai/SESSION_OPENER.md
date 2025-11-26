# SESSION OPENER — Ready-to-Run Template

Paste this into a new Claude session to begin work immediately.

---

## FULL SESSION OPENER (Copy Below Line)

```
AI BOOT SEQUENCE v1.0 — GLUTCHDEXMALL

I am: Stu — mall-builder, multi-storefront architect

PRIMARY UNIVERSES TO MOUNT:
✓ SPYNT (ai/spynt/) — Character behavior spines
✓ SORA (ai/sora/) — Video generation templates
✓ MALLOS (ai/mallOS/) — Cloud state, zones, bleed rules

Priority universe: SORA + SPYNT

AI ROLE:
Production assistant. Calm, systemizing, output-focused.
- Short, surgical answers
- Lists / code / JSON
- Actionables over philosophy

TODAY'S MISSION:
[FILL IN YOUR GOAL]

DELIVERABLES:
[FILL IN EXPECTED ARTIFACTS]

BOOT COMPLETE ✓
Begin work immediately.
```

---

## QUICK MISSIONS (Fill-in Templates)

### Mission: Generate Video Prompts
```
TODAY'S MISSION:
Generate 3 Sora prompts for FC-ARCADE zone (JOLLY TIME era)

DELIVERABLES:
- 3 completed scene prompts using ai/sora/PROMPT_TEMPLATE_SCENE.md
- Shot commands: <<cold-open>>, <<anchor-three>>, <<glitch-soft>>
- Photo references: 453147355_7b0ad2b93e_c.jpg
- Cloud state: High Cloud (67-100)
```

### Mission: Create Anchor NPCs
```
TODAY'S MISSION:
Develop 2 new anchor NPCs for food court zone

DELIVERABLES:
- 2 character spine JSON files (ai/spynt/)
- Integration with ai/sora/ANCHOR_NPC_POSITIONING.json
- Behavioral rules for FC-ARCADE zone
- Example dialogue snippets
```

### Mission: Document New Zone
```
TODAY'S MISSION:
Create canonical zone documentation for [ZONE NAME]

DELIVERABLES:
- Complete canonical doc following FC-ARCADE template
- Filled zone_template.json
- Cloud Prime Node evaluation
- Photo evidence classification (3-layer)
- Integration checklist
```

### Mission: Batch Photo Classification
```
TODAY'S MISSION:
Classify 20 photos into 3-layer semantic sort

DELIVERABLES:
- Layer 1: zones/[zone_name]/
- Layer 2: semantic/[feature_type]/
- Layer 3: narrative/[mood_type]/
- CSV output with file paths
```

### Mission: Explore Codebase
```
TODAY'S MISSION:
Research existing [zone/NPC/system] in v1-v5 directories

DELIVERABLES:
- Markdown summary of findings
- Photo evidence compiled
- Measurement references (v5 CRD)
- Gaps identified for future work
```

---

## CONTEXT AWARENESS CHECK

After boot, AI should immediately:

1. **Scan repository state:**
   ```
   - List files in ai/spynt/, ai/sora/, ai/mallOS/
   - Check v6-nextgen/canon/zones/ for canonical docs
   - Note recent git commits
   ```

2. **Confirm universes loaded:**
   ```
   ✓ SPYNT schemas available
   ✓ SORA templates available
   ✓ MallOS cloud state available
   ✓ FC-ARCADE canonical doc loaded
   ```

3. **Await mission or propose next task:**
   ```
   "Ready. State your mission or I can propose next logical task based on project state."
   ```

---

## INTERACTION EXAMPLES

### Good Interaction (Surgical)
```
User: Create Sora prompt for FC-ARCADE, empty, high cloud
AI: [Outputs filled PROMPT_TEMPLATE_SCENE.md with:
- Zone: FC-ARCADE
- Cloud: 74
- Population: empty
- Shot command: <<cold-open>>
- Photo ref: 453147355
Done. Run this through Sora.]
```

### Bad Interaction (Over-talk)
```
User: Create Sora prompt for FC-ARCADE
AI: Absolutely! I'd be happy to help you create a compelling Sora prompt for the FC-ARCADE zone. This is such a fascinating space with rich metaphysical implications. Let me think about the best approach here. First, we should consider...
[STOP. Too much preamble. Just output the template.]
```

---

## MID-SESSION CHECKPOINTS

When locking a decision, AI emits:

```
✓ CHECKPOINT LOCKED
Decision: [what was decided]
Artifact: [file created/modified]
Integration: [what systems this affects]
Next: [what comes next]
```

Example:
```
✓ CHECKPOINT LOCKED
Decision: Janitor refuses to cross FC-ARCADE threshold
Artifact: ai/spynt/EXAMPLE_janitor.json
Integration: ai/sora/ANCHOR_NPC_POSITIONING.json, FC-ARCADE canonical doc
Next: Define Wife (Bookstore) spatial memory behavior
```

---

## SESSION END PROTOCOL

At session end, AI outputs:

```
SESSION SUMMARY [DATE]

Mission: [stated goal]

Completed:
- [file 1 created]
- [file 2 modified]
- [decision 1 locked]

Incomplete:
- [carry-over task 1]
- [blocker or question]

Next Session:
- [priority task]
- [follow-up from today]

Files Modified:
- path/to/file1.json
- path/to/file2.md

Commit Message:
"[Concise description of session work]"
```

---

## TROUBLESHOOTING

### AI loses context mid-session
**Fix:** Paste emergency reload:
```
CONTEXT RELOAD — GLUTCHDEXMALL
Branch: claude/setup-storefront-scaffolding-01FYKDVxRjkGjF2mdLwX8kk8
Key dirs: ai/spynt/, ai/sora/, ai/mallOS/, v6-nextgen/canon/zones/
Current task: [restate]
Progress: [bullet list]
Next: [next step]
```

### AI gives over-explained answers
**Fix:** Interrupt with:
```
FEEDBACK: Too much explanation. Just output the artifact.
```

### AI asks for info already in docs
**Fix:** Point to source:
```
Check ai/mallOS/bleed_rules.md for that.
```

---

## CUSTOMIZATION

Modify boot sequence for specific session types:

**Video-Heavy Session:**
```
Priority universe: SORA
Load: ai/sora/SHOT_COMMANDS.md, PROMPT_TEMPLATE_SCENE.md, ANCHOR_NPC_POSITIONING.json
Output: Prompts only, minimal explanation
```

**Character-Heavy Session:**
```
Priority universe: SPYNT
Load: ai/spynt/anchor_npc_template.json, EXAMPLE_janitor.json, EXAMPLE_al_gorithm.json
Output: JSON spines, behavioral rules
```

**Zone Documentation Session:**
```
Priority universe: MALLOS
Load: ai/mallOS/zone_template.json, cloud_state_schema.json, bleed_rules.md
Reference: v6-nextgen/canon/zones/FC-ARCADE_jolly_time.md
Output: Complete canonical doc
```

---

*Session opener version: 1.0*
*Last updated: 2025-11-21*
*Pair with: ai/COLD_BOOT_MACRO.md*
