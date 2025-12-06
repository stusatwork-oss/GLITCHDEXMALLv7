#!/usr/bin/env python3
"""
QBIT Topology Debug Tools - V6

Real-time monitoring and logging of QBIT-weighted zone topology.

Features:
- Snapshot topology state (zones, adjacency, Cloud level)
- Human-readable console output
- ASCII adjacency matrix visualization
- JSONL logging for analysis
- Integration with main game loop

Usage:
    from topology_debug import (
        build_topology_snapshot,
        print_topology_summary,
        print_adjacency_matrix_ascii,
        log_topology_snapshot_json
    )

    # In main loop (every N seconds):
    snapshot = build_topology_snapshot(zones, adjacency, cloud)
    print_topology_summary(snapshot)
    log_topology_snapshot_json(snapshot, log_file)
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
import json
import time


@dataclass
class ZoneDebugState:
    """Debug state for a single zone."""
    zone_id: str
    qbit_score: float
    resonance: float
    turbulence: float
    top_neighbors: List[Tuple[str, float]]  # (zone_id, probability)


@dataclass
class TopologySnapshot:
    """Complete topology snapshot at a point in time."""
    timestamp: float
    cloud_level: float
    cloud_mood: str
    bleed_tier: int
    zones: List[ZoneDebugState]


def _get_top_neighbors(
    zone_id: str,
    adjacency: Dict[str, Dict[str, float]],
    k: int = 3
) -> List[Tuple[str, float]]:
    """Get top k adjacent zones by probability."""
    row = adjacency.get(zone_id, {})
    # Sort by probability, descending
    sorted_neighbors = sorted(row.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_neighbors[:k]


def build_topology_snapshot(
    zones: Dict,  # Dict[str, ZoneMicrostate]
    adjacency: Dict[str, Dict[str, float]],
    cloud_state,  # Cloud instance
    top_k: int = 3
) -> TopologySnapshot:
    """
    Build a complete topology snapshot.

    Args:
        zones: Dict of zone_id → ZoneMicrostate
        adjacency: Adjacency matrix (zone_id → zone_id → probability)
        cloud_state: Cloud instance
        top_k: Number of top neighbors to include per zone

    Returns:
        TopologySnapshot with all zone and Cloud state
    """
    zone_states: List[ZoneDebugState] = []

    for zone_id, zone in zones.items():
        zone_states.append(
            ZoneDebugState(
                zone_id=zone_id,
                qbit_score=getattr(zone, "qbit_aggregate", 0.0),
                resonance=getattr(zone, "resonance", 0.0),
                turbulence=getattr(zone, "turbulence", 0.0),
                top_neighbors=_get_top_neighbors(zone_id, adjacency, top_k),
            )
        )

    # Get Cloud mood as string
    mall_mood = getattr(cloud_state, "mall_mood", None)
    if hasattr(mall_mood, "value"):
        mood_str = mall_mood.value
    else:
        mood_str = str(mall_mood) if mall_mood else "unknown"

    return TopologySnapshot(
        timestamp=time.time(),
        cloud_level=getattr(cloud_state, "cloud_level", 0.0),
        cloud_mood=mood_str,
        bleed_tier=getattr(cloud_state, "current_bleed_tier", 0),
        zones=zone_states,
    )


def log_topology_snapshot_json(
    snapshot: TopologySnapshot,
    fp
) -> None:
    """
    Write one line per snapshot as JSONL.

    Args:
        snapshot: TopologySnapshot to log
        fp: Open file-like object (e.g. log file)
    """
    data = asdict(snapshot)
    fp.write(json.dumps(data) + "\n")
    fp.flush()


def print_topology_summary(
    snapshot: TopologySnapshot,
    max_neighbors: int = 3
) -> None:
    """
    Human-readable console dump of current topology.

    Args:
        snapshot: TopologySnapshot to print
        max_neighbors: Maximum neighbors to show per zone
    """
    print("\n=== TOPOLOGY DEBUG SNAPSHOT ===")
    print(
        f"t={snapshot.timestamp:.0f} | "
        f"cloud={snapshot.cloud_level:.1f} ({snapshot.cloud_mood}) | "
        f"bleed_tier={snapshot.bleed_tier}"
    )

    for z in snapshot.zones:
        print(
            f"\n[ZONE] {z.zone_id} "
            f"| QBIT={z.qbit_score:.2f} "
            f"| resonance={z.resonance:.1f} "
            f"| turb={z.turbulence:.2f}"
        )

        if not z.top_neighbors:
            print("   (no adjacency row)")
            continue

        print("   top neighbors:")
        for i, (nz, p) in enumerate(z.top_neighbors[:max_neighbors], start=1):
            print(f"     {i}. {nz:<18} p={p:.3f}")


def print_adjacency_matrix_ascii(
    adjacency: Dict[str, Dict[str, float]],
    precision: int = 2
) -> None:
    """
    Very simple ASCII matrix for quick visual inspection.

    Args:
        adjacency: Adjacency matrix (zone_id → zone_id → probability)
        precision: Decimal precision for probability values
    """
    zone_ids = sorted(adjacency.keys())
    if not zone_ids:
        print("[adjacency] (empty)")
        return

    # Column headers
    header = "        " + " ".join(f"{z[:6]:>7}" for z in zone_ids)
    print("\n[Adjacency Matrix]")
    print(header)

    # Rows
    for row_z in zone_ids:
        row = adjacency.get(row_z, {})
        line = [f"{row_z[:6]:>7}"]
        for col_z in zone_ids:
            if col_z == row_z:
                line.append("   ----")  # Diagonal (self-connection)
            else:
                p = row.get(col_z, 0.0)
                line.append(f"{p:7.{precision}f}")
        print(" ".join(line))


def calculate_topology_metrics(snapshot: TopologySnapshot) -> Dict:
    """
    Calculate high-level topology metrics.

    Args:
        snapshot: TopologySnapshot

    Returns:
        Dict with metrics:
        - total_qbit: Sum of all zone QBIT scores
        - avg_qbit: Average QBIT score
        - max_qbit_zone: Zone with highest QBIT
        - avg_turbulence: Average turbulence across zones
        - avg_resonance: Average resonance across zones
    """
    if not snapshot.zones:
        return {}

    total_qbit = sum(z.qbit_score for z in snapshot.zones)
    total_turbulence = sum(z.turbulence for z in snapshot.zones)
    total_resonance = sum(z.resonance for z in snapshot.zones)

    max_qbit_zone = max(snapshot.zones, key=lambda z: z.qbit_score)

    return {
        "total_qbit": total_qbit,
        "avg_qbit": total_qbit / len(snapshot.zones),
        "max_qbit_zone": max_qbit_zone.zone_id,
        "max_qbit_value": max_qbit_zone.qbit_score,
        "avg_turbulence": total_turbulence / len(snapshot.zones),
        "avg_resonance": total_resonance / len(snapshot.zones),
        "zone_count": len(snapshot.zones)
    }


def print_topology_metrics(metrics: Dict) -> None:
    """Print topology metrics summary."""
    print("\n=== TOPOLOGY METRICS ===")
    print(f"Total QBIT:       {metrics.get('total_qbit', 0):.1f}")
    print(f"Average QBIT:     {metrics.get('avg_qbit', 0):.2f}")
    print(f"Max QBIT Zone:    {metrics.get('max_qbit_zone', 'N/A')} "
          f"({metrics.get('max_qbit_value', 0):.1f})")
    print(f"Avg Turbulence:   {metrics.get('avg_turbulence', 0):.2f}")
    print(f"Avg Resonance:    {metrics.get('avg_resonance', 0):.2f}")
    print(f"Zone Count:       {metrics.get('zone_count', 0)}")


# ========== MODULE TESTING ==========

if __name__ == "__main__":
    print("=" * 60)
    print("TOPOLOGY DEBUG TOOLS TEST")
    print("=" * 60)

    # Create mock objects for testing
    class MockZone:
        def __init__(self, zone_id, qbit_aggregate, resonance, turbulence):
            self.zone_id = zone_id
            self.qbit_aggregate = qbit_aggregate
            self.resonance = resonance
            self.turbulence = turbulence

    class MockCloud:
        def __init__(self):
            self.cloud_level = 42.5
            self.mall_mood = type('obj', (object,), {'value': 'uneasy'})()
            self.current_bleed_tier = 1

    # Create test data
    zones = {
        "FC-ARCADE": MockZone("FC-ARCADE", 1154.0, 25.0, 5.5),
        "CORRIDOR": MockZone("CORRIDOR", 100.0, 10.0, 2.0),
        "SERVICE_HALL": MockZone("SERVICE_HALL", 300.0, 15.0, 3.5),
    }

    adjacency = {
        "FC-ARCADE": {"CORRIDOR": 0.45, "SERVICE_HALL": 0.55},
        "CORRIDOR": {"FC-ARCADE": 0.30, "SERVICE_HALL": 0.70},
        "SERVICE_HALL": {"FC-ARCADE": 0.40, "CORRIDOR": 0.60},
    }

    cloud = MockCloud()

    # Build snapshot
    print("\nBuilding topology snapshot...")
    snapshot = build_topology_snapshot(zones, adjacency, cloud, top_k=2)

    # Print summary
    print_topology_summary(snapshot, max_neighbors=2)

    # Print ASCII matrix
    print_adjacency_matrix_ascii(adjacency, precision=3)

    # Calculate and print metrics
    metrics = calculate_topology_metrics(snapshot)
    print_topology_metrics(metrics)

    # Test JSONL logging
    print("\n" + "-" * 60)
    print("Testing JSONL logging...")

    import io
    log_buffer = io.StringIO()
    log_topology_snapshot_json(snapshot, log_buffer)

    log_output = log_buffer.getvalue()
    print(f"JSONL output ({len(log_output)} bytes):")
    print(log_output[:200] + "..." if len(log_output) > 200 else log_output)

    # Verify JSON is valid
    log_buffer.seek(0)
    parsed = json.loads(log_buffer.readline())
    print(f"\n✓ JSONL parse successful")
    print(f"  Cloud level: {parsed['cloud_level']}")
    print(f"  Zone count: {len(parsed['zones'])}")

    print("\n✓ Topology debug tools test complete")
