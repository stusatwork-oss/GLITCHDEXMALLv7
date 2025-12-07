# Law System Workflow: From Consensus to Interpretation

## The Three-Layer System

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: IMMUTABLE TRUTHS (QBIT + Political Power)    │
│  • QBIT snapshot at enactment                          │
│  • Political power calculation (consensus)             │
│  • Law text and weights                                │
│  • Stored in: constitution_log.jsonl                   │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LAYER 2: CONSTRAINTS (Math, not politics)             │
│  • law_strength = f(political_power)                   │
│  • interpretation_radius = 1/(1 + strength)            │
│  • Enforcement parameters                              │
│  • Calculated from Layer 1, never negotiated           │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  LAYER 3: GOVERNOR INTERPRETATIONS (Within wiggle room)│
│  • Specific enforcement decisions                      │
│  • Edge case rulings                                   │
│  • Creative applications                               │
│  • Stored in: Jupyter notebook cells                   │
└─────────────────────────────────────────────────────────┘
```

## Workflow

### Step 1: Law Proposed
```python
food_court_curfew = Law(
    law_id="LC_0231",
    title="Food Court Curfew",
    qbit_weights={
        "heat": -0.4,      # What the law wants
        "debt": -0.1,
        "coherence": 0.3,
        "gravity": 0.2
    },
    effects={
        "npc_density_max": 0.35,
        "allowed_classes": ["JANITOR", "SECURITY"]
    }
)
```

### Step 2: Consensus Calculated (IMMUTABLE)
```python
# Query existing QBIT system (your math, untouched)
actors = get_current_political_actors()

# Calculate political power via consensus
political_power, breakdown = law_sys.evaluate_law(food_court_curfew, actors)

# Result: political_power = 0.67 (strong support)
```

**This is IMMUTABLE TRUTH:**
- At this timestamp
- With this QBIT state
- These actors voted this way
- Political power = 0.67

**No negotiation. No interpretation. Pure math.**

### Step 3: Law Enacted → Logged to Filing Cabinet
```python
law_sys.enact(food_court_curfew, political_power, breakdown)

# Writes to constitution_log.jsonl:
{
    "law": {...},
    "political_power": 0.67,
    "power_breakdown": {...},
    "qbit_snapshot": {...},  # World state at enactment
    "timestamp": "2025-12-07T19:00:00",
    "strength": 0.67,               # Calculated, not decided
    "interpretation_radius": 0.60   # Calculated, not decided
}
```

**Filing Cabinet Entry Created (IMMUTABLE)**

### Step 4: Governor Interprets (MUTABLE, WITHIN CONSTRAINTS)

The governor opens the Jupyter notebook (filing cabinet) and adds interpretation:

```python
# In constitutional_bible.ipynb

# Load the immutable truth
law = load_law("LC_0231")
print(f"Interpretation radius: {law['interpretation_radius']}")  # 0.60

# Governor's ruling (within 0.60 wiggle room)
```

**New Jupyter Cell: Governor's Interpretation**
```python
"""
GOVERNOR'S INTERPRETATION: Food Court Curfew LC_0231
Date: 2025-12-07
Interpretation Radius: 0.60 (moderate flexibility)

EDGE CASE: What if a customer is still eating at 10:01pm?

RULING (within wiggle room):
The law says "after hours only maintenance and security."
But interpretation_radius = 0.60 allows creative application.

I interpret "security" to include:
- Active security personnel (strict reading)
- Persons under security escort (flexible reading)

Therefore: Customer finishing meal at 10:01pm is ALLOWED if:
1. Security is present
2. Customer is actively eating (not loitering)
3. Customer exits within 15 minutes

This interpretation uses 0.4 of the 0.60 available wiggle room.

IMMUTABLE ANCHOR:
- QBIT weights: heat=-0.4 (reduce activity) ✓
- Political power: 0.67 (strong support) ✓
- Core effect: npc_density_max=0.35 ✓

My interpretation reduces activity (heat=-0.4) while allowing
reasonable completion of legitimate business. This aligns with
the law's QBIT direction.

LOGGED: This ruling becomes case law for future AI constructors.
"""

# Add to interpretation log (appended to Jupyter notebook)
interpretations["LC_0231"].append({
    "date": "2025-12-07",
    "case": "Customer finishing meal after curfew",
    "ruling": "Allowed under security escort, must exit within 15 min",
    "wiggle_used": 0.4,
    "wiggle_available": 0.60,
    "rationale": "Aligns with law's heat reduction goal while allowing completion of legitimate activity"
})
```

**This interpretation is MUTABLE but CONSTRAINED:**
- ✅ Can't violate core effects (npc_density_max stays 0.35)
- ✅ Can't contradict QBIT weights (must reduce heat, increase coherence)
- ✅ Can't exceed interpretation_radius (only 0.60 wiggle room)
- ✅ Must align with political power (0.67 = strong support, not controversial)

### Step 5: AI Constructors Query Both Layers

When generating NPC behavior:

```python
# Query immutable truth
law = load_law("LC_0231")
base_params = law["effects"]  # npc_density_max = 0.35

# Query governor's interpretations
case_law = load_interpretations("LC_0231")

# Apply to specific situation
if time > "22:00" and npc.class == "CUSTOMER" and npc.is_eating:
    # Check governor's ruling
    ruling = case_law.find_matching("customer_after_hours")

    if ruling:
        # Apply interpretation (within wiggle room)
        allow_with_escort = True
        time_limit = 15  # minutes
    else:
        # Fall back to strict reading
        force_exit = True
```

## The Filing Cabinet Structure

```
constitution_log.jsonl          ← IMMUTABLE truths
│
└─ Each entry:
   ├─ Law definition (text, weights, effects)
   ├─ Political power (consensus calculation)
   ├─ QBIT snapshot (world state)
   ├─ Timestamp
   └─ Calculated constraints (strength, interpretation_radius)

constitutional_bible.ipynb      ← IMMUTABLE archive + MUTABLE interpretations
│
├─ Analysis cells (queries on immutable data)
│  ├─ "What was world like when law passed?"
│  ├─ "How has QBIT drifted since?"
│  └─ "Which laws are obsolete?"
│
└─ Governor's interpretation cells (rulings within wiggle room)
   ├─ Edge case rulings
   ├─ Creative applications
   ├─ Precedent for AI constructors
   └─ MUST stay within interpretation_radius
```

## Key Principle: Immutable vs Mutable

### IMMUTABLE (Never Changes)
- QBIT snapshot at enactment
- Political power calculation
- Law text and weights
- Core effects
- Timestamp
- Calculated constraints (strength, interpretation_radius)

**Source of truth:** `constitution_log.jsonl`

### MUTABLE (Governor Can Modify, Within Constraints)
- Specific enforcement decisions
- Edge case rulings
- Creative applications of law text
- Precedent for similar situations

**Workspace:** Jupyter notebook cells

**Constraint:** MUST stay within `interpretation_radius`

## Example: Strong Law vs Weak Law

### Strong Law (interpretation_radius = 0.2)
```python
smoking_ban = Law(
    law_id="LC_0089",
    title="Mickey's Wing Smoking Ban",
    qbit_weights={"coherence": 0.4, "gravity": 0.3},
    effects={"smoking_allowed": False}
)

# High political support → high strength → low wiggle room
political_power = 0.85
strength = 0.85
interpretation_radius = 0.15  # Very little freedom

# Governor's interpretation must be STRICT:
"""
RULING: No smoking means NO SMOKING.
Interpretation radius too small for creative application.
E-cigarettes? NO. (Would need 0.3+ radius)
Vaping? NO. (Would need 0.3+ radius)
Standing outside doorway? NO. (Would need 0.2+ radius)

Only interpretation available (0.15 wiggle):
- "Smoking" includes all nicotine delivery devices.
- Enforcement begins at threshold of Mickey's Wing.
"""
```

### Weak Law (interpretation_radius = 0.75)
```python
assembly_law = Law(
    law_id="LC_0145",
    title="Free Speech Zone",
    qbit_weights={"coherence": -0.2, "gravity": -0.1},
    effects={"allow_assembly": True, "max_crowd_size": 50}
)

# Mixed political support → lower strength → high wiggle room
political_power = 0.25
strength = 0.25
interpretation_radius = 0.75  # Lots of freedom

# Governor's interpretation can be CREATIVE:
"""
RULING: Assembly allowed, with flexible interpretation.

Given high interpretation radius (0.75), I rule:
- "50 max" can flex to 65 if peaceful (uses 0.3 wiggle)
- "Assembly" includes performances, speeches, drumming (uses 0.2 wiggle)
- "Zone" can spill slightly into corridors if no obstruction (uses 0.15 wiggle)
- Total wiggle used: 0.65 of 0.75 available

This creative interpretation still respects:
- QBIT weights: coherence=-0.2 (some disorder OK) ✓
- Political power: 0.25 (contested, so flexibility justified) ✓
- Core effect: allow_assembly=True ✓
"""
```

## AI Constructor Workflow

```python
# 1. Load immutable truth
law = constitution.get_law("LC_0231")

# 2. Check constraints
if law["interpretation_radius"] < 0.3:
    # Strict enforcement only
    creative_mode = False
else:
    # Can query governor's interpretations
    creative_mode = True

# 3. Query governor's case law (if creative mode)
if creative_mode:
    interpretations = governor.get_interpretations("LC_0231")

    # Find matching precedent
    precedent = interpretations.find_similar(current_situation)

    if precedent:
        # Apply governor's ruling
        apply_interpretation(precedent)
    else:
        # Generate new interpretation (within radius)
        # Will be logged for governor to approve/reject
        propose_interpretation(current_situation)
else:
    # Strict reading of law text
    apply_strict_enforcement(law["effects"])

# 4. Log action to constitutional bible
log_enforcement_action(law_id, action_taken, wiggle_used)
```

## Summary

| Aspect | Immutable Truth | Mutable Interpretation |
|--------|----------------|----------------------|
| **What** | Law text, QBIT snapshot, political power | Specific rulings, edge cases |
| **Who decides** | Consensus (math) | Governor (within constraints) |
| **Where stored** | constitution_log.jsonl | Jupyter notebook cells |
| **Can change?** | NO | YES (but constrained) |
| **Constraint** | N/A (it's the source) | interpretation_radius |
| **Purpose** | Source of truth | Practical application |

**The Filing Cabinet = Both:**
- Archive of immutable constitutional history
- Workspace for governor's constrained interpretations

**Jupyter Notebook = Game Bible:**
- Query: "What was the world like?"
- Query: "What did the governor rule?"
- Add: "Here's my new ruling (within wiggle room)"

---

## Technical Implementation

### Immutable Layer (JSONL)
```bash
cat data/constitution_log.jsonl | jq '.'
# Each line = complete constitutional entry
# Never modified, only appended
```

### Mutable Layer (Jupyter Cells)
```python
# In constitutional_bible.ipynb

# Cell 1: Load immutable
constitution = load_constitution_log()

# Cell 2: Governor adds interpretation
"""
GOVERNOR RULING: LC_0231 edge case...
(This cell can be edited, but must respect interpretation_radius)
"""
```

### Query Interface
```python
# AI constructor queries both layers

# Immutable: What's the law?
law_text = constitution.get_law("LC_0231")

# Mutable: How has it been interpreted?
case_law = governor.get_interpretations("LC_0231")

# Constraint: Can I be creative?
wiggle = law_text["interpretation_radius"]
if my_proposal.wiggle_used <= wiggle:
    allowed = True
```

---

**The governor doesn't change the math. The governor interprets within the math's constraints.**

**QBIT + consensus = immutable truth**

**Governor = constrained creativity within interpretation_radius**

**Jupyter = filing cabinet for both**
