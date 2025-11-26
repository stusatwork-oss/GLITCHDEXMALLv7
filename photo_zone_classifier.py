#!/usr/bin/env python3
"""
Photo Zone Classifier - Batch Processing System
Processes Eastland Mall photos into zone categories without context freeze.

Process:
1. Load photo list
2. Process in small batches (10 at a time)
3. Generate classifications
4. Output UNPLACEABLE.md for review
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Set

# Zone definitions based on existing structure
ZONES = {
    "atrium": [
        "main atrium", "central atrium", "glass roof", "skylight",
        "open court", "vertical space", "multi-story open", "balcony view"
    ],
    "food_court": [
        "food court", "dining area", "tables", "seating area",
        "sunken level", "FC-ARCADE", "JOLLY TIME", "glass block",
        "fountain", "eating area"
    ],
    "escalators": [
        "escalator", "moving stairs", "vertical transport",
        "up/down", "mechanical stairs"
    ],
    "exterior": [
        "outside", "parking lot", "entrance", "facade",
        "exterior wall", "signage external", "building exterior",
        "outdoor", "parking", "entry"
    ],
    "movie_mouth": [
        "cinema", "theater", "movie", "cinema 6", "theater entrance",
        "ticket booth", "movie entrance", "theater signage"
    ],
    "comphut": [
        "Computer Hut", "COMPHUT", "computer store", "electronics store"
    ],
    "maintenance": [
        "utility", "mechanical", "back of house", "service corridor",
        "janitor", "maintenance area", "utility room"
    ],
    "corridors": [
        "hallway", "corridor", "walkway", "passage", "concourse",
        "main corridor", "side corridor", "connecting passage"
    ],
    "anchor_stores": [
        "department store", "JCPenney", "Sears", "Carson",
        "anchor store", "large store entrance"
    ],
    "storefronts": [
        "store", "shop", "retail", "storefront", "display window",
        "mall store", "tenant space"
    ]
}

# Keywords that indicate uncertainty
UNCERTAIN_KEYWORDS = [
    "ice rink", "skating", "ice skating", "hockey rink",
    "unclear", "blurry", "indistinct", "cannot identify",
    "too dark", "overexposed", "partial view"
]

class PhotoClassifier:
    def __init__(self, photo_dir: str, output_dir: str):
        self.photo_dir = Path(photo_dir)
        self.output_dir = Path(output_dir)
        self.unplaceable = []
        self.classifications = {zone: [] for zone in ZONES.keys()}
        self.classifications['corridors'] = []
        self.classifications['anchor_stores'] = []
        self.classifications['storefronts'] = []

    def scan_photos(self) -> List[Path]:
        """Get all photos in archive."""
        extensions = {'.jpg', '.jpeg', '.png', '.gif'}
        photos = []
        for ext in extensions:
            photos.extend(self.photo_dir.glob(f'*{ext}'))
            photos.extend(self.photo_dir.glob(f'*{ext.upper()}'))
        return sorted(photos)

    def classify_batch(self, photos: List[Path], batch_num: int) -> Dict:
        """
        Classify a batch of photos.
        Returns dict with classifications and unplaceable items.
        """
        print(f"\n--- Batch {batch_num} ({len(photos)} photos) ---")
        batch_result = {
            'classified': [],
            'unplaceable': []
        }

        for photo in photos:
            filename = photo.name
            print(f"Processing: {filename}")

            # Manual classification would happen here
            # For now, this is a placeholder that marks all as unplaceable
            # In real usage, you'd inspect each photo
            batch_result['unplaceable'].append({
                'filename': filename,
                'reason': 'Awaiting manual review',
                'path': str(photo.relative_to(self.photo_dir.parent.parent.parent))
            })

        return batch_result

    def generate_report(self):
        """Generate UNPLACEABLE.md report."""
        report = []
        report.append("# UNPLACEABLE PHOTOS - Manual Review Required\n")
        report.append(f"**Total Photos Scanned:** {self.total_photos}")
        report.append(f"**Unplaceable:** {len(self.unplaceable)}")
        report.append(f"**Classified:** {self.total_photos - len(self.unplaceable)}\n")
        report.append("---\n")
        report.append("## Instructions\n")
        report.append("Review each photo below and manually classify into zones:\n")
        report.append("- `atrium/` - Main atrium, central court, glass roof areas")
        report.append("- `food_court/` - Food court, JOLLY TIME, sunken dining")
        report.append("- `escalators/` - Escalator photos")
        report.append("- `exterior/` - Outside views, parking, facade")
        report.append("- `movie_mouth/` - Cinema 6, theater entrance")
        report.append("- `comphut/` - Computer Hut store")
        report.append("- `maintenance/` - Utility, service areas")
        report.append("- `corridors/` - Hallways, passages, concourse")
        report.append("- `anchor_stores/` - JCPenney, Sears, Carson's, etc.")
        report.append("- `storefronts/` - Individual stores, retail spaces")
        report.append("- `DELETE` - Wrong mall (skating rink) or unusable\n")
        report.append("---\n")
        report.append("## Photos Requiring Classification\n\n")

        for i, photo in enumerate(self.unplaceable, 1):
            report.append(f"### {i}. `{photo['filename']}`\n")
            report.append(f"**Path:** `{photo['path']}`  ")
            report.append(f"**Reason:** {photo['reason']}  ")
            report.append(f"**Action:** [ ] Classify to zone: ___________  \n")

        return "\n".join(report)

    def run_batch_process(self, batch_size: int = 10):
        """Main processing loop."""
        photos = self.scan_photos()
        self.total_photos = len(photos)

        print(f"Found {self.total_photos} photos in {self.photo_dir}")
        print(f"Processing in batches of {batch_size}...")

        # Process in batches
        for i in range(0, len(photos), batch_size):
            batch = photos[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            result = self.classify_batch(batch, batch_num)

            self.unplaceable.extend(result['unplaceable'])

        # Generate report
        report_content = self.generate_report()
        report_path = Path("/home/user/GLUTCHDEXMALL/UNPLACEABLE.md")
        report_path.write_text(report_content)

        print(f"\n✓ Processing complete!")
        print(f"✓ Report written to: UNPLACEABLE.md")
        print(f"\nSummary:")
        print(f"  Total: {self.total_photos}")
        print(f"  Unplaceable: {len(self.unplaceable)}")
        print(f"  Classified: {self.total_photos - len(self.unplaceable)}")


if __name__ == "__main__":
    classifier = PhotoClassifier(
        photo_dir="/home/user/GLUTCHDEXMALL/v6-nextgen/assets/photos/eastland-archive",
        output_dir="/home/user/GLUTCHDEXMALL/v6-nextgen/assets/photos/zones"
    )
    classifier.run_batch_process(batch_size=10)
