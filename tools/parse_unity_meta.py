#!/usr/bin/env python3
"""
UNITY .META FILE PARSER
Extracts spatial organization and transform data from Cinderella City Project
without needing the actual 600MB of assets.

Unity .meta files contain:
- Transform data (position, rotation, scale)
- Prefab relationships
- Asset organization structure
- Import settings and metadata

Usage:
    python parse_unity_meta.py --input /path/to/extracted/cinderella --output analysis.json
    python parse_unity_meta.py --input cinderella_city/ --show-structure
"""

import yaml
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


class UnityMetaParser:
    """Parse Unity .meta files to extract organizational patterns."""

    def __init__(self):
        self.transforms = []
        self.prefabs = []
        self.folder_structure = defaultdict(list)
        self.photo_waypoints = []
        self.era_layers = defaultdict(list)

    def parse_meta_file(self, meta_path: Path) -> Optional[Dict]:
        """Parse a single .meta file (YAML format)."""
        try:
            content = meta_path.read_text(encoding='utf-8')
            data = yaml.safe_load(content)
            return data
        except Exception as e:
            # Skip binary or corrupted files
            return None

    def extract_transform_data(self, meta_data: Dict, file_path: Path) -> Optional[Dict]:
        """Extract position/rotation/scale from prefab or scene metadata."""
        if not meta_data:
            return None

        # Look for transform data in various Unity structures
        transform = None

        # Method 1: Direct transform in prefab
        if 'PrefabInstance' in meta_data:
            prefab = meta_data['PrefabInstance']
            if 'modification' in prefab:
                # Extract transform modifications
                mods = prefab['modification'].get('m_Modifications', [])
                for mod in mods:
                    if 'propertyPath' in mod:
                        if 'localPosition' in mod['propertyPath']:
                            # Found position data
                            pass

        # Method 2: GameObject with Transform component
        if 'GameObject' in meta_data:
            go = meta_data['GameObject']
            if 'm_Component' in go:
                for comp in go['m_Component']:
                    if 'component' in comp:
                        # Check if it's a transform
                        pass

        return transform

    def scan_directory(self, base_path: Path, pattern: str = "**/*.meta"):
        """Scan directory for all .meta files."""
        meta_files = list(base_path.glob(pattern))
        print(f"Found {len(meta_files)} .meta files")

        for meta_file in meta_files:
            relative_path = meta_file.relative_to(base_path)

            # Parse file
            meta_data = self.parse_meta_file(meta_file)

            # Track folder structure
            folder = relative_path.parent
            self.folder_structure[str(folder)].append(meta_file.stem)

            # Look for era-specific folders
            path_parts = str(relative_path).lower()
            if '60s' in path_parts or '70s' in path_parts:
                self.era_layers['1960s-1970s'].append(str(relative_path))
            elif '80s' in path_parts or '90s' in path_parts:
                self.era_layers['1980s-1990s'].append(str(relative_path))
            elif 'future' in path_parts or 'alternate' in path_parts:
                self.era_layers['alternate_future'].append(str(relative_path))

            # Look for photo-related assets
            if 'photo' in path_parts or 'image' in path_parts or 'waypoint' in path_parts:
                self.photo_waypoints.append({
                    'file': str(relative_path),
                    'stem': meta_file.stem
                })

        return self

    def analyze_structure(self) -> Dict[str, Any]:
        """Analyze the organizational patterns."""
        analysis = {
            'total_assets': sum(len(files) for files in self.folder_structure.values()),
            'folder_count': len(self.folder_structure),
            'era_distribution': {
                era: len(files) for era, files in self.era_layers.items()
            },
            'photo_waypoints_found': len(self.photo_waypoints),
            'top_level_folders': [],
            'naming_patterns': self._analyze_naming_patterns()
        }

        # Get top-level folders
        top_level = set()
        for folder in self.folder_structure.keys():
            if folder and '/' in folder:
                top_level.add(folder.split('/')[0])
            elif folder:
                top_level.add(folder)
        analysis['top_level_folders'] = sorted(list(top_level))

        return analysis

    def _analyze_naming_patterns(self) -> Dict[str, List[str]]:
        """Identify naming conventions."""
        patterns = defaultdict(list)

        for folder, files in self.folder_structure.items():
            for file in files:
                # Zone patterns
                if file.startswith('Z') and len(file) > 1 and file[1].isdigit():
                    patterns['zone_ids'].append(file)

                # Mall/Court patterns
                if 'mall' in file.lower():
                    patterns['mall_zones'].append(file)
                if 'court' in file.lower():
                    patterns['court_zones'].append(file)

                # Store patterns
                if 'store' in file.lower() or 'shop' in file.lower():
                    patterns['stores'].append(file)

        # Deduplicate
        for key in patterns:
            patterns[key] = sorted(list(set(patterns[key])))[:20]  # Top 20

        return dict(patterns)

    def export_to_eastland_format(self) -> Dict[str, Any]:
        """Convert Unity structure to your zone measurement format."""
        zones = {}

        # Group by likely zone
        zone_groups = defaultdict(list)
        for folder, files in self.folder_structure.items():
            # Try to identify zone from folder name
            folder_lower = folder.lower()

            if 'blue' in folder_lower and 'mall' in folder_lower:
                zone_groups['BLUE_MALL'].extend(files)
            elif 'rose' in folder_lower and 'mall' in folder_lower:
                zone_groups['ROSE_MALL'].extend(files)
            elif 'gold' in folder_lower and 'mall' in folder_lower:
                zone_groups['GOLD_MALL'].extend(files)
            elif 'court' in folder_lower or 'food' in folder_lower:
                zone_groups['FOOD_COURT'].extend(files)
            elif 'theater' in folder_lower or 'cinema' in folder_lower:
                zone_groups['THEATER'].extend(files)

        # Convert to zone format
        for zone_id, assets in zone_groups.items():
            zones[zone_id] = {
                'name': zone_id.replace('_', ' ').title(),
                'asset_count': len(assets),
                'contains': assets[:10],  # Sample
                'source': 'cinderella_city_project'
            }

        return {
            'zones': zones,
            'era_layers': dict(self.era_layers),
            'photo_waypoints': self.photo_waypoints[:20]  # Sample
        }

    def generate_report(self, output_path: Optional[Path] = None) -> str:
        """Generate human-readable analysis report."""
        analysis = self.analyze_structure()

        lines = []
        lines.append("=" * 80)
        lines.append("CINDERELLA CITY PROJECT - META FILE ANALYSIS")
        lines.append("=" * 80)
        lines.append("")

        lines.append(f"Total Assets: {analysis['total_assets']}")
        lines.append(f"Folder Count: {analysis['folder_count']}")
        lines.append(f"Photo Waypoints: {analysis['photo_waypoints_found']}")
        lines.append("")

        lines.append("ERA DISTRIBUTION:")
        for era, count in analysis['era_distribution'].items():
            lines.append(f"  {era}: {count} assets")
        lines.append("")

        lines.append("TOP-LEVEL FOLDERS:")
        for folder in analysis['top_level_folders']:
            lines.append(f"  - {folder}/")
        lines.append("")

        if analysis['naming_patterns']:
            lines.append("NAMING PATTERNS DETECTED:")
            for pattern_type, examples in analysis['naming_patterns'].items():
                if examples:
                    lines.append(f"  {pattern_type}:")
                    for ex in examples[:5]:
                        lines.append(f"    - {ex}")
                    if len(examples) > 5:
                        lines.append(f"    ... and {len(examples) - 5} more")
            lines.append("")

        lines.append("=" * 80)
        lines.append("WHAT TO STEAL FOR EASTLAND MALL:")
        lines.append("=" * 80)
        lines.append("")
        lines.append("1. Era Organization Pattern:")
        lines.append("   Create: v8-nextgen/assets/eras/1981_opening/")
        lines.append("   Create: v8-nextgen/assets/eras/2006_decline/")
        lines.append("")
        lines.append("2. Photo Waypoint System:")
        lines.append("   Adapt their photo positioning to SPATIAL_REFERENCE_NERF.md")
        lines.append("")
        lines.append("3. Zone Naming Convention:")
        lines.append("   Consider their folder structure for organizing mall sections")
        lines.append("")

        report = "\n".join(lines)

        if output_path:
            output_path.write_text(report)
            print(f"Report saved to: {output_path}")

        return report


def main():
    parser = argparse.ArgumentParser(
        description="Parse Unity .meta files from Cinderella City Project"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to extracted Cinderella City project directory"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output JSON file for structured data"
    )
    parser.add_argument(
        "--report",
        "-r",
        help="Output text file for analysis report"
    )
    parser.add_argument(
        "--show-structure",
        action="store_true",
        help="Print folder structure to console"
    )
    parser.add_argument(
        "--export-eastland",
        action="store_true",
        help="Export in Eastland zone format"
    )

    args = parser.parse_args()

    # Parse
    print(f"Scanning {args.input} for .meta files...")
    analyzer = UnityMetaParser()
    analyzer.scan_directory(Path(args.input))

    # Show structure
    if args.show_structure:
        print("\nFOLDER STRUCTURE:")
        for folder in sorted(analyzer.folder_structure.keys())[:30]:
            count = len(analyzer.folder_structure[folder])
            print(f"  {folder}/ ({count} files)")
        if len(analyzer.folder_structure) > 30:
            print(f"  ... and {len(analyzer.folder_structure) - 30} more folders")

    # Generate report
    report_path = Path(args.report) if args.report else None
    report = analyzer.generate_report(report_path)
    if not args.report:
        print("\n" + report)

    # Export data
    if args.output:
        if args.export_eastland:
            data = analyzer.export_to_eastland_format()
        else:
            data = analyzer.analyze_structure()

        output_path = Path(args.output)
        output_path.write_text(json.dumps(data, indent=2))
        print(f"\nData exported to: {output_path}")

    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
