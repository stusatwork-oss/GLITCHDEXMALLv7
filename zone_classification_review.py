#!/usr/bin/env python3
"""
ZONE CLASSIFICATION REVIEW SYSTEM v1.0
Eastland Mall Reconstruction - NeRF/Dream Machine Pipeline Prep

PURPOSE:
Organize 248 reference images for Luma/NeRFstudio processing
Generate priority lists and coverage analysis for Dream Machine gap-filling

WORKFLOW:
1. Scan existing zone classifications
2. Analyze architectural features (scale, structure, coverage)
3. Generate NeRF-ready folder structure
4. Output manifests, priorities, and coverage gaps
5. Create coordination breadcrumbs for multi-AI workflow

SCALE REFERENCE (Industry Standard Escalators):
- Riser height: 8 inches
- Tread depth: 15-16 inches
- Width variants: 24", 32", 40"
- Standard 3-story mall escalator: ~30-35 feet vertical (45-52 risers)

CIVIC-SCALE INDICATORS:
- Ceiling heights >40ft
- Tensile roof sails (100+ ft clear spans)
- Dome structures
- Multiple escalator banks in frame
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import hashlib

# ============================================================================
# CONFIGURATION
# ============================================================================

# Input paths
ZONES_BASE = Path(r"C:\Users\stusa\Documents\GitHub\glitchLFS1121origin\v6-nextgen\assets\photos\zones")

# Output paths
LUMA_INPUT_BASE = Path(r"C:\Users\stusa\Documents\GitHub\glitchLFS1121origin\v6-nextgen\luma_input")
COORDINATION_BASE = Path(r"C:\Users\stusa\Documents\GitHub\glitchLFS1121origin\v6-nextgen\COORDINATION")

# Zone definitions with narrative importance
ZONE_CONFIG = {
    "escalators": {
        "display_name": "ESCALATOR_PIT",
        "qbit_weight": 0.88,
        "narrative_importance": "critical_vertical_transition",
        "dreamweight": "liminal_high"
    },
    "food_court": {
        "display_name": "SUNKEN_FOOD_COURT",
        "qbit_weight": 0.82,
        "narrative_importance": "cloud_prime_node",
        "dreamweight": "atmospheric_medium"
    },
    "atrium": {
        "display_name": "ATRIUM_MAST",
        "qbit_weight": 0.75,
        "narrative_importance": "civic_anchor",
        "dreamweight": "structural_high"
    },
    "movie_mouth": {
        "display_name": "CINEMA_ENTRANCE",
        "qbit_weight": 0.70,
        "narrative_importance": "threshold_space",
        "dreamweight": "liminal_medium"
    },
    "comphut": {
        "display_name": "COMPHUT",
        "qbit_weight": 0.65,
        "narrative_importance": "tech_artifact",
        "dreamweight": "nostalgic_high"
    },
    "maintenance": {
        "display_name": "SERVICE_HALL",
        "qbit_weight": 0.60,
        "narrative_importance": "backrooms_access",
        "dreamweight": "surreal_high"
    },
    "exterior": {
        "display_name": "EXTERIOR_DOME",
        "qbit_weight": 0.55,
        "narrative_importance": "context_reference",
        "dreamweight": "architectural_low"
    },
    "Unknown": {
        "display_name": "UNCLASSIFIED",
        "qbit_weight": 0.30,
        "narrative_importance": "needs_review",
        "dreamweight": "undefined"
    }
}

# Architectural feature keywords for detection
STRUCTURAL_KEYWORDS = [
    "exposed", "ceiling", "beam", "column", "truss", "duct", "mechanical",
    "roof", "sail", "tension", "cable", "structure", "frame", "bones"
]

CIVIC_SCALE_KEYWORDS = [
    "atrium", "dome", "mast", "multiple_levels", "escalator_banks",
    "grand", "vast", "volume", "height"
]

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_file_hash(filepath):
    """Generate MD5 hash for duplicate detection"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def analyze_filename_hints(filename):
    """Extract hints from filename about content"""
    lower_name = filename.lower()
    hints = {
        "structural_bones": any(kw in lower_name for kw in STRUCTURAL_KEYWORDS),
        "civic_scale": any(kw in lower_name for kw in CIVIC_SCALE_KEYWORDS),
        "escalator_visible": "escalat" in lower_name or "escal" in lower_name,
        "remodel_shot": "remodel" in lower_name or "construction" in lower_name
    }
    return hints

def estimate_coverage_quality(image_count, zone_config):
    """Estimate NeRF coverage quality based on image count and zone importance"""
    # Baseline: 20+ images = good coverage
    # Adjust based on zone complexity and importance
    
    base_coverage = min(image_count / 20.0, 1.0)  # Cap at 1.0
    
    # Bonus for high narrative importance
    importance_bonus = zone_config.get("qbit_weight", 0.5) * 0.2
    
    # Penalty if too few images
    if image_count < 5:
        base_coverage *= 0.3
    elif image_count < 10:
        base_coverage *= 0.6
    
    final_coverage = min(base_coverage + importance_bonus, 1.0)
    return round(final_coverage, 2)

def calculate_priority_score(zone_name, image_count, structural_count, zone_config):
    """Calculate priority score for NeRF processing order"""
    
    # Base factors
    qbit_weight = zone_config.get("qbit_weight", 0.5)
    coverage_factor = min(image_count / 20.0, 1.0)
    structural_bonus = min(structural_count / 5.0, 0.2)  # Up to 20% bonus
    
    # Penalty for insufficient data
    if image_count < 5:
        coverage_factor *= 0.3
    
    # Combine factors
    priority = (qbit_weight * 0.5) + (coverage_factor * 0.3) + (structural_bonus * 0.2)
    
    return round(priority, 3)

def generate_dream_machine_needs(image_count, coverage_estimate, zone_name):
    """Identify what needs Dream Machine generation"""
    needs = []
    
    if coverage_estimate < 0.3:
        needs.append("entire zone passthrough sequence")
        needs.append("establishing shots from multiple angles")
    elif coverage_estimate < 0.6:
        needs.append("ceiling detail shots")
        needs.append("corner and transition areas")
        needs.append("supplemental atmospheric passes")
    elif coverage_estimate < 0.8:
        needs.append("minor gap filling")
        needs.append("detail enhancements")
    else:
        needs.append("optional atmospheric enhancement only")
    
    # Zone-specific needs
    if "escalator" in zone_name.lower():
        needs.append("upper landing detail")
        needs.append("handrail and step closeups")
    elif "food_court" in zone_name.lower():
        needs.append("seating area coverage")
        needs.append("storefront details")
    elif "atrium" in zone_name.lower():
        needs.append("tensile sail connection points")
        needs.append("full vertical sweep")
    
    return needs

# ============================================================================
# MAIN PROCESSING
# ============================================================================

def scan_existing_zones():
    """Scan current zone folders and catalog images"""
    print("=" * 80)
    print("ZONE CLASSIFICATION REVIEW SYSTEM v1.0")
    print("Eastland Mall Reconstruction - NeRF Pipeline Prep")
    print("=" * 80)
    print()
    
    if not ZONES_BASE.exists():
        print(f"ERROR: Zones directory not found: {ZONES_BASE}")
        print("Please verify the path in the script configuration.")
        return None
    
    zone_data = {}
    total_images = 0
    
    print("Scanning existing zones...")
    print()
    
    for zone_folder in ZONES_BASE.iterdir():
        if not zone_folder.is_dir():
            continue
            
        zone_name = zone_folder.name
        if zone_name not in ZONE_CONFIG:
            print(f"WARNING: Unknown zone folder '{zone_name}' - skipping")
            continue
        
        zone_config = ZONE_CONFIG[zone_name]
        
        # Collect image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        images = [f for f in zone_folder.iterdir() 
                 if f.suffix.lower() in image_extensions]
        
        # Analyze images
        structural_images = []
        civic_scale_images = []
        hashes = set()
        duplicates = 0
        
        for img in images:
            # Check for duplicates
            img_hash = get_file_hash(img)
            if img_hash in hashes:
                duplicates += 1
                continue
            hashes.add(img_hash)
            
            # Analyze filename
            hints = analyze_filename_hints(img.name)
            if hints["structural_bones"]:
                structural_images.append(img.name)
            if hints["civic_scale"]:
                civic_scale_images.append(img.name)
        
        unique_images = len(images) - duplicates
        total_images += unique_images
        
        # Store analysis
        zone_data[zone_name] = {
            "config": zone_config,
            "images": [img.name for img in images if get_file_hash(img) in hashes],
            "count": unique_images,
            "duplicates": duplicates,
            "structural_images": structural_images,
            "civic_scale_images": civic_scale_images,
            "source_path": str(zone_folder)
        }
        
        # Print summary
        print(f"📁 {zone_config['display_name']}")
        print(f"   Images: {unique_images} ({duplicates} duplicates removed)")
        print(f"   Structural shots: {len(structural_images)}")
        print(f"   Civic-scale indicators: {len(civic_scale_images)}")
        print(f"   QBIT Weight: {zone_config['qbit_weight']}")
        print()
    
    print(f"Total unique images scanned: {total_images}")
    print()
    
    return zone_data

def generate_luma_structure(zone_data):
    """Generate Luma/NeRFstudio folder structure"""
    print("=" * 80)
    print("GENERATING LUMA/NERFSTUDIO FOLDER STRUCTURE")
    print("=" * 80)
    print()
    
    # Create base directory
    LUMA_INPUT_BASE.mkdir(parents=True, exist_ok=True)
    
    zone_manifests = {}
    
    for zone_name, data in zone_data.items():
        display_name = data["config"]["display_name"]
        zone_output = LUMA_INPUT_BASE / display_name
        zone_output.mkdir(exist_ok=True)
        
        # Copy images
        copied_count = 0
        for img_name in data["images"]:
            src = Path(data["source_path"]) / img_name
            dst = zone_output / img_name
            if src.exists():
                shutil.copy2(src, dst)
                copied_count += 1
        
        # Calculate metrics
        coverage = estimate_coverage_quality(data["count"], data["config"])
        priority = calculate_priority_score(
            zone_name,
            data["count"],
            len(data["structural_images"]),
            data["config"]
        )
        
        # Generate manifest
        zone_manifests[display_name] = {
            "frames": data["images"],
            "frame_count": copied_count,
            "priority_score": priority,
            "coverage_estimate": coverage,
            "qbit_weight": data["config"]["qbit_weight"],
            "narrative_importance": data["config"]["narrative_importance"],
            "dreamweight": data["config"]["dreamweight"],
            "structural_frames": len(data["structural_images"]),
            "source_zone": zone_name
        }
        
        print(f"✅ {display_name}")
        print(f"   Copied: {copied_count} images")
        print(f"   Coverage: {coverage:.2f}")
        print(f"   Priority: {priority:.3f}")
        print()
    
    # Write global manifest
    manifest_path = LUMA_INPUT_BASE / "zone_manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(zone_manifests, f, indent=2)
    
    print(f"📄 Global manifest written: {manifest_path}")
    print()
    
    return zone_manifests

def generate_priority_list(zone_manifests):
    """Generate priority-ordered list for NeRF processing"""
    print("=" * 80)
    print("GENERATING PRIORITY LIST")
    print("=" * 80)
    print()
    
    # Sort by priority score
    sorted_zones = sorted(
        zone_manifests.items(),
        key=lambda x: x[1]["priority_score"],
        reverse=True
    )
    
    priority_list = []
    
    for rank, (zone_name, data) in enumerate(sorted_zones, 1):
        # Generate reason
        reasons = []
        
        if data["narrative_importance"] in ["critical_vertical_transition", "cloud_prime_node"]:
            reasons.append("Critical narrative importance")
        
        if data["qbit_weight"] > 0.8:
            reasons.append("High QBIT influence")
        
        if data["coverage_estimate"] > 0.7:
            reasons.append("Good coverage for NeRF")
        
        if data["structural_frames"] > 3:
            reasons.append("Strong structural documentation")
        
        if data["frame_count"] < 5:
            reasons.append("LIMITED DATA - may need Dream Machine support")
        
        priority_entry = {
            "rank": rank,
            "zone": zone_name,
            "priority_score": data["priority_score"],
            "reason": ", ".join(reasons) if reasons else "Standard processing",
            "frame_count": data["frame_count"],
            "coverage_estimate": data["coverage_estimate"],
            "recommended_action": "NeRF FIRST" if data["coverage_estimate"] > 0.6 else "Dream Machine PRIMARY"
        }
        
        priority_list.append(priority_entry)
        
        # Print summary
        emoji = "🔥" if rank <= 3 else "⚡" if rank <= 5 else "📍"
        print(f"{emoji} #{rank} {zone_name}")
        print(f"   Score: {data['priority_score']:.3f}")
        print(f"   Coverage: {data['coverage_estimate']:.2f}")
        print(f"   Action: {priority_entry['recommended_action']}")
        print(f"   Reason: {priority_entry['reason']}")
        print()
    
    # Write priority list
    COORDINATION_BASE.mkdir(parents=True, exist_ok=True)
    priority_path = LUMA_INPUT_BASE / "priority_list.json"
    with open(priority_path, 'w') as f:
        json.dump({"zone_priorities": priority_list}, f, indent=2)
    
    print(f"📄 Priority list written: {priority_path}")
    print()
    
    return priority_list

def generate_coverage_gaps(zone_manifests):
    """Generate coverage gap analysis for Dream Machine"""
    print("=" * 80)
    print("GENERATING COVERAGE GAP ANALYSIS")
    print("=" * 80)
    print()
    
    coverage_gaps = {"zones": {}}
    
    for zone_name, data in zone_manifests.items():
        dream_needs = generate_dream_machine_needs(
            data["frame_count"],
            data["coverage_estimate"],
            zone_name
        )
        
        gap_entry = {
            "frames": data["frame_count"],
            "coverage_estimate": data["coverage_estimate"],
            "needs_dream_machine": dream_needs,
            "dreamweight": data["dreamweight"],
            "structural_documentation": "GOOD" if data["structural_frames"] > 3 else "LIMITED"
        }
        
        coverage_gaps["zones"][zone_name] = gap_entry
        
        # Print summary
        status = "🟢" if data["coverage_estimate"] > 0.7 else "🟡" if data["coverage_estimate"] > 0.4 else "🔴"
        print(f"{status} {zone_name}")
        print(f"   Coverage: {data['coverage_estimate']:.2f}")
        print(f"   Frames: {data['frame_count']}")
        print(f"   Dream Machine needs:")
        for need in dream_needs:
            print(f"      • {need}")
        print()
    
    # Write coverage gaps
    gaps_path = LUMA_INPUT_BASE / "coverage_gaps.json"
    with open(gaps_path, 'w') as f:
        json.dump(coverage_gaps, f, indent=2)
    
    print(f"📄 Coverage gaps written: {gaps_path}")
    print()
    
    return coverage_gaps

def generate_coordination_report(zone_data, zone_manifests, priority_list, coverage_gaps):
    """Generate markdown report for multi-AI coordination"""
    print("=" * 80)
    print("GENERATING COORDINATION REPORT")
    print("=" * 80)
    print()
    
    COORDINATION_BASE.mkdir(parents=True, exist_ok=True)
    report_path = COORDINATION_BASE / "ZONE_CLASSIFICATION_REPORT.md"
    
    with open(report_path, 'w') as f:
        f.write("# ZONE CLASSIFICATION REPORT\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Images Processed:** {sum(d['count'] for d in zone_data.values())}\n\n")
        f.write("---\n\n")
        
        # Executive Summary
        f.write("## EXECUTIVE SUMMARY\n\n")
        f.write("Zone classification complete. Assets organized for Luma/NeRFstudio pipeline.\n\n")
        
        ready_zones = sum(1 for z in zone_manifests.values() if z["coverage_estimate"] > 0.6)
        partial_zones = sum(1 for z in zone_manifests.values() if 0.3 < z["coverage_estimate"] <= 0.6)
        insufficient_zones = sum(1 for z in zone_manifests.values() if z["coverage_estimate"] <= 0.3)
        
        f.write(f"- **NeRF-READY ZONES:** {ready_zones}\n")
        f.write(f"- **PARTIAL COVERAGE:** {partial_zones}\n")
        f.write(f"- **DREAM MACHINE PRIMARY:** {insufficient_zones}\n\n")
        
        f.write("---\n\n")
        
        # Priority Processing Order
        f.write("## PRIORITY PROCESSING ORDER\n\n")
        f.write("Process zones in this order for optimal NeRF reconstruction:\n\n")
        
        for entry in priority_list[:5]:  # Top 5
            f.write(f"### {entry['rank']}. {entry['zone']}\n")
            f.write(f"- **Priority Score:** {entry['priority_score']:.3f}\n")
            f.write(f"- **Coverage:** {entry['coverage_estimate']:.2f}\n")
            f.write(f"- **Action:** {entry['recommended_action']}\n")
            f.write(f"- **Reason:** {entry['reason']}\n\n")
        
        f.write("---\n\n")
        
        # Coverage Gaps
        f.write("## DREAM MACHINE GAP-FILLING NEEDS\n\n")
        
        for zone_name, gap_data in coverage_gaps["zones"].items():
            if gap_data["coverage_estimate"] < 0.7:
                f.write(f"### {zone_name}\n")
                f.write(f"- **Coverage:** {gap_data['coverage_estimate']:.2f}\n")
                f.write(f"- **Dreamweight:** {gap_data['dreamweight']}\n")
                f.write("- **Needs:**\n")
                for need in gap_data["needs_dream_machine"]:
                    f.write(f"  - {need}\n")
                f.write("\n")
        
        f.write("---\n\n")
        
        # File Locations
        f.write("## OUTPUT FILES\n\n")
        f.write(f"- **Luma Input:** `{LUMA_INPUT_BASE}`\n")
        f.write(f"- **Zone Manifest:** `{LUMA_INPUT_BASE / 'zone_manifest.json'}`\n")
        f.write(f"- **Priority List:** `{LUMA_INPUT_BASE / 'priority_list.json'}`\n")
        f.write(f"- **Coverage Gaps:** `{LUMA_INPUT_BASE / 'coverage_gaps.json'}`\n\n")
        
        f.write("---\n\n")
        
        # Next Steps
        f.write("## NEXT STEPS\n\n")
        f.write("1. **Process top 3 priority zones in Luma/NeRFstudio first**\n")
        f.write("2. **Use Dream Machine for zones with coverage <0.6**\n")
        f.write("3. **Focus on structural 'bones' shots for accuracy**\n")
        f.write("4. **Generate connective sequences between zones**\n\n")
        
        f.write("---\n\n")
        f.write("*Report generated by zone_classification_review.py*\n")
    
    print(f"📄 Coordination report written: {report_path}")
    print()
    
    return report_path

def main():
    """Main execution flow"""
    try:
        # Step 1: Scan existing zones
        zone_data = scan_existing_zones()
        if zone_data is None:
            return
        
        # Step 2: Generate Luma structure
        zone_manifests = generate_luma_structure(zone_data)
        
        # Step 3: Generate priority list
        priority_list = generate_priority_list(zone_manifests)
        
        # Step 4: Generate coverage gaps
        coverage_gaps = generate_coverage_gaps(zone_manifests)
        
        # Step 5: Generate coordination report
        report_path = generate_coordination_report(
            zone_data, zone_manifests, priority_list, coverage_gaps
        )
        
        # Final summary
        print("=" * 80)
        print("✅ ZONE CLASSIFICATION COMPLETE")
        print("=" * 80)
        print()
        print(f"📁 Luma input ready: {LUMA_INPUT_BASE}")
        print(f"📄 Coordination report: {report_path}")
        print()
        print("NEXT: Upload priority zones to Luma AI for NeRF processing")
        print()
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
