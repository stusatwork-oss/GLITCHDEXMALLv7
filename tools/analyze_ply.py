#!/usr/bin/env python3
"""
PLY POINT CLOUD ANALYZER
Analyze Marble-generated PLY files to understand what you got and how to improve.

PLY files from Marble contain:
- Point positions (x, y, z)
- Colors (r, g, b)
- Normals (nx, ny, nz) - sometimes
- Gaussian splat data - sometimes

Usage:
    python3 analyze_ply.py --input eastland_foodcourt.ply
    python3 analyze_ply.py --input *.ply --compare
"""

import struct
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re


class PLYAnalyzer:
    """Analyze PLY point cloud files."""

    def __init__(self, ply_path: Path):
        self.path = ply_path
        self.header = {}
        self.vertex_count = 0
        self.properties = []
        self.bounds = None
        self.has_color = False
        self.has_normals = False
        self.has_splat_data = False

    def parse_header(self) -> Dict:
        """Parse PLY header to understand structure."""
        with open(self.path, 'rb') as f:
            # Read header (ASCII)
            header_lines = []
            while True:
                line = f.readline().decode('ascii').strip()
                header_lines.append(line)
                if line == 'end_header':
                    break

        # Parse header info
        for line in header_lines:
            if line.startswith('element vertex'):
                self.vertex_count = int(line.split()[-1])
            elif line.startswith('property'):
                parts = line.split()
                prop_type = parts[1]
                prop_name = parts[2]
                self.properties.append((prop_name, prop_type))

                # Check for common properties
                if prop_name in ['red', 'green', 'blue', 'r', 'g', 'b']:
                    self.has_color = True
                elif prop_name in ['nx', 'ny', 'nz']:
                    self.has_normals = True
                elif 'scale' in prop_name or 'rotation' in prop_name or 'opacity' in prop_name:
                    self.has_splat_data = True

        return {
            'vertex_count': self.vertex_count,
            'properties': self.properties,
            'has_color': self.has_color,
            'has_normals': self.has_normals,
            'has_splat_data': self.has_splat_data
        }

    def analyze_bounds(self) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        """Calculate bounding box of point cloud."""
        # Simple approach: read all vertices
        # For large files, you might want to sample

        min_x = min_y = min_z = float('inf')
        max_x = max_y = max_z = float('-inf')

        with open(self.path, 'rb') as f:
            # Skip header
            while True:
                line = f.readline().decode('ascii').strip()
                if line == 'end_header':
                    break

            # Read vertices (assuming binary format, little endian, float)
            # This is a simplified parser - real PLY can vary
            try:
                for _ in range(min(self.vertex_count, 10000)):  # Sample first 10k points
                    # Read x, y, z (first 3 floats)
                    x = struct.unpack('f', f.read(4))[0]
                    y = struct.unpack('f', f.read(4))[0]
                    z = struct.unpack('f', f.read(4))[0]

                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
                    min_z = min(min_z, z)
                    max_z = max(max_z, z)

                    # Skip remaining properties
                    bytes_per_prop = 4  # Assuming float
                    remaining_props = len(self.properties) - 3
                    f.read(bytes_per_prop * remaining_props)

            except:
                # If binary parsing fails, we at least got header info
                pass

        self.bounds = ((min_x, min_y, min_z), (max_x, max_y, max_z))
        return self.bounds

    def calculate_dimensions(self) -> Dict[str, float]:
        """Calculate physical dimensions in feet (if scaled properly)."""
        if not self.bounds:
            self.analyze_bounds()

        if self.bounds:
            min_pt, max_pt = self.bounds
            width = max_pt[0] - min_pt[0]
            depth = max_pt[1] - min_pt[1]
            height = max_pt[2] - min_pt[2]

            return {
                'width': width,
                'depth': depth,
                'height': height,
                'diagonal': (width**2 + depth**2 + height**2)**0.5
            }
        return {}

    def generate_report(self) -> str:
        """Generate analysis report."""
        self.parse_header()
        self.analyze_bounds()
        dims = self.calculate_dimensions()

        lines = []
        lines.append("=" * 80)
        lines.append(f"PLY ANALYSIS: {self.path.name}")
        lines.append("=" * 80)
        lines.append("")

        # Basic info
        lines.append("BASIC INFO:")
        lines.append(f"  Point Count: {self.vertex_count:,}")
        lines.append(f"  File Size: {self.path.stat().st_size / 1024 / 1024:.2f} MB")
        lines.append("")

        # Features
        lines.append("FEATURES:")
        lines.append(f"  Has Color: {'✓' if self.has_color else '✗'}")
        lines.append(f"  Has Normals: {'✓' if self.has_normals else '✗'}")
        lines.append(f"  Has Splat Data: {'✓' if self.has_splat_data else '✗'}")
        lines.append("")

        # Properties
        lines.append("PROPERTIES:")
        for prop_name, prop_type in self.properties:
            lines.append(f"  - {prop_name} ({prop_type})")
        lines.append("")

        # Dimensions
        if dims:
            lines.append("DIMENSIONS (units from Marble):")
            lines.append(f"  Width:  {dims['width']:.2f}")
            lines.append(f"  Depth:  {dims['depth']:.2f}")
            lines.append(f"  Height: {dims['height']:.2f}")
            lines.append("")

        # Bounds
        if self.bounds:
            min_pt, max_pt = self.bounds
            lines.append("BOUNDING BOX:")
            lines.append(f"  Min: ({min_pt[0]:.2f}, {min_pt[1]:.2f}, {min_pt[2]:.2f})")
            lines.append(f"  Max: ({max_pt[0]:.2f}, {max_pt[1]:.2f}, {max_pt[2]:.2f})")
            lines.append("")

        # Quality assessment
        lines.append("QUALITY ASSESSMENT:")
        if self.vertex_count < 1000:
            lines.append("  ⚠️  Very low point count - try more detailed prompts")
        elif self.vertex_count < 10000:
            lines.append("  ⚠️  Low point count - could be more detailed")
        elif self.vertex_count < 100000:
            lines.append("  ✓ Moderate point count - decent quality")
        else:
            lines.append("  ✓✓ High point count - good quality")

        if not self.has_color:
            lines.append("  ⚠️  No color data - might be grayscale")
        if not self.has_normals:
            lines.append("  ℹ️  No normals - expected for Gaussian splats")

        lines.append("")

        # Suggestions
        lines.append("SUGGESTIONS FOR NEXT ITERATION:")
        if self.vertex_count < 50000:
            lines.append("  - Add more detail to your prompt")
            lines.append("  - Specify materials and textures explicitly")
            lines.append("  - Mention lighting conditions")

        if dims:
            # Compare to expected Eastland dimensions
            lines.append("")
            lines.append("SCALE CHECK (vs Eastland measurements):")
            if 'food_court' in self.path.name.lower():
                expected_diameter = 120  # feet
                actual = max(dims['width'], dims['depth'])
                ratio = actual / expected_diameter if expected_diameter > 0 else 0
                lines.append(f"  Expected diameter: ~120 feet")
                lines.append(f"  Actual max dimension: {actual:.2f}")
                if ratio > 0:
                    lines.append(f"  Scale ratio: {ratio:.2f}x")
                    if ratio < 0.8 or ratio > 1.2:
                        lines.append(f"  ⚠️  Scale mismatch - consider adding size hints to prompt")

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze PLY point cloud files from Marble"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        nargs='+',
        help="PLY file(s) to analyze"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Save report to file"
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare multiple PLY files"
    )

    args = parser.parse_args()

    # Analyze files
    analyses = []
    for ply_file in args.input:
        path = Path(ply_file)
        if not path.exists():
            print(f"❌ File not found: {path}")
            continue

        print(f"\nAnalyzing {path.name}...")
        analyzer = PLYAnalyzer(path)
        report = analyzer.generate_report()
        analyses.append((path, analyzer, report))

        if not args.compare:
            print(report)

    # Comparison mode
    if args.compare and len(analyses) > 1:
        print("\n" + "=" * 80)
        print("COMPARISON")
        print("=" * 80)
        print("")
        print(f"{'File':<40} {'Points':>12} {'Size (MB)':>12} {'Color':>8}")
        print("-" * 80)
        for path, analyzer, _ in analyses:
            color_status = '✓' if analyzer.has_color else '✗'
            size_mb = path.stat().st_size / 1024 / 1024
            print(f"{path.name:<40} {analyzer.vertex_count:>12,} {size_mb:>12.2f} {color_status:>8}")

    # Save output
    if args.output:
        output_path = Path(args.output)
        combined_report = "\n\n".join(report for _, _, report in analyses)
        output_path.write_text(combined_report)
        print(f"\n✅ Report saved to {output_path}")


if __name__ == "__main__":
    main()
