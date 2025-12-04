"""Perseverance layer contract validation."""

from cloud import RoutingOverride, ZoneMicrostate
from perseverance import tick_perseverance


class DummyWorld:
    def __init__(self, zone):
        self.zones = {zone.zone_id: zone}


def test_tick_perseverance_recovers_zone_state():
    """Cloud pressure decays, QBIT heals, and routing overrides expire."""

    zone = ZoneMicrostate("FC-ARCADE")
    zone.cloud_pressure = 40.0
    zone.qbit_baseline = 100.0
    zone.qbit_aggregate = 50.0
    zone.routing_overrides.append(
        RoutingOverride(
            source_zone="FC-ARCADE",
            target_zone="Z4_FOOD_COURT",
            probability=0.8,
            ttl=2,
            reason="test",
        )
    )

    world = DummyWorld(zone)

    tick_perseverance(world, dt=1)
    tick_perseverance(world, dt=1)

    assert zone.cloud_pressure < 40.0, "Cloud pressure should decay toward calm"
    assert 50.0 < zone.qbit_aggregate < zone.qbit_baseline, "QBIT should lerp toward baseline"
    assert not zone.routing_overrides, "Routing overrides should expire when TTL elapses"
