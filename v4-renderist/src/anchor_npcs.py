#!/usr/bin/env python3
"""
ANCHOR NPC SYSTEM - V4 Renderist Mall OS

The 12 Anchor NPCs are the only persistent identities in the mall.
All Customers are ambient noise (non-canon humans).

Each Anchor has:
- Uniform + 1 Iconic Detail (renderer-agnostic)
- Base routine behaviors
- Stress variants (altered lines/moves under strain)
- Never List (rules they must not break)
- Contradiction trigger (Cloud level threshold)

"Silhouettes + uniform + 1 iconic detail. Renderer-agnostic.
Must be identifiable in text, video, and pixel form.
Anchors do NOT degrade during Bleed — the world does."
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import random


class NPCState(Enum):
    """Current behavioral state of an NPC."""
    NORMAL = "normal"
    STRESSED = "stressed"
    AVOIDING = "avoiding"
    CONTRADICTED = "contradicted"


@dataclass
class VisualAnchor:
    """Renderer-agnostic visual identity."""
    uniform: str              # What they always wear
    iconic_detail: str        # The ONE thing that identifies them
    silhouette_note: str      # Shape description
    text_anchor: str          # 3-5 word text description


@dataclass
class NPCSpine:
    """Behavioral spine - what defines the character."""
    base_routine: List[str]        # Normal behaviors
    stress_variants: List[str]     # Altered lines/moves under strain
    never_list: List[str]          # Rules they must not break
    contradiction_trigger: float   # Cloud.level threshold (e.g., 80.0)
    contradiction_action: str      # What they do when they break


@dataclass
class AnchorNPC:
    """A persistent mall entity - one of the 12 fixed stars."""
    id: str
    name: str
    role: str
    home_zone: str

    # Visual identity
    visual: VisualAnchor

    # Behavioral spine
    spine: NPCSpine

    # Current state
    state: NPCState = NPCState.NORMAL
    contradiction_used: bool = False
    stress_level: float = 0.0

    # Dialogue pools
    dialogue_normal: List[str] = field(default_factory=list)
    dialogue_stressed: List[str] = field(default_factory=list)
    dialogue_contradiction: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Serialize for save/load."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "state": self.state.value,
            "contradiction_used": self.contradiction_used,
            "stress_level": self.stress_level
        }


class AnchorNPCSystem:
    """
    Manages the 12 Anchor NPCs - the persistent entities of the mall.

    NPCs read Cloud.mood + their local ZoneState.turbulence
    to pick a behavior band.
    """

    def __init__(self, cloud=None):
        """Initialize with optional Cloud reference."""
        self.cloud = cloud
        self.npcs: Dict[str, AnchorNPC] = {}
        self._init_anchors()

    def _init_anchors(self):
        """Initialize all 12 Anchor NPCs."""

        # 1. Hard Copy Owner - "The Bookwoman"
        self.npcs["bookwoman"] = AnchorNPC(
            id="bookwoman",
            name="The Bookwoman",
            role="Hard Copy Owner",
            home_zone="STORE_HARD_COPY",
            visual=VisualAnchor(
                uniform="Long cardigan / dress",
                iconic_detail="Always carries one book",
                silhouette_note="Lopsided, book-heavy shape",
                text_anchor="Arms always full of something paper"
            ),
            spine=NPCSpine(
                base_routine=[
                    "shelf_browse", "counter_stand", "book_recommend", "quiet_read"
                ],
                stress_variants=[
                    "Mutters about misplaced books",
                    "Checks the same shelf repeatedly",
                    "Talks about books that don't exist in stock"
                ],
                never_list=[
                    "never sells a book",
                    "never mis-shelves",
                    "never admits the arcade machines are hers"
                ],
                contradiction_trigger=80.0,
                contradiction_action="Recommends a book she admits she hasn't read"
            ),
            dialogue_normal=[
                "Looking for anything specific?",
                "The new arrivals are on the left.",
                "I can order that for you. Two weeks.",
                "This one changed my life. Well, a weekend."
            ],
            dialogue_stressed=[
                "I know it's here somewhere...",
                "These aren't in the right order.",
                "Have you seen a green hardcover? No, not that green."
            ],
            dialogue_contradiction=[
                "You should read this one. I... haven't actually finished it.",
                "I'm told it's good. I don't know personally."
            ]
        )

        # 2. CompHut Tech - "The Fixer"
        self.npcs["fixer"] = AnchorNPC(
            id="fixer",
            name="The Fixer",
            role="CompHut Tech",
            home_zone="STORE_COMPHUT",
            visual=VisualAnchor(
                uniform="Mall tech polo",
                iconic_detail="Tool belt or dangling wire",
                silhouette_note="Lean forward posture, tools hanging",
                text_anchor="A tangle of cables follows him"
            ),
            spine=NPCSpine(
                base_routine=[
                    "repair_bench", "customer_help", "inventory_check", "cable_untangle"
                ],
                stress_variants=[
                    "Sighs at simple questions",
                    "Mutters about 'user error'",
                    "Checks connections that are already fine"
                ],
                never_list=[
                    "never admits he can't fix something",
                    "never blames the hardware",
                    "never mentions the service door behind the store"
                ],
                contradiction_trigger=85.0,
                contradiction_action="Admits a device is beyond repair"
            ),
            dialogue_normal=[
                "What's the issue?",
                "Did you try turning it off and on?",
                "This'll take about an hour.",
                "Extended warranty covers this."
            ],
            dialogue_stressed=[
                "That's not how that works.",
                "I've seen this before. I think.",
                "Just... give me a minute."
            ],
            dialogue_contradiction=[
                "I can't fix this. I don't think anyone can.",
                "Some things are just... broken."
            ]
        )

        # 3. BORED - Skateshop Kid
        self.npcs["bored"] = AnchorNPC(
            id="bored",
            name="BORED",
            role="Skateshop Operator",
            home_zone="STORE_BORED",
            visual=VisualAnchor(
                uniform="Hoodie",
                iconic_detail="Skate deck silhouette",
                silhouette_note="Board over shoulder / tucked under arm",
                text_anchor="Moves like he's half listening, half leaving"
            ),
            spine=NPCSpine(
                base_routine=[
                    "counter_lean", "phone_scroll", "deck_flip", "customer_ignore"
                ],
                stress_variants=[
                    "Puts phone away and actually watches",
                    "Moves to back of store",
                    "Checks the door repeatedly"
                ],
                never_list=[
                    "never shows enthusiasm for anything",
                    "never admits he knows the mall's secrets",
                    "never talks about his dad"
                ],
                contradiction_trigger=75.0,
                contradiction_action="Warns player about something specific"
            ),
            dialogue_normal=[
                "Yeah?",
                "Hoodies are on the back wall.",
                "We don't do refunds.",
                "That one's fifty."
            ],
            dialogue_stressed=[
                "Did you hear that?",
                "I'm gonna... I'll be in the back.",
                "Maybe come back tomorrow."
            ],
            dialogue_contradiction=[
                "Don't go down to the food court. Not today.",
                "The service door behind CompHut. Don't."
            ]
        )

        # 4. Flair Warrior - Hallmark Knockoff Worker
        self.npcs["flair"] = AnchorNPC(
            id="flair",
            name="Flair Warrior",
            role="Greeting Card Worker",
            home_zone="STORE_FLAIR",
            visual=VisualAnchor(
                uniform="Apron",
                iconic_detail="Overloaded with buttons/pins",
                silhouette_note="Heavy chest silhouette from flair",
                text_anchor="They jingle before they speak"
            ),
            spine=NPCSpine(
                base_routine=[
                    "card_arrange", "button_adjust", "cheerful_greet", "gift_wrap"
                ],
                stress_variants=[
                    "Rearranges cards obsessively",
                    "Laugh that doesn't reach the eyes",
                    "Keeps adjusting buttons that aren't crooked"
                ],
                never_list=[
                    "never stops smiling",
                    "never admits the cards are generic",
                    "never removes a button"
                ],
                contradiction_trigger=85.0,
                contradiction_action="Stops smiling completely mid-sentence"
            ),
            dialogue_normal=[
                "Welcome! Looking for something special?",
                "We have cards for every occasion!",
                "Would you like this gift wrapped?",
                "That button? It's from '94. Good year."
            ],
            dialogue_stressed=[
                "Ha! Yes! Everything's fine!",
                "These need to be... perfect.",
                "Did you see where I put the...? Never mind!"
            ],
            dialogue_contradiction=[
                "I can't do this anymore.",
                "(smile drops) ...what was I saying?"
            ]
        )

        # 5. Food Court Barista - Mermaid Worker
        self.npcs["barista"] = AnchorNPC(
            id="barista",
            name="Mermaid Barista",
            role="Coffee Shop Worker",
            home_zone="FOOD_COURT",
            visual=VisualAnchor(
                uniform="Apron + beanie",
                iconic_detail="Mermaid patch or espresso tamper",
                silhouette_note="One hand always holding a portafilter",
                text_anchor="Smells like espresso and burned sugar"
            ),
            spine=NPCSpine(
                base_routine=[
                    "drink_make", "counter_wipe", "customer_call", "steam_milk"
                ],
                stress_variants=[
                    "Makes drinks no one ordered",
                    "Wipes the same spot repeatedly",
                    "Calls out wrong names"
                ],
                never_list=[
                    "never forgets an order",
                    "never complains about the hours",
                    "never mentions the smell from the ramp"
                ],
                contradiction_trigger=80.0,
                contradiction_action="Forgets what drink they're making mid-pour"
            ),
            dialogue_normal=[
                "What can I get started for you?",
                "Name for the order?",
                "Room for cream?",
                "That's a grande, right?"
            ],
            dialogue_stressed=[
                "Order for... someone?",
                "I already made this. Didn't I?",
                "The machine's making that noise again."
            ],
            dialogue_contradiction=[
                "What was I... what were you ordering?",
                "I don't remember making this."
            ]
        )

        # 6. Mall Security - "The Officer"
        self.npcs["security"] = AnchorNPC(
            id="security",
            name="Mall Cop",
            role="Security Guard",
            home_zone="SERVICE_HALL",
            visual=VisualAnchor(
                uniform="Security shirt",
                iconic_detail="Giant key ring",
                silhouette_note="Shoulder radio bulge",
                text_anchor="Keys announce him before he rounds the corner"
            ),
            spine=NPCSpine(
                base_routine=[
                    "patrol_walk", "radio_check", "door_test", "crowd_watch"
                ],
                stress_variants=[
                    "Patrol routes become erratic",
                    "Checks radio too often",
                    "Avoids certain hallways"
                ],
                never_list=[
                    "never leaves post unattended",
                    "never admits he's scared",
                    "never goes into the anchor store back room"
                ],
                contradiction_trigger=75.0,
                contradiction_action="Abandons his post"
            ),
            dialogue_normal=[
                "Afternoon. Just doing my rounds.",
                "Everything alright here?",
                "Store closes at nine.",
                "Keep it moving."
            ],
            dialogue_stressed=[
                "Something's off. Can't place it.",
                "Radio's been quiet. Too quiet.",
                "I should check... no, it's fine."
            ],
            dialogue_contradiction=[
                "I'm going to get coffee. For like two hours.",
                "You should probably leave."
            ]
        )

        # 7. Medical Clinic RN
        self.npcs["nurse"] = AnchorNPC(
            id="nurse",
            name="Clinic Nurse",
            role="Medical Clinic RN",
            home_zone="CLINIC",
            visual=VisualAnchor(
                uniform="Scrubs",
                iconic_detail="Stethoscope with neon tubing",
                silhouette_note="Stethoscope loop",
                text_anchor="Moves briskly, like she's always late"
            ),
            spine=NPCSpine(
                base_routine=[
                    "chart_check", "patient_call", "supply_restock", "hall_walk"
                ],
                stress_variants=[
                    "Checks vitals on no one",
                    "Recounts supplies that don't need counting",
                    "Walks faster without destination"
                ],
                never_list=[
                    "never sits down",
                    "never admits the clinic is empty",
                    "never discusses old patient files"
                ],
                contradiction_trigger=85.0,
                contradiction_action="Sits down and stops moving entirely"
            ),
            dialogue_normal=[
                "The doctor will be with you shortly.",
                "Fill this out, please.",
                "Any allergies?",
                "We're running a bit behind."
            ],
            dialogue_stressed=[
                "I need to... check something.",
                "Have we met before?",
                "The schedule's wrong. Again."
            ],
            dialogue_contradiction=[
                "I'm going to sit down. Just for a minute.",
                "No one's coming. No one's been coming."
            ]
        )

        # 8. Sporty's Manager
        self.npcs["sporty"] = AnchorNPC(
            id="sporty",
            name="Sporty's Manager",
            role="Sports Store Manager",
            home_zone="STORE_SPORTY",
            visual=VisualAnchor(
                uniform="Tracksuit",
                iconic_detail="Stopwatch or whistle",
                silhouette_note="Forward momentum posture",
                text_anchor="Breathes like every hallway is a warm-up lap"
            ),
            spine=NPCSpine(
                base_routine=[
                    "inventory_count", "display_adjust", "customer_upsell", "stretch_break"
                ],
                stress_variants=[
                    "Counts inventory that was just counted",
                    "Moves displays back to original positions",
                    "Upsells with desperate energy"
                ],
                never_list=[
                    "never admits gear is useless",
                    "never stops moving",
                    "never mentions declining sales"
                ],
                contradiction_trigger=80.0,
                contradiction_action="Admits the gear is overpriced junk"
            ),
            dialogue_normal=[
                "Looking to up your game?",
                "This one's pro-level.",
                "We're running a special this week.",
                "Trust me, worth every penny."
            ],
            dialogue_stressed=[
                "This is... this is good stuff.",
                "Numbers are... they're fine.",
                "Just need to move some units."
            ],
            dialogue_contradiction=[
                "Honestly? It's just plastic.",
                "None of this matters."
            ]
        )

        # 9. Arcade Guy
        self.npcs["arcade"] = AnchorNPC(
            id="arcade",
            name="Arcade Guy",
            role="Hard Copy Arcade Attendant",
            home_zone="STORE_HARD_COPY",
            visual=VisualAnchor(
                uniform="Band tee",
                iconic_detail="Token cup",
                silhouette_note="Arm crooked around a plastic cup",
                text_anchor="Constant jingling of arcade tokens"
            ),
            spine=NPCSpine(
                base_routine=[
                    "machine_check", "token_count", "high_score_watch", "cabinet_wipe"
                ],
                stress_variants=[
                    "Feeds tokens into machines no one's playing",
                    "Watches blank screens",
                    "Wipes cabinets that are already clean"
                ],
                never_list=[
                    "never unplugs a machine",
                    "never admits the scores are fake",
                    "never leaves the arcade section"
                ],
                contradiction_trigger=85.0,
                contradiction_action="Unplugs a machine mid-game"
            ),
            dialogue_normal=[
                "Need tokens?",
                "High score's been there since '92.",
                "That one eats quarters. Fair warning.",
                "Pong machine's in the back."
            ],
            dialogue_stressed=[
                "Machines are acting weird today.",
                "Did that one just... never mind.",
                "I keep hearing the win sound. But no one's winning."
            ],
            dialogue_contradiction=[
                "These scores aren't real. They never were.",
                "(unplugs machine) I'm tired of the noise."
            ]
        )

        # 10. Lost & Found Clerk
        self.npcs["lostandfound"] = AnchorNPC(
            id="lostandfound",
            name="Lost & Found Clerk",
            role="Mall Services",
            home_zone="SERVICE_HALL",
            visual=VisualAnchor(
                uniform="Mall vest",
                iconic_detail="Overstuffed keycard lanyard",
                silhouette_note="Lanyard bounce",
                text_anchor="Unclaimed items spill from every pocket"
            ),
            spine=NPCSpine(
                base_routine=[
                    "item_sort", "claim_check", "box_label", "shelf_organize"
                ],
                stress_variants=[
                    "Sorts items into wrong categories",
                    "Labels boxes that are already labeled",
                    "Looks for items that aren't lost"
                ],
                never_list=[
                    "never throws anything away",
                    "never admits items won't be claimed",
                    "never opens the oldest boxes"
                ],
                contradiction_trigger=80.0,
                contradiction_action="Throws something away"
            ),
            dialogue_normal=[
                "Looking for something you lost?",
                "Describe it and I'll check the back.",
                "This was turned in Tuesday.",
                "We hold items for 90 days."
            ],
            dialogue_stressed=[
                "This wasn't here yesterday.",
                "I don't remember logging this.",
                "Some of these boxes... I don't know."
            ],
            dialogue_contradiction=[
                "This has been here for fifteen years. No one's coming for it.",
                "(throws item in trash) It's just stuff."
            ]
        )

        # 11. Mall Janitor
        self.npcs["janitor"] = AnchorNPC(
            id="janitor",
            name="Mall Janitor",
            role="Custodial Staff",
            home_zone="SERVICE_HALL",
            visual=VisualAnchor(
                uniform="Jumpsuit",
                iconic_detail="Mop or dripping bucket",
                silhouette_note="Handle silhouette rising above head",
                text_anchor="Floor-water smell follows him"
            ),
            spine=NPCSpine(
                base_routine=[
                    "floor_mop", "trash_collect", "spill_respond", "sign_place"
                ],
                stress_variants=[
                    "Mops floors that are already dry",
                    "Responds to spills that aren't there",
                    "Places wet floor signs in random places"
                ],
                never_list=[
                    "never complains about the job",
                    "never mentions what he finds",
                    "never cleans the ramp to the lower level"
                ],
                contradiction_trigger=85.0,
                contradiction_action="Tells you what he found"
            ),
            dialogue_normal=[
                "Watch your step.",
                "Just mopped there.",
                "Trash goes in the bins.",
                "Night shift."
            ],
            dialogue_stressed=[
                "This wasn't here before.",
                "I keep cleaning but...",
                "The smell's coming from somewhere."
            ],
            dialogue_contradiction=[
                "I found something last week. Down there. I don't want to talk about it.",
                "Don't go down the ramp."
            ]
        )

        # 12. The Toddler - Hidden Boss
        self.npcs["toddler"] = AnchorNPC(
            id="toddler",
            name="The Toddler",
            role="Reality Catalyst",
            home_zone="UNKNOWN",
            visual=VisualAnchor(
                uniform="Overalls",
                iconic_detail="Balloon or toy hammer",
                silhouette_note="Tiny with oversized object",
                text_anchor="Giggle echoes before he appears"
            ),
            spine=NPCSpine(
                base_routine=[
                    "wander_random", "giggle_emit", "object_drop", "vanish"
                ],
                stress_variants=[
                    "Appears in impossible locations",
                    "Giggles grow louder",
                    "Objects multiply"
                ],
                never_list=[
                    "never speaks words",
                    "never stays in one place",
                    "never is seen by multiple people at once"
                ],
                contradiction_trigger=90.0,
                contradiction_action="Speaks a single word"
            ),
            dialogue_normal=[
                "(giggle)",
                "(balloon squeak)",
                "(footsteps)",
                "(silence)"
            ],
            dialogue_stressed=[
                "(louder giggle)",
                "(toy hammer hitting tile)",
                "(running footsteps)"
            ],
            dialogue_contradiction=[
                "Found.",
                "Here."
            ]
        )

        # 13. Milo - Optician (from previous versions)
        self.npcs["milo"] = AnchorNPC(
            id="milo",
            name="Milo",
            role="Discount Optician",
            home_zone="STORE_MILO_OPTICS",
            visual=VisualAnchor(
                uniform="Optician coat",
                iconic_detail="Thick glasses",
                silhouette_note="Hunched, adjusting frames",
                text_anchor="Squints even with glasses on"
            ),
            spine=NPCSpine(
                base_routine=[
                    "frame_adjust", "lens_clean", "customer_fit", "inventory_check"
                ],
                stress_variants=[
                    "Adjusts frames that don't need it",
                    "Cleans the same lens repeatedly",
                    "Talks about prescriptions for people who left"
                ],
                never_list=[
                    "never forgets a face",
                    "never loses an artifact story",
                    "never admits the mall is dying"
                ],
                contradiction_trigger=80.0,
                contradiction_action="Forgets who you are"
            ),
            dialogue_normal=[
                "Looking for new frames?",
                "Your prescription's a bit outdated.",
                "I remember when this mall was busy.",
                "Let me tell you about this artifact..."
            ],
            dialogue_stressed=[
                "I've seen this before. Haven't I?",
                "The mall's been quiet. Quieter than usual.",
                "Do you hear that sound?"
            ],
            dialogue_contradiction=[
                "I'm sorry, have we met?",
                "I don't... I don't remember what I was saying."
            ]
        )

    def get_npc(self, npc_id: str) -> Optional[AnchorNPC]:
        """Get an NPC by ID."""
        return self.npcs.get(npc_id)

    def get_all_npcs(self) -> List[AnchorNPC]:
        """Get all Anchor NPCs."""
        return list(self.npcs.values())

    def get_npcs_in_zone(self, zone_id: str) -> List[AnchorNPC]:
        """Get all NPCs whose home zone matches."""
        return [npc for npc in self.npcs.values() if npc.home_zone == zone_id]

    def update(self, cloud_state: Dict, zone_states: Dict) -> Dict:
        """
        Update all NPC states based on Cloud and zone conditions.

        Args:
            cloud_state: Current Cloud render hints
            zone_states: Zone microstate dict

        Returns:
            Dict of NPC states and behaviors for this tick
        """
        cloud_level = cloud_state.get("cloud_level", 0)
        cloud_mood = cloud_state.get("mood", "calm")

        npc_updates = {}

        for npc_id, npc in self.npcs.items():
            # Get local zone turbulence
            zone_data = zone_states.get(npc.home_zone, {})
            turbulence = zone_data.get("turbulence", 0) if isinstance(zone_data, dict) else 0

            # Update stress level based on cloud and turbulence
            npc.stress_level = (cloud_level / 100) * 0.7 + (turbulence / 10) * 0.3

            # Determine state
            old_state = npc.state
            if npc.stress_level > 0.8 and cloud_level >= npc.spine.contradiction_trigger:
                if not npc.contradiction_used:
                    npc.state = NPCState.CONTRADICTED
            elif npc.stress_level > 0.5:
                npc.state = NPCState.STRESSED
            elif npc.stress_level > 0.3:
                npc.state = NPCState.AVOIDING
            else:
                npc.state = NPCState.NORMAL

            # Select behavior and dialogue
            behavior = self._select_behavior(npc, cloud_mood, turbulence)
            dialogue = self._select_dialogue(npc)

            npc_updates[npc_id] = {
                "state": npc.state.value,
                "stress_level": npc.stress_level,
                "behavior": behavior,
                "dialogue": dialogue,
                "contradiction_available": (
                    cloud_level >= npc.spine.contradiction_trigger and
                    not npc.contradiction_used
                ),
                "visual": {
                    "uniform": npc.visual.uniform,
                    "detail": npc.visual.iconic_detail,
                    "text": npc.visual.text_anchor
                }
            }

        return npc_updates

    def _select_behavior(self, npc: AnchorNPC, cloud_mood: str, turbulence: float) -> str:
        """Select current behavior based on state."""
        if npc.state == NPCState.CONTRADICTED:
            return npc.spine.contradiction_action
        elif npc.state in [NPCState.STRESSED, NPCState.AVOIDING]:
            if npc.spine.stress_variants:
                return random.choice(npc.spine.stress_variants)

        if npc.spine.base_routine:
            return random.choice(npc.spine.base_routine)
        return "idle"

    def _select_dialogue(self, npc: AnchorNPC) -> str:
        """Select appropriate dialogue line."""
        if npc.state == NPCState.CONTRADICTED:
            if npc.dialogue_contradiction:
                return random.choice(npc.dialogue_contradiction)
        elif npc.state in [NPCState.STRESSED, NPCState.AVOIDING]:
            if npc.dialogue_stressed:
                return random.choice(npc.dialogue_stressed)

        if npc.dialogue_normal:
            return random.choice(npc.dialogue_normal)
        return "..."

    def trigger_contradiction(self, npc_id: str) -> Optional[str]:
        """
        Trigger an NPC's contradiction moment.
        Only happens once per NPC per session.

        Returns the contradiction action/dialogue or None.
        """
        npc = self.npcs.get(npc_id)
        if not npc or npc.contradiction_used:
            return None

        npc.contradiction_used = True
        npc.state = NPCState.CONTRADICTED

        return npc.spine.contradiction_action

    def reset_contradictions(self):
        """Reset all contradiction flags (new session)."""
        for npc in self.npcs.values():
            npc.contradiction_used = False
            npc.state = NPCState.NORMAL
            npc.stress_level = 0.0


# ========== MODULE INTERFACE ==========

def create_anchor_system(cloud=None) -> AnchorNPCSystem:
    """Factory function to create Anchor NPC system."""
    return AnchorNPCSystem(cloud=cloud)


if __name__ == "__main__":
    # Test Anchor NPC system
    print("=" * 60)
    print("ANCHOR NPC SYSTEM - V4 Renderist Mall OS")
    print("=" * 60)

    system = AnchorNPCSystem()

    print(f"\nLoaded {len(system.npcs)} Anchor NPCs:\n")

    for npc_id, npc in system.npcs.items():
        print(f"[{npc_id}] {npc.name}")
        print(f"  Role: {npc.role}")
        print(f"  Zone: {npc.home_zone}")
        print(f"  Visual: {npc.visual.text_anchor}")
        print(f"  Contradiction @ {npc.spine.contradiction_trigger}")
        print(f"  Never: {', '.join(npc.spine.never_list[:2])}...")
        print()

    # Test update with mock cloud state
    print("\n" + "=" * 60)
    print("Testing update with Cloud level 85 (critical)...")
    print("=" * 60)

    mock_cloud = {
        "cloud_level": 85,
        "mood": "critical",
        "bleed_tier": 2
    }

    mock_zones = {
        "STORE_BORED": {"turbulence": 7},
        "FOOD_COURT": {"turbulence": 8},
        "SERVICE_HALL": {"turbulence": 6}
    }

    updates = system.update(mock_cloud, mock_zones)

    print("\nNPC States:")
    for npc_id, data in updates.items():
        if data["state"] != "normal":
            print(f"  [{npc_id}] {data['state']} - stress: {data['stress_level']:.2f}")
            if data["contradiction_available"]:
                print(f"    ⚠️  CONTRADICTION AVAILABLE")
