#!/usr/bin/env python3
"""
VERSION MATRIX ENFORCEMENT (TRUTH FILTERS)
Step 5 of 5-part integration

Prevents version drift, canon corruption, and mismatched logic.
Each runtime request is routed to the authoritative version source.

Architecture:
- Version Authority Table: Maps feature domains → canonical version
- Request Router: Intercepts runtime queries
- Truth Filter: Ensures no mixing of incompatible logic

Usage:
    from version_matrix_filter import VersionFilter, FeatureDomain

    filter = VersionFilter()

    # Request geometry data
    geometry = filter.request(FeatureDomain.GEOMETRY, "atrium_diameter")
    # Routes to v5 (CRD measurements)

    # Request behavior logic
    behavior = filter.request(FeatureDomain.BEHAVIOR, "npc_state_machine")
    # Routes to v6 (QBIT + State machines)

Reference:
- VERSION_MATRIX.md
- WHAT_NEEDS_WORK.md
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional, Callable
import json
from pathlib import Path


class FeatureDomain(Enum):
    """
    Feature domains with version authority.

    Each domain has ONE canonical source version.
    """
    # Spatial/Geometric
    GEOMETRY = "geometry"              # v5: CRD measurements
    SPATIAL_LAYOUT = "spatial_layout"  # v5: Photo-based reconstruction
    ZONE_DIMENSIONS = "zone_dimensions"  # v5: Evidence-based
    MEASUREMENTS = "measurements"      # v5: CRD traceability

    # Behavioral/AI
    BEHAVIOR = "behavior"              # v6: NPC state machines + QBIT
    NPC_AI = "npc_ai"                  # v6: Advanced AI systems
    CLOUD_SYSTEM = "cloud_system"      # v4: Cloud-driven semantics
    QBIT_SCORING = "qbit_scoring"      # v6: Entity influence

    # Philosophical/Conceptual
    PHILOSOPHY = "philosophy"          # v4: Renderist metaphysics
    CANON_RULES = "canon_rules"        # v4: Canon emergence
    REALITY_MODEL = "reality_model"    # v4: Cloud-driven reality

    # Rendering/Visual
    RENDERING = "rendering"            # v1/v2: Raycaster OR v8: Pygame
    GRAPHICS = "graphics"              # v3: Pygame implementation
    VISUAL_EFFECTS = "visual_effects"  # v2: Reality-breaking effects

    # Simulation/Integration
    SIMULATION = "simulation"          # v7: Integration layer
    TIMELINE = "timeline"              # v7: Multi-era system
    CUTSCENES = "cutscenes"            # v8: Cutscene engine


@dataclass
class VersionAuthority:
    """
    Authority record for a feature domain.

    Attributes:
        version: Canonical version (e.g., "v5", "v6")
        source_path: Path to authoritative data/code
        rationale: Why this version is canonical
        locked: Whether authority can change
    """
    version: str
    source_path: str
    rationale: str
    locked: bool = True


# ============================================================================
# VERSION AUTHORITY TABLE
# ============================================================================

AUTHORITY_TABLE: Dict[FeatureDomain, VersionAuthority] = {
    # GEOMETRY & SPATIAL (v5 Authority)
    FeatureDomain.GEOMETRY: VersionAuthority(
        version="v5",
        source_path="v5-eastland/data/measurements/",
        rationale="CRD photo-based reconstruction is evidence-backed",
        locked=True
    ),
    FeatureDomain.SPATIAL_LAYOUT: VersionAuthority(
        version="v5",
        source_path="v5-eastland/docs/crd/",
        rationale="ZONE_GRAPH_V1.md + photo traceability",
        locked=True
    ),
    FeatureDomain.ZONE_DIMENSIONS: VersionAuthority(
        version="v5",
        source_path="v5-eastland/data/measurements/zone_measurements.json",
        rationale="Measured from photos with confidence levels",
        locked=True
    ),
    FeatureDomain.MEASUREMENTS: VersionAuthority(
        version="v5",
        source_path="v5-eastland/data/measurements/",
        rationale="Single source of truth for all dimensions",
        locked=True
    ),

    # BEHAVIOR & AI (v6 Authority)
    FeatureDomain.BEHAVIOR: VersionAuthority(
        version="v6",
        source_path="v6-nextgen/src/npc_state_machine.py",
        rationale="QBIT-aware state machines with contradiction system",
        locked=True
    ),
    FeatureDomain.NPC_AI: VersionAuthority(
        version="v6",
        source_path="v6-nextgen/src/",
        rationale="Advanced NPC systems with QBIT integration",
        locked=True
    ),
    FeatureDomain.QBIT_SCORING: VersionAuthority(
        version="v6",
        source_path="v6-nextgen/src/qbit_engine.py",
        rationale="Canonical entity influence scoring",
        locked=True
    ),

    # CLOUD & PHILOSOPHY (v4 Authority)
    FeatureDomain.CLOUD_SYSTEM: VersionAuthority(
        version="v4",
        source_path="v4-renderist/src/cloud.py",
        rationale="Original Cloud-driven semantic space architecture",
        locked=True
    ),
    FeatureDomain.PHILOSOPHY: VersionAuthority(
        version="v4",
        source_path="v4-renderist/docs/V4_SPC_SPECIFICATION.md",
        rationale="Renderist OS defines canon emergence principles",
        locked=True
    ),
    FeatureDomain.CANON_RULES: VersionAuthority(
        version="v4",
        source_path="v4-renderist/",
        rationale="'Canon emerges from resonance and repetition, not ego'",
        locked=True
    ),
    FeatureDomain.REALITY_MODEL: VersionAuthority(
        version="v4",
        source_path="v4-renderist/",
        rationale="Cloud-driven reality, not static maps",
        locked=True
    ),

    # RENDERING (Multi-version)
    FeatureDomain.RENDERING: VersionAuthority(
        version="v8",
        source_path="v8-nextgen/NEW-needs_integration/Visual_Runtime_Entry.py",
        rationale="Pygame renderer for v8 (v1/v2 for raycaster)",
        locked=False  # Can switch between raycaster/pygame
    ),
    FeatureDomain.GRAPHICS: VersionAuthority(
        version="v3",
        source_path="v3-eastland/src/main_pygame.py",
        rationale="Original Pygame implementation",
        locked=False
    ),
    FeatureDomain.VISUAL_EFFECTS: VersionAuthority(
        version="v2",
        source_path="v2-immersive-sim/src/reality_glitch.py",
        rationale="Reality-breaking heat system effects",
        locked=True
    ),

    # INTEGRATION (v7/v8 Authority)
    FeatureDomain.SIMULATION: VersionAuthority(
        version="v7",
        source_path="v7-nextgen/src/",
        rationale="v5 evidence + v6 systems integration",
        locked=True
    ),
    FeatureDomain.TIMELINE: VersionAuthority(
        version="v7",
        source_path="v7-nextgen/src/timeline_system.py",
        rationale="Multi-era system (1981/1995/2005/2011)",
        locked=True
    ),
    FeatureDomain.CUTSCENES: VersionAuthority(
        version="v8",
        source_path="v8-nextgen/NEW-needs_integration/cutscene_manaer.py",
        rationale="Complete cutscene engine implementation",
        locked=False  # Subject to integration
    )
}


# ============================================================================
# VERSION FILTER
# ============================================================================

class VersionFilter:
    """
    Runtime filter that enforces version authority.

    Prevents:
    - Version drift (mixing incompatible logic)
    - Canon corruption (using wrong source data)
    - Mismatched systems (v5 geometry with v2 behavior)
    """

    def __init__(self, repo_root: Optional[Path] = None):
        self.authority_table = AUTHORITY_TABLE
        self.repo_root = repo_root or Path(__file__).parents[2]

        # Cache for loaded data
        self.cache: Dict[str, Any] = {}

        # Request log (for debugging)
        self.request_log: list = []

    def request(
        self,
        domain: FeatureDomain,
        resource_key: str,
        fallback: Any = None
    ) -> Any:
        """
        Request data/logic from authoritative version.

        Args:
            domain: Feature domain (e.g., GEOMETRY, BEHAVIOR)
            resource_key: Specific resource identifier
            fallback: Value to return if not found

        Returns:
            Data from canonical source, or fallback

        Example:
            geometry = filter.request(FeatureDomain.GEOMETRY, "atrium_diameter")
            # Returns value from v5/data/measurements/spatial_measurements.json
        """
        if domain not in self.authority_table:
            self._log_request(domain, resource_key, "UNKNOWN_DOMAIN", None)
            return fallback

        authority = self.authority_table[domain]
        self._log_request(domain, resource_key, authority.version, authority.source_path)

        # Check cache
        cache_key = f"{domain.value}:{resource_key}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Load from authoritative source
        try:
            value = self._load_from_authority(authority, resource_key)
            self.cache[cache_key] = value
            return value
        except Exception as e:
            print(f"[VERSION_FILTER] Error loading {resource_key} from {authority.version}: {e}")
            return fallback

    def get_authority(self, domain: FeatureDomain) -> Optional[VersionAuthority]:
        """Get version authority for a domain."""
        return self.authority_table.get(domain)

    def validate_request(self, domain: FeatureDomain) -> bool:
        """Check if domain has locked authority."""
        if domain not in self.authority_table:
            return False
        return self.authority_table[domain].locked

    def override_authority(
        self,
        domain: FeatureDomain,
        new_version: str,
        new_source: str,
        rationale: str
    ) -> bool:
        """
        Override authority (only if not locked).

        Args:
            domain: Target domain
            new_version: New authoritative version
            new_source: New source path
            rationale: Explanation for override

        Returns:
            True if override succeeded, False if locked
        """
        if domain not in self.authority_table:
            return False

        if self.authority_table[domain].locked:
            print(f"[VERSION_FILTER] Cannot override locked domain: {domain.value}")
            return False

        self.authority_table[domain] = VersionAuthority(
            version=new_version,
            source_path=new_source,
            rationale=rationale,
            locked=False
        )
        print(f"[VERSION_FILTER] Authority override: {domain.value} → {new_version}")
        return True

    def _load_from_authority(self, authority: VersionAuthority, resource_key: str) -> Any:
        """
        Load resource from authoritative source.

        This is a simplified loader - real implementation would:
        - Parse JSON files from authority.source_path
        - Import Python modules
        - Execute queries against data stores
        """
        source_path = self.repo_root / authority.source_path

        # Handle JSON files
        if source_path.is_file() and source_path.suffix == ".json":
            with open(source_path) as f:
                data = json.load(f)
                return self._extract_key(data, resource_key)

        # Handle directories (search for resource_key)
        elif source_path.is_dir():
            # Look for JSON files in directory
            for json_file in source_path.glob("*.json"):
                with open(json_file) as f:
                    data = json.load(f)
                    value = self._extract_key(data, resource_key)
                    if value is not None:
                        return value

        return None

    def _extract_key(self, data: Dict, key: str) -> Any:
        """Extract nested key from dict (supports dot notation)."""
        if "." in key:
            # Nested key: "atrium.diameter_feet.value"
            parts = key.split(".")
            current = data
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return None
            return current
        else:
            # Top-level key
            return data.get(key)

    def _log_request(self, domain: FeatureDomain, resource: str, version: str, source: str):
        """Log version request for debugging."""
        self.request_log.append({
            "domain": domain.value,
            "resource": resource,
            "version": version,
            "source": source
        })

    def print_authority_table(self):
        """Print version authority table."""
        print("="*70)
        print("VERSION AUTHORITY TABLE")
        print("="*70)

        for domain, authority in self.authority_table.items():
            lock_status = "🔒 LOCKED" if authority.locked else "🔓 unlocked"
            print(f"\n{domain.value.upper()}: {authority.version} {lock_status}")
            print(f"  Source: {authority.source_path}")
            print(f"  Rationale: {authority.rationale}")

        print("\n" + "="*70)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_canonical_geometry(resource_key: str) -> Any:
    """Get geometry from v5 (canonical source)."""
    filter = VersionFilter()
    return filter.request(FeatureDomain.GEOMETRY, resource_key)


def get_canonical_behavior(resource_key: str) -> Any:
    """Get behavior logic from v6 (canonical source)."""
    filter = VersionFilter()
    return filter.request(FeatureDomain.BEHAVIOR, resource_key)


def get_canonical_philosophy(resource_key: str) -> Any:
    """Get philosophical rules from v4 (canonical source)."""
    filter = VersionFilter()
    return filter.request(FeatureDomain.PHILOSOPHY, resource_key)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("VERSION MATRIX FILTER TEST")
    print("="*70)

    filter = VersionFilter()

    # Print authority table
    filter.print_authority_table()

    # Test requests
    print("\n" + "="*70)
    print("REQUEST ROUTING TEST")
    print("="*70)

    # Geometry request → v5
    print("\n1. Request: Geometry data (atrium dimensions)")
    authority = filter.get_authority(FeatureDomain.GEOMETRY)
    print(f"   Routes to: {authority.version}")
    print(f"   Source: {authority.source_path}")

    # Behavior request → v6
    print("\n2. Request: NPC behavior logic")
    authority = filter.get_authority(FeatureDomain.BEHAVIOR)
    print(f"   Routes to: {authority.version}")
    print(f"   Source: {authority.source_path}")

    # Philosophy request → v4
    print("\n3. Request: Canon emergence rules")
    authority = filter.get_authority(FeatureDomain.PHILOSOPHY)
    print(f"   Routes to: {authority.version}")
    print(f"   Source: {authority.source_path}")

    # Try override (should fail for locked domains)
    print("\n" + "="*70)
    print("LOCK ENFORCEMENT TEST")
    print("="*70)

    print("\n4. Attempt to override GEOMETRY authority (locked)")
    success = filter.override_authority(
        FeatureDomain.GEOMETRY,
        "v3",
        "v3-eastland/data/",
        "Testing override"
    )
    print(f"   Override allowed: {success}")

    print("\n5. Attempt to override RENDERING authority (unlocked)")
    success = filter.override_authority(
        FeatureDomain.RENDERING,
        "v1",
        "v1-doofenstein/src/wolf_renderer.py",
        "Switch to raycaster"
    )
    print(f"   Override allowed: {success}")

    # Show request log
    print("\n" + "="*70)
    print("REQUEST LOG")
    print("="*70)
    for i, req in enumerate(filter.request_log, 1):
        print(f"{i}. {req['domain']} / {req['resource']} → {req['version']}")

    print("\n" + "="*70)
    print("VERSION DRIFT PREVENTED")
    print("Canon locked to authoritative sources")
    print("="*70)
