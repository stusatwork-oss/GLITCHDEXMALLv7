from rejected_consensus import MorphFirmware, ScrapPool, record_rejected_consensus
from objects.recycler import RecyclerTrashCan


def test_rejected_consensus_scrap_pipeline():
    scrap_pool = ScrapPool()

    scrap_pool.record_rejection(
        source="dialogue_branch",
        zone_id="Z4_ARCADE",
        conditions={"cloud_min": 60},
        qbit_signature={"power": 40, "charisma": 900},
        reason="player_never_selected",
        tick_recorded=184203,
    )
    scrap_pool.record_rejection(
        source="npc_route",
        zone_id="Z1_CENTRAL_ATRIUM",
        conditions={"route": "token_to_arcade"},
        qbit_signature={"power": 10, "charisma": 25},
        reason="blocked_by_rule",
        tick_recorded=184204,
    )

    recycler = RecyclerTrashCan(zone_id="Z4_ARCADE", cloud_relief=1.0, cooldown_seconds=0.0)
    result = recycler.use(sim_state={}, current_time=0.0, scrap_pool=scrap_pool, harvest_limit=5)

    assert result.success
    assert result.scrap_harvested is not None
    assert len(result.scrap_harvested) == 2
    assert len(scrap_pool) == 0

    firmware = MorphFirmware()
    synthesized = firmware.synthesize(result.scrap_harvested, zone_hint="Z4_ARCADE")

    assert len(synthesized) == 2
    assert {s["output_type"] for s in synthesized} == {"anomaly_event", "voxel_object"}
    assert all(entry["id"].startswith("MORPH_RC_") for entry in synthesized)


def test_record_helper_targets_scrap_pool():
    class DummyWorld:
        def __init__(self) -> None:
            self.scrap_pool = ScrapPool()

    world = DummyWorld()
    record = record_rejected_consensus(
        world,
        source="player_option",
        zone_id="Z5_SERVICE",
        conditions={"guard_check": "failed"},
        qbit_signature={"charisma": 120},
        reason="player_never_selected",
        tick_recorded=1010,
    )

    assert len(world.scrap_pool) == 1
    assert record.id.startswith("RC_")
    assert record.reason == "player_never_selected"
